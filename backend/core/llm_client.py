import os
from openai import OpenAI
from dotenv import load_dotenv

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
        return completion

def main():
    qwen_agent = QwenV3()
    content = "what is the capital of France"
    stream = qwen_agent.send_message(content)
    for chunk in stream:
        reply = chunk.choices[0].delta.content
        if reply:
            print(reply, end="")
    

if __name__ == "__main__":
    main()