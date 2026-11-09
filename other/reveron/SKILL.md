---
name: reveron
description: >
  Genera imágenes, SVG, videos, GIF, audio y modelos 3D (GLB) eligiendo el mejor modelo por caso y respetando umbrales de costo.
  Usa OpenAI (gpt-image-1/2), Gemini (Nano-Banana, Imagen 4, Veo 3), FAL (FLUX, Recraft, Kling, Ideogram), KIE (gateway Sora/MJ/Kling), HeyGen (avatar + HyperFrames), ElevenLabs (TTS + SFX), Tripo3D (texto/imagen → modelo 3D GLB).
  Trigger: usuario invoca "Reverón", pide generar imagen/video/svg/gif/logo/banner/hero/thumbnail/avatar/tts/voz/audio/sfx/modelo 3D/GLB, o cuando cualquier proyecto necesita assets visuales o 3D.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "2.0"
---

## When to Use

- Usuario pide explícitamente "Reverón" o menciona el skill por nombre
- Usuario pide crear/generar/hacer una imagen, video, SVG, GIF, logo, banner, hero, thumbnail
- Usuario pide un asset visual para su proyecto (landing, RRSS, presentación, mockup)
- Usuario pide editar una imagen existente (cambiar fondo, inpaint, character swap)
- Usuario pide narración, voz, TTS, doblaje, o sound effects
- Usuario pide un video de avatar hablando (para RRHH, ventas, tutoriales)
- Usuario pide un modelo 3D, GLB, asset para juego/AR/impresión 3D, desde texto o desde una imagen de referencia
- Usuario pasa URLs de imágenes/videos para "inspirarte" o "usar como referencia"

## Global Library

**Toda generación queda guardada en la biblioteca global** (`~/.reveron/`), no solo en el proyecto local. Esto significa:

- Accedé a tus assets desde cualquier proyecto
- Usá generaciones previas como referencias en nuevas generaciones
- Consultá costo total y tendencias desde el dashboard (`reveron serve`)
- Exportá o buscá en `reveron import` desde manifestos de proyectos anteriores

Use `--refs reveron:<id>` para referenciar un asset guardado:

```bash
reveron image --provider gemini --model nano-banana \
  --prompt "misma pose pero en la playa" \
  --refs reveron:84ac4a32-5c48-4f8e-8f4c-a8f8c8f8c8f8
```

Ideal para iteración: cambios de estilo, character consistency, refinamientos sobre trabajo anterior.

## Critical Patterns

### 1. Decisión de proveedor/modelo — REGLA MAESTRA

Consultar `references/model-matrix.md` para la matriz completa. Resumen del árbol de decisión:

```
¿pidió SVG explícito?                → fal + recraft-v3-svg
¿pidió video?                         → default fal + kling-1.6-pro (calidad/precio óptimo)
                                     → con audio sincronizado: gemini + veo-3
¿pidió TTS/voz?                       → elevenlabs multilingual-v2
¿pidió avatar hablando?               → heygen avatar-video
¿pidió modelo 3D / GLB / asset 3D?    → tripo (text-to-model si es texto, image-to-model si pasó ref)
¿pasó imagen como referencia?         → gemini nano-banana (edit)
¿pidió "vector"/"logo"/"flat"?        → fal recraft-v3
¿pidió texto legible en imagen?       → fal ideogram-v3 o gpt-image-2
resto (imagen desde texto)            → fal flux-pro-ultra (default premium)
                                     → si el usuario dijo "rápido" → flux-schnell
```

### 2. Umbrales de costo — INNEGOCIABLE

| Costo estimado | Acción |
|---|---|
| `< $0.10` | Ejecuta directo |
| `$0.10 – $1.00` | Ejecuta pero AVISA el costo en tu respuesta al user |
| `> $1.00` | **PIDE CONFIRMACIÓN EXPLÍCITA** antes de correr con `--force` |

Nunca corras un video con `kling-2.1-master`, `veo-3` (no fast), o batches de 5+ imágenes premium sin confirmación explícita. Es plata real.

### 3. Análisis de referencias — obligatorio

Cuando el usuario pasa una URL como referencia:
1. Descargala mentalmente (Claude visión analiza la URL si es imagen)
2. Extraé: estilo, paleta, composición, elementos clave
3. Enriquecé el prompt con esa info textual
4. Pasá la URL al proveedor como `--refs URL1,URL2` para que TAMBIÉN la use

### 4. Nunca hardcodees valores del usuario

El skill soporta **3 fuentes de secretos** con auto-detección (ver README §Setup):
- **Infisical** — si `INFISICAL_URL`, `INFISICAL_CLIENT_ID`, `INFISICAL_CLIENT_SECRET`, `DAVINCI_PROJECT_ID` están seteadas
- **Archivo .env** — busca `$DAVINCI_ENV_FILE` → `./.da-vinci.env` → `~/.config/da-vinci/.env` → `~/.claude/skills/da-vinci/.env`
- **Env vars directas** — cualquier combinación de las 6 keys en `process.env`

Override manual: `DAVINCI_SECRETS_SOURCE=infisical|dotenv|env`

Si el usuario dice "no me funciona", primero verificá con:
```bash
node ~/.claude/skills/da-vinci/scripts/generate.mjs image \
  --provider fal --model flux-schnell --prompt "test" --dry-run --verbose
# Muestra qué fuente detectó y qué keys cargó
```

Si NO tiene ninguna fuente configurada, el error te da un setup guide con las 3 opciones.

### 5. Registrar SIEMPRE en manifest

Toda generación queda en `<cwd>/assets/generated/manifest.json`. El helper lo hace automáticamente, pero si escribís lógica custom, respetá esa convención.

## Commands

```bash
# ── Imagen ──────────────────────────────────────────────────────
# Default (flux-pro-ultra, calidad premium)
reveron image \
  --provider fal --model flux-pro-ultra \
  --prompt "..." --aspect 16:9

# Rápida y barata (flux-schnell, para iterar)
reveron image --provider fal --model flux-schnell --prompt "..."

# Con edición desde referencia (Nano-Banana)
reveron image \
  --provider gemini --model nano-banana \
  --prompt "cambiá el fondo a un bosque" \
  --refs "https://ejemplo.com/original.png"

# Texto legible en imagen
reveron image --provider fal --model ideogram-v3 \
  --prompt "poster que dice 'AgendaZap' en tipografía moderna"

# ── SVG (siempre FAL Recraft V3 SVG) ────────────────────────────
reveron svg --prompt "logo minimalista para una clínica"

# ── Video ───────────────────────────────────────────────────────
# Default (kling-1.6-pro, ~$0.42 por 5s)
reveron video --provider fal --model kling-1.6-pro \
  --prompt "café siendo servido, cinemático" --duration 5

# Con audio sincronizado (Veo 3, requiere --force por costo)
reveron video --provider gemini --model veo-3 \
  --prompt "..." --duration 5 --force

# Fast + barato (Veo 3 Fast)
reveron video --provider gemini --model veo-3-fast \
  --prompt "..." --duration 5

# ── Modelo 3D / GLB (Tripo3D) ───────────────────────────────────
# Desde texto
reveron model-3d --prompt "una espada medieval low poly" \
  --texture true --pbr true

# Desde imagen de referencia (image-to-model)
reveron model-3d --refs "https://ejemplo.com/producto.png"

# Sin textura (más barato, solo geometría)
reveron model-3d --prompt "silla moderna minimalista" --texture false

# ── Avatar hablando (HeyGen) ────────────────────────────────────
reveron list-avatars                        # ver IDs disponibles
reveron list-voices --provider heygen       # ver voices
reveron avatar-video \
  --avatar "AVATAR_ID" --voice "VOICE_ID" \
  --script "Hola, soy Reverón..."

# ── TTS + SFX (ElevenLabs) ──────────────────────────────────────
reveron list-voices --provider elevenlabs
reveron tts --text "..." --voice "VOICE_ID" --model multilingual-v2
reveron sfx --text "explosión épica" --duration 3

# ── Post-processing ─────────────────────────────────────────────
reveron bg-remove --image "URL"
reveron upscale --image "URL" --model clarity

# ── Costo pre-flight ────────────────────────────────────────────
# Agregá --dry-run para SOLO estimar sin ejecutar
reveron video --provider fal --model kling-2.1-master \
  --prompt "..." --duration 10 --dry-run
```

## Code Examples

### Cuando el usuario pide un hero image

```
Usuario: "Reverón, necesito un hero para una landing de clínica dental, moderna"

Claude debe:
1. Detectar intent: image, hero de landing → premium quality
2. Elegir: fal + flux-pro-ultra + aspect 16:9
3. Estimar costo: $0.06 → nivel auto
4. Enriquecer prompt con contexto:
   "Hero image for dental clinic landing page, modern minimal design,
    soft blue and white color palette, ambient lighting, empty space
    on the left for headline overlay, professional photography style"
5. Ejecutar CLI
6. Mostrar al user: path del asset generado + costo
```

### Cuando el usuario pasa una referencia visual

```
Usuario: "hacé esta misma imagen pero con fondo playero" [+ URL]

Claude debe:
1. Detectar intent: image edit con referencia
2. Elegir: gemini + nano-banana (rey del edit con character consistency)
3. Estimar costo: $0.039 → nivel auto
4. Ejecutar con --refs URL
5. NO tratar de re-crear la imagen desde cero — usar la referencia
```

### Cuando el costo es alto

```
Usuario: "hacé un video con veo 3 de 8 segundos"

Claude debe:
1. Estimar: gemini:veo-3:8s = $4.00 → nivel CONFIRM
2. NO ejecutar. Responder:
   "🛑 Este video con Veo 3 (8s) sale ~$4. ¿Confirmás? Si sí, corro con --force."
3. Esperar respuesta del usuario
4. Solo entonces ejecutar con --force
```

## Extension: agregar modelos nuevos

Cuando salga un modelo que no está en el registry (los proveedores actualizan rápido):

1. Agregar al provider correspondiente en `scripts/providers/<provider>.mjs`:
   ```js
   // Ej en fal.mjs
   'flux-3': 'fal-ai/flux-3',
   ```
2. Agregar costo en `scripts/utils/cost-estimator.mjs`
3. Actualizar `references/model-matrix.md` con el nuevo caso de uso
4. Bump `metadata.version` en este SKILL.md

## Resources

- **Router CLI**: `src/generate.mjs`
- **Providers**: `src/providers/{fal,openai,gemini,kie,heygen,elevenlabs,tripo}.mjs`
- **Utils**: `src/utils/{infisical,cost-estimator,reference-loader,manifest}.mjs`
- **Matriz de decisión**: [references/model-matrix.md](references/model-matrix.md)
- **Setup + Troubleshooting**: [README.md](README.md)
