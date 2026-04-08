from fastapi import FastAPI

print("🔥 APP STARTING...")

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend is running"}
