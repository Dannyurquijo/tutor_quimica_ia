import os

DIAGRAMS_DIR = os.path.join(os.path.dirname(__file__), "static", "diagrams")
os.makedirs(DIAGRAMS_DIR, exist_ok=True)

bohr_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="100%" height="100%" style="background:#0f172a; font-family:'Segoe UI',system-ui,sans-serif;">
  <defs>
    <radialGradient id="nucGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ef4444"/>
      <stop offset="100%" stop-color="#991b1b"/>
    </radialGradient>
    <radialGradient id="elecGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#0284c7"/>
    </radialGradient>
  </defs>

  <rect x="20" y="15" width="760" height="50" rx="10" fill="#1e293b" stroke="#334155"/>
  <text x="40" y="47" fill="#38bdf8" font-size="20" font-weight="bold">Modelo Atómico de Bohr — Átomo de Sodio (Na, Z=11)</text>
  <text x="680" y="47" fill="#94a3b8" font-size="13" font-weight="600">Config: 2, 8, 1</text>

  <circle cx="380" cy="270" r="180" fill="none" stroke="#475569" stroke-width="1.5" stroke-dasharray="6 4"/>
  <text x="380" y="82" fill="#64748b" font-size="12" text-anchor="middle" font-weight="bold">Capa M (n=3) — 1 electron de valencia</text>

  <circle cx="380" cy="270" r="125" fill="none" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4 3"/>
  <text x="380" y="137" fill="#64748b" font-size="12" text-anchor="middle" font-weight="bold">Capa L (n=2) — 8 electrones</text>

  <circle cx="380" cy="270" r="70" fill="none" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="380" y="193" fill="#64748b" font-size="12" text-anchor="middle" font-weight="bold">Capa K (n=1) — 2 electrones</text>

  <circle cx="380" cy="270" r="38" fill="url(#nucGrad)" stroke="#fca5a5" stroke-width="2"/>
  <text x="380" y="266" fill="#ffffff" font-size="14" font-weight="bold" text-anchor="middle">11 p+</text>
  <text x="380" y="286" fill="#fef08a" font-size="12" font-weight="bold" text-anchor="middle">12 n0</text>

  <circle cx="380" cy="200" r="7" fill="url(#elecGrad)"/>
  <circle cx="380" cy="340" r="7" fill="url(#elecGrad)"/>

  <circle cx="505" cy="270" r="7" fill="url(#elecGrad)"/>
  <circle cx="255" cy="270" r="7" fill="url(#elecGrad)"/>
  <circle cx="468" cy="358" r="7" fill="url(#elecGrad)"/>
  <circle cx="292" cy="182" r="7" fill="url(#elecGrad)"/>
  <circle cx="468" cy="182" r="7" fill="url(#elecGrad)"/>
  <circle cx="292" cy="358" r="7" fill="url(#elecGrad)"/>
  <circle cx="380" cy="145" r="7" fill="url(#elecGrad)"/>
  <circle cx="380" cy="395" r="7" fill="url(#elecGrad)"/>

  <circle cx="560" cy="270" r="9" fill="#facc15" stroke="#ffffff" stroke-width="2"/>
  <line x1="560" y1="270" x2="630" y2="230" stroke="#facc15" stroke-width="2"/>
  <rect x="630" y="205" width="145" height="48" rx="8" fill="#1e293b" stroke="#facc15" stroke-width="1.5"/>
  <text x="640" y="225" fill="#facc15" font-size="12" font-weight="bold">e- de Valencia</text>
  <text x="640" y="243" fill="#cbd5e1" font-size="10">Determina reactividad</text>

  <rect x="30" y="430" width="740" height="55" rx="10" fill="#1e293b" stroke="#334155"/>
  <circle cx="55" cy="457" r="7" fill="#ef4444"/>
  <text x="70" y="461" fill="#fca5a5" font-size="12" font-weight="bold">Protones (p+): Carga positiva (+1)</text>
  <circle cx="290" cy="457" r="7" fill="#94a3b8"/>
  <text x="305" y="461" fill="#cbd5e1" font-size="12" font-weight="bold">Neutrones (n0): Sin carga electrica</text>
  <circle cx="530" cy="457" r="7" fill="#38bdf8"/>
  <text x="545" y="461" fill="#7dd3fc" font-size="12" font-weight="bold">Electrones (e-): Carga negativa (-1)</text>
</svg>"""

enlaces_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="100%" height="100%" style="background:#0f172a; font-family:'Segoe UI',sans-serif;">
  <rect x="20" y="15" width="760" height="50" rx="10" fill="#1e293b" stroke="#334155"/>
  <text x="40" y="47" fill="#38bdf8" font-size="20" font-weight="bold">Comparacion: Enlace Covalente vs. Enlace Ionico</text>

  <rect x="30" y="80" width="355" height="340" rx="14" fill="#1e293b" stroke="#3b82f6" stroke-width="2"/>
  <text x="50" y="112" fill="#60a5fa" font-size="16" font-weight="bold">1. Enlace Covalente (H2O)</text>
  <text x="50" y="132" fill="#94a3b8" font-size="12">COMPARTICION mutua de pares de electrones</text>

  <circle cx="160" cy="250" r="55" fill="#1e3a8a" stroke="#60a5fa" stroke-width="2"/>
  <text x="160" y="258" fill="#ffffff" font-size="22" font-weight="bold" text-anchor="middle">O</text>

  <circle cx="280" cy="190" r="35" fill="#065f46" stroke="#34d399" stroke-width="2"/>
  <text x="280" y="198" fill="#ffffff" font-size="16" font-weight="bold" text-anchor="middle">H</text>

  <circle cx="280" cy="310" r="35" fill="#065f46" stroke="#34d399" stroke-width="2"/>
  <text x="280" y="318" fill="#ffffff" font-size="16" font-weight="bold" text-anchor="middle">H</text>

  <circle cx="218" cy="210" r="6" fill="#facc15"/>
  <circle cx="232" cy="220" r="6" fill="#facc15"/>
  <circle cx="218" cy="290" r="6" fill="#facc15"/>
  <circle cx="232" cy="280" r="6" fill="#facc15"/>

  <rect x="50" y="360" width="315" height="42" rx="8" fill="#0f172a"/>
  <text x="60" y="385" fill="#facc15" font-size="12" font-weight="bold">No metal + No metal (H2O, CH4, O2)</text>

  <rect x="415" y="80" width="355" height="340" rx="14" fill="#1e293b" stroke="#ef4444" stroke-width="2"/>
  <text x="435" y="112" fill="#f87171" font-size="16" font-weight="bold">2. Enlace Ionico (NaCl)</text>
  <text x="435" y="132" fill="#94a3b8" font-size="12">TRANSFERENCIA de electron (Atraccion electrostatica)</text>

  <circle cx="510" cy="250" r="42" fill="#7f1d1d" stroke="#ef4444" stroke-width="2"/>
  <text x="510" y="253" fill="#ffffff" font-size="18" font-weight="bold" text-anchor="middle">Na+</text>
  <text x="510" y="272" fill="#fca5a5" font-size="11" font-weight="bold" text-anchor="middle">Cation (Perdio 1 e-)</text>

  <path d="M 555 240 Q 600 200 645 240" fill="none" stroke="#facc15" stroke-width="3" stroke-dasharray="6 3"/>
  <circle cx="600" cy="215" r="6" fill="#facc15"/>
  <text x="600" y="195" fill="#facc15" font-size="11" font-weight="bold" text-anchor="middle">e- transferido</text>

  <circle cx="690" cy="250" r="58" fill="#14532d" stroke="#22c55e" stroke-width="2"/>
  <text x="690" y="253" fill="#ffffff" font-size="20" font-weight="bold" text-anchor="middle">Cl-</text>
  <text x="690" y="275" fill="#86efac" font-size="11" font-weight="bold" text-anchor="middle">Anion (Gano 1 e-)</text>

  <rect x="435" y="360" width="315" height="42" rx="8" fill="#0f172a"/>
  <text x="445" y="385" fill="#f87171" font-size="12" font-weight="bold">Metal + No metal (NaCl, CaO, KBr)</text>

  <rect x="30" y="435" width="740" height="45" rx="8" fill="#1e293b" stroke="#334155"/>
  <text x="400" y="462" fill="#e2e8f0" font-size="12" font-weight="bold" text-anchor="middle">Regla de Oro: Enlace covalente = compartir electrones. Enlace ionico = cargas opuestas atraidas.</text>
</svg>"""

reaccion_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="100%" height="100%" style="background:#0f172a; font-family:'Segoe UI',sans-serif;">
  <rect x="20" y="15" width="760" height="50" rx="10" fill="#1e293b" stroke="#334155"/>
  <text x="40" y="47" fill="#38bdf8" font-size="20" font-weight="bold">Ley de Conservacion de la Materia: 2 H2 + O2 -&gt; 2 H2O</text>

  <rect x="100" y="80" width="600" height="70" rx="12" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
  <text x="400" y="125" fill="#f8fafc" font-size="28" font-weight="bold" text-anchor="middle">2 H2 + 1 O2   --&gt;   2 H2O</text>

  <rect x="30" y="170" width="330" height="230" rx="12" fill="#1e293b" stroke="#475569"/>
  <text x="195" y="200" fill="#93c5fd" font-size="16" font-weight="bold" text-anchor="middle">REACTIVOS (Entrada)</text>
  
  <circle cx="90" cy="270" r="18" fill="#38bdf8"/>
  <circle cx="120" cy="270" r="18" fill="#38bdf8"/>
  <text x="105" y="275" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">H-H</text>

  <circle cx="90" cy="330" r="18" fill="#38bdf8"/>
  <circle cx="120" cy="330" r="18" fill="#38bdf8"/>
  <text x="105" y="335" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">H-H</text>
  <text x="105" y="375" fill="#38bdf8" font-size="13" font-weight="bold" text-anchor="middle">2 H2 (4 atomos H)</text>

  <text x="180" y="300" fill="#cbd5e1" font-size="24" font-weight="bold">+</text>

  <circle cx="250" cy="290" r="26" fill="#ef4444"/>
  <circle cx="295" cy="290" r="26" fill="#ef4444"/>
  <text x="272" y="296" fill="#ffffff" font-size="14" font-weight="bold" text-anchor="middle">O=O</text>
  <text x="272" y="355" fill="#ef4444" font-size="13" font-weight="bold" text-anchor="middle">1 O2 (2 atomos O)</text>

  <g transform="translate(375, 260)">
    <line x1="0" y1="20" x2="40" y2="20" stroke="#f59e0b" stroke-width="4"/>
    <polygon points="50,20 35,12 35,28" fill="#f59e0b"/>
    <text x="25" y="8" fill="#f59e0b" font-size="11" font-weight="bold" text-anchor="middle">Reaccion</text>
  </g>

  <rect x="440" y="170" width="330" height="230" rx="12" fill="#1e293b" stroke="#475569"/>
  <text x="605" y="200" fill="#86efac" font-size="16" font-weight="bold" text-anchor="middle">PRODUCTOS (Salida)</text>

  <circle cx="560" cy="270" r="26" fill="#ef4444"/>
  <text x="560" y="276" fill="#ffffff" font-size="14" font-weight="bold" text-anchor="middle">O</text>
  <circle cx="535" cy="245" r="16" fill="#38bdf8"/>
  <text x="535" y="250" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">H</text>
  <circle cx="585" cy="245" r="16" fill="#38bdf8"/>
  <text x="585" y="250" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">H</text>

  <circle cx="670" cy="310" r="26" fill="#ef4444"/>
  <text x="670" y="316" fill="#ffffff" font-size="14" font-weight="bold" text-anchor="middle">O</text>
  <circle cx="645" cy="285" r="16" fill="#38bdf8"/>
  <text x="645" y="290" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">H</text>
  <circle cx="695" cy="285" r="16" fill="#38bdf8"/>
  <text x="695" y="290" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">H</text>

  <text x="605" y="375" fill="#4ade80" font-size="13" font-weight="bold" text-anchor="middle">2 H2O (4 atomos H + 2 atomos O)</text>

  <rect x="30" y="420" width="740" height="60" rx="10" fill="#1e293b" stroke="#334155"/>
  <text x="50" y="445" fill="#f59e0b" font-size="13" font-weight="bold">Balance Atomico Total:</text>
  <text x="50" y="465" fill="#cbd5e1" font-size="12">Entran 4 atomos de H y 2 atomos de O = Salen 4 atomos de H y 2 atomos de O. La materia no se crea ni se destruye.</text>
</svg>"""

escala_ph_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="100%" height="100%" style="background:#0f172a; font-family:'Segoe UI',sans-serif;">
  <defs>
    <linearGradient id="phGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ef4444"/>
      <stop offset="25%" stop-color="#f97316"/>
      <stop offset="45%" stop-color="#eab308"/>
      <stop offset="50%" stop-color="#22c55e"/>
      <stop offset="70%" stop-color="#06b6d4"/>
      <stop offset="85%" stop-color="#3b82f6"/>
      <stop offset="100%" stop-color="#8b5cf6"/>
    </linearGradient>
  </defs>

  <rect x="20" y="15" width="760" height="50" rx="10" fill="#1e293b" stroke="#334155"/>
  <text x="40" y="47" fill="#38bdf8" font-size="20" font-weight="bold">Escala de pH: Acidez, Neutralidad y Alcalinidad (0 - 14)</text>

  <rect x="40" y="90" width="720" height="40" rx="8" fill="url(#phGradient)" stroke="#ffffff" stroke-width="2"/>

  <text x="50" y="150" fill="#ef4444" font-size="15" font-weight="bold" text-anchor="middle">0</text>
  <text x="101" y="150" fill="#f87171" font-size="15" font-weight="bold" text-anchor="middle">1</text>
  <text x="152" y="150" fill="#fb923c" font-size="15" font-weight="bold" text-anchor="middle">2</text>
  <text x="204" y="150" fill="#fbbf24" font-size="15" font-weight="bold" text-anchor="middle">3</text>
  <text x="255" y="150" fill="#fde047" font-size="15" font-weight="bold" text-anchor="middle">4</text>
  <text x="307" y="150" fill="#bef264" font-size="15" font-weight="bold" text-anchor="middle">5</text>
  <text x="358" y="150" fill="#86efac" font-size="15" font-weight="bold" text-anchor="middle">6</text>
  <text x="400" y="155" fill="#22c55e" font-size="20" font-weight="bold" text-anchor="middle">7</text>
  <text x="442" y="150" fill="#67e8f9" font-size="15" font-weight="bold" text-anchor="middle">8</text>
  <text x="493" y="150" fill="#38bdf8" font-size="15" font-weight="bold" text-anchor="middle">9</text>
  <text x="545" y="150" fill="#60a5fa" font-size="15" font-weight="bold" text-anchor="middle">10</text>
  <text x="596" y="150" fill="#818cf8" font-size="15" font-weight="bold" text-anchor="middle">11</text>
  <text x="648" y="150" fill="#a78bfa" font-size="15" font-weight="bold" text-anchor="middle">12</text>
  <text x="699" y="150" fill="#c084fc" font-size="15" font-weight="bold" text-anchor="middle">13</text>
  <text x="750" y="150" fill="#e879f9" font-size="15" font-weight="bold" text-anchor="middle">14</text>

  <rect x="40" y="180" width="225" height="190" rx="10" fill="#1e293b" stroke="#ef4444" stroke-width="1.5"/>
  <text x="60" y="210" fill="#f87171" font-size="16" font-weight="bold">ACIDOS (pH &lt; 7)</text>
  <text x="60" y="235" fill="#fca5a5" font-size="12" font-weight="600">Alta concentracion de [H+]</text>
  <text x="60" y="270" fill="#cbd5e1" font-size="12">pH 0: Acido sulfurico bateria</text>
  <text x="60" y="295" fill="#cbd5e1" font-size="12">pH 1-2: Jugos gastricos / HCl</text>
  <text x="60" y="320" fill="#cbd5e1" font-size="12">pH 2.5: Limon y vinagre</text>
  <text x="60" y="345" fill="#cbd5e1" font-size="12">pH 5.0: Cafe negro</text>

  <rect x="285" y="180" width="230" height="190" rx="10" fill="#1e293b" stroke="#22c55e" stroke-width="2"/>
  <text x="310" y="210" fill="#4ade80" font-size="16" font-weight="bold">NEUTRO (pH = 7)</text>
  <text x="310" y="235" fill="#86efac" font-size="12" font-weight="600">[H+] = [OH-] en equilibrio</text>
  <text x="310" y="270" fill="#cbd5e1" font-size="12">pH 7.0: Agua pura destilada</text>
  <text x="310" y="295" fill="#cbd5e1" font-size="12">pH 7.4: Sangre humana sana</text>
  <text x="310" y="330" fill="#facc15" font-size="12" font-weight="bold">Equilibrio vital celular</text>

  <rect x="535" y="180" width="225" height="190" rx="10" fill="#1e293b" stroke="#8b5cf6" stroke-width="1.5"/>
  <text x="555" y="210" fill="#c084fc" font-size="16" font-weight="bold">BASES (pH &gt; 7)</text>
  <text x="555" y="235" fill="#d8b4fe" font-size="12" font-weight="600">Alta concentracion de [OH-]</text>
  <text x="555" y="270" fill="#cbd5e1" font-size="12">pH 8.5: Bicarbonato de sodio</text>
  <text x="555" y="295" fill="#cbd5e1" font-size="12">pH 10.0: Jabon y antiacidos</text>
  <text x="555" y="320" fill="#cbd5e1" font-size="12">pH 12.0: Cloro y blanqueador</text>
  <text x="555" y="345" fill="#cbd5e1" font-size="12">pH 14.0: Sosa caustica (NaOH)</text>

  <rect x="40" y="390" width="720" height="75" rx="10" fill="#1e293b" stroke="#334155"/>
  <text x="400" y="420" fill="#38bdf8" font-size="16" font-weight="bold" text-anchor="middle">Formula: pH = -log10 [H+]   |   pOH = -log10 [OH-]   |   pH + pOH = 14</text>
  <text x="400" y="445" fill="#94a3b8" font-size="12" text-anchor="middle">Cada unidad de cambio en la escala de pH representa una variacion de 10 VECES en la concentracion de protones.</text>
</svg>"""

estequiometria_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="100%" height="100%" style="background:#0f172a; font-family:'Segoe UI',sans-serif;">
  <rect x="20" y="15" width="760" height="50" rx="10" fill="#1e293b" stroke="#334155"/>
  <text x="40" y="47" fill="#38bdf8" font-size="20" font-weight="bold">Mapa de Conversiones Estequiometricas: El Mol como Puente</text>

  <circle cx="400" cy="240" r="70" fill="#0284c7" stroke="#38bdf8" stroke-width="3"/>
  <text x="400" y="235" fill="#ffffff" font-size="22" font-weight="bold" text-anchor="middle">MOLES</text>
  <text x="400" y="258" fill="#e0f2fe" font-size="14" font-weight="600" text-anchor="middle">(n = m / MM)</text>

  <rect x="50" y="195" width="180" height="90" rx="12" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
  <text x="140" y="235" fill="#f59e0b" font-size="16" font-weight="bold" text-anchor="middle">Masa (m)</text>
  <text x="140" y="260" fill="#fde68a" font-size="12" text-anchor="middle">Gramos (g)</text>

  <line x1="230" y1="230" x2="330" y2="230" stroke="#f59e0b" stroke-width="2.5"/>
  <text x="280" y="220" fill="#f59e0b" font-size="10" font-weight="bold" text-anchor="middle">/ Masa Molar</text>
  <line x1="330" y1="250" x2="230" y2="250" stroke="#f59e0b" stroke-width="2.5"/>
  <text x="280" y="265" fill="#f59e0b" font-size="10" font-weight="bold" text-anchor="middle">* Masa Molar</text>

  <rect x="570" y="195" width="180" height="90" rx="12" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
  <text x="660" y="230" fill="#34d399" font-size="16" font-weight="bold" text-anchor="middle">Particulas</text>
  <text x="660" y="250" fill="#a7f3d0" font-size="11" text-anchor="middle">Atomos o Moleculas</text>
  <text x="660" y="270" fill="#6ee7b7" font-size="10" font-weight="bold" text-anchor="middle">N = n * N_A</text>

  <line x1="470" y1="230" x2="570" y2="230" stroke="#34d399" stroke-width="2.5"/>
  <text x="520" y="220" fill="#34d399" font-size="10" font-weight="bold" text-anchor="middle">* 6.022 x 10^23</text>
  <line x1="570" y1="250" x2="470" y2="250" stroke="#34d399" stroke-width="2.5"/>
  <text x="520" y="265" fill="#34d399" font-size="10" font-weight="bold" text-anchor="middle">/ 6.022 x 10^23</text>

  <rect x="300" y="360" width="200" height="75" rx="12" fill="#1e293b" stroke="#a855f7" stroke-width="2"/>
  <text x="400" y="390" fill="#c084fc" font-size="15" font-weight="bold" text-anchor="middle">Volumen de Gas (C.N.)</text>
  <text x="400" y="415" fill="#e9d5ff" font-size="12" font-weight="bold" text-anchor="middle">1 mol = 22.4 Litros</text>

  <line x1="400" y1="310" x2="400" y2="360" stroke="#a855f7" stroke-width="2"/>

  <rect x="40" y="445" width="720" height="42" rx="8" fill="#1e293b" stroke="#334155"/>
  <text x="400" y="471" fill="#f8fafc" font-size="12" text-anchor="middle">Constante de Avogadro: 1 mol = 6.022 x 10^23 particulas (atomos o moleculas exactas)</text>
</svg>"""

tabla_periodica_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="100%" height="100%" style="background:#0f172a; font-family:'Segoe UI',sans-serif;">
  <rect x="20" y="15" width="760" height="50" rx="10" fill="#1e293b" stroke="#334155"/>
  <text x="40" y="47" fill="#38bdf8" font-size="20" font-weight="bold">Organizacion de la Tabla Periodica y Propiedades</text>

  <rect x="40" y="100" width="100" height="230" rx="8" fill="#991b1b" stroke="#ef4444" stroke-width="1.5"/>
  <text x="90" y="130" fill="#fca5a5" font-size="13" font-weight="bold" text-anchor="middle">Grupo 1 (IA)</text>
  <text x="90" y="155" fill="#ffffff" font-size="11" text-anchor="middle">Alcalinos</text>
  <text x="90" y="195" fill="#fca5a5" font-size="14" font-weight="bold" text-anchor="middle">Li, Na, K...</text>
  <text x="90" y="240" fill="#fecaca" font-size="10" text-anchor="middle">Valencia: +1</text>
  <text x="90" y="270" fill="#fecaca" font-size="10" text-anchor="middle">Muy reactivos</text>

  <rect x="160" y="140" width="310" height="190" rx="8" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="315" y="170" fill="#93c5fd" font-size="14" font-weight="bold" text-anchor="middle">Metales de Transicion (Bloque d)</text>
  <text x="315" y="205" fill="#ffffff" font-size="13" text-anchor="middle">Fe, Cu, Zn, Ag, Au...</text>
  <text x="315" y="240" fill="#bfdbfe" font-size="11" text-anchor="middle">Varios estados de oxidacion</text>
  <text x="315" y="270" fill="#bfdbfe" font-size="11" text-anchor="middle">Conductores de calor y electricidad</text>

  <rect x="490" y="100" width="130" height="230" rx="8" fill="#065f46" stroke="#10b981" stroke-width="1.5"/>
  <text x="555" y="130" fill="#6ee7b7" font-size="13" font-weight="bold" text-anchor="middle">No Metales</text>
  <text x="555" y="155" fill="#ffffff" font-size="11" text-anchor="middle">C, N, O, P, S, Cl</text>
  <text x="555" y="195" fill="#a7f3d0" font-size="11" text-anchor="middle">Halogenos: F, Cl, Br</text>
  <text x="555" y="240" fill="#a7f3d0" font-size="10" text-anchor="middle">Alta electronegatividad</text>
  <text x="555" y="270" fill="#a7f3d0" font-size="10" text-anchor="middle">Ganan electrones</text>

  <rect x="640" y="100" width="110" height="230" rx="8" fill="#5b21b6" stroke="#8b5cf6" stroke-width="1.5"/>
  <text x="695" y="130" fill="#c084fc" font-size="13" font-weight="bold" text-anchor="middle">Grupo 18 (VIII)</text>
  <text x="695" y="155" fill="#ffffff" font-size="11" text-anchor="middle">Gases Nobles</text>
  <text x="695" y="195" fill="#e9d5ff" font-size="14" font-weight="bold" text-anchor="middle">He, Ne, Ar, Kr</text>
  <text x="695" y="240" fill="#f3e8ff" font-size="10" text-anchor="middle">Octeto Completo</text>
  <text x="695" y="270" fill="#f3e8ff" font-size="10" text-anchor="middle">Inertes y estables</text>

  <rect x="40" y="355" width="710" height="40" rx="8" fill="#1e293b" stroke="#f59e0b"/>
  <text x="55" y="380" fill="#f59e0b" font-size="13" font-weight="bold">Electronegatividad:</text>
  <text x="210" y="380" fill="#cbd5e1" font-size="12">Aumenta hacia la DERECHA y hacia ARRIBA. El Fluor (F = 4.0) es el mas electronegativo.</text>

  <rect x="40" y="410" width="710" height="40" rx="8" fill="#1e293b" stroke="#06b6d4"/>
  <text x="55" y="435" fill="#06b6d4" font-size="13" font-weight="bold">Radio Atomico:</text>
  <text x="180" y="435" fill="#cbd5e1" font-size="12">Aumenta hacia la IZQUIERDA y hacia ABAJO. El Francio (Fr) tiene el mayor radio atomico.</text>
</svg>"""

diagrams = {
    "estructura_atomica_bohr.svg": bohr_svg,
    "enlaces_quimicos.svg": enlaces_svg,
    "reaccion_quimica.svg": reaccion_svg,
    "escala_ph.svg": escala_ph_svg,
    "estequiometria_mol.svg": estequiometria_svg,
    "tabla_periodica.svg": tabla_periodica_svg,
}

if __name__ == "__main__":
    for filename, content in diagrams.items():
        filepath = os.path.join(DIAGRAMS_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"Generated: {filename}")
    print("All diagrams generated successfully!")
