import asyncio
import random
import string
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

class MonkeyState:
    def __init__(self):
        self.is_running = False

monkey_state = MonkeyState()

def generate_random_letter():
    letter = random.choice(string.ascii_letters + " ")
    return letter

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            if monkey_state.is_running:
                letter = generate_random_letter()
                await websocket.send_text(letter)
                await asyncio.sleep(0.01)
            else:
                await asyncio.sleep(0.1)
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=0.001)
                if data == "start":
                    monkey_state.is_running = True
                elif data == "stop":
                    monkey_state.is_running = False
            except asyncio.TimeoutError:
                pass
    except WebSocketDisconnect:
        monkey_state.is_running = False
        print("Client disconnected")
