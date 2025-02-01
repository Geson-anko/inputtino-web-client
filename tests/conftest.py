import pytest

from inputtino_web_client.base_client import InputtinoBaseClient
from tests.helpers import get_test_client_params


@pytest.fixture
def practical_client():
    host, port = get_test_client_params()
    return InputtinoBaseClient(host, port)
