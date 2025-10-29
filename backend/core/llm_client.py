import os
from openai import OpenAI
from dotenv import load_dotenv
import time

load_dotenv()

class QwenV3():
    # initial parameters
    VL_switch = False
    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=os.getenv("HF_KEY"),
    )

    def send_text_message(self, messages):
        # generate reply
        completion = self.client.chat.completions.create(
            model="Qwen/Qwen3-30B-A3B-Thinking-2507:nebius",
            messages=messages,
            stream=True
        )

        # return generator of streaming response
        for chunk in completion:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield delta.content 
            time.sleep(0.01)

        # return end flag
        yield "[[END]]"