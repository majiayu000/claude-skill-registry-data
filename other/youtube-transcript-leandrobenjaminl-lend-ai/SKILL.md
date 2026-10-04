---
name: youtube-transcript
description: >
  Extrae y procesa transcripciones de YouTube — obtiene el texto completo
  de subtítulos y genera resúmenes estructurados.
  Trigger: Cuando necesitás entender el contenido de un video de YouTube, extraer su texto, o generar un resumen estructurado.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
---

# Skill: youtube-transcript

Transcripciones de YouTube. Sacale el texto a cualquier video.

## Trigger

- Querés el texto de un video de YouTube
- Necesitás un resumen de un video largo
- Vas a usar el contenido de un video como fuente para un análisis
- Querés buscar información específica dentro de un video

## Workflow LEND

1. ANALIZAR
   ├── URL: ¿es de YouTube? ¿válida?
   ├── Video: ¿tiene subtítulos/CC? ¿en qué idioma?
   ├── Contenido: ¿es técnico, educativo, conferencia, tutorial?
   └── Destino: ¿resumen, análisis, traducción, cita textual?

2. OFRECER (Menú del Senior)
   ├── A) Transcripción completa — texto íntegro del video
   ├── B) Resumen estructurado — puntos clave, timestamps, conclusiones
   └── C) Análisis temático — extraer tópicos, citas textuales, ideas principales

3. ELEGIR → confirmación

4. HACER
   ├── Extraer: youtube-transcript-api o herramienta similar
   ├── Idioma: español o inglés, según el video
   ├── Resumen: ideas principales, ejemplos clave, conclusiones
   ├── Timestamps: referencias a minutos importantes
   └── Guardar: texto en archivo o en engram para referencia futura

5. VERIFICAR
   ├── La transcripción cubre el video completo
   ├── El resumen captura las ideas principales
   └── Los timestamps son precisos
