import argparse
import os
from typing import Optional, List, Union, Dict, Any

import defaults


def create_parser() -> argparse.ArgumentParser:
    """Creates a parser to process command line arguments."""
    parser = argparse.ArgumentParser('Minechat chat client')
    parser.add_argument('--loglevel', type=str, choices=('DEBUG', 'INFO', 'WARNING', 'ERROR'), help='Logging level',
                        required=False)
    group_reader = parser.add_argument_group('Chat reader settings')
    group_reader.add_argument('--read-host', type=str, help='Chat address')
    group_reader.add_argument('--read-port', type=int, help='Chat port')
    group_reader.add_argument('--history-path', metavar='FILEPATH', type=str, help='Path to a history file')
    group_writer = parser.add_argument_group('Chat sender settings')
    group_writer.add_argument('--write-host', type=str, help='Chat write address')
    group_writer.add_argument('--write-port', type=int, help='Chat write port')
    group_writer.add_argument('--token', type=str, help='Authentication toklen')
    return parser


def read_from_parser(
        parser_obj: argparse.ArgumentParser,
        cmd_params: Optional[List[str]] = None
) -> Dict[str, Union[str, int]]:
    """
    Read chat settings from command line arguments.

    :param parser_obj: Argument parser
    :param cmd_params: used for simpler testing. If None - argparser uses sys.argv[1:]
    :return: program settings what was set (not null)
    """
    parsed_from_args = parser_obj.parse_args(args=cmd_params)
    settings_from_args = {
        'read_host': parsed_from_args.read_host,
        'read_port': parsed_from_args.read_port,
        'history_path': parsed_from_args.history_path,
        'write_host': parsed_from_args.write_host,
        'write_port': parsed_from_args.write_port,
        'token': parsed_from_args.token,
        'loglevel': parsed_from_args.loglevel,
    }
    return {k: v for k, v in settings_from_args.items() if v is not None}


def read_from_environment() -> Dict[str, Union[str, int]]:
    """
    Read chat settings from environmental variables.
    :return: program settings what was set (not null)
    """
    read_port = os.getenv('MINECHAT_READ_PORT')
    write_port = os.getenv('MINECHAT_WRITE_PORT')
    # Note - I don't throw exception here because port env variables can be overwritten
    # by command-line arguments and be OK
    try:
        read_port = int(read_port)
    except (TypeError, ValueError):
        read_port = None
    try:
        write_port = int(write_port)
    except (TypeError, ValueError):
        write_port = None
    settings_from_env = {
        'read_host': os.getenv('MINECHAT_READ_HOST'),
        'read_port': read_port,
        'history_path': os.getenv('MINECHAT_HISTORY_PATH'),
        'write_host': os.getenv('MINECHAT_WRITE_HOST'),
        'write_port': write_port,
        'token': os.getenv('MINECHAT_TOKEN'),
        'loglevel': os.getenv('MINECHAT_LOGLEVEL'),
    }
    return {k: v for k, v in settings_from_env.items() if v is not None}

def read_token_from_file(filepath: str) -> Optional[str]:
    if os.path.isfile(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.readline()
    return None


def read_settings(
        parser: Optional[argparse.ArgumentParser] = None,
        cmd_params: Optional[List[str]] = None,
) -> Dict[str, Union[str, int]]:
    """
    Combine all the settings (token file, defaults, command-line params, env variables).

    Environmental variables have priority over defaults
    Command line values have priority over environmental variables.
    """
    if not parser:
        parser = create_parser()
    from_args = read_from_parser(parser, cmd_params)
    from_env = read_from_environment()
    default_args = {
        'token': read_token_from_file(defaults.TOKEN_PATH),
        'read_host': defaults.READ_HOST,
        'read_port': defaults.READ_PORT,
        'history_path': defaults.HISTORY_PATH,
        'write_host': defaults.WRITE_HOST,
        'write_port': defaults.WRITE_PORT,
        'loglevel': defaults.LOGLEVEL,
    }
    return {
        **default_args,
        **from_env,
        **from_args,
    }

def get_logging_settings(logging_level: str) -> Dict[str, Any]:
    """
    Prepare settings for logging module.

    level can be CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
    """
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'watchdog': {
                'format': '[%(created)d] %(message)s',
            },
        },
        'handlers': {
            'watchdog': {
                'formatter': 'watchdog',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            '': {
                'level': logging_level,
            },
            'watchdog': {
                'level': logging_level,
                'handlers': ['watchdog'],
                'propagate': False,
            },
        },
    }
