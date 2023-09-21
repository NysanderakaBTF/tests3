from fastapi import FastAPI
from starlette.websockets import WebSocket

from db_service import DBService

app = FastAPI()

@app.websocket("/ws")
async def get_question(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json(await DBService.get_random_question())

