"""Prueba de nuevas funcionalidades: asignación de temas, gráficas y vista del alumno para el docente."""
import unittest
from fastapi.testclient import TestClient
import main
from database import SessionLocal
import auth

class NewFeaturesTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(main.app)

    def test_teacher_assign_topic_and_preview(self):
        import time
        ts = int(time.time())
        docente_email = f"docente_{ts}@balmoral.edu"
        alumno_email = f"carlos_{ts}@balmoral.edu"

        # 1. Crear usuario docente y usuario alumno
        with SessionLocal() as db:
            teacher_user = auth.register_user(db, "Maestra", "Prueba", docente_email, "password123", "maestro")
            student_user = auth.register_user(db, "Carlos", "Pérez", alumno_email, "password123", "alumno")
            auth.update_alumno_profile(db, student_user.id, grado="2do Bachillerato", nivel="Intermedio")
            student_id = student_user.id
            teacher_id = teacher_user.id

        # 2. Login como docente
        res_login_t = self.client.post("/api/login", json={"email": docente_email, "password": "password123"})
        self.assertEqual(res_login_t.status_code, 200)

        # 3. Consultar datos del docente y verificar analíticas
        res_t_dash = self.client.get("/dashboard-teacher")
        self.assertEqual(res_t_dash.status_code, 200)
        self.assertIn("Promedio de Dominio por Módulo Curricular", res_t_dash.text)

        # 4. Asignar/Actualizar un tema al alumno Carlos Pérez
        payload_assign = {
            "alumno_id": student_id,
            "tema_codigo": "topic-1",
            "tema_nombre": "Estructura Atómica y Tabla Periódica",
            "estado": "Dominado",
            "progreso": 95,
            "nivel_deduccion": "Autónoma"
        }
        res_assign = self.client.post("/api/teacher/assign-topic", json=payload_assign)
        self.assertEqual(res_assign.status_code, 200)
        self.assertEqual(res_assign.json()["message"], "Tema asignado y actualizado correctamente")

        # 5. Probar "Ver vista del alumno" (Previsualización del docente)
        res_preview = self.client.get(f"/dashboard?preview_student_id={student_id}")
        self.assertEqual(res_preview.status_code, 200)
        self.assertIn("Modo Previsualización Docente", res_preview.text)
        self.assertIn("Carlos Pérez", res_preview.text)
        self.assertIn("Estructura Atómica y Tabla Periódica", res_preview.text)

        # 6. Login como alumno y verificar que ve su tema dominado y su gráfica
        self.client.get("/logout")
        self.client.post("/api/login", json={"email": alumno_email, "password": "password123"})
        res_s_dash = self.client.get("/dashboard")
        self.assertEqual(res_s_dash.status_code, 200)
        self.assertIn("Dominado", res_s_dash.text)
        self.assertIn("Estructura Atómica y Tabla Periódica", res_s_dash.text)

        print("\nSUCCESS: Todas las pruebas de asignacion de temas, graficas y vista previa pasaron exitosamente!")

if __name__ == '__main__':
    unittest.main()
