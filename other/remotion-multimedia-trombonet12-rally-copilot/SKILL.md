---
name: remotion-multimedia
description: Obtener duración o dimensiones de archivos de audio y vídeo en el navegador con Mediabunny (Remotion); no compone ni renderiza vídeo.
metadata:
  version: "4.0.537"
---

Mediabunny is a multimedia library for dealing with audio and video in the browser.
Here is a compact overview of its capabilities: https://mediabunny.dev/llms.txt

## Getting audio duration

See [get-audio-duration.md](get-audio-duration.md) for getting the duration of an audio file in seconds with Mediabunny.

## Getting video dimensions

See [get-video-dimensions.md](get-video-dimensions.md) for getting the width and height of a video file with Mediabunny.

## Getting video duration

See [get-video-duration.md](get-video-duration.md) for getting the duration of a video file in seconds with Mediabunny.

## Cuándo usarla
- Leer duración de audio o vídeo, o dimensiones de un vídeo, dentro del proyecto Remotion de `video/` (p. ej. `calculateMetadata` para clips de `public/clips/`).

## Cuándo NO usarla
- Componer o editar escenas → `remotion-best-practices`.
- Exportar → `remotion-render`.
- Inspección puntual desde la shell → `ffprobe`.

## Precondiciones
- `video/` con `npm install` hecho (Remotion 4.0.533 fijado).
- Mediabunny es dependencia nueva: añadirla solo con la skill `dependency-add`, en versión exacta compatible.

## Pasos
1. Elegir la guía (audio, dimensiones o duración de vídeo) y seguir su código.
2. Integrarlo en `video/src`, p. ej. en `calculateMetadata`.

## Validaciones / tests
- `cd video && npm run typecheck` sin errores.
- La duración o dimensiones obtenidas coinciden con `ffprobe` sobre el mismo archivo.

## Definition of Done
- [ ] Valores correctos verificados contra `ffprobe`.
- [ ] Dependencias añadidas solo vía `dependency-add`.

## Docs a actualizar
- `video/README.md` si cambia algo del proyecto · docs/ESTADO.md (skill session-handoff)

## Origen
- Repo https://github.com/remotion-dev/skills (espejo de `packages/skills` de remotion-dev/remotion), versión 4.0.537, copiado el 2026-10-20.
- Licencia: la del monorepo, https://github.com/remotion-dev/remotion/blob/main/LICENSE.md (el espejo no tiene LICENSE propia).
- Adaptado al repo: frontmatter (`version` pasa a `metadata`), `description` en español y secciones de la plantilla; el cuerpo técnico original queda intacto.
