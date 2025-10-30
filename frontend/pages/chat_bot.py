import streamlit as st
import io, base64
import requests
from PIL import Image
import pandas as pd

# ------------------ Initialization ------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Ask me anything..."}]

if "displayed_files" not in st.session_state:
    st.session_state.displayed_files = set()

# ------------------ Display Chat History ------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("type") == "Dataframe":
            st.dataframe(msg["content"])
        elif msg.get("type") == "Image":
            st.image(msg["content"])
        else:
            st.markdown(msg["content"])

# ------------------ Helper Functions ------------------
def stream_response(response, placeholder):
    """Stream backend response to placeholder"""
    full_response = ""
    try:
        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
            if chunk == "[[END]]":
                break
            full_response += chunk
            placeholder.markdown(full_response + "▌")
    except Exception as e:
        placeholder.markdown(f"❌ Stream error: {e}")
    return full_response


def handle_file_upload(file_obj):
    """Handle uploaded CSV / Excel / Image"""
    st.session_state.messages.append({"role": "assistant", "content": ""})
    with st.chat_message("assistant"):
        placeholder = st.empty()

    msg_type = ""
    data = None
    response = None

    try:
        response = requests.post(
            "http://127.0.0.1:8000/chat/upload_file",
            files={"file": (file_obj.name, file_obj, file_obj.type)},
            timeout=30,
        )

        if response.status_code == 200:
            result = response.json()
            msg_type = result["msg_type"]
            data = result["data"]

            if msg_type == "Dataframe":
                data = pd.DataFrame(data)
                placeholder.dataframe(data)

            elif msg_type == "Image":
                data = io.BytesIO(base64.b64decode(data))
                placeholder.image(data)

            else:
                placeholder.markdown(f"❌ Unsupported type: {msg_type}")

            # Save to chat history
            st.session_state.messages[-1].update({"type": msg_type, "content": data})

        else:
            err_msg = response.json().get("detail", "Unknown error")
            st.error(f"❌ Upload failed with {response.status_code}: {err_msg}")

    except Exception as e:
        if response is not None:
            err_msg = response.text
            st.error(f"❌ Upload failed ({response.status_code}): {err_msg}")
        else:
            st.error(f"❌ Request failed: {e}")



def handle_user_message(user_text):
    """Handle user text message and stream assistant reply"""
    # --- Display user message ---
    st.session_state.messages.append({"role": "user", "content": user_text})
    st.session_state.messages.append({"role": "assistant", "content": ""})

    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        placeholder = st.empty()

        try:
            response = requests.post(
                "http://127.0.0.1:8000/chat/text",
                json={"message": user_text},
                stream=True,
                timeout=30,
            )
            full_response = stream_response(response, placeholder)
            st.session_state.messages[-1]["content"] = full_response
            placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.session_state.messages[-1]["content"] = f"Error occurred: {e}"

# ------------------ Sidebar File Upload ------------------
st.sidebar.header("📂 Upload Files")
uploaded_files = st.sidebar.file_uploader(
    label="Upload CSV / Excel / Image",
    type=["csv", "txt", "xlsx", "png", "jpg", "jpeg"],
    accept_multiple_files=True,
)

if uploaded_files:
    for f in uploaded_files:
        if f.name not in st.session_state.displayed_files:
            st.session_state.displayed_files.add(f.name)
            with st.spinner("Uploading and processing file..."):
                handle_file_upload(f)

# ------------------ Chat Input ------------------
user_input = st.chat_input("💬 Ask anything")
if user_input:
    handle_user_message(user_input)
