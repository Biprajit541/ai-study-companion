from fastapi import APIRouter
from pydantic import BaseModel
from services.llm import generate_response

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

@router.post("/chat")
def chat(req: ChatRequest):
    try:
        answer = generate_response(req.question)
        return {"response": answer}
    except Exception as e:
        return {"response": f"⚠️ Error: {str(e)}"}
