from importlib import metadata

from .keyboard import Keyboard
from .mouse import Mouse

__version__ = metadata.version(__name__.replace("_", "-"))

__all__ = ["Mouse", "Keyboard"]
