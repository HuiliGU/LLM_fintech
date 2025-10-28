import os
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
import time

load_dotenv()

class QwenV3():
    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=os.getenv("HF_KEY"),
    )

    def send_message(self, content):
        completion = self.client.chat.completions.create(
            model="Qwen/Qwen3-30B-A3B-Thinking-2507:nebius",
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ],
            stream=True
        )
        for chunk in completion:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield delta.content 
            time.sleep(0.01)

        yield "[[END]]"
    