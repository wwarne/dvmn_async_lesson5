import asyncio
import json
import logging
from asyncio.streams import StreamReader, StreamWriter
from typing import Dict

from anyio import create_task_group

import gui
from common_tools import connect, write_line_to_chat, read_line_from_chat
from exceptions import InvalidToken, UnknownError, MinechatException


async def authenticate(
        access_token: str,
        reader: StreamReader,
        writer: StreamWriter,
        watchdog_queue: asyncio.Queue
) -> Dict[str, str]:
    """Authenticate user by token."""
    await read_line_from_chat(reader)
    await watchdog_queue.put('Greetings before authentication')
    await write_line_to_chat(writer, access_token)
    response = await read_line_from_chat(reader)
    try:
        account_info = json.loads(response)
    except json.JSONDecodeError:
        raise UnknownError('Не удалось обработать ответ сервера')
    else:
        if account_info is None:
            raise InvalidToken('Неверный токен', 'Проверьте токен, сервер его не узнал')
        await watchdog_queue.put('Authenticated')
        return account_info


async def register(
        reader: StreamReader,
        writer: StreamWriter,
        nickname: str,
) -> None:
    """New user registration."""
    await read_line_from_chat(reader)
    await write_line_to_chat(writer, '')  # say 'we don't have a token'
    await read_line_from_chat(reader)  # ask_for_nickname
    await write_line_to_chat(writer, nickname)
    response_content = await read_line_from_chat(reader)
    if not response_content:
        raise MinechatException('Ошибка при регистрации, попробуйте позднее.')
    try:
        response = json.loads(response_content)
    except json.decoder.JSONDecodeError:
        raise MinechatException('Сервер ответил не в json.')
    return response


async def send_user_messages(
        writer: StreamWriter,
        messages_queue: asyncio.Queue,
        watchdog_queue: asyncio.Queue
) -> None:
    """Reads messages from queue and send them to server."""
    while True:
        message = await messages_queue.get()
        logging.debug(f'Пользователь написал {message}')
        await write_line_to_chat(writer, message)
        # message doesn't appear in the chat if only one `\n` used
        await write_line_to_chat(writer, '')
        await watchdog_queue.put('Message has been sent')


async def send_healthcheck_messages(
        writer: StreamWriter,
        interval: float = 1,
) -> None:
    """Send healthcheck messages (pings) to the server."""
    while True:
        writer.write(b'\n')
        await writer.drain()
        await asyncio.sleep(interval)


async def read_healthcheck_messages(
        reader: StreamReader,
        watchdog_queue: asyncio.Queue,
) -> None:
    """Reads server responses to healthcheck messages."""
    while True:
        new_line = await reader.readline()
        # note - readline() returns an empty string hundreds times per second then connection to server breaks.
        # sleep here is to prevent eventloop blocking and 100% cpu load.
        if new_line == b'':
            await asyncio.sleep(0)
            continue
        await watchdog_queue.put('Healthcheck message')


async def send_messages(
        host: str,
        port: int,
        access_token: str,
        status_update_queue: asyncio.Queue,
        sending_queue: asyncio.Queue,
        watchdog_queue: asyncio.Queue,
) -> None:
    """Send messages to minechat."""
    async with connect(
        host=host,
        port=port,
        status_update_queue=status_update_queue,
        gui_state_class=gui.SendingConnectionStateChanged,
        timeout=1,
    ) as (reader, writer):
        account_info = await authenticate(
            access_token,
            reader,
            writer,
            watchdog_queue,
        )
        await status_update_queue.put(gui.NicknameReceived(account_info['nickname']))
        async with create_task_group() as tg:
            await tg.spawn(send_user_messages, writer, sending_queue, watchdog_queue)
            await tg.spawn(send_healthcheck_messages, writer, 1)
            await tg.spawn(read_healthcheck_messages, reader, watchdog_queue)
