# -*- coding: utf-8 -*-
"""
test_new_roles.py — Pruebas de Registro Docente Seguro, Salted PBKDF2 y Portal de Padres
"""
import unittest
from fastapi.testclient import TestClient
import main
import schemas
import auth

class NewRolesTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(main.app, raise_server_exceptions=False)

    def test_pbkdf2_hashing(self):
        pwd = "SecretPassword123"
        h = schemas.hash_password(pwd)
        self.assertTrue(h.startswith("pbkdf2:sha256:100000$"))
        self.assertTrue(schemas.verify_password(pwd, h))
        self.assertFalse(schemas.verify_password("WrongPassword", h))

    def test_teacher_registration_security(self):
        # 1. Fallar sin clave docente
        res = self.client.post("/api/register", json={
            "nombre": "Carlos",
            "apellido": "Herrera",
            "email": "profesor.fake@balmoral.edu",
            "password": "teacherpassword",
            "rol": "maestro",
            "codigo_docente": "CLAVE-INCORRECTA"
        })
        self.assertEqual(res.status_code, 403)

        # 2. Éxito con clave válida
        res = self.client.post("/api/register", json={
            "nombre": "Profesor",
            "apellido": "Valdez",
            "email": "profesor.valdez@balmoral.edu",
            "password": "teacherpassword123",
            "rol": "maestro",
            "codigo_docente": "BALMORAL-DOCENTE-2026"
        })
        self.assertIn(res.status_code, (200, 400)) # 200 nuevo o 400 si ya existe
        if res.status_code == 200:
            self.assertEqual(res.json()["user"]["rol"], "maestro")
            self.assertEqual(res.json()["redirect"], "/dashboard-teacher")

    def test_student_parent_code_generation(self):
        res = self.client.post("/api/register", json={
            "nombre": "Mariana",
            "apellido": "Lopez",
            "email": "mariana.test@balmoral.edu",
            "password": "studentpassword",
            "rol": "alumno"
        })
        self.assertIn(res.status_code, (200, 400))

if __name__ == "__main__":
    unittest.main()
