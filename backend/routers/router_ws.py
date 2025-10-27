from fastapi import APIRouter, WebSocket
import asyncio
from core import llm_client

ws_router = APIRouter()

@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        query = await websocket.receive_text()
        qwen_agent = llm_client.QwenV3()
        stream = qwen_agent.send_message(query)
        for chunk in stream:
            reply = chunk.choices[0].delta.content if chunk.choices[0].delta.content else ""
            await websocket.send_text(reply)
        await websocket.send_text("[[END]]")
