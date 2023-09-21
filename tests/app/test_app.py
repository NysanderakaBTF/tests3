import asyncio
import json

import pytest
from starlette.testclient import TestClient

from main import app
from models.models import init


@pytest.fixture(autouse=True, scope='session')
def execute_before_any_test():
    print("Executing before any test")
    asyncio.run(init())


@pytest.mark.asyncio
async def test_get_question():
    client = TestClient(app)
    with client.websocket_connect('/ws') as websocket:
        data = json.loads(websocket.receive_json())
        assert data is not None
        assert list(data.keys()) == ["question"]

@pytest.mark.asyncio
async def test_post_answer():
    client = TestClient(app)
    with client.websocket_connect('/ws') as websocket:
        data = json.loads(websocket.receive_json())
        websocket.send_json("Alla")
        data = json.loads(websocket.receive_json())
        assert data is not None
        assert list(data.keys()) == ["answer", "question"]