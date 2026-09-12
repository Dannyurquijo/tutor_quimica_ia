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
    print("Respuesta completa:")
    print(response)
    print("Content:", response.choices[0].message.content)
    print("Role:", response.choices[0].message.role)
    # Check if there's reasoning content
    msg = response.choices[0].message
    if hasattr(msg, 'reasoning_content'):
        print("Reasoning:", msg.reasoning_content)
except Exception as e:
    print("Error:", type(e).__name__, e)
