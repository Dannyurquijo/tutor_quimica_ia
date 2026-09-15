/**
 * script.js — Lógica del frontend para Tutor Socrático Balmoral
 * Conecta el chat, animaciones del robot QuimiBot, onboarding y UI.
 */

// Variables de sesión
window.QUIMIBOT_SESSION = window.QUIMIBOT_SESSION || 'session-demo-' + Date.now();
window.QUIMIBOT_USER_ID = window.QUIMIBOT_USER_ID || 'alumno-demo';
window.QUIMIBOT_NOMBRE  = window.QUIMIBOT_NOMBRE  || 'Alumno';

// ─────────────────────────────────────────────
// SISTEMA DE VOZ SOCRÁTICA QUIMIBOT (Web Speech API)
// ─────────────────────────────────────────────
window.isQuimibotSpeaking = false;
let quimibotVoices = [];

function loadQuimibotVoices() {
  if ('speechSynthesis' in window) {
    quimibotVoices = window.speechSynthesis.getVoices();
  }
}
loadQuimibotVoices();
if ('speechSynthesis' in window) {
  window.speechSynthesis.onvoiceschanged = loadQuimibotVoices;
}

function getBestSpanishVoice() {
  if (!quimibotVoices || quimibotVoices.length === 0) {
    loadQuimibotVoices();
  }
  const esVoices = quimibotVoices.filter(v => v.lang && v.lang.toLowerCase().startsWith('es'));
  if (!esVoices.length) return null;

  const preferredNames = ['google', 'natural', 'paulina', 'sabina', 'monica', 'jorge', 'raul', 'helena', 'alva'];
  for (const name of preferredNames) {
    const match = esVoices.find(v => v.name.toLowerCase().includes(name));
    if (match) return match;
  }
  const latam = esVoices.find(v => v.lang.toLowerCase() === 'es-mx' || v.lang.toLowerCase() === 'es-419');
  if (latam) return latam;

  return esVoices[0];
}

function cleanTextForSpeech(text) {
  if (!text) return '';
  return text
    .replace(/https?:\/\/\S+/gi, '')
    .replace(/\*\*(.*?)\*\*/g, '$1')
    .replace(/\*(.*?)\*/g, '$1')
    .replace(/`{1,3}(.*?)`{1,3}/g, '$1')
    .replace(/^#{1,6}\s+/gm, '')
    .replace(/\[(.*?)\]\(.*?\)/g, '$1')
    .replace(/^[\*\-\+]\s+/gm, '')
    .replace(/^\d+\.\s+/gm, '')
    .replace(/[\u{1F300}-\u{1F9FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{1F600}-\u{1F64F}\u{1F680}-\u{1F6FF}]/gu, '')
    .replace(/\bH2O\b/g, 'H dos O')
    .replace(/\bCO2\b/g, 'C O dos')
    .replace(/\bO2\b/g, 'oxígeno molecular O dos')
    .replace(/\bNaCl\b/g, 'cloruro de sodio')
    .replace(/\s+/g, ' ')
    .trim();
}

window.isVoiceEnabled = function() {
  const saved = localStorage.getItem('quimibot_voice_enabled');
  return saved === null ? true : saved === 'true';
};

window.toggleQuimibotVoice = function() {
  const currentState = window.isVoiceEnabled();
  const newState = !currentState;
  localStorage.setItem('quimibot_voice_enabled', newState ? 'true' : 'false');
  window.updateVoiceToggleUI(newState);
  if (!newState && 'speechSynthesis' in window) {
    window.stopQuimibotVoice();
  }
};

window.updateVoiceToggleUI = function(enabled) {
  const toggleBtn = document.getElementById('voiceToggleBtn');
  const icon = document.getElementById('voiceToggleIcon');
  const label = document.getElementById('voiceToggleLabel');
  if (toggleBtn) {
    if (enabled) {
      toggleBtn.className = 'ios-tap px-2.5 py-1 rounded-full text-[11px] font-bold border transition-all flex items-center gap-1 bg-cyan-500/10 border-cyan-500/40 text-cyan-700 shadow-2xs hover:bg-cyan-500/20';
      if (icon) icon.textContent = '🔊';
      if (label) label.textContent = 'Voz ON';
      toggleBtn.title = 'Voz de QuimiBot activada (Haz clic para silenciar)';
    } else {
      toggleBtn.className = 'ios-tap px-2.5 py-1 rounded-full text-[11px] font-bold border transition-all flex items-center gap-1 bg-slate-100 border-slate-300 text-slate-500 shadow-2xs hover:bg-slate-200';
      if (icon) icon.textContent = '🔇';
      if (label) label.textContent = 'Voz Mute';
      toggleBtn.title = 'Voz de QuimiBot silenciada (Haz clic para activar)';
    }
  }
};

window.stopQuimibotVoice = function() {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }
  window.isQuimibotSpeaking = false;
  if (speechKeepAliveTimer) {
    clearInterval(speechKeepAliveTimer);
    speechKeepAliveTimer = null;
  }
  window.setBotEmotion('idle');
};

let speechKeepAliveTimer = null;

function keepSpeechAlive() {
  if (speechKeepAliveTimer) clearInterval(speechKeepAliveTimer);
  speechKeepAliveTimer = setInterval(() => {
    if (!('speechSynthesis' in window)) {
      clearInterval(speechKeepAliveTimer);
      return;
    }
    if (window.speechSynthesis.speaking) {
      if (window.speechSynthesis.paused) {
        window.speechSynthesis.resume();
      }
    } else if (!window.isQuimibotSpeaking) {
      clearInterval(speechKeepAliveTimer);
      speechKeepAliveTimer = null;
    }
  }, 400);
}

// Desbloquear motor de voz de manera síncrona en el gesto del usuario (Click / Submit)
window.unlockSpeechSynthesis = function() {
  if (!('speechSynthesis' in window)) return;
  try {
    if (window.speechSynthesis.paused) {
      window.speechSynthesis.resume();
    }
    const silent = new SpeechSynthesisUtterance(' ');
    silent.volume = 0.01;
    silent.rate = 10;
    window.speechSynthesis.speak(silent);
  } catch (e) {}
};

window.speakQuimibotText = function(text) {
  if (!('speechSynthesis' in window)) return;
  if (!window.isVoiceEnabled()) return;

  const cleanText = cleanTextForSpeech(text);
  if (!cleanText) return;

  try {
    if (window.speechSynthesis.paused) {
      window.speechSynthesis.resume();
    }
    window.speechSynthesis.cancel();
  } catch (e) {}

  setTimeout(() => {
    try {
      if (window.speechSynthesis.paused) {
        window.speechSynthesis.resume();
      }

      const utterance = new SpeechSynthesisUtterance(cleanText);
      const voice = getBestSpanishVoice();
      if (voice) {
        utterance.voice = voice;
        utterance.lang = voice.lang;
      } else {
        utterance.lang = 'es-MX';
      }
      utterance.rate = 1.05;
      utterance.pitch = 1.05;

      utterance.onstart = function() {
        window.isQuimibotSpeaking = true;
        window.setBotEmotion('speaking', '¡Hablando contigo! 🗣️ Escucha con atención...');
        const statusText = document.getElementById('robotStatusText');
        const statusDot = document.getElementById('statusIndicatorDot');
        if (statusText) statusText.textContent = 'Hablando... 🗣️';
        if (statusDot) statusDot.className = 'w-2 h-2 rounded-full bg-cyan-400 animate-ping';
        keepSpeechAlive();
      };

      utterance.onend = function() {
        window.isQuimibotSpeaking = false;
        if (speechKeepAliveTimer) {
          clearInterval(speechKeepAliveTimer);
          speechKeepAliveTimer = null;
        }
        window.setBotEmotion('idle');
      };

      utterance.onerror = function(err) {
        console.warn('Speech error:', err);
        window.isQuimibotSpeaking = false;
        if (speechKeepAliveTimer) {
          clearInterval(speechKeepAliveTimer);
          speechKeepAliveTimer = null;
        }
        window.setBotEmotion('idle');
      };

      window.speechSynthesis.speak(utterance);

      // Despertar inmediatamente por si Chromium se quedó suspendido
      if (window.speechSynthesis.paused) {
        window.speechSynthesis.resume();
      }
      keepSpeechAlive();
    } catch (err) {
      console.error('Error speakQuimibotText:', err);
      window.isQuimibotSpeaking = false;
      window.setBotEmotion('idle');
    }
  }, 60);
};

window.speakMessageText = function(btn) {
  const container = btn.closest('.bot-bubble-container') || btn.closest('.flex.gap-3');
  if (!container) return;
  const body = container.querySelector('.bot-text-body');
  if (body) {
    window.speakQuimibotText(body.innerText || body.textContent);
  }
};

// Exponer función de emociones globalmente
window.setBotEmotion = function(emotion, bubbleText) {
  const avatar = document.getElementById('quimibotAvatar');
  const orb = document.getElementById('robotAntennaOrb');
  const cheeks = document.getElementById('robotCheeks');
  const eyesIdle = document.getElementById('eyesIdle');
  const eyesHappy = document.getElementById('eyesHappy');
  const eyesThinking = document.getElementById('eyesThinking');
  const eyesCurious = document.getElementById('eyesCurious');
  const mouthNormal = document.getElementById('mouthNormal');
  const mouthHappy = document.getElementById('mouthHappy');
  const mouthSpeaking = document.getElementById('mouthSpeaking');
  const bubble = document.getElementById('robotBubble');
  const statusText = document.getElementById('robotStatusText');
  const statusDot = document.getElementById('statusIndicatorDot');

  if (!avatar) return;

  // Resetear estados visuales
  [eyesIdle, eyesHappy, eyesThinking, eyesCurious].forEach(el => el && el.classList.add('hidden'));
  [mouthNormal, mouthHappy, mouthSpeaking].forEach(el => el && el.classList.add('hidden'));
  if (cheeks) cheeks.classList.add('hidden');
  avatar.classList.remove('robot-float', 'robot-happy', 'robot-curious');
  if (orb) orb.setAttribute('class', 'antenna-normal');

  switch (emotion) {
    case 'happy':
      avatar.classList.add('robot-happy');
      if (eyesHappy) eyesHappy.classList.remove('hidden');
      if (mouthHappy) mouthHappy.classList.remove('hidden');
      if (cheeks) cheeks.classList.remove('hidden');
      if (orb) orb.setAttribute('class', 'antenna-active');
      if (statusText) statusText.textContent = '¡Entusiasmado!';
      if (statusDot) statusDot.className = 'w-2 h-2 rounded-full bg-amber-400 animate-bounce';
      if (bubble) bubble.textContent = bubbleText || '¡Excelente razonamiento! ✨ ¡Sigue así!';
      break;

    case 'thinking':
      avatar.classList.add('robot-curious');
      if (eyesThinking) eyesThinking.classList.remove('hidden');
      if (mouthNormal) mouthNormal.classList.remove('hidden');
      if (orb) orb.setAttribute('class', 'antenna-active');
      if (statusText) statusText.textContent = 'Analizando...';
      if (statusDot) statusDot.className = 'w-2 h-2 rounded-full bg-cyan-400 animate-ping';
      if (bubble) bubble.textContent = bubbleText || 'Analizando tu hipótesis con principios químicos... ⚡';
      break;

    case 'curious':
      avatar.classList.add('robot-curious');
      if (eyesCurious) eyesCurious.classList.remove('hidden');
      if (mouthNormal) mouthNormal.classList.remove('hidden');
      if (statusText) statusText.textContent = 'Inquisitivo';
      if (statusDot) statusDot.className = 'w-2 h-2 rounded-full bg-emerald-400';
      if (bubble) bubble.textContent = bubbleText || '¡Qué punto tan fascinante! 🤔 ¿Por qué crees que sea así?';
      break;

    case 'explaining':
    case 'speaking':
      avatar.classList.add('robot-float');
      if (eyesIdle) eyesIdle.classList.remove('hidden');
      if (mouthSpeaking) mouthSpeaking.classList.remove('hidden');
      if (orb) orb.setAttribute('class', 'antenna-active');
      if (statusText) statusText.textContent = emotion === 'speaking' ? 'Hablando... 🗣️' : 'Explicando';
      if (statusDot) statusDot.className = 'w-2 h-2 rounded-full bg-cyan-400 animate-ping';
      if (bubble) bubble.textContent = bubbleText || '¡Mira esta pista socrática para deducirlo! 💡';
      break;

    case 'idle':
    default:
      if (window.isQuimibotSpeaking) return;
      avatar.classList.add('robot-float');
      if (eyesIdle) eyesIdle.classList.remove('hidden');
      if (mouthNormal) mouthNormal.classList.remove('hidden');
      if (statusText) statusText.textContent = 'Activo';
      if (statusDot) statusDot.className = 'w-2 h-2 rounded-full bg-emerald-500 animate-pulse';
      if (bubble) bubble.textContent = bubbleText || '¡Listo para aprender! 🧪 Escribe tu hipótesis o pide un diagrama.';
      break;
  }
};

window.openImageModal = function(url, title) {
  const modal = document.getElementById('imageZoomModal');
  const img = document.getElementById('imageZoomImg');
  const titleEl = document.getElementById('imageZoomTitle');
  if (modal && img) {
    img.src = url;
    if (titleEl && title) titleEl.innerHTML = `<span>🔬</span><span>${title}</span>`;
    modal.classList.remove('hidden');
  }
};

window.closeImageModal = function() {
  const modal = document.getElementById('imageZoomModal');
  if (modal) modal.classList.add('hidden');
};

window.appendImage = function(imageUrl, title) {
  const chatHistory = document.getElementById('chatHistory');
  if (!chatHistory || !imageUrl) return;

  const card = document.createElement('div');
  card.className = 'flex items-start gap-3 my-3 animate-in fade-in slide-in-from-bottom-2 duration-300';
  
  const displayTitle = title || 'Ilustración Científica QuimiBot';
  const isMolecular = /agua|h2o|enlace|molecula|polar|nacl|co2|ch4/i.test(imageUrl + ' ' + displayTitle);

  card.innerHTML = `
    <div class="w-8 h-8 rounded-full bg-cyan-600/20 text-cyan-600 border border-cyan-500/30 flex items-center justify-center font-bold text-xs flex-shrink-0">
      🔬
    </div>
    <div class="ios-glass-card max-w-lg w-full rounded-2xl overflow-hidden shadow-md border border-cyan-500/20 bg-white/95">
      <div class="px-4 py-2 bg-gradient-to-r from-slate-900 to-indigo-950 text-white flex items-center justify-between">
        <span class="text-xs font-bold flex items-center gap-1.5 text-cyan-300">
          <span>🖼️</span>
          <span>${displayTitle}</span>
        </span>
        <span class="text-[10px] font-semibold bg-cyan-500/20 text-cyan-300 px-2 py-0.5 rounded-full border border-cyan-400/30">Ilustración HD</span>
      </div>
      <div class="p-2 bg-slate-950/90 flex items-center justify-center cursor-pointer group relative" onclick="window.openImageModal('${imageUrl}', '${displayTitle}')" title="Haz clic para ampliar en alta definición">
        <img src="${imageUrl}" alt="${displayTitle}" class="max-h-64 w-auto object-contain rounded-lg group-hover:scale-[1.02] transition-transform duration-200" />
        <div class="absolute bottom-3 right-3 bg-black/60 backdrop-blur-md text-white text-[10px] font-bold px-2.5 py-1 rounded-full opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1">
          <span>🔍</span> Ampliar
        </div>
      </div>
      <div class="p-3 bg-slate-50/90 border-t border-slate-200/80 flex items-center justify-between gap-2">
        <button type="button" onclick="window.openImageModal('${imageUrl}', '${displayTitle}')" class="text-xs font-bold text-cyan-700 hover:text-cyan-900 flex items-center gap-1">
          <span>🔍</span> <span>Ver en Pantalla Completa</span>
        </button>
        ${isMolecular ? `
        <button type="button" onclick="if(window.openMoleculeViewer) window.openMoleculeViewer();" class="text-xs font-extrabold bg-cyan-600 hover:bg-cyan-700 text-white px-3 py-1 rounded-full shadow-sm flex items-center gap-1 transition-all active:scale-95">
          <span>🔬</span> <span>Explorar en 3D</span>
        </button>
        ` : ''}
      </div>
    </div>
  `;

  chatHistory.appendChild(card);
  chatHistory.scrollTo({ top: chatHistory.scrollHeight, behavior: 'smooth' });
};

document.addEventListener('DOMContentLoaded', () => {

  // ─────────────────────────────────────────────
  // CHAT SOCRÁTICO (learning.html)
  // ─────────────────────────────────────────────
  const chatForm    = document.getElementById('chatForm');
  const chatInput   = document.getElementById('chatInput');
  const chatHistory = document.getElementById('chatHistory');

  if (chatForm && chatInput && chatHistory) {
    chatInput.disabled = true;
    window.setBotEmotion('idle');

    fetch('/api/chat/history?session_id=' + encodeURIComponent(window.QUIMIBOT_SESSION))
      .then(async res => {
        if (!res.ok) throw new Error('history');
        const data = await res.json();
        if (!data.messages.length) {
          const topicName = window.QUIMIBOT_TOPIC_NAME || 'Química General';
          appendBotMessage('¡Hola! Soy **QuimiBot** 🧪, tu tutor socrático de química para la Preparatoria Balmoral. Estamos trabajando sobre el módulo: **' + topicName + '**. ¿Qué duda, pregunta o hipótesis inicial tienes sobre este tema?', false);
          window.setBotEmotion('happy', '¡Bienvenido a Química Balmoral! 👋');
          setTimeout(() => { window.setBotEmotion('idle'); }, 3000);
        } else {
          data.messages.forEach(m => m.role === 'user' ? appendUserMessage(m.content) : appendBotMessage(m.content, false));
        }
      }).catch(() => appendErrorMessage('No se pudo recuperar el historial. Recarga la página para consultarlo.'))
      .finally(() => { chatInput.disabled = false; });

    // ─────────────────────────────────────────────
    // BLINDAJE PEDAGÓGICO ANTI-COPIAR / PEGAR (Anti-IA)
    // ─────────────────────────────────────────────
    function warnAgainstPasting(reason) {
      if (window.setBotEmotion) {
        window.setBotEmotion('curious', '✍️ ¡En QuimiBot razonamos con nuestras palabras! El copiado y pegado está desactivado para entrenar tu mente.');
      }
      if (window.speakQuimibotText && window.isVoiceEnabled && window.isVoiceEnabled()) {
        window.speakQuimibotText('¡Ey, científico! En QuimiBot razonamos con nuestras propias palabras. El copiado y pegado está desactivado.');
      }
      chatInput.classList.add('ring-2', 'ring-rose-500', 'bg-rose-50');
      setTimeout(() => {
        chatInput.classList.remove('ring-2', 'ring-rose-500', 'bg-rose-50');
      }, 1500);
    }

    // Bloquear pegado (Ctrl+V, Cmd+V, menú contextual)
    chatInput.addEventListener('paste', (e) => {
      e.preventDefault();
      warnAgainstPasting('paste');
    });

    // Bloquear arrastrar y soltar (Drag & Drop)
    chatInput.addEventListener('drop', (e) => {
      e.preventDefault();
      warnAgainstPasting('drop');
    });

    // Bloquear atajos de pegado en teclado y capturar Enter para activar audio
    chatInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        if (window.unlockSpeechSynthesis) window.unlockSpeechSynthesis();
      }
      if ((e.ctrlKey || e.metaKey) && (e.key === 'v' || e.key === 'V')) {
        e.preventDefault();
        warnAgainstPasting('paste-key');
      } else if (e.shiftKey && e.key === 'Insert') {
        e.preventDefault();
        warnAgainstPasting('paste-key');
      }
    });

    const submitBtn = chatForm.querySelector('button[type=submit]');
    if (submitBtn) {
      submitBtn.addEventListener('pointerdown', () => {
        if (window.unlockSpeechSynthesis) window.unlockSpeechSynthesis();
      });
    }

    chatForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      // Desbloquear motor de síntesis de voz de inmediato en el gesto del usuario
      if (window.unlockSpeechSynthesis) {
        window.unlockSpeechSynthesis();
      }
      const message = chatInput.value.trim();
      if (!message || chatInput.disabled) return;

      appendUserMessage(message);
      chatInput.value = '';
      chatInput.disabled = true;

      // Reaccionar según el tipo de mensaje
      const isImageRequest = /imagen|foto|diagrama|esquema|dibuja|visual|modelo/i.test(message);
      const isGreeting = /hola|buenos|que tal|buenas/i.test(message);

      if (isGreeting) {
        window.setBotEmotion('happy', '¡Hola! ¡Qué gusto verte! 😊');
      } else if (isImageRequest) {
        window.setBotEmotion('thinking', '¡Generando tu esquema químico visual! 🎨');
      } else {
        window.setBotEmotion('thinking', '¡Analizando tu hipótesis con química! ⚡');
      }

      const loadingId = appendLoading();
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 30000); // 30s límite
      const sendButton = chatForm.querySelector('button[type=submit]');
      if (sendButton) sendButton.disabled = true;

      try {
        const response = await fetch('/api/tutor', {
          signal: controller.signal,
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            session_id:      window.QUIMIBOT_SESSION,
            id_alumno:       window.QUIMIBOT_USER_ID,
            mensaje_alumno:  message
          })
        });

        removeLoading(loadingId);
        const data = await response.json();

        if (response.ok) {
          window.setBotEmotion('explaining', isImageRequest ? '¡Aquí tienes la ilustración! 🖼️' : '¡Reflexiona en esta pista! 💡');
          // QuimiBot habla automáticamente si la voz está activada
          if (window.speakQuimibotText) {
            window.speakQuimibotText(data.respuesta);
          }
          await appendBotMessageAnimated(data.respuesta);
          
          if (data.image_url) {
            window.appendImage(data.image_url);
            window.setBotEmotion('happy', '¡Observa los detalles del esquema! 🔍');
          }

          // Celebrar si el alumno desbloqueó una o más insignias
          if (data.new_badges && data.new_badges.length > 0) {
            data.new_badges.forEach((badge, idx) => {
              setTimeout(() => {
                if (window.celebrateBadge) {
                  window.celebrateBadge(badge);
                }
              }, idx * 6500);
            });
          }
        } else {
          chatInput.value = message;
          appendErrorMessage(data.detail || 'No se pudo procesar el mensaje.');
          window.setBotEmotion('curious', 'Mmm, revisemos de nuevo... 🤔');
        }
      } catch (error) {
        removeLoading(loadingId);
        chatInput.value = message;
        appendErrorMessage(error.name === 'AbortError' ? 'La respuesta demoró más de lo esperado. Haz clic en Enviar para reintentar.' : 'Sin conexión con el servidor.');
        window.setBotEmotion('idle');
      } finally {
        clearTimeout(timer);
        if (sendButton) sendButton.disabled = false;
        chatInput.disabled = false;
        chatInput.focus();
        setTimeout(() => { 
          if (!window.isQuimibotSpeaking) {
            window.setBotEmotion('idle'); 
          }
        }, 4000);
      }
    });
  }

  // ─────────────────────────────────────────────
  // Funciones de renderizado del chat estilo iOS
  // ─────────────────────────────────────────────
  function appendUserMessage(text) {
    if (!chatHistory) return;
    const div = document.createElement('div');
    div.className = 'flex justify-end mb-3.5';
    div.innerHTML = `
      <div class="max-w-xs lg:max-w-md bg-gradient-to-tr from-primary to-primary-container text-white rounded-3xl rounded-br-xs px-4 py-3 shadow-md shadow-primary/20">
        <p class="text-sm leading-relaxed font-semibold">${escapeHtml(text)}</p>
      </div>`;
    chatHistory.appendChild(div);
    chatHistory.scrollTop = chatHistory.scrollHeight;
  }

  function appendBotMessage(text, animate = false) {
    if (!chatHistory) return;
    const div = document.createElement('div');
    div.className = 'bot-bubble-container flex gap-3 mb-4 items-start';
    div.innerHTML = `
      <div class="w-9 h-9 rounded-2xl bg-gradient-to-tr from-slate-900 to-slate-800 text-cyan-400 border border-slate-700/80 flex-shrink-0 flex items-center justify-center font-bold text-sm shadow-md">
        🤖
      </div>
      <div class="max-w-xs lg:max-w-lg bg-white/90 backdrop-blur-xl border border-slate-200/90 rounded-3xl rounded-tl-xs p-4 shadow-sm">
        <div class="flex items-center justify-between gap-2 mb-1.5 border-b border-slate-100 pb-1">
          <div class="flex items-center gap-1.5">
            <span class="text-xs font-extrabold text-slate-900">QuimiBot</span>
            <span class="text-[10px] bg-tertiary/10 text-tertiary font-extrabold px-2 py-0.5 rounded-full uppercase tracking-wider">Tutor Socrático</span>
          </div>
          <div class="flex items-center gap-1.5">
            <button type="button" onclick="window.speakMessageText(this)" class="ios-tap text-xs text-slate-400 hover:text-cyan-600 p-1 rounded-md hover:bg-slate-100 transition-colors" title="Escuchar respuesta con voz de QuimiBot">
              🔊
            </button>
            <span class="text-[10px] text-slate-400 font-semibold">Ahora</span>
          </div>
        </div>
        <div class="text-sm leading-relaxed text-slate-800 font-medium bot-text-body">${markdownToHtml(text)}</div>
      </div>`;
    chatHistory.appendChild(div);
    chatHistory.scrollTop = chatHistory.scrollHeight;
  }

  async function appendBotMessageAnimated(text) {
    if (!chatHistory) return;
    const div = document.createElement('div');
    div.className = 'bot-bubble-container flex gap-3 mb-4 items-start';
    div.innerHTML = `
      <div class="w-9 h-9 rounded-2xl bg-gradient-to-tr from-slate-900 to-slate-800 text-cyan-400 border border-slate-700/80 flex-shrink-0 flex items-center justify-center font-bold text-sm shadow-md animate-bounce" style="animation-iteration-count: 2;">
        🤖
      </div>
      <div class="max-w-xs lg:max-w-lg bg-white/90 backdrop-blur-xl border border-slate-200/90 rounded-3xl rounded-tl-xs p-4 shadow-sm">
        <div class="flex items-center justify-between gap-2 mb-1.5 border-b border-slate-100 pb-1">
          <div class="flex items-center gap-1.5">
            <span class="text-xs font-extrabold text-slate-900">QuimiBot</span>
            <span class="text-[10px] bg-tertiary/10 text-tertiary font-extrabold px-2 py-0.5 rounded-full uppercase tracking-wider">Tutor Socrático</span>
          </div>
          <div class="flex items-center gap-1.5">
            <button type="button" onclick="window.speakMessageText(this)" class="ios-tap text-xs text-slate-400 hover:text-cyan-600 p-1 rounded-md hover:bg-slate-100 transition-colors" title="Escuchar respuesta con voz de QuimiBot">
              🔊
            </button>
            <span class="text-[10px] text-slate-400 font-semibold">Ahora</span>
          </div>
        </div>
        <div class="text-sm leading-relaxed text-slate-800 font-medium bot-text-body"></div>
      </div>`;
    chatHistory.appendChild(div);

    const bodyContainer = div.querySelector('.bot-text-body');
    const words = text.split(' ');
    let currentText = '';

    for (let i = 0; i < words.length; i++) {
      currentText += (i === 0 ? '' : ' ') + words[i];
      bodyContainer.innerHTML = markdownToHtml(currentText);
      chatHistory.scrollTop = chatHistory.scrollHeight;
      await new Promise(r => setTimeout(r, 16));
    }
  }

  function appendLoading() {
    if (!chatHistory) return null;
    const id = 'loading-' + Date.now();
    const div = document.createElement('div');
    div.id = id;
    div.className = 'flex gap-3 mb-4 items-center';
    div.innerHTML = `
      <div class="w-9 h-9 rounded-2xl bg-gradient-to-tr from-slate-900 to-slate-800 text-cyan-400 border border-slate-700/80 flex-shrink-0 flex items-center justify-center font-bold text-sm shadow-md animate-pulse">
        🤖
      </div>
      <div class="bg-white/90 backdrop-blur-xl border border-slate-200/80 rounded-full px-4 py-2.5 shadow-sm">
        <div class="flex gap-2 items-center h-4">
          <span class="text-xs text-slate-500 font-semibold mr-0.5">QuimiBot analizando</span>
          <div class="w-2 h-2 bg-cyan-500 rounded-full animate-bounce" style="animation-delay:0ms"></div>
          <div class="w-2 h-2 bg-cyan-500 rounded-full animate-bounce" style="animation-delay:150ms"></div>
          <div class="w-2 h-2 bg-cyan-500 rounded-full animate-bounce" style="animation-delay:300ms"></div>
        </div>
      </div>`;
    chatHistory.appendChild(div);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    return id;
  }

  function appendImage(url) {
    if (!chatHistory || !url) return;
    const div = document.createElement('div');
    div.className = 'flex gap-3 mb-4';
    div.innerHTML = `
      <div class="w-9 h-9 rounded-xl bg-amber-500 text-white flex-shrink-0 flex items-center justify-center font-bold text-sm shadow-sm">
        🖼️
      </div>
      <div class="bg-white border-2 border-amber-400/60 rounded-2xl p-4 shadow-md max-w-sm lg:max-w-lg overflow-hidden transition-all hover:border-amber-500">
        <div class="flex items-center justify-between text-xs font-extrabold text-amber-900 mb-2.5">
          <span class="flex items-center gap-1.5">
            <span class="text-base">🔬</span>
            <span>Diagrama Conceptual Balmoral</span>
          </span>
          <button type="button" onclick="openImageModal('${url}', 'Diagrama Pedagógico de Química')" class="text-[11px] bg-amber-100 hover:bg-amber-200 text-amber-950 font-extrabold px-2.5 py-0.5 rounded-full uppercase tracking-wider flex items-center gap-1 transition-all active:scale-95 shadow-2xs">
            <span>🔍</span><span>Ampliar</span>
          </button>
        </div>
        
        <div class="rounded-xl overflow-hidden bg-slate-950 border border-slate-700 shadow-inner group relative cursor-pointer" onclick="openImageModal('${url}', 'Diagrama Conceptual Balmoral')">
          <img src="${url}" alt="Diagrama de Química Educativo" 
            class="w-full h-auto max-h-72 object-contain rounded-xl transition-transform duration-300 group-hover:scale-102" 
            loading="lazy"
            onerror="this.parentElement.innerHTML='<div class=\\'p-6 text-center text-xs text-slate-300 font-semibold\\'>🔬 Ilustración química disponible para este concepto.</div>'"/>
          <div class="absolute inset-0 bg-slate-900/30 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center pointer-events-none">
            <span class="bg-slate-950/80 text-cyan-300 text-xs font-bold px-3 py-1.5 rounded-full shadow-lg border border-slate-700 flex items-center gap-1">
              <span>🔍</span><span>Haz clic para ver en grande</span>
            </span>
          </div>
        </div>

        <p class="text-[11px] text-slate-600 font-semibold mt-2.5 text-center flex items-center justify-center gap-1">
          <span>🔍</span>
          <span>Analiza el esquema para deducir y justificar tu respuesta a QuimiBot.</span>
        </p>
      </div>`;
    chatHistory.appendChild(div);
    chatHistory.scrollTop = chatHistory.scrollHeight;
  }



  function appendErrorMessage(text) {
    if (!chatHistory) return;
    const div = document.createElement('div');
    div.className = 'flex justify-center mb-3';
    div.innerHTML = `<span class="text-xs font-semibold text-slate-600 bg-slate-100 border border-slate-200 px-4 py-1.5 rounded-full shadow-xs">${escapeHtml(text)}</span>`;
    chatHistory.appendChild(div);
    chatHistory.scrollTop = chatHistory.scrollHeight;
  }

  function escapeHtml(text) {
    return text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  function markdownToHtml(text) {
    return escapeHtml(text)
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.+?)\*/g, '<em>$1</em>')
      .replace(/`(.+?)`/g, '<code class="bg-slate-200 px-1 rounded text-xs">$1</code>')
      .replace(/\n/g, '<br>');
  }

  // ─────────────────────────────────────────────
  // ONBOARDING (onboarding.html)
  // ─────────────────────────────────────────────
  const onboardingForm = document.getElementById('onboardingForm');
  if (onboardingForm) {
    onboardingForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      await submitDiagnostic();
    });
  }

  document.addEventListener('click', async (e) => {
    const btn = e.target.closest('[data-action="finish-onboarding"]');
    if (btn) {
      e.preventDefault();
      await submitDiagnostic();
    }
  });

  async function submitDiagnostic() {
    const grado = document.getElementById('inputGrade')?.value
                || document.querySelector('select[name="grado"]')?.value
                || '2do Bachillerato';
    const estilo = document.getElementById('inputStyle')?.value
                 || document.querySelector('select[name="estilo"]')?.value
                 || 'Visual';
    const conocimiento = document.getElementById('inputKnowledge')?.value
                       || document.querySelector('textarea[name="conocimiento"]')?.value
                       || 'Básico';
    const dificultades = document.getElementById('inputDifficulties')?.value
                       || document.querySelector('textarea[name="dificultades"]')?.value
                       || 'Por determinar';

    const button = onboardingForm.querySelector('button[type=submit]');
    const status = document.getElementById('diagnosticStatus');
    if (button.disabled) return;
    button.disabled = true;
    if (status) status.textContent = 'Guardando tu diagnóstico…';
    try {
      const res = await fetch('/api/diagnostic', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          id_alumno:          window.QUIMIBOT_USER_ID,
          nivel_academico:    document.getElementById('inputLevel')?.value || 'Intermedio',
          conocimiento_previo: conocimiento,
          dificultades:       dificultades,
          estilo_aprendizaje: estilo,
          grado:              grado
        })
      });
      if (res.ok) {
        window.location.href = '/dashboard';
      } else {
        if (status) status.textContent = 'No se pudo guardar. Revisa los datos e intenta de nuevo.';
      }
    } catch (err) {
      if (status) status.textContent = 'Sin conexión. Tu diagnóstico no se ha guardado; vuelve a intentar.';
    } finally {
      button.disabled = false;
    }
  }

  // ─────────────────────────────────────────────
  // NAVEGACIÓN ACTIVA
  // ─────────────────────────────────────────────
  const currentPath = window.location.pathname;
  document.querySelectorAll('nav a[href]').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('bg-primary-container', 'text-on-primary-container');
      link.classList.remove('text-inverse-on-surface/80');
    }
  });

  // Inicializar estado del botón de voz socrática
  if (window.updateVoiceToggleUI && window.isVoiceEnabled) {
    window.updateVoiceToggleUI(window.isVoiceEnabled());
  }

});
