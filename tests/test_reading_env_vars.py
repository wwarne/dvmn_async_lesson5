import pytest

from settings import read_from_environment

class TestReadEnv:
    def test_read_host(self, monkeypatch):
        monkeypatch.setenv('MINECHAT_READ_HOST', 'example.com')
        results = read_from_environment()
        assert results['read_host'] == 'example.com'

    def test_read_port(self, monkeypatch):
        monkeypatch.setenv('MINECHAT_READ_PORT', '5050')
        results = read_from_environment()
        assert results['read_port'] == 5050

    def test_bad_read_port(self, monkeypatch):
        monkeypatch.setenv('MINECHAT_READ_PORT', 'not-integer')
        results = read_from_environment()
        assert results.get('read_port') is None

    def test_write_host(self, monkeypatch):
        monkeypatch.setenv('MINECHAT_WRITE_HOST', 'example.com')
        results = read_from_environment()
        assert results['write_host'] == 'example.com'

    def test_write_port(self, monkeypatch):
        monkeypatch.setenv('MINECHAT_WRITE_PORT', '5080')
        results = read_from_environment()
        assert results['write_port'] == 5080

    def test_bad_write_port(self, monkeypatch):
        monkeypatch.setenv('MINECHAT_WRITE_PORT', 'not-integer')
        results = read_from_environment()
        assert results.get('write_port') is None

    def test_history_path(self, monkeypatch):
        monkeypatch.setenv('MINECHAT_HISTORY_PATH', 'history.txt')
        results = read_from_environment()
        assert results['history_path'] == 'history.txt'

    def test_token(self, monkeypatch):
        monkeypatch.setenv('MINECHAT_WRITE_TOKEN', 'some-token')
        results = read_from_environment()
        assert results['token'] == 'some-token'

    def test_loglevel(self, monkeypatch):
        monkeypatch.setenv('MINECHAT_LOGLEVEL', 'DEBUG')
        results = read_from_environment()
        assert results['loglevel'] == 'DEBUG'

    def test_bad_loglevel(self, monkeypatch):
        monkeypatch.setenv('MINECHAT_LOGLEVEL', 'WRONG VALUE')
        results = read_from_environment()
        assert results.get('loglevel') is None
