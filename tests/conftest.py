import pytest

from inputtino_web_client.base_client import InputtinoBaseClient
from tests.helpers import get_test_client_params


@pytest.fixture
def practical_client_address() -> tuple[str, int]:
    return get_test_client_params()


@pytest.fixture
def practical_client(practical_client_address):
    host, port = practical_client_address
    return InputtinoBaseClient(host, port)
