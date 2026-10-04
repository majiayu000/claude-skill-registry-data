---
name: c5-spatial-audio-architect
description: Auditoría epistemológica y refactorización termodinámica de pipelines DSP de audio. Falsación de técnicas estéreo planar y diseño de arquitecturas Ambisonics (HOA) / Binaural. Dispara con "auditoría dsp", "audio espacial", "criticar estéreo", "hoa", "binaural", "ambisonics", "spatial audio".
---

# C5-REAL Spatial Audio Architect

## 1. Falsación Topológica (Axioma #2: Mapa vs. Territorio)
Al analizar pipelines de audio (ej. scripts Python con `scipy`, `numpy`, o ruteos DAW):
- Identifica técnicas de espacialización artificial (como *Mid/Side widening*, efecto Haas, o delay estéreo) que inyectan **entropía de fase (anergía)** sin incrementar dimensiones espaciales reales.
- Diagnostica si la señal sufre un estrangulamiento al ser colapsada tempranamente a un bus de amplitud $L/R$ (un mapa 1D que descarta el territorio esférico 3D).

## 2. Cuantificación y Modelado Matemático
- Emplea modelos físicos y matemáticos rigurosos: Teorema de Nyquist Espacial, matrices de rotación de Wigner $SO(3)$, y funciones de Armónicos Esféricos $Y_l^m(\theta, \phi)$.
- Traduce las operaciones de audio a su impacto en la función de información (ej. correlación cruzada interaural IACC).

## 3. Refactorización Exergética
Propón siempre soluciones orientadas a **Object-Based Audio (OBA)** y **Higher-Order Ambisonics (HOA)**:
1. Retener las coordenadas esféricas $(\theta, \phi, r)$ de cada fuente sonora.
2. Codificar la escena acústica en coeficientes de campo (ej. HOA de 3er Orden, 16 canales).
3. Desacoplar la renderización final (ej. decodificación binaural dinámica acoplada a *head-tracking* vía filtros Woodworth/BRIR o síntesis WFS) del masterizado, asegurando la exteriorización física (anti *In-Head Localization*).
