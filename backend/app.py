from fastapi import FastAPI

print("🔥 APP STARTING...")

app = FastAPI()

app.include_router(chat.router)
app.include_router(planner.router)
app.include_router(notes.router)

@app.get("/")
def root():
    return {"message": "Backend is running"}
