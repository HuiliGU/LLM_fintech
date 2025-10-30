import io, base64
import requests
import pandas as pd
import streamlit as st

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


def handle_file_upload(file_obj, page_id="data_agent"):
    """Handle uploaded CSV / Excel / Image"""
    st.session_state[f"{page_id}_messages"].append({"role": "assistant", "content": ""})
    with st.chat_message("assistant"):
        placeholder = st.empty()

    msg_type = ""
    data = None
    response = None

    try:
        response = requests.post(
            "http://127.0.0.1:8000/agent/upload_file",
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

            else:
                placeholder.markdown(f"❌ Unsupported type: {msg_type}")

            # Save to chat history
            st.session_state[f"{page_id}_messages"][-1].update({"type": msg_type, "content": data})

        else:
            err_msg = response.json().get("detail", "Unknown error")
            st.error(f"❌ Upload failed with {response.status_code}: {err_msg}")

    except Exception as e:
        if response is not None:
            err_msg = response.text
            st.error(f"❌ Upload failed ({response.status_code}): {err_msg}")
        else:
            st.error(f"❌ Request failed: {e}")



def handle_user_message(user_text, page_id="data_agent"):
    """Handle user text message and stream assistant reply"""
    # --- Display user message ---
    st.session_state[f"{page_id}_messages"].append({"role": "user", "content": user_text})
    st.session_state[f"{page_id}_messages"].append({"role": "assistant", "content": ""})

    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        placeholder = st.empty()

        try:
            response = requests.post(
                "http://127.0.0.1:8000/agent/text",
                json={"message": user_text},
                stream=True,
                timeout=30,
            )
            full_response = stream_response(response, placeholder)
            st.session_state[f"{page_id}_messages"][-1]["content"] = full_response
            placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.session_state[f"{page_id}_messages"][-1]["content"] = f"Error occurred: {e}"