from fastapi import FastAPI
from starlette.websockets import WebSocket
from tortoise.contrib.pydantic import pydantic_model_creator

from db_service import DBService
from models.models import Question

app = FastAPI()

Question_Pydantic = pydantic_model_creator(Question)


@app.websocket("/ws")
async def get_question(websocket: WebSocket):
    await websocket.accept()
    q = await DBService.get_random_question()
    qj = await Question_Pydantic.from_tortoise_orm(q)
    await websocket.send_json(qj.model_dump_json(include={'question'}))

