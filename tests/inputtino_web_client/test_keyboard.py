import pytest
from pytest_mock import MockerFixture

from inputtino_web_client.keyboard import Keyboard, KeyCode
from inputtino_web_client.models import DeviceResponse
from tests.helpers import mark_practical


@pytest.fixture
def keyboard_device():
    return DeviceResponse(
        device_id="123",
        client_id="client1",
        type="KEYBOARD",
        device_nodes=["/dev/input/event0"],
    )


@pytest.fixture
def keyboard(mocker: MockerFixture, keyboard_device: DeviceResponse):
    mocker.patch(
        "inputtino_web_client.keyboard.InputtinoBaseClient.add_device",
        return_value=keyboard_device,
    )
    return Keyboard()


def test_init(mocker: MockerFixture, keyboard_device: DeviceResponse):
    mock_add_device = mocker.patch(
        "inputtino_web_client.keyboard.InputtinoBaseClient.add_device",
        return_value=keyboard_device,
    )
    keyboard = Keyboard("testhost", 9090)

    assert keyboard.base_url == "http://testhost:9090/api/v1.0"
    mock_add_device.assert_called_once()
    assert keyboard.device_id == "123"


def test_press(keyboard: Keyboard, mocker: MockerFixture):
    mock_post = mocker.patch.object(keyboard, "_post")
    keyboard.press("a")

    mock_post.assert_called_once_with(
        "/devices/keyboard/123/press", json={"key": KeyCode.A}
    )


def test_release(keyboard: Keyboard, mocker: MockerFixture):
    mock_post = mocker.patch.object(keyboard, "_post")
    keyboard.release("b")

    mock_post.assert_called_once_with(
        "/devices/keyboard/123/release", json={"key": KeyCode.B}
    )


def test_type(keyboard: Keyboard, mocker: MockerFixture):
    mock_press = mocker.patch.object(keyboard, "press")
    mock_release = mocker.patch.object(keyboard, "release")

    keyboard.type("c")

    mock_press.assert_called_once_with("c")
    mock_release.assert_called_once_with("c")


@mark_practical
def test_practical_keyboard_operations(practical_client_address):
    """Test basic keyboard operations with actual API."""
    host, port = practical_client_address
    keyboard = Keyboard(host=host, port=port)
    keyboard.type("a")
    keyboard.press("shift")
    keyboard.type("b")
    keyboard.release("shift")
