from .base_client import InputtinoBaseClient
from .models import DeviceType, KeyboardRequest


class Keyboard(InputtinoBaseClient):
    """Client for controlling keyboard input devices through the Inputtino
    API."""

    def __init__(self, host: str = "localhost", port: int = 8080) -> None:
        """Initialize Keyboard client and create a keyboard device.

        Args:
            host: Hostname of the Inputtino server
            port: Port number of the Inputtino server
        """
        super().__init__(host, port)
        self.device = self.add_device(DeviceType.KEYBOARD)

    @property
    def device_id(self) -> str:
        """Get the device ID of the keyboard."""
        return self.device.device_id

    def press(self, key: str) -> None:
        """Press a keyboard key.

        Args:
            key: Key to press
        """
        request = KeyboardRequest(key=key)
        self._post(
            f"/devices/keyboard/{self.device_id}/press", json=request.model_dump()
        )

    def release(self, key: str) -> None:
        """Release a keyboard key.

        Args:
            key: Key to release
        """
        request = KeyboardRequest(key=key)
        self._post(
            f"/devices/keyboard/{self.device_id}/release", json=request.model_dump()
        )

    def type(self, key: str) -> None:
        """Type a key (press and release).

        Args:
            key: Key to type
        """
        self.press(key)
        self.release(key)
