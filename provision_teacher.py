"""Crea una cuenta docente local: python provision_teacher.py"""
from getpass import getpass
from database import SessionLocal, Base, engine
import auth

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    name = input('Nombre: ').strip()
    surname = input('Apellido: ').strip()
    email = input('Correo: ').strip()
    password = getpass('Contraseña (mínimo 10 caracteres): ')
    if not name or '@' not in email or len(password) < 10:
        raise SystemExit('Datos inválidos.')
    with SessionLocal() as db:
        auth.register_user(db, name, surname, email, password, 'maestro')
    print('Cuenta docente creada.')
