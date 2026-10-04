---
name: pika-generative-video-pipeline
display_name: "Pipeline de Generación y Control Parámetrico en Pika Art (A/V)"
description: "Generación de vídeo e integración de audio en Pika Art. Cheatsheet de cámara (-camera), control de física (-motion, -fps), Pikaffects y Pika Audio Models. Dispara con 'pika art', 'pika tutorial', 'pika camera', 'pikaffects', 'pika prompt'."
---

# Pika Art Generative Video & Audio Pipeline

Esta habilidad proporciona las directrices y el cheatsheet determinista para la generación cinematográfica en Pika Art (1.0, 1.5, 2.0+) y su suite de audio.

## 🎯 Criterios de Activación
- Palabras clave / Intenciones: "pika art", "pika labs", "pika tutorial", "pikaffects", "pika camera", "pika audio", "pika prompt".

---

## 🛠️ Cheatsheet de Parámetros

### 📹 Control de Cámara (`-camera`)
- **Zoom:** `-camera zoom in` / `-camera zoom out`
- **Panorámica:** `-camera pan left` / `right` / `up` / `down`
- **Rotación:** `-camera rotate cw` / `ccw`
- *Nota:* Se pueden combinar vectores de cámara (ej. `-camera pan up right zoom in`).

### ⚙️ Parámetros de Calidad y Dinámica
- `-motion 1-4`: Intensidad de movimiento (1 = sutil/cinemático, 4 = caótico/FX).
- `-fps 8-24`: Tasa de refresco (24 = fluido, 12/8 = stop-motion/anime).
- `-gs 8-24`: Adherencia al prompt (Guidance Scale, default: 12).
- `-neg "..."`: Prompt negativo.
- `-ar [ratio]`: Relación de aspecto (16:9, 9:16, 1:1, 4:5).

---

## 🎨 Fórmula de Prompting en 4 Capas

$$\text{Prompt} = \text{[Sujeto + Acción Dinámica]} + \text{[Entorno + Iluminación]} + \text{[Lente + Estilo Fílmico]} + \text{[Flags]}$$

*Ejemplo:*
`Cyberpunk female android turning her head, eyes glowing cyan, standing in neon-drenched rain street, anamorphic lens 35mm, volumetric fog, cinematic lighting -camera zoom in -motion 2 -fps 24 -gs 14 -neg "ugly, cartoon, low quality"`

---

## 💥 Deformaciones Físicas (*Pikaffects*)
1. `Melt`: Derretimiento en fluido viscoso.
2. `Inflate`: Inflado de globo previo a colapso.
3. `Squish`: Aplastamiento vertical.
4. `Crush`: Compresión multidireccional.
5. `Explode`: Desintegración en partículas.
6. `Cakeify`: Revelado interior de textura de pastel.

---

## 🎵 Pika Audio Models Suite
1. **Pika Soundtrack:** Banda sonora cinemática coordinada con el movimiento.
2. **Pika Music:** Producción de canciones completas (voz + instrumental).
3. **Pika SFX:** Efectos de sonido Foley diegéticos.
4. **Pika Speech:** Clonación de voz y doblaje.

---

## 💻 Integración con CLI Soberano Local
Usar `pika_suno_sovereign_cli.py` para auditar la sintaxis de corchetes `[...]` y calcular la fricción de créditos antes de lanzar llamadas a `dev.pika.art`:
```bash
python3 scripts/pika_suno_sovereign_cli.py --calc-cost <duración_segundos> --iterations <n>
```
