from fastapi import FastAPI
from app.routers import note_router, user_router


from dotenv import load_dotenv
import os



app = FastAPI()

load_dotenv()
secret = os.getenv("SECRET")

@app.get("/")
def health():
    return {"status": "ok"}


app.include_router(note_router)
app.include_router(user_router)