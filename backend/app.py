from fastapi import FastAPI
from routes import chat, planner, notes

print("🔥 APP STARTING...")

app = FastAPI()

app.include_router(chat.router)
app.include_router(planner.router)
app.include_router(notes.router)

@app.get("/")
def root():
    return {"message": "Backend is running"}
