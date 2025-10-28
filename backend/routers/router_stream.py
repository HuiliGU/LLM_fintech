from fastapi import APIRouter, Request
import asyncio
from backend.core import llm_client
from fastapi.responses import StreamingResponse

chat_router = APIRouter()

@chat_router.post("/stream")
async def chat_stream(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    qwen_agent = llm_client.QwenV3()
    return StreamingResponse(qwen_agent.send_message(user_message), media_type="text/plain")

    






