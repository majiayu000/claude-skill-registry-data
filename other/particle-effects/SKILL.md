---
name: particle-effects
description: |
  Generate master-level particle effects for web projects using Three.js, Canvas 2D, WebGL, or WebGPU.
  Translates visual intent into precise, production-quality implementations with correct physics,
  rendering, and the aesthetic judgment of top creative studios (Lusion, Active Theory level).
  Use when: "particle effect", "particles", "particle system", "floating dots", "background animation",
  "mouse trail", "dissolve effect", "smoke effect", "galaxy animation", "text morphing particles",
  "hover burst", "scroll reveal particles", "radial pulse", "fluid simulation", "physics sandbox",
  "ambient background", "point cloud", "particle playground", or any request involving animated dots,
  sprites, or procedural motion effects on a webpage. Also use when the user describes a visual effect
  that involves many small moving elements, even if they don't use the word "particle" — e.g.,
  "I want sparkles following the cursor", "floating dust", "stars in the background",
  "text that breaks apart", "confetti explosion", "smoke wisps".
---

# Particle Effects

Generate particle effects that belong on an Awwwards-winning site, not a CodePen demo.

The gap between amateur and master is not the algorithm — it is the details: color harmony,
motion weight, layered depth, and restrained post-processing. This skill encodes the judgment
of studios like Lusion and artists like Robert Hodgin (flight404), Inigo Quilez, and Yuri Artiukh
directly into the workflow so every output meets a professional bar.

Before writing any code, read `references/mastery.md` — it contains the quality principles that
govern every decision below. Internalize those principles; they are not optional polish.

## Workflow

### Step 1: Identify the Pattern

Match the user's intent to one of 10 proven interaction patterns:

| # | Pattern | One-liner | Key Tech |
|---|---------|-----------|----------|
| 01 | **Ambient Background** | Slow-drifting atmospheric particles | simplex noise + point sprites + additive blending |
| 02 | **Mouse Trail** | Cursor leaves a particle wake | emitter at cursor + velocity inheritance + alpha decay |
| 03 | **Image/Text Morph** | Image or text dissolves into / assembles from particles | canvas sampling + spring physics + noise scatter |
| 04 | **Hover Burst** | Particles explode from a button on hover | radial velocity + gravity + short lifetime |
| 05 | **Scroll Reveal** | Elements materialize via particles on scroll | IntersectionObserver + spring interpolation |
| 06 | **Radial Pulse** | Concentric rings of particles breathing outward | ring emitter + sin modulation + alpha falloff |
| 07 | **Galaxy / Spiral** | Rotating spiral arms of particles | log-spiral distribution + vortex + FBM noise |
| 08 | **Fluid / Smoke** | Organic flowing wisps | curl noise velocity field + soft blending + narrow color ramp |
| 09 | **Dissolve** | Object crumbles into drifting particles | mesh vertices + noise threshold + bloom edge |
| 10 | **Physics Playground** | Particles with real collisions & forces | N-body / spatial hashing + collision detection |

For full pattern details (parameters, variants, prompt examples), read `references/patterns.md`.

### Step 2: Choose the Tech Stack

| Scale | Recommended Stack | Why |
|-------|------------------|-----|
| < 1,000 particles | **Canvas 2D** | Simple, no deps, good for trails & bursts |
| 1,000 – 50,000 | **Three.js + Points/InstancedMesh** | Battle-tested, great ecosystem |
| 50,000 – 500,000 | **Three.js + GPGPU (FBO ping-pong)** | GPU-computed positions, CPU just renders |
| 500,000+ | **WebGPU compute shaders** | Native GPU compute, highest ceiling |
| React project | **React Three Fiber** | Three.js with React integration |

### Step 3: Design the Color

**Color is the #1 amateur tell.** Before writing physics, decide the palette.

1. **Never use pure colors.** No `#ffffff`, `#ff0000`, `#000000`. Tint everything.
   Background: `#08080f` or `#0a0a1a` (dark navy, not pure black).
   Whites: `#f0e6ff` or `#e8f4ff` (tinted, not stark).

2. **Build a 5-7 color palette** with weighted distribution:
   - 60% dominant mood color
   - 25% secondary color
   - 10% accent (contrasting temperature)
   - 5% highlight (near-white, tinted)

3. **Warm-cool contrast.** The best effects mix temperatures:
   cool blue base + warm gold accents, or warm orange flames + cool dark edges.
   Single-temperature palettes look flat.

4. **Color over lifetime.** Particles should shift color as they age — bright at birth,
   muted at death (or vice versa). This one technique adds more visual richness than
   any physics change. See `references/mastery.md` Section 1 for code patterns.

### Step 4: Build the Motion

**Every particle should move as if it has mass. Weightless motion looks fake.**

1. **Spring physics, not lerp.** Use `vel += (target - pos) * stiffness; vel *= damping`
   instead of `pos += (target - pos) * factor`. Springs have overshoot, settle, and weight.

2. **Multi-octave noise.** Never use a single noise layer — it looks mechanical.
   Layer 2-3 octaves with irrational frequency multipliers (2.13x, 4.37x) to avoid repetition:
   ```
   v += noise(p * freq, t) * amp
   v += noise(p * freq * 2.13, t * 1.37) * amp * 0.35
   v += noise(p * freq * 4.37, t * 1.71) * amp * 0.15
   ```

3. **Velocity inheritance.** When spawning from a moving source (cursor, scroll),
   particles must inherit the source's momentum. Without this, trails look placed, not emitted.

4. **Graceful birth and death.** Particles fade in over the first ~15% of life and
   fade out over the last ~30%. No popping.

5. **Choose damping to match weight:**
   - 0.85–0.90: heavy, viscous (underwater, thick smoke)
   - 0.91–0.95: natural, weighted (most effects — the sweet spot)
   - 0.96–0.99: light, floaty (space, zero-gravity, ambient)

6. **Never use Math.random() per frame for motion.** Use curl/simplex noise for organic flow.
   Random jitter ≠ organic movement.

For noise type selection, see `references/terminology.md` (Noise Types section).

### Step 5: Compose with Depth

**The space between particles is as important as the particles themselves.**

1. **Layer at multiple scales.** Use 2-3 layers, not one uniform field:
   - Background (15%): tiny, dim, slow — creates atmosphere
   - Mid (80%): standard — the main effect
   - Foreground (5%): large, bright, fast — creates depth illusion

2. **Size variation.** Never uniform. Use a distribution skewed toward small:
   `size = Math.exp(Math.random() * 1.2 - 0.3)` gives many small, few large.

3. **Respect negative space.** Professional work never fills the screen uniformly.
   Dense regions draw the eye; empty regions give it rest. Aim for 30-40% coverage
   on ambient effects; focal effects should have dense centers and sparse edges.

### Step 6: Apply Post-Processing

**Post-processing is not optional. It separates WebGL demo from shipped product.**

1. **Bloom (UnrealBloomPass):** Always include, but with restraint:
   - strength: **0.2–0.5** (not 1.0+)
   - threshold: **0.3–0.6** (only bright particles glow, not everything)
   - radius: **0.3–0.7** (tight, focused, not giant halos)

2. **Additive blending opacity rules** (the most common mistake):
   - Dense effects (smoke, galaxy): **0.05–0.15**
   - Medium effects (ambient, morph): **0.15–0.35**
   - Sparse effects (trails, bursts): **0.3–0.6**
   - If the output looks washed out / white, opacity is too high.

3. **Optional enhancements** for premium effects:
   - Depth of Field: blur distant particles
   - Chromatic aberration: subtle RGB offset at edges
   - Vignette: darken screen edges to focus attention

### Step 7: Wire the Controls

**lil-gui is a design tool, not a debug panel.**

1. Always include lil-gui (unless the user explicitly declines).
2. Group parameters into semantic folders: Emitter, Physics, Mouse, Rendering.
3. Name controls for the user, not the code: "Wind Strength" not "noiseAmplitude".
4. Include presets if the effect supports multiple moods:
   ```javascript
   const presets = {
     dreamy:    { noiseSpeed: 0.08, damping: 0.97, bloomStrength: 0.4 },
     energetic: { noiseSpeed: 0.3,  damping: 0.90, bloomStrength: 0.2 },
     minimal:   { noiseSpeed: 0.05, damping: 0.98, bloomStrength: 0.1 },
   };
   ```
5. Parameter changes must take effect immediately — no restart required.

### Step 8: Quality Gate

Before delivering, verify against these anti-patterns (the "deadly sins" of particle effects):

| Check | What to look for | Fix |
|-------|-----------------|-----|
| White-out | Dense areas burn to pure white | Lower opacity, raise bloom threshold |
| Uniform soup | All particles same size/speed/color | Add size variation, layering, palette weights |
| Linear motion | Constant speed, no acceleration | Use spring physics, easing, damping |
| Hard edges | Particles pop in/out instantly | Add fade in/out over first/last 15% of life |
| Noise jitter | Shaking instead of flowing | Use curl/simplex noise, not Math.random() |
| Screen stuffing | Particles everywhere, no rest | Reduce count, add negative space |
| Dead calm | Assembled particles perfectly still | Add very subtle noise idle drift (amp 0.002-0.005) |
| Missing GUI | Hard-coded magic numbers | Add lil-gui with grouped, named parameters |

**The bar is not "does it work." The bar is: would this look at home on a Lusion project page?**

## Quick Reference

- Full terminology dictionary (40+ terms): `references/terminology.md`
- All 10 patterns with parameters & prompt examples: `references/patterns.md`
- Libraries, tools, websites & classic cases: `references/resources.md`
- **Master-level principles & anti-patterns: `references/mastery.md`** ← read this first

## Universal Prompt Template

When the user's request is vague, fill in this brief before coding:

```
Pattern: [from the 10 patterns above]
Tech stack: [Three.js / Canvas 2D / WebGPU / R3F]
Particle count: [5K / 50K / 500K]
Interaction: [mouse repel / attract / trail / scroll / none]
Visual style: [dreamy soft / hard sci-fi / organic natural / minimal geometric]
Palette: [5-7 specific hex values with warm-cool contrast]
Noise: [curl / simplex / FBM / none] × [octave count]
Post-processing: [bloom settings + optional DOF/vignette]
GUI presets: [mood names and their parameter values]
```
