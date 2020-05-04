import asyncio
import logging.config
from tkinter import messagebox

import gui
from exceptions import MinechatException
from gui import TkAppClosed
from history_client import history_restore, history_save
from nursery_helper import create_handy_nursery
from settings import read_settings, get_logging_settings
from watchdog import handle_connection


async def run_chat_internals(
        reader_host: str,
        reader_port: int,
        writer_host: str,
        writer_port: int,
        access_token: str,
        history_path: str,
):
    """Runs all coroutines."""
    messages_queue = asyncio.Queue()
    sending_queue = asyncio.Queue()
    status_updates_queue = asyncio.Queue()
    history_queue = asyncio.Queue()
    watchdog_queue = asyncio.Queue()
    async with create_handy_nursery() as nursery:
        nursery.start_soon(
            gui.draw(
                messages_queue=messages_queue,
                sending_queue=sending_queue,
                status_updates_queue=status_updates_queue,
            )
        )
        await history_restore(
            path=history_path,
            messages_queue=messages_queue,
        )
        nursery.start_soon(
            history_save(
                path=history_path,
                history_queue=history_queue,
            )
        )
        nursery.start_soon(
            handle_connection(
                reader_host=reader_host,
                reader_port=reader_port,
                writer_host=writer_host,
                writer_port=writer_port,
                access_token=access_token,
                messages_queue=messages_queue,
                sending_queue=sending_queue,
                history_queue=history_queue,
                status_update_queue=status_updates_queue,
                watchdog_queue=watchdog_queue,
            )
        )


def run_chat() -> None:
    """Entry point to setup and start the application."""
    total_settings = read_settings()
    logger_dict_config = get_logging_settings(total_settings['loglevel'])
    logging.config.dictConfig(logger_dict_config)

    try:
        asyncio.run(run_chat_internals(
            reader_host=total_settings['read_host'],
            reader_port=total_settings['read_port'],
            writer_host=total_settings['write_host'],
            writer_port=total_settings['write_port'],
            access_token=total_settings['token'],
            history_path=total_settings['history_path'],
        ))
    except MinechatException as e:
        messagebox.showinfo(title=e.title, message=e.message)
    except (KeyboardInterrupt, TkAppClosed):
        pass


if __name__ == '__main__':
    run_chat()
