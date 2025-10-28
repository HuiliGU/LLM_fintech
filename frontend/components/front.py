import streamlit as st
import websocket
import threading
import time

st.set_page_config(page_title="Chat Demo", page_icon="💬")
st.title("💬Chat Demo")

# 初始化状态
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "ws" not in st.session_state:
    try:
        ws = websocket.WebSocket()
        ws.connect("ws://localhost:8000/chat/ws")
        st.session_state["ws"] = ws
    except Exception as e:
        st.error(f"WebSocket连接失败: {e}")
        st.stop()

def stream_reply(user_text: str, ws: websocket, msg: list):
    """发送消息并实时接收WebSocket流式回复"""
    ws.send(user_text)
    reply = ""
    while True:
        chunk = ws.recv()
        print(chunk)
        if chunk == "[[END]]":
            break
        reply += chunk
        msg[-1]["content"] = reply

# 输入框
user_input = st.chat_input("输入你的消息...")

if user_input:
    # 添加用户消息
    st.session_state["messages"].append({"role": "user", "content": user_input})
    # 预留一条空消息（assistant）
    st.session_state["messages"].append({"role": "assistant", "content": ""})
    # 新线程异步接收回复
    ws = st.session_state["ws"]
    msg = st.session_state["messages"]
    threading.Thread(target=stream_reply, args=(user_input, ws, msg)).start()

# 渲染消息历史
placeholder = st.empty()
while True:
    with placeholder.container():
        for msg in st.session_state["messages"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
    # 检查是否有活跃线程
    active_threads = [t for t in threading.enumerate() if t.name != "MainThread"]
    if not active_threads:
        break
