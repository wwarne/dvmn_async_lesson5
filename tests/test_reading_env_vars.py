import pytest

from settings import create_parser


class TestReadEnv:
    def test_read_host(self, monkeypatch):
        monkeypatch.setenv('MINECHAT_READ_HOST', 'example.com')
        parser = create_parser()
        settings = parser.parse_args(args=[])
        assert settings.read_host == 'example.com'

    def test_read_port(self, monkeypatch):
        monkeypatch.setenv('MINECHAT_READ_PORT', '5050')
        parser = create_parser()
        settings = parser.parse_args(args=[])
        assert settings.read_port == 5050

    def test_bad_read_port(self, monkeypatch):
        monkeypatch.setenv('MINECHAT_READ_PORT', 'not-integer')
        parser = create_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(args=[])


    def test_write_host(self, monkeypatch):
        monkeypatch.setenv('MINECHAT_WRITE_HOST', 'example.com')
        parser = create_parser()
        settings = parser.parse_args(args=[])
        assert settings.write_host == 'example.com'

    def test_write_port(self, monkeypatch):
        monkeypatch.setenv('MINECHAT_WRITE_PORT', '5080')
        parser = create_parser()
        settings = parser.parse_args(args=[])
        assert settings.write_port == 5080

    def test_bad_write_port(self, monkeypatch):
        monkeypatch.setenv('MINECHAT_WRITE_PORT', 'not-integer')
        with pytest.raises(SystemExit):
            parser = create_parser()
            parser.parse_args(args=[])

    def test_history_path(self, monkeypatch):
        monkeypatch.setenv('MINECHAT_HISTORY_PATH', 'history.txt')
        parser = create_parser()
        settings = parser.parse_args(args=[])
        assert settings.history_path == 'history.txt'

    def test_token(self, monkeypatch):
        monkeypatch.setenv('MINECHAT_TOKEN', 'some-token')
        parser = create_parser()
        settings = parser.parse_args(args=[])
        assert settings.token == 'some-token'

    def test_loglevel(self, monkeypatch):
        monkeypatch.setenv('MINECHAT_LOGLEVEL', 'DEBUG')
        parser = create_parser()
        settings = parser.parse_args(args=[])
        assert settings.loglevel == 'DEBUG'

    def test_bad_loglevel(self, monkeypatch):
        monkeypatch.setenv('MINECHAT_LOGLEVEL', 'WRONG VALUE')
        with pytest.raises(SystemExit):
            parser = create_parser()
            parser.parse_args(args=[])
