import asyncio
import logging
import socket

import aionursery
import async_timeout

from nursery_helper import create_handy_nursery
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
            watchdog_logger.info(f'{event}')


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
                async with create_handy_nursery() as nursery:
                    nursery.start_soon(
                        read_messages(
                            host=reader_host,
                            port=reader_port,
                            status_update_queue=status_update_queue,
                            messages_queue=messages_queue,
                            history_queue=history_queue,
                            watchdog_queue=watchdog_queue,
                        )
                    )
                    nursery.start_soon(
                        send_messages(
                            host=writer_host,
                            port=writer_port,
                            access_token=access_token,
                            status_update_queue=status_update_queue,
                            sending_queue=sending_queue,
                            watchdog_queue=watchdog_queue,
                        )
                    )
                    nursery.start_soon(
                        watch_for_connection(
                            watchdog_queue=watchdog_queue,
                            timeout=2,
                        )
                    )
            except socket.gaierror:
                raise ConnectionError
            except aionursery.MultiError as multi_e:
                for error in multi_e.exceptions:
                    if isinstance(error, (socket.gaierror, ConnectionError)):
                        raise ConnectionError
                raise
        except ConnectionError:
            logging.info(f'Connection error, reconnect in {reconnect_delay} sec.')
            await asyncio.sleep(reconnect_delay)
        else:
            return
