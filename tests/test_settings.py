from settings import read_settings

def test_parse_args_has_called(mocker):
    mocked_parser = mocker.Mock()
    read_settings(mocked_parser, cmd_params=['example'])
    assert mocked_parser.parse_args.called is True
    assert mocked_parser.parse_args.call_args[1]['args'] == ['example']


def test_read_env_has_called(mocker):
    read_env = mocker.patch('settings.read_from_environment')
    mocked_parser = mocker.Mock()
    read_settings(mocked_parser, cmd_params=[])
    assert read_env.called is True

def test_args_have_priority_over_env(monkeypatch, arg_parser):
    monkeypatch.setenv('MINECHAT_READ_HOST', 'example.com')
    settings = read_settings(arg_parser, cmd_params=['--read-host=test'])
    assert settings['read_host'] == 'test'


def test_settings_key_names(arg_parser):
    settings = read_settings(arg_parser, cmd_params=[])
    assert set(settings.keys()) == {
        'history_path',
        'loglevel',
        'read_host',
        'read_port',
        'token',
        'write_host',
        'write_port',
    }

