from fastapi.testclient import TestClient
import pytest
from backend.main import app

client = TestClient(app)

def test_chat_stream():
    payload = {"message": "Hello"}

    with client.stream("POST", "/chat/stream", json=payload) as response:
        assert response.status_code == 200
        content = ""
        for chunk in response.iter_text():
            if chunk == "[[END]]":
                break
            content += chunk
        print(content)

