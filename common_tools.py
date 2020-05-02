import contextlib
from typing import AsyncGenerator, Tuple, TypeVar, Type

import logging
import async_timeout
import asyncio
from asyncio.streams import StreamReader, StreamWriter
from gui import (
    ReadConnectionStateChanged,
    SendingConnectionStateChanged,
    NicknameReceived,
)


def sanitize_message(message: str) -> str:
    """
    Clears message fro, the new line symbols.

    New line symbol means an end of the message as stated in
    the chat protocol specifications.
    """
    cleared = message.replace('\r', '').replace('\n', ' ').strip()
    return f'{cleared}\n'


async def read_line_from_chat(reader: StreamReader) -> str:
    """Grabs bytes string from connection and decode it into text."""
    chat_data = await reader.readline()
    try:
        return chat_data.decode(encoding='utf-8').strip()
    except (SyntaxError, UnicodeDecodeError):
        logging.error('Got message that can\'t be decoded', exc_info=True)
        return ''


async def write_line_to_chat(writer: StreamWriter, message: str):
    """Encode message and send it to the server."""
    message = sanitize_message(message).encode(encoding='utf-8')
    writer.write(message)
    await writer.drain()

StateChangeEnum = TypeVar('StateChangeEnum', ReadConnectionStateChanged, SendingConnectionStateChanged)

@contextlib.asynccontextmanager
async def connect(
        host: str,
        port: int,
        status_update_queue: asyncio.Queue,
        gui_state_class: Type[StateChangeEnum],
        timeout: float = 1.0,
) -> AsyncGenerator[Tuple[StreamReader, StreamWriter], None]:
    """Create connection and send status into queue."""
    await status_update_queue.put(gui_state_class.INITIATED)
    try:
        async with async_timeout.timeout(timeout):
            reader, writer = await asyncio.open_connection(host, port)
    except (asyncio.TimeoutError, ConnectionRefusedError):
        raise ConnectionError
    await status_update_queue.put(gui_state_class.ESTABLISHED)
    try:
        yield reader, writer
    finally:
        writer.close()
        await writer.wait_closed()
        await status_update_queue.put(gui_state_class.CLOSED)
        await status_update_queue.put(NicknameReceived('неизвестно'))
