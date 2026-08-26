import asyncio
import json
import urllib.error
import urllib.request

from fastapi import APIRouter, HTTPException
from starlette import status

from config.settings import settings
from schemas.ai import AIChatRequest
from utils.response import success_response

router = APIRouter(prefix="/api/ai", tags=["ai"])


def _call_ai_provider(payload: dict) -> dict:
    request = urllib.request.Request(
        settings.ai_api_endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.ai_api_key}",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=settings.ai_request_timeout) as response:
        return json.loads(response.read().decode("utf-8"))


@router.post("/chat")
async def chat(data: AIChatRequest):
    if not settings.ai_api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI chat is not configured",
        )

    payload = {
        "model": data.model or settings.ai_model,
        "messages": [message.model_dump() for message in data.messages],
        "stream": False,
    }

    try:
        provider_response = await asyncio.to_thread(_call_ai_provider, payload)
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI provider request failed: {error_body}",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI provider request failed",
        ) from exc

    content = (
        provider_response.get("choices", [{}])[0]
        .get("message", {})
        .get("content")
    )

    if not content:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI provider returned an empty response",
        )

    return success_response(data={"content": content})
