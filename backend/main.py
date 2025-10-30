from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers.router_stream import chat_router
from backend.routers.router_agent import agent_router

app = FastAPI(title="AI Agent routers")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/chat", tags=["text", "upload_file"])
app.include_router(agent_router, prefix="/agent", tags=["text", "upload_file"])