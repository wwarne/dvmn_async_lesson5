import asyncio

from common_tools import connect, read_line_from_chat
from gui import ReadConnectionStateChanged


async def read_messages(
        host: str,
        port: int,
        status_update_queue: asyncio.Queue,
        messages_queue: asyncio.Queue,
        history_queue: asyncio.Queue,
        watchdog_queue: asyncio.Queue,
        timeout: float = 1,
) -> None:
    """Establish connection and read messages from a chat."""
    async with connect(
        host=host,
        port=port,
        status_update_queue=status_update_queue,
        gui_state_class=ReadConnectionStateChanged,
        timeout=timeout,
    ) as (reader, writer):
        while True:
            new_message = await read_line_from_chat(reader)
            if not new_message:
                # Got an empty message. Usually it happens because of connection problems.
                break
            await watchdog_queue.put('New message in chat')
            await messages_queue.put(new_message)
            await history_queue.put(new_message)
