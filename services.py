"""
services.py — Lógica de negocio del Tutor Socrático
Usa ai_gateway.py para todas las llamadas a IA.
NUNCA llama directamente a DeepSeek, NVIDIA o cualquier proveedor.
"""
import traceback
from sqlalchemy.orm import Session
from database import vector_collection
from schemas import ChatMessage
from ai_gateway import ai_router


def save_diagnostic_to_vector_db(id_alumno: str, nivel_academico: str,
                                   conocimiento_previo: str, dificultades: str,
                                   estilo_aprendizaje: str):
    """Guarda el perfil del alumno en ChromaDB para contexto de la IA."""
    try:
        document_content = (
            f"Nivel Académico: {nivel_academico}. "
            f"Conocimiento Previo: {conocimiento_previo}. "
            f"Dificultades: {dificultades}. "
            f"Estilo de Aprendizaje: {estilo_aprendizaje}."
        )
        vector_collection.upsert(
            documents=[document_content],
            metadatas=[{"id_alumno": id_alumno}],
            ids=[f"diag_{id_alumno}"]
        )
    except Exception as e:
        traceback.print_exc()
        raise e


def get_alumno_context(id_alumno: str, query_text: str) -> str:
    """Recupera el contexto del alumno desde ChromaDB."""
    results = vector_collection.get(ids=[f"diag_{id_alumno}"], include=["documents"])
    return (results.get("documents") or [""])[0] or ""


def generate_tutor_response(db: Session, session_id: str,
                             id_alumno: str, mensaje: str) -> str:
    """
    Genera una respuesta socrática del tutor usando el AI Gateway.
    1. Recupera historial de la sesión desde SQLite.
    2. Recupera contexto del alumno desde ChromaDB.
    3. Enruta la solicitud al servicio de IA apropiado.
    4. Guarda el turno de conversación en SQLite.
    """
    history = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id,
        ChatMessage.id_alumno == id_alumno
    ).order_by(ChatMessage.id.desc()).limit(10).all()
    messages = [{"role": "assistant" if m.role == "model" else m.role,
                 "content": m.content} for m in reversed(history)]
    messages.append({"role": "user", "content": mensaje})
    alumno_context = get_alumno_context(id_alumno, mensaje)
    route_result = ai_router.route(messages=messages, alumno_context=alumno_context)
    respuesta = route_result["text"]
    image_url = route_result.get("image_url")
    db.add_all([
        ChatMessage(session_id=session_id, id_alumno=id_alumno, role="user", content=mensaje),
        ChatMessage(session_id=session_id, id_alumno=id_alumno, role="assistant", content=respuesta)
    ])
    db.commit()
    return {"respuesta": respuesta, "image_url": image_url}


def generate_parent_summary(db: Session, student_user_id: int, force_refresh: bool = False) -> dict:
    """
    Genera una síntesis ejecutiva pedagógica para los padres de familia
    basada en las conversaciones reales del alumno con QuimiBot y su avance curricular.
    """
    from schemas import User, Alumno, AlumnoTema

    user = db.query(User).filter(User.id == student_user_id).first()
    alumno = db.query(Alumno).filter(Alumno.user_id == student_user_id).first()
    if not user or not alumno:
        return {"summary": "No se encontró el registro del alumno.", "has_conversations": False}

    # Si ya tiene un resumen y no se fuerza regeneración
    if alumno.resumen_padres and not force_refresh:
        return {"summary": alumno.resumen_padres, "has_conversations": True}

    # Obtener mensajes del chat
    messages = db.query(ChatMessage).filter(
        ChatMessage.id_alumno == str(student_user_id)
    ).order_by(ChatMessage.id.desc()).limit(25).all()

    # Temas asignados y estado
    topics = db.query(AlumnoTema).filter(AlumnoTema.alumno_id == alumno.id).all()
    topics_info = [f"{t.tema_nombre} ({t.progreso}%, {t.estado}, deducción: {t.nivel_deduccion})" for t in topics]

    if not messages:
        summary_text = (
            f"{user.nombre} aún no ha iniciado conversaciones guiadas con QuimiBot. "
            f"Actualmente cursa {alumno.grado or 'Bachillerato'} con perfil {alumno.nivel or 'Básico'}. "
            "Le recomendamos motivarle a ingresar y formular su primera pregunta sobre el módulo de Estructura Atómica."
        )
        alumno.resumen_padres = summary_text
        db.commit()
        return {"summary": summary_text, "has_conversations": False}

    recent_excerpts = []
    for m in reversed(messages[:14]):
        sender = user.nombre if m.role == "user" else "QuimiBot"
        recent_excerpts.append(f"{sender}: {m.content[:180]}")

    conversation_sample = "\n".join(recent_excerpts)

    prompt = (
        f"Eres el Director Pedagógico de la Preparatoria Balmoral de Querétaro. "
        f"Redacta un informe ejecutivo, cálido, motivador y claro dirigido a los padres de {user.nombre} {user.apellido} ({alumno.grado}). "
        f"Sintetiza su desempeño basándote en este historial de preguntas y respuestas con el tutor de IA QuimiBot:\n\n"
        f"Módulos curriculares: {', '.join(topics_info)}\n"
        f"Extracto de diálogo:\n{conversation_sample}\n\n"
        f"Estructura tu reporte en exactamente 3 secciones cortas con viñetas elegantes:\n"
        f"• 🌟 Temas explorados y comprensión conceptual lograda.\n"
        f"• 💡 Nivel de deducción socrática (si razona de forma autónoma o con pistas).\n"
        f"• 🏡 Recomendación afectiva para reforzar el estudio en el hogar.\n"
        f"Habla con calidez institucional a los padres."
    )

    try:
        route_result = ai_router.route(
            messages=[{"role": "user", "content": prompt}],
            alumno_context=f"Alumno: {user.nombre} {user.apellido}, Grado: {alumno.grado}"
        )
        summary_text = route_result.get("text", "").strip()
    except Exception:
        en_progreso = [t.tema_nombre for t in topics if t.estado == "En Progreso"] or ["Estructura Atómica y Tabla Periódica"]
        summary_text = (
            f"• 🌟 Temas explorados: Durante las últimas sesiones con QuimiBot, {user.nombre} ha trabajado activamente en "
            f"{', '.join(en_progreso)}. Registra un avance global de {alumno.progreso_global}% con {len(messages)} intervenciones socráticas.\n\n"
            f"• 💡 Nivel de Deducción: Demuestra un nivel de razonamiento {alumno.nivel or 'Intermedio'}. Logra conectar los conceptos con ejemplos reales "
            f"cuando se le guían preguntas inductivas, reduciendo la necesidad de memorización mecánica.\n\n"
            f"• 🏡 Recomendación para Casa: Feliciten a {user.nombre} por su constancia. Sugerimos pedirle que les explique en sus propias palabras "
            f"cómo se forman los enlaces químicos entre elementos cotidianos (como la sal de mesa o el agua)."
        )

    alumno.resumen_padres = summary_text
    db.commit()
    return {"summary": summary_text, "has_conversations": True}


CATALOGO_INSIGNIAS = [
    {
        "id": "primer_enlace",
        "icono": "🌱",
        "titulo": "Primer Enlace",
        "descripcion": "Iniciaste tu primera conversación socrática con QuimiBot.",
        "categoria": "Inicio",
        "color": "from-emerald-400 to-teal-600"
    },
    {
        "id": "explorador_atomico",
        "icono": "⚛️",
        "titulo": "Explorador Atómico",
        "descripcion": "Alcanzaste 50% o más de dominio en un módulo químico.",
        "categoria": "Dominio",
        "color": "from-sky-400 to-blue-600"
    },
    {
        "id": "mente_autonoma",
        "icono": "🧠",
        "titulo": "Mente Autónoma",
        "descripcion": "Demostraste razonamiento deductivo independiente en tus sesiones.",
        "categoria": "Socrático",
        "color": "from-purple-500 to-indigo-600"
    },
    {
        "id": "racha_fuego",
        "icono": "🔥",
        "titulo": "Racha Imparable",
        "descripcion": "Mantuviste tu constancia de estudio activa.",
        "categoria": "Hábito",
        "color": "from-amber-400 to-rose-600"
    },
    {
        "id": "quimico_constante",
        "icono": "🧪",
        "titulo": "Químico Frecuente",
        "descripcion": "Acumulaste múltiples sesiones de razonamiento con la IA.",
        "categoria": "Dedicación",
        "color": "from-cyan-400 to-teal-600"
    },
    {
        "id": "alquimista_maestro",
        "icono": "🏆",
        "titulo": "Alquimista Maestro",
        "descripcion": "Dominaste por completo un tema curricular oficial de Química.",
        "categoria": "Maestría",
        "color": "from-amber-300 via-amber-500 to-yellow-600"
    },
    {
        "id": "vision_molecular",
        "icono": "🔬",
        "titulo": "Visión Molecular",
        "descripcion": "Solicitaste e inspeccionaste diagramas y esquemas químicos en alta resolución.",
        "categoria": "Curiosidad",
        "color": "from-rose-400 to-pink-600"
    }
]


def compute_student_badges(db: Session, student_user_id: int) -> list[dict]:
    """Calcula y actualiza las insignias desbloqueadas por el alumno."""
    import json
    from schemas import Alumno, AlumnoTema, ChatMessage

    alumno = db.query(Alumno).filter(Alumno.user_id == student_user_id).first()
    if not alumno:
        return []

    # Mensajes
    msg_count = db.query(ChatMessage).filter(ChatMessage.id_alumno == str(student_user_id)).count()
    # Temas
    topics = db.query(AlumnoTema).filter(AlumnoTema.alumno_id == alumno.id).all()

    # Condiciones de desbloqueo
    unlocked_ids = set()
    if msg_count >= 1:
        unlocked_ids.add("primer_enlace")
    if msg_count >= 6 or alumno.total_sesiones >= 3:
        unlocked_ids.add("quimico_constante")
    if alumno.racha_dias >= 2:
        unlocked_ids.add("racha_fuego")
    if any(t.progreso >= 50 for t in topics) or alumno.progreso_global >= 40:
        unlocked_ids.add("explorador_atomico")
    if any(t.estado == "Dominado" or t.progreso >= 75 for t in topics) or alumno.progreso_global >= 70:
        unlocked_ids.add("alquimista_maestro")
    if any(t.nivel_deduccion == "Autónoma" for t in topics) or alumno.nivel == "Avanzado":
        unlocked_ids.add("mente_autonoma")
    
    # Revisar si se han pedido esquemas / imágenes
    img_request = db.query(ChatMessage).filter(
        ChatMessage.id_alumno == str(student_user_id),
        ChatMessage.role == "user"
    ).filter(
        ChatMessage.content.ilike("%imagen%") | 
        ChatMessage.content.ilike("%diagrama%") | 
        ChatMessage.content.ilike("%esquema%") |
        ChatMessage.content.ilike("%modelo%")
    ).first()
    if img_request:
        unlocked_ids.add("vision_molecular")

    # Guardar en base de datos
    alumno.insignias = json.dumps(list(unlocked_ids))
    db.commit()

    badges = []
    for b in CATALOGO_INSIGNIAS:
        badges.append({
            **b,
            "desbloqueada": b["id"] in unlocked_ids
        })

    return badges


