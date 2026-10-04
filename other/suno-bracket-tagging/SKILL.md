---
name: suno-bracket-tagging
display_name: "Protocolo de Ingeniería Acústica y Control Causal para Audio AI (Suno/Udio/YuE)"
description: "Protocolo de ingeniería acústica forense, control causal, etiquetado estructurado [...], cadena de señal física, desensamblado ontológico de artistas y rescate espectral en DAW para motores de síntesis de audio AI (Suno, Udio, YuE, DDSP). Dispara con \"suno prompt\", \"udio tags\", \"prompt musical\", \"etiquetas suno\", \"control causal audio\", \"audio ai\", \"jailbreak acustico\", \"des-plasticar audio\"."
---

# Protocolo C5: Ingeniería Acústica y Control Causal para Audio AI

Este protocolo rige la estructuración determinista de prompts, anotaciones de ingeniería de sonido, gramática de corchetes `[...]` y rescate exergético para motores de síntesis de audio neuronal (Suno AI v3.5/v4, Udio, YuE, Stable Audio).

---

## 1. Gramática Formal de Etiquetas `[...]` (Lyrics Box)

El cuadro de letra opera como la mesa de mezclas temporal del modelo:

| Categoría | Sintaxis de Control `[...]` | Ejemplos Operativos |
| :--- | :--- | :--- |
| **Estructura** | `[Section Name]` | `[Intro]`, `[Verse 1]`, `[Pre-Chorus]`, `[Chorus]`, `[False Drop]`, `[Bridge]`, `[Outro]`, `[End]` |
| **Cadena Vocal & DSP** | `[Vocal / FX Directive]` | `[Vocal: Close-Mic, Dry, Breathy Contralto]`, `[Whisper]`, `[Robotic Vocoder -12st]`, `[Monotone Baritone]` |
| **Dinámica & Transición** | `[Dynamic Directive]` | `[Stripped Down]`, `[Wall of Sound]`, `[Sudden Silence]`, `[Tape Stop Click]`, `[Bass Drop]` |
| **Atmósfera & Espacialidad**| `[SFX / Room Directive]` | `[SFX: Rain and Tape Flutter]`, `[Binaural Room Reflections]`, `[Subtle Vinyl Dust]` |
| **Métrica & Microtonalidad**| `[Metric / Tuning]` | `[BPM: 116]`, `[Key: D Minor]`, `[Balkan 7/8: 2+2+3]`, `[Tuning: 24-TET Makam]` |

---

## 2. La Fórmula Canónica del Style Box (4 Capas Físicas)

Nunca solicitar emociones abstractas (*"sad epic song"*); definir la **cadena de producción de estudio**:

```
[Subgénero Híbrido Estricto] + [Micro-Instrumentación Específica] + [Cadena de Señal / Mastering Analógico] + [Tempo & Tonalidad]
```

* **Ejemplo de Alta Exergía:**  
  `Nordic Chamber Noir, bowed upright bass, felt upright piano, intimate close-mic female breathy vocal, analog tape flutter, Neve preamp warmth, no auto-tune, EMT 140 plate reverb, BPM: 76, Key: A minor, spacious acoustic room, dry master`

---

## 3. Desensamblado Ontológico (Bypass de Artistas Protegidos)

Para eludir listas negras de artistas protegidos, descomponer su identidad en **equipamiento físico, microfonía y técnicas de sala**:

* **Daft Punk (Discovery):** `French Touch, vintage Heil Talkbox, Minimoog saw bass, SP-1200 12-bit grit, Mutron III phaser sweep, aggressively sidechained kick, vinyl crackle, BPM: 123`
* **Radiohead (In Rainbows):** `Art Rock, hollow-body Gibson ES-330 fingerpicking, Ondes Martenot sub-sine, dead room dry drums, heavy tea-towel damping, rhythmic 5/4 syncopation, intimate falsetto, EMT 140 plate`
* **Billie Eilish / Finneas:** `Dark Minimal Bedroom Pop, 38Hz pure sine 808 sub-bass, ASMR whispered vocal, stacked quintupled vocal harmonies hard-panned L/R, ultra-dry Neumann U87, dynamic silence`

---

## 4. Control Fonético Forense y Escansión Métrica

1. **Isosilabismo:** Conteo silábico regular compás a compás para evitar atropellamiento vocal (*vocal rush*).
2. **Mitigación de Sibilancias:** Evitar fricativas duras (`S`, `T`, `P`, `CH`) en notas altas que saturen cuantizadores RVQ en 6–10 kHz; priorizar nasales y líquidas (`M`, `N`, `L`, `R`).
3. **Acento Tónico para Contorno Melódico ($F_0$):** Mayúsculas y tildes fuerzan subidas tonales (e.g. `el cielo CAY-e... so-BRE el máár`).
4. **Melisma Forzado:** Usar guiones y vocales repetidas (e.g. `Gloo-o-o-ria`, `vuel-va-a-as`).

---

## 5. Inyección de Semilla de Audio y Chaining Quirúrgico

* **Anclaje Temporal y de Fase:** Subir un clip de audio de 15–30s con claqueta/swing estricto y un acorde raíz para forzar al modelo a sincronizar BPM y fase antes de extender (`Extend`).
* **Chaining de 20 Segundos:** Extender en bloques de $\le 20-30\text{s}$ cortando siempre en valles dinámicos o silencios (nunca sobre colas de reverb) para prevenir acumulación entrópica.

---

## 6. Canal DAW de Rescate Espectral (Des-plasticar el Audio)

1. **Mono-Bass Inmediato:** Side-cut lineal en EQ por debajo de $120 \text{ Hz}$ a mono estricto.
2. **Supresión de Resonancias del Vocoder:** Atenuar $2-4 \text{ dB}$ en las frecuencias estacionarias de convolución (**$3.150 \text{ Hz}$, $4.800 \text{ Hz}$ y $8.200 \text{ Hz}$**) mediante Soothe2 o DSEQ3.
3. **Transient Shaping:** Incrementar ataque (+2 a +3 dB) y reducir sustain (-1.5 dB) para restaurar transitorios aplastados por el RVQ.
4. **Resíntesis Armónica:** Saturación analógica de cinta/válvulas para rellenar vacíos espectrales.

---

## 7. Desacoplamiento de Stems y Transcripción MIDI

* **Aislamiento de Voz de Fase Coherente:** Procesar externamente con **UVR5 (modelo BS-Roformer-Viperx-1297)** con Window Size 512 y Overlap 8x/16x.
* **Sustitución Tímbrica Vocal:** Pasar la acapella limpia por **RVC v2** para reemplazar formantes plásticos por modelos de voz hiper-limpios.
* **Extracción Simbólica a MIDI:** Usar **Spotify Basic Pitch** para transcribir la armonía y reemplazar instrumentos de IA por librerías orquestales/sintetizadores virtuales profesionales en el DAW.

---

## 8. Documentación y Referencias Complementarias

* **Fundamentos Matemáticos, Físicos y Código DDSP:** Ver [`references/neural_audio_engineering_handbook.md`](./references/neural_audio_engineering_handbook.md).
* **Génesis de Subgéneros Electrónicos Avant-Garde:** Ver [`references/subgenre_genesis_protocol.md`](./references/subgenre_genesis_protocol.md).
