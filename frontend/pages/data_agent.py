import streamlit as st
from utils.agent_helper import handle_file_upload, handle_user_message

# ------------------ Initialization ------------------
page_id = "data_agent"

if f"{page_id}_uploaded_files" not in st.session_state:
    st.session_state[f"{page_id}_uploaded_files"] = set()

if f"{page_id}_messages" not in st.session_state:
    st.session_state[f"{page_id}_messages"] = [{"role": "assistant", "content": "Ask me anything..."}]

# ------------------ Display Chat History ------------------
for msg in st.session_state[f"{page_id}_messages"]:
    with st.chat_message(msg["role"]):
        if msg.get("type") == "Dataframe":
            st.dataframe(msg["content"])
        else:
            st.markdown(msg["content"])

# ------------------ Display Uploaded Files ------------------
if st.session_state[f"{page_id}_uploaded_files"]:
    st.sidebar.subheader("📄 Uploaded Files")
    for fname in st.session_state[f"{page_id}_uploaded_files"]:
        st.sidebar.write(f"- {fname}")

# ------------------ Sidebar File Upload ------------------
st.sidebar.header("📂 Upload Files")
uploaded_file = st.sidebar.file_uploader(
    label="Upload CSV / Excel",
    type=["csv", "txt", "xlsx"],
    accept_multiple_files=False,
)

if uploaded_file:
    with st.spinner("Uploading and processing file..."):
        if uploaded_file.name not in st.session_state[f"{page_id}_uploaded_files"]:
            st.session_state[f"{page_id}_uploaded_files"].add(uploaded_file.name)
            handle_file_upload(uploaded_file)

# ------------------ Chat Input ------------------
user_input = st.chat_input("💬 Try with data agent...")
if user_input:
    handle_user_message(user_input)



