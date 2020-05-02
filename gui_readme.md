Интерфейс построен на базе Tkinter с использованием asyncio.

## Как запустить

```python
import asyncio
import gui

loop = asyncio.get_event_loop()

messages_queue = asyncio.Queue()
sending_queue = asyncio.Queue()
status_updates_queue = asyncio.Queue()

loop.run_until_complete(gui.draw(messages_queue, sending_queue, status_updates_queue))
```

Управление происходит через очереди [asyncio.Queue](https://docs.python.org/3/library/asyncio-queue.html), они позволяют организовать взаимодействие между корутинами — `gui.draw(...)` и внешним кодом для работы с сокетами. Используются три очереди: `messages_queue`, `sending_queue` и`status_updates_queue`.

## Очереди сообщений

### messages_queue

Из этой очереди интерфейс считывает сообщения, чтобы отобразить их в истории переписки. Каждое сообщение — это строка текста. Добавление нового сообщения выглядит так:

```python3
messages_queue.put_nowait('Иван: Привет всем в этом чатике!')
```

### sending_queue

В эту очередь интерфейс отправляет текст сообщения, напечатанного пользователем программы. Из поля ввода текст попадает в очередь сообщений, получить его можно так:

```python3
msg = await sending_queue.get()
print(msg)  # Иван: Привет всем в этом чатике!
```

### status_updates_queue

Из этой очереди интерфейс считывает сообщения об изменении статуса, чтобы затем отобразить их в интерфейсе. Поддерживается несколько видов сообщений:

```python3
gui.ReadConnectionStateChanged.INITIATED  # устанавливаем соединение
gui.ReadConnectionStateChanged.ESTABLISHED  # соединение установлено
gui.ReadConnectionStateChanged.CLOSED  # соединение закрыто
```

При изменении состояния сетевого интерфейса сообщить об этом можно так:

```python3
status_updates_queue.put_nowait(gui.ReadConnectionStateChanged.INITIATED)
```

Аналогичных три статуса есть для `SendingConnectionStateChanged`.

Дополнительно есть тип сообщений `NicknameReceived`, отправьте его когда узнаете имя пользователя в чатруме, оно отобразится в интейрфейсе:

```python3
event = gui.NicknameReceived('Василий Пупкин')
status_updates_queue.put_nowait(event)
```
