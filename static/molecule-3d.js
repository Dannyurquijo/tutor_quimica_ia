/**
 * molecule-3d.js — Visor Molecular 3D Interactivo para Tutor de Química IA
 * Renderiza moléculas con física 3D en Canvas HTML5 (rotación táctil, profundidad y sombreado esférico).
 */

(function() {
  // Catálogo de moléculas educativas
  const MOLECULES = {
    h2o: {
      name: "Agua (H₂O)",
      formula: "H₂O",
      geometry: "Angular (104.5°)",
      enlace: "Covalente Polar",
      desc: "Dos átomos de hidrógeno unidos covalentemente a un oxígeno central con dipolo eléctrico permanente.",
      atoms: [
        { elem: "O", x: 0, y: -15, z: 0, r: 30, color: "#ef4444", label: "O (-)" },
        { elem: "H", x: -65, y: 35, z: 0, r: 18, color: "#f8fafc", label: "H (+)" },
        { elem: "H", x: 65, y: 35, z: 0, r: 18, color: "#f8fafc", label: "H (+)" }
      ],
      bonds: [
        [0, 1],
        [0, 2]
      ]
    },
    co2: {
      name: "Dióxido de Carbono (CO₂)",
      formula: "CO₂",
      geometry: "Lineal (180°)",
      enlace: "Covalente No Polar (molécula simétrica)",
      desc: "Un carbono central con dobles enlaces covalentes a dos oxígenos opuestos.",
      atoms: [
        { elem: "C", x: 0, y: 0, z: 0, r: 28, color: "#334155", label: "C" },
        { elem: "O", x: -90, y: 0, z: 0, r: 26, color: "#ef4444", label: "O" },
        { elem: "O", x: 90, y: 0, z: 0, r: 26, color: "#ef4444", label: "O" }
      ],
      bonds: [
        [0, 1],
        [0, 2]
      ]
    },
    ch4: {
      name: "Metano (CH₄)",
      formula: "CH₄",
      geometry: "Tetraédrica (109.5°)",
      enlace: "Covalente No Polar",
      desc: "Un carbono central rodeado simétricamente por cuatro hidrógenos en los vértices de un tetraedro.",
      atoms: [
        { elem: "C", x: 0, y: 0, z: 0, r: 30, color: "#1e293b", label: "C" },
        { elem: "H", x: 0, y: -75, z: 0, r: 18, color: "#f8fafc", label: "H" },
        { elem: "H", x: 70, y: 28, z: 0, r: 18, color: "#f8fafc", label: "H" },
        { elem: "H", x: -35, y: 28, z: 62, r: 18, color: "#f8fafc", label: "H" },
        { elem: "H", x: -35, y: 28, z: -62, r: 18, color: "#f8fafc", label: "H" }
      ],
      bonds: [
        [0, 1],
        [0, 2],
        [0, 3],
        [0, 4]
      ]
    },
    nacl: {
      name: "Cloruro de Sodio (Sal Común - NaCl)",
      formula: "NaCl",
      geometry: "Red Iónica Cristalina",
      enlace: "Iónico (Atracción electrostática)",
      desc: "Transferencia de 1 electrón del Sodio (Na⁺ catión) al Cloro (Cl⁻ anión).",
      atoms: [
        { elem: "Na", x: -55, y: 0, z: 0, r: 26, color: "#8b5cf6", label: "Na⁺ (Catión)" },
        { elem: "Cl", x: 60, y: 0, z: 0, r: 36, color: "#10b981", label: "Cl⁻ (Anión)" }
      ],
      bonds: [
        [0, 1]
      ]
    },
    nh3: {
      name: "Amoníaco (NH₃)",
      formula: "NH₃",
      geometry: "Piramidal Trigonal (107°)",
      enlace: "Covalente Polar",
      desc: "Un nitrógeno central con un par de electrones libres que empuja a tres hidrógenos hacia abajo.",
      atoms: [
        { elem: "N", x: 0, y: -25, z: 0, r: 28, color: "#2563eb", label: "N" },
        { elem: "H", x: -55, y: 35, z: -25, r: 18, color: "#f8fafc", label: "H" },
        { elem: "H", x: 55, y: 35, z: -25, r: 18, color: "#f8fafc", label: "H" },
        { elem: "H", x: 0, y: 35, z: 55, r: 18, color: "#f8fafc", label: "H" }
      ],
      bonds: [
        [0, 1],
        [0, 2],
        [0, 3]
      ]
    }
  };

  let activeMolKey = "h2o";
  let canvas, ctx;
  let rotX = 0.2, rotY = 0.4;
  let velX = 0.003, velY = 0.005;
  let isDragging = false;
  let lastMouseX = 0, lastMouseY = 0;
  let animId = null;
  let autoRotate = true;

  function initViewer() {
    canvas = document.getElementById("mol3dCanvas");
    if (!canvas) return;
    ctx = canvas.getContext("2d");

    function resize() {
      const rect = canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      ctx.scale(dpr, dpr);
    }
    resize();
    window.addEventListener("resize", resize);

    // Eventos de Mouse
    canvas.addEventListener("mousedown", (e) => {
      isDragging = true;
      lastMouseX = e.clientX;
      lastMouseY = e.clientY;
      autoRotate = false;
    });

    window.addEventListener("mousemove", (e) => {
      if (!isDragging) return;
      const dx = e.clientX - lastMouseX;
      const dy = e.clientY - lastMouseY;
      rotY += dx * 0.012;
      rotX += dy * 0.012;
      velX = dy * 0.002;
      velY = dx * 0.002;
      lastMouseX = e.clientX;
      lastMouseY = e.clientY;
    });

    window.addEventListener("mouseup", () => {
      isDragging = false;
    });

    // Eventos Touch para móviles
    canvas.addEventListener("touchstart", (e) => {
      if (e.touches.length === 1) {
        isDragging = true;
        lastMouseX = e.touches[0].clientX;
        lastMouseY = e.touches[0].clientY;
        autoRotate = false;
      }
    }, { passive: true });

    canvas.addEventListener("touchmove", (e) => {
      if (!isDragging || e.touches.length !== 1) return;
      const dx = e.touches[0].clientX - lastMouseX;
      const dy = e.touches[0].clientY - lastMouseY;
      rotY += dx * 0.015;
      rotX += dy * 0.015;
      velX = dy * 0.002;
      velY = dx * 0.002;
      lastMouseX = e.touches[0].clientX;
      lastMouseY = e.touches[0].clientY;
    }, { passive: true });

    canvas.addEventListener("touchend", () => {
      isDragging = false;
    });

    renderLoop();
    updateUIInfo();
  }

  function rotatePoint(x, y, z, rx, ry) {
    // Rotar en Y
    const cosY = Math.cos(ry);
    const sinY = Math.sin(ry);
    const x1 = x * cosY + z * sinY;
    const z1 = -x * sinY + z * cosY;

    // Rotar en X
    const cosX = Math.cos(rx);
    const sinX = Math.sin(rx);
    const y2 = y * cosX - z1 * sinX;
    const z2 = y * sinX + z1 * cosX;

    return { x: x1, y: y2, z: z2 };
  }

  function renderLoop() {
    if (!canvas || !ctx) return;
    const w = canvas.getBoundingClientRect().width;
    const h = canvas.getBoundingClientRect().height;
    const cx = w / 2;
    const cy = h / 2;

    ctx.clearRect(0, 0, w, h);

    if (autoRotate) {
      rotY += 0.012;
      rotX += 0.004;
    } else if (!isDragging) {
      rotX += velX;
      rotY += velY;
      velX *= 0.95;
      velY *= 0.95;
      if (Math.abs(velX) < 0.0001 && Math.abs(velY) < 0.0001) {
        autoRotate = true;
      }
    }

    const mol = MOLECULES[activeMolKey];
    if (!mol) return;

    // 1. Proyectar átomos en 3D
    const fov = 350;
    const projectedAtoms = mol.atoms.map((atom, idx) => {
      const p = rotatePoint(atom.x, atom.y, atom.z, rotX, rotY);
      const scale = fov / (fov + p.z);
      return {
        id: idx,
        elem: atom.elem,
        label: atom.label,
        color: atom.color,
        origR: atom.r,
        px: cx + p.x * scale,
        py: cy + p.y * scale,
        pz: p.z,
        scale: scale,
        r: atom.r * scale
      };
    });

    // 2. Ordenar por profundidad Z (Pintor: lo más lejano se dibuja primero)
    const renderQueue = [];

    // Añadir enlaces a la cola
    mol.bonds.forEach(([aIdx, bIdx]) => {
      const a = projectedAtoms[aIdx];
      const b = projectedAtoms[bIdx];
      const avgZ = (a.pz + b.pz) / 2;
      renderQueue.push({
        type: "bond",
        z: avgZ,
        a: a,
        b: b
      });
    });

    // Añadir átomos a la cola
    projectedAtoms.forEach(a => {
      renderQueue.push({
        type: "atom",
        z: a.pz,
        atom: a
      });
    });

    renderQueue.sort((i1, i2) => i2.z - i1.z); // Z mayor (más profundo) primero

    // 3. Dibujar elementos
    renderQueue.forEach(item => {
      if (item.type === "bond") {
        drawBond(item.a, item.b);
      } else {
        drawAtom(item.atom);
      }
    });

    animId = requestAnimationFrame(renderLoop);
  }

  function drawBond(a, b) {
    ctx.save();
    const bondWidth = Math.max(4, 9 * Math.min(a.scale, b.scale));
    
    // Gradiente a lo largo del enlace
    const grad = ctx.createLinearGradient(a.px, a.py, b.px, b.py);
    grad.addColorStop(0, "rgba(148, 163, 184, 0.8)");
    grad.addColorStop(0.5, "rgba(226, 232, 240, 0.95)");
    grad.addColorStop(1, "rgba(148, 163, 184, 0.8)");

    ctx.strokeStyle = grad;
    ctx.lineWidth = bondWidth;
    ctx.lineCap = "round";

    ctx.beginPath();
    ctx.moveTo(a.px, a.py);
    ctx.lineTo(b.px, b.py);
    ctx.stroke();

    // Línea de brillo central del cilindro
    ctx.strokeStyle = "rgba(255, 255, 255, 0.5)";
    ctx.lineWidth = bondWidth * 0.35;
    ctx.beginPath();
    ctx.moveTo(a.px, a.py);
    ctx.lineTo(b.px, b.py);
    ctx.stroke();

    ctx.restore();
  }

  function drawAtom(atom) {
    ctx.save();
    const { px, py, r, color, label } = atom;

    // Sombra proyectada
    ctx.beginPath();
    ctx.arc(px, py, r, 0, Math.PI * 2);
    ctx.fillStyle = color;
    ctx.shadowColor = "rgba(0, 0, 0, 0.35)";
    ctx.shadowBlur = 12 * atom.scale;
    ctx.shadowOffsetX = 3 * atom.scale;
    ctx.shadowOffsetY = 4 * atom.scale;
    ctx.fill();
    ctx.restore();

    ctx.save();
    // Iluminación esférica 3D (gradiente radial)
    const highlightX = px - r * 0.32;
    const highlightY = py - r * 0.35;
    const sphereGrad = ctx.createRadialGradient(
      highlightX, highlightY, r * 0.08,
      px, py, r
    );

    sphereGrad.addColorStop(0, "#ffffff");
    sphereGrad.addColorStop(0.2, color);
    sphereGrad.addColorStop(0.8, color);
    sphereGrad.addColorStop(1, shadeColor(color, -35));

    ctx.beginPath();
    ctx.arc(px, py, r, 0, Math.PI * 2);
    ctx.fillStyle = sphereGrad;
    ctx.fill();

    // Borde sutil
    ctx.strokeStyle = "rgba(255, 255, 255, 0.35)";
    ctx.lineWidth = 1.2;
    ctx.stroke();

    // Etiqueta del elemento
    ctx.font = `bold ${Math.max(10, Math.round(13 * atom.scale))}px "SF Pro Display", sans-serif`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillStyle = (atom.elem === "H") ? "#0f172a" : "#ffffff";
    ctx.shadowColor = "rgba(0, 0, 0, 0.4)";
    ctx.shadowBlur = 3;
    ctx.fillText(atom.elem, px, py);

    ctx.restore();
  }

  function shadeColor(color, percent) {
    let R = parseInt(color.substring(1,3), 16);
    let G = parseInt(color.substring(3,5), 16);
    let B = parseInt(color.substring(5,7), 16);

    R = parseInt(R * (100 + percent) / 100);
    G = parseInt(G * (100 + percent) / 100);
    B = parseInt(B * (100 + percent) / 100);

    R = (R < 255) ? R : 255;  
    G = (G < 255) ? G : 255;  
    B = (B < 255) ? B : 255;  

    const RR = ((R.toString(16).length === 1) ? "0" + R.toString(16) : R.toString(16));
    const GG = ((G.toString(16).length === 1) ? "0" + G.toString(16) : G.toString(16));
    const BB = ((B.toString(16).length === 1) ? "0" + B.toString(16) : B.toString(16));

    return "#" + RR + GG + BB;
  }

  function updateUIInfo() {
    const mol = MOLECULES[activeMolKey];
    if (!mol) return;

    const titleEl = document.getElementById("mol3dTitle");
    const geomEl = document.getElementById("mol3dGeometry");
    const bondEl = document.getElementById("mol3dBond");
    const descEl = document.getElementById("mol3dDesc");

    if (titleEl) titleEl.textContent = mol.name;
    if (geomEl) geomEl.textContent = mol.geometry;
    if (bondEl) bondEl.textContent = mol.enlace;
    if (descEl) descEl.textContent = mol.desc;
  }

  // API Global accesible desde la vista
  window.MoleculeViewer = {
    init: initViewer,
    selectMolecule: function(key) {
      if (MOLECULES[key]) {
        activeMolKey = key;
        autoRotate = true;
        updateUIInfo();
      }
    },
    toggleAutoRotate: function() {
      autoRotate = !autoRotate;
    }
  };
})();
