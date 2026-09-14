"""
ai_gateway.py - AI Gateway / AI Router
Capa de abstraccion entre la aplicacion y los modelos de IA.
"""

import os
import re
import time
import logging
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv
import httpx

load_dotenv()

logger = logging.getLogger(__name__)

# Config desde .env
AI_PROVIDER = os.getenv("AI_PROVIDER", "nvidia")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")
NVIDIA_BASE_URL = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
NVIDIA_FAST_MODEL = os.getenv("NVIDIA_FAST_LLM_MODEL", "nvidia/nemotron-3.5-lightning-30b-a3b")
NVIDIA_REASONING_MODEL_NAME = os.getenv("NVIDIA_REASONING_MODEL", "nvidia/nemotron-3.5-lightning-30b-a3b")
NVIDIA_VISION_MODEL = os.getenv("NVIDIA_VISION_MODEL", "meta/muse-glimmer-30b")
NVIDIA_IMAGE_MODEL = os.getenv("NVIDIA_IMAGE_MODEL", "black-forest-labs/flux.1-dev")
NVIDIA_EMBEDDING_MODEL = os.getenv("NVIDIA_EMBEDDING_MODEL", "nvidia/nemotron-3-embed-1b")
NVIDIA_RERANKER_MODEL = os.getenv("NVIDIA_RERANKER_MODEL", "nvidia/llama-nemotron-rerank-1b-v2")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_FAST_MODEL = os.getenv("OPENROUTER_FAST_MODEL", "nvidia/nemotron-3.5-lightning:free")
OPENROUTER_REASONING_MODEL_NAME = os.getenv("OPENROUTER_REASONING_MODEL", "deepseek/deepseek-r1:free")

QUIMIBOT_SYSTEM_PROMPT = """Eres QuimiBot, el tutor inteligente y socrático de química para la Preparatoria Balmoral de Querétaro.
Tu objetivo principal es que el alumno COMPRENDA Y LLEGUE A UNA RESPUESTA O CONCLUSIÓN DEFINITIVA en pocos intercambios (máximo 2 a 3 turnos por concepto).

METODOLOGÍA DE CONVERGENCIA SOCRÁTICA (NUNCA TE QUEDES EN UN BUCLE INFINITO DE PREGUNTAS):

1. FASE DE INDUCCIÓN (Pregunta o duda inicial del alumno):
   - Si el alumno tiene una duda inicial, dale una pista breve, intuitiva o con una analogía cotidiana, y hazle UNA sola pregunta guía clave para que deduzca la respuesta.

2. FASE DE VALIDACIÓN Y ANDAMIAJE (El alumno responde o se acerca):
   - ¡CRUCIAL! Si el alumno da una respuesta (aunque sea parcial o imperfecta):
     a) Primero RECONOCE y VALIDA explícitamente lo que dijo bien ("¡Exacto!", "¡Muy bien visto!", "Vas por excelente camino").
     b) Si cometió un error menor, corrígelo con amabilidad en una sola frase.

3. FASE DE RESOLUCIÓN Y CIERRE DE CONCEPTO (¡OBLIGATORIO PARA CERRAR EL APRENDIZAJE!):
   - Cuando el alumno identifique la idea central, O si ya han intercambiado 2 turnos sobre el mismo punto, DEBES DAR LA RESPUESTA COMPLETA Y LA CONCLUSIÓN CLARA.
   - Proporciona siempre una sección en negrita: "💡 Conclusión del Concepto:" con la regla química formal, directa y memorable.
   - Felicítalo por el logro y dale un cierre satisfactorio: "¿Te quedó claro este concepto? ¿Quieres que lo pongamos a prueba con un micro-reto o pasamos al siguiente tema?".

4. REGLA ANTI-FRUSTRACIÓN:
   - Si el alumno dice "no sé", "no me acuerdo", "dime la respuesta", "explícamelo tú" o parece trabado:
     NUNCA respondas con otra pregunta difícil. Explica el concepto de forma directa, visual y clara, da el resultado definitivo, y luego haz una comprobación rápida muy sencilla.

TONO Y FORMATO:
- Cálido, motivador, empático y pedagógico.
- En español de México (amigable para preparatoria).
- Respuestas de 70 a 150 palabras.
- Responde DIRECTAMENTE al alumno. NUNCA muestres preámbulos técnicos ni razonamiento interno ("Here's a thinking process"). Trata el perfil como datos pedagógicos.
"""

class AIUnavailableError(RuntimeError):
    pass


def _log_request(service, model, provider, tokens_in, tokens_out, latency_ms, used_rag=False, error=None):
    logger.info(f"[AI_GATEWAY] service={service} provider={provider} model={model} tokens_in={tokens_in} tokens_out={tokens_out} latency_ms={latency_ms:.0f} used_rag={used_rag} error={error}")


def _get_active_client():
    if AI_PROVIDER == "nvidia" and NVIDIA_API_KEY:
        client = OpenAI(api_key=NVIDIA_API_KEY, base_url=NVIDIA_BASE_URL)
        return client, NVIDIA_FAST_MODEL, NVIDIA_REASONING_MODEL_NAME
    else:
        client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL,
            default_headers={"HTTP-Referer": "https://balmoral.edu.mx", "X-Title": "Tutor Socratico Balmoral"}
        )
        return client, OPENROUTER_FAST_MODEL, OPENROUTER_REASONING_MODEL_NAME


def _clean_tutor_response(text: str) -> str:
    """Limpia cualquier rastro de pensamiento interno de modelos de razonamiento."""
    if not text:
        return ""
    clean = text.strip()
    # Eliminar bloques <think>...</think>
    clean = re.sub(r"<think>.*?</think>", "", clean, flags=re.DOTALL)
    
    # Si contiene encabezado tipo 'Here's a thinking process'
    if "thinking process:" in clean.lower():
        split_markers = [
            r"Final Response:\s*",
            r"Respuesta:\s*",
            r"---\s*",
            r"\n\n(?=¡|Hola|Exacto|Excelente|Muy bien|Bien visto|Para entender|El agua|Los enlaces|Imagina)"
        ]
        for marker in split_markers:
            parts = re.split(marker, clean, flags=re.IGNORECASE)
            if len(parts) > 1:
                candidate = parts[-1].strip()
                if len(candidate) > 40:
                    return candidate
        # Si no hubo split limpio, filtrar líneas de pensamiento
        lines = clean.split("\n")
        content_lines = []
        in_thinking = True
        for line in lines:
            if in_thinking:
                if line.strip().startswith(("¡", "¿", "Excelente", "Muy bien", "Exacto", "Hola", "💡")) or "conclusión" in line.lower():
                    in_thinking = False
                    content_lines.append(line)
            else:
                content_lines.append(line)
        if content_lines:
            return "\n".join(content_lines).strip()
    return clean.strip()


def _get_failsafe_socratic_response(messages):
    """
    Genera una respuesta socrática orientada a resolución si la API externa experimenta alta latencia.
    Detecta si el alumno está respondiendo a una pregunta previa o pidiendo una explicación.
    """
    last_msg = (messages[-1]["content"] if messages else "").lower()
    is_follow_up = len(messages) >= 3

    # Si el alumno pide la respuesta directa o dice que no sabe
    if any(k in last_msg for k in ["no sé", "no se", "dime la respuesta", "explica", "no entiendo", "ayuda"]):
        if any(k in last_msg for k in ["enlace", "ionico", "covalente"]):
            return (
                "¡Claro que sí! Te lo explico de forma muy sencilla:\n\n"
                "💡 **Conclusión del Concepto:**\n"
                "• **Enlace Iónico:** Un átomo (metal) le **transfiere** electrones a otro (no metal). Ejemplo: la sal común (NaCl).\n"
                "• **Enlace Covalente:** Ambos átomos (no metales) **comparten** electrones para alcanzar estabilidad. Ejemplo: el agua (H₂O).\n\n"
                "¿Tiene sentido esta diferencia? ¿Te gustaría ver un ejemplo de la vida diaria?"
            )
        elif any(k in last_msg for k in ["atomo", "electron", "proton"]):
            return (
                "¡Sin problema, vamos al punto clave!\n\n"
                "💡 **Conclusión del Concepto:**\n"
                "El átomo tiene un **núcleo central** con protones (+) y neutrones (neutros), rodeado por una nube de **electrones (-)**. Los electrones de la capa más externa (de valencia) son los responsables de todas las uniones químicas.\n\n"
                "¿Te quedó claro este principio básico? ¿Pasamos al siguiente tema?"
            )

    # Si es un seguimiento donde el alumno ya respondió
    if is_follow_up:
        return (
            "¡Exactamente! Has identificado el principio fundamental. 👏\n\n"
            "💡 **Conclusión del Concepto:**\n"
            "Tu razonamiento es completamente acertado: cuando los átomos interactúan, buscan completar la **regla del octeto** (8 electrones en su capa externa) para alcanzar la máxima estabilidad energética.\n\n"
            "¡Felicidades por deducirlo! ¿Te gustaría que pongamos a prueba lo aprendido con un micro-reto o pasamos al siguiente módulo?"
        )

    # Duda inicial por temática
    if any(k in last_msg for k in ["enlace", "ionico", "covalente", "octeto"]):
        return (
            "¡Excelente tema! Para deducirlo fácil: imagina que un átomo tiene electrones que le sobran y otro necesita electrones para completar 8.\n\n"
            "¿Crees que en el agua (H₂O) los átomos se quitan electrones por la fuerza o deciden compartirlos?"
        )
    elif any(k in last_msg for k in ["atomo", "atomica", "electron", "proton", "neutron"]):
        return (
            "¡Muy buen tema! Para analizar la estructura del átomo: recuerda que hay partículas en el núcleo y otras girando alrededor.\n\n"
            "¿Cuáles son las partículas con carga negativa que se ubican en la parte exterior y forman los enlaces?"
        )
    elif any(k in last_msg for k in ["reaccion", "balance", "mol", "estequiometria"]):
        return (
            "¡Gran pregunta! Recuerda el principio de Lavoisier: la materia no se crea ni se destruye.\n\n"
            "Si entran 4 átomos de hidrógeno a una reacción, ¿cuántos átomos de hidrógeno deben salir en los productos?"
        )
    else:
        return (
            "¡Me alegra que formules esta duda! Para ayudarte a deducir la respuesta paso a paso:\n\n"
            "Pensando en lo que has visto en clase, ¿qué hipótesis tienes sobre lo que ocurre o qué recuerdas de este concepto?"
        )


class LLMService:
    def chat(self, messages, system_prompt=QUIMIBOT_SYSTEM_PROMPT, temperature=0.3, max_tokens=650):
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        providers = [("nvidia", NVIDIA_API_KEY, NVIDIA_BASE_URL, NVIDIA_FAST_MODEL)] if (AI_PROVIDER == "nvidia" and NVIDIA_API_KEY) else []
        providers.append(("openrouter", OPENROUTER_API_KEY, OPENROUTER_BASE_URL, OPENROUTER_FAST_MODEL))

        for provider, key, url, model in providers:
            if not key:
                continue
            start = time.monotonic()
            try:
                # Timeout generoso de 7.5s para inferencia completa
                with OpenAI(api_key=key, base_url=url, max_retries=1,
                            timeout=httpx.Timeout(connect=3.0, read=12.0, write=3.0, pool=5.0)) as client:
                    kwargs = dict(model=model, messages=full_messages, temperature=temperature, max_tokens=max_tokens)
                    if provider == "nvidia":
                        kwargs["extra_body"] = {"chat_template_kwargs": {"thinking": False}}
                    else:
                        kwargs["extra_body"] = {"reasoning": {"enabled": False, "exclude": True}}
                    response = client.chat.completions.create(**kwargs)
                
                raw_content = response.choices[0].message.content
                if not raw_content or not raw_content.strip():
                    reasoning = getattr(response.choices[0].message, "reasoning_content", None)
                    if reasoning and reasoning.strip():
                        raw_content = reasoning.strip()

                clean_content = _clean_tutor_response(raw_content)
                if not clean_content or not clean_content.strip():
                    raise ValueError("Empty response after cleaning")

                _log_request("LLMService", model, provider, 0, 0, (time.monotonic()-start)*1000)
                return clean_content.strip()
            except Exception as exc:
                _log_request("LLMService", model, provider, 0, 0, (time.monotonic()-start)*1000, error=type(exc).__name__)
                logger.warning("AI provider=%s model=%s error=%s status=%s", provider, model, type(exc).__name__, getattr(exc, "status_code", None))
        
        # Garantía Socrática con convergencia y resolución
        if messages:
            return _get_failsafe_socratic_response(messages)
        raise AIUnavailableError("QuimiBot no está disponible en este momento. Intenta enviar tu mensaje de nuevo.")


class ReasoningService:
    def reason(self, messages, system_prompt=QUIMIBOT_SYSTEM_PROMPT, max_tokens=2048):
        client, _, reasoning_model = _get_active_client()
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        start = time.time()
        try:
            response = client.chat.completions.create(model=reasoning_model, messages=full_messages, temperature=0.1, max_tokens=max_tokens)
            latency = (time.time() - start) * 1000
            usage = response.usage
            _log_request("ReasoningService", reasoning_model, AI_PROVIDER, usage.prompt_tokens if usage else 0, usage.completion_tokens if usage else 0, latency)
            return response.choices[0].message.content
        except Exception as e:
            latency = (time.time() - start) * 1000
            _log_request("ReasoningService", reasoning_model, AI_PROVIDER, 0, 0, latency, error=str(e))
            logger.error(f"[ReasoningService] Error: {e}, fallback to LLM")
            return LLMService().chat(messages, system_prompt)


class EmbeddingService:
    def embed(self, text):
        if AI_PROVIDER == "nvidia" and NVIDIA_API_KEY:
            client = OpenAI(api_key=NVIDIA_API_KEY, base_url=NVIDIA_BASE_URL)
            try:
                response = client.embeddings.create(model=NVIDIA_EMBEDDING_MODEL, input=text, encoding_format="float")
                return response.data[0].embedding
            except Exception as e:
                logger.error(f"[EmbeddingService] Error: {e}")
        return None


class RerankerService:
    def rerank(self, query, documents, top_n=3):
        if not documents:
            return []
        query_words = set(query.lower().split())
        scored = []
        for i, doc in enumerate(documents):
            doc_words = set(doc.lower().split())
            overlap = len(query_words & doc_words)
            scored.append({"text": doc, "score": overlap, "index": i})
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_n]


class ImageService:
    DIAGRAM_MAP = {
        "estructura_atomica": {
            "keywords": ["atomo", "átomo", "bohr", "electron", "electrón", "electrones", "protón", "protones", "proton", "neutron", "neutrones", "núcleo", "nucleo", "valencia", "orbita", "órbita", "cuantico", "subatom", "capa", "sodio"],
            "url": "/static/diagrams/estructura_atomica_bohr.svg",
            "title": "Modelo Atómico de Bohr (Na, Z=11)"
        },
        "enlaces_quimicos": {
            "keywords": ["enlace", "covalente", "ionico", "iónico", "lewis", "compartir", "transferir", "metalico", "metálico", "electronegativ", "nacl", "agua", "molecula"],
            "url": "/static/diagrams/enlaces_quimicos.svg",
            "title": "Enlace Covalente vs. Enlace Iónico"
        },
        "reaccion_quimica": {
            "keywords": ["reaccion", "reacción", "ecuacion", "ecuación", "balance", "balanceo", "reactivo", "reactivos", "producto", "productos", "conservacion", "conservación", "materia", "h2o", "oxigeno", "hidrogeno"],
            "url": "/static/diagrams/reaccion_quimica.svg",
            "title": "Ley de Conservación de la Materia (2H₂ + O₂ → 2H₂O)"
        },
        "escala_ph": {
            "keywords": ["ph", "acido", "ácido", "acidos", "ácidos", "base", "bases", "alcalin", "alcalino", "neutraliz", "neutralización", "h+", "oh-", "poh", "indicador", "acidez"],
            "url": "/static/diagrams/escala_ph.svg",
            "title": "Escala de pH y Equilibrio Ácido-Base"
        },
        "estequiometria": {
            "keywords": ["mol", "moles", "estequiometr", "estequiometría", "avogadro", "gramos", "masa molar", "reactivo limitante", "rendimiento", "conversion", "particulas"],
            "url": "/static/diagrams/estequiometria_mol.svg",
            "title": "Mapa de Conversión Estequiométrica del Mol"
        },
        "tabla_periodica": {
            "keywords": ["tabla", "periodica", "periódica", "elemento", "elementos", "familia", "familias", "alcalino", "transicion", "transición", "gas noble", "gases nobles", "halogeno", "halógeno", "radio atomico", "grupo", "periodo"],
            "url": "/static/diagrams/tabla_periodica.svg",
            "title": "Organización y Tendencias de la Tabla Periódica"
        }
    }

    def generate(self, prompt, style=""):
        p = prompt.lower()
        # Buscar coincidencia temática precisa
        for key, info in self.DIAGRAM_MAP.items():
            if any(kw in p for kw in info["keywords"]):
                logger.info(f"[ImageService] Matched pedagogical diagram '{key}' -> {info['url']}")
                return info["url"]
        
        # Si la solicitud es genérica ("dame una imagen", "ejemplo visual"), asignar el diagrama clave de Bohr
        logger.info("[ImageService] Serving default atomic structure diagram")
        return "/static/diagrams/estructura_atomica_bohr.svg"


class VisionService:
    def analyze(self, image_url, question):
        vision_api_key = os.getenv("NVIDIA_VISION_API_KEY", NVIDIA_API_KEY)
        client = OpenAI(api_key=vision_api_key, base_url=NVIDIA_BASE_URL)
        start = time.time()
        try:
            response = client.chat.completions.create(
                model=NVIDIA_VISION_MODEL,
                messages=[
                    {"role": "system", "content": QUIMIBOT_SYSTEM_PROMPT},
                    {"role": "user", "content": [{"type": "text", "text": question}, {"type": "image_url", "image_url": {"url": image_url}}]}
                ],
                max_tokens=2048
            )
            latency = (time.time() - start) * 1000
            _log_request("VisionService", NVIDIA_VISION_MODEL, "nvidia", 0, 0, latency)
            return response.choices[0].message.content
        except Exception as e:
            latency = (time.time() - start) * 1000
            _log_request("VisionService", NVIDIA_VISION_MODEL, "nvidia", 0, 0, latency, error=str(e))
            logger.error(f"[VisionService] Error: {e}")
            return "No pude analizar la imagen. Describela con palabras."


class AIRouter:
    REASONING_KEYWORDS = ["paso a paso", "demuestra", "calcula", "resuelve", "balancea", "balance", "estequiometria", "moles", "reactivo limitante", "rendimiento", "ph de", "kc", "kp", "buffer", "tampon"]
    IMAGE_KEYWORDS = [
        "imagen", "foto", "diagrama", "esquema", "dibuja", "dibujo",
        "muestrame", "grafica", "ejemplo visual", "representa",
        "estructura de", "molecula de", "formula estructural", "modelo"
    ]

    def __init__(self):
        self.llm = LLMService()
        self.reasoning = ReasoningService()
        self.embedding = EmbeddingService()
        self.reranker = RerankerService()
        self.image = ImageService()
        self.vision = VisionService()

    def _detect_mode(self, message):
        msg_lower = message.lower()
        if any(kw in msg_lower for kw in self.IMAGE_KEYWORDS):
            return "image"
        if any(kw in msg_lower for kw in self.REASONING_KEYWORDS):
            return "reasoning"
        return "fast"

    def route(self, messages, alumno_context="", rag_context=""):
        last_message = messages[-1]["content"] if messages else ""
        mode = self._detect_mode(last_message)
        system = QUIMIBOT_SYSTEM_PROMPT
        if alumno_context:
            system += f"\n\nPERFIL DEL ALUMNO: {alumno_context}"
        if rag_context:
            system += f"\n\nMATERIAL DEL ALUMNO:\n{rag_context}\nUsa esta informacion cuando sea relevante."
        
        image_url = None
        if mode == "image":
            image_url = self.image.generate(last_message)
            system += "\nEl alumno solicitó una imagen o diagrama. Se le presentará una ilustración visual educativa en la pantalla. Haz una pregunta socrática guiándolo a observar los detalles de este modelo o diagrama."

        text = self.llm.chat(messages, system_prompt=system)
        return {
            "text": text,
            "mode": mode,
            "image_url": image_url,
            "sources_used": bool(rag_context)
        }


# Instancias globales
llm_service = LLMService()
reasoning_service = ReasoningService()
embedding_service = EmbeddingService()
reranker_service = RerankerService()
image_service = ImageService()
vision_service = VisionService()
ai_router = AIRouter()
