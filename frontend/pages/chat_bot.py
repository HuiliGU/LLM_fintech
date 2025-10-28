import streamlit as st
import requests

st.write("Ask the chatbot anything...")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat historys
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask anything")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": ""})
    
    # Display the user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Display empty assistant message placeholder
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

    # 调用 FastAPI 流式接口
    try:
        response = requests.post("http://127.0.0.1:8000/chat/stream", json={"message": user_input}, stream=True)
        
        full_response = ""
        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
            if chunk == "[[END]]":
                break
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")

        st.session_state.messages[-1]["content"] = full_response
        message_placeholder.markdown(full_response)
        
    except Exception as e:
        st.error(f"Error: {e}")
        st.session_state.messages[-1]["content"] = f"Error occurred: {str(e)}"


