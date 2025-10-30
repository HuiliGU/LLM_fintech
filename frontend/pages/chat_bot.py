import streamlit as st
from utils.chat_helper import handle_file_upload, handle_user_message

# ------------------ Initialization ------------------
page_id = "chat_bot"

if f"{page_id}_uploaded_files" not in st.session_state:
    st.session_state[f"{page_id}_uploaded_files"] = set()

if f"{page_id}_messages" not in st.session_state:
    st.session_state[f"{page_id}_messages"] = [{"role": "assistant", "content": "Ask me anything..."}]

# ------------------ Display Chat History ------------------
for msg in st.session_state[f"{page_id}_messages"]:
    with st.chat_message(msg["role"]):
        if msg.get("type") == "Dataframe":
            st.dataframe(msg["content"])
        elif msg.get("type") == "Image":
            st.image(msg["content"])
        else:
            st.markdown(msg["content"])

# ------------------ Display Uploaded Files ------------------
if st.session_state[f"{page_id}_uploaded_files"]:
    st.sidebar.subheader("📄 Uploaded Files")
    for fname in st.session_state[f"{page_id}_uploaded_files"]:
        st.sidebar.write(f"- {fname}")

# ------------------ Sidebar File Upload ------------------
st.sidebar.header("📂 Upload Files")
uploaded_files = st.sidebar.file_uploader(
    label="Upload CSV / Excel / Image",
    type=["csv", "txt", "xlsx", "png", "jpg", "jpeg"],
    accept_multiple_files=True,
)

if uploaded_files:
    for f in uploaded_files:
        if f.name not in st.session_state[f"{page_id}_uploaded_files"]:
            st.session_state[f"{page_id}_uploaded_files"].add(f.name)
            with st.spinner("Uploading and processing file..."):
                handle_file_upload(f)

# ------------------ Chat Input ------------------
user_input = st.chat_input("💬 Ask anything")
if user_input:
    handle_user_message(user_input)

