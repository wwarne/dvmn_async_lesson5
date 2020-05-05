import asyncio

import aiofiles

from exceptions import MinechatException


async def history_restore(
        path: str,
        messages_queue: asyncio.Queue,
) -> None:
    """Restore messages from history file."""
    try:
        async with aiofiles.open(path, mode='r', encoding='utf-8') as f:
            async for message in f:
                await messages_queue.put(message.strip())
    except (FileNotFoundError, PermissionError):
        pass


async def history_save(
        path: str,
        history_queue: asyncio.Queue,
) -> None:
    """Dumps incoming messages into a file."""
    try:
        async with aiofiles.open(path, mode='a', encoding='utf-8') as f:
            while True:
                message = await history_queue.get()
                await f.write(f'{message}\n')
    except PermissionError:
        raise MinechatException(
            title='Не удаётся открыть файл',
            message=f'Не могу открыть файл {path} для записи истории.',
        )
