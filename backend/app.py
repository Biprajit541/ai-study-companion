from fastapi import FastAPI
from routes import chat, planner, notes

app = FastAPI()

app.include_router(chat.router)
app.include_router(planner.router)
app.include_router(notes.router)
