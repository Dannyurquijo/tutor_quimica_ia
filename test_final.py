import os
os.environ["AI_PROVIDER"] = "nvidia"
from dotenv import load_dotenv
load_dotenv()

from ai_gateway import ai_router, AI_PROVIDER
print("Provider:", AI_PROVIDER)

result = ai_router.route([{"role": "user", "content": "Hola, soy alumna de quimica"}])
print("Modo:", result["mode"])
print("Respuesta:", result["text"][:300] if result["text"] else "VACIA")
