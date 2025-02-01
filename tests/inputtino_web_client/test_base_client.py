import pytest
from httpx import HTTPError

from inputtino_web_client.base_client import InputtinoBaseClient
from inputtino_web_client.models import DeviceType


@pytest.fixture
def base_client():
    return InputtinoBaseClient()


def test_init():
    client = InputtinoBaseClient("testhost", 9090)
    assert client.base_url == "http://testhost:9090/api/v1.0"


def test_list_devices(base_client, mocker):
    mock_response = {
        "devices": [
            {
                "device_id": "123",
                "client_id": "client1",
                "type": "KEYBOARD",
                "device_nodes": ["/dev/input/event0"],
            }
        ]
    }
    mocker.patch.object(
        base_client.client,
        "get",
        return_value=mocker.Mock(
            json=lambda: mock_response, raise_for_status=lambda: None
        ),
    )

    devices = base_client.list_devices()
    assert len(devices) == 1
    assert devices[0].device_id == "123"
    assert devices[0].type == "KEYBOARD"


def test_add_device(base_client, mocker):
    mock_response = {
        "device_id": "123",
        "client_id": "client1",
        "type": "KEYBOARD",
        "device_nodes": ["/dev/input/event0"],
    }
    mocker.patch.object(
        base_client.client,
        "post",
        return_value=mocker.Mock(
            json=lambda: mock_response, raise_for_status=lambda: None
        ),
    )

    device = base_client.add_device(DeviceType.KEYBOARD)
    assert device.device_id == "123"
    assert device.type == "KEYBOARD"


def test_remove_device(base_client, mocker):
    mock_response = {"success": True}
    mocker.patch.object(
        base_client.client,
        "delete",
        return_value=mocker.Mock(
            json=lambda: mock_response, raise_for_status=lambda: None
        ),
    )

    base_client.remove_device("123")  # Should not raise any exception


def test_request_error(base_client, mocker):
    mocker.patch.object(base_client.client, "get", side_effect=HTTPError("Test error"))

    with pytest.raises(HTTPError):
        base_client.list_devices()


def test_context_manager():
    with InputtinoBaseClient() as client:
        assert isinstance(client, InputtinoBaseClient)
