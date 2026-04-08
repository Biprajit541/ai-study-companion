from fastapi import APIRouter
from pydantic import BaseModel
from services.llm import generate_response

router = APIRouter()

class PlanRequest(BaseModel):
    subject: str
    days: int


@router.post("/plan")
def generate_plan(req: PlanRequest):
    try:
        prompt = f"Create a {req.days}-day study plan for {req.subject}."

        response = generate_response([
            {"role": "system", "content": "You create structured study plans."},
            {"role": "user", "content": prompt}
        ])

        return {"plan": response}

    except Exception as e:
        return {"error": str(e)}
