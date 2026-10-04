---
name: vidtsx-2d-generator
description: Generate production-ready 2D TSX video files for VidTSX (Remotion-based) from a shot, scene, or video description. Use whenever the user wants to create or generate a VidTSX video, a 2D TSX shot or scene, an animated clip, title card, or rendered motion graphic — including when they describe a visual animation they want built, or say "make a shot", "build this scene", "generate the TSX", or "turn this into a video". Covers the mandatory file structure and composition config, dimension presets (horizontal/vertical/square), six style presets (minimalist, memphis, neo-brutalism, glassmorphism, neon, corporate), and the hard rules that keep renders from crashing, covering frame-based animation only (no useState/useEffect/setTimeout), strictly monotonic interpolate ranges, Easing.bezier not wrapper syntax, and the chroma-js and @remotion/paths import gotchas. Not for 3D/three.js compositions, general React work, or editing video files.
---

# VidTSX 2D Video Generator

Generate production-ready 2D TSX video files for VidTSX from a description of a shot or video. The files are Remotion compositions that VidTSX renders frame-by-frame, so correctness matters more than cleverness: a single non-monotonic `interpolate` range or a stray `useState` will crash the render.

This skill covers **2D motion graphics**. 3D work (`@remotion/three` / React Three Fiber) is out of scope.

## How to use this skill

1. **Clear single shot** → generate the `.tsx` file directly.
2. **Complex, multi-shot, or visually ambiguous request** → confirm the shot breakdown or visual direction in one short message first, then generate. Don't over-ask; a one-line confirmation is enough.
3. **Deliver as an actual `.tsx` file**, not inline code. These TSX components always exceed 20 lines, and the user edits these files directly. Default to **one shot per file** (atomic, easy to edit) unless the user asks for a single combined deliverable.
4. The file contains **only the component code** — the structural section comments below are welcome, but no markdown fences, no prose explanations inside the file.
5. **Render it and look before calling it done** — see [Verify the render](#verify-the-render-do-not-skip). A shot you have only reasoned about is not finished; a still (and, for reveals/scrolls, frames at each cue) is the bar.

---

## Output spec

### Dimension presets

| Format     | Width | Height | Use case                   |
|------------|-------|--------|----------------------------|
| horizontal | 1920  | 1080   | YouTube, presentations     |
| vertical   | 1080  | 1920   | TikTok, Reels, Shorts      |
| square     | 1080  | 1080   | Instagram feed             |

### Defaults

- **Format:** horizontal (1920×1080)
- **Duration:** 5 seconds
- **FPS:** 30
- **Style:** minimalist (see `references/style-presets.md`)

---

## Mandatory file structure

Every generated file follows this skeleton. The labeled section comments are intentional — they keep large files navigable.

```tsx
import React from 'react';
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
  AbsoluteFill,
  Sequence,
} from 'remotion';

// =============================================================================
// COMPOSITION CONFIG
// =============================================================================
export const compositionConfig = {
  id: 'ComponentName', // PascalCase only — NO hyphens or underscores
  durationInSeconds: 5,
  fps: 30,
  width: 1920,
  height: 1080,
};

// =============================================================================
// STYLE CONSTANTS
// =============================================================================
const COLORS = {
  primary: '#6366f1',
  secondary: '#8b5cf6',
  accent: '#06b6d4',
  background: '#0f0f23',
  text: '#ffffff',
} as const;

const TYPOGRAPHY = {
  fontFamily: 'Inter, system-ui, sans-serif',
} as const;

const EASINGS = {
  easeOut: Easing.bezier(0.33, 1, 0.68, 1),
  easeIn: Easing.bezier(0.32, 0, 0.67, 0),
  easeInOut: Easing.bezier(0.37, 0, 0.63, 1),
  overshoot: Easing.bezier(0.34, 1.56, 0.64, 1),
} as const;

// =============================================================================
// PRE-GENERATED DATA (computed once at module level, NOT during render)
// =============================================================================
const seededRandom = (seed: number): number => {
  const x = Math.sin(seed * 9999) * 10000;
  return x - Math.floor(x);
};

// =============================================================================
// MAIN COMPONENT
// =============================================================================
const ComponentName: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames, width, height } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.background }}>
      {/* Content */}
    </AbsoluteFill>
  );
};

export default ComponentName;
```

Swap `ComponentName` for a PascalCase name describing the shot, set the `COLORS` block from the chosen style preset, and set `width`/`height`/`durationInSeconds`/`fps` from the request.

---

## Correctness rules

These are not stylistic preferences — they are what makes a render succeed. VidTSX (via Remotion) renders each frame by calling the component at a fixed frame number. There is no event loop, no persistence between frames, and no wall-clock time. Anything that assumes those things will break.

### Animation is frame-based, always

- Drive **all** motion from `useCurrentFrame()` + `interpolate()`.
- **Never** use `useState`, `useEffect`, `setTimeout`, `setInterval`, or CSS animations/transitions. They don't fit the frame-by-frame model and produce broken or non-deterministic output.
- For anything random or procedural, use `seededRandom` (or an equivalent seeded function) so every render of a given frame is identical. Pre-generate particle/random arrays **at module level**, never inside the render function — recomputing per frame causes flicker.
- Stagger animations so elements enter in sequence rather than all at once. It reads better and is the expected look.

### interpolate — input ranges must be strictly increasing

`interpolate`'s input range has to be strictly monotonically increasing. Duplicate or descending values throw at runtime.

```tsx
// ✅ Correct
interpolate(frame, [0, 30, 60], [0, 1, 0]);

// ❌ Throws — input range descends
interpolate(frame, [60, 30, 0], [0, 1, 0]);
```

To **reverse** a mapping, flip the *output* range, never the input range:

```tsx
// ✅ Correct — maps 0→100, 1→0
interpolate(value, [0, 1], [100, 0]);

// ❌ Wrong
interpolate(value, [1, 0], [100, 0]);
```

For index-based timing, make sure `startFrame < endFrame` and always clamp:

```tsx
const startFrame = index * 30;
const endFrame = startFrame + 30;
interpolate(frame, [startFrame, endFrame], [0, 1], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
```

**Always** pass `extrapolateLeft: 'clamp'` and `extrapolateRight: 'clamp'` unless an unbounded value is genuinely wanted — without them, values shoot past their range before/after the keyframes.

### Easing — use Easing.bezier(), never wrapper syntax

Wrapper forms like `Easing.out(Easing.cubic)` crash. Define named beziers once (see the `EASINGS` block in the skeleton) and reference them:

```tsx
// ❌ Crashes
Easing.out(Easing.cubic);
Easing.in(Easing.quad);

// ✅ Correct
interpolate(frame, [0, 30], [0, 1], {
  easing: EASINGS.easeOut,
  extrapolateRight: 'clamp',
});
```

### chroma-js — namespace import only

```tsx
// ✅ Correct
import * as chroma from 'chroma-js';
const color = chroma('#00bfff').brighten(0.5).hex();

// ❌ Wrong — "chroma is not a function"
import chroma from 'chroma-js';
```

### @remotion/paths — only the real functions exist

These helpers **do not exist** and must never be used:
`makeCircle()`, `makeRect()`, `makeTriangle()`, `makeLine()`, `makePie()`, `makePolygon()`, `makeEllipse()`, `makeStar()`.

Only these imports are valid:

```tsx
import { evolvePath, getLength, getPointAtLength, getTangentAtLength } from '@remotion/paths';
```

Write SVG path strings by hand and animate them with `evolvePath`:

```tsx
const circlePath = 'M 50 10 A 40 40 0 1 1 49.99 10 Z';
const rectPath = 'M 0 0 L 100 0 L 100 50 L 0 50 Z';
const linePath = 'M 0 0 L 100 100';

const { strokeDasharray, strokeDashoffset } = evolvePath(progress, rectPath);
```

### Composition ID

`compositionConfig.id` is **PascalCase only** — no hyphens, no underscores (e.g. `ProductReveal`, not `product-reveal` or `product_reveal`).

---

## Layout

### Safe zones

- **Top 10%:** reserve for platform UI.
- **Bottom 15%:** reserve for captions/buttons.
- Keep primary content between **25%–75%** vertically.

### Centering helper

```tsx
const centered: React.CSSProperties = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
};
```

---

## Typography

| Element       | Size       | Weight  |
|---------------|------------|---------|
| Headlines     | 72–120px   | 700–900 |
| Subheadlines  | 36–48px    | 500–700 |
| Body          | 28–36px    | 400–500 |

Always set `margin: 0` on text elements — browser defaults push layouts off-center.

---

## Style presets

When the user names a style, load its palette and characteristics from **`references/style-presets.md`** and drop the `COLORS` object into the skeleton. The six presets are: **minimalist** (default), **memphis**, **neo-brutalism**, **glassmorphism**, **neon/cyberpunk**, and **corporate**. If no style is named, use minimalist.

---

## Verify the render (do not skip)

A shot is not done until you have **looked at it**. After writing the `.tsx`, render at least one still and open it — never hand over a shot you have only reasoned about. Rendering succeeds and the numbers look right, yet text overflows its card, an image is cropped at the wrong crop, an element is off-screen, or two things overlap. Only a screenshot catches these.

- Render a still (e.g. `node scripts/render-all.mjs --still --scale=1 <ShotId>`) and Read the PNG.
- For time-based reveals (elements entering on a cue, scrolls, staged phases), a single 60%-of-duration still is not enough — render the full clip and pull frames at each key moment (`ffmpeg -ss <t> -i out/<id>.mp4 -frames:v 1 f.jpg`), or render stills at several offsets. Verify the state at each cue, not just one frame.
- Check specifically: images fit their slot (no important content cropped; prefer `objectFit: contain` on a matching background for heterogeneous real images), text is not clipped or overflowing, nothing is off the safe area, and each animated element is actually visible when it should be.
- If it is composited over other footage, also spot-check a frame from the final baked output, not just the isolated shot.

Fix what the screenshot reveals, then re-render and look again. Treat "I rendered it and it looks correct" — with the frame shown — as the bar for done.

---

## Final output

Generate the complete `.tsx` file and nothing else inside it — no surrounding markdown, no commentary before or after the code in the file itself. A short one-line note in chat when handing over the file is fine.
