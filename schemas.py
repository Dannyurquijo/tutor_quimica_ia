import hashlib
import secrets
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.sql import func
from database import Base


# ─────────────────────────────────────────────
# Modelos SQLAlchemy (ORM)
# ─────────────────────────────────────────────

class User(Base):
    """Usuario del sistema (alumno, maestro o padre)."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    rol = Column(String, default="alumno")  # alumno | maestro | padre
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)


class Alumno(Base):
    """Perfil académico del alumno."""
    __tablename__ = "alumnos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    grado = Column(String, default="")          # 1ro, 2do, 3ro Bachillerato
    nivel = Column(String, default="Básico")    # Básico | Intermedio | Avanzado
    estilo_aprendizaje = Column(String, default="Visual")
    conocimiento_previo = Column(Text, default="")
    dificultades = Column(Text, default="")
    progreso_global = Column(Float, default=0.0)  # 0-100
    racha_dias = Column(Integer, default=0)
    total_sesiones = Column(Integer, default=0)
    codigo_padre = Column(String, unique=True, index=True, nullable=True) # Código familiar para acceso de padres (ej. PADRE-SOF-8291)
    resumen_padres = Column(Text, default="", nullable=True)             # Resumen ejecutivo periódico para padres
    insignias = Column(Text, default="[]", nullable=True)                 # Insignias y medallas desbloqueadas (JSON)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class AlumnoTema(Base):
    """Temas asignados y progreso de temas por alumno."""
    __tablename__ = "alumno_temas"

    id = Column(Integer, primary_key=True, index=True)
    alumno_id = Column(Integer, ForeignKey("alumnos.id"), index=True)
    tema_codigo = Column(String, nullable=False)   # topic-1..topic-6
    tema_nombre = Column(String, nullable=False)
    estado = Column(String, default="Asignado")    # Asignado | En Progreso | Dominado
    progreso = Column(Integer, default=0)          # 0 - 100%
    preguntas_respondidas = Column(Integer, default=0)
    nivel_deduccion = Column(String, default="Inicial") # Inicial | Guiada | Autónoma
    asignado_por = Column(String, default="Profesor")
    fecha_asignacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class SessionToken(Base):
    """Tokens de sesión para autenticación por cookie."""
    __tablename__ = "session_tokens"

    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))


class ChatMessage(Base):
    """Historial de mensajes del chat."""
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    id_alumno = Column(String, index=True)
    role = Column(String)   # 'user' o 'model'
    content = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


# ─────────────────────────────────────────────
# Helpers de contraseñas
# ─────────────────────────────────────────────

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

def generate_token() -> str:
    return secrets.token_urlsafe(32)


# ─────────────────────────────────────────────
# Esquemas Pydantic (validación de la API)
# ─────────────────────────────────────────────

class RegisterRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    nombre: str = Field(min_length=1, max_length=100)
    apellido: str = Field(min_length=1, max_length=100)
    email: str = Field(pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$", max_length=254)
    password: str = Field(min_length=6, max_length=128)
    rol: Literal["alumno"] = "alumno"

class LoginRequest(BaseModel):
    email: str
    password: str

class DiagnosticRequest(BaseModel):
    id_alumno: str
    nivel_academico: Literal["Básico", "Intermedio", "Avanzado"]
    conocimiento_previo: str = Field(min_length=1, max_length=2000)
    dificultades: str = Field(min_length=1, max_length=2000)
    estilo_aprendizaje: str = Field(min_length=1, max_length=100)
    grado: str = Field(min_length=1, max_length=100)

class ChatRequest(BaseModel):
    id_alumno: str
    session_id: str = Field(min_length=1, max_length=128)
    mensaje_alumno: str = Field(min_length=1, max_length=4000, pattern=r"\S")

class UserOut(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str
    rol: str

    class Config:
        from_attributes = True

class AssignTopicRequest(BaseModel):
    alumno_id: int
    tema_codigo: str
    tema_nombre: str
    estado: Literal["Asignado", "En Progreso", "Dominado"] = "Asignado"
    progreso: int = Field(default=0, ge=0, le=100)
    nivel_deduccion: Literal["Inicial", "Guiada", "Autónoma"] = "Inicial"

class ParentLoginRequest(BaseModel):
    codigo: str = Field(min_length=3, max_length=50)

