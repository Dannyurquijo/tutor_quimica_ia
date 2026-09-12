# 🧪 Tutor de Química IA - Plataforma Educativa Inteligente

Plataforma educativa de química basada en inteligencia artificial (IA Socrática con NVIDIA AI / Nemotron), diseñada para estudiantes, profesores e instituciones educativas.

---

## ✨ Características Principales

- **🎓 Interfaz para Estudiantes**:
  - Chatbot pedagógico socrático que guía sin dar respuestas directas.
  - Fondo animado e interactivo de química (partículas y enlaces atómicos) estilo retina display / iOS.
  - Sistema de gamificación con vitrina de 7 insignias (Átomo Principiante, Reacción en Cadena, Maestro de Enlaces, etc.).
  - Retos socráticos (`Quiz Challenge`) interactivos con retroalimentación inmediata.
  - Código único para compartir avances con padres de familia.

- **👨‍👩‍👧 Portal para Padres (`/padres`)**:
  - Acceso privado mediante código de vinculación familiar (ej. `PADRE-SOF-1079`).
  - Resumen ejecutivo generado por IA sobre las fortalezas, dudas recurrentes y avances del alumno.
  - Historial y transcripciones de conversaciones con el tutor.

- **🏫 Portal para Profesores y Directivos (`/dashboard-teacher`)**:
  - Métricas institucionales de uso, retención y nivel de dominio conceptual.
  - Reporte institucional imprimible / PDF listo para comités académicos (`/dashboard-teacher/report`).

---

## 🛠️ Stack Tecnológico

- **Backend**: Python 3.10+, FastAPI, Uvicorn
- **Base de Datos**: SQLite con migraciones automáticas (`database.py`)
- **IA / LLM**: NVIDIA AI Foundation Endpoints (Llama-3.1 / Nemotron) con fallback inteligente
- **Frontend**: Jinja2 Templates, HTML5 Canvas interactivo, TailwindCSS, FontAwesome

---

## 🚀 Despliegue en la Nube (Render.com)

1. **Build Command**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Command**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

3. **Variables de Entorno (Environment Variables)**:
   - `NVIDIA_API_KEY`: Tu clave de API de NVIDIA NIM (opcional si usas modo demo/fallback)
   - `JWT_SECRET`: Llave secreta para sesiones seguras

---

## 💻 Ejecución Local

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Iniciar servidor de desarrollo:
   ```bash
   python -m uvicorn main:app --reload --port 8000
   ```

3. Acceder en el navegador:
   - Inicio / Login: `http://localhost:8000`
   - Portal Padres: `http://localhost:8000/padres`
   - Dashboard Profesor: `http://localhost:8000/dashboard-teacher`
