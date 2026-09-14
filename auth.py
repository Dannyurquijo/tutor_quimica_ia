"""
auth.py — Sistema de autenticación con cookies de sesión
Maneja registro, login, logout y recuperación del usuario actual.
"""
from datetime import datetime, timedelta, timezone
from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from schemas import User, Alumno, SessionToken, hash_password, verify_password, generate_token


def is_secure_request(request: Request) -> bool:
    """Detecta si la petición utiliza HTTPS directo o detrás de proxy/túnel."""
    if not request:
        return False
    if request.url.scheme == "https":
        return True
    return request.headers.get("x-forwarded-proto", "").lower() == "https"


def register_user(db: Session, nombre: str, apellido: str, email: str,
                  password: str, rol: str = "alumno", codigo_docente: str = None) -> User:
    """Crea un nuevo usuario y perfil de alumno si aplica, validando clave si es docente."""
    clean_email = email.lower().strip()
    existing = db.query(User).filter(User.email == clean_email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Este correo ya está registrado")

    if rol == "maestro":
        import os
        teacher_key = os.getenv("TEACHER_SIGNUP_KEY", "BALMORAL-DOCENTE-2026").strip()
        if not codigo_docente or codigo_docente.strip() != teacher_key:
            raise HTTPException(
                status_code=403,
                detail="Clave de activación docente inválida. Solicítala a la Dirección Escolar de Preparatoria Balmoral."
            )

    user = User(
        nombre=nombre.strip(),
        apellido=apellido.strip(),
        email=clean_email,
        password_hash=hash_password(password),
        rol=rol
    )
    db.add(user)
    db.flush()  # Para obtener el id antes del commit

    # Si es alumno, crear perfil académico inicial con su código familiar
    if rol == "alumno":
        alumno = Alumno(
            user_id=user.id,
            codigo_padre=generate_parent_code(user.id, nombre)
        )
        db.add(alumno)

    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, email: str, password: str) -> tuple[User, str]:
    """Valida credenciales y devuelve (user, token)."""
    clean_email = email.lower().strip()
    clean_password = password.strip()
    user = db.query(User).filter(User.email == clean_email).first()
    if not user or not verify_password(clean_password, user.password_hash):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Cuenta desactivada")

    # Crear token de sesión (válido 30 días)
    token = generate_token()
    session = SessionToken(
        token=token,
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=30)
    )
    db.add(session)
    db.commit()
    return user, token


def get_current_user(request: Request, db: Session) -> User | None:
    """Recupera el usuario autenticado desde la cookie de sesión."""
    token = request.cookies.get("session_token")
    if not token:
        return None

    session = db.query(SessionToken).filter(SessionToken.token == token).first()
    if not session:
        return None

    # Verificar expiración
    if session.expires_at and datetime.now(timezone.utc) > session.expires_at.replace(tzinfo=timezone.utc):
        db.delete(session)
        db.commit()
        return None

    return db.query(User).filter(User.id == session.user_id, User.is_active.is_(True)).first()


def require_user(request: Request, db: Session) -> User:
    """Como get_current_user pero lanza 401 si no está autenticado."""
    user = get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Debes iniciar sesión")
    return user


def logout_user(request: Request, db: Session):
    """Elimina el token de sesión del usuario."""
    token = request.cookies.get("session_token")
    if token:
        session = db.query(SessionToken).filter(SessionToken.token == token).first()
        if session:
            db.delete(session)
            db.commit()


def generate_parent_code(user_id: int, nombre: str) -> str:
    """Genera un código único y memorable para acceso de los padres (ej. PADRE-SOF-1079)."""
    clean_nom = "".join(c for c in nombre if c.isalnum())[:3].upper() or "ALU"
    num_suffix = (user_id * 37 + 1042) % 10000
    return f"PADRE-{clean_nom}-{num_suffix:04d}"


def get_alumno_profile(db: Session, user_id: int) -> Alumno | None:
    """Obtiene el perfil académico de un alumno y asegura su código familiar."""
    alumno = db.query(Alumno).filter(Alumno.user_id == user_id).first()
    if alumno and not alumno.codigo_padre:
        user = db.query(User).filter(User.id == user_id).first()
        nom = user.nombre if user else "ALU"
        alumno.codigo_padre = generate_parent_code(user_id, nom)
        db.commit()
        db.refresh(alumno)
    return alumno


def get_alumno_by_parent_code(db: Session, codigo: str) -> tuple[Alumno, User] | None:
    """Busca el alumno y usuario correspondiente a un código familiar."""
    from sqlalchemy import func
    clean_code = codigo.strip().upper()
    alumno = db.query(Alumno).filter(func.upper(Alumno.codigo_padre) == clean_code).first()
    if not alumno:
        return None
    user = db.query(User).filter(User.id == alumno.user_id).first()
    return (alumno, user) if user else None


def login_parent_by_code(db: Session, codigo: str) -> tuple[User, Alumno, str]:
    """Valida el código familiar y crea una sesión de acceso para el padre."""
    found = get_alumno_by_parent_code(db, codigo)
    if not found:
        raise HTTPException(status_code=404, detail="El código de acceso familiar no es válido o no existe.")
    
    alumno, user = found
    token = generate_token()
    session = SessionToken(
        token=token,
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=30)
    )
    db.add(session)
    db.commit()
    return user, alumno, token


def update_alumno_profile(db: Session, user_id: int, grado: str = None,
                           nivel: str = None, estilo: str = None,
                           conocimiento: str = None, dificultades: str = None):
    """Actualiza el perfil académico del alumno."""
    alumno = db.query(Alumno).filter(Alumno.user_id == user_id).first()
    if not alumno:
        alumno = Alumno(user_id=user_id)
        db.add(alumno)

    if not alumno.codigo_padre:
        user = db.query(User).filter(User.id == user_id).first()
        nom = user.nombre if user else "ALU"
        alumno.codigo_padre = generate_parent_code(user_id, nom)

    if grado is not None:
        alumno.grado = grado
    if nivel is not None:
        alumno.nivel = nivel
    if estilo is not None:
        alumno.estilo_aprendizaje = estilo
    if conocimiento is not None:
        alumno.conocimiento_previo = conocimiento
    if dificultades is not None:
        alumno.dificultades = dificultades

    db.commit()
    db.refresh(alumno)
    return alumno

