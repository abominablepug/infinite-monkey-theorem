import asyncio
import random
import string
import json
import os
import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from spellchecker import SpellChecker
from contextlib import asynccontextmanager

DATA_PATH = "/app/data/found_words.json"

def save_found_words():
    try:
        with open(DATA_PATH, "w") as f:
            json.dump(monkey_state.found_words, f)
    except Exception as e:
        print(f"Error saving found words: {e}")

def load_found_words():
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, "r") as f:
                monkey_state.found_words = json.load(f)
        except Exception as e:
            print(f"Error loading found words: {e}")

class MonkeyState:
    def __init__(self):
        self.is_running = False
        self.current_word = ""
        self.letter_history = ""
        self.found_words = []
        self.active_connections: list[WebSocket] = []
        self.active_time = 0.0

monkey_state = MonkeyState()

def generate_random_letter():
    letter = random.choice(string.ascii_letters + " ")
    return letter

spell = SpellChecker()

def check_word(word: str):
    word = word.strip().lower()
    if len(word) > 1 and spell.known([word]):
        now = datetime.datetime.now().strftime("%H:%M:%S %Y-%m-%d")
        return {
            "type": "word",
            "text": word,
            "active_time": monkey_state.active_time,
            "timestamp": now
        }
    return None

async def typing_monkey():
    while True:
        if monkey_state.is_running:
            letter = generate_random_letter()
            monkey_state.letter_history += letter
            monkey_state.active_time += 0.001

            broadcast_message = {"type": "letter", "text": letter, "active_time": monkey_state.active_time}
            if letter == " ":
                if monkey_state.current_word.strip():
                    word_info = check_word(monkey_state.current_word)
                    if word_info:
                        monkey_state.found_words.append({
                            "text": word_info["text"],
                            "timestamp": word_info["timestamp"]
                        })
                        save_found_words()
                        broadcast_message = word_info
                monkey_state.current_word = ""
            else:
                monkey_state.current_word += letter

            for connection in monkey_state.active_connections:
                try:
                    await connection.send_json(broadcast_message)
                except:
                    pass

            await asyncio.sleep(0.001)
        else:
            await asyncio.sleep(0.1)

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_found_words()
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
        "words": monkey_state.found_words,
        "active_time": monkey_state.active_time
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

