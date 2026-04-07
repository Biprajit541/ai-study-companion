from fastapi import APIRouter
from pydantic import BaseModel
from services.llm import generate_response

router = APIRouter()

class NotesRequest(BaseModel):
    content: str

@router.post("/summarize")
def summarize_notes(req: NotesRequest):
    prompt = f"Summarize the following notes:\n{req.content}"
    return {"summary": generate_response(prompt)}
