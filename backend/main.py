from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers.router_stream import chat_router

app = FastAPI(title="聊天应用（模块化 Router）")

# 跨域设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载路由
app.include_router(chat_router, prefix="/chat", tags=["stream"])
