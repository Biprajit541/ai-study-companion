from fastapi import APIRouter
from pydantic import BaseModel
from services.llm import generate_response

router = APIRouter()

class PlanRequest(BaseModel):
    subject: str
    days: int

@router.post("/plan")
def create_plan(req: PlanRequest):
    prompt = f"Create a {req.days}-day study plan for {req.subject}"
    plan = generate_response(prompt)
    return {"plan": plan}