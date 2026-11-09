---
name: create-game-vfx
description: Design reusable game effects, stage versioned VFX packages, and review their timing, readability, rights, budgets and accessibility. Use for individual effects or effects coordinated with model actions.
engines: [AGNOSTIC]
---

# Create Game Vfx

## When to use

- Adding feedback for a gameplay event or state.
- Building sprite, particle, shader, mesh, trail, or screen-space effects.
- Reviewing VFX for readability, timing, accessibility, or runtime cost.

## Workflow

For reusable assets, read [versioned-vfx-assets.md](references/versioned-vfx-assets.md) and use `./commands/vfx-assets.sh`. Start with a task-bound brief and rights evidence, inspect prerequisites, stage inexpensive provisional work, and obtain a current independent complete-phase review before detailed work. Preserve immutable inputs, rejected attempts and version ancestry. The command validates packages through Bubo; it does not create a STYLE primary, select another engine, install dependencies or grant generation or asset promotion.

Check actual capabilities before promising production. Use native bounded preparation for owned/licensed PNG sheets, ordered sequences and typed masks. The THREEJS bridge supplies nine bounded layer families and a review-scene attachment; it requires exact host-admitted libraries, decoded resource correspondence and actual target captures. MODEL_TO_ACTION v2 schedules reviewed reusable effects with real exported clips through one shared Scene clock. Read `./.hephaera/docs/MODEL_TO_ACTION.md` for source-export admission, explicit endpoint/outcome policies, tails and native receiving gates. V1 retains its original cues and primitive behavior. Generated-receipt admission and video decoding remain unavailable. Standalone VFX staging grants no promotion; native action promotion still requires current technical, independent and separate human runtime acceptance. A valid package does not establish rendered quality.

For effects timed across a dance, combination or charge/cast sequence, coordinate with `build-model-actions`. Bind cues to real reviewed step/clip markers and anchors, capture fixed target points explicitly, and keep cancellation/resource cleanup separate from gameplay hit and projectile decisions.

For THREEJS, particle production uses the engine-selected `threejs-build-particles` Quarks owner and host-locked compatible packages. Missing dependencies or an unsupported renderer require direction; do not silently substitute native point primitives or install another backend. Other engine owners remain unchanged.

1. Define the gameplay event, audience, visibility distance, camera, duration, priority, and success signal.
2. Break the effect into anticipation, activation, impact, sustain, and release as applicable.
3. Assign shape, color, motion, scale, depth, audio, camera, and UI layers without duplicating feedback.
4. Resolve the active engine and compatible material/animation feature skills through `resolve-skill.sh`; define pool, allocation, overdraw, light, particle, and texture budgets. This agnostic VFX workflow does not authorize another engine's APIs or select a different art pipeline.
5. Author reduced-flash, reduced-motion, contrast and color-independent alternatives that preserve essential cues. Capture and review them with the real action and camera; emission scaling alone does not establish accessible readability.
6. Validate timing against authoritative gameplay events and test cleanup under repeated activation.
7. Define the effect's clock, cancellation owner, overlap/intensity cap, and expiration under pause, focus loss, scene exit, and prediction correction. Coordinate its layer with camera, sound, HUD, and optional haptics through the gameplay-feedback owner; a visual impact is not a tactile effect.

When reviewing a set of concurrent effects, name the competing cue meanings and which must remain legible. At the declared gameplay camera and concurrency, check whether routine effects obscure the important cue's origin, affected region or timing, including the authored accessibility variants. Use existing complete captures where they cover that case; missing coverage stays open. Record the obstructing layer and correction rather than inventing a universal effect-count threshold, automatic visibility metric or gameplay outcome.

When a staged effect is authored or simulated in Blender, use `simulate-blender-effects` for deterministic solver and cache ownership before this skill defines runtime timing, pooling, and gameplay validation.

Read [vehicle-speed-and-warp.md](references/vehicle-speed-and-warp.md) for motion-package anchors, continuous travel effects, warp phases and cancellation. Use `build-model-animations` for the model/motion package; this skill owns the selected-engine effects and their runtime evidence.

## Output

- A VFX timing and layer brief.
- Runtime asset, budget, pooling, accessibility, and fallback requirements.
- Representative gameplay and stress-test acceptance criteria.

## Guardrails

- Do not let VFX timing decide authoritative hits or state.
- Do not obscure hazards, targets, UI, or player silhouettes.
- Do not create unbounded particles, lights, allocations, or screen flashes.
