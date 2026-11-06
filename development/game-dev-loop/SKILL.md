---
name: game-dev-loop
description: "Game development only (game design, engine, playtest). The complete game-development loop — persist the goal → classify the game idea → write GDD + TDD → pick an engine and scaffold → implement → test and debug → render-quality + playthrough guide → polish → write durable memory. Use when starting or running a real game build, when a task needs design, docs, code, testing, and polish chained in order, or when the user asks for a game \"from idea to playable\". Not for general software work - use software-dev-loop."

version: 1.1.1
metadata:
  category: game-dev
  created_by: agent
---

# Game Dev Loop — idea → docs → build → test → polish

One loop that chains the vault's game-dev skills into a single build process. It
does not replace any of them — it is the sequence and the handoff between them.

```
game idea → GDD/TDD → engine+template → implement → test/debug → quality loop → guide → memory
  └────────────────────← bug / goal unmet / quality short ←────────────────────┘
```

## When to Use

- Starting a real game build (web, single-file, Phaser, Three.js, or UE) that needs design, docs, code, testing, and polish chained in order.
- A task large enough that "just write code" would drift — you need a GDD and a plan on paper first.
- The user asks to go "from idea to playable", or to ship ONE polished scene.

## The loop

1. **Persist the goal.** Capture the objective once; keep it intact for the whole run. (`goal-persistence`)
2. **Classify the idea.** Pick the archetype and the right engine/template before writing anything. A mismatched engine is the most expensive mistake. (`game-archetype-classifier`, or reason inline for non-2D ideas.)
3. **Write GDD + TDD.** Game Design Document first, then the Technical Design Document that makes each GDD section a buildable contract. (`gdd-markdown-template`, `technical-design-document`)
4. **Scaffold.** Pick the engine/template and get a runnable skeleton before adding features:
   - 2D Phaser → `phaser-gamedev`
   - single-file zero-dependency HTML → `single-file-html-game`
   - parallel multi-agent DDD swarm → `kimi3-game-gen`
   - Three.js PBR / high-fidelity 3D → `three-pbr-workflow`
   - AI-editable 3D engine (core/adapters + tokenized world) → `cat-game-architecture`
5. **Implement in vertical slices.** One feature → one test → repeat. Don't write all code then all tests. (`test-driven-development` / `tdd`)
6. **Test + debug.** Deterministic E2E with screenshots/assertions; for UE shader/GPU issues use the UE-specific skills. (`playwright-testing`, `webapp-testing`, `ue4-shader-debug`, `ue-renderdoc-auto-capture`)
7. **Quality loop.** Screenshot → evaluate → improve, until it meets the bar. (`render-quality-loop` for visuals; `intro-scene-until-perfect` for the single-scene polish discipline)
8. **Playthrough guide.** Turn the verified probes into a human-readable how-to. (`guide-from-probes`)
9. **Write long-term memory.** Decisions, gotchas, and next steps land in the durable store the same turn they happen.

**Loop back:** a failing test, an unmet goal, or a quality shortfall returns to the plan (step 3), not straight to more code.

**2D / template-based variant:** for a 2D template project, `game-dev-agent-workflow` is the
concrete phase script for steps 2–6 (classify → scaffold → design → assets → config/registration →
implement → verify). Use it instead of re-deriving those phases; `game-template` /
`game-template-engineering` cover scaffolding and the KEEP/COPY hook discipline,
`game-debug` the living debug protocol, `game-build-verification` the pre-ship checklist.

## Pillars → skills

| Pillar | Skill | Contribution |
|---|---|---|
| Goal | `goal-persistence` | durable objective, anti-drift steering, completion audit |
| Design — GDD | `gdd-markdown-template` | 13-section design doc |
| Design — TDD | `technical-design-document` | engineering spec that complements the GDD |
| Classify | `game-archetype-classifier` | physics-first archetype before scaffolding |
| Build — Phaser | `phaser-gamedev` | 2D scenes, sprites, physics, tilemaps |
| Build — single-file | `single-file-html-game` | zero-dep HTML, tiered against GAME_TIERS.json |
| Build — swarm | `kimi3-game-gen` | DDD + parallel coder agents, no asset files |
| Build — 3D PBR | `three-pbr-workflow` | runnable Three.js PBR scene, token-friendly |
| Build — AI-editable 3D | `cat-game-architecture` | C.A.T framework, core/adapters split |
| Test | `playwright-testing`, `webapp-testing` | deterministic E2E, screenshots, assertions |
| UE debug | `ue4-shader-debug`, `ue-renderdoc-auto-capture` | shader X30xx + GPU frame capture |
| Quality | `render-quality-loop` | screenshot → evaluate → improve |
| Polish | `intro-scene-until-perfect` | ONE scene, vertical slice, infinite polish |
| Guide | `guide-from-probes` | assertions (not pixels) → playthrough guide |
| Long-term memory | (this skill) | durable memory file |

## Rules

1. **Goal first, never narrowed.** Re-inject the objective every turn; audit completion against real state, never self-declared.
2. **Classify before code.** The engine/template choice is the most expensive decision; make it in step 2, on paper.
3. **GDD before TDD before code.** A game without a GDD drifts; a GDD without a TDD isn't buildable. Don't skip either for a real build.
4. **Vertical slices.** One feature → one test → repeat. Don't write all features then all tests.
5. **Measure quality.** "It runs" is not a result; a screenshot evaluation against a bar is. (`render-quality-loop`)
6. **Write memory as you go.** Decisions and gotchas land in the durable store the same turn they happen.
7. **Loop back on failure.** Return to the plan (GDD/TDD), not to more code.

## Stage handoff

Each stage hands a written artifact to the next:

- **goal** → objective + status + completion evidence
- **classify** → archetype + engine/template choice + why
- **GDD/TDD** → design doc + engineering spec (each section a build contract)
- **scaffold** → runnable skeleton (proves the engine choice before features)
- **implement** → code + what changed (vertical slices)
- **test/debug** → red-green results + fixed error signatures
- **quality** → screenshot evaluation vs bar + improvements
- **guide** → playthrough how-to (from probe assertions)
- **memory** → durable facts / decisions / lessons appended to the store

## Per-round gate (answer at the end of EVERY round)

A round does not close until all four questions are answered explicitly. Do not
advance to the next step — or repeat — on an unanswered gate.

1. **Success / fail criteria?** State the acceptance bar for THIS round: what must be true (tests green? quality met? blocking issues = 0?) for the round to count as success vs failure. No criteria = drift, not a round.
2. **What should touch / not touch?** State the scope boundary: which files / areas / behaviors this round may modify, and which are off-limits. Anything outside the boundary is a scope violation, not a fix.
3. **Report criteria?** State what the end-of-round report must contain — use the fixed report format below, nothing else as the round summary.
4. **Self-review rounds + next step?** State how many critic rounds you will run before accepting (`source-anchored-design`: repeat until blocking = 0; set a hard cap if the round has a budget), and whether the next step auto-starts and repeats.

## Round report (fixed format)

At the end of every round, emit exactly this block — nothing else as the round's
summary. The agent does NOT judge success/failure itself; it restates the
original criteria, reports each one's current status, and gives only a
confidence score so the human can judge:

```
success criteria: <restate this round's original criteria verbatim>
criteria status: <one line per criterion: met / not met / partial, with evidence>
success confidence: <0-10>
failure confidence: <0-10>
touch: <files/areas modified>
not touch: <files/areas deliberately left alone>
next: <single next action>
self review status: <critic rounds run, blocking issues remaining>
next step status: <auto-start | wait-for-user | done>
```

The two confidence scores (0–10) are the agent's own estimate of how likely the
round succeeded and how likely it failed — they are NOT a verdict. The human
decides success/failure from the criteria status, not from the scores.

## Termination

The loop ends when the goal's completion audit passes against real state — tests green, quality meets the bar, memory and guide written — and the final round report shows all criteria `met` with `next step status: done`. The agent never declares the loop a success itself; the human does, from the criteria status. A failing test, an unmet goal, or a quality shortfall is not termination; it is a return to step 3 (plan).

## When NOT to use

- Trivial one-shot edits — a one-line change does not need the whole loop.
- A task one skill already covers — don't compose for the sake of composing.
- Pure asset/art generation with no code — use the asset-direction or creative skills directly.
