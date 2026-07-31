from fastapi import APIRouter

from app.services.ai_service import get_assistant_reply

router = APIRouter()


@router.post("/ask")
def ask_assistant(payload: dict):
    prompt = payload.get("question") or payload.get("prompt", "")
    return {"answer": get_assistant_reply(str(prompt))}
