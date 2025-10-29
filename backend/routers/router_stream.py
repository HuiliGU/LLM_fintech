from fastapi import APIRouter, Request, File, UploadFile
import pandas as pd
from backend.core import llm_client
from fastapi.responses import StreamingResponse
import os, io
from collections import defaultdict


chat_router = APIRouter()
qwen_agent = llm_client.QwenV3()
chat_historys = defaultdict(list)


def generate(messages):
    if messages:
        for chunk in qwen_agent.send_text_message(messages):
            yield chunk  
        yield "[[END]]"


@chat_router.post("/text")
async def chat_in_text(request: Request):
    """
    Endpoint to handle text messages, 
    stream a generated response
    """
    data = await request.json()
    message = data.get("message", "")
    user_id = data.get("user_id", "anonymous")
    chat_history = chat_historys[user_id]
    chat_history.append({"role": "user", "content": message})

    return StreamingResponse(generate(chat_history), media_type="text/plain")


@chat_router.post("/upload_file")
async def chat_with_file(request: Request):
    """
    Endpoint to handle both CSV and Excel file uploads, 
    read them into pandas DataFrame, 
    and stream a generated response based on the data.
    """
    # Get form data from the request
    form = await request.form()
    uploaded_file = form.get("file")
    user_id = form.get("user_id", "anonymous")
    chat_history = chat_historys[user_id]

    filename = uploaded_file.filename
    ext = os.path.splitext(filename)[1].lower()

    # Read content safely
    content = await uploaded_file.read()
    if ext in [".txt", ".csv"]:
        df = pd.read_csv(io.BytesIO(content))
    elif ext in [".xls", ".xlsx"]:
        df = pd.read_excel(io.BytesIO(content))
    else:
        return {"error": "Unsupported file type"}
    
    message = f"Answer questions based on data in {df.head(5).to_dict()}"
    chat_history.append({"role": "user", "content": message})

    return None
