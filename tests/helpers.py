import os

import pytest

mark_practical = pytest.mark.practical


def get_test_client_params() -> tuple[str, int]:
    """Get test client parameters from environment variables."""
    host = os.getenv("INPUTTINO_HOST", "localhost")
    port = int(os.getenv("INPUTTINO_PORT", "8080"))
    return host, port
