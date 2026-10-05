---
name: iteration-loop
description: Use when bringing any system — visual (terrain/biome/dungeon/town/castle/character/enemy/NPC/spell-fx), systemic (balance/economy/difficulty), or narrative (lore/quests) — up to fidelity with its intended target through repeated cycles, in any engine. Covers the generic Reference → Diff → Prioritize → Generate/Implement → Verify loop, a preview-harness pattern for screenshotting/inspecting a system in isolation, the animation-can't-be-eyeballed-from-one-frame problem (contact-sheet capture), the external-asset/content-request escalation (when generation is the wrong tool — e.g. animations, trees), the two playtesting channels — human playtesters and an AI playtester that self-verifies via logs/screenshots through a "playtester API" — a human-checkpoint/batching pattern for scaling a generated visual change (including a cheap-mockup gate before heavyweight 3D/tileset generation), and an asset-pack organization + browsable-studio/explorer pattern for what gets approved. Also use to diagnose a project that's generating content/assets without ever checking them against a target, stuck eyeballing single animation frames, about to batch-apply a generated visual change across many instances before a human has seen it, or accumulating approved assets with no organized, browsable home. Triggers on "iteration loop", "loop based development", "visual fidelity loop", "close the gap", "bench", "preview harness", "concept art diff", "reference vs implementation", "playtester", "AI playtester", "self-play", "playtest loop", "external asset request", "animation contact sheet", "generate review iterate", "human checkpoint", "human in the loop", "AI can't judge its own art", "batch asset request", "3D model generation", "Meshy", "Hyper3D", "tileset generation", "icon pack", "asset pack", "mockup before generating", "image to mesh", "asset studio", "asset explorer".
---

# Iteration Loop

The loop every gamestack content type runs to close the gap between an **intended target** and **what's actually implemented** — whether the target is concept art, a balance curve, or lore canon. One loop shape, instantiated per modality.

> **Tier:** process (tier-spanning, lives in `gamestack-core`). Not a knowledge skill — a recurring procedure other skills plug into.

## The loop

**Reference → Diff → Prioritize → Generate/Implement → Verify**, run per system, repeated until the gap closes or is explicitly deferred.

1. **Reference** — pull the intended target for *this* system: a concept-art subset, a stated balance target, a lore-canon fact set. If references aren't organized per-system, that's the first fix — an unindexed reference pile can't be diffed against.
2. **Diff** — compare the current implementation against the reference and name the **single biggest delta** (not a laundry list). This step stays human/agent *judgment*, not a mechanical pixel-diff or string-diff — see `LOOP.md` for why and for the modality-specific diff method.
3. **Prioritize** — pick the highest-benefit delta to close next. One delta at a time keeps each cycle verifiable.
4. **Generate/Implement** — close it: generate an asset (asset-gen pipeline + your project's optimize/import pass), tune a system (cost curves, drop tables), or author content (within established canon) — then wire it in **data-driven**, never as a hardcoded one-off, and file it into its categorized asset pack (`LOOP.md` §7). For visual/aesthetic deltas, generate against **one instance first**, not the whole system; for heavyweight pipelines (3D model gen, tileset gen), stage that behind a few cheap 2D mockups first — see `LOOP.md` §6 for why and the batching pattern. When generation is the wrong tool for this delta (animations, trees, a hand-authored hero asset, …), route to the external-request escalation (§5) instead of forcing a worse generated result.
5. **Verify** — re-check against the reference. Did the named delta close? If not, the cycle repeats; if a new bigger delta surfaced, that's the next Prioritize. For visual/aesthetic deltas, the generating agent's own judgment of "does this look right" isn't reliable verification — that routes through a human checkpoint (`LOOP.md` §6) before the change scales beyond the single instance.

`LOOP.md` has the full per-modality table (visual / systemic / narrative), the preview-harness pattern, the animation contact-sheet requirement, the playtester channels, the external-request escalation, the human-checkpoint/batching pattern for scaling a visual change, and the asset-pack/studio organization pattern for what gets approved.

## Scope

This skill owns **the loop shape and its two verification channels** (inspection, playtesting). It does not own what "good" looks like for any one modality — that's the knowledge skill the loop calls into:
- Visual fidelity → `art-direction-and-readability` (readability/style target), `3d-graphics-and-rendering` / `shaders-and-vfx` / `animation-systems` / `procedural-geometry` (what gets tuned)
- Systemic fidelity → `difficulty-and-balancing` (the simulation/self-play verification method)
- Narrative fidelity → `worldbuilding-and-lore` (the never-violate fact-check grid), `ai-authored-content-coherence` (the self-review pass)
- Content *variety* (a different axis from fidelity — is each instance distinct, not just on-target) → `procgen-review` + `shared/GATE.md`
- Routing the Implement step to engine code → `engine-router`

## The two verification channels

Every modality's Verify step can run through either or both:

- **Inspection** — modality-specific spot-check of one system in isolation (a screenshot, a metrics readout, a fact-check pass). Cheap, fast, run every cycle.
- **Playtesting** — exercising the *combination* of systems in actual play. Slower, catches what isolated inspection can't (a biome that reads fine alone but feels wrong next to its neighbor). Two playtester types, not a hierarchy — use both:
  - **Human playtester** — the only source for genuine fun/feel judgment.
  - **AI playtester** — an agent that plays or drives the game and self-verifies via a **playtester API**: programmatic read access to its own logs, game state, and screenshot output (input injection too, where available). Cheap enough to run every cycle; escalate to a human when the AI's read is ambiguous or the question is subjective ("is this fun"), not when it's just expensive to set up.

## The one rule

> **Never generate or implement without a reference to diff against.** Generation without a target produces output nobody checked against intent — the same failure `procgen-review` polices for *variety*, this skill polices for *fidelity*. If there's no organized reference for a system yet, organizing one is the first loop cycle, not a skippable prerequisite.

Start at `LOOP.md`.
