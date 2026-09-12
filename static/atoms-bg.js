/**
 * atoms-bg.js — Fondo Dinámico Interactivo con Átomos y Enlaces Químicos
 * Renderizado de alta fidelidad estilo Apple Retina con aceleración Canvas 60fps.
 */
(function() {
  function initAtomsBackground() {
    let canvas = document.getElementById('atomsBackgroundCanvas');
    if (!canvas) {
      canvas = document.createElement('canvas');
      canvas.id = 'atomsBackgroundCanvas';
      canvas.style.position = 'fixed';
      canvas.style.top = '0';
      canvas.style.left = '0';
      canvas.style.width = '100vw';
      canvas.style.height = '100vh';
      canvas.style.pointerEvents = 'none';
      canvas.style.zIndex = '0';
      canvas.style.opacity = '0.55';
      canvas.style.transition = 'opacity 1s ease-in-out';
      document.body.prepend(canvas);
    }

    const ctx = canvas.getContext('2d');
    let width, height, dpr;
    let atoms = [];
    let mouse = { x: -1000, y: -1000, active: false };

    // Paleta de colores químicos estilo Apple Retina / Neón
    const COLOR_PALETTES = [
      { core: '#06b6d4', glow: 'rgba(6, 182, 212, 0.4)', name: 'Cian/Cuántico' },
      { core: '#38bdf8', glow: 'rgba(56, 189, 248, 0.35)', name: 'Azul Sistema' },
      { core: '#e02e2b', glow: 'rgba(224, 46, 43, 0.35)', name: 'Carmesí Balmoral' },
      { core: '#10b981', glow: 'rgba(16, 185, 129, 0.35)', name: 'Esmeralda Reactivo' },
      { core: '#f59e0b', glow: 'rgba(245, 158, 11, 0.35)', name: 'Ámbar Energía' },
      { core: '#8b5cf6', glow: 'rgba(139, 92, 246, 0.35)', name: 'Violeta Orbital' }
    ];

    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      ctx.scale(dpr, dpr);
    }

    class Atom {
      constructor() {
        this.reset(true);
      }

      reset(initial = false) {
        this.x = initial ? Math.random() * width : (Math.random() > 0.5 ? -30 : width + 30);
        this.y = Math.random() * height;
        this.vx = (Math.random() - 0.5) * 0.7;
        this.vy = (Math.random() - 0.5) * 0.7;
        this.radius = 4 + Math.random() * 5; // Radio del núcleo
        this.palette = COLOR_PALETTES[Math.floor(Math.random() * COLOR_PALETTES.length)];
        
        // Configuración de órbitas de electrones
        this.orbits = [
          { r: this.radius * 3.2, angle: Math.random() * Math.PI * 2, speed: 0.02 + Math.random() * 0.03, tilt: Math.random() * Math.PI },
          { r: this.radius * 5.4, angle: Math.random() * Math.PI * 2, speed: -0.015 - Math.random() * 0.025, tilt: Math.random() * Math.PI }
        ];
        this.electronCount = 2 + Math.floor(Math.random() * 3);
        this.pulse = Math.random() * Math.PI * 2;
      }

      update() {
        this.x += this.vx;
        this.y += this.vy;
        this.pulse += 0.03;

        // Rebote suave en bordes
        if (this.x < -40) this.x = width + 40;
        if (this.x > width + 40) this.x = -40;
        if (this.y < -40) this.y = height + 40;
        if (this.y > height + 40) this.y = -40;

        // Interacción suave con mouse
        if (mouse.active) {
          const dx = this.x - mouse.x;
          const dy = this.y - mouse.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 140 && dist > 0) {
            const force = (140 - dist) / 140 * 0.8;
            this.x += (dx / dist) * force;
            this.y += (dy / dist) * force;
          }
        }

        // Actualizar rotación de órbitas
        for (let orbit of this.orbits) {
          orbit.angle += orbit.speed;
        }
      }

      draw() {
        ctx.save();
        ctx.translate(this.x, this.y);

        // Resplandor del núcleo (Glow)
        const currentRadius = this.radius + Math.sin(this.pulse) * 0.8;
        const grad = ctx.createRadialGradient(0, 0, 0, 0, 0, currentRadius * 2.5);
        grad.addColorStop(0, this.palette.core);
        grad.addColorStop(0.5, this.palette.glow);
        grad.addColorStop(1, 'rgba(0,0,0,0)');
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(0, 0, currentRadius * 2.5, 0, Math.PI * 2);
        ctx.fill();

        // Núcleo atómico central sólido
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(0, 0, currentRadius * 0.75, 0, Math.PI * 2);
        ctx.fill();

        // Dibujar anillos orbitales elípticos
        for (let i = 0; i < this.orbits.length; i++) {
          const orbit = this.orbits[i];
          ctx.save();
          ctx.rotate(orbit.tilt);
          
          ctx.strokeStyle = this.palette.glow;
          ctx.lineWidth = 0.9;
          ctx.beginPath();
          ctx.ellipse(0, 0, orbit.r, orbit.r * 0.45, 0, 0, Math.PI * 2);
          ctx.stroke();

          // Electrón orbitando
          const ex = Math.cos(orbit.angle) * orbit.r;
          const ey = Math.sin(orbit.angle) * orbit.r * 0.45;
          ctx.fillStyle = this.palette.core;
          ctx.beginPath();
          ctx.arc(ex, ey, 2.2, 0, Math.PI * 2);
          ctx.fill();

          // Destello del electrón
          ctx.fillStyle = '#ffffff';
          ctx.beginPath();
          ctx.arc(ex, ey, 1, 0, Math.PI * 2);
          ctx.fill();

          ctx.restore();
        }

        ctx.restore();
      }
    }

    function initAtoms() {
      // Ajustar cantidad de átomos según tamaño de pantalla (optimizado para rendimiento)
      const count = Math.min(Math.floor((width * height) / 45000), 24);
      atoms = [];
      for (let i = 0; i < Math.max(count, 12); i++) {
        atoms.push(new Atom());
      }
    }

    // Dibujar enlaces químicos (líneas de valencia conectando átomos cercanos)
    function drawChemicalBonds() {
      const maxDistance = 160;
      for (let i = 0; i < atoms.length; i++) {
        for (let j = i + 1; j < atoms.length; j++) {
          const dx = atoms[i].x - atoms[j].x;
          const dy = atoms[i].y - atoms[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < maxDistance) {
            const alpha = (1 - dist / maxDistance) * 0.35;
            const grad = ctx.createLinearGradient(atoms[i].x, atoms[i].y, atoms[j].x, atoms[j].y);
            grad.addColorStop(0, atoms[i].palette.core);
            grad.addColorStop(1, atoms[j].palette.core);

            ctx.strokeStyle = grad;
            ctx.globalAlpha = alpha;
            ctx.lineWidth = 1.2;
            ctx.beginPath();
            ctx.moveTo(atoms[i].x, atoms[i].y);
            ctx.lineTo(atoms[j].x, atoms[j].y);
            ctx.stroke();

            // Pequeño pulso de energía sobre el enlace
            if (dist < 100) {
              const midX = (atoms[i].x + atoms[j].x) / 2;
              const midY = (atoms[i].y + atoms[j].y) / 2;
              ctx.fillStyle = '#ffffff';
              ctx.beginPath();
              ctx.arc(midX, midY, 1.2, 0, Math.PI * 2);
              ctx.fill();
            }

            ctx.globalAlpha = 1.0;
          }
        }
      }
    }

    let animationFrameId;
    let isRunning = true;

    function render() {
      if (!isRunning) return;
      ctx.clearRect(0, 0, width, height);

      // Enlaces químicos de fondo
      drawChemicalBonds();

      // Dibujar y actualizar átomos
      for (let atom of atoms) {
        atom.update();
        atom.draw();
      }

      animationFrameId = requestAnimationFrame(render);
    }

    // Eventos de ventana
    window.addEventListener('resize', () => {
      resize();
      initAtoms();
    });

    window.addEventListener('mousemove', (e) => {
      mouse.x = e.clientX;
      mouse.y = e.clientY;
      mouse.active = true;
    });

    window.addEventListener('mouseleave', () => {
      mouse.active = false;
    });

    // Pausar render si la pestaña está en segundo plano para ahorrar batería/CPU
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        isRunning = false;
        cancelAnimationFrame(animationFrameId);
      } else {
        isRunning = true;
        render();
      }
    });

    resize();
    initAtoms();
    render();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAtomsBackground);
  } else {
    initAtomsBackground();
  }
})();
