import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1"
)

try:
    response = client.chat.completions.create(
        model="deepseek-ai/deepseek-v4-flash-0731",
        messages=[{"role": "user", "content": "Di hola en espanol en una sola linea."}],
        max_tokens=50,
        stream=False
    )
    print("NVIDIA DeepSeek Flash OK:")
    print(response.choices[0].message.content)
except Exception as e:
    print("Error NVIDIA:", e)
