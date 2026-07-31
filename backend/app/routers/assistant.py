from fastapi import APIRouter

router = APIRouter()


@router.post("/ask")
def ask_assistant(payload: dict):
    prompt = payload.get("question") or payload.get("prompt", "")
    reply = (
        f"I can help you with E-Setu: "
        f"{prompt or 'share a ward, drop-off point, or reward request.'}"
    )
    return {"answer": reply}
