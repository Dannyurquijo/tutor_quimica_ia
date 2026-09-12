import os
from pathlib import Path
import chromadb
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Configuración de ChromaDB (Base de Datos Vectorial)
ROOT = Path(__file__).resolve().parent
chroma_client = chromadb.PersistentClient(path=os.getenv("CHROMA_PATH", str(ROOT / "chroma_db")))
vector_collection = chroma_client.get_or_create_collection(name="contexto_escolar")

# 2. Configuración de SQLite (Base de Datos Relacional)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///" + str(ROOT / "tutor_sqlite.db"))

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def migrate_db():
    """Asegura que todas las columnas necesarias existan en SQLite."""
    from sqlalchemy import text
    try:
        with engine.connect() as conn:
            # Revisar tabla alumnos
            res = conn.execute(text("PRAGMA table_info(alumnos)")).fetchall()
            cols = [r[1] for r in res]
            if cols:
                if "codigo_padre" not in cols:
                    conn.execute(text("ALTER TABLE alumnos ADD COLUMN codigo_padre VARCHAR"))
                if "resumen_padres" not in cols:
                    conn.execute(text("ALTER TABLE alumnos ADD COLUMN resumen_padres TEXT"))
                if "insignias" not in cols:
                    conn.execute(text("ALTER TABLE alumnos ADD COLUMN insignias TEXT DEFAULT '[]'"))
                conn.commit()
    except Exception as e:
        print(f"Warning during DB migration: {e}")

# Ejecutar migración segura
migrate_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

