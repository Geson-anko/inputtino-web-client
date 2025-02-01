import pytest
from httpx import HTTPError

from inputtino_web_client.base_client import InputtinoBaseClient
from inputtino_web_client.models import DeviceType
from tests.helpers import mark_practical


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


@mark_practical
def test_practical_device_lifecycle(practical_client: InputtinoBaseClient):
    """Test full device lifecycle with actual API."""
    # Add keyboard device
    keyboard = practical_client.add_device(DeviceType.KEYBOARD)
    assert keyboard.device_id
    assert keyboard.type == "KEYBOARD"

    # List devices and verify
    devices = practical_client.list_devices()
    assert any(d.device_id == keyboard.device_id for d in devices)

    # Remove device
    practical_client.remove_device(keyboard.device_id)

    # Verify removal
    devices = practical_client.list_devices()
    assert not any(d.device_id == keyboard.device_id for d in devices)


@mark_practical
def test_practical_multiple_devices(practical_client: InputtinoBaseClient):
    """Test managing multiple devices simultaneously."""
    devices = []

    # Add multiple devices
    for device_type in [DeviceType.KEYBOARD, DeviceType.MOUSE]:
        device = practical_client.add_device(device_type)
        devices.append(device)
        assert device.device_id

    # Verify all devices present
    listed_devices = practical_client.list_devices()
    device_ids = {d.device_id for d in devices}
    assert all(any(ld.device_id == did for ld in listed_devices) for did in device_ids)

    # Cleanup
    for device in devices:
        practical_client.remove_device(device.device_id)
