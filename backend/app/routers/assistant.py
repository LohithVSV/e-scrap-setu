from fastapi import APIRouter

router = APIRouter()


def _build_reply(prompt: str) -> str:
    text = (prompt or "").strip().lower()

    if any(word in text for word in ["credit", "credits", "reward", "redeem"]):
        return "You earn Green Credits by logging e-waste at a verified drop-off point. You can redeem them later for bus passes and utility discounts."

    if any(word in text for word in ["drop", "drop-off", "point", "scan", "qr"]):
        return "Scan the QR code at a civic drop-off point, enter the item details, and the collection will be logged for officer confirmation."

    if any(word in text for word in ["ward", "officer", "official", "dashboard"]):
        return "Field officers confirm collections and update the ward dashboard so citizens and supervisors can track progress in real time."

    return "I can help with credits, drop-off points, QR scanning, and officer workflows for E-Setu."


@router.post("/ask")
def ask_assistant(payload: dict):
    prompt = payload.get("question") or payload.get("prompt", "")
    return {"answer": _build_reply(str(prompt))}
