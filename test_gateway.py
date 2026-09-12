from ai_gateway import ai_router
print("Probando AIRouter con OpenRouter (DeepSeek V3 free)...")
result = ai_router.route([{"role": "user", "content": "Hola QuimiBot, soy nuevo aqui"}])
print("Modo detectado:", result["mode"])
print("Respuesta:")
print(result["text"])
