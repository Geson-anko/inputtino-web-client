from enum import StrEnum

from pydantic import BaseModel


class DeviceType(StrEnum):
    KEYBOARD = "keyboard"
    MOUSE = "mouse"


class MouseButton(StrEnum):
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"
    SIDE = "side"
    EXTRA = "extra"


class ScrollDirection(StrEnum):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


class AddDeviceRequest(BaseModel):
    type: DeviceType


class DeviceResponse(BaseModel):
    device_id: str
    client_id: str
    type: str
    device_nodes: list[str]


class DevicesListResponse(BaseModel):
    devices: list[DeviceResponse]


class MouseMoveRelRequest(BaseModel):
    delta_x: float = 0.0
    delta_y: float = 0.0


class MouseMoveAbsRequest(BaseModel):
    abs_x: float = 0.0
    abs_y: float = 0.0
    screen_width: float = 0.0
    screen_height: float = 0.0


class MouseButtonRequest(BaseModel):
    button: MouseButton = MouseButton.LEFT


class MouseScrollRequest(BaseModel):
    direction: ScrollDirection = ScrollDirection.VERTICAL
    distance: float = 0.0


class KeyboardRequest(BaseModel):
    key: int


class SuccessResponse(BaseModel):
    success: bool


class ErrorResponse(BaseModel):
    error: str
