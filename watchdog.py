import asyncio
import logging
import socket

import async_timeout
from anyio import create_task_group
from anyio.exceptions import ExceptionGroup

from read_client import read_messages
from write_client import send_messages

watchdog_logger = logging.getLogger('watchdog')

async def watch_for_connection(
        watchdog_queue: asyncio.Queue,
        timeout: float = 2,
):
    """Raises exception if it seems connection is down."""
    while True:
        try:
            async with async_timeout.timeout(timeout) as cm:
                event = await watchdog_queue.get()
        except asyncio.TimeoutError:
            watchdog_logger.info(f'{timeout} s timeout is elapsed.')
            raise ConnectionError
        else:
            watchdog_logger.info(f'Connection is alive. {event}')


async def handle_connection(
        reader_host: str,
        reader_port: int,
        writer_host: str,
        writer_port: int,
        access_token: str,
        messages_queue: asyncio.Queue,
        sending_queue: asyncio.Queue,
        history_queue: asyncio.Queue,
        status_update_queue: asyncio.Queue,
        watchdog_queue: asyncio.Queue,
        reconnect_delay: float = 1.0,
) -> None:
    """Manages all the connections."""
    while True:
        try:
            try:
                async with create_task_group() as nursery:
                    await nursery.spawn(read_messages,
                                        reader_host,
                                        reader_port,
                                        status_update_queue,
                                        messages_queue,
                                        history_queue,
                                        watchdog_queue
                                        )
                    await nursery.spawn(send_messages,
                                        writer_host,
                                        writer_port,
                                        access_token,
                                        status_update_queue,
                                        sending_queue,
                                        watchdog_queue,
                                        )
                    await nursery.spawn(watch_for_connection,
                                        watchdog_queue,
                                        2,
                                        )
            except socket.gaierror:
                raise ConnectionError
            except ExceptionGroup as multi_e:
                for error in multi_e.exceptions:
                    if isinstance(error, (socket.gaierror, ConnectionError)):
                        raise ConnectionError
                raise
        except ConnectionError:
            watchdog_logger.info(f'Connection error, reconnect in {reconnect_delay} sec.')
            await asyncio.sleep(reconnect_delay)
        else:
            return
