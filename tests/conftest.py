import pytest
from settings import create_parser

@pytest.fixture()
def arg_parser():
    yield create_parser()