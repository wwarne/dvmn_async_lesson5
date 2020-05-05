import pytest

@pytest.mark.parametrize('arg_name, arg_value', [
    ('read-host', 'localhost'),
    ('read-port', '5050'),
    ('history-path', '/tmp/bad.txt'),
    ('write-host', 'localhost'),
    ('write-port', '5060'),
    ('token', '123-321'),
    ('loglevel', 'DEBUG'),
])
def test_command_line_arg_names(arg_parser, arg_name, arg_value):
    """Check if every command line argument is accepted."""
    if not arg_value:
        param = f'--{arg_name}'
    else:
        param = f'--{arg_name}={arg_value}'
    arg_parser.parse_args([param])


def test_casting_inputs(arg_parser):
    settings = arg_parser.parse_args(['--read-port=5050', '--write-port=6060'])
    assert settings.read_port == 5050
    assert settings.write_port == 6060


@pytest.mark.parametrize('int_param_name', [
    'read-port',
    'write-port',
])
def test_errors_with_wrong_ports(arg_parser, int_param_name, capsys):
    with pytest.raises(SystemExit):
        arg_parser.parse_args([f'--{int_param_name}=non-int'])
    out, err = capsys.readouterr()
    assert 'invalid int value' in err
