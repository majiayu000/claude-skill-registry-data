---
name: motion-render
description: "Use when turning a locked brief and beat map into a film file — deterministic seek(t) scene split into classic scripts (springs, springSum, stagger, density validator, actor, CSS 3D, cursor interaction, pinned lit three.js), zero-dependency Chrome capture, staged render (stills one per beat → draft → master with subframe motion blur, stills by default), ffmpeg mp4 + GIF, VHS terminal films, audio on a measured beat grid, and verification of the delivered file."
versions:
  fuse-motion: "1.0.0"
  ffmpeg: "9.0.2"
  bun: "1.4.2"
  vhs: "0.12.1"
user-invocable: true
references: references/seek-contract.md, references/determinism.md, references/stages-budgets.md, references/encoding.md, references/delivery-github.md, references/vhs-terminal.md, references/verification.md, references/audio.md, references/templates/capture-cdp.md, references/templates/render-cli.md, references/templates/timeline-seek.md, references/templates/interaction-kit.md, references/templates/webgl-scene.md, references/templates/index-skeleton.md, references/templates/vhs-tape.md
related-skills: motion-art-direction, motion-method, motion-craft, motion-assets, motion-review, fuse-design:design-motion
---

<objective>
The production half of the fuse-motion pipeline: from `.motion/brief.md` and
`.motion/beats.md` (owned by `motion-method`) to a verified file. A film is a pure
function of time — an HTML or canvas scene exposing `window.seek(t)` — captured frame by
frame by headless Chrome over the DevTools Protocol with zero dependencies, then encoded
by ffmpeg (H.264 mp4 + palette GIF). Rendering is staged: `stills` (the default when
`--stage` is omitted, so a forgotten flag can never skip a gate) → owner gate G1 →
`draft` 540p → critic + owner gate G2 → `master`, whose FILE is verified by ffprobe,
frame count, byte budget and SSIM against the approved stills.

Terminal subjects use VHS tapes; sound, when the brief asks for it, follows the audio
reference. Templates are generalized from the proven `docs/demo/statusline-mod/` and
`docs/demo/hook-sniper.tape` pipelines and were run end to end before shipping.
</objective>

# Motion Render

## Agent Workflow (MANDATORY)

1. **Read the locked inputs**: `.motion/brief.md` (surfaces, byte budgets, aspect,
   duration) and `.motion/beats.md` — if either is missing, go back to `motion-method`.
2. **Check tools**: `ffmpeg -version`, `ffprobe -version`, `bun --version`, a Chrome
   binary (or `CHROME_BIN`); `vhs --version` + `ttyd` for terminal films. Missing tool →
   say so, never fake a render.
3. **Scaffold the scene**: `motion-art-direction` templates FIRST —
   composition-grid (layout), kinetic-type (word behaviours), cut-rhythm (beat map) —
   only after `look.md` and the key frames exist. This skill then adds the mechanics:
   the shell, the `seek` clock, capture and encode (never hand-roll a capture).
4. **Render `stills`** → STOP at G1. **`draft`** → `motion-critic` → STOP at G2.
   **`master`** → verify the FILE. The harness `motion` scope denies draft/master until
   the owner types `MOTION-APPROVE` — stop at each gate anyway, never lean on the deny.
5. **Hand off**: lead runs `fuse-ai-pilot:sniper` on the scripts and the challenger on
   the "done" claim.

---

## Overview

| Concern | Choice | Reference |
|---------|--------|-----------|
| Scene | DOM, 2D canvas or a WebGL layer with `window.seek(t)`, DURATION, FPS, STILLS, ready; a gesture in progress at every moment (`validateDensity`); look from `motion-art-direction` | [seek-contract.md](references/seek-contract.md) |
| Reproducibility | Time-driven only, seeded PRNG, double rAF, proven vs reported flags; CSS 3D and lit WebGL paths | [determinism.md](references/determinism.md) |
| Stages | stills (default, one per beat) → draft → master, budget log, `--jobs` chunks | [stages-budgets.md](references/stages-budgets.md) |
| Encoding | libx264 yuv420p BT.709 faststart; GIF palettegen/paletteuse; master motion blur from subframes + `tmix` | [encoding.md](references/encoding.md) |
| Delivery | GIF inline + mp4 link on GitHub | [delivery-github.md](references/delivery-github.md) |
| Terminal | VHS tape + scripted demo | [vhs-terminal.md](references/vhs-terminal.md) |
| Proof | ffprobe facts, exact frames, budgets, SSIM, spikes, color tags | [verification.md](references/verification.md) |
| Sound | Licensed track ~120 BPM, beat grid measured from the song, start on a downbeat, SFX by measured peak, -14 LUFS, silent cut | [audio.md](references/audio.md) |

---

## Critical Rules

1. **`seek(t)` is pure** — same `t`, same pixels, any order. No CSS animation, no wall
   clock, no unseeded randomness, no state between frames.
2. **`--stage` defaults to `stills`** — omitting it cannot skip a gate; unknown values
   exit 2. Pass a literal stage: the harness counts `--stage "$S"` as master. Stop at
   G1 and G2.
3. **Verify the file, not the frames** — exact `DURATION x FPS` frames, h264/yuv420p,
   budget, SSIM vs approved stills. "ffmpeg exited 0" is not proof.
4. **No invented flags or APIs** — every Chrome/ffmpeg option is either proven by the
   reference pipeline or labelled "reported, verify".
5. **Facts from files only** — on-screen numbers from `.motion/facts.md`, labelled example
   data; no client names, no real spend, real masked screenshots (`motion-assets`).
6. **Fix in the scene, not with re-renders** — a critic finding is a code change + a new
   draft, never a sequence of masters.

---

## Architecture

```
.motion/
├── brief.md, beats.md, facts.md, assets.json   ← motion-method / motion-assets
├── scene/index.html + lib.js, beats.js|rhythm.js, grid.js, kinetic.js, timeline.js
│                                               ← classic scripts in that order (each within `FUSE_SOLID_MAX_LINES`):
│                                                 index-skeleton.md shell + timeline-seek.md clock
├── capture.js                                  ← capture-cdp.md
├── render.js + encode.js                       ← render-cli.md
├── terminal.tape + terminal-demo.sh            ← vhs-tape.md (terminal films)
├── stills/   still-1..N.png, contact.png       (G1 artifact)
├── out/      draft.mp4 (G2 artifact), master.mp4, master.gif
├── review/   review pack (motion-review)
├── work/     frames + Chrome profiles (gitignore)
└── budget.json                                 renders per stage + wall time
```

→ See [render-cli.md](references/templates/render-cli.md) for the complete CLI

---

## Reference Guide

### Concepts

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Seek contract** | [seek-contract.md](references/seek-contract.md) | Writing/porting a scene; GSAP/WAAPI adapters; canvas camera |
| **Determinism** | [determinism.md](references/determinism.md) | Drift, stutter, blank frames, cuts on frame boundaries |
| **Stages & budgets** | [stages-budgets.md](references/stages-budgets.md) | Choosing a stage, long films, render counts |
| **Encoding** | [encoding.md](references/encoding.md) | mp4/GIF settings, color shift, banding, over budget |
| **GitHub delivery** | [delivery-github.md](references/delivery-github.md) | README/docs embedding, size limits |
| **VHS terminal** | [vhs-terminal.md](references/vhs-terminal.md) | Terminal/CLI films |
| **Verification** | [verification.md](references/verification.md) | After every master, before "done" |
| **Audio** | [audio.md](references/audio.md) | Brief asks for music/SFX |

### Templates

| Template | When to Use |
|----------|-------------|
| [capture-cdp.md](references/templates/capture-cdp.md) | `.motion/capture.js` — zero-dep Chrome capture |
| [render-cli.md](references/templates/render-cli.md) | `.motion/render.js` + `encode.js` — stages, encoders, verification |
| [timeline-seek.md](references/templates/timeline-seek.md) | The scene split into classic scripts (`lib.js` → `beats.js` → blocks → `timeline.js`): springs ζ ≥ 0.85, `springSum`, `stagger`, `validateDensity` (0.75 s / 1.2 s / 1 per s), the recurring actor, a flat CSS 3D cube; or the dense 2D-canvas scene |
| [interaction-kit.md](references/templates/interaction-kit.md) | One continuous object driven by a cursor: dual-edge springs, click/drag with spring-back, `swapBlur` (≤ 0.1 s, ≤ 8 px), loop seam check |
| [webgl-scene.md](references/templates/webgl-scene.md) | A lit three.js beat: pinned local three r186, SwiftShader, twice-rendered sha256 proof or CSS 3D fallback |
| [index-skeleton.md](references/templates/index-skeleton.md) | `.motion/scene/index.html` mechanics — stage = VIEW, kill-switch, local fonts, hidden shots, actor, rule, CSS 3D cube, script order |
| [vhs-tape.md](references/templates/vhs-tape.md) | Terminal film: tape + scripted demo |

---

## Best Practices

### DO
- Render stills twice when touching the scene's clock: the contact sha256 must not change
- Put hard cuts on frame boundaries (`t = k / FPS`) so a cut lands on the same frame at every rate and in every chunk
- Use `--jobs` past ~25 s; frames keep a global index
- Run the `motion-review` pack (spikes, phone view) on the draft and the master
- Report renders per stage, wall time, sizes vs budgets, SSIM and spikes

### DON'T
- Capture the preview loop or record the screen in real time
- Add motion blur to stills or the draft — master only, `--subframes` (4 default, ≥ 12 if any move > ~2 % W/frame — encoding.md), cuts on frame boundaries
- Ship a lit WebGL beat without the twice-rendered sha256 proof, or load three from a CDN at render time
- Build a crossfade or dissolve, or an opacity-only entrance — banned (`motion-craft` anti-slop-video.md)
- Write a scene file over the hook ceiling `FUSE_SOLID_MAX_LINES` — split it into another classic script
- Leave frame 0 blank or fading in — `seek(0)` shows the opening statement at full value
- Add a "reported" Chrome flag without the twice-rendered hash test
- Lower the SSIM threshold to make a master pass — investigate the change
- Commit `.motion/work/` frames or Chrome profiles
- Use Remotion as a dependency (license — mention it only as an alternative)
- Copy design-motion's UI micro-durations into film holds — films use `motion-craft` holds
