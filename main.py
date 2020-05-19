import asyncio
import logging.config
from tkinter import messagebox

from anyio import create_task_group

import gui
from exceptions import MinechatException
from gui import TkAppClosed
from history_client import restore_history, save_history
from settings import read_settings, get_logging_settings
from watchdog import handle_connection


async def run_chat_internals(
        reader_host: str,
        reader_port: int,
        writer_host: str,
        writer_port: int,
        access_token: str,
        history_path: str,
) -> None:
    """Runs all coroutines."""
    messages_queue = asyncio.Queue()
    sending_queue = asyncio.Queue()
    status_updates_queue = asyncio.Queue()
    history_queue = asyncio.Queue()
    watchdog_queue = asyncio.Queue()
    async with create_task_group() as tg:
        await tg.spawn(gui.draw,
                       messages_queue,
                       sending_queue,
                       status_updates_queue,
                       )
        await restore_history(
            path=history_path,
            messages_queue=messages_queue,
        )
        await tg.spawn(save_history,
                       history_path,
                       history_queue,
                       )
        await tg.spawn(handle_connection,
                       reader_host,
                       reader_port,
                       writer_host,
                       writer_port,
                       access_token,
                       messages_queue,
                       sending_queue,
                       history_queue,
                       status_updates_queue,
                       watchdog_queue,
                       )


def run_chat() -> None:
    """Entry point to initialize and start the application."""
    total_settings = read_settings()
    logger_dict_config = get_logging_settings(total_settings['loglevel'])
    logging.config.dictConfig(logger_dict_config)

    try:
        asyncio.run(run_chat_internals(
            reader_host=total_settings.read_host,
            reader_port=total_settings.read_port,
            writer_host=total_settings.write_host,
            writer_port=total_settings.write_port,
            access_token=total_settings.token,
            history_path=total_settings.history_path,
        ))
    except MinechatException as e:
        messagebox.showinfo(title=e.title, message=e.message)
    except (KeyboardInterrupt, TkAppClosed):
        pass


if __name__ == '__main__':
    run_chat()
