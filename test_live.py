import json, urllib.request, time
time.sleep(3)
req = urllib.request.Request(
    "http://localhost:8000/api/tutor",
    data=json.dumps({"session_id": "test-demo", "id_alumno": "sofia-123", "mensaje_alumno": "Hola QuimiBot, quiero estudiar enlaces quimicos"}).encode(),
    headers={"Content-Type": "application/json"}
)
try:
    with urllib.request.urlopen(req, timeout=40) as r:
        data = json.loads(r.read())
        print("STATUS: OK")
        print("Respuesta QuimiBot:")
        print(data.get("respuesta", data))
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code, e.read().decode())
except Exception as e:
    print("Error:", type(e).__name__, e)
