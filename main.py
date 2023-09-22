import asyncio
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.websockets import WebSocket, WebSocketDisconnect
from tortoise.contrib.pydantic import pydantic_model_creator
from websockets.exceptions import ConnectionClosed

from db_service import DBService
from models.models import Question, init

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init()


Question_Pydantic = pydantic_model_creator(Question)


async def get_random_question_json():
    q = await DBService.get_random_question()
    if not q:
        return {"question": "No questions available"}
    return await Question_Pydantic.from_tortoise_orm(q)


@app.websocket("/ws")
async def get_question(websocket: WebSocket):
    await websocket.accept()
    qq = await get_random_question_json()
    if isinstance(qq, dict):
        await websocket.send_json(qq)
        await websocket.close()
        return
    else:
        await websocket.send_json(qq.model_dump().get('question'))

    while True:
        try:
            ans = await websocket.receive_text()
        except WebSocketDisconnect:
            print(f"Terminated")
            return

        if ans.lower() == qq.answer.lower():
            await websocket.send_text("Correct!")
            qq = await get_random_question_json()
            if isinstance(qq, dict):
                await websocket.send_json(qq)
                await websocket.close()
                return
            else:
                await websocket.send_json(qq.model_dump().get('question'))
        else:
            await websocket.send_text("Wrong!")


class QuestionCreate(BaseModel):
    question: str
    answer: str


class QuestionUpdate(BaseModel):
    question: str
    answer: str


class QuestionResponse(BaseModel):
    id: int
    question: str
    answer: str


@app.get("/questions", response_model=List[QuestionResponse])
async def get_all_questions():
    questions = await DBService.get_all_questions()
    return questions


@app.post("/questions", response_model=QuestionResponse)
async def create_question(question: QuestionCreate):
    q = await DBService.create_question(question.question, question.answer)
    return q
