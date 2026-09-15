/**
 * celebration.js — Festejo Inmersivo de Insignias Balmoral
 * Confeti multicolor + Explosión de Átomos en Órbita 3D + QuimiBot Festejando (6 segundos)
 */

(function() {
  let celebrationActive = false;
  let celebrationTimer = null;
  let animFrameId = null;

  window.celebrateBadge = function(badge) {
    if (celebrationActive) {
      window.closeBadgeCelebration();
    }
    celebrationActive = true;

    // Datos por defecto para pruebas o fallbacks
    const b = badge || {
      id: "explorador_atomico",
      icono: "⚛️",
      titulo: "Explorador Atómico",
      descripcion: "¡Alcanzaste un nuevo nivel de deducción y dominio en química!",
      categoria: "Dominio",
      color: "from-amber-400 to-amber-600"
    };

    // 1. Crear Canvas de Confeti y Átomos
    const canvas = document.createElement('canvas');
    canvas.id = 'badgeCelebrationCanvas';
    canvas.style.position = 'fixed';
    canvas.style.inset = '0';
    canvas.style.width = '100vw';
    canvas.style.height = '100vh';
    canvas.style.pointerEvents = 'none';
    canvas.style.zIndex = '9998';
    document.body.appendChild(canvas);

    // 2. Crear Modal de QuimiBot Festejando
    const overlay = document.createElement('div');
    overlay.id = 'badgeCelebrationOverlay';
    overlay.className = 'fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-md transition-opacity duration-500 opacity-0';
    overlay.onclick = function(e) {
      if (e.target === overlay) window.closeBadgeCelebration();
    };

    overlay.innerHTML = `
      <div class="relative max-w-md w-full bg-gradient-to-b from-slate-900 via-slate-900 to-slate-950 border-2 border-amber-400/80 rounded-3xl p-6 md:p-8 text-center shadow-2xl overflow-hidden transform scale-90 transition-transform duration-500 text-white" onclick="event.stopPropagation()">
        
        <!-- Resplandor de Fondo Dorado / Neón -->
        <div class="absolute -top-24 -left-24 w-48 h-48 bg-amber-500/20 rounded-full blur-3xl pointer-events-none"></div>
        <div class="absolute -bottom-24 -right-24 w-48 h-48 bg-cyan-500/20 rounded-full blur-3xl pointer-events-none"></div>

        <!-- Barra Superior de Conteo Regresivo (6 segundos) -->
        <div class="absolute top-0 left-0 right-0 h-1.5 bg-slate-800">
          <div id="celebrationProgressBar" class="h-full bg-gradient-to-r from-amber-400 via-rose-500 to-cyan-400 w-full transition-all duration-[6000ms] ease-linear"></div>
        </div>

        <!-- Etiqueta de Logro -->
        <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-400/15 border border-amber-400/40 text-amber-300 text-[11px] font-extrabold uppercase tracking-widest mb-3">
          <span>⭐</span><span>¡NUEVA INSIGNIA DESBLOQUEADA!</span><span>⭐</span>
        </div>

        <!-- QuimiBot Festejando y Medalla Gigante -->
        <div class="flex items-center justify-center gap-4 my-2">
          <!-- Robot QuimiBot Feliz Rebotando -->
          <div class="w-20 h-20 bg-slate-800/80 border-2 border-cyan-400/80 rounded-2xl p-1.5 shadow-lg flex-shrink-0 animate-bounce">
            <svg viewBox="0 0 140 140" class="w-full h-full drop-shadow">
              <line x1="70" y1="28" x2="70" y2="10" stroke="#94a3b8" stroke-width="4" stroke-linecap="round"/>
              <circle cx="70" cy="8" r="7" fill="#f59e0b" class="animate-ping"/>
              <rect x="14" y="52" width="8" height="22" rx="4" fill="#e02e2b"/>
              <rect x="118" y="52" width="8" height="22" rx="4" fill="#e02e2b"/>
              <rect x="22" y="26" width="96" height="80" rx="22" fill="#00686d" stroke="#ffffff" stroke-width="3"/>
              <rect x="32" y="38" width="76" height="56" rx="14" fill="#0f172a"/>
              <!-- Mejillas sonrojadas de fiesta -->
              <circle cx="39" cy="74" r="5" fill="#ff766d"/>
              <circle cx="101" cy="74" r="5" fill="#ff766d"/>
              <!-- Ojos felices (^ ^) -->
              <path d="M 43 64 Q 52 50 61 64" stroke="#38bdf8" stroke-width="5" fill="none" stroke-linecap="round"/>
              <path d="M 79 64 Q 88 50 97 64" stroke="#38bdf8" stroke-width="5" fill="none" stroke-linecap="round"/>
              <!-- Boca sonriente -->
              <path d="M 54 76 Q 70 88 86 76" stroke="#38bdf8" stroke-width="4.5" fill="none" stroke-linecap="round"/>
            </svg>
          </div>

          <!-- Medalla Gigante -->
          <div class="w-20 h-20 rounded-2xl bg-gradient-to-tr from-amber-400 via-amber-500 to-yellow-600 border-2 border-white/60 flex items-center justify-center text-4xl shadow-xl shadow-amber-500/30 transform hover:scale-110 transition-transform">
            ${b.icono || "⚛️"}
          </div>
        </div>

        <!-- Título y Descripción del Logro -->
        <h3 class="text-2xl font-black text-amber-300 tracking-tight mt-3 mb-1">
          ${b.titulo}
        </h3>
        <p class="text-xs text-slate-300 font-medium leading-relaxed max-w-sm mx-auto mb-4">
          ${b.descripcion}
        </p>

        <!-- Mensaje de QuimiBot -->
        <div class="bg-slate-800/80 border border-slate-700 rounded-2xl p-3 text-xs text-cyan-200 font-semibold mb-5 flex items-center justify-center gap-2">
          <span>🤖💬</span>
          <span>"¡Increíble razonamiento! Has demostrado verdadero pensamiento socrático."</span>
        </div>

        <!-- Botón de Continuar -->
        <button type="button" onclick="window.closeBadgeCelebration()" class="ios-tap w-full py-3 px-6 rounded-2xl bg-gradient-to-r from-amber-400 via-rose-500 to-cyan-500 hover:brightness-110 text-slate-950 font-black text-sm uppercase tracking-wider shadow-lg transition-all active:scale-95 flex items-center justify-center gap-2 cursor-pointer">
          <span>¡Continuar Aprendiendo!</span>
          <span>🚀</span>
        </button>
      </div>
    `;

    document.body.appendChild(overlay);

    // Animación de entrada suave
    requestAnimationFrame(() => {
      overlay.classList.remove('opacity-0');
      overlay.classList.add('opacity-100');
      const card = overlay.querySelector('div');
      if (card) {
        card.classList.remove('scale-90');
        card.classList.add('scale-100');
      }
      const pBar = document.getElementById('celebrationProgressBar');
      if (pBar) {
        setTimeout(() => { pBar.style.width = '0%'; }, 50);
      }
    });

    // 3. QuimiBot Felicita con Voz
    if (window.speakQuimibotText && window.isVoiceEnabled && window.isVoiceEnabled()) {
      window.speakQuimibotText(`¡Felicidades! Has desbloqueado la insignia ${b.titulo}. ¡Excelente deducción científica!`);
    }

    // 4. Iniciar Animación de Partículas (Confeti + Átomos Volando)
    startParticleEngine(canvas);

    // 5. Cierre automático a los 6 segundos (6000ms)
    celebrationTimer = setTimeout(() => {
      window.closeBadgeCelebration();
    }, 6000);
  };

  window.closeBadgeCelebration = function() {
    if (celebrationTimer) {
      clearTimeout(celebrationTimer);
      celebrationTimer = null;
    }
    if (animFrameId) {
      cancelAnimationFrame(animFrameId);
      animFrameId = null;
    }

    const overlay = document.getElementById('badgeCelebrationOverlay');
    const canvas = document.getElementById('badgeCelebrationCanvas');

    if (overlay) {
      overlay.classList.remove('opacity-100');
      overlay.classList.add('opacity-0');
      setTimeout(() => { overlay.remove(); }, 400);
    }
    if (canvas) {
      canvas.style.transition = 'opacity 0.4s ease-out';
      canvas.style.opacity = '0';
      setTimeout(() => { canvas.remove(); }, 400);
    }
    celebrationActive = false;
  };

  // Motor Gráfico de Partículas (Canvas 60fps)
  function startParticleEngine(canvas) {
    const ctx = canvas.getContext('2d');
    let w = canvas.width = window.innerWidth;
    let h = canvas.height = window.innerHeight;

    const CONFETTI_COLORS = ['#f59e0b', '#06b6d4', '#10b981', '#ec4899', '#e02e2b', '#8b5cf6', '#ffffff', '#38bdf8'];
    const ATOM_COLORS = ['#38bdf8', '#06b6d4', '#f59e0b', '#10b981', '#ff766d'];

    // 1. Crear Confeti (130 piezas)
    const confetti = [];
    for (let i = 0; i < 130; i++) {
      confetti.push({
        x: Math.random() * w,
        y: Math.random() * -h * 0.5,
        vx: (Math.random() - 0.5) * 4,
        vy: 2 + Math.random() * 5,
        size: 6 + Math.random() * 8,
        color: CONFETTI_COLORS[Math.floor(Math.random() * CONFETTI_COLORS.length)],
        rotation: Math.random() * Math.PI * 2,
        rotSpeed: (Math.random() - 0.5) * 0.15,
        sway: Math.random() * Math.PI * 2,
        swaySpeed: 0.04 + Math.random() * 0.04
      });
    }

    // 2. Crear Átomos Cinéticos en Órbita (22 átomos saliendo por todos lados)
    const atoms = [];
    const centerX = w / 2;
    const centerY = h / 2;

    for (let i = 0; i < 22; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = 4 + Math.random() * 9;
      atoms.push({
        x: centerX + (Math.random() - 0.5) * 100,
        y: centerY + (Math.random() - 0.5) * 100,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed - 1.5,
        gravity: 0.08,
        friction: 0.985,
        radius: 6 + Math.random() * 6,
        color: ATOM_COLORS[Math.floor(Math.random() * ATOM_COLORS.length)],
        orbitRadius: 18 + Math.random() * 16,
        orbitAngle: Math.random() * Math.PI * 2,
        orbitSpeed: 0.08 + Math.random() * 0.12,
        tilt: Math.random() * Math.PI,
        opacity: 1
      });
    }

    let startTime = Date.now();

    function render() {
      const elapsed = Date.now() - startTime;
      ctx.clearRect(0, 0, w, h);

      // A. Dibujar Confeti
      for (let c of confetti) {
        c.x += c.vx + Math.sin(c.sway) * 1.5;
        c.y += c.vy;
        c.sway += c.swaySpeed;
        c.rotation += c.rotSpeed;

        if (c.y > h + 20) {
          c.y = -20;
          c.x = Math.random() * w;
        }

        ctx.save();
        ctx.translate(c.x, c.y);
        ctx.rotate(c.rotation);
        ctx.fillStyle = c.color;
        ctx.fillRect(-c.size / 2, -c.size / 2, c.size, c.size * 0.6);
        ctx.restore();
      }

      // B. Dibujar Átomos Cinéticos en Órbita 3D
      for (let a of atoms) {
        a.x += a.vx;
        a.y += a.vy;
        a.vy += a.gravity;
        a.vx *= a.friction;
        a.vy *= a.friction;
        a.orbitAngle += a.orbitSpeed;

        ctx.save();
        ctx.translate(a.x, a.y);
        ctx.globalAlpha = Math.max(0, 1 - (elapsed / 6000));

        // Resplandor del núcleo atómico
        const grad = ctx.createRadialGradient(0, 0, 0, 0, 0, a.radius * 2.2);
        grad.addColorStop(0, a.color);
        grad.addColorStop(0.5, 'rgba(255,255,255,0.8)');
        grad.addColorStop(1, 'rgba(0,0,0,0)');
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(0, 0, a.radius * 2.2, 0, Math.PI * 2);
        ctx.fill();

        // Núcleo blanco brillante
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(0, 0, a.radius * 0.8, 0, Math.PI * 2);
        ctx.fill();

        // Órbita 1
        ctx.save();
        ctx.rotate(a.tilt);
        ctx.strokeStyle = a.color;
        ctx.lineWidth = 1.2;
        ctx.beginPath();
        ctx.ellipse(0, 0, a.orbitRadius, a.orbitRadius * 0.4, 0, 0, Math.PI * 2);
        ctx.stroke();

        // Electrón 1
        const ex1 = Math.cos(a.orbitAngle) * a.orbitRadius;
        const ey1 = Math.sin(a.orbitAngle) * a.orbitRadius * 0.4;
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(ex1, ey1, 2.5, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();

        // Órbita 2 (Cruzada a 90 grados)
        ctx.save();
        ctx.rotate(a.tilt + Math.PI / 2);
        ctx.strokeStyle = a.color;
        ctx.lineWidth = 1.2;
        ctx.beginPath();
        ctx.ellipse(0, 0, a.orbitRadius * 0.85, a.orbitRadius * 0.35, 0, 0, Math.PI * 2);
        ctx.stroke();

        // Electrón 2
        const ex2 = Math.cos(-a.orbitAngle * 1.3) * a.orbitRadius * 0.85;
        const ey2 = Math.sin(-a.orbitAngle * 1.3) * a.orbitRadius * 0.35;
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(ex2, ey2, 2.5, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();

        ctx.restore();
      }

      if (elapsed < 6000) {
        animFrameId = requestAnimationFrame(render);
      }
    }

    render();
  }
})();
