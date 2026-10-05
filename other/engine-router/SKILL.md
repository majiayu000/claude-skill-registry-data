---
name: engine-router
description: The platform router for the gamestack framework. Use when a game's design is ready to implement, when the target engine is chosen or needs choosing, or when handing off a spec to engine code — "build this in Godot/Unity/Unreal/Three.js", "which engine", "now implement it", "wire the design to code". Routes design phases to gamestack's foundation skills and implementation to the matching engine pack (godot, unreal, unity). Engine-agnostic itself; it decides where work goes.
---

# Engine Router

## Preamble (auto-loaded)

!`cat "${CLAUDE_PLUGIN_ROOT}/shared/PREAMBLE.md"; echo; cat "${CLAUDE_PLUGIN_ROOT}/ETHOS.md"`

> FALLBACK: if the line above rendered literally or empty (`disableSkillShellExecution`),
> Read `${CLAUDE_PLUGIN_ROOT}/shared/PREAMBLE.md` and `${CLAUDE_PLUGIN_ROOT}/ETHOS.md` now
> and **follow PREAMBLE.md as instructions**, then continue.

gamestack splits a game into two jobs: the **design brain** (engine-agnostic, first-party) and the **engine hands** (per-platform, the curated engine packs). This skill is the design→engine handoff — it consumes the finished design bible and sends implementation to whichever engine pack owns the target platform. It does **not** sequence design phases (that is `game-design-process`); it only routes a ready design to code.

The preamble has already detected the engine and loaded `${CLAUDE_PLUGIN_ROOT}/overlays/<engine>.md` — that overlay holds the spec→pack-skill mapping for this target. Use it as the translation table below.

## When to use this

- A design/spec is ready and it's time to write engine code
- Choosing a target engine, or supporting more than one
- Mid-build, deciding "is this a design question or an engine question?" and pulling the right skill

## The core stance

1. **Design once, implement per engine.** The world bible, systems, combat feel, and procgen rules from the foundation skills are engine-independent. Don't re-derive them inside an engine — translate them.
2. **Never put design logic in an engine skill, or engine APIs in a design skill.** If you're reaching for `Node`/`Actor`/`THREE.Scene` while still deciding *what interesting decision a system creates*, stop — that's a foundation question (`game-design-fundamentals`).
3. **One spec, one handoff artifact.** The design pipeline's output (specs, content, quality verdicts) is the contract the engine pack consumes. Engine choice never changes the spec.

## Routing table

| Phase / question | Layer | Skill to pull |
|------------------|-------|---------------|
| Concept, pillars, core loop, "is this an interesting decision?" | Foundation (design) | `game-design-fundamentals` |
| World structure, navigation, spatial pacing | Foundation (design) | `open-world-design` |
| Generating + reviewing content without sameness | Foundation (design) | `procedural-generation`, `procgen-review` |
| Combat & game feel (juice, telegraphing, encounters) | Foundation (design) | `combat-design` |
| Sequencing the whole design end to end | Foundation (process) | `game-design-process` |
| **Implement in Godot 4.x** (GDScript, systems, optimization, export) | Engine hands | `godot` pack (`/plugin install godot@gamestack`) |
| **Implement in Unreal** (C++ gameplay framework, rendering, networking) | Engine hands | `unreal` pack (`/plugin install unreal@gamestack`) |
| **Debug a Unity build** (logging, runtime commands, watching) | Engine hands | `unity-jahro` pack (`/plugin install unity-jahro@gamestack`) |
| **Implement in Unity (general authoring)** | Engine hands | ⬜ roadmap — no curated pack yet; use general C#/Unity knowledge + the foundation specs |
| **Implement in Three.js / web** | Engine hands | ⬜ roadmap — no curated pack yet; use the foundation specs + general Three.js knowledge |

## The handoff procedure

1. **Confirm the engine.** The preamble already detected it and loaded the overlay; if it had to ask, the answer is now in `./.gamestack/bible/engine`. Don't guess silently.
2. **Confirm the bible/spec exists.** Implementation consumes the design bible (`./.gamestack/bible/`). If it's empty or missing, route *back* to `game-design-process` first — don't improvise design inside engine code.
3. **Install / confirm the engine pack** for the target (per the loaded overlay). If the platform is a roadmap gap (Unity-general, Three.js), say so explicitly and fall back to the bible specs plus general engine knowledge — never silently pretend a pack exists.
4. **Translate, don't redesign.** Use the overlay's spec→pack-skill mapping: each `systems.md` / `world.md` entry maps to a named engine-pack skill. Design intent is fixed; only the implementation is engine-specific.
5. **Keep the loop closed.** Bugs in *feel* or *balance* go back to the foundation skill that owns them (and update the bible); bugs in *implementation* stay in the engine pack.

## The one rule

> **The spec is engine-independent; the code is engine-specific. This skill is the only place the two meet.** Cross-contaminate them and you'll be redoing design work in every engine you port to.

## Output

End with a completion status per the preamble protocol: **DONE** (engine confirmed, pack installed, spec→skill mapping handed off) / **DONE_WITH_CONCERNS** (e.g. a roadmap-gap engine) / **BLOCKED** / **NEEDS_CONTEXT** (e.g. empty bible — route back to `game-design-process`).
