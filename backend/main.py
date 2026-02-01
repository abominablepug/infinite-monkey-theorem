import random
import string
from fastapi import FastAPI

app = FastAPI()

def generate_random_letter():
    letter = random.choice(string.ascii_letters)
    return letter

@app.get("/")
def read_root():
    letters = ""
    for i in range(100):
        letters += generate_random_letter()
    return {"random_letters": letters}
