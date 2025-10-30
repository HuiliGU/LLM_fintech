from fastapi import APIRouter, Request, File, UploadFile, Form
import pandas as pd
from backend.core import llm_client
from fastapi.responses import StreamingResponse
import io, os, base64
from collections import defaultdict
from PIL import Image


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
async def upload_file(file: UploadFile = File(...), user_id: str = Form("anonymous")):
    ext = os.path.splitext(file.filename)[1].lower()
    msg_type = ""
    data = None

    if ext in [".csv", ".txt", ".xls", ".xlsx"]:
        msg_type = "Dataframe"
        if ext in [".csv", ".txt"]:
            df = pd.read_csv(file.file)
        else:  
            df = pd.read_excel(file.file)
        
        df = df.replace([float("inf"), float("-inf")], None) 
        df = df.fillna(value=0)
        data = df.head(10).to_dict(orient="records")

    elif ext in [".jpg", ".jpeg", ".png"]:
        # Image file -> convert to base64 for frontend display
        msg_type = "Image"
        img = Image.open(file.file)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        data = base64.b64encode(buf.getvalue()).decode("utf-8")

    else:
        # Unsupported file type
        msg_type = "Error"
        data = "Unsupported file type. Please upload CSV, Excel, or Image."

    return {"msg_type": msg_type, "data": data}


