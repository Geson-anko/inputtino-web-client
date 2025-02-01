from typing import Any, Self

import httpx

from .models import (
    AddDeviceRequest,
    DeviceResponse,
    DevicesListResponse,
    DeviceType,
)


class InputtinoBaseClient:
    """Base client for interacting with the Inputtino HTTP API.

    Provides core HTTP request functionality and device management
    methods.
    """

    def __init__(self, host: str = "localhost", port: int = 8080) -> None:
        """Initialize the base client.

        Args:
            host: Hostname of the Inputtino server
            port: Port number of the Inputtino server
        """
        self.base_url = f"http://{host}:{port}/api/v1.0"
        self.client = httpx.Client(timeout=5.0)

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict:
        """Send GET request to the API.

        Args:
            path: API endpoint path
            params: Query parameters

        Returns:
            Response JSON data

        Raises:
            httpx.HTTPError: If the request fails
        """
        response = self.client.get(f"{self.base_url}{path}", params=params)
        response.raise_for_status()
        return response.json()

    def _post(self, path: str, json: dict[str, Any] | None = None) -> dict:
        """Send POST request to the API.

        Args:
            path: API endpoint path
            json: Request body data

        Returns:
            Response JSON data

        Raises:
            httpx.HTTPError: If the request fails
        """
        response = self.client.post(f"{self.base_url}{path}", json=json)
        response.raise_for_status()
        return response.json()

    def _delete(self, path: str) -> dict:
        """Send DELETE request to the API.

        Args:
            path: API endpoint path

        Returns:
            Response JSON data

        Raises:
            httpx.HTTPError: If the request fails
        """
        response = self.client.delete(f"{self.base_url}{path}")
        response.raise_for_status()
        return response.json()

    def list_devices(self) -> list[DeviceResponse]:
        """Get list of all connected devices.

        Returns:
            List of device information
        """
        response = self._get("/devices")
        return DevicesListResponse(**response).devices

    def add_device(self, device_type: DeviceType) -> DeviceResponse:
        """Add a new device.

        Args:
            device_type: Type of device to add

        Returns:
            Information about the added device
        """
        request = AddDeviceRequest(type=device_type)
        response = self._post("/devices/add", json=request.model_dump())
        return DeviceResponse(**response)

    def remove_device(self, device_id: str) -> None:
        """Remove a device.

        Args:
            device_id: ID of the device to remove
        """
        self._delete(f"/devices/{device_id}")

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: Any, **kwds: Any) -> None:
        self.client.close()
