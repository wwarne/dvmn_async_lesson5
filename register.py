import asyncio
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

import aiofiles
from anyio import create_task_group

import defaults
from common_tools import connect
from exceptions import MinechatException
from gui import TkAppClosed, update_tk, SendingConnectionStateChanged
from write_client import register


def start_register(
        address_field: tk.Entry,
        nickname_field: tk.Entry,
        events_queue: asyncio.Queue,
) -> None:
    """Send an event message to start registration."""
    server_address = address_field.get()
    nickname = nickname_field.get()
    events_queue.put_nowait((server_address, nickname))


async def show_log(
        log_queue: asyncio.Queue,
        log_text_area: ScrolledText,
) -> None:
    """Show log messages in the GUI."""
    while True:
        msg = await log_queue.get()
        if isinstance(msg, str):
            msg, level = msg, 'INFO'
        else:
            msg, level = msg
        log_text_area.configure(state='normal')
        log_text_area.insert(tk.END, msg + '\n', level)
        log_text_area.configure(state='disabled')
        # Autoscroll to the bottom
        log_text_area.yview(tk.END)


async def write_token_to_file(
        token: str,
        filepath: str
) -> bool:
    """Writes token into a file and returns a success status."""
    try:
        async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
            await f.write(token)
            return True
    except (PermissionError, IsADirectoryError):
        return False


async def watch_register(
        events_queue: asyncio.Queue,
        log_queue: asyncio.Queue,
        result_token_field: tk.Entry,
):
    """Validate user's input and register user on a server."""
    while True:
        server_address, nickname = await events_queue.get()
        nickname = nickname.strip()
        try:
            host, port = server_address.split(':')
            port = int(port)
        except ValueError:
            await log_queue.put(('Проверьте, что адрес сервера указан в формате host:port', 'ERROR'))
            continue
        if not nickname:
            await log_queue.put(('Пожалуйста, укажите свой ник.', 'ERROR'))
            continue
        await log_queue.put(f'Начинаем процесс регистрации. {nickname} на {host}:{port}')
        # NOTE - to reuse the "connect" method we need to provide it with status queue and status enum.
        dummy_queue = asyncio.Queue()
        try:
            async with connect(host, port, dummy_queue, SendingConnectionStateChanged) as (reader, writer):
                result = await register(
                    reader=reader,
                    writer=writer,
                    nickname=nickname,
                )
        except (ConnectionError, UnicodeDecodeError, MinechatException) as e:
            await log_queue.put(('Не удалось зарегистрироваться. Пожалуйста, попробуйте позднее.', 'ERROR'))
        else:
            result_token_field.delete(0, tk.END)
            result_token_field.insert(0, result['account_hash'])
            to_file_status = await write_token_to_file(result['account_hash'], defaults.TOKEN_PATH)
            if to_file_status:
                await log_queue.put((f'Успешная регистрация. Токен сохранён в файле {defaults.TOKEN_PATH}', 'SUCCESS'))
            else:
                await log_queue.put(('Успешная регистрация. Не забудьте сохранить токен и использовать его при запуске чата.', 'SUCCESS'))

async def draw(
        events_queue: asyncio.Queue,
        log_queue: asyncio.Queue,
) -> None:
    """Draw a GUI."""
    root = tk.Tk()
    root.title('Регистрация в чате Майнкрафта')

    root_frame = tk.Frame()
    root_frame.pack(fill='both', expand=True)

    address_frame = tk.Frame(root_frame)
    # server address and port field
    address_label = tk.Label(address_frame, text='Адрес сервера: ', width=20, pady=10)
    address_field = tk.Entry(address_frame, width=40)
    address_field.delete(0, tk.END)
    address_field.insert(0, f'{defaults.WRITE_HOST}:{defaults.WRITE_PORT}')
    address_frame.pack()
    address_label.pack(side=tk.LEFT)
    address_field.pack(expand=1)

    # nickname field
    nickname_frame = tk.Frame(root_frame)
    nickname_label = tk.Label(nickname_frame, text='Введите ник: ', width=20, pady=10)
    nickname_field = tk.Entry(nickname_frame, width=40)
    nickname_frame.pack()
    nickname_label.pack(side=tk.LEFT)
    nickname_field.pack(expand=1)

    # register button
    reg_button_frame = tk.Frame(root_frame)
    reg_button = tk.Button(reg_button_frame, text='Зарегистрироваться')
    reg_button_frame.pack()
    reg_button.pack()

    # resulting token field
    result_token_frame = tk.Frame(root_frame)
    result_token_label = tk.Label(result_token_frame, text='Ваш токен: ', width=20, pady=10)
    result_token_field = tk.Entry(result_token_frame, width=40)
    result_token_frame.pack()
    result_token_label.pack(side=tk.LEFT)
    result_token_field.pack(expand=1)

    # log messages area
    log_frame = tk.Frame(root_frame)
    log_text_area = ScrolledText(log_frame, state='disabled', height=12)
    log_text_area.configure(font='TkFixedFont')
    log_text_area.tag_configure('INFO', foreground='gray')
    log_text_area.tag_configure('ERROR', foreground='orange', background='red')
    log_text_area.tag_configure('SUCCESS', foreground='orange', background='green')
    log_frame.pack()
    log_text_area.pack(expand=1)

    reg_button['command'] = lambda: start_register(address_field, nickname_field, events_queue)

    async with create_task_group() as tg:
        await tg.spawn(update_tk, root)
        await tg.spawn(watch_register, events_queue, log_queue, result_token_field)
        await tg.spawn(show_log, log_queue, log_text_area)


async def main() -> None:
    """Starting point to run register programm."""
    events_queue = asyncio.Queue()
    log_queue = asyncio.Queue()
    try:
        async with create_task_group() as nursery:
            await nursery.spawn(draw, events_queue, log_queue)
    except TkAppClosed:
        pass


if __name__ == '__main__':
    asyncio.run(main())
