import os

DIAGRAMS_DIR = os.path.join(os.path.dirname(__file__), "static", "diagrams")
os.makedirs(DIAGRAMS_DIR, exist_ok=True)

# 1. Molécula de Agua y Polaridad
agua_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 540" width="100%" height="100%" style="background:#0b1329; font-family:'Segoe UI',system-ui,sans-serif;">
  <defs>
    <radialGradient id="oxGrad" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#ff6b6b"/>
      <stop offset="40%" stop-color="#ee5253"/>
      <stop offset="85%" stop-color="#c0392b"/>
      <stop offset="100%" stop-color="#5f27cd" stop-opacity="0.6"/>
    </radialGradient>
    <radialGradient id="hGrad" cx="30%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="50%" stop-color="#e2e8f0"/>
      <stop offset="85%" stop-color="#94a3b8"/>
      <stop offset="100%" stop-color="#475569"/>
    </radialGradient>
    <linearGradient id="bondGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ee5253"/>
      <stop offset="50%" stop-color="#f1f5f9"/>
      <stop offset="100%" stop-color="#cbd5e1"/>
    </linearGradient>
    <filter id="atomShadow" x="-20%" y="-20%" width="150%" height="150%">
      <feDropShadow dx="0" dy="12" stdDeviation="14" flood-color="#000000" flood-opacity="0.6"/>
    </filter>
  </defs>

  <rect x="25" y="20" width="790" height="58" rx="14" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="50" y="55" fill="#38bdf8" font-size="20" font-weight="800">Estructura y Polaridad de la Molécula de Agua (H₂O)</text>
  <text x="670" y="55" fill="#f59e0b" font-size="14" font-weight="bold">Geometría Angular</text>

  <g transform="translate(50, 40)">
    <line x1="270" y1="210" x2="150" y2="340" stroke="url(#bondGrad1)" stroke-width="18" stroke-linecap="round"/>
    <line x1="270" y1="210" x2="150" y2="340" stroke="#ffffff" stroke-width="4" stroke-linecap="round" opacity="0.6"/>

    <line x1="270" y1="210" x2="390" y2="340" stroke="url(#bondGrad1)" stroke-width="18" stroke-linecap="round"/>
    <line x1="270" y1="210" x2="390" y2="340" stroke="#ffffff" stroke-width="4" stroke-linecap="round" opacity="0.6"/>

    <path d="M 215 270 A 75 75 0 0 0 325 270" fill="none" stroke="#f59e0b" stroke-width="3.5" stroke-dasharray="6 4"/>
    <rect x="235" y="285" width="70" height="28" rx="8" fill="#0f172a" stroke="#f59e0b" stroke-width="1"/>
    <text x="270" y="304" fill="#f59e0b" font-size="14" font-weight="800" text-anchor="middle">104.5°</text>

    <circle cx="270" cy="210" r="65" fill="url(#oxGrad)" filter="url(#atomShadow)"/>
    <text x="270" y="218" fill="#ffffff" font-size="28" font-weight="900" text-anchor="middle">O</text>
    <rect x="235" y="110" width="70" height="28" rx="8" fill="#dc2626" stroke="#fca5a5" stroke-width="1.5"/>
    <text x="270" y="129" fill="#ffffff" font-size="16" font-weight="900" text-anchor="middle">δ 2−</text>

    <ellipse cx="215" cy="155" rx="14" ry="7" fill="#38bdf8" opacity="0.8" transform="rotate(-35 215 155)"/>
    <ellipse cx="325" cy="155" rx="14" ry="7" fill="#38bdf8" opacity="0.8" transform="rotate(35 325 155)"/>
    <text x="270" y="95" fill="#94a3b8" font-size="11" font-weight="bold" text-anchor="middle">2 pares de electrones libres (repulsión)</text>

    <circle cx="150" cy="340" r="42" fill="url(#hGrad)" filter="url(#atomShadow)"/>
    <text x="150" y="347" fill="#0f172a" font-size="20" font-weight="900" text-anchor="middle">H</text>
    <rect x="115" y="395" width="70" height="26" rx="8" fill="#0284c7" stroke="#7dd3fc" stroke-width="1.5"/>
    <text x="150" y="413" fill="#ffffff" font-size="15" font-weight="900" text-anchor="middle">δ +</text>

    <circle cx="390" cy="340" r="42" fill="url(#hGrad)" filter="url(#atomShadow)"/>
    <text x="390" y="347" fill="#0f172a" font-size="20" font-weight="900" text-anchor="middle">H</text>
    <rect x="355" y="395" width="70" height="26" rx="8" fill="#0284c7" stroke="#7dd3fc" stroke-width="1.5"/>
    <text x="390" y="413" fill="#ffffff" font-size="15" font-weight="900" text-anchor="middle">δ +</text>

    <g transform="translate(30, 0)">
      <line x1="470" y1="350" x2="470" y2="160" stroke="#a855f7" stroke-width="6" stroke-linecap="round"/>
      <line x1="455" y1="350" x2="485" y2="350" stroke="#a855f7" stroke-width="5" stroke-linecap="round"/>
      <polygon points="470,140 458,165 482,165" fill="#a855f7"/>
      <text x="540" y="245" fill="#c084fc" font-size="14" font-weight="800">Momento Dipolar Neto (μ ≠ 0)</text>
      <text x="540" y="265" fill="#94a3b8" font-size="12">Apunta hacia el polo negativo (Oxígeno)</text>
    </g>
  </g>

  <rect x="490" y="330" width="325" height="175" rx="14" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
  <text x="510" y="358" fill="#38bdf8" font-size="14" font-weight="bold">💡 ¿Por qué es polar y no se anula?</text>
  <text x="510" y="385" fill="#cbd5e1" font-size="12">1. El Oxígeno (EN=3.44) atrae con más</text>
  <text x="510" y="403" fill="#cbd5e1" font-size="12">   fuerza a los electrones que el H (EN=2.20).</text>
  <text x="510" y="428" fill="#cbd5e1" font-size="12">2. Su forma es ANGULAR, por lo que los</text>
  <text x="510" y="446" fill="#cbd5e1" font-size="12">   dipolos no se cancelan (a diferencia del CO₂).</text>
  <text x="510" y="475" fill="#4ade80" font-size="12" font-weight="bold">✔ Resultado: Molécula Covalente Polar</text>
</svg>"""

# 2. Conducción Eléctrica de NaCl en Solución
nacl_electricidad_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 540" width="100%" height="100%" style="background:#0b1329; font-family:'Segoe UI',system-ui,sans-serif;">
  <defs>
    <radialGradient id="naGrad" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#c084fc"/>
      <stop offset="60%" stop-color="#8b5cf6"/>
      <stop offset="100%" stop-color="#581c87"/>
    </radialGradient>
    <radialGradient id="clGrad" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#4ade80"/>
      <stop offset="60%" stop-color="#10b981"/>
      <stop offset="100%" stop-color="#064e3b"/>
    </radialGradient>
    <filter id="glowFoco" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="25" y="20" width="790" height="58" rx="14" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="50" y="55" fill="#38bdf8" font-size="20" font-weight="800">Conducción Eléctrica: Disociación de Sal (NaCl) en Solución Acuosa</text>

  <!-- LADO IZQUIERDO: CRISTAL SÓLIDO (NO CONDUCE) -->
  <g transform="translate(30, 95)">
    <rect x="0" y="0" width="360" height="320" rx="16" fill="#1e293b" stroke="#ef4444" stroke-width="1.5"/>
    <text x="25" y="35" fill="#ef4444" font-size="16" font-weight="800">1. Estado Sólido (Cristal)</text>
    <text x="25" y="55" fill="#94a3b8" font-size="12">Los iones están FIJOS en la red cristalina</text>

    <!-- Foco Apagado -->
    <circle cx="180" cy="115" r="22" fill="#334155" stroke="#64748b" stroke-width="2"/>
    <text x="180" y="120" fill="#94a3b8" font-size="11" font-weight="bold" text-anchor="middle">Apagado</text>

    <!-- Red cristalina de esferas compactas -->
    <g transform="translate(65, 160)">
      <!-- Fila 1 -->
      <circle cx="40" cy="30" r="16" fill="url(#naGrad)"/><text x="40" y="34" fill="#fff" font-size="10" font-weight="bold" text-anchor="middle">Na⁺</text>
      <circle cx="85" cy="30" r="22" fill="url(#clGrad)"/><text x="85" y="35" fill="#fff" font-size="12" font-weight="bold" text-anchor="middle">Cl⁻</text>
      <circle cx="130" cy="30" r="16" fill="url(#naGrad)"/><text x="130" y="34" fill="#fff" font-size="10" font-weight="bold" text-anchor="middle">Na⁺</text>
      <circle cx="175" cy="30" r="22" fill="url(#clGrad)"/><text x="175" y="35" fill="#fff" font-size="12" font-weight="bold" text-anchor="middle">Cl⁻</text>

      <!-- Fila 2 -->
      <circle cx="40" cy="75" r="22" fill="url(#clGrad)"/><text x="40" y="80" fill="#fff" font-size="12" font-weight="bold" text-anchor="middle">Cl⁻</text>
      <circle cx="85" cy="75" r="16" fill="url(#naGrad)"/><text x="85" y="79" fill="#fff" font-size="10" font-weight="bold" text-anchor="middle">Na⁺</text>
      <circle cx="130" cy="75" r="22" fill="url(#clGrad)"/><text x="130" y="80" fill="#fff" font-size="12" font-weight="bold" text-anchor="middle">Cl⁻</text>
      <circle cx="175" cy="75" r="16" fill="url(#naGrad)"/><text x="175" y="79" fill="#fff" font-size="10" font-weight="bold" text-anchor="middle">Na⁺</text>
    </g>

    <rect x="25" y="260" width="310" height="42" rx="8" fill="#0f172a"/>
    <text x="35" y="286" fill="#fca5a5" font-size="12" font-weight="bold">❌ NO conduce: No hay cargas libres en movimiento</text>
  </g>

  <!-- LADO DERECHO: SOLUCIÓN ACUOSA (SÍ CONDUCE) -->
  <g transform="translate(420, 95)">
    <rect x="0" y="0" width="395" height="320" rx="16" fill="#1e293b" stroke="#10b981" stroke-width="1.5"/>
    <text x="25" y="35" fill="#10b981" font-size="16" font-weight="800">2. En Solución Acuosa (Disuelto en H₂O)</text>
    <text x="25" y="55" fill="#94a3b8" font-size="12">El agua disocia la sal en IONES MÓVILES</text>

    <!-- Foco Encendido con brillo -->
    <circle cx="200" cy="115" r="24" fill="#facc15" filter="url(#glowFoco)"/>
    <circle cx="200" cy="115" r="24" fill="#fef08a"/>
    <text x="200" y="120" fill="#854d0e" font-size="11" font-weight="black" text-anchor="middle">¡LUZ!</text>

    <!-- Vaso de agua con electrodos -->
    <rect x="70" y="170" width="260" height="85" rx="10" fill="#0284c7" opacity="0.35"/>
    <!-- Electrodos -->
    <rect x="110" y="150" width="14" height="90" fill="#64748b" stroke="#94a3b8"/>
    <rect x="270" y="150" width="14" height="90" fill="#64748b" stroke="#94a3b8"/>
    <text x="117" y="145" fill="#f87171" font-size="11" font-weight="bold" text-anchor="middle">(+)</text>
    <text x="277" y="145" fill="#38bdf8" font-size="11" font-weight="bold" text-anchor="middle">(−)</text>

    <!-- Iones libres flotando con flechas -->
    <circle cx="160" cy="195" r="16" fill="url(#naGrad)"/><text x="160" y="199" fill="#fff" font-size="10" font-weight="bold" text-anchor="middle">Na⁺</text>
    <path d="M 180 195 L 250 195" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4 2" marker-end="url(#arrow)"/>

    <circle cx="220" cy="225" r="20" fill="url(#clGrad)"/><text x="220" y="230" fill="#fff" font-size="12" font-weight="bold" text-anchor="middle">Cl⁻</text>
    <path d="M 195 225 L 135 225" stroke="#f87171" stroke-width="2" stroke-dasharray="4 2"/>

    <rect x="25" y="260" width="345" height="42" rx="8" fill="#0f172a"/>
    <text x="35" y="286" fill="#4ade80" font-size="12" font-weight="bold">✔ SÍ conduce: Iones libres transportan la electricidad</text>
  </g>

  <!-- RESUMEN PEDAGÓGICO INFERIOR -->
  <rect x="25" y="430" width="790" height="90" rx="14" fill="#1e293b" stroke="#334155"/>
  <text x="45" y="458" fill="#f59e0b" font-size="14" font-weight="800">💡 Regla Científica de Oro:</text>
  <text x="45" y="482" fill="#e2e8f0" font-size="13">Para conducir electricidad se requieren dos condiciones: <tspan fill="#38bdf8" font-weight="bold">1) Cargas eléctricas</tspan> y <tspan fill="#38bdf8" font-weight="bold">2) Movilidad física</tspan>.</text>
  <text x="45" y="504" fill="#94a3b8" font-size="12">En el cristal sólido los iones están atrapados; al disolverse en agua se hidratan y fluyen libremente hacia los electrodos.</text>
</svg>"""

# 3. Geometría Molecular VSEPR (RPECV)
vsepr_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 540" width="100%" height="100%" style="background:#0b1329; font-family:'Segoe UI',system-ui,sans-serif;">
  <rect x="25" y="20" width="790" height="58" rx="14" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="50" y="55" fill="#38bdf8" font-size="20" font-weight="800">Geometría Molecular 3D — Teoría de Repulsión (VSEPR / RPECV)</text>

  <!-- 4 TARJETAS COMPARATIVAS -->
  <!-- 1. LINEAL -->
  <g transform="translate(30, 95)">
    <rect x="0" y="0" width="180" height="310" rx="14" fill="#1e293b" stroke="#334155"/>
    <text x="20" y="32" fill="#38bdf8" font-size="15" font-weight="800">1. Lineal</text>
    <text x="20" y="52" fill="#f59e0b" font-size="13" font-weight="bold">Ángulo: 180°</text>

    <!-- Molécula CO2 -->
    <g transform="translate(90, 150)">
      <line x1="-55" y1="0" x2="55" y2="0" stroke="#94a3b8" stroke-width="8" stroke-linecap="round"/>
      <circle cx="0" cy="0" r="22" fill="#334155" stroke="#94a3b8" stroke-width="2"/><text x="0" y="5" fill="#fff" font-size="11" font-weight="bold" text-anchor="middle">C</text>
      <circle cx="-55" cy="0" r="18" fill="#ef4444"/><text x="-55" y="4" fill="#fff" font-size="10" font-weight="bold" text-anchor="middle">O</text>
      <circle cx="55" cy="0" r="18" fill="#ef4444"/><text x="55" y="4" fill="#fff" font-size="10" font-weight="bold" text-anchor="middle">O</text>
    </g>

    <text x="90" y="240" fill="#94a3b8" font-size="11" text-anchor="middle">Ejemplo: CO₂, BeCl₂</text>
    <rect x="15" y="255" width="150" height="36" rx="8" fill="#0f172a"/>
    <text x="90" y="278" fill="#4ade80" font-size="11" font-weight="bold" text-anchor="middle">No Polar (Simétrica)</text>
  </g>

  <!-- 2. ANGULAR -->
  <g transform="translate(230, 95)">
    <rect x="0" y="0" width="180" height="310" rx="14" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
    <text x="20" y="32" fill="#38bdf8" font-size="15" font-weight="800">2. Angular</text>
    <text x="20" y="52" fill="#f59e0b" font-size="13" font-weight="bold">Ángulo: 104.5°</text>

    <!-- Molécula H2O -->
    <g transform="translate(90, 130)">
      <line x1="0" y1="0" x2="-40" y2="55" stroke="#94a3b8" stroke-width="7" stroke-linecap="round"/>
      <line x1="0" y1="0" x2="40" y2="55" stroke="#94a3b8" stroke-width="7" stroke-linecap="round"/>
      <circle cx="0" cy="0" r="24" fill="#ef4444"/><text x="0" y="5" fill="#fff" font-size="12" font-weight="bold" text-anchor="middle">O</text>
      <circle cx="-40" cy="55" r="15" fill="#f1f5f9"/><text x="-40" y="59" fill="#0f172a" font-size="10" font-weight="bold" text-anchor="middle">H</text>
      <circle cx="40" cy="55" r="15" fill="#f1f5f9"/><text x="40" y="59" fill="#0f172a" font-size="10" font-weight="bold" text-anchor="middle">H</text>
    </g>

    <text x="90" y="240" fill="#94a3b8" font-size="11" text-anchor="middle">Ejemplo: H₂O, SO₂</text>
    <rect x="15" y="255" width="150" height="36" rx="8" fill="#0f172a"/>
    <text x="90" y="278" fill="#38bdf8" font-size="11" font-weight="bold" text-anchor="middle">POLAR (Dipolo neto)</text>
  </g>

  <!-- 3. TRIGONAL PLANA -->
  <g transform="translate(430, 95)">
    <rect x="0" y="0" width="180" height="310" rx="14" fill="#1e293b" stroke="#334155"/>
    <text x="20" y="32" fill="#38bdf8" font-size="15" font-weight="800">3. Trigonal Plana</text>
    <text x="20" y="52" fill="#f59e0b" font-size="13" font-weight="bold">Ángulo: 120°</text>

    <!-- Molécula BF3 -->
    <g transform="translate(90, 150)">
      <line x1="0" y1="0" x2="0" y2="-50" stroke="#94a3b8" stroke-width="6" stroke-linecap="round"/>
      <line x1="0" y1="0" x2="-45" y2="35" stroke="#94a3b8" stroke-width="6" stroke-linecap="round"/>
      <line x1="0" y1="0" x2="45" y2="35" stroke="#94a3b8" stroke-width="6" stroke-linecap="round"/>
      <circle cx="0" cy="0" r="20" fill="#ec4899"/><text x="0" y="4" fill="#fff" font-size="10" font-weight="bold" text-anchor="middle">B</text>
      <circle cx="0" cy="-50" r="15" fill="#a855f7"/><text x="0" y="-46" fill="#fff" font-size="9" font-weight="bold" text-anchor="middle">F</text>
      <circle cx="-45" cy="35" r="15" fill="#a855f7"/><text x="-45" y="39" fill="#fff" font-size="9" font-weight="bold" text-anchor="middle">F</text>
      <circle cx="45" cy="35" r="15" fill="#a855f7"/><text x="45" y="39" fill="#fff" font-size="9" font-weight="bold" text-anchor="middle">F</text>
    </g>

    <text x="90" y="240" fill="#94a3b8" font-size="11" text-anchor="middle">Ejemplo: BF₃, SO₃</text>
    <rect x="15" y="255" width="150" height="36" rx="8" fill="#0f172a"/>
    <text x="90" y="278" fill="#4ade80" font-size="11" font-weight="bold" text-anchor="middle">No Polar (Simétrica)</text>
  </g>

  <!-- 4. TETRAÉDRICA -->
  <g transform="translate(630, 95)">
    <rect x="0" y="0" width="180" height="310" rx="14" fill="#1e293b" stroke="#334155"/>
    <text x="20" y="32" fill="#38bdf8" font-size="15" font-weight="800">4. Tetraédrica</text>
    <text x="20" y="52" fill="#f59e0b" font-size="13" font-weight="bold">Ángulo: 109.5°</text>

    <!-- Molécula CH4 -->
    <g transform="translate(90, 150)">
      <line x1="0" y1="0" x2="0" y2="-50" stroke="#94a3b8" stroke-width="6" stroke-linecap="round"/>
      <line x1="0" y1="0" x2="45" y2="25" stroke="#94a3b8" stroke-width="6" stroke-linecap="round"/>
      <line x1="0" y1="0" x2="-40" y2="35" stroke="#94a3b8" stroke-width="6" stroke-linecap="round"/>
      <line x1="0" y1="0" x2="-20" y2="45" stroke="#64748b" stroke-width="8" stroke-dasharray="2 3"/>
      <circle cx="0" cy="0" r="22" fill="#1e293b" stroke="#94a3b8"/><text x="0" y="4" fill="#fff" font-size="11" font-weight="bold" text-anchor="middle">C</text>
      <circle cx="0" cy="-50" r="14" fill="#f1f5f9"/><text x="0" y="-46" fill="#0f172a" font-size="9" font-weight="bold" text-anchor="middle">H</text>
      <circle cx="45" cy="25" r="14" fill="#f1f5f9"/><text x="45" y="29" fill="#0f172a" font-size="9" font-weight="bold" text-anchor="middle">H</text>
      <circle cx="-40" cy="35" r="14" fill="#f1f5f9"/><text x="-40" y="39" fill="#0f172a" font-size="9" font-weight="bold" text-anchor="middle">H</text>
    </g>

    <text x="90" y="240" fill="#94a3b8" font-size="11" text-anchor="middle">Ejemplo: CH₄, CCl₄</text>
    <rect x="15" y="255" width="150" height="36" rx="8" fill="#0f172a"/>
    <text x="90" y="278" fill="#4ade80" font-size="11" font-weight="bold" text-anchor="middle">No Polar (Simétrica)</text>
  </g>

  <!-- BARRA INFERIOR -->
  <rect x="25" y="425" width="790" height="95" rx="14" fill="#1e293b" stroke="#334155"/>
  <text x="45" y="452" fill="#38bdf8" font-size="14" font-weight="800">💡 ¿Por qué se forman estas geometrías espaciales?</text>
  <text x="45" y="476" fill="#e2e8f0" font-size="13">Los pares de electrones alrededor del átomo central tienen carga negativa y <tspan fill="#f59e0b" font-weight="bold">SE REPELEN AL MÁXIMO</tspan>.</text>
  <text x="45" y="498" fill="#94a3b8" font-size="12">Se acomodan en el espacio tridimensional a la mayor distancia angular posible para minimizar la energía de repulsión.</text>
</svg>"""

with open(os.path.join(DIAGRAMS_DIR, "molecula_agua_polaridad.svg"), "w", encoding="utf-8") as f:
    f.write(agua_svg)
print("Created molecula_agua_polaridad.svg")

with open(os.path.join(DIAGRAMS_DIR, "disolucion_nacl_electricidad.svg"), "w", encoding="utf-8") as f:
    f.write(nacl_electricidad_svg)
print("Created disolucion_nacl_electricidad.svg")

with open(os.path.join(DIAGRAMS_DIR, "geometria_molecular_vsepr.svg"), "w", encoding="utf-8") as f:
    f.write(vsepr_svg)
print("Created geometria_molecular_vsepr.svg")

# 4. Enlaces Químicos Realistas (Covalente vs Iónico)
enlaces_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 620" width="100%" height="100%">
  <defs>
    <filter id="glow-cyan" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <filter id="glow-gold" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="5" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <filter id="shadow-soft" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="12" stdDeviation="10" flood-color="#000000" flood-opacity="0.6"/>
    </filter>
    <radialGradient id="sphere-oxygen" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#ff8585" />
      <stop offset="35%" stop-color="#ef4444" />
      <stop offset="75%" stop-color="#991b1b" />
      <stop offset="100%" stop-color="#450a0a" />
    </radialGradient>
    <radialGradient id="sphere-hydrogen" cx="30%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="45%" stop-color="#e2e8f0" />
      <stop offset="80%" stop-color="#94a3b8" />
      <stop offset="100%" stop-color="#475569" />
    </radialGradient>
    <radialGradient id="sphere-sodium" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#c084fc" />
      <stop offset="40%" stop-color="#8b5cf6" />
      <stop offset="80%" stop-color="#5b21b6" />
      <stop offset="100%" stop-color="#2e1065" />
    </radialGradient>
    <radialGradient id="sphere-chlorine" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#86efac" />
      <stop offset="35%" stop-color="#22c55e" />
      <stop offset="75%" stop-color="#15803d" />
      <stop offset="100%" stop-color="#052e16" />
    </radialGradient>
    <radialGradient id="covalent-cloud" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.5" />
      <stop offset="60%" stop-color="#0284c7" stop-opacity="0.2" />
      <stop offset="100%" stop-color="#0369a1" stop-opacity="0" />
    </radialGradient>
  </defs>

  <rect width="1000" height="620" fill="#090d16" />
  <g transform="translate(30, 24)">
    <rect width="940" height="60" rx="14" fill="#0f172a" stroke="#334155" stroke-width="1.2" filter="url(#shadow-soft)"/>
    <text x="35" y="38" fill="#38bdf8" font-size="20" font-weight="900" text-anchor="middle" font-family="'Segoe UI',sans-serif">&#x269B;</text>
    <text x="65" y="32" fill="#f8fafc" font-size="17" font-weight="800" font-family="'Segoe UI',sans-serif">ENLACES QUÍMICOS FUNDAMENTALES: COMPARATIVA COVALENTE vs. IÓNICO</text>
    <text x="65" y="49" fill="#94a3b8" font-size="12" font-family="'Segoe UI',sans-serif">Diferencia de electronegatividad, compartición de electrones y atracción electrostática</text>
  </g>

  <!-- COLUMNA COVALENTE -->
  <g transform="translate(30, 105)">
    <rect width="455" height="485" rx="18" fill="#0f172a" stroke="#0284c7" stroke-width="1.8" filter="url(#shadow-soft)"/>
    <path d="M 0 18 Q 0 0 18 0 L 437 0 Q 455 0 455 18 L 455 48 L 0 48 Z" fill="#0369a1" fill-opacity="0.25" />
    <text x="20" y="31" fill="#38bdf8" font-size="15" font-weight="800" font-family="'Segoe UI',sans-serif">1. ENLACE COVALENTE (H₂O, CH₄, CO₂)</text>
    <rect x="330" y="14" width="110" height="22" rx="6" fill="#0284c7" fill-opacity="0.3"/>
    <text x="385" y="29" fill="#bae6fd" font-size="10.5" font-weight="700" text-anchor="middle" font-family="'Segoe UI',sans-serif">No metal + No metal</text>
    <text x="20" y="75" fill="#e2e8f0" font-size="13" font-weight="600" font-family="'Segoe UI',sans-serif">Mecanismo: <tspan fill="#38bdf8" font-weight="800">COMPARTICIÓN MUTUA</tspan> de electrones</text>
    <text x="20" y="94" fill="#94a3b8" font-size="11.5" font-family="'Segoe UI',sans-serif">Ambos átomos comparten electrones para alcanzar estabilidad (octeto).</text>

    <g transform="translate(225, 230)">
      <ellipse cx="-45" cy="25" rx="55" ry="32" transform="rotate(-35 -45 25)" fill="url(#covalent-cloud)"/>
      <ellipse cx="45" cy="25" rx="55" ry="32" transform="rotate(35 45 25)" fill="url(#covalent-cloud)"/>
      <line x1="0" y1="-30" x2="-80" y2="70" stroke="#38bdf8" stroke-width="2.5" stroke-dasharray="4 4" opacity="0.6"/>
      <line x1="0" y1="-30" x2="80" y2="70" stroke="#38bdf8" stroke-width="2.5" stroke-dasharray="4 4" opacity="0.6"/>
      <circle cx="0" cy="-30" r="58" fill="url(#sphere-oxygen)" filter="url(#shadow-soft)"/>
      <text x="0" y="-21" fill="#ffffff" font-size="28" font-weight="900" text-anchor="middle" font-family="'Segoe UI',sans-serif">O</text>
      <circle cx="-85" cy="75" r="34" fill="url(#sphere-hydrogen)" filter="url(#shadow-soft)"/>
      <text x="-85" y="82" fill="#0f172a" font-size="18" font-weight="900" text-anchor="middle" font-family="'Segoe UI',sans-serif">H</text>
      <circle cx="85" cy="75" r="34" fill="url(#sphere-hydrogen)" filter="url(#shadow-soft)"/>
      <text x="85" y="82" fill="#0f172a" font-size="18" font-weight="900" text-anchor="middle" font-family="'Segoe UI',sans-serif">H</text>

      <g filter="url(#glow-gold)">
        <circle cx="-45" cy="18" r="5.5" fill="#facc15"/>
        <circle cx="-35" cy="30" r="5.5" fill="#facc15"/>
        <circle cx="45" cy="18" r="5.5" fill="#facc15"/>
        <circle cx="35" cy="30" r="5.5" fill="#facc15"/>
      </g>
      <rect x="-70" y="118" width="140" height="24" rx="6" fill="#0369a1" fill-opacity="0.4" stroke="#38bdf8" stroke-width="1"/>
      <text x="0" y="134" fill="#e0f2fe" font-size="10.5" font-weight="800" text-anchor="middle" font-family="'Segoe UI',sans-serif">Pares e&#x207B; Compartidos</text>
    </g>
    <g transform="translate(18, 395)">
      <rect width="418" height="74" rx="10" fill="#090d16" stroke="#1e293b" stroke-width="1.2"/>
      <text x="14" y="24" fill="#38bdf8" font-size="12" font-weight="800" font-family="'Segoe UI',sans-serif">Regla del Covalente:</text>
      <text x="14" y="44" fill="#cbd5e1" font-size="11" font-family="'Segoe UI',sans-serif">• Los electrones orbitan entre ambos núcleos.</text>
      <text x="14" y="62" fill="#cbd5e1" font-size="11" font-family="'Segoe UI',sans-serif">• No hay iones libres aislados &#x2794; No conduce electricidad en agua pura.</text>
    </g>
  </g>

  <!-- COLUMNA IÓNICA -->
  <g transform="translate(515, 105)">
    <rect width="455" height="485" rx="18" fill="#0f172a" stroke="#ef4444" stroke-width="1.8" filter="url(#shadow-soft)"/>
    <path d="M 0 18 Q 0 0 18 0 L 437 0 Q 455 0 455 18 L 455 48 L 0 48 Z" fill="#991b1b" fill-opacity="0.25" />
    <text x="20" y="31" fill="#f87171" font-size="15" font-weight="800" font-family="'Segoe UI',sans-serif">2. ENLACE IÓNICO (NaCl, MgO, CaCl₂)</text>
    <rect x="330" y="14" width="110" height="22" rx="6" fill="#ef4444" fill-opacity="0.3"/>
    <text x="385" y="29" fill="#fecaca" font-size="10.5" font-weight="700" text-anchor="middle" font-family="'Segoe UI',sans-serif">Metal + No metal</text>
    <text x="20" y="75" fill="#e2e8f0" font-size="13" font-weight="600" font-family="'Segoe UI',sans-serif">Mecanismo: <tspan fill="#f87171" font-weight="800">TRANSFERENCIA TOTAL</tspan> de electrones</text>
    <text x="20" y="94" fill="#94a3b8" font-size="11.5" font-family="'Segoe UI',sans-serif">El metal cede su electrón de valencia al no metal muy electronegativo.</text>

    <g transform="translate(225, 230)">
      <path d="M -70 -25 Q 0 -95 70 -20" fill="none" stroke="#facc15" stroke-width="3" stroke-dasharray="6 4" />
      <polygon points="73,-14 62,-26 73,-30" fill="#facc15"/>
      <circle cx="0" cy="-60" r="7.5" fill="#facc15" filter="url(#glow-gold)"/>
      <text x="0" y="-76" fill="#facc15" font-size="11" font-weight="800" text-anchor="middle" font-family="'Segoe UI',sans-serif">e&#x207B; transferido</text>

      <circle cx="-105" cy="0" r="46" fill="url(#sphere-sodium)" filter="url(#shadow-soft)"/>
      <text x="-105" y="8" fill="#ffffff" font-size="24" font-weight="900" text-anchor="middle" font-family="'Segoe UI',sans-serif">Na&#x207A;</text>
      <circle cx="105" cy="0" r="66" fill="url(#sphere-chlorine)" filter="url(#shadow-soft)"/>
      <text x="105" y="10" fill="#ffffff" font-size="28" font-weight="900" text-anchor="middle" font-family="'Segoe UI',sans-serif">Cl&#x207B;</text>
      <g filter="url(#glow-gold)">
        <circle cx="105" cy="-56" r="4.5" fill="#facc15"/>
        <circle cx="116" cy="-54" r="4.5" fill="#facc15"/>
        <circle cx="160" cy="-5" r="4.5" fill="#facc15"/>
        <circle cx="160" cy="8" r="4.5" fill="#facc15"/>
        <circle cx="105" cy="56" r="4.5" fill="#facc15"/>
        <circle cx="116" cy="54" r="4.5" fill="#facc15"/>
        <circle cx="50" cy="-5" r="4.5" fill="#facc15"/>
        <circle cx="50" cy="8" r="4.5" fill="#facc15"/>
      </g>
    </g>
    <g transform="translate(18, 395)">
      <rect width="418" height="74" rx="10" fill="#090d16" stroke="#1e293b" stroke-width="1.2"/>
      <text x="14" y="24" fill="#f87171" font-size="12" font-weight="800" font-family="'Segoe UI',sans-serif">Regla del Iónico:</text>
      <text x="14" y="44" fill="#cbd5e1" font-size="11" font-family="'Segoe UI',sans-serif">• Los iones se mantienen unidos por fuerzas electrostáticas (Coulomb).</text>
      <text x="14" y="62" fill="#cbd5e1" font-size="11" font-family="'Segoe UI',sans-serif">• En agua se disocian &#x2794; Iones libres que SÍ conducen electricidad.</text>
    </g>
  </g>
</svg>"""

with open(os.path.join(DIAGRAMS_DIR, "enlaces_quimicos.svg"), "w", encoding="utf-8") as f:
    f.write(enlaces_svg)
print("Updated enlaces_quimicos.svg")

# 5. Modelo Atómico de Bohr (Sodio Na Z=11)
bohr_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 620" width="100%" height="100%">
  <defs>
    <filter id="glow-gold" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="5" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <filter id="glow-cyan" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <filter id="shadow-deep" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="12" stdDeviation="12" flood-color="#000000" flood-opacity="0.7"/>
    </filter>
    <radialGradient id="grad-proton" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#ff8585" />
      <stop offset="40%" stop-color="#ef4444" />
      <stop offset="85%" stop-color="#991b1b" />
      <stop offset="100%" stop-color="#450a0a" />
    </radialGradient>
    <radialGradient id="grad-neutron" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#f1f5f9" />
      <stop offset="40%" stop-color="#94a3b8" />
      <stop offset="85%" stop-color="#475569" />
      <stop offset="100%" stop-color="#1e293b" />
    </radialGradient>
    <radialGradient id="grad-electron" cx="30%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="35%" stop-color="#38bdf8" />
      <stop offset="80%" stop-color="#0284c7" />
      <stop offset="100%" stop-color="#0369a1" />
    </radialGradient>
    <radialGradient id="grad-valence" cx="30%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="30%" stop-color="#fde047" />
      <stop offset="75%" stop-color="#eab308" />
      <stop offset="100%" stop-color="#854d0e" />
    </radialGradient>
  </defs>

  <rect width="1000" height="620" fill="#070b14" />
  <g transform="translate(30, 24)">
    <rect width="940" height="60" rx="14" fill="#0f172a" stroke="#334155" stroke-width="1.2" filter="url(#shadow-deep)"/>
    <text x="35" y="38" fill="#38bdf8" font-size="20" font-weight="900" text-anchor="middle" font-family="'Segoe UI',sans-serif">&#x269B;</text>
    <text x="65" y="32" fill="#f8fafc" font-size="17" font-weight="800" font-family="'Segoe UI',sans-serif">MODELO ATÓMICO DE BOHR: SODIO (Na, Z = 11, A = 23)</text>
    <text x="65" y="49" fill="#94a3b8" font-size="12" font-family="'Segoe UI',sans-serif">Estructura nuclear (protones y neutrones) y capas cuánticas de energía (K, L, M) con electrón de valencia</text>
  </g>

  <g transform="translate(420, 335)">
    <ellipse cx="0" cy="0" rx="280" ry="175" fill="none" stroke="#475569" stroke-width="1.6" stroke-dasharray="6 4" opacity="0.6"/>
    <ellipse cx="0" cy="0" rx="195" ry="120" fill="none" stroke="#38bdf8" stroke-width="1.8" opacity="0.75"/>
    <ellipse cx="0" cy="0" rx="115" ry="70" fill="none" stroke="#818cf8" stroke-width="1.8" opacity="0.85"/>

    <g filter="url(#shadow-deep)">
      <circle cx="-16" cy="-14" r="14" fill="url(#grad-neutron)" />
      <circle cx="18" cy="-12" r="14" fill="url(#grad-neutron)" />
      <circle cx="-12" cy="16" r="14" fill="url(#grad-neutron)" />
      <circle cx="15" cy="14" r="14" fill="url(#grad-neutron)" />
      <circle cx="-20" cy="2" r="15" fill="url(#grad-proton)" /><text x="-20" y="7" fill="#fff" font-size="15" font-weight="900" text-anchor="middle">+</text>
      <circle cx="2" cy="-8" r="15" fill="url(#grad-proton)" /><text x="2" y="-3" fill="#fff" font-size="15" font-weight="900" text-anchor="middle">+</text>
      <circle cx="22" cy="4" r="15" fill="url(#grad-proton)" /><text x="22" y="9" fill="#fff" font-size="15" font-weight="900" text-anchor="middle">+</text>
    </g>

    <!-- K layer e- -->
    <g filter="url(#glow-cyan)">
      <circle cx="-115" cy="0" r="7" fill="url(#grad-electron)" />
      <circle cx="115" cy="0" r="7" fill="url(#grad-electron)" />
    </g>
    <!-- L layer e- -->
    <g filter="url(#glow-cyan)">
      <circle cx="0" cy="-120" r="7" fill="url(#grad-electron)" />
      <circle cx="0" cy="120" r="7" fill="url(#grad-electron)" />
      <circle cx="-195" cy="0" r="7" fill="url(#grad-electron)" />
      <circle cx="195" cy="0" r="7" fill="url(#grad-electron)" />
    </g>
    <!-- M layer (Valencia) -->
    <g filter="url(#glow-gold)">
      <circle cx="215" cy="-112" r="16" fill="none" stroke="#facc15" stroke-width="1.8" opacity="0.6"/>
      <circle cx="215" cy="-112" r="9.5" fill="url(#grad-valence)" />
      <text x="215" y="-108" fill="#713f12" font-size="11" font-weight="900" text-anchor="middle">-</text>
    </g>
    <path d="M 230 -118 L 290 -160 L 370 -160" fill="none" stroke="#facc15" stroke-width="2" />
    <rect x="370" y="-185" width="165" height="50" rx="8" fill="#1e1b4b" stroke="#eab308" stroke-width="1.5" filter="url(#shadow-deep)"/>
    <text x="382" y="-167" fill="#fef08a" font-size="11.5" font-weight="900" font-family="'Segoe UI',sans-serif">&#x26A1; Electrón de Valencia</text>
    <text x="382" y="-149" fill="#fef9c3" font-size="10" font-family="'Segoe UI',sans-serif">Capa 3 (M): Cede este e&#x207B;</text>
    <text x="382" y="-137" fill="#facc15" font-size="10" font-weight="700" font-family="'Segoe UI',sans-serif">para formar Na&#x207A; (octeto)</text>
  </g>

  <!-- PANEL DERECHO -->
  <g transform="translate(740, 105)">
    <rect width="230" height="150" rx="14" fill="#0f172a" stroke="#334155" stroke-width="1.4" filter="url(#shadow-deep)"/>
    <rect x="0" y="0" width="230" height="34" rx="14" fill="#1e293b" />
    <text x="16" y="23" fill="#38bdf8" font-size="12.5" font-weight="800" font-family="'Segoe UI',sans-serif">Distribución Cuántica</text>
    <text x="16" y="58" fill="#94a3b8" font-size="11" font-family="'Segoe UI',sans-serif">Configuración completa:</text>
    <text x="16" y="76" fill="#f8fafc" font-size="12.5" font-weight="800" font-family="'Segoe UI',sans-serif">1s² 2s² 2p⁶ <tspan fill="#facc15">3s¹</tspan></text>
    <text x="16" y="108" fill="#94a3b8" font-size="11" font-family="'Segoe UI',sans-serif">Capas de Bohr:</text>
    <text x="16" y="126" fill="#38bdf8" font-size="12" font-weight="700" font-family="'Segoe UI',sans-serif">K: 2 e⁻ | L: 8 e⁻</text>
    <text x="16" y="142" fill="#facc15" font-size="12" font-weight="800" font-family="'Segoe UI',sans-serif">M: 1 e⁻ (Valencia)</text>
  </g>
  <g transform="translate(740, 275)">
    <rect width="230" height="195" rx="14" fill="#0f172a" stroke="#334155" stroke-width="1.4" filter="url(#shadow-deep)"/>
    <rect x="0" y="0" width="230" height="34" rx="14" fill="#1e293b" />
    <text x="16" y="23" fill="#34d399" font-size="12.5" font-weight="800" font-family="'Segoe UI',sans-serif">Propiedades Clave</text>
    <text x="16" y="56" fill="#94a3b8" font-size="11" font-family="'Segoe UI',sans-serif">Familia:</text>
    <text x="16" y="73" fill="#f8fafc" font-size="11.5" font-weight="700" font-family="'Segoe UI',sans-serif">Metales Alcalinos (Grupo 1)</text>
    <text x="16" y="96" fill="#94a3b8" font-size="11" font-family="'Segoe UI',sans-serif">Comportamiento:</text>
    <text x="16" y="113" fill="#fca5a5" font-size="11.5" font-weight="700" font-family="'Segoe UI',sans-serif">Alta reactividad química</text>
    <text x="16" y="136" fill="#94a3b8" font-size="11" font-family="'Segoe UI',sans-serif">Energía de ionización:</text>
    <text x="16" y="153" fill="#fef08a" font-size="11.5" font-weight="700" font-family="'Segoe UI',sans-serif">Baja (cede e⁻ fácilmente)</text>
  </g>
</svg>"""

with open(os.path.join(DIAGRAMS_DIR, "estructura_atomica_bohr.svg"), "w", encoding="utf-8") as f:
    f.write(bohr_svg)
print("Updated estructura_atomica_bohr.svg")
