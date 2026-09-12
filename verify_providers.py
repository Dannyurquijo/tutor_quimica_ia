"""Sondeo manual del proveedor sin imprimir credenciales."""
import ai_gateway as g
from openai import OpenAI
import time

if __name__ == '__main__':
    for provider, key, url, model in [('nvidia', g.NVIDIA_API_KEY, g.NVIDIA_BASE_URL, g.NVIDIA_FAST_MODEL), ('openrouter', g.OPENROUTER_API_KEY, g.OPENROUTER_BASE_URL, g.OPENROUTER_FAST_MODEL)]:
        print(provider, model, flush=True)
        started = time.monotonic()
        try:
            with OpenAI(api_key=key, base_url=url, timeout=20, max_retries=0) as client:
                extra = {'chat_template_kwargs': {'thinking': False}} if provider == 'nvidia' else {'reasoning': {'enabled': False, 'exclude': True}}
                response = client.chat.completions.create(model=model, messages=[{'role': 'system', 'content': g.QUIMIBOT_SYSTEM_PROMPT}, {'role': 'user', 'content': '¿Por qué el sodio pierde electrones?'}], max_tokens=400, extra_body=extra)
                print('Respuesta:', response.choices[0].message.content, flush=True)
        except Exception as exc:
            msg = str(exc)
            for secret in [g.NVIDIA_API_KEY, g.OPENROUTER_API_KEY]:
                if secret:
                    msg = msg.replace(secret, '[REDACTED]')
            print(type(exc).__name__, msg[:800], flush=True)
        print('Segundos:', round(time.monotonic()-started, 2), flush=True)
