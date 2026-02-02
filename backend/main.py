import asyncio
import random
import string
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from spellchecker import SpellChecker
from contextlib import asynccontextmanager

class MonkeyState:
    def __init__(self):
        self.is_running = False
        self.current_word = ""
        self.letter_history = ""
        self.found_words = []
        self.active_connections: list[WebSocket] = []

monkey_state = MonkeyState()

def generate_random_letter():
    letter = random.choice(string.ascii_letters + " ")
    return letter

spell = SpellChecker()

def check_word(word: str):
    word = word.strip().lower()
    if len(word) > 1 and spell.known([word]):
        return {"type": "word", "text": word.strip()}
    return None

async def typing_monkey():
    while True:
        if monkey_state.is_running:
            letter = generate_random_letter()
            monkey_state.letter_history += letter

            broadcast_message = {"type": "letter", "text": letter}
            if letter == " ":
                if monkey_state.current_word.strip():
                    word_info = check_word(monkey_state.current_word)
                    if word_info:
                        monkey_state.found_words.append(word_info)
                        broadcast_message = word_info
                monkey_state.current_word = ""
            else:
                monkey_state.current_word += letter

            for connection in monkey_state.active_connections:
                try:
                    await connection.send_json(broadcast_message)
                except:
                    pass

            await asyncio.sleep(0.01)
        else:
            await asyncio.sleep(0.1)

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(typing_monkey())
    yield


app = FastAPI(lifespan=lifespan)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    monkey_state.active_connections.append(websocket)

    history_check = {
        "type": "history",
        "letters": monkey_state.letter_history[-5000:],
        "words": monkey_state.found_words[-500:]
    }
    await websocket.send_json(history_check)

    try:
        while True:
            data = await websocket.receive_text()
            if data == "start":
                monkey_state.is_running = True
            elif data == "stop":
                monkey_state.is_running = False
            elif data == "reset":
                monkey_state.current_word = ""
                monkey_state.letter_history = ""
                monkey_state.found_words = []
    except WebSocketDisconnect:
        monkey_state.active_connections.remove(websocket)

