"""CLI interface for inputtino web client."""

import os
from dataclasses import dataclass

import cmd2
from tyro import cli

from .keyboard import Keyboard
from .models import MouseButton, ScrollDirection
from .mouse import Mouse


class InputtinoCLI(cmd2.Cmd):
    """Interactive CLI for controlling mouse and keyboard through inputtino."""

    def __init__(self, host: str = "localhost", port: int = 8080) -> None:
        """Initialize CLI with mouse and keyboard clients."""
        super().__init__()
        self.mouse = Mouse(host, port)
        self.keyboard = Keyboard(host, port)
        self.prompt = "inputtino> "
        self.intro = "Welcome to inputtino CLI. Type ? to list commands."

    def do_move(self, args: str) -> None:
        """Move mouse relatively.

        Usage: move <x> <y>
        """
        try:
            x, y = map(float, args.split())
            self.mouse.move_rel(x, y)
        except ValueError:
            print("Usage: move <x> <y>")

    def do_move_abs(self, args: str) -> None:
        """Move mouse to absolute position.

        Usage: move_abs <x> <y> <width> <height>
        """
        try:
            x, y, width, height = map(float, args.split())
            self.mouse.move_abs(x, y, width, height)
        except ValueError:
            print("Usage: move_abs <x> <y> <width> <height>")

    def do_click(self, args: str) -> None:
        """Click mouse button.

        Usage: click [left|right|middle|side|extra]
        """
        button = args.strip() or "left"
        try:
            self.mouse.click(MouseButton(button))
        except ValueError:
            print("Invalid button. Use: left, right, middle, side, or extra")

    def do_scroll(self, args: str) -> None:
        """Scroll mouse wheel.

        Usage: scroll <distance> [vertical|horizontal]
        """
        try:
            parts = args.split()
            distance = float(parts[0])
            direction = parts[1] if len(parts) > 1 else "vertical"
            self.mouse.scroll(distance, ScrollDirection(direction))
        except (ValueError, IndexError):
            print("Usage: scroll <distance> [vertical|horizontal]")

    def do_type(self, args: str) -> None:
        """Type a key.

        Usage: type <key>
        """
        if args:
            self.keyboard.type(args)
        else:
            print("Usage: type <key>")

    def do_exit(self, _: str) -> bool:
        """Exit the CLI."""
        return True


@dataclass
class Args:
    """CLI arguments."""

    host: str = os.getenv("INPUTTINO_HOST", "localhost")
    port: int = int(os.getenv("INPUTTINO_PORT", "8080"))


def main() -> None:
    """Entry point for the CLI application."""
    args = cli(Args)
    app = InputtinoCLI(host=args.host, port=args.port)
    app.cmdloop()


if __name__ == "__main__":
    main()
