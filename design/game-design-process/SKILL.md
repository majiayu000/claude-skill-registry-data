---
name: game-design-process
description: The orchestrator for designing a game end to end. Use when starting or steering a game's design — "I'm making a game", "where do I start", "design this game with me", "what's next in the design", or running headless to take a concept to generated, reviewed content. Engine-agnostic; tuned for procedural / AI-authored games (e.g. a procgen open-world RPG in Godot). Sequences the pipeline and names which knowledge/process skill to pull at each phase. Stops at design/spec — does not write gameplay code.
---

# Game-Design Process

## Preamble (auto-loaded)

!`cat "${CLAUDE_PLUGIN_ROOT}/shared/PREAMBLE.md"; echo; cat "${CLAUDE_PLUGIN_ROOT}/ETHOS.md"`

> FALLBACK: if the line above rendered literally or empty (your host has
> `disableSkillShellExecution` set), Read `${CLAUDE_PLUGIN_ROOT}/shared/PREAMBLE.md` and
> `${CLAUDE_PLUGIN_ROOT}/ETHOS.md` now and **follow PREAMBLE.md as instructions** (load
> the design bible, detect the engine), then continue.

The spine of the pack. This skill turns a one-line game concept into a designed, generated, self-reviewed game — and tells you which other skill does the work at each step. It is also the **first-touch router**: when the user describes a game or asks "where do I start / what's next", classify the intent and enter at the right phase below. (Routing is advisory — you invoke the next skill; there is no automatic dispatch.)

## First-touch routing

- "I have an idea / starting fresh / where do I start" → Phase 1 (Concept).
- "What's next / health-check the design" → read `./.gamestack/bible/`, find the earliest unfinished phase, resume there.
- "It's designed, now build it / which engine" → hand off to `engine-router`.
- A specific design question (combat, world, loot...) → invoke that knowledge skill directly.
- This is an existing project with design canon already established elsewhere (a `CLAUDE.md`, a `docs/`/`design/` tree, a lore graph) → the preamble's bible-init step (`shared/PREAMBLE.md` §1) handles adoption-mode detection and pointer-file setup. Once `sources.md` is written, classify the genre from the existing canon and record it in the bible — **do not re-run Phase 1 Concept** against docs that already answer it.

The design bible at `./.gamestack/bible/` (loaded by the preamble) is the persistent record of every phase's output and decisions. Read it to know what's done; append decisions to `decisions.md` as you make them.

## Classify the genre, then pull the right lens

This pipeline is **genre-aware** (see `docs/architecture.md`). After Phase 1's concept, name the game's **genre family** (open-world RPG, platformer, shooter, puzzle, strategy, sim, deckbuilder, roguelike…) and record it in the bible (`genre`). That selection decides which skills you pull:

- **🌐 Universal craft — always in play, every genre:** `game-design-fundamentals`, `game-feel-and-juice`, `level-design`, `onboarding-and-teaching`, `ui-ux-and-feedback`, `difficulty-and-balancing`, `pacing-and-the-player-journey`, `art-direction-and-readability`.
- **🎯 Genre lens — pull the ones that match:** open-world RPG → `open-world-design` + `rpg-systems` + `worldbuilding-and-lore` + `narrative-and-quest-design`; action/combat → `combat-design`; high-lethality → `permadeath-and-lethality`. (More genres are on the roadmap — until a lens exists, apply the universal spine and flag the gap.)
- **🛠️ Technical craft — pull when the game has real-time 3D, or 2D with lighting/shading:** `3d-graphics-and-rendering` (pipeline, lighting, performance budget), `shaders-and-vfx` (materials, particles, stylization), `animation-systems` (rig, blending, IK, motion matching), `procedural-geometry` (terrain, meshes, structures — pull alongside `procedural-generation` when content generation includes geometry, not just narrative content).
- **🔧 Technique module — pull when the game uses it:** procedural / AI-authored → `procedural-generation`, `ai-authored-content-coherence`, `systemic-emergent-design`.

Phase 2 below is therefore *"build this genre's core,"* not *"build a world."* The universal skills always apply; the genre lens is what changes.

## When to use this

- Kicking off a new game's design, or unsure what the next design move is
- Running headless: an agent loop that designs and generates content without a human in the seat
- Doing a design-health pass on an existing game ("which phase did we skip?")

## The core stance

1. **Design from interlocking systems and constraints, not content volume.** A headless/procedural agent's superpower is authoring *rules* that generate content, not hand-placing it. Lean into systemic and procedural design.
2. **Every element must earn its place.** Each system answers "what interesting decision does this create?"; each generated location answers "who made this and what happened here?" If neither, cut it.
3. **Hand-author a static backbone; proceduralize the connective tissue.** Finite legendary loot, named landmarks, the mythic spine, key quests = hand-authored anchors. Everything between = constrained generation.
4. **Gate generated content against hard quality bars** before it's committed. This is non-negotiable for procgen — see `procgen-review`, and `${CLAUDE_PLUGIN_ROOT}/shared/GATE.md` for the headless generate→review→repair loop.
5. **Stop at the spec, then hand off.** This pipeline produces world bibles, system specs, content, and review verdicts. Implementation is a separate, engine-specific step — when the spec is ready, pass it to `engine-router`, which routes the build to the matching engine pack (Godot/Unreal/Unity). For a tracked production cycle (epics, stories, sprints) once implementation starts, this pack has none — pair with a production-process framework like [BMad Game Dev Studio](https://github.com/bmad-code-org/bmad-module-game-dev-studio) instead (see `docs/architecture.md` § Relationship to other frameworks).

## The pipeline

Read **`PIPELINE.md`** for the full phase-by-phase process with entry/exit gates. In brief:

| Phase | Goal | Universal craft (always) | Genre lens / technique (selected) |
|-------|------|--------------------------|-----------------------------------|
| **1 · Concept** | Fantasy, 3–5 pillars, core loop, signature mechanics. Prove each is an "interesting decision." Then **classify the genre**. | `game-design-fundamentals` | — |
| **2 · Build the genre's core** | The genre's primary systems & spaces; how it feels, teaches, paces, and balances. | `game-feel-and-juice`, `level-design`, `difficulty-and-balancing`, `onboarding-and-teaching`, `pacing-and-the-player-journey`, `ui-ux-and-feedback` | open-world RPG → `open-world-design`, `rpg-systems`, `combat-design`, `systemic-emergent-design`; real-time 3D/2D → `3d-graphics-and-rendering`, `shaders-and-vfx`, `animation-systems` |
| **3 · Content** | Lore bible + constraint set; generate content from handcrafted anchors + constrained fill. Each system brought to fidelity via `iteration-loop`. | `art-direction-and-readability` | `procedural-generation`, `worldbuilding-and-lore`, `narrative-and-quest-design`, `ai-authored-content-coherence`; generated geometry → `procedural-geometry`; per-system fidelity loop → `iteration-loop` |
| **4 · Review & gate** | Run the quality bars: oatmeal, fanfic/retell, cross-instance sameness, intentionality, anti-patterns. | — | `procgen-review`, `design-review` |
| **5 · Playtest & iterate** | Watch the benchmarks (human + AI playtester); feed failures back to the phase that owns them. | — | `iteration-loop` (playtesting channel), `procgen-review` (loop) |

> Skills marked above that don't exist yet (e.g. some genre lenses, `design-review`, playtest analysis) are on the roadmap — use the matching section of an existing skill / `PIPELINE.md` in the meantime, and apply the universal spine regardless of genre.

## The one rule for headless loops

> **Never commit generated content that hasn't passed `procgen-review`.** Generation is cheap and confident; sameness is invisible from inside a single sample. The review pass is what stands in for the human designer's eye.

Start at `PIPELINE.md` Phase 1, or jump to the phase you're in.

## Output

Write phase outputs to the design bible (`./.gamestack/bible/`) and log decisions to `decisions.md`. End with a completion status per the preamble protocol: **DONE** (phase complete, bible updated) / **DONE_WITH_CONCERNS** / **BLOCKED** / **NEEDS_CONTEXT** — plus the named next phase or the `engine-router` handoff.
