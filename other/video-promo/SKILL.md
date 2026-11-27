---
name: video-promo
description: Regenerar el vídeo promocional horizontal de Rally Copilot (Remotion, 1920×1080, ~32 s) con clips reales del emulador y video/src/guion.ts; no sube a YouTube ni toca la ficha de Play.
argument-hint: "[--grabar|--solo-grabar|--sin-render|--control]"
allowed-tools: Read, Bash(node scripts/video/promo.mjs*), Bash(bash scripts/video/grabar-clips.sh*), Bash(adb *), Bash(ffprobe *)
disable-model-invocation: true
---

# video-promo

Compone `build/promo/rally-copilot-promo-1920x1080.mp4` (1920×1080, 30 fps, ~32 s, música CC0 de
`video/public/musica/` y la voz del copiloto de los clips). Proyecto Remotion en `video/` (DECISIONES.md § H12a). Todo lo
editable está en `video/src/guion.ts`: tramos (clip, inicio, duración, título, subtítulo, tono, voz, crono), bpm,
entrada, cierre y música.

Reglas de Play (https://support.google.com/googleplay/android-developer/answer/9866151): la app real en los primeros
10 s y en ≥ 80 % del vídeo, poco texto, nada de «mejor», «#1» ni «descarga ya», ni la marca «WRC». Horizontal.

## Cuándo usarla
- Tras cambios visibles en la app o antes de una versión de producción.
- Para cambiar textos, tiempos o animaciones del vídeo, o para regrabar los clips `c1`…`c5`.

## Cuándo NO usarla
- Capturas de la ficha → `node scripts/ficha-play.mjs --capturas` (ver `docs/play.md`).
- Solo instalar la app o una captura suelta → `android-install-and-logcat`.
- Cómo animar en Remotion → `remotion-best-practices`; exportar → `remotion-render`.

## Precondiciones
- Para regrabar: emulador `trombito-36` con la app debug instalada, scrcpy (winget `Genymobile.scrcpy`) y la traza
  `docs/rutas/ma-2141-sa-calobra.gpx`. `grabar-clips.sh` deja el emulador en un estado conocido y lo restaura al acabar.
- Sin regrabar: `build/promo/clips/` o `video/public/clips/` con `c1-notas`, `c2-tramo`, `c3-fantasma`, `c4-resumen`,
  `c5-temporada` (`.mp4`).
- `video/node_modules` (si falta, `promo.mjs` ejecuta `npm ci`). ffprobe y Python con Pillow para el control.

## Pasos
1. Regrabar si cambió la app: `node scripts/video/promo.mjs --grabar` (o `bash scripts/video/grabar-clips.sh <fase>`).
2. Solo renderizar: `node scripts/video/promo.mjs`.
3. Cambiar textos o tiempos: `video/src/guion.ts`. Previsualizar: `cd video && npm run studio` (lo arranca Joan).
4. Control: `node scripts/video/promo.mjs --control` (con `--sin-render`, solo stills) y mirar
   `build/promo/control-hoja.png`: nada cortado, sin diálogos ni pantallas vacías, la app antes del s 10.
5. Subida (manual, Joan): YouTube «Oculto», no dirigido a niños; pegar `https://www.youtube.com/watch?v=<id>` en Play
   Console > Ficha > Vídeo.

## Validaciones / tests
- `cd video && npm run typecheck`.
- `ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,pix_fmt -of csv=p=0 build/promo/rally-copilot-promo-1920x1080.mp4` → `1920,1080,30/1,yuv420p`.
- Duración entre 28 y 34 s y pista de audio presente (`-select_streams a`).
- `build/` y `video/public/clips/` no se versionan.

## Definition of Done
- [ ] Clips reales sin diálogos ni errores, con la voz en `c1`–`c3`.
- [ ] MP4 validado con ffprobe y hoja de control revisada.
- [ ] Emulador restaurado (tamaño, densidad, modo demo).
- [ ] Subida a YouTube y URL en Play: pendiente de Joan, anotada en `docs/ESTADO.md` si no se hace en la sesión.

## Docs a actualizar
- `docs/play.md` · `video/README.md` · `docs/ESTADO.md` (session-handoff)
