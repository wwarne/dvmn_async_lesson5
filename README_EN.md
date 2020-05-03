# Lesson 05 - Minecraft undeground chat

![][russia_flag] [Для версии на русском нажмите здесь](../README.md)

Chat client with graphical interface for a secret chat of professional players.

Some features:

* GUI for register a new user in a chat.
* Saving chat history into a file


# Requirements

* python 3.7+ is recommended
* [Poetry](https://poetry.eustace.io/) for dependency management. 

# How to use


## Install dependencies

```bash
$ poetry install
```
### Run chat command

To run commands you can either activate virtual environment via running ```poetry shell```
or run every command as ```poetry run command_to_run```. It's up to you. 


### Registration in a chat

Before using a chat you need a token. To register an account just run 

```bash
python register.py
```

Your token will be saved in a `my-token.txt` file or you can copy it and pass via chat client parameters.


![Successfull registration][registration]


## Working with chat

To run the chat use ```python main.py```. 


### Passing your chat token

You can provide your chat token with many different ways:

* Save it in file `my-token.txt`
* Save it into env variable `MINECHAT_TOKEN`
* Pass it as a command-line parameter ```python manage.py --token=```

Env variable have priority over file, and command line parameter have the highest priority of all.


### Chat settings

You can pass settings as environmental variables or as command line parameters.
If you pass some parameter with both methods - command line parameter be used.


| env parameter |  command-line parameter | default value |  description  |
|---|---|---|---|
| MINECHAT_READ_HOST  | --read_host  | minechat.dvmn.org  | Chat address for reading (ip or host name)  |
| MINECHAT_READ_PORT  | --read_port  | 5000  | Port number of read server |
| MINECHAT_WRITE_HOST  | --write_host  | minechat.dvmn.org  | Chat address for writing (ip or host name)  |
| MINECHAT_WRITE_PORT  | --write_port  | 5050  | Port number of a write server |
| MINECHAT_HISTORY_PATH  | --history_path  | minechat.history  | Path to a file with chat history  |
| MINECHAT_TOKEN  | --token  |   | Token to authenticate in chat |
| MINECHAT_LOGLEVEL  | --loglevel  | INFO  | Level of logging |


### Using chat

```bash
$ python main.py
```

![Chat client is running][chat_window]


# Project Goals

The code is written for educational purposes.


[registration]: readme_pics/registration.png "Registration window"
[chat_window]: readme_pics/chat.png "Chat in work"
[russia_flag]: readme_pics/russia_icon.png.png "Russia flag"