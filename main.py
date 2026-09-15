import traceback
from typing import Optional
from pathlib import Path
from sqlalchemy import func
from ai_gateway import AIUnavailableError
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from schemas import (
    DiagnosticRequest, ChatRequest,
    RegisterRequest, LoginRequest, UserOut,
    User, Alumno, ChatMessage, AlumnoTema, AssignTopicRequest,
    ParentLoginRequest
)
import services
import auth as auth_service

TEMAS_CURRICULO_BALMORAL = [
    {
        "codigo": "topic-1",
        "nombre": "Estructura Atómica y Tabla Periódica",
        "descripcion": "Modelos atómicos, niveles de energía, electrones de valencia y propiedades periódicas.",
        "progreso_inicial": 65,
        "estado_inicial": "En Progreso",
        "deduccion_inicial": "Guiada"
    },
    {
        "codigo": "topic-2",
        "nombre": "Enlace Químico y Geometría Molecular",
        "descripcion": "Enlaces iónicos, covalentes y metálicos; polaridad y estructuras de Lewis.",
        "progreso_inicial": 40,
        "estado_inicial": "En Progreso",
        "deduccion_inicial": "Inicial"
    },
    {
        "codigo": "topic-3",
        "nombre": "Reacciones Químicas y Estequiometría",
        "descripcion": "Balanceo de ecuaciones, concepto de mol, reactivo limitante y rendimiento de reacción.",
        "progreso_inicial": 15,
        "estado_inicial": "En Progreso",
        "deduccion_inicial": "Inicial"
    },
    {
        "codigo": "topic-4",
        "nombre": "Soluciones, Solubilidad y pH",
        "descripcion": "Molaridad, soluciones acuosas, escala de pH, ácidos, bases y neutralización.",
        "progreso_inicial": 0,
        "estado_inicial": "Asignado",
        "deduccion_inicial": "Inicial"
    },
    {
        "codigo": "topic-5",
        "nombre": "Termoquímica y Cinética Química",
        "descripcion": "Reacciones exotérmicas y endotérmicas, entalpía y velocidad de reacción.",
        "progreso_inicial": 0,
        "estado_inicial": "Asignado",
        "deduccion_inicial": "Inicial"
    },
    {
        "codigo": "topic-6",
        "nombre": "Química Orgánica Fundamental",
        "descripcion": "Hidrocarburos, grupos funcionales (alcoholes, aldehídos) y nomenclatura IUPAC.",
        "progreso_inicial": 0,
        "estado_inicial": "Asignado",
        "deduccion_inicial": "Inicial"
    }
]

def ensure_student_topics(db: Session, alumno_id: int):
    """Asegura que el alumno tenga asignados los temas base del currículo de Química."""
    existing = db.query(AlumnoTema).filter(AlumnoTema.alumno_id == alumno_id).all()
    if not existing:
        for t in TEMAS_CURRICULO_BALMORAL:
            at = AlumnoTema(
                alumno_id=alumno_id,
                tema_codigo=t["codigo"],
                tema_nombre=t["nombre"],
                estado=t["estado_inicial"],
                progreso=t["progreso_inicial"],
                nivel_deduccion=t["deduccion_inicial"],
                asignado_por="Profesor / Sistema Balmoral"
            )
            db.add(at)
        db.commit()
        existing = db.query(AlumnoTema).filter(AlumnoTema.alumno_id == alumno_id).all()
    return existing


# Crear tablas en SQLite si no existen
Base.metadata.create_all(bind=engine)

# Auto-seed de usuarios demo para producción si la base de datos es nueva
try:
    _db_init = next(get_db())
    if _db_init.query(User).count() == 0:
        import seed_users
        seed_users.seed()
except Exception as _e:
    print(f"[STARTUP] Seed check: {_e}")

app = FastAPI(
    title="Tutor Socrático Balmoral",
    description="Plataforma de tutoría socrática con IA para Preparatoria Balmoral",
    version="3.0.0",
)

# --- Manejo Global de Errores ---
@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor", "code": "internal_error"},
    )

# --- Frontend ---
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


# ─────────────────────────────────────────────
# Rutas de páginas (HTML)
# ─────────────────────────────────────────────

@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    user = auth_service.get_current_user(request, db)
    if user:
        # Si ya está logueado, redirigir según rol
        if user.rol == "alumno":
            return RedirectResponse(url="/dashboard", status_code=302)
        else:
            return RedirectResponse(url="/dashboard-teacher", status_code=302)
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/onboarding")
def onboarding(request: Request, db: Session = Depends(get_db)):
    user = auth_service.get_current_user(request, db)
    if not user:
        return RedirectResponse("/", status_code=302)
    if user.rol != "alumno":
        return RedirectResponse("/dashboard-teacher", status_code=302)
    alumno_profile = None
    if user and user.rol == "alumno":
        alumno_profile = auth_service.get_alumno_profile(db, user.id)
    return templates.TemplateResponse(
        request=request,
        name="onboarding.html",
        context={"user": user, "alumno": alumno_profile}
    )

@app.get("/dashboard")
def dashboard(request: Request, preview_student_id: Optional[int] = None, db: Session = Depends(get_db)):
    user = auth_service.get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    is_preview = False
    target_user = user

    if user.rol in ("maestro", "admin") and preview_student_id:
        student_user = db.query(User).filter(User.id == preview_student_id, User.rol == "alumno").first()
        if student_user:
            target_user = student_user
            is_preview = True
    elif user.rol != "alumno":
        return RedirectResponse("/dashboard-teacher", status_code=302)

    alumno = auth_service.get_alumno_profile(db, target_user.id)
    if not alumno or not alumno.grado:
        if is_preview:
            alumno = auth_service.update_alumno_profile(db, target_user.id, grado="2do Bachillerato", nivel="Intermedio")
        else:
            return RedirectResponse("/onboarding", status_code=302)

    topics = ensure_student_topics(db, alumno.id)
    if topics:
        avg_prog = sum(t.progreso for t in topics) / len(topics)
        alumno.progreso_global = round(avg_prog, 1)
        db.commit()

    badges = services.compute_student_badges(db, target_user.id)

    return templates.TemplateResponse(
        request=request,
        name="dashboard_student.html",
        context={
            "user": target_user,
            "alumno": alumno,
            "topics": topics,
            "curriculum": TEMAS_CURRICULO_BALMORAL,
            "badges": badges,
            "is_preview": is_preview,
            "real_user": user
        }
    )


def teacher_data(db):
    from database import vector_collection
    pairs = db.query(User, Alumno).outerjoin(Alumno, Alumno.user_id == User.id).filter(User.rol == "alumno").order_by(User.nombre).all()
    ids = [f"diag_{u.id}" for u, _ in pairs]
    available = True
    try:
        data = vector_collection.get(ids=ids, include=["documents"]) if ids else {"ids": [], "documents": []}
        docs = dict(zip(data["ids"], data["documents"]))
    except Exception:
        docs, available = {}, False

    counts = dict(db.query(ChatMessage.id_alumno, func.count(func.distinct(ChatMessage.session_id))).filter(ChatMessage.role == "user").group_by(ChatMessage.id_alumno).all())

    students_list = []
    topic_summary_map = {t["codigo"]: {"nombre": t["nombre"], "total_progreso": 0, "count": 0} for t in TEMAS_CURRICULO_BALMORAL}

    for u, p in pairs:
        if p:
            topics = ensure_student_topics(db, p.id)
        else:
            topics = []

        topics_data = []
        for t in topics:
            topics_data.append({
                "codigo": t.tema_codigo,
                "nombre": t.tema_nombre,
                "estado": t.estado,
                "progreso": t.progreso,
                "nivel_deduccion": t.nivel_deduccion,
                "asignado_por": t.asignado_por
            })
            if t.tema_codigo in topic_summary_map:
                topic_summary_map[t.tema_codigo]["total_progreso"] += t.progreso
                topic_summary_map[t.tema_codigo]["count"] += 1

        avg_progress = round(sum(t.progreso for t in topics) / len(topics), 1) if topics else (p.progreso_global if p else 0)

        students_list.append({
            "id": u.id,
            "alumno_id": p.id if p else None,
            "name": f"{u.nombre} {u.apellido}",
            "email": u.email,
            "grade": p.grado if p else "2do Bachillerato",
            "level": p.nivel if p else "Intermedio",
            "style": p.estilo_aprendizaje if p else "Visual",
            "diagnostic": docs.get(f"diag_{u.id}", ""),
            "sessions": counts.get(str(u.id), 0),
            "progreso_global": avg_progress,
            "racha": p.racha_dias if p else 0,
            "codigo_padre": p.codigo_padre if p else "",
            "topics": topics_data
        })

    analytics = {
        "topics_overview": [
            {
                "codigo": code,
                "nombre": info["nombre"],
                "promedio": round(info["total_progreso"] / info["count"], 1) if info["count"] > 0 else 0
            }
            for code, info in topic_summary_map.items()
        ],
        "deduction_distribution": {
            "Inicial": sum(1 for s in students_list if any(t["nivel_deduccion"] == "Inicial" for t in s["topics"])),
            "Guiada": sum(1 for s in students_list if any(t["nivel_deduccion"] == "Guiada" for t in s["topics"])),
            "Autónoma": sum(1 for s in students_list if any(t["nivel_deduccion"] == "Autónoma" for t in s["topics"]))
        }
    }

    return students_list, available, analytics


@app.get("/dashboard-teacher")
def dashboard_teacher(request: Request, db: Session = Depends(get_db)):
    user = auth_service.get_current_user(request, db)
    if not user:
        return RedirectResponse("/", status_code=302)
    if user.rol not in ("maestro", "admin"):
        raise HTTPException(403, "Acceso exclusivo para docentes")
    rows, vector_available, analytics = teacher_data(db)
    return templates.TemplateResponse(
        request=request,
        name="dashboard_teacher.html",
        context={
            "user": user,
            "students": rows,
            "vector_available": vector_available,
            "analytics": analytics,
            "curriculum": TEMAS_CURRICULO_BALMORAL,
            "completed": sum(bool(r["diagnostic"]) for r in rows),
            "sessions": sum(r["sessions"] for r in rows)
        }
    )


@app.post("/api/teacher/assign-topic")
def assign_topic(request: Request, req: AssignTopicRequest, db: Session = Depends(get_db)):
    user = auth_service.require_user(request, db)
    if user.rol not in ("maestro", "admin"):
        raise HTTPException(403, "Acceso exclusivo para docentes")
    
    alumno = db.query(Alumno).filter(Alumno.id == req.alumno_id).first()
    if not alumno:
        alumno = db.query(Alumno).filter(Alumno.user_id == req.alumno_id).first()
    if not alumno:
        raise HTTPException(404, "Alumno no encontrado")

    at = db.query(AlumnoTema).filter(
        AlumnoTema.alumno_id == alumno.id,
        AlumnoTema.tema_codigo == req.tema_codigo
    ).first()

    if not at:
        at = AlumnoTema(
            alumno_id=alumno.id,
            tema_codigo=req.tema_codigo,
            tema_nombre=req.tema_nombre,
            estado=req.estado,
            progreso=req.progreso,
            nivel_deduccion=req.nivel_deduccion,
            asignado_por=f"{user.nombre} {user.apellido}"
        )
        db.add(at)
    else:
        at.estado = req.estado
        at.progreso = req.progreso
        at.nivel_deduccion = req.nivel_deduccion
        at.asignado_por = f"{user.nombre} {user.apellido}"

    db.commit()

    all_topics = db.query(AlumnoTema).filter(AlumnoTema.alumno_id == alumno.id).all()
    if all_topics:
        alumno.progreso_global = round(sum(t.progreso for t in all_topics) / len(all_topics), 1)
        db.commit()

    return {"message": "Tema asignado y actualizado correctamente", "alumno_id": alumno.id, "progreso_global": alumno.progreso_global}


@app.get("/api/teacher/students")
def teacher_students(request: Request, db: Session = Depends(get_db)):
    user = auth_service.require_user(request, db)
    if user.rol not in ("maestro", "admin"):
        raise HTTPException(403, "Acceso exclusivo para docentes")
    rows, available, analytics = teacher_data(db)
    return {"students": rows, "vector_available": available, "analytics": analytics}


@app.get("/dashboard-teacher/report")
def teacher_institutional_report(request: Request, db: Session = Depends(get_db)):
    """Genera el informe institucional ejecutivo imprimible/PDF para la Dirección y Docentes."""
    user = auth_service.get_current_user(request, db)
    is_demo = False
    if not user or user.rol not in ("maestro", "admin"):
        is_demo = True
        demo_teacher = db.query(User).filter(User.rol == "maestro").first()
        user = demo_teacher or User(
            id=0,
            nombre="Directora Martha",
            apellido="Balmoral",
            email="directora.demo@balmoral.example",
            rol="maestro",
            institucion="Colegio Balmoral",
            avatar="👩‍🏫"
        )
    
    rows, available, analytics = teacher_data(db)
    
    return templates.TemplateResponse(
        request=request,
        name="report_teacher.html",
        context={
            "user": user,
            "students": rows,
            "analytics": analytics,
            "curriculum": TEMAS_CURRICULO_BALMORAL,
            "fecha_reporte": datetime.now().strftime("%d de %B de %Y"),
            "is_demo": is_demo
        }
    )


@app.post("/api/quiz/challenge")
def get_socratic_challenge(request: Request, db: Session = Depends(get_db)):
    """Activa un micro-desafío socrático lúdico de 3 preguntas para el alumno."""
    user = auth_service.require_user(request, db)
    if user.rol != "alumno":
        raise HTTPException(403, "Exclusivo para alumnos")
    
    alumno = auth_service.get_alumno_profile(db, user.id)
    topics = ensure_student_topics(db, alumno.id)
    active_topic = next((t for t in topics if t.estado != "Dominado"), topics[0] if topics else None)
    
    topic_name = active_topic.tema_nombre if active_topic else "Química General"
    challenge_text = (
        f"🎯 ¡Desafío Socrático Activado sobre **{topic_name}**!\n\n"
        f"**Pregunta 1 de 3:** Imagina que tienes una muestra de sal de mesa (NaCl) y un trozo de azúcar (C₁₂H₂₂O₁₁). "
        f"Al disolverlos en agua, solo uno conduce la electricidad. ¿Cuál crees que sea y qué tipo de enlace químico lo explica?"
    )
    return {
        "topic": topic_name,
        "challenge_text": challenge_text
    }



@app.get("/health")
def health(db: Session = Depends(get_db)):
    from sqlalchemy import text
    db.execute(text("SELECT 1"))
    return {"status": "ok"}


@app.get("/learning")
def learning(request: Request, topic: Optional[str] = None, preview_student_id: Optional[int] = None, db: Session = Depends(get_db)):
    user = auth_service.get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    is_preview = False
    target_user = user

    if user.rol in ("maestro", "admin") and preview_student_id:
        student_user = db.query(User).filter(User.id == preview_student_id, User.rol == "alumno").first()
        if student_user:
            target_user = student_user
            is_preview = True
    elif user.rol != "alumno":
        return RedirectResponse("/dashboard-teacher", status_code=302)

    alumno = auth_service.get_alumno_profile(db, target_user.id)
    if not alumno or not alumno.grado:
        if is_preview:
            alumno = auth_service.update_alumno_profile(db, target_user.id, grado="2do Bachillerato", nivel="Intermedio")
        else:
            return RedirectResponse("/onboarding", status_code=302)
    
    topics = ensure_student_topics(db, alumno.id)
    active_topic = next((t for t in topics if t.tema_codigo == topic), topics[0] if topics else None)

    return templates.TemplateResponse(
        request=request,
        name="learning.html",
        context={
            "user": target_user,
            "alumno": alumno,
            "topics": topics,
            "active_topic": active_topic,
            "curriculum": TEMAS_CURRICULO_BALMORAL,
            "is_preview": is_preview,
            "real_user": user
        }
    )


@app.get("/privacy")
def privacy(request: Request):
    return templates.TemplateResponse(request=request, name="privacy.html")

@app.get("/legal")
def legal(request: Request):
    return templates.TemplateResponse(request=request, name="legal.html")

@app.get("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    auth_service.logout_user(request, db)
    resp = RedirectResponse(url="/", status_code=302)
    resp.delete_cookie("session_token")
    return resp


# ─────────────────────────────────────────────
# Rutas del Portal de Padres de Familia (Código)
# ─────────────────────────────────────────────

@app.get("/padres")
def parent_portal_landing(request: Request, codigo: Optional[str] = None, db: Session = Depends(get_db)):
    """Página de acceso para padres de familia con código."""
    if codigo:
        return RedirectResponse(f"/padres/dashboard?codigo={codigo.strip().upper()}", status_code=302)
    return templates.TemplateResponse(
        request=request,
        name="portal_parent_login.html",
        context={}
    )


@app.post("/api/padres/login")
def parent_login(req: ParentLoginRequest, request: Request, response: Response, db: Session = Depends(get_db)):
    """Valida el código familiar del alumno y establece la sesión para el padre."""
    user, alumno, token = auth_service.login_parent_by_code(db, req.codigo)
    response.set_cookie(
        key="session_token", value=token,
        httponly=True, max_age=30*24*3600, samesite="lax",
        secure=auth_service.is_secure_request(request)
    )
    return {
        "message": "Acceso familiar verificado",
        "student_name": f"{user.nombre} {user.apellido}",
        "redirect": "/padres/dashboard"
    }


@app.get("/padres/dashboard")
def parent_dashboard(request: Request, response: Response, codigo: Optional[str] = None, db: Session = Depends(get_db)):
    """Dashboard para padres: progreso curricular y resumen de conversaciones con QuimiBot."""
    from datetime import timedelta
    from schemas import SessionToken
    
    user = None
    alumno = None

    if codigo:
        found = auth_service.get_alumno_by_parent_code(db, codigo)
        if found:
            alumno, user = found
            token = auth_service.generate_token()
            session = SessionToken(
                token=token,
                user_id=user.id,
                expires_at=datetime.now(timezone.utc) + timedelta(days=30)
            )
            db.add(session)
            db.commit()
            response.set_cookie(
                key="session_token", value=token,
                httponly=True, max_age=30*24*3600, samesite="lax",
                secure=auth_service.is_secure_request(request)
            )

    if not user:
        user = auth_service.get_current_user(request, db)
        if not user:
            return RedirectResponse(url="/padres", status_code=302)
        alumno = auth_service.get_alumno_profile(db, user.id)

    if not alumno:
        return RedirectResponse(url="/padres", status_code=302)

    topics = ensure_student_topics(db, alumno.id)
    if topics:
        avg_prog = sum(t.progreso for t in topics) / len(topics)
        alumno.progreso_global = round(avg_prog, 1)
        db.commit()

    # Generar / obtener síntesis para padres
    summary_data = services.generate_parent_summary(db, user.id)

    # Obtener historial de conversaciones agrupadas
    chat_rows = db.query(ChatMessage).filter(
        ChatMessage.id_alumno == str(user.id)
    ).order_by(ChatMessage.id.desc()).limit(60).all()

    # Agrupar mensajes por session_id
    sessions_dict = {}
    for m in reversed(chat_rows):
        s_id = m.session_id or "default"
        if s_id not in sessions_dict:
            sessions_dict[s_id] = {
                "session_id": s_id,
                "first_date": m.timestamp,
                "messages": []
            }
        sessions_dict[s_id]["messages"].append({
            "role": m.role,
            "content": m.content,
            "timestamp": m.timestamp
        })

    sessions_list = list(sessions_dict.values())
    sessions_list.reverse()

    return templates.TemplateResponse(
        request=request,
        name="dashboard_parent.html",
        context={
            "user": user,
            "alumno": alumno,
            "topics": topics,
            "curriculum": TEMAS_CURRICULO_BALMORAL,
            "parent_summary": summary_data.get("summary", ""),
            "has_conversations": summary_data.get("has_conversations", False),
            "sessions_list": sessions_list,
            "total_messages": len(chat_rows),
            "codigo_padre": alumno.codigo_padre,
            "is_parent": True
        }
    )


@app.post("/api/padres/refresh-summary")
def refresh_parent_summary(request: Request, db: Session = Depends(get_db)):
    """Regenera la síntesis de IA para padres con los últimos datos."""
    user = auth_service.require_user(request, db)
    summary_data = services.generate_parent_summary(db, user.id, force_refresh=True)
    return {"summary": summary_data.get("summary", "")}



# ─────────────────────────────────────────────
# API de Autenticación
# ─────────────────────────────────────────────

@app.post("/api/register")
def register(req: RegisterRequest, request: Request, response: Response, db: Session = Depends(get_db)):
    """Registra un nuevo usuario (alumno o maestro) y crea sesión automáticamente."""
    user = auth_service.register_user(
        db, req.nombre, req.apellido, req.email, req.password, req.rol, req.codigo_docente
    )
    _, token = auth_service.login_user(db, req.email, req.password)
    response.set_cookie(
        key="session_token", value=token,
        httponly=True, max_age=30*24*3600, samesite="lax",
        secure=auth_service.is_secure_request(request)
    )
    return {
        "message": "Registro exitoso",
        "user": {"id": user.id, "nombre": user.nombre, "email": user.email, "rol": user.rol},
        "redirect": "/onboarding" if user.rol == "alumno" else "/dashboard-teacher"
    }

@app.post("/api/login")
def login(req: LoginRequest, request: Request, response: Response, db: Session = Depends(get_db)):
    """Inicia sesión y establece cookie de sesión segura."""
    user, token = auth_service.login_user(db, req.email, req.password)
    response.set_cookie(
        key="session_token", value=token,
        httponly=True, max_age=30*24*3600, samesite="lax",
        secure=auth_service.is_secure_request(request)
    )
    redirect = "/dashboard" if user.rol == "alumno" else "/dashboard-teacher"
    return {
        "message": "Sesión iniciada",
        "user": {"id": user.id, "nombre": user.nombre, "email": user.email, "rol": user.rol},
        "redirect": redirect
    }

@app.get("/api/me")
def get_me(request: Request, db: Session = Depends(get_db)):
    """Devuelve el usuario autenticado actual."""
    user = auth_service.get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="No autenticado")
    alumno = auth_service.get_alumno_profile(db, user.id) if user.rol == "alumno" else None
    return {
        "id": user.id,
        "nombre": user.nombre,
        "apellido": user.apellido,
        "email": user.email,
        "rol": user.rol,
        "alumno": {
            "grado": alumno.grado if alumno else "",
            "nivel": alumno.nivel if alumno else "Básico",
            "progreso_global": alumno.progreso_global if alumno else 0.0,
            "racha_dias": alumno.racha_dias if alumno else 0,
            "total_sesiones": alumno.total_sesiones if alumno else 0,
            "estilo_aprendizaje": alumno.estilo_aprendizaje if alumno else "Visual",
        } if alumno else None
    }


# ─────────────────────────────────────────────
# API de Diagnóstico y Chat
# ─────────────────────────────────────────────

@app.post("/api/diagnostic")
def save_diagnostic(request: Request, req: DiagnosticRequest, db: Session = Depends(get_db)):
    """Guarda el diagnóstico inicial del alumno en ChromaDB y SQLite."""
    user = auth_service.require_user(request, db)
    if user.rol != "alumno":
        raise HTTPException(403, "Se requiere una cuenta de alumno")
    services.save_diagnostic_to_vector_db(str(user.id), req.nivel_academico,
        req.conocimiento_previo, req.dificultades, req.estilo_aprendizaje)
    auth_service.update_alumno_profile(db, user.id, grado=req.grado,
        nivel=req.nivel_academico, estilo=req.estilo_aprendizaje,
        conocimiento=req.conocimiento_previo, dificultades=req.dificultades)
    return {"message": "Diagnóstico guardado correctamente", "id_alumno": str(user.id)}

@app.get("/api/chat/history")
def chat_history(request: Request, session_id: str, db: Session = Depends(get_db)):
    user = auth_service.require_user(request, db)
    rows = db.query(ChatMessage).filter(ChatMessage.id_alumno == str(user.id),
        ChatMessage.session_id == session_id).order_by(ChatMessage.id.desc()).limit(100).all()
    return {"messages": [{"role": m.role, "content": m.content} for m in reversed(rows)]}

@app.post("/api/tutor")
def chat_tutor(request: Request, req: ChatRequest, db: Session = Depends(get_db)):
    user = auth_service.require_user(request, db)
    if user.rol != "alumno":
        raise HTTPException(403, "Se requiere una cuenta de alumno")
    try:
        tutor_data = services.generate_tutor_response(db, req.session_id, str(user.id), req.mensaje_alumno)
    except AIUnavailableError as exc:
        raise HTTPException(503, str(exc)) from None
    alumno = auth_service.get_alumno_profile(db, user.id)
    if alumno:
        alumno.total_sesiones = db.query(func.count(func.distinct(ChatMessage.session_id))).filter(ChatMessage.id_alumno == str(user.id), ChatMessage.role == "user").scalar()
        db.commit()
    return {"respuesta": tutor_data["respuesta"], "image_url": tutor_data.get("image_url")}


@app.get("/pitch")
@app.get("/presentacion")
def business_pitch_deck(request: Request):
    """Página ejecutiva de presentación comercial y pitch B2B para colegios e inversionistas."""
    return templates.TemplateResponse(request=request, name="pitch.html")


@app.get("/manual")
@app.get("/guia")
def interactive_user_manual(request: Request):
    """Manual interactivo gamificado para Alumnos, Docentes y Padres."""
    return templates.TemplateResponse(request=request, name="manual.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
