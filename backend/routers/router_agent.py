from fastapi import APIRouter, Request, File, UploadFile, Form
import pandas as pd
from backend.core.data_agents import code_generator
import os
from fastapi import HTTPException
from collections import defaultdict


agent_router = APIRouter()
code_gen = code_generator.codeGenerator()
file_historys = defaultdict(dict)
chat_historys = defaultdict(list)

@agent_router.post("/text")
async def chat_in_text(request: Request):
    """
    Endpoint to handle text messages, 
    stream a generated response
    """
    data = await request.json()
    user_request = data.get("message", "")
    user_id = data.get("user_id", "anonymous")
    file_history = file_historys[user_id]
    code = code_gen.generate_code(
        user_request=user_request,
        input_data=str(file_history["data"])
    )

    return code

@agent_router.post("/upload_file")
async def upload_files(
    file: UploadFile = File(...),
    user_id: str = Form("anonymous")
):
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()

    if ext not in [".csv", ".txt", ".xls", ".xlsx"]:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    try:
        if ext in [".csv", ".txt"]:
            df = pd.read_csv(file.file)
        else:
            df = pd.read_excel(file.file)

        df = df.replace([float("inf"), float("-inf")], None)
        df = df.fillna(value=0)

        data_preview = df.head(10).to_dict(orient="records")
        file_historys[user_id] = {
            "filename": filename,
            "data": data_preview
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process {filename}: {str(e)}")

    return {"msg_type": "Dataframe","data": data_preview}
