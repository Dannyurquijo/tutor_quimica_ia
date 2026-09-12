import urllib.request, json, time
print("Enviando al chat...", flush=True)
body = json.dumps({"session_id":"session-user-1","id_alumno":"1","mensaje_alumno":"Que es un enlace ionico?"}).encode()
req = urllib.request.Request("http://localhost:8000/api/tutor", data=body, headers={"Content-Type":"application/json"})
try:
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.loads(r.read())
        print("STATUS 200 OK")
        print("RESPUESTA:", data.get("respuesta","")[:300])
except Exception as e:
    print("ERROR:", type(e).__name__, str(e)[:200])
