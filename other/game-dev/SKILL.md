---
name: game-dev
description: Use when building browser games, simulations, shader art, GPU particle systems, physics sandboxes, procedural generation, or other interactive canvas/WebGL/WebGPU artifacts. Also use for requests like "make a game," "build a simulation," "particle effects," "fluid dynamics," "generative art," or iterative web-game development and testing with Playwright.
---

# Game Dev (Web Sim Engine)

<!-- Merged from: develop-web-game (2026-04-05). Legacy material preserved under merged/. -->

> Build production-quality browser games, simulations, GPU particle systems, physics engines, and generative art — from simple Canvas 2D platformers to advanced WebGL2/WebGPU compute pipelines. Everything ships as a single-file HTML artifact.

## Claude.ai Artifact Constraints

When outputting as a claude.ai artifact (`.html` or `.jsx` file), these hard constraints apply:

**HTML Artifacts:**
- Single-file only. All CSS, JS, shaders inline. No external files except CDN imports.
- **No `localStorage` or `sessionStorage`** — these APIs are blocked in the artifact iframe sandbox. Use in-memory state (JS variables/objects) or `window.storage` (Anthropic's persistent storage API) instead.
- CDN imports allowed from `cdnjs.cloudflare.com` only. Three.js r128, D3, etc.
- Canvas, WebGL2, and WebAudio all work inside the artifact iframe.
- WebGPU may not be available — always include feature detection and WebGL2 fallback.
- The artifact iframe is sandboxed: no popups, no navigation, no top-level access.
- Use `100dvh` / `100dvw` for full-bleed layouts. The iframe handles sizing.

**React/JSX Artifacts:**
- Use only Tailwind core utility classes (no compiler available).
- Available libraries: `react`, `lucide-react@0.263.1`, `recharts`, `mathjs`, `lodash`, `d3`, `plotly`, `three` (r128), `papaparse`, `sheetjs`, `shadcn/ui`, `chart.js`, `tone`, `mammoth`, `tensorflow`.
- Default export required, no required props.

**Choosing HTML vs JSX:**
- **HTML** for anything using Canvas, WebGL, WebGPU, or raw shader code (games, simulations, generative art).
- **JSX** for UI-heavy interactive tools, dashboards, or data visualizations using React + Tailwind.
- When in doubt for games/simulations, use HTML.

## Always-On Rules

1. **Fixed timestep is non-negotiable.** Decouple physics (60Hz fixed) from rendering (variable + interpolation). Without this, physics breaks on 120Hz+ monitors and backgrounded tabs cause spiral-of-death. See `assets/simulation-base.html` for the canonical loop.
2. **Data-Oriented Design.** Structure-of-Arrays with `Float32Array`, object pooling, swap-and-pop removal. GC pauses (V8: 10-100ms+) are the #1 source of jank.
3. **Spatial hash for broadphase.** O(1) average lookup, minimal allocation, scales to 20k+ entities. Brute force is fine under ~100 objects. Quadtrees are rarely worth it in JS.
4. **Ping-pong buffers for GPU sims.** Whether particles (Transform Feedback), fluids (FBO textures), reaction-diffusion, or cellular automata — two buffers swapped each frame is the universal pattern.
5. **WebGL2 first, WebGPU for compute.** Ship WebGL2 for rendering compatibility. Use WebGPU only when compute shaders provide meaningful gains (>100k particles, fluid sim, XPBD). Always include feature detection.
6. **No magic numbers.** Expose physics constants, spawn rates, force magnitudes as clearly named top-level `const` values. Makes tuning possible.

## Performance Tier Hierarchy

| Tier | Technology | Typical Ceiling | Use When |
|------|-----------|----------------|----------|
| 1 | CPU JS (Canvas 2D) | ~10k-50k particles | Simple games, <100 physics bodies |
| 2 | Rust/WASM (Rapier) | 5k-10k rigid bodies @ 60fps | Serious rigid body physics |
| 3 | WebGL2 GPGPU | ~1M-4M particles | Particle systems, shader sims |
| 4 | WebGPU Compute | ~10M-30M+ particles | Fluid sim, massive particles, XPBD |

## Routing Table

Read relevant reference files based on task type. Multiple files often apply.

| Task Type | Load These References |
|---|---|
| **Any simulation/game** | `references/game-loop-and-architecture.md` (always) |
| **Simple 2D Canvas games (platformers, top-down, puzzle)** | `references/game-patterns.md`, `references/responsive-design.md` |
| **Canvas 2D performance / mobile optimization** | `references/performance.md` |
| **Responsive design / DPR / touch / mobile** | `references/responsive-design.md` |
| **Collision detection / rigid body physics** | `references/collision-and-physics.md` |
| **GPU particle systems / force fields** | `references/gpu-particles.md` |
| **WebGL2 rendering / shaders / post-processing** | `references/shaders-and-rendering.md` |
| **Generative art (reaction-diffusion, fractals, noise)** | `references/generative-art.md` |
| **Fluid dynamics / soft bodies / cloth** | `references/fluids-and-softbody.md` |
| **Game feel / juice / polish** | `references/game-feel-and-juice.md` |
| **AI, pathfinding, procedural generation** | `references/ai-and-pcg.md`, `references/game-patterns.md` |
| **Mobile, audio, accessibility, shipping** | `references/mobile-audio-shipping.md` |
| **WebGPU compute pipelines** | `references/webgpu-patterns.md` |

## Feedback Loop

This skill uses a feedback log to improve over time. The cycle:

1. **Detect** — After completing a task using this skill, note anything that went wrong, was suboptimal, or could be improved (bad defaults, missing patterns, unclear instructions, broken templates, missing reference coverage).
2. **Search** — Check `FEEDBACK.md` for prior entries on the same topic to avoid duplicates.
3. **Scope** — Keep the feedback entry to 1–3 lines: category tag, what happened, what should change.
4. **Draft & Ask** — Draft the feedback entry and show it to the user before writing.
5. **Write on Approval** — Append the approved entry to `FEEDBACK.md`.
6. **Compact at 75** — When FEEDBACK.md reaches 75 entries, summarize and compact older entries to keep the file useful.

**Always read `FEEDBACK.md` when reading this skill.**

## Deep Reference System

The `references/deep/` folder contains the full research reports (~2000+ lines total across 10 files). These are **never auto-loaded**. The compressed reference files contain grep pointers like:

```
⤷ grep -A 80 "### Fixed Timestep" references/deep/run-01-game-engine-fundamentals.md
```

Run these grep commands **only when you need full implementation details** for a specific technique. The compressed references give enough context for most decisions.

### Deep Reference Files
| File | Contents |
|---|---|
| `deep/run-01-game-engine-fundamentals.md` | Game loop, ECS, SoA, object pools, spatial hash, state machines |
| `deep/run-02-collision-physics.md` | AABB, SAT, GJK, impulse resolution, Sequential Impulse, friction |
| `deep/run-03-rendering-sprites-vfx.md` | WebGL2 batching, sprite atlases, normal maps, bloom, tone mapping |
| `deep/run-04-realtime-physics-sim.md` | Rapier WASM, XPBD, MLS-MPM fluids, cloth, WebGPU physics |
| `deep/run-05-gpu-particles.md` | Transform Feedback, WebGPU compute particles, force fields, 10M+ |
| `deep/run-06-algorithmic-generative-art.md` | Noise, fBm, domain warping, reaction-diffusion, Physarum, fractals |
| `deep/run-07-webgl-glsl-shaders.md` | GLSL patterns, SDF, ray marching, FBO techniques, post-processing |
| `deep/run-08-game-feel-juice.md` | Screen shake, hit stop, coyote time, camera, feedback hierarchy |
| `deep/run-09-ai-pcg.md` | Behavior trees, utility AI, flow fields, A*, dungeon gen, WFC |
| `deep/run-10-shipping-platform.md` | Mobile, audio, accessibility, networking, performance profiling |

## Key Formulas (Always Available)

```
Impulse resolution:
j = -(1+e)(v_rel · n) / (1/m_a + 1/m_b + (r_a × n)²/I_a + (r_b × n)²/I_b)

Camera smoothing (frame-rate independent):
lerp(current, target, 1 - pow(damping, dt))

Trauma-based screen shake:
offset = noise(t) * max_distance * (trauma²)

Domain warping:
f(p) = fBm(p + fBm(p + fBm(p)))

Gray-Scott reaction-diffusion:
dA/dt = D_A·∇²A - A·B² + f·(1-A)
dB/dt = D_B·∇²B + A·B² - (k+f)·B

Smooth fractal coloring:
nu = n + 1 - log2(log|z|)
```

## Essential GLSL (Always Available)

```glsl
// Smooth SDF blending (metaballs, organic shapes)
float smin(float a, float b, float k) {
    float h = clamp(0.5 + 0.5*(b-a)/k, 0.0, 1.0);
    return mix(b, a, h) - k*h*(1.0-h);
}

// ACES filmic tone mapping
vec3 aces(vec3 x) {
    const float a=2.51, b=0.03, c=2.43, d=0.59, e=0.14;
    return clamp((x*(a*x+b))/(x*(c*x+d)+e), 0.0, 1.0);
}

// Anti-aliased SDF edge
float aa = fwidth(d);
float alpha = 1.0 - smoothstep(-aa, aa, d);
```

## Asset Templates

| Template | Use For |
|---|---|
| `assets/game-base.html` | Canvas 2D games — responsive setup, DPR, unified input, virtual canvas, pause/visibility |
| `assets/simulation-base.html` | Ping-pong FBO shader simulations (reaction-diffusion, fluids, cellular automata) |
| `assets/particle-base.html` | WebGL2 Transform Feedback particle systems with force fields |
| `assets/webgpu-compute-base.html` | WebGPU compute + render pipeline with WebGL2 fallback detection |

Copy the appropriate template to `/home/claude/`, customize, then move final to `/mnt/user-data/outputs/`.

## Utility Scripts

Production-ready JS utilities in `scripts/` — inline into your single-file artifact as needed:

| Script | Provides |
|---|---|
| `scripts/physics.js` | AABB/circle collision, MTV resolution, swept AABB (anti-tunneling) |
| `scripts/spatial-hash.js` | Broad-phase spatial hash (O(1) lookup, >50 entities) |
| `scripts/input.js` | Unified Pointer Events input manager (mouse/touch/pen) |
| `scripts/pool.js` | Object pooling (particles, bullets — zero GC) |
| `scripts/ecs.js` | Minimal Entity-Component System with typed queries |
| `scripts/animator.js` | Frame-based sprite animation |

## Output Principles

- **Artifacts:** Single-file HTML. All shaders inline as `<script type="x-shader/...">` or template literals. All utility code inlined (don't reference external script files).
- **CDN imports:** Three.js r128 from `cdnjs.cloudflare.com`. D3 from cdnjs. No npm in artifacts.
- **State storage:** Use JS variables/objects. Never `localStorage`/`sessionStorage` (blocked in artifact iframe). For persistence across sessions, use `window.storage` API if needed.
- **WebGPU detection:**
  ```javascript
  if (navigator.gpu) { /* WebGPU path */ } else { /* WebGL2 fallback */ }
  ```
- **Font loading:** Google Fonts `<link>` when UI labels needed.
- **Visual themes:** For simulation aesthetics, reference the user's visual themes in `design-maestro` skill's `references/themes.md` or the `design-extraction` skill.
- **Game feel:** Layer juice on last, not first. Get the simulation correct, then add screen shake / particles / trails.
- **Responsive:** Use virtual canvas pattern for games (see `assets/game-base.html`). Use `100dvh`/`100dvw` for fullscreen sims.

## Complexity Routing

Choose the right tier for the request:

| Request | Approach |
|---|---|
| Simple 2D game (platformer, top-down, puzzle) | Canvas 2D + `game-base.html` template + utility scripts |
| Game with particle effects / post-processing | Canvas 2D game logic + WebGL2 for effects |
| Physics sandbox / rigid body sim | CPU physics (<100 bodies) or Rapier WASM (>100) |
| GPU particle system / shader art | WebGL2 Transform Feedback or fragment shader |
| Fluid sim / massive particles / XPBD | WebGPU compute with WebGL2 fallback |
| Generative art (noise, fractals, reaction-diffusion) | Fragment shader (WebGL2) for most; compute shader for cellular automata |

## Quick Start (Canvas 2D Games)

For simple 2D games (platformers, top-down, puzzle), follow this workflow:

1. Copy `assets/game-base.html` to `/home/claude/`
2. Customize game logic in `fixedUpdate()` and `render()`
3. Inline any needed utility scripts from `scripts/`
4. Test responsive behavior (desktop/tablet/mobile)
5. Move final game to `/mnt/user-data/outputs/`

The `game-base.html` template includes: fixed timestep game loop, DPR-aware responsive canvas, unified input handling, pause/resume system, and Page Visibility handling.

## Common Patterns

### State Management

```javascript
const STATES = { MENU: 0, PLAYING: 1, PAUSED: 2, GAME_OVER: 3 };
let gameState = STATES.MENU;

function fixedUpdate(dt) {
  switch (gameState) {
    case STATES.PLAYING:
      // Game logic
      break;
    case STATES.PAUSED:
      // Don't update
      break;
  }
}
```

### Scene Switching

```javascript
class Scene {
  init() {}
  enter() {}
  exit() {}
  update(dt) {}
  render(ctx) {}
}

const scenes = {
  menu: new MenuScene(),
  game: new GameScene(),
  gameover: new GameOverScene()
};

let activeScene = scenes.menu;
function switchTo(key) {
  activeScene.exit();
  activeScene = scenes[key];
  activeScene.enter();
}
```

## Best Practices

### Performance
1. Use object pooling for frequently created/destroyed objects
2. Spatial hash for broad-phase when you have many objects (>50)
3. Limit particles — cap at 200-500 max on mobile
4. Render static backgrounds once to an offscreen canvas
5. Profile on real devices — Chrome DevTools with 4x CPU throttle

### Mobile
1. Support both orientations or lock appropriately
2. Use safe area insets for notches (see `references/responsive-design.md`)
3. Minimum touch target: 44pt (about 44px at 1x)
4. Pause when tab hidden (Page Visibility API)
5. Offer 30fps mode for battery/thermal management

### Physics
1. Use fixed timestep (never variable dt for physics)
2. Resolve Y before X for platformers (better feel)
3. Use swept AABB for fast movers (>4 pixels per frame)
4. Clamp velocities to prevent tunneling

### Audio
1. Resume AudioContext on first user gesture
2. Use AudioBuffer (decode once, play many times)
3. Pool gain nodes for sound effects
4. Mute when tab hidden

## Playwright Test Harness

For iterative game development with automated testing (especially when building in a local dev environment rather than as a claude.ai artifact), use the Playwright-based test harness:

### Setup

```bash
export WEB_GAME_CLIENT="$HOME/.codex/skills/game-dev/merged/develop-web-game/scripts/web_game_playwright_client.js"
export WEB_GAME_ACTIONS="$HOME/.codex/skills/game-dev/merged/develop-web-game/references/action_payloads.json"
```

Verify Playwright is available: `command -v npx >/dev/null 2>&1`

### Required game hooks

For automated testing to work, expose these two hooks in the game:

**1. `window.render_game_to_text()`** — returns a concise JSON string of current game state:

```js
window.render_game_to_text = () => JSON.stringify({
  mode: state.mode,
  player: { x: state.player.x, y: state.player.y },
  entities: state.entities.map(e => ({ x: e.x, y: e.y })),
  score: state.score,
});
```

**2. `window.advanceTime(ms)`** — deterministic frame stepping:

```js
window.advanceTime = (ms) => {
  const steps = Math.max(1, Math.round(ms / (1000 / 60)));
  for (let i = 0; i < steps; i++) update(1 / 60);
  render();
};
```

### Running the test script

```bash
node "$WEB_GAME_CLIENT" \
  --url http://localhost:5173 \
  --actions-file "$WEB_GAME_ACTIONS" \
  --click-selector "#start-btn" \
  --iterations 3 \
  --pause-ms 250
```

Inline JSON actions (no file needed):

```json
{
  "steps": [
    { "buttons": ["left_mouse_button"], "frames": 2, "mouse_x": 120, "mouse_y": 80 },
    { "buttons": [], "frames": 6 },
    { "buttons": ["right"], "frames": 8 },
    { "buttons": ["space"], "frames": 4 }
  ]
}
```

### Test loop workflow

1. **Implement** the smallest change that moves the game forward.
2. **Run** the Playwright client after each meaningful change.
3. **Inspect** screenshots — open and visually verify, don't just generate them.
4. **Check** `render_game_to_text` output matches what's on screen.
5. **Review** console errors — fix the first new error before continuing.
6. **Reset** between distinct scenarios to avoid cross-test state pollution.
7. **Iterate** — change one variable at a time, then repeat.

**Test coverage:** primary movement/interaction inputs, win/lose transitions, score/health changes, boundary collisions, menu/pause flow, and any special actions tied to the request.

**Progress tracking:** Use a `progress.md` file to record the original prompt, TODOs, gotchas, and notes so another agent can continue seamlessly.

## Testing Checklist

### Functionality
- Game loop runs at stable framerate
- All controls respond correctly
- Collision detection works (no tunneling)
- Audio plays after user gesture
- Pause/resume works properly

### Responsive Design
- Works on mobile (320px width)
- Works on tablet (768px width)
- Works on desktop (1920px width)
- Maintains aspect ratio on all screens

### Mobile Specific
- Touch controls work (if applicable)
- Runs smoothly on mobile device
- No scroll/zoom interference
- Respects safe area insets
- Pauses when tab hidden

## Troubleshooting

**Game stutters or lags:** Check frame budget with `console.time/timeEnd`. Enable object pooling. Use spatial hash for broad-phase. Reduce particle count. Profile with Chrome DevTools Performance tab.

**Objects tunnel through walls:** Use swept AABB for fast-moving objects (see `scripts/physics.js`). Clamp maximum velocities. Reduce timestep to 1/120. Check collision order (Y before X for platformers).

**Touch controls don't work:** Verify `touch-action: none` on canvas. Use Pointer Events (not Touch Events). Check `e.preventDefault()`. Test `setPointerCapture`.

**Canvas is blurry on high-DPI:** Ensure canvas backing size = CSS size × devicePixelRatio. Scale context with `ctx.setTransform(dpr, 0, 0, dpr, 0, 0)`.

**Audio doesn't play on mobile:** Resume AudioContext on user gesture. Check autoplay policies. Use AudioBuffer, not HTMLAudioElement. Test on actual device.

## Relationship to Other Skills

- **`algorithmic-art-enhanced`** — Use for p5.js generative art with seeded randomness. Use *this* skill for WebGL/WebGPU shader-based generative art (reaction-diffusion, fractals, Physarum, fluid art).
- **`design-maestro`** / **`design-extraction`** — Reference for simulation aesthetics and UI polish.
