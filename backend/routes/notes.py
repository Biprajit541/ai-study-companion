from fastapi import APIRouter
from pydantic import BaseModel
from services.llm import generate_response

router = APIRouter()

class NotesRequest(BaseModel):
    content: str

@router.post("/summarize")
def summarize(req: NotesRequest):
    prompt = f"Summarize this into bullet points:\n{req.content}"
    summary = generate_response(prompt)
    return {"summary": summary}