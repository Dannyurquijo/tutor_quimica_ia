# Cambiar proveedor a nvidia y probar
import os
os.environ["AI_PROVIDER"] = "nvidia"
os.environ["NVIDIA_API_KEY"] = open(".env").read().split("NVIDIA_API_KEY=")[1].split()[0]
os.environ["NVIDIA_BASE_URL"] = "https://integrate.api.nvidia.com/v1"
os.environ["NVIDIA_FAST_LLM_MODEL"] = "deepseek-ai/deepseek-v4-flash-0731"

# Reload after env change
import importlib
import ai_gateway
importlib.reload(ai_gateway)

result = ai_gateway.ai_router.route([{"role": "user", "content": "Hola, soy alumna de quimica"}])
print("Modo:", result["mode"])
print("Respuesta:", result["text"][:300])
