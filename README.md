# Lesson 05 - Minecraft undeground chat

![][usa_flag] [For english version press here](../README_EN.md)

Клиент чата майнкрафтеров с графическим интерфейсом.

Некоторые возможности:

* Графический интерфейс для регистрации нового пользователя.
* История сообщений чата сохраняется в файле.


# Требования для запуска

* Рекомендуемая версия интерпритатора - python 3.7+
* [Poetry](https://poetry.eustace.io/) для управления зависимостями. 

# Как пользоваться


## Установка зависимостей

```bash
$ poetry install
```
### Запуск команд с помощью poetry

Способо 1: Активировать виртуальное окружение командой ```poetry shell``` и далее запускать команды.

Способ 2: Запускать каждую команду как ```poetry run команда, которую хотите запустить```.

Как удобнее - решать вам.

### Регистрация в чате

Перед использованием чата необходимо получить токен доступа, для этого запустите

```bash
python register.py
```

Полученный токен будет сохранён в файле `my-token.txt` или вы можете скопировать его и передать в программу в качестве параметра.


![Successfull registration][registration]


## Работа с чатом

Чтобы запустить клиент чата введите команду ```python main.py```. 


### Как передать ваш токен для аутентификации

Токен можно передать разными способами:

* Сохранить его в файле `my-token.txt`, при запуске он будет прочитан оттуда.
* Сохранить его в переменную окружения `MINECHAT_TOKEN`
* Передать как параметр командной строки ```python manage.py --token=```

Переменная окружения имеет более высокий приоритет, чем файл ```my-token.txt```, 
а параметр командной строки - более высокий приоритет, чем переменная окружения.


### Настройки чата

Вы можете передавать параметры чата как переменные окружения или как параметры командной строки.
Параметры командной строки имеют более высокий приоритет.


| env parameter |  command-line parameter | default value |  description  |
|---|---|---|---|
| MINECHAT_READ_HOST  | --read_host  | minechat.dvmn.org  | Адрес сервера чата для чтения (ip или доменное имя)  |
| MINECHAT_READ_PORT  | --read_port  | 5000  | Порт чата для чтения сообщений |
| MINECHAT_WRITE_HOST  | --write_host  | minechat.dvmn.org  | Адрес сервера чата для записи (ip или доменное имя)  |
| MINECHAT_WRITE_PORT  | --write_port  | 5050  | Порт чата для отправки сообщений |
| MINECHAT_HISTORY_PATH  | --history_path  | minechat.history  | Путь к файлу с историей чата  |
| MINECHAT_TOKEN  | --token  |   | Токен для аутентификации |
| MINECHAT_LOGLEVEL  | --loglevel  | INFO  | Уровень детальности логов |


![Chat client is running][chat_window]


# Цели проекта

Код написан в образовательных целях.


[registration]: readme_pics/registration.png "Registration window"
[chat_window]: readme_pics/chat.png "Chat in work"
[usa_flag]: readme_pics/usa_icon.png "USA flag"