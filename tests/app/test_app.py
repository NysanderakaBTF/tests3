import asyncio

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
        data = await websocket.receive_json()
        assert data is not None
        assert data.keys() == ["question"]