import os, re

with open("ai_gateway.py", "r", encoding="utf-8") as f:
    content = f.read()

# Fix LLMService chat: add extra_body for NVIDIA to disable thinking
old = '            response = client.chat.completions.create(model=fast_model, messages=full_messages, temperature=temperature, max_tokens=max_tokens)'
new = '''            kwargs = dict(model=fast_model, messages=full_messages, temperature=temperature, max_tokens=max_tokens)
            if AI_PROVIDER == "nvidia":
                kwargs["extra_body"] = {"chat_template_kwargs": {"thinking": False}}
            response = client.chat.completions.create(**kwargs)'''
content = content.replace(old, new)

# Fix response content: handle None content (reasoning models)
old = '            return response.choices[0].message.content'
new = '''            msg = response.choices[0].message
            return msg.content or getattr(msg, "reasoning_content", "") or ""'''
content = content.replace(old, new, 1)  # only first occurrence

with open("ai_gateway.py", "w", encoding="utf-8") as f:
    f.write(content)
print("ai_gateway.py updated")
