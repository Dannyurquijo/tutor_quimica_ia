import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# Probar con el modelo nemotron gratuito de NVIDIA en OpenRouter
try:
    response = client.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-a55b:free",
        messages=[{"role": "user", "content": "Hola, soy un estudiante de quimica. Presenta brevemente quien eres."}],
        max_tokens=200
    )
    print("Modelo: nvidia/nemotron-3-ultra-550b-a55b:free")
    print("Respuesta:", response.choices[0].message.content)
except Exception as e:
    print("Error:", e)
