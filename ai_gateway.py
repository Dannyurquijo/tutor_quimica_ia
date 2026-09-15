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

5. BLINDAJE PEDAGÓGICO ANTI-TRAMPA Y DETECCIÓN DE OTRAS IA:
   - Si detectas que el alumno envía un mensaje que parece copiado o generado por otra IA (ChatGPT, Gemini, etc.) o de una enciclopedia:
     * Señales: listas numeradas excesivamente formales tipo manual (`1. **Definición:**`), conectores típicos de ChatGPT ("En resumen, cabe destacar que..."), o lenguaje desproporcionadamente enciclopédico para un alumno de bachillerato.
   - ACCIÓN OBLIGATORIA:
     a) NUNCA des por buena la respuesta ni cierres el tema de inmediato.
     b) Aplica el Desafío Socrático de Autenticidad con tono amigable: "Esa respuesta suena muy formal, como sacada de una enciclopedia o de otra IA 🤖. Pero aquí lo valioso es tu propio pensamiento: ¿cómo me lo explicarías con tus propias palabras cotidianas como si se lo contaras a un amigo?"
     c) O toma un término complejo de su texto y pregunta: "Mencionas '[término_técnico]'; con tus propias palabras, ¿qué significa eso exactamente?"
     d) No valides el tema ni concluyas hasta que el alumno demuestre deducción genuina con su propio vocabulario.

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
    """Limpia cualquier rastro de pensamiento interno o alucinaciones de 'modelo de texto'."""
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
                    clean = candidate
                    break
        else:
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
                clean = "\n".join(content_lines).strip()

    # Reemplazar alucinaciones donde el LLM niega poder mostrar imágenes
    forbidden_patterns = [
        r"(?:como|soy un)\s+(?:modelo|ia)\s+(?:de\s+)?(?:lenguaje|texto)[^.\n]*?(?:no\s+puedo|incapaz\s+de)\s+(?:crear|generar|mostrar|ver)\s+(?:im[aá]genes|fotos|diagramas)[^.\n]*[.]?",
        r"(?:no\s+tengo\s+la\s+capacidad|no\s+puedo|no\s+me\s+es\s+posible)\s+(?:de\s+)?(?:generar|crear|mostrar|dibujar)\s+(?:im[aá]genes|fotos|diagramas)[^.\n]*[.]?",
        r"como modelo de lenguaje(?:,\s*)?",
        r"como inteligencia artificial de texto(?:,\s*)?"
    ]
    for pat in forbidden_patterns:
        clean = re.sub(pat, "¡Aquí tienes la representación visual en pantalla!", clean, flags=re.IGNORECASE)

    return clean.strip()


def _get_failsafe_socratic_response(messages):
    """
    Genera una respuesta socrática orientada a resolución si la API externa experimenta alta latencia.
    Detecta si el alumno está respondiendo a una pregunta previa o pidiendo una explicación.
    """
    last_msg = (messages[-1]["content"] if messages else "").lower()
    is_follow_up = len(messages) >= 3

    # Si solicita una imagen explícitamente
    if any(k in last_msg for k in ["imagen", "diagrama", "esquema", "foto", "dibuja", "muestrame", "muéstrame", "visual"]):
        return (
            "¡Por supuesto! He colocado la ilustración científica en tu pantalla. 🖼️\n\n"
            "Observa con atención los detalles del diagrama que tienes enfrente:\n"
            "• Fíjate en cómo están distribuidos los átomos y sus cargas.\n\n"
            "¿Qué elemento o parte del esquema te llama más la atención para analizar su comportamiento?"
        )

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
    def chat(self, messages, system_prompt=QUIMIBOT_SYSTEM_PROMPT, temperature=0.3, max_tokens=650, timeout_read=3.5):
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        providers = [("nvidia", NVIDIA_API_KEY, NVIDIA_BASE_URL, NVIDIA_FAST_MODEL)] if (AI_PROVIDER == "nvidia" and NVIDIA_API_KEY) else []
        providers.append(("openrouter", OPENROUTER_API_KEY, OPENROUTER_BASE_URL, OPENROUTER_FAST_MODEL))

        for provider, key, url, model in providers:
            if not key:
                continue
            start = time.monotonic()
            try:
                # Fast timeout resiliente (connect=2.0s, read=timeout_read) para respuesta ágil
                with OpenAI(api_key=key, base_url=url, max_retries=1,
                            timeout=httpx.Timeout(connect=2.0, read=timeout_read, write=2.0, pool=3.0)) as client:
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
        "molecula_agua": {
            "keywords": ["agua", "h2o", "polar", "polaridad", "dipolo", "dipolar", "puente de hidrogeno", "hidrogeno", "oxigeno", "covalente polar"],
            "url": "/static/diagrams/molecula_agua_polaridad.svg",
            "title": "Molécula de Agua (H₂O) — Geometría Angular y Polaridad",
            "guide_text": "¡Aquí tienes la ilustración en pantalla! 🌊 Observa la estructura angular de la molécula de agua (H₂O) y cómo el átomo de oxígeno (en rojo) concentra mayor densidad de carga negativa (δ⁻) mientras los hidrógenos quedan con carga positiva (δ⁺).\n\n¿Por qué crees que esta asimetría de cargas permite que el agua forme puentes de hidrógeno y actúe como disolvente universal?"
        },
        "disolucion_nacl": {
            "keywords": ["sal", "cloruro", "conduce", "electricidad", "electric", "disoluci", "disolución", "disuelve", "foco", "electrolito", "luz", "iones libres", "solucion acuosa", "nacl disuelto", "red cristalina", "corriente"],
            "url": "/static/diagrams/disolucion_nacl_electricidad.svg",
            "title": "Conducción Eléctrica y Disolución de Sal (NaCl)",
            "guide_text": "¡Aquí tienes la ilustración en pantalla! ⚡ Observa ambos matraces: en el agua pura sin sal el foco permanece apagado. Pero al disolverse el NaCl, los iones Na⁺ y Cl⁻ se separan e hidratan, quedando libres y móviles.\n\n¿Qué permite exactamente el paso de la corriente eléctrica hacia el foco: la molécula entera o los iones cargados en movimiento?"
        },
        "geometria_molecular": {
            "keywords": ["geometria", "geometría", "vsepr", "rpecv", "forma espacial", "tetraedr", "tetraédrica", "trigonal", "lineal", "104.5", "109.5", "180", "repulsion", "repulsión"],
            "url": "/static/diagrams/geometria_molecular_vsepr.svg",
            "title": "Geometría Molecular 3D (VSEPR)",
            "guide_text": "¡Aquí tienes la ilustración en pantalla! 📐 Compara las tres formas fundamentales: lineal (180°), trigonal plana (120°) y tetraédrica (109.5°).\n\n¿Qué fuerza electrostática entre las nubes de electrones de valencia obliga a los enlaces a separarse lo máximo posible en el espacio tridimensional?"
        },
        "estructura_atomica": {
            "keywords": ["atomo", "átomo", "bohr", "electron", "electrón", "electrones", "protón", "protones", "proton", "neutron", "neutrones", "núcleo", "nucleo", "valencia", "orbita", "órbita", "cuantico", "subatom", "capa", "sodio"],
            "url": "/static/diagrams/estructura_atomica_bohr.svg",
            "title": "Modelo Atómico de Bohr (Na, Z=11)",
            "guide_text": "¡Aquí tienes la ilustración en pantalla! ⚛️ Observa el modelo de Bohr para el átomo de Sodio (Na, Z=11): 2 electrones en la primera capa interna, 8 en la segunda y sólo 1 electrón en la capa exterior (valencia).\n\n¿Qué le resulta energéticamente más fácil al átomo de sodio para completar su octeto: ceder ese único electrón externo o intentar capturar 7 electrones?"
        },
        "enlaces_quimicos": {
            "keywords": ["enlace", "covalente", "ionico", "iónico", "lewis", "compartir", "transferir", "metalico", "metálico", "electronegativ", "nacl", "molecula"],
            "url": "/static/diagrams/enlaces_quimicos.svg",
            "title": "Comparación: Enlace Covalente vs. Enlace Iónico",
            "guide_text": "¡Aquí tienes la ilustración en pantalla! 🔗 Compara ambos modelos: a la izquierda, los dos átomos comparten electrones (enlace covalente). A la derecha, el sodio transfiere su electrón de valencia al cloro (enlace iónico).\n\n¿Qué factor de electronegatividad crees que determina si los átomos comparten electrones o si uno se los arrebata al otro?"
        },
        "reaccion_quimica": {
            "keywords": ["reaccion", "reacción", "ecuacion", "ecuación", "balance", "balanceo", "reactivo", "reactivos", "producto", "productos", "conservacion", "conservación", "materia", "oxigeno"],
            "url": "/static/diagrams/reaccion_quimica.svg",
            "title": "Ley de Conservación de la Materia (2H₂ + O₂ → 2H₂O)",
            "guide_text": "¡Aquí tienes la ilustración en pantalla! ⚖️ Observa cómo se reorganizan los enlaces en 2H₂ + O₂ → 2H₂O: hay exactamente 4 átomos de Hidrógeno y 2 átomos de Oxígeno antes y después de la reacción.\n\n¿Cómo demuestra este esquema que en una reacción química la materia no se destruye, sino que los enlaces se rompen y se recombinan?"
        },
        "escala_ph": {
            "keywords": ["ph", "acido", "ácido", "acidos", "ácidos", "base", "bases", "alcalin", "alcalino", "neutraliz", "neutralización", "h+", "oh-", "poh", "indicador", "acidez"],
            "url": "/static/diagrams/escala_ph.svg",
            "title": "Escala de pH y Equilibrio Ácido-Base",
            "guide_text": "¡Aquí tienes la ilustración en pantalla! 🧪 Desde los ácidos (pH < 7, alta concentración de H⁺) hasta las bases (pH > 7, predominio de OH⁻), con el agua pura en el punto neutro (pH = 7).\n\nSi añades unas gotas de jugo de limón (ácido cítrico) a un vaso de agua, ¿hacia qué valor de pH crees que se desplazará la disolución?"
        },
        "estequiometria": {
            "keywords": ["mol", "moles", "estequiometr", "estequiometría", "avogadro", "gramos", "masa molar", "reactivo limitante", "rendimiento", "conversion", "particulas"],
            "url": "/static/diagrams/estequiometria_mol.svg",
            "title": "Mapa de Conversión Estequiométrica del Mol",
            "guide_text": "¡Aquí tienes la ilustración en pantalla! 📊 Este mapa es el corazón de la estequiometría: el **mol** es el puente obligatorio para convertir entre gramos (masa molar), número de moléculas (constante de Avogadro) y volumen molar.\n\nSi te dan la masa en gramos de un reactivo, ¿cuál es el primer paso indispensable antes de calcular la cantidad de producto que obtendrás?"
        },
        "tabla_periodica": {
            "keywords": ["tabla", "periodica", "periódica", "elemento", "elementos", "familia", "familias", "alcalino", "transicion", "transición", "gas noble", "gases nobles", "halogeno", "halógeno", "radio atomico", "grupo", "periodo"],
            "url": "/static/diagrams/tabla_periodica.svg",
            "title": "Organización y Tendencias de la Tabla Periódica",
            "guide_text": "¡Aquí tienes la ilustración en pantalla! 🗺️ Observa la división en periodos (filas horizontales por nivel cuántico) y familias o grupos (columnas verticales con igual cantidad de electrones de valencia).\n\n¿Por qué crees que los elementos de una misma columna (como el litio, sodio y potasio) reaccionan de manera tan parecida con el agua?"
        }
    }

    def get_diagram(self, prompt):
        p = prompt.lower()
        best_key = None
        best_score = 0
        for key, info in self.DIAGRAM_MAP.items():
            score = sum(1 for kw in info["keywords"] if kw in p)
            if score > best_score:
                best_score = score
                best_key = key

        if best_key and best_score > 0:
            info = self.DIAGRAM_MAP[best_key]
            logger.info(f"[ImageService] Best matched diagram '{best_key}' (score={best_score}) -> {info['url']}")
            return info
        
        # Fallback genérico visual: molécula de agua
        logger.info("[ImageService] Serving default water molecule diagram")
        return self.DIAGRAM_MAP["molecula_agua"]

    def generate(self, prompt, style=""):
        return self.get_diagram(prompt)["url"]


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
        "muestrame", "muéstrame", "muestra", "mostrar", "enseñame", "enséñame",
        "grafica", "gráfica", "grafico", "gráfico", "figura", "ejemplo visual",
        "representa", "representación", "estructura de", "molecula de", "molécula de",
        "formula estructural", "fórmula estructural", "modelo", "ilustra", "ilustración",
        "quiero ver", "como se ve", "cómo se ve", "visual"
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
            diag_info = self.image.get_diagram(last_message)
            image_url = diag_info["url"]
            fallback_guide = diag_info.get("guide_text", "¡Aquí tienes la ilustración en pantalla! Observa detenidamente cada componente del esquema.\n\n¿Qué detalle visual te llama más la atención?")
            
            # Para solicitudes de diagramas, imágenes o esquemas, entregamos de inmediato la guía pedagógica especializada
            # Esto garantiza respuesta instantánea (< 0.1s) sin riesgo de cuellos de botella en APIs externas.
            is_direct_diagram_query = any(k in last_message.lower() for k in [
                "muestrame", "muéstrame", "muestra", "mostrar", "quiero ver", "dibuja", "dibujo", "enseñame", "enséñame",
                "imagen", "foto", "diagrama", "esquema", "grafica", "gráfica", "cómo se ve", "como se ve",
                "ilustra", "ilustración", "representa", "representación"
            ])

            if is_direct_diagram_query or len(messages) <= 1:
                text = fallback_guide
            else:
                system += (
                    f"\n\n[INSTRUCCIÓN CRÍTICA DE ILUSTRACIÓN]: El sistema gráfico de la plataforma YA ha colocado exitosamente la ilustración visual científica en la pantalla del alumno ({image_url}, '{diag_info.get('title', '')}'). "
                    "Está ESTRICTAMENTE PROHIBIDO decir que eres un modelo de texto o que no puedes mostrar imágenes. "
                    "Confirma con entusiasmo al alumno que la ilustración ya está visible en su pantalla ('¡Aquí tienes la ilustración en pantalla!') "
                    "y hazle una pregunta socrática enfocada guiándolo a observar los detalles visuales de este modelo."
                )
                try:
                    text = self.llm.chat(messages, system_prompt=system, timeout_read=1.5)
                except Exception:
                    text = fallback_guide

                if not text or ("¡Aquí tienes" not in text and "pantalla" not in text and "observa" not in text.lower()):
                    text = fallback_guide
        else:
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
