---
name: remotion-render
description: Exportar un vídeo o still de Remotion con npx remotion render/still, incluido vídeo con transparencia; el promo de Rally Copilot se renderiza con node scripts/video/promo.mjs.
metadata:
  version: "4.0.537"
---

## General rendering strategy

Render a video using:

```
npx remotion render
```

Full list of options: https://www.remotion.dev/docs/cli/render.md

Render a still using:

```
npx remotion still
```

Full list of options: https://www.remotion.dev/docs/cli/still.md

To render several frames as images in one call, use `render --frames`:

```
npx remotion render [composition-id] out/frames --frames=0,30,90 --image-format=png
```

See https://www.remotion.dev/docs/cli/render.md#--frames for more options.

## Transparent videos

See [Transparent videos](./transparent-videos.md) for rendering out a video with transparency.

## Cuándo usarla
- Exportar el vídeo o un fotograma del proyecto Remotion de `video/` (el proyecto usa Remotion 4.0.533 fijado).
- Renderizar con opciones avanzadas (frames sueltos, transparencia ProRes/VP9).

## Cuándo NO usarla
- Escribir o editar composiciones → `remotion-best-practices`.
- Grabar clips del emulador y montaje ffmpeg → `video-promo`.

## Precondiciones
- `video/` con `npm install` hecho; ejecutar los comandos `npx remotion` desde `video/`.
- Render del promo: `node scripts/video/promo.mjs` (salida en `build/promo/`, ignorado por git).

## Pasos
1. Render habitual: `node scripts/video/promo.mjs`; para otras opciones, `npx remotion render` desde `video/` según la guía anterior.
2. En Windows, `--props` debe ser un archivo.
3. Comprobar la salida con `ffprobe`.

## Validaciones / tests
- `ffprobe -v error -show_entries stream=width,height,r_frame_rate -of csv=p=0 <salida>` coincide con la composición.
- `cd video && npm run typecheck` en verde antes de renderizar.

## Definition of Done
- [ ] Archivo generado en `build/promo/` y verificado con `ffprobe`.
- [ ] Nada de salidas de render añadidas al repo.

## Docs a actualizar
- `video/README.md` si cambian comandos de render · docs/ESTADO.md (skill session-handoff)

## Origen
- Repo https://github.com/remotion-dev/skills (espejo de `packages/skills` de remotion-dev/remotion), versión 4.0.537, copiado el 2026-10-20.
- Licencia: la del monorepo, https://github.com/remotion-dev/remotion/blob/main/LICENSE.md (el espejo no tiene LICENSE propia).
- Adaptado al repo: frontmatter (`version` pasa a `metadata`), `description` en español y secciones de la plantilla; el cuerpo técnico original queda intacto.
