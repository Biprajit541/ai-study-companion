from fastapi import FastAPI
from routes import chat

app = FastAPI()

app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "Backend is running"}
