---
name: p5js
description: 'p5.js sketches: gen art, shaders, interactive, 3D.'
version: 1.0.0
platforms:
- linux
- macos
- windows
metadata:
  hermes:
    tags:
    - creative-coding
    - generative-art
    - p5js
    - canvas
    - interactive
    - visualization
    - webgl
    - shaders
    - animation
    related_skills:
    - ascii-video
    - manim-video
    - excalidraw
author: Hermes Agent
license: MIT
lane: worker-vision
reasoning_effort: xhigh
---
# p5.js Production Pipeline

## When to use

Use when users request: p5.js sketches, creative coding, generative art, interactive visualizations, canvas animations, browser-based visual art, data viz, shader effects, or any p5.js project.

## What's inside

Production pipeline for browser-based generative art using p5.js. Outputs HTML, PNG, GIF, MP4, or SVG. Covers: 2D/3D rendering, noise and particle systems, flow fields, GLSL shaders, pixel manipulation, kinetic typography, WebGL, audio analysis, mouse/keyboard interaction, and headless high-res export. Pipeline: concept → design → code → preview → export → verify.

## Creative Standard

This is visual art rendered in the browser. The canvas is the medium; the algorithm is the brush.

**Before any code**, articulate the creative concept — what it communicates, what makes the viewer stop scrolling, what separates it from a tutorial example. The user's prompt is a starting point; interpret it with creative ambition.

**First-render excellence is non-negotiable.** The output must be visually striking on first load. If it looks like a tutorial exercise, a default configuration, or "AI-generated creative coding," it is wrong.

**Go beyond the reference vocabulary.** Noise functions, particle systems, palettes, and shader effects are a starting vocabulary. The catalog is a palette of paints — you write the painting.

**Be proactively creative.** If the user asks for "a particle system," deliver one with emergent flocking, trailing ghost echoes, palette-shifted depth fog, and a noise field that breathes. Include at least one visual detail the user didn't ask for.

**Dense, layered, considered.** Never flat white backgrounds. Always compositional hierarchy. Always intentional color.

**Cohesive aesthetic over feature count.** All elements must serve a unified visual language — shared color temperature, consistent stroke vocabulary, harmonious motion speeds.

## Modes

| Mode | Reference |
|------|-----------|
| Generative art, image processing, particles, texture | `references/visual-effects.md` |
| Data viz, interactive, audio-reactive, layering, fxhash | `references/interactive-patterns.md` |
| 3D scene, shaders, WebGL | `references/webgl-shaders.md` |
| Animation, motion, sketches, export pipeline | `references/sketches.md`, `animation.md`, `export-pipeline.md` |

## Stack

Single self-contained HTML file per project. No build step required.

| Layer | Tool | Purpose |
|-------|------|---------|
| Core | p5.js 1.11.3 (CDN) | Canvas rendering, math, transforms |
| 3D | p5.js WebGL mode | 3D geometry, camera, lighting, GLSL |
| Audio | p5.sound.js (CDN) | FFT, amplitude, mic input, oscillators |
| Export | `saveCanvas/Gif/Frames` | PNG, GIF, frame sequence |
| Capture | CCapture.js (optional) | Deterministic WebM/GIF |
| Headless | Puppeteer + Node (optional) | High-res rendering, MP4 via ffmpeg |
| SVG | p5.js-svg 1.6.0 (optional) | Vector output for print |
| Texture | p5.grain (optional) | Film grain, texture overlays |

**p5.js 1.x** (1.11.3) is the default — broadest library compatibility. **p5.js 2.x** adds `async setup()`, OKLCH color, `splineVertex()`, shader `.modify()`, variable fonts, `textToContours()`. See `references/core-api.md` § p5.js 2.0.

## Pipeline

```
CONCEPT → DESIGN → CODE → PREVIEW → EXPORT → VERIFY
```

1. **CONCEPT** — Mood, color world, motion vocabulary, what makes this unique
2. **DESIGN** — Mode, canvas size, interaction model, color system, export format
3. **CODE** — Single HTML file with inline p5.js. Globals → `preload()` → `setup()` → `draw()` → helpers → classes → event handlers. See `references/sketches.md` for the canonical scaffold
4. **PREVIEW** — Open in browser, verify visual quality at target resolution
5. **EXPORT** — `saveCanvas()` for PNG, `saveGif()` for GIF, `saveFrames()` + ffmpeg for MP4, Puppeteer for headless batch
6. **VERIFY** — Match concept? Visually striking at intended display size? Would you frame it?

## Aesthetic Dimensions

| Dimension | Reference |
|-----------|-----------|
| Color, noise, motion, easing | `references/color-and-noise.md` |
| Shaders, 3D, WebGL, lighting | `references/webgl-shaders.md` |
| Interaction, audio, scroll, fxhash, layers | `references/interactive-patterns.md` |
| Particles, texture, image processing | `references/visual-effects.md` |
| Shapes, geometry, SDF, SVG paths | `references/shapes-and-geometry.md` |
| Animation, typography, composition, color systems | `references/animation.md`, `typography.md`, `core-api.md`, `color-systems.md` |
| Performance, troubleshooting | `references/performance.md`, `references/troubleshooting.md` |

## Per-Project Variation Rules

Never use default configurations:

- **Custom palette** (3–7 colors) — never raw `fill(255, 0, 0)`
- **Custom stroke vocabulary** — thin (0.5), medium (1–2), bold (3–5)
- **Background treatment** — never plain `background(0)` or `background(255)`; always textured, gradient, or layered
- **Motion variety** — primary at 1x, secondary at 0.3x, ambient at 0.1x
- **At least one invented element** — custom particle behavior, novel noise use, unique interaction response

## Quick-Start: Minimum Viable Sketch

```html
<!DOCTYPE html><html><head><meta charset="UTF-8"><title>p5 Sketch</title>
<script>p5.disableFriendlyErrors = true;</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.11.3/p5.min.js"></script>
<style>html,body{margin:0;padding:0;overflow:hidden}canvas{display:block}</style>
</head><body><script>
const SEED = 42; let t = 0;
function setup() {
  createCanvas(1920, 1080);
  colorMode(HSB, 360, 100, 100, 100);
  randomSeed(SEED); noiseSeed(SEED);
}
function draw() {
  background(220, 30, 8);
  // ... your algorithm here ...
  t += 0.01;
}
</script></body></html>
```

Open in browser. For full scaffold (CONFIG/PALETTE/classes/exports) see `references/sketches.md`.

## API Quick-Reference

| Category | Calls |
|----------|-------|
| **Canvas** | `createCanvas(w,h[,WEBGL])`, `resizeCanvas`, `pixelDensity(1)`, `push/pop/translate/rotate/scale` |
| **Color** | `colorMode(HSB,360,100,100,100)`, `fill(h,s,b,a)`, `stroke`, `noFill`, `noStroke`, `lerpColor(c1,c2,t)`, `blendMode` |
| **Math** | `map(v,a,b,c,d)`, `constrain`, `lerp(a,b,t)`, `norm(v,a,b)`, `dist`, `TAU` |
| **Random** | `random(a,b)`, `randomSeed(s)`, `noise(x,y,z)`, `noiseSeed(s)` — use FBM (see color-and-noise.md) |
| **Shape** | `rect`, `ellipse`, `line`, `beginShape/vertex/endShape`, `bezierVertex`, `curveVertex` |
| **Image** | `loadImage`, `image(img,x,y)`, `loadPixels`, `updatePixels`, `filter(BLUR\|INVERT\|...)` |
| **Buffer** | `createGraphics(w,h)`, `image(buf,0,0)` — for layers/trails (see interactive-patterns.md) |
| **Text** | `text(str,x,y)`, `textSize`, `textAlign`, `loadFont`, `textToPoints` (see typography.md) |
| **Export** | `saveCanvas('name','png')`, `saveGif('name',5)`, `saveFrames('f','png',10,30)` |
| **3D** | `box`, `sphere`, `plane`, `camera`, `orbitControl`, `ambientLight`, `directionalLight` |
| **Shader** | `loadShader(v,f)`, `shader(s)`, `filter(s)`, `s.setUniform(name,val)` (see webgl-shaders.md) |
| **Events** | `mousePressed/Released/Dragged/Moved`, `keyPressed/Released`, `touchStarted/Moved`, `windowResized` |
| **State** | `mouseX/Y`, `mouseIsPressed`, `key`, `keyCode`, `millis()`, `frameCount` |

## Critical Rules

- **Disable FES**: `p5.disableFriendlyErrors = true` BEFORE `setup()` — 10x perf hit otherwise
- **`pixelDensity(1)`** on retina — prevent 2x–4x overdraw
- **Seeded randomness always**: `randomSeed()` + `noiseSeed()` — never `Math.random()` for visual elements
- **Use HSB**: dramatically easier than RGB for generative art. Define palette object, derive variations procedurally
- **Use FBM** (multi-octave noise): raw `noise()` looks like smooth blobs — see `references/color-and-noise.md`
- **Use offscreen buffers** (`createGraphics()`): layer bg/fg/trails, never single-pass
- **Vectorize**: one `beginShape(POINTS)` + many `vertex()` beats many `ellipse()`. For massive counts use pixel buffer directly
- **Hot-loop math**: `Math.sin/cos/sqrt` faster than p5 wrappers. No `console.log` / DOM mutation in `draw()`
- **Standard key bindings**: `s` = save PNG, `g` = save GIF, `r` = reseed, space = pause — see `references/sketches.md`
- **Headless export**: `noLoop()` + `window._p5Ready = true` required for Puppeteer capture
- **Instance mode** for multiple sketches per page or framework integration
- **WebGL gotchas**: origin is center, Y-axis flipped, `translate(-w/2, -h/2)` for P2D coords, `push()/pop()` every transform
- **Audio**: `mic.start()` must follow a user gesture (browser autoplay rule)

## Workflow

1. **Write HTML** — single self-contained file, all code inline
2. **Open in browser** — `xdg-open sketch.html` (Linux) / `open sketch.html` (macOS)
3. **Local assets** (fonts, images) require a server: `python3 -m http.server 8080`
4. **Export PNG/GIF** — add `keyPressed()` shortcuts (see `references/sketches.md`), tell user which key
5. **Headless export** — `node scripts/export-frames.js sketch.html --frames 300` (sketch must use `noLoop()` + `_p5Ready`)
6. **MP4 rendering** — `bash scripts/render.sh sketch.html output.mp4 --duration 30`
7. **Iterate** — edit HTML, user refreshes browser
8. **Load references on demand** — `skill_view(name="p5js", file_path="references/...")`

## References

**Core (created by this slim-down)** — deep dives for the patterns referenced above:

| File | Contents |
|------|----------|
| `references/sketches.md` | HTML scaffold, CONFIG/PALETTE patterns, key bindings, `noLoop()` headless export |
| `references/webgl-shaders.md` | WebGL gotchas, instance mode, `createShader`, GLSL uniforms, 3D primitives, lighting |
| `references/interactive-patterns.md` | Mouse/keyboard/touch, DOM controls, p5.sound audio, scroll-driven, fxhash, `createGraphics` layers |
| `references/performance.md` | FES disable, hot-loop `Math.*`, vectorization, pixel buffer, profiling, memory leaks |
| `references/color-and-noise.md` | HSB, FBM noise, domain warping, curl noise, p5.Vector, easing, trig quick-ref |

**Subject index** (consult as needed during a project):

- Shapes, geometry, SDF, SVG paths → `references/shapes-and-geometry.md`
- Particles, texture, image processing, reaction-diffusion → `references/visual-effects.md`
- Composition, offscreen buffers, p5.js 2.0 → `references/core-api.md`
- Blend modes, color harmony → `references/color-systems.md`
- Animation, easing, state machines, timeline → `references/animation.md`
- Typography, `textToPoints`, kinetic text → `references/typography.md`
- Export pipeline (saveCanvas/Gif, Puppeteer, CCapture, ffmpeg, SVG, fxhash) → `references/export-pipeline.md`
- Troubleshooting, common mistakes, browser compat, CORS → `references/troubleshooting.md`
- Interactive viewer template (seed nav, sliders, download) → `templates/viewer.html`

## Creative Divergence

Use when the user requests experimental / creative / unique / unconventional output. Pick one strategy BEFORE generating code.

- **Conceptual Blending** — user names two things to combine. Map correspondences (X = A, Y = B). Blend selectively; code as one unified system
- **SCAMPER** — take a known pattern (flow field, particle system, L-system, cellular automata) and transform via Substitute / Combine / Adapt / Modify / Purpose / Eliminate / Reverse
- **Distance Association** — anchor on user's concept, generate close (obvious) / medium (interesting) / far (abstract) associations, develop the medium ones

The medium-distance associations are the sweet spot: specific enough to visualize but unexpected enough to be interesting.