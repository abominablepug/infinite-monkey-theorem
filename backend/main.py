import asyncio
import random
import string
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from spellchecker import SpellChecker

app = FastAPI()

class MonkeyState:
    def __init__(self):
        self.is_running = False
        self.current_word = ""
        self.letter_history = ""
        self.found_words = []

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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()


    history_check = {
        "type": "history",
        "letters": monkey_state.letter_history[-5000:],
        "words": monkey_state.found_words[-500:]
    }

    try:
        while True:
            if monkey_state.is_running:
                letter = generate_random_letter()

                monkey_state.letter_history += letter
                if len(monkey_state.letter_history) > 10000:
                    monkey_state.letter_history = monkey_state.letter_history[-10000:]

                await websocket.send_text(letter)
                
                if letter == " ":
                    if monkey_state.current_word.strip():
                        word_info = check_word(monkey_state.current_word)
                        if word_info:
                            monkey_state.found_words.append(word_info)
                            await websocket.send_json(word_info)
                    monkey_state.current_word = ""
                else:
                    monkey_state.current_word += letter

                await asyncio.sleep(0.01)
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=0.001)
                if data == "start":
                    monkey_state.is_running = True
                elif data == "stop":
                    monkey_state.is_running = False
                elif data == "reset":
                    monkey_state.current_word = ""
            except asyncio.TimeoutError:
                pass
    except WebSocketDisconnect:
        monkey_state.is_running = False
        print("Client disconnected")

