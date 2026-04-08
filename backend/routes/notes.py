from fastapi import APIRouter
from pydantic import BaseModel
from services.llm import generate_response

router = APIRouter()

class NotesRequest(BaseModel):
    content: str

@router.post("/summarize")
def summarize_notes(req: NotesRequest):
    try:
        prompt = f"Summarize this:\n{req.content}"

        response = generate_response([
            {"role": "system", "content": "You summarize notes."},
            {"role": "user", "content": prompt}
        ])

        return {"summary": response}

    except Exception as e:
        return {"error": str(e)}
