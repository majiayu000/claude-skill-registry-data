---
name: user-session-video-to-backlog
description: >
  Video-User-interactive-dev: método nombrado por el usuario para analizar un vídeo
  de sesión (path o adjunto), revisión completa documentada y procedimiento de
  desarrollo en un solo informe. También: sesiones MP4/MOV (iPhone, Loom, OBS),
  metadatos, JSON + Markdown en docs/team/ux-feedback. Use when the user says
  Video-User-interactive-dev, shares a session video path, or wants USER POV
  video analysis and a dev plan in Calculadora-BMC.
---

# User session video → backlog (USER + funcionalidad)

## Método canónico: **Video-User-interactive-dev**

Cuando el usuario diga explícitamente **Video-User-interactive-dev** (o “método vídeo usuario interactivo”) y dé la **ruta del vídeo** o lo **adjunte**:

1. Leer [`METHOD-VIDEO-USER-INTERACTIVE-DEV.md`](../../../docs/team/ux-feedback/METHOD-VIDEO-USER-INTERACTIVE-DEV.md).
2. Usar la plantilla [`TEMPLATE-VIDEO-USER-INTERACTIVE-DEV-REPORT.md`](../../../docs/team/ux-feedback/TEMPLATE-VIDEO-USER-INTERACTIVE-DEV-REPORT.md) como **esqueleto obligatorio** del informe único.
3. **Analizar por completo** lo evaluado en el vídeo (narración + pantalla); no afirmar lo no observable.
4. **Entregar en la misma corrida:**
   - **Un solo Markdown** que incluya **Parte A** (revisión documentada del análisis) **y Parte B** (procedimiento de desarrollo y ajustes):

`docs/team/ux-feedback/VIDEO-USER-INTERACTIVE-DEV-REPORT-YYYY-MM-DD-<slug>.md`

   - **JSON** estructurado paralelo:

`docs/team/ux-feedback/VIDEO-USER-INTERACTIVE-DEV-ANALYSIS-YYYY-MM-DD-<slug>.json`

   (Mismo esquema JSON que en “Esquema JSON” más abajo; el campo `metadata` puede incluir `"method": "Video-User-interactive-dev"`.)

5. Si el usuario **no** nombró el método pero pidió análisis de vídeo / backlog, se pueden usar los nombres legacy `USER-SESSION-VIDEO-REPORT-*` y `USER-SESSION-VIDEO-ANALYSIS-*`; si nombró **Video-User-interactive-dev**, usar **solo** los prefijos `VIDEO-USER-INTERACTIVE-DEV-*`.

## Rol del agente

Interpretar **evidencia de sesión** (vídeo y/o transcripción con marcas de tiempo, notas sobre frames, logs opcionales) y producir **artefactos ejecutables** en el repo, **sin inventar** pantallas, errores ni causas que no consten en la evidencia.

## Cuándo usar esta skill

- Invocación **Video-User-interactive-dev** + path o adjunto.
- Grabación **tablet + teléfono**, **Loom / OBS / MP4** con voz.
- Pedido de plan o backlog **desde la demo** o **desde el vídeo**.

## Relación con otras piezas del repo

| Situación | Skill / doc |
|-----------|-------------|
| Solo transcripción + capturas + URL (sin vídeo) | `navigation-user-feedback` → `USER-NAV-REPORT-*.md` |
| Vídeo + método nombrado | **Esta skill** + regla `video-user-interactive-dev.mdc` |
| Plan por equipos | `bmc-implementation-plan-reporter` (después, si aplica) |

## Entradas que el usuario debe aportar

1. **Vídeo** (MP4/MOV) y/o **transcripción con timestamps** si el chat no procesa vídeo.
2. **`metadata.json`** (opcional; plantilla abajo o carpeta `sessions/<slug>/`).
3. **URL base** de la app si es web.
4. Opcional: **rrweb**, **HAR**, capturas, **consola** / **logcat**.

### Plantilla `metadata.json` (copiar y rellenar)

```json
{
  "project": "Calculadora-BMC / Panelin",
  "app_version": "semver o git short hash",
  "env": "local | preview | production",
  "recorder": "nombre",
  "recording_device": "ej. iPhone — cámara trasera",
  "target_device": "ej. iPad — Safari",
  "date_iso": "2026-04-02T12:00:00-03:00",
  "app_surface": "web | tablet-web | native",
  "base_url": "https://… o http://localhost:5173",
  "notes": "clap de sync al inicio; sin PII en pantalla"
}
```

## Grabación tablet + teléfono (checklist breve)

- Trípode; **apaisado**; bloqueo de rotación; No molestar.
- Brillo alto en tablet; luz frontal suave; evitar reflejo.
- Android: **Opciones de desarrollador → Mostrar toques** si aplica.
- **Clap** visible y audible al inicio (sync y cortes).
- Narrar: objetivo, versión, rol, expectativa antes de cada acción, errores al ocurrir, resumen de mejoras al cerrar.
- Duración orientativa **2–15 min**; clips separados si es más largo.
- **Privacidad:** datos ficticios o blur; no tokens ni PII reales.

## Solo compartir el vídeo (iPhone → tú → Cursor)

1. **Mínimo:** adjuntar **MP4/MOV** + decir **Video-User-interactive-dev** y la ruta si no adjunta; opcional `base_url`.
2. **Recomendado (Mac):** `npm run session:video-ingest -- ~/Downloads/IMG_….MOV [base_url]` → al inicio comprueba **node** + **ffmpeg**; en macOS con Homebrew, si falta **ffmpeg** intenta **`brew install ffmpeg`**, luego copia/extrae/metadatos. Carpeta bajo `sessions/` con `CURSOR-CHAT-PROMPT.txt`.
3. **Solo comprobar deps:** `npm run session:video-deps` (check) o `npm run session:video-deps:ensure` (e intentar instalar ffmpeg en macOS/Brew).

La parte **LLM** ocurre en Cursor; no hay worker en segundo plano.

## Modo A — Multimodal en el chat (rápido)

- Adjuntar **MP4 + metadata.json** si el modelo acepta vídeo.
- Segmentos con **timestamps** (`mm:ss`), `confidence` `low|medium|high` por ítem.

## Modo B — Preprocesado local (audio + capturas espaciadas)

1. MP4 en `docs/team/ux-feedback/sessions/<fecha>-<slug>/`.
2. `npm run session:video-extract -- "…/session.mp4"` genera:
   - **`audio.wav`**: pista **completa** en 16 kHz mono (Whisper / adjunto al modelo para **entender la narración**).
   - **`frames/frame_*.jpg`**: por defecto **1 captura cada 5 s**, ancho máx. **640 px**, JPEG comprimido (`q:v` ~14) para **poco peso** y UI aún legible.
3. Variables opcionales (antes del comando):
   - `BMC_SESSION_VIDEO_FRAME_INTERVAL_SEC` (default **5**) — segundos entre capturas.
   - `BMC_SESSION_VIDEO_FRAME_MAX_WIDTH` (default **640**; **0** = sin escalar).
   - `BMC_SESSION_VIDEO_JPEG_Q` (**2–31**, default **14**; más alto = más chafa/más liviano).
4. Para **entender qué pasa** sin subir el MP4 entero: adjuntar **`audio.wav`** + una selección de **frames** (p. ej. cada 30 s o los que muestren errores) + `metadata.json`.
5. Transcribir `audio.wav` (Whisper / API) o export Loom/Descript; pegar transcript en el chat si ayuda al timeline.

## Salida obligatoria (el agente crea archivos)

### 1) JSON de análisis

**Video-User-interactive-dev (preferido si el usuario nombró el método):**

`docs/team/ux-feedback/VIDEO-USER-INTERACTIVE-DEV-ANALYSIS-YYYY-MM-DD-<slug>.json`

**Legacy (si no se usó el nombre del método):**

`docs/team/ux-feedback/USER-SESSION-VIDEO-ANALYSIS-YYYY-MM-DD-<slug>.json`

Esquema mínimo:

```json
{
  "metadata": { "method": "Video-User-interactive-dev" },
  "timeline": [
    {
      "start_sec": 0,
      "end_sec": 12.5,
      "transcript": "",
      "visual_notes": "",
      "ocr_snippets": [],
      "linked_logs": []
    }
  ],
  "bugs": [
    {
      "id": "B-001",
      "title": "",
      "severity": "P0|P1|P2|P3",
      "repro_steps_timestamped": ["00:00:05 …"],
      "evidence": [],
      "suspected_layer": "src/|server/|Sheets|deploy|unknown",
      "confidence": "low|medium|high",
      "suggestion": ""
    }
  ],
  "features": [
    {
      "id": "F-001",
      "title": "",
      "description": "",
      "acceptance_criteria": [],
      "priority": "P0|P1|P2|P3",
      "confidence": "low|medium|high"
    }
  ],
  "roadmap": [{ "order": 1, "item": "", "rationale": "" }],
  "tech_tasks": [],
  "risks": [],
  "qa_checklist": []
}
```

### 2) Informe Markdown

**Video-User-interactive-dev:** un solo archivo **Parte A + Parte B** según `TEMPLATE-VIDEO-USER-INTERACTIVE-DEV-REPORT.md`:

`docs/team/ux-feedback/VIDEO-USER-INTERACTIVE-DEV-REPORT-YYYY-MM-DD-<slug>.md`

**Legacy:** `USER-SESSION-VIDEO-REPORT-YYYY-MM-DD-<slug>.md` con secciones equivalentes si no aplica el nombre del método.

## Reglas estrictas

- **No inventar** UI, errores o causas ausentes en vídeo, transcript, OCR, logs o capturas.
- **`NEEDS_CONFIRMATION`** si reflejos, audio ilegible o ambigüedad.
- **PII:** no copiar datos sensibles; advertir en `risks`.
- Tras trabajo sustantivo: línea en `docs/team/PROJECT-STATE.md` (Cambios recientes) enlazando el informe `VIDEO-USER-INTERACTIVE-DEV-REPORT-*.md`.

## Plataforma (recomendación)

**Artefactos locales o en chat + Cursor** es el MVP. Loom/Descript como fuente de transcript.

## Referencias

- Método: [`METHOD-VIDEO-USER-INTERACTIVE-DEV.md`](../../../docs/team/ux-feedback/METHOD-VIDEO-USER-INTERACTIVE-DEV.md)
- Plantilla informe: [`TEMPLATE-VIDEO-USER-INTERACTIVE-DEV-REPORT.md`](../../../docs/team/ux-feedback/TEMPLATE-VIDEO-USER-INTERACTIVE-DEV-REPORT.md)
- Índice UX: [`README.md`](../../../docs/team/ux-feedback/README.md)
- Extracción: `npm run session:video-extract`, `npm run session:video-ingest`
- Propagación: [`PROJECT-TEAM-FULL-COVERAGE.md`](../../../docs/team/PROJECT-TEAM-FULL-COVERAGE.md)
