---
name: motion-background
description: This skill should be used when the user asks to "add an animated background", "build a mesh/gradient background", "make an aurora/shader background", "add constellation/particle background", "animated hero background", or "a subtle looping background behind content". Covers CSS mesh gradients, GLSL shader gradients (Three.js), canvas particle constellations, seamless loops, and reduced-motion/performance handling — fully self-contained.
version: 0.1.0
---

# Motion Background

Ambient, living backgrounds that sit behind content without stealing focus. The goal is subtle, seamlessly looping motion that stays readable and performant. This skill is self-contained: every technique below ships its own runnable code — CSS, GLSL, and canvas — with no external dependencies beyond Three.js where a shader is involved.

## When to use

- Hero/landing background that subtly moves; section ambience.
- Login/splash/empty-state living backdrops.
- A gradient, mesh, aurora, shader, or particle/constellation field behind text or UI.

## Pick an approach

| Look | Technique | Cost |
|---|---|---|
| Soft animated gradient/mesh | CSS gradients + keyframes | Cheapest, no JS |
| Flowing aurora / organic noise | GLSL fragment shader (Three.js full-screen quad) | GPU, moderate |
| Constellation / drifting dots | Canvas 2D particles | CPU, scales with count |
| Depth / parallax | Same shader/particles with mouse-driven offset | Moderate |

Default to CSS if a gradient suffices — it is the cheapest and most reliable. Use a shader for organic flowing color; use canvas particles for a constellation/network look.

## Design rules

- **Subtle**: low contrast versus content, slow motion (long periods, 8–30s loops), nothing that competes with text.
- **Readable**: keep contrast for foreground text; add a scrim (`linear-gradient` overlay or `backdrop`) if needed.
- **Seamless loop**: drive motion with periodic functions so time wraps with no visible jump (see below).
- **Respect motion preferences and battery**: honor `prefers-reduced-motion`, and pause when offscreen or the tab is hidden.

## Core techniques (inlined, runnable)

### 1. Animated CSS mesh gradient (no JS)

Layered radial gradients whose positions drift. Animating `background-position` on a larger-than-viewport gradient loops seamlessly.

```css
.bg {
  position: fixed; inset: 0; z-index: -1;
  background:
    radial-gradient(40% 50% at 20% 30%, #5b8cff55, transparent 60%),
    radial-gradient(45% 55% at 80% 20%, #b05bff55, transparent 60%),
    radial-gradient(50% 60% at 50% 80%, #2de1c255, transparent 60%),
    #0b0e1a;
  background-size: 200% 200%;
  animation: meshmove 24s ease-in-out infinite;
}
@keyframes meshmove {
  0%, 100% { background-position: 0% 0%, 100% 0%, 50% 100%; }
  50%      { background-position: 30% 20%, 70% 30%, 60% 70%; }
}
@media (prefers-reduced-motion: reduce) {
  .bg { animation: none; }
}
```

The `0%` and `100%` keyframes are identical, so the loop has no seam.

### 2. Full-screen GLSL gradient + noise shader (Three.js)

A flowing aurora/gradient using value noise in a fragment shader on a full-screen plane. `uTime` advances each frame; to loop, feed it a wrapped time (section 4).

```js
import * as THREE from 'three';

const canvas = document.querySelector('#bg');
const renderer = new THREE.WebGLRenderer({canvas, antialias: true});
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // cap for perf
const scene = new THREE.Scene();
const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);

const uniforms = {
  uTime: {value: 0},
  uRes: {value: new THREE.Vector2()},
  uColorA: {value: new THREE.Color('#5b8cff')},
  uColorB: {value: new THREE.Color('#b05bff')},
};

const material = new THREE.ShaderMaterial({
  uniforms,
  vertexShader: `void main(){ gl_Position = vec4(position, 1.0); }`,
  fragmentShader: `
    precision highp float;
    uniform float uTime; uniform vec2 uRes;
    uniform vec3 uColorA, uColorB;

    // hash + value noise
    float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1,311.7)))*43758.5453); }
    float noise(vec2 p){
      vec2 i = floor(p), f = fract(p);
      float a = hash(i), b = hash(i+vec2(1,0));
      float c = hash(i+vec2(0,1)), d = hash(i+vec2(1,1));
      vec2 u = f*f*(3.0-2.0*f);
      return mix(mix(a,b,u.x), mix(c,d,u.x), u.y);
    }
    float fbm(vec2 p){
      float v=0.0, a=0.5;
      for(int i=0;i<5;i++){ v += a*noise(p); p*=2.0; a*=0.5; }
      return v;
    }
    void main(){
      vec2 uv = gl_FragCoord.xy / uRes.xy;
      float n = fbm(uv*3.0 + vec2(uTime*0.05, uTime*0.03));
      vec3 col = mix(uColorA, uColorB, smoothstep(0.2, 0.8, n + uv.y*0.3));
      gl_FragColor = vec4(col, 1.0);
    }`,
});

const quad = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), material);
scene.add(quad);

function resize(){
  renderer.setSize(window.innerWidth, window.innerHeight);
  uniforms.uRes.value.set(window.innerWidth, window.innerHeight);
}
window.addEventListener('resize', resize); resize();

const clock = new THREE.Clock();
let running = true;
function loop(){
  if (running){
    uniforms.uTime.value = clock.getElapsedTime();
    renderer.render(scene, camera);
  }
  requestAnimationFrame(loop);
}
loop();
```

### 3. Canvas constellation particles

Drifting points connected by lines when near — the classic "network" background. Pure canvas 2D, no dependencies.

```js
const canvas = document.querySelector('#stars');
const ctx = canvas.getContext('2d');
let W, H, pts;
const COUNT = 80, LINK = 120;

function init(){
  W = canvas.width = innerWidth; H = canvas.height = innerHeight;
  pts = Array.from({length: COUNT}, () => ({
    x: Math.random()*W, y: Math.random()*H,
    vx: (Math.random()-0.5)*0.3, vy: (Math.random()-0.5)*0.3,
  }));
}
addEventListener('resize', init); init();

function frame(){
  ctx.clearRect(0, 0, W, H);
  for (const p of pts){
    p.x += p.vx; p.y += p.vy;
    if (p.x<0||p.x>W) p.vx*=-1;
    if (p.y<0||p.y>H) p.vy*=-1;
    ctx.fillStyle = '#9db4ff'; ctx.fillRect(p.x, p.y, 2, 2);
  }
  for (let i=0;i<COUNT;i++) for (let j=i+1;j<COUNT;j++){
    const dx=pts[i].x-pts[j].x, dy=pts[i].y-pts[j].y;
    const d=Math.hypot(dx, dy);
    if (d<LINK){
      ctx.strokeStyle = `rgba(157,180,255,${1-d/LINK})`;
      ctx.beginPath(); ctx.moveTo(pts[i].x,pts[i].y); ctx.lineTo(pts[j].x,pts[j].y); ctx.stroke();
    }
  }
  requestAnimationFrame(frame);
}
frame();
```

The O(n²) link loop is fine to ~120 points; above that, spatial-hash into a grid and only test neighboring cells.

### 4. Seamless loop technique

For canvas/JS, wrap time into a fixed period so motion repeats exactly. Use the loop *phase* (0→2π) as the argument to periodic functions:

```js
const PERIOD = 12; // seconds
const phase = (t % PERIOD) / PERIOD * Math.PI * 2;
const offset = Math.sin(phase) * amp;          // returns to start at t = PERIOD
```

Any motion built only from `sin`/`cos` of `phase` (or integer multiples) loops seamlessly. In the shader, feed `uTime = phase` and use only `sin`/`cos` of it; for noise-scrolled gradients, scroll by an integer number of noise cells per period so the field tiles.

### 5. Reduced motion + offscreen/hidden pause

```js
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
if (reduce) {
  running = false;                 // render one static frame, then stop
  renderer.render(scene, camera);
}

// Pause when the tab is hidden
document.addEventListener('visibilitychange', () => {
  running = !document.hidden && !reduce;
});

// Pause when the canvas scrolls offscreen
new IntersectionObserver(([e]) => {
  running = e.isIntersecting && !document.hidden && !reduce;
}).observe(canvas);
```

When `running` is false, skip the render inside the rAF loop (as in section 2) — the loop stays alive to resume cheaply, but does no GPU/CPU work.

## Deliver & verify (standalone HTML)

> **Packaged helper** (`scripts/`): `scripts/seek-shot.sh anim.html 0 1.5 3` freezes the `?t=N` harness and screenshots each moment; `scripts/contact-sheet.sh sheet.png frame-*.png` tiles them for one-glance review. See `scripts/README.md`.

A motion background ships as **one `.html` file that opens directly in a browser** — markup, the background, and (for shader/canvas) Three.js or canvas JS from CDN, all inline. One file is the right tier.

**Output contract:**
- One `.html` file: the background layer + a sample of foreground text on top to check readability/contrast.
- One animation driver — the CSS `@keyframes`, the shader rAF loop, or the canvas rAF loop; just one.
- Include the freeze harness below, matched to the technique, so any moment can be screenshotted deterministically.

**Freeze harness — pin a frame for screenshots.** Match the mechanism to the technique:

```html
<script>
  const t = new URLSearchParams(location.search).get("t");
  if (t !== null) {
    const T = parseFloat(t);
    // CSS mesh gradient:
    document.querySelectorAll(".bg").forEach(el => {
      el.style.animationDelay = (-T) + "s";
      el.style.animationPlayState = "paused";
    });
    // GLSL shader instead? → render exactly one frame at fixed time:
    //   uniforms.uTime.value = T; renderer.render(scene, camera); running = false;
    // Canvas particles? → seed deterministically, step the sim to T, draw once, stop the loop.
  }
  window.__ready = true;                                          // ready signal for headless wait
</script>
```

**Verify loop — render → freeze → screenshot → check:**
1. Open the file frozen at start / mid / end across one loop period: `…/bg.html?t=0`, `?t=<period/2>`, `?t=<period>`.
2. Screenshot each frozen frame.
3. Check **fidelity** (subtle, on-brand, seamless) and **artifacts** — text contrast holds at every frame, no banding in gradients/shader, the loop seam (`t=0` vs `t=period`) matches, no GPU/console errors.

```bash
npx playwright screenshot --wait-for-timeout=600 "file://$PWD/bg.html?t=12" frame-mid.png
```

**Before you finish:**
1. Opens standalone in a browser — no console/WebGL errors, no missing CDN.
2. One driver; `?t=N` freezes the exact frame (shader renders one frame, canvas sim stepped deterministically).
3. Screenshotted at start / mid / end — foreground text stays readable, no banding, loop seam invisible.
4. `prefers-reduced-motion` honored (one static frame rendered, loop stopped) + pauses offscreen/hidden.
5. `devicePixelRatio` capped at 2; motion is slow and subtle, never out-contrasting content.

## Quick reference

| Need | Do |
|---|---|
| Cheapest gradient | CSS layered `radial-gradient` + `background-position` keyframes |
| Organic flow | GLSL `fbm` noise, scroll `uTime` |
| Network/dots | canvas particles + distance-linked lines |
| No seam | drive motion by `sin/cos(phase)`, identical first/last keyframe |
| Perf cap | `setPixelRatio(min(dpr, 2))`, throttle, reduce particle count on mobile |
| Accessibility | `prefers-reduced-motion` static fallback |
| Save battery | pause on `visibilitychange` + `IntersectionObserver` |

## Gotchas

- Never let the background out-contrast the foreground text — add a scrim if it does.
- Uncapped `devicePixelRatio` on retina/4K murders the GPU; cap at 2.
- `background-position` loops only if first and last keyframes match exactly.
- Noise-scrolled shaders loop only if the scroll is an integer number of cells per period; otherwise the loop visibly jumps.
- Forgetting the offscreen/hidden pause drains battery on mobile even when the user can't see it.

## Reference files

- `references/background-recipes.md` — fuller drop-in implementations: a richer multi-blob CSS mesh with blur, the complete Three.js aurora shader with mouse parallax and a true seamless-loop time wrap, a grid-optimized constellation field with mouse repulsion, a perfectly-looping noise-flow technique, and a complete reduced-motion + offscreen-pause manager wrapping all of them.
