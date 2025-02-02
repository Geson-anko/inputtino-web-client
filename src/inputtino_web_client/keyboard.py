from enum import IntEnum

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
        request = KeyboardRequest(key=get_keycode_from_string(key))
        self._post(
            f"/devices/keyboard/{self.device_id}/press", json=request.model_dump()
        )

    def release(self, key: str) -> None:
        """Release a keyboard key.

        Args:
            key: Key to release
        """
        request = KeyboardRequest(key=get_keycode_from_string(key))
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


class KeyCode(IntEnum):
    """KeyCode mapping for virtual key codes.

    This class provides a mapping between human-readable key names and
    their corresponding virtual key codes used by the input system.

    Key codes are referred from
    <https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes>
    """

    # Standard Keys
    BACKSPACE = 0x08
    TAB = 0x09
    CLEAR = 0x0C
    ENTER = 0x0D
    SHIFT = 0x10
    CTRL = 0x11
    ALT = 0x12
    PAUSE = 0x13
    CAPS_LOCK = 0x14
    ESC = 0x1B
    SPACE = 0x20
    PAGE_UP = 0x21
    PAGE_DOWN = 0x22
    END = 0x23
    HOME = 0x24
    LEFT = 0x25
    UP = 0x26
    RIGHT = 0x27
    DOWN = 0x28
    PRINTSCREEN = 0x2C
    INSERT = 0x2D
    DELETE = 0x2E

    # Numbers
    KEY_0 = 0x30
    KEY_1 = 0x31
    KEY_2 = 0x32
    KEY_3 = 0x33
    KEY_4 = 0x34
    KEY_5 = 0x35
    KEY_6 = 0x36
    KEY_7 = 0x37
    KEY_8 = 0x38
    KEY_9 = 0x39

    # Letters
    A = 0x41
    B = 0x42
    C = 0x43
    D = 0x44
    E = 0x45
    F = 0x46
    G = 0x47
    H = 0x48
    I = 0x49
    J = 0x4A
    K = 0x4B
    L = 0x4C
    M = 0x4D
    N = 0x4E
    O = 0x4F
    P = 0x50
    Q = 0x51
    R = 0x52
    S = 0x53
    T = 0x54
    U = 0x55
    V = 0x56
    W = 0x57
    X = 0x58
    Y = 0x59
    Z = 0x5A

    # Windows Keys
    LEFT_WIN = 0x5B
    RIGHT_WIN = 0x5C
    APP = 0x5D

    # Numpad
    NUMPAD_0 = 0x60
    NUMPAD_1 = 0x61
    NUMPAD_2 = 0x62
    NUMPAD_3 = 0x63
    NUMPAD_4 = 0x64
    NUMPAD_5 = 0x65
    NUMPAD_6 = 0x66
    NUMPAD_7 = 0x67
    NUMPAD_8 = 0x68
    NUMPAD_9 = 0x69
    MULTIPLY = 0x6A
    ADD = 0x6B
    SUBTRACT = 0x6D
    DECIMAL = 0x6E
    DIVIDE = 0x6F

    # Function Keys
    F1 = 0x70
    F2 = 0x71
    F3 = 0x72
    F4 = 0x73
    F5 = 0x74
    F6 = 0x75
    F7 = 0x76
    F8 = 0x77
    F9 = 0x78
    F10 = 0x79
    F11 = 0x7A
    F12 = 0x7B
    F13 = 0x7C
    F14 = 0x7D
    F15 = 0x7E
    F16 = 0x7F
    F17 = 0x80
    F18 = 0x81
    F19 = 0x82
    F20 = 0x83
    F21 = 0x84
    F22 = 0x85
    F23 = 0x86
    F24 = 0x87

    # Lock Keys
    NUM_LOCK = 0x90
    SCROLL_LOCK = 0x91

    # Left/Right Keys
    LEFT_SHIFT = 0xA0
    RIGHT_SHIFT = 0xA1
    LEFT_CONTROL = 0xA2
    RIGHT_CONTROL = 0xA3
    LEFT_ALT = 0xA4
    RIGHT_ALT = 0xA5

    # Media Keys
    VOLUME_MUTE = 0xAD
    VOLUME_DOWN = 0xAE
    VOLUME_UP = 0xAF
    MEDIA_NEXT = 0xB0
    MEDIA_PREV = 0xB1
    MEDIA_STOP = 0xB2
    MEDIA_PLAY_PAUSE = 0xB3

    # OEM Keys
    SEMICOLON = 0xBA  # ;:
    PLUS = 0xBB  # =+
    COMMA = 0xBC  # ,<
    MINUS = 0xBD  # -_
    PERIOD = 0xBE  # .>
    SLASH = 0xBF  # /?
    TILDE = 0xC0  # `~
    OPEN_BRACKET = 0xDB  # [{
    BACKSLASH = 0xDC  # \|
    CLOSE_BRACKET = 0xDD  # ]}
    QUOTE = 0xDE  # '"


def get_keycode_from_string(key: str) -> KeyCode:
    """Convert a string representation to a KeyCode enum value.

    Args:
        key: A string representing the key name.

    Returns:
        The corresponding KeyCode enum value.

    Raises:
        ValueError: If no matching KeyCode is found for the given key.
    """
    # Create a mapping of normalized key names to KeyCode values
    key_mapping = {
        # Standard Keys
        "backspace": KeyCode.BACKSPACE,
        "tab": KeyCode.TAB,
        "clear": KeyCode.CLEAR,
        "enter": KeyCode.ENTER,
        "shift": KeyCode.SHIFT,
        "ctrl": KeyCode.CTRL,
        "alt": KeyCode.ALT,
        "pause": KeyCode.PAUSE,
        "capslock": KeyCode.CAPS_LOCK,
        "esc": KeyCode.ESC,
        "space": KeyCode.SPACE,
        "pageup": KeyCode.PAGE_UP,
        "pagedown": KeyCode.PAGE_DOWN,
        "end": KeyCode.END,
        "home": KeyCode.HOME,
        "left": KeyCode.LEFT,
        "up": KeyCode.UP,
        "right": KeyCode.RIGHT,
        "down": KeyCode.DOWN,
        "printscreen": KeyCode.PRINTSCREEN,
        "insert": KeyCode.INSERT,
        "delete": KeyCode.DELETE,
        # Numbers
        "0": KeyCode.KEY_0,
        "1": KeyCode.KEY_1,
        "2": KeyCode.KEY_2,
        "3": KeyCode.KEY_3,
        "4": KeyCode.KEY_4,
        "5": KeyCode.KEY_5,
        "6": KeyCode.KEY_6,
        "7": KeyCode.KEY_7,
        "8": KeyCode.KEY_8,
        "9": KeyCode.KEY_9,
        # Letters
        "a": KeyCode.A,
        "b": KeyCode.B,
        "c": KeyCode.C,
        "d": KeyCode.D,
        "e": KeyCode.E,
        "f": KeyCode.F,
        "g": KeyCode.G,
        "h": KeyCode.H,
        "i": KeyCode.I,
        "j": KeyCode.J,
        "k": KeyCode.K,
        "l": KeyCode.L,
        "m": KeyCode.M,
        "n": KeyCode.N,
        "o": KeyCode.O,
        "p": KeyCode.P,
        "q": KeyCode.Q,
        "r": KeyCode.R,
        "s": KeyCode.S,
        "t": KeyCode.T,
        "u": KeyCode.U,
        "v": KeyCode.V,
        "w": KeyCode.W,
        "x": KeyCode.X,
        "y": KeyCode.Y,
        "z": KeyCode.Z,
        # Windows Keys
        "leftwin": KeyCode.LEFT_WIN,
        "rightwin": KeyCode.RIGHT_WIN,
        "app": KeyCode.APP,
        # Numpad
        "numpad0": KeyCode.NUMPAD_0,
        "numpad1": KeyCode.NUMPAD_1,
        "numpad2": KeyCode.NUMPAD_2,
        "numpad3": KeyCode.NUMPAD_3,
        "numpad4": KeyCode.NUMPAD_4,
        "numpad5": KeyCode.NUMPAD_5,
        "numpad6": KeyCode.NUMPAD_6,
        "numpad7": KeyCode.NUMPAD_7,
        "numpad8": KeyCode.NUMPAD_8,
        "numpad9": KeyCode.NUMPAD_9,
        "multiply": KeyCode.MULTIPLY,
        "add": KeyCode.ADD,
        "subtract": KeyCode.SUBTRACT,
        "decimal": KeyCode.DECIMAL,
        "divide": KeyCode.DIVIDE,
        # Function Keys
        "f1": KeyCode.F1,
        "f2": KeyCode.F2,
        "f3": KeyCode.F3,
        "f4": KeyCode.F4,
        "f5": KeyCode.F5,
        "f6": KeyCode.F6,
        "f7": KeyCode.F7,
        "f8": KeyCode.F8,
        "f9": KeyCode.F9,
        "f10": KeyCode.F10,
        "f11": KeyCode.F11,
        "f12": KeyCode.F12,
        "f13": KeyCode.F13,
        "f14": KeyCode.F14,
        "f15": KeyCode.F15,
        "f16": KeyCode.F16,
        "f17": KeyCode.F17,
        "f18": KeyCode.F18,
        "f19": KeyCode.F19,
        "f20": KeyCode.F20,
        "f21": KeyCode.F21,
        "f22": KeyCode.F22,
        "f23": KeyCode.F23,
        "f24": KeyCode.F24,
        # Lock Keys
        "numlock": KeyCode.NUM_LOCK,
        "scrolllock": KeyCode.SCROLL_LOCK,
        # Left/Right Keys
        "leftshift": KeyCode.LEFT_SHIFT,
        "rightshift": KeyCode.RIGHT_SHIFT,
        "leftcontrol": KeyCode.LEFT_CONTROL,
        "rightcontrol": KeyCode.RIGHT_CONTROL,
        "leftalt": KeyCode.LEFT_ALT,
        "rightalt": KeyCode.RIGHT_ALT,
        # Media Keys
        "volumemute": KeyCode.VOLUME_MUTE,
        "volumedown": KeyCode.VOLUME_DOWN,
        "volumeup": KeyCode.VOLUME_UP,
        "medianext": KeyCode.MEDIA_NEXT,
        "mediaprev": KeyCode.MEDIA_PREV,
        "mediastop": KeyCode.MEDIA_STOP,
        "mediaplaypause": KeyCode.MEDIA_PLAY_PAUSE,
        # OEM Keys
        "semicolon": KeyCode.SEMICOLON,
        "plus": KeyCode.PLUS,
        "comma": KeyCode.COMMA,
        "minus": KeyCode.MINUS,
        "period": KeyCode.PERIOD,
        "slash": KeyCode.SLASH,
        "tilde": KeyCode.TILDE,
        "openbracket": KeyCode.OPEN_BRACKET,
        "backslash": KeyCode.BACKSLASH,
        "closebracket": KeyCode.CLOSE_BRACKET,
        "quote": KeyCode.QUOTE,
    }

    # Normalize the input key (convert to lowercase and remove spaces)
    normalized_key = key.lower().replace(" ", "")

    # Try to find the KeyCode
    if normalized_key in key_mapping:
        return key_mapping[normalized_key]

    raise ValueError(f"No KeyCode found for key: {key}")
