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
        assert data == 'Correct!' or data == 'Wrong!'
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
        assert data == 'Wrong!' or data == 'Correct!'
        websocket.close()

@pytest.mark.asyncio
async def test_get_all_questions():
    async with AsyncClient(app=app, base_url='http://localhost:8000') as client:
        response = await client.get("/questions")
        assert response.status_code == 200
        assert type(response.json()) is list

@pytest.mark.asyncio
async def test_create_question():
    async with AsyncClient(app=app, base_url='http://localhost:8000') as client:
        data = {"question": "https://th.bing.com/th/id/OIP.-5DjlgC_p1i9w2sWFRkmQQHaDQ?pid=ImgDet&rs=1", "answer": "MVC"}
        response = await client.post("/questions", json=data)
        assert response.status_code == 200
        assert response.json()["question"] == "https://th.bing.com/th/id/OIP.-5DjlgC_p1i9w2sWFRkmQQHaDQ?pid=ImgDet&rs=1"
        assert response.json()["answer"] == "MVC"

@pytest.mark.asyncio
async def test_update_question():
    q = await DBService.create_question("test", "test")

    async with AsyncClient(app=app, base_url='http://localhost:8000') as client:
        data = {"question": "What is the capital of Germany?", "answer": "Berlin"}
        response = await client.put("/questions/"+str(q.id), json=json.dumps(data))
        assert response.status_code == 200
        ans = response.json()
        assert response.json()["question"] == "What is the capital of Germany?"
        assert response.json()["answer"] == "Berlin"

@pytest.mark.asyncio
async def test_update_question2():
    async with AsyncClient(app=app, base_url='http://localhost:8000') as client:
        data = {"question": "What is the capital of Germany?", "answer": "Berlin"}
        response = await client.put("/questions/99999999", json=json.dumps(data))
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_question():

    q = await DBService.create_question("test", "test")

    async with AsyncClient(app=app, base_url='http://localhost:8000') as client:
        response = await client.delete("/questions/"+str(q.id))
        assert response.status_code == 200
        assert response.json() == {"message": "Question deleted"}

@pytest.mark.asyncio
async def test_delete_question_no_exist():

    q = await DBService.create_question("test", "test")

    async with AsyncClient(app=app, base_url='http://localhost:8000') as client:
        response = await client.delete("/questions/999999999")
        assert response.status_code == 200
        assert response.json() == {"message": "Question deleted"}