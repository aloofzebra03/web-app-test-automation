import socket
import subprocess
import sys
import time

import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"


def _port_is_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.2)
        return sock.connect_ex((host, port)) == 0


@pytest.fixture(scope="session", autouse=True)
def app_server():
    """Start the demo application once for the full test session."""
    if _port_is_open("127.0.0.1", 8000):
        yield BASE_URL
        return

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    deadline = time.time() + 15
    while time.time() < deadline:
        try:
            response = requests.get(f"{BASE_URL}/api/health", timeout=0.5)
            if response.status_code == 200:
                break
        except requests.RequestException:
            time.sleep(0.2)
    else:
        process.terminate()
        raise RuntimeError("FastAPI test server did not start")

    yield BASE_URL

    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()


@pytest.fixture
def base_url():
    return BASE_URL
