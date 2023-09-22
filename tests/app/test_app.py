import asyncio
import json

import pytest
from httpx import AsyncClient
from starlette.testclient import TestClient

from db_service import DBService
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
        data = json.loads(websocket.receive_text())
        print(data)
        assert data is not None
        assert type(data) is str


@pytest.mark.asyncio
async def test_post_answer():
    await DBService.create_question("test", "test")
    client = TestClient(app)
    with client.websocket_connect('/ws') as websocket:
        data = json.loads(websocket.receive_text())
        websocket.send_text("test")
        data = websocket.receive_text()
        assert data is not None
        assert data == 'Correct!'
        websocket.close()


@pytest.mark.asyncio
async def test_post_answer_weong():
    await DBService.create_question("test", "test")
    client = TestClient(app)
    with client.websocket_connect('/ws') as websocket:
        data = json.loads(websocket.receive_text())
        websocket.send_text("tesqwqwqwt")
        data = websocket.receive_text()
        assert data is not None
        assert data == 'Wrong!'
        websocket.close()

@pytest.mark.asyncio
async def test_get_all_questions():
    async with AsyncClient(app=app, base_url='http://localhost:8000') as client:
        response = await client.get("/questions")
        assert response.status_code == 200
        assert type(response.json()) is list

