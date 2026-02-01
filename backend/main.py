import asyncio
import random
import string
import enchant
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

class MonkeyState:
    def __init__(self):
        self.is_running = False

monkey_state = MonkeyState()

def generate_random_letter():
    letter = random.choice(string.ascii_letters + " ")
    return letter

dictionary = enchant.Dict("en_US")

def check_for_words(text):
    words = text.split()
    found_words = []

    for word in words:
        if dictionary.check(word):
            found_words.append(word)

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

@app.get("/check_words/{text}")
async def check_words_endpoint(text: str):
    found_words = check_for_words(text)
    return {"found_words": found_words}
