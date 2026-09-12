import json, urllib.request
req = urllib.request.Request(
    "http://localhost:8000/api/tutor",
    data=json.dumps({"session_id": "test-demo", "id_alumno": "sofia-123", "mensaje_alumno": "Hola QuimiBot, quiero estudiar enlaces quimicos"}).encode(),
    headers={"Content-Type": "application/json"}
)
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
        print("OK! Respuesta de QuimiBot:")
        print(data["respuesta"])
except Exception as e:
    print("Error:", e)
