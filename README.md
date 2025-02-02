# Inputtino Web Client

A Python library for controlling mouse and keyboard input through the Inputtino HTTP API. This library provides a clean, type-safe interface for programmatic input control.

## Features

- Full mouse control (movement, clicking, scrolling)
- Comprehensive keyboard input support
- Type-safe API with complete type hints
- CLI tool for interactive control

## Current Limitations

- Gamepad inputs are not currently supported

## Requirements

- Python 3.12 or higher
- Running Inputtino server (see [Games-on-Whales/inputtino](https://github.com/games-on-whales/inputtino))

## Installation

You can install the package using pip:

```bash
pip install inputtino-web-client
```

For CLI support, install with the optional CLI dependencies:

```bash
pip install inputtino-web-client[cli]
```

## Quick Start

### Mouse Control

```python
from inputtino_web_client import Mouse, MouseButton, ScrollDirection

# Initialize mouse control
mouse = Mouse(host="localhost", port=8080)

# Move mouse relatively
mouse.move_rel(100, 50)  # Move right 100, down 50

# Move to absolute position (based on screen dimensions)
mouse.move_abs(500, 300, screen_width=1920, screen_height=1080)

# Click operations
mouse.click(MouseButton.LEFT)
mouse.click(MouseButton.RIGHT)

# Scrolling
mouse.scroll(120, direction=ScrollDirection.VERTICAL)  # Scroll up
mouse.scroll(-120, direction="vertical")  # Scroll down
```

### Keyboard Control

```python
from inputtino_web_client import Keyboard, KeyCode

# Initialize keyboard control
keyboard = Keyboard(host="localhost", port=8080)

# Type individual keys
keyboard.type(KeyCode.A)
keyboard.type(KeyCode.from_str("enter")) # from string

# Press and release keys separately
keyboard.press(KeyCode.SHIFT)
keyboard.type(KeyCode.A)  # Types capital A
keyboard.release(KeyCode.SHIFT)
```

## CLI Usage

After installing with CLI support, you can use the interactive command-line interface:

```bash
inputtino-cli
```

Available commands:

- `move <x> <y>` - Move mouse relatively
- `move_abs <x> <y> <width> <height>` - Move mouse to absolute position
- `click [left|right|middle|side|extra]` - Click mouse button
- `scroll <distance> [vertical|horizontal]` - Scroll mouse wheel
- `type <key>` - Type a keyboard key

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed information about contributing to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Games-on-Whales/inputtino](https://github.com/games-on-whales/inputtino) - The underlying input control server
