from fastapi import APIRouter, Request
import asyncio
from backend.core import llm_client
from fastapi.responses import StreamingResponse

chat_router = APIRouter()

@chat_router.post("/stream")
async def chat_stream(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    print("用户输入：", user_message)

    qwen_agent = llm_client.QwenV3()

    def generate():
        for chunk in qwen_agent.send_message(user_message):
            yield chunk  
        yield "[[END]]"

    return StreamingResponse(generate(), media_type="text/plain")

    






