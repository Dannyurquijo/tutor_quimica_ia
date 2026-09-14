# -*- coding: utf-8 -*-
"""
seed_users.py — Inicializador de Cuentas Demo y Primeros Usuarios
Crea o actualiza de forma idempotente las 3 cuentas modelo para pruebas y clientes:
1. Alumno: sofia@balmoral.edu.mx / quimica123 (Código familiar: PADRE-SOF-1079)
2. Maestro / Directora: directora.demo@balmoral.example / directora123
3. Papá: Acceso mediante el código PADRE-SOF-1079 en /padres
"""
import sys
import os
from pathlib import Path

# Soporte UTF-8 en consola Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import database
import schemas
import auth
import main

def seed():
    database.Base.metadata.create_all(bind=database.engine)
    db = next(database.get_db())

    print("=" * 60)
    print("🌱 INICIALIZADOR DE USUARIOS — TUTOR SOCRÁTICO BALMORAL")
    print("=" * 60)

    # 1. ALUMNO MODELO: Sofía Morales
    student_email = "sofia@balmoral.edu.mx"
    student_user = db.query(schemas.User).filter(schemas.User.email == student_email).first()
    if not student_user:
        student_user = auth.register_user(
            db, nombre="Sofía", apellido="Morales",
            email=student_email, password="quimica123", rol="alumno"
        )
        print(f"✅ Alumno creado: {student_user.nombre} ({student_email})")
    else:
        student_user.password_hash = schemas.hash_password("quimica123")
        db.commit()
        print(f"ℹ️ Alumno ya existía: {student_email} (credenciales verificadas)")

    # Perfil de alumno y código familiar
    alumno_profile = auth.get_alumno_profile(db, student_user.id)
    alumno_profile.grado = "2do Bachillerato"
    alumno_profile.nivel = "Intermedio"
    alumno_profile.estilo_aprendizaje = "Visual"
    alumno_profile.codigo_padre = "PADRE-SOF-1079"
    alumno_profile.progreso_global = 68.5
    alumno_profile.racha_dias = 4
    alumno_profile.total_sesiones = 12
    db.commit()

    main.ensure_student_topics(db, alumno_profile.id)

    # 2. MAESTRO / DIRECTORA: Directora Martha Balmoral
    teacher_email = "directora.demo@balmoral.example"
    teacher_user = db.query(schemas.User).filter(schemas.User.email == teacher_email).first()
    if not teacher_user:
        teacher_user = schemas.User(
            nombre="Directora Martha",
            apellido="Balmoral",
            email=teacher_email,
            password_hash=schemas.hash_password("directora123"),
            rol="maestro"
        )
        db.add(teacher_user)
        db.commit()
        print(f"✅ Docente/Directora creada: {teacher_user.nombre} ({teacher_email})")
    else:
        teacher_user.password_hash = schemas.hash_password("directora123")
        teacher_user.rol = "maestro"
        db.commit()
        print(f"ℹ️ Docente ya existía: {teacher_email} (credenciales verificadas)")

    print("\n" + "=" * 60)
    print("🎉 USUARIOS LISTOS PARA USAR Y COMPARTIR:")
    print("=" * 60)
    print("1. 🎓 ALUMNO:")
    print(f"   • Correo:      {student_email}")
    print("   • Contraseña:  quimica123")
    print("   • Rol:         Alumno de Bachillerato")
    print("   • Portal:      /")
    print("\n2. 👩‍🏫 MAESTRO / DIRECTORA:")
    print(f"   • Correo:      {teacher_email}")
    print("   • Contraseña:  directora123")
    print("   • Clave Escolar de Registro: BALMORAL-DOCENTE-2026")
    print("   • Panel:       /dashboard-teacher")
    print("\n3. 👨‍👩‍👧 PADRE DE FAMILIA:")
    print("   • Acceso:      Portal para Padres (/padres)")
    print("   • Código único: PADRE-SOF-1079")
    print("   • Enlace Directo: /padres?codigo=PADRE-SOF-1079")
    print("=" * 60)

if __name__ == '__main__':
    seed()
