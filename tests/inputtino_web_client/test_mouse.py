import pytest
from pytest_mock import MockerFixture

from inputtino_web_client.models import DeviceResponse, MouseButton, ScrollDirection
from inputtino_web_client.mouse import Mouse
from tests.helpers import get_test_client_params, mark_practical


@pytest.fixture
def mouse_device():
    return DeviceResponse(
        device_id="123",
        client_id="client1",
        type="MOUSE",
        device_nodes=["/dev/input/event0"],
    )


@pytest.fixture
def mouse(mocker: MockerFixture, mouse_device: DeviceResponse):
    mocker.patch(
        "inputtino_web_client.mouse.InputtinoBaseClient.add_device",
        return_value=mouse_device,
    )
    return Mouse()


def test_init(mocker: MockerFixture, mouse_device: DeviceResponse):
    mock_add_device = mocker.patch(
        "inputtino_web_client.mouse.InputtinoBaseClient.add_device",
        return_value=mouse_device,
    )
    mouse = Mouse("testhost", 9090)

    assert mouse.base_url == "http://testhost:9090/api/v1.0"
    mock_add_device.assert_called_once()
    assert mouse.device_id == "123"


def test_move_rel(mouse: Mouse, mocker: MockerFixture):
    mock_post = mocker.patch.object(mouse, "_post")
    mouse.move_rel(10.0, -5.0)

    mock_post.assert_called_once_with(
        "/devices/mouse/123/move_rel", json={"delta_x": 10.0, "delta_y": -5.0}
    )


def test_move_abs(mouse: Mouse, mocker: MockerFixture):
    mock_post = mocker.patch.object(mouse, "_post")
    mouse.move_abs(100.0, 200.0, 1920.0, 1080.0)

    mock_post.assert_called_once_with(
        "/devices/mouse/123/move_abs",
        json={
            "abs_x": 100.0,
            "abs_y": 200.0,
            "screen_width": 1920.0,
            "screen_height": 1080.0,
        },
    )


def test_press(mouse: Mouse, mocker: MockerFixture):
    mock_post = mocker.patch.object(mouse, "_post")
    mouse.press(MouseButton.RIGHT)

    mock_post.assert_called_once_with(
        "/devices/mouse/123/press", json={"button": "right"}
    )


def test_release(mouse: Mouse, mocker: MockerFixture):
    mock_post = mocker.patch.object(mouse, "_post")
    mouse.release(MouseButton.MIDDLE)

    mock_post.assert_called_once_with(
        "/devices/mouse/123/release", json={"button": "middle"}
    )


def test_click(mouse: Mouse, mocker: MockerFixture):
    mock_press = mocker.patch.object(mouse, "press")
    mock_release = mocker.patch.object(mouse, "release")

    mouse.click(MouseButton.LEFT)

    mock_press.assert_called_once_with(MouseButton.LEFT)
    mock_release.assert_called_once_with(MouseButton.LEFT)


def test_scroll(mouse: Mouse, mocker: MockerFixture):
    mock_post = mocker.patch.object(mouse, "_post")
    mouse.scroll(120.0, ScrollDirection.HORIZONTAL)

    mock_post.assert_called_once_with(
        "/devices/mouse/123/scroll", json={"direction": "horizontal", "distance": 120.0}
    )


@mark_practical
def test_practical_mouse_operations(practical_client_address):
    """Test basic mouse operations with actual API."""
    host, port = practical_client_address
    mouse = Mouse(host=host, port=port)
    mouse.move_rel(10.0, 10.0)
    mouse.move_abs(100.0, 100.0, 1920.0, 1080.0)
    mouse.click(MouseButton.LEFT)
    mouse.scroll(120.0, ScrollDirection.VERTICAL)
