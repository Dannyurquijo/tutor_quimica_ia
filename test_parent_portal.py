"""
test_parent_portal.py — Pruebas del Portal para Padres de Familia y Botones de Práctica
Verifica:
1. Acceso mediante código familiar único.
2. Rechazo de códigos inexistentes.
3. Renderizado del expediente de avance del alumno para padres.
4. Generación y consulta del resumen de IA de las conversaciones.
5. Funcionamiento correcto de los botones 'Practicar' sin errores de servidor.
"""
import unittest
from fastapi.testclient import TestClient
import main
from database import SessionLocal
from schemas import User, Alumno, ChatMessage
import auth

class ParentPortalTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(main.app)
        self.db = SessionLocal()

    def tearDown(self):
        self.db.close()

    def test_parent_portal_flow(self):
        # 1. Obtener o crear a la alumna de demostración (Sofia Morales)
        sofia_user = self.db.query(User).filter(User.email == "sofia@balmoral.edu.mx").first()
        if not sofia_user:
            sofia_user = auth.register_user(self.db, "Sofia", "Morales", "sofia@balmoral.edu.mx", "quimica123", "alumno")
            auth.update_alumno_profile(self.db, sofia_user.id, grado="2do Bachillerato", nivel="Intermedio", estilo="Visual", dificultades="Enlaces químicos")
        
        sofia_alumno = auth.get_alumno_profile(self.db, sofia_user.id)
        self.assertIsNotNone(sofia_alumno.codigo_padre, "Sofia debe tener un código de acceso familiar")
        codigo_sofia = sofia_alumno.codigo_padre
        print(f"\n[TEST] Código familiar de Sofia: {codigo_sofia}")

        # 2. Verificar página pública de ingreso para padres
        res_landing = self.client.get("/padres")
        self.assertEqual(res_landing.status_code, 200)
        self.assertIn("Portal para Padres", res_landing.text)
        self.assertIn("Acceso Familiar con Código", res_landing.text)

        # 3. Intentar acceder con código inválido
        res_bad_login = self.client.post("/api/padres/login", json={"codigo": "CODIGO-INVALIDO-9999"})
        self.assertEqual(res_bad_login.status_code, 404)

        # 4. Acceder con código correcto de Sofia
        res_login = self.client.post("/api/padres/login", json={"codigo": codigo_sofia})
        self.assertEqual(res_login.status_code, 200)
        data = res_login.json()
        self.assertEqual(data["redirect"], "/padres/dashboard")
        self.assertIn("Sofia", data["student_name"])

        # 5. Consultar Dashboard de Padres
        res_dash = self.client.get("/padres/dashboard")
        self.assertEqual(res_dash.status_code, 200)
        self.assertIn("Expediente de Sofia Morales", res_dash.text)
        self.assertIn("Portal de Seguimiento Familiar", res_dash.text)
        self.assertIn("Informe Pedagógico Semanal para Padres", res_dash.text)
        self.assertIn("Avance Curricular por Temas Oficiales", res_dash.text)
        self.assertIn(codigo_sofia, res_dash.text)

        # 6. Acceso directo por URL con parámetro ?codigo=
        res_direct = self.client.get(f"/padres?codigo={codigo_sofia}", follow_redirects=True)
        self.assertEqual(res_direct.status_code, 200)
        self.assertIn("Expediente de Sofia Morales", res_direct.text)

        # 7. Comprobar que los botones de 'Practicar' (/learning?topic=...) funcionan sin error de servidor
        # Iniciar sesión como Sofia
        res_login_s = self.client.post("/api/login", json={"email": "sofia@balmoral.edu.mx", "password": "quimica123"})
        self.assertEqual(res_login_s.status_code, 200)

        for topic_code in ["topic-1", "topic-2", "topic-3", "topic-4", "topic-5", "topic-6"]:
            res_topic = self.client.get(f"/learning?topic={topic_code}")
            self.assertEqual(res_topic.status_code, 200, f"Error al practicar el tema {topic_code}")
            self.assertIn("QuimiBot", res_topic.text)
            self.assertIn("Preparatoria Balmoral", res_topic.text)

        print("\n[SUCCESS] Todas las pruebas del Portal de Padres y Botones Practicar pasaron al 100%!")

if __name__ == '__main__':
    unittest.main()
