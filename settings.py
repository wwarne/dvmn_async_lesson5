import argparse
import os
from typing import Optional, List, Dict, Any

import configargparse

import defaults


def create_parser() -> argparse.ArgumentParser:
    """Creates a parser to process command line arguments."""
    parser = configargparse.ArgParser('Minechat chat client', default_config_files=['minechat.conf'])
    parser.add_argument('--loglevel', type=str, choices=defaults.POSSIBLE_LOGLEVELS, help='Logging level', required=False, env_var='MINECHAT_LOGLEVEL')
    group_reader = parser.add_argument_group('Chat reader settings')
    group_reader.add_argument('--read-host', type=str, help='Chat address', env_var='MINECHAT_READ_HOST')
    group_reader.add_argument('--read-port', type=int, help='Chat port', env_var='MINECHAT_READ_PORT')
    group_reader.add_argument('--history-path', metavar='FILEPATH', type=str, help='Path to a history file', env_var='MINECHAT_HISTORY_PATH')
    group_writer = parser.add_argument_group('Chat sender settings')
    group_writer.add_argument('--write-host', type=str, help='Chat write address', env_var='MINECHAT_WRITE_HOST')
    group_writer.add_argument('--write-port', type=int, help='Chat write port', env_var='MINECHAT_WRITE_PORT')
    group_writer.add_argument('--token', type=str, help='Authentication token', env_var='MINECHAT_TOKEN')
    return parser


def read_token_from_file(filepath: str) -> Optional[str]:
    """
    Reads a token saved in a file.

    :param filepath: path to a file
    :return: token or None
    """
    if os.path.isfile(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.readline()
    return None


def read_settings(
        parser: Optional[argparse.ArgumentParser] = None,
        cmd_params: Optional[List[str]] = None,
) -> argparse.Namespace:
    """
    Combine all the settings (token file, defaults, command-line params, env variables).

    Environmental variables have priority over defaults
    Command line values have priority over environmental variables.
    """
    if not parser:
        parser = create_parser()
    settings = parser.parse_args(args=cmd_params)
    settings.token = settings.token or read_token_from_file(defaults.TOKEN_PATH)
    return settings


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
