import json
import os
from urllib import error, request


def get_assistant_reply(prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        return (
            "The AI service is not configured yet, but you can still earn Green Credits by logging e-waste at a verified drop-off point. "
            "Add an OPENAI_API_KEY or GEMINI_API_KEY to enable real AI responses."
        )

    provider = "openai" if os.getenv("OPENAI_API_KEY") else "gemini"
    if provider == "openai":
        try:
            payload = {
                "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are E-Setu Assistant for a GVMC e-waste collection app. "
                            "Answer briefly, help citizens with credits, drop-off points, QR scanning, and officer workflows."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.3,
            }
            req = request.Request(
                "https://api.openai.com/v1/chat/completions",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                method="POST",
            )
            with request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"].strip()
        except (error.URLError, error.HTTPError, KeyError, IndexError, ValueError):
            return "The AI service is unavailable right now. Please try again shortly."

    try:
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": (
                                "You are E-Setu Assistant for a GVMC e-waste collection app. "
                                "Answer briefly, help citizens with credits, drop-off points, QR scanning, and officer workflows.\n\n"
                                f"User: {prompt}"
                            )
                        }
                    ]
                }
            ]
        }
        req = request.Request(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
            data=json.dumps(payload).encode("utf-8"),
            headers={"x-goes-api-key": api_key, "Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (error.URLError, error.HTTPError, KeyError, IndexError, ValueError):
        return "The AI service is unavailable right now. Please try again shortly."
