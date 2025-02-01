from .base_client import InputtinoBaseClient
from .models import (
    DeviceType,
    MouseButton,
    MouseButtonRequest,
    MouseMoveAbsRequest,
    MouseMoveRelRequest,
    MouseScrollRequest,
    ScrollDirection,
)


class Mouse(InputtinoBaseClient):
    """Client for controlling mouse input devices through the Inputtino API."""

    def __init__(self, host: str = "localhost", port: int = 8080) -> None:
        """Initialize Mouse client and create a mouse device.

        Args:
            host: Hostname of the Inputtino server
            port: Port number of the Inputtino server
        """
        super().__init__(host, port)
        self.device = self.add_device(DeviceType.MOUSE)

    @property
    def device_id(self) -> str:
        """Get the device ID of the mouse."""
        return self.device.device_id

    def move_rel(self, delta_x: float, delta_y: float) -> None:
        """Move the mouse cursor relatively.

        Args:
            delta_x: Relative movement in x-direction
            delta_y: Relative movement in y-direction
        """
        request = MouseMoveRelRequest(delta_x=delta_x, delta_y=delta_y)
        self._post(
            f"/devices/mouse/{self.device_id}/move_rel", json=request.model_dump()
        )

    def move_abs(
        self, x: float, y: float, screen_width: float, screen_height: float
    ) -> None:
        """Move the mouse cursor to absolute screen coordinates.

        Args:
            x: Absolute x-coordinate
            y: Absolute y-coordinate
            screen_width: Width of the screen
            screen_height: Height of the screen
        """
        request = MouseMoveAbsRequest(
            abs_x=x, abs_y=y, screen_width=screen_width, screen_height=screen_height
        )
        self._post(
            f"/devices/mouse/{self.device_id}/move_abs", json=request.model_dump()
        )

    def press(self, button: MouseButton) -> None:
        """Press a mouse button.

        Args:
            button: Mouse button to press
        """
        request = MouseButtonRequest(button=button)
        self._post(f"/devices/mouse/{self.device_id}/press", json=request.model_dump())

    def release(self, button: MouseButton) -> None:
        """Release a mouse button.

        Args:
            button: Mouse button to release
        """
        request = MouseButtonRequest(button=button)
        self._post(
            f"/devices/mouse/{self.device_id}/release", json=request.model_dump()
        )

    def click(self, button: MouseButton) -> None:
        """Click a mouse button (press and release).

        Args:
            button: Mouse button to click
        """
        self.press(button)
        self.release(button)

    def scroll(self, distance: float, direction: ScrollDirection) -> None:
        """Scroll the mouse wheel.

        Args:
            distance: Scroll distance
            direction: Scroll direction
        """
        request = MouseScrollRequest(direction=direction, distance=distance)
        self._post(f"/devices/mouse/{self.device_id}/scroll", json=request.model_dump())
