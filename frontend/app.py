import streamlit as st
import requests

st.set_page_config(page_title="AI Chat Demo")

st.write("This is an AI chatbot based on **Qwen3-30B-A3B-Thinking-2507**")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Ask anything")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": ""})
    placeholder = st.empty()

    # 调用 FastAPI 流式接口
    response = requests.post("http://127.0.0.1:8000/chat/stream", json={"message": user_input}, stream=True)

    for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
        if chunk == "[[END]]":
            break
        st.session_state.messages[-1]["content"] += chunk
        # 刷新 UI
        with placeholder.container():
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])


