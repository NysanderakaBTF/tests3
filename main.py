import asyncio
import json
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.requests import Request
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


async def end_on_no_question_or_send(question, websocket: WebSocket):
    if isinstance(question, dict):
        await websocket.send_json(question)
        await websocket.close()
        return
    else:
        await websocket.send_json(question.model_dump().get('question'))

@app.websocket("/ws")
async def get_question(websocket: WebSocket):
    await websocket.accept()
    qq = await get_random_question_json()
    await end_on_no_question_or_send(qq, websocket)
    while True:
        try:
            ans = await websocket.receive_text()
        except WebSocketDisconnect:
            print(f"Terminated")
            return
        if ans.lower() == qq.answer.lower():
            await websocket.send_text("Correct!")
            qq = await get_random_question_json()
            await end_on_no_question_or_send(qq, websocket)
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


@app.put("/questions/{id}")
async def update_question(id: int, request: Request):
    req = json.loads(await request.json())
    if list(req.keys()) != ['question', 'answer']:
        raise HTTPException(status_code=400, detail="Bad request")
    q = await DBService.update_question(id, req['question'], req['answer'])
    if q is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return q


@app.delete("/questions/{id}")
async def delete_question(id: int):
    await DBService.delete_question(id)
    return {"message": "Question deleted"}
