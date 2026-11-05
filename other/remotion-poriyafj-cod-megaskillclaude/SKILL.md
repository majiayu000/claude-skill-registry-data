---
name: remotion
description: Generate cinematic videos programmatically with React (Remotion), including animations, captions/subtitles, effects and rendering pipelines. Use for code-based video creation.
---

# Remotion — Programmatic Video

Build videos as code with React + Remotion.

## Project structure
- `src/Root.tsx` — register `Composition`s (id, durationInFrames, fps, width/height).
- Scenes as components; drive everything off `useCurrentFrame()` and `interpolate()` / `spring()` from `remotion`.
- Assets in `public/`; dynamic content via `defaultProps`/`calculateMetadata`.

## Techniques
1. **Animation** — `spring()` for organic motion, `interpolate(..., {easing})` for transitions; sequence with `<Series>` or absolute frame math.
2. **Captions** — word/sentence timing JSON → `<Caption>` component; styles: karaoke highlight, pop-in, bottom third.
3. **Audio** — `<Audio>`, `getAudioDurationInSeconds` to sync scenes; ducking via volume functions.
4. **Effects** — masking, blur/shake transitions, particle overlays (canvas), Lottie layers.
5. **Templates** — parameterize text, colors, media so one comp renders many videos.

## Render
```bash
npx remotion studio            # preview
npx remotion render MyComp out.mp4
npx remotion render MyComp out.mp4 --props='{"title":"..."}'
npx remotion lambda render ... # serverless scale
```

## Rules
- 30/60fps; safe margins for captions; mobile-first 9:16 variants via separate comps.
- Keep every animation frame-pure (no side effects in render).

## Output
Runnable Remotion project + render commands + parameter table.
