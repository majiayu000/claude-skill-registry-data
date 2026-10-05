---
name: procgen-review
description: Run this to review a batch of procedurally- or AI-generated game content (dungeons, regions, quests, items, NPCs, lore, history) before it's committed. Stands in for the human designer's eye in a headless generation loop. Runs the oatmeal test (perceptual sameness), the fanfic/retell test (is it worth retelling), a cross-instance sameness scan (structural/thematic duplication), an intentionality gate (who/what/why + completion arc), and an anti-pattern gate. Outputs a structured pass/fail verdict with specific fixes routed back to the generator. Triggers on "review generated content", "check for sameness", "procgen review", "oatmeal test", "is my generated content any good", "gate this content".
---

# Procgen Review

## Preamble (auto-loaded)

!`cat "${CLAUDE_PLUGIN_ROOT}/shared/PREAMBLE.md"; echo; cat "${CLAUDE_PLUGIN_ROOT}/ETHOS.md"`

> FALLBACK: if the line above rendered literally or empty (`disableSkillShellExecution`),
> Read `${CLAUDE_PLUGIN_ROOT}/shared/PREAMBLE.md` and `${CLAUDE_PLUGIN_ROOT}/ETHOS.md` now
> and **follow PREAMBLE.md as instructions**, then continue.

The quality gate for generated content. Generation is cheap and confident; **sameness is invisible from inside a single sample.** This skill is the review pass that catches it — designed to run automatically in a headless generate-review-repair loop (see `${CLAUDE_PLUGIN_ROOT}/shared/GATE.md` for the loop harness).

## When to use this

- After any batch of content is generated, **before it's committed** to the game
- As the standing gate inside a headless authoring loop
- To audit existing generated content for the failure modes a generator can't self-detect

## What it needs

- The **batch** of generated artifacts (ideally ≥8 instances of a type, so sameness is detectable)
- The generator's **constraint set** / definition of "good" (from `procedural-generation`)
- Access to **prior committed instances** of the same type (for the sameness scan)

## What it produces

A structured verdict per `REVIEW.md`'s format: each artifact gets PASS / SOFT-FAIL / HARD-FAIL across five gates, with specific, actionable fixes routed to the phase that owns them (per `game-design-process` Phase 5).

**Headless contract (for the GATE.md loop):** emit the machine-readable verdict as the **final fenced ```json block** of your output, shape `{ "pass": bool, "score": number, "failures": [{ "gate", "detail" }] }`. `pass` is false if any artifact HARD-FAILs. The harness extracts the last fenced json block — nothing else needs to be parseable.

## The procedure

Read **`REVIEW.md`** for the full step-by-step. The five gates, in order:

1. **Oatmeal test** — perceptual, not mathematical, uniqueness.
2. **Fanfic/retell test** — would a player retell it?
3. **Cross-instance sameness scan** — structural & thematic duplication vs. prior instances.
4. **Intentionality gate** — who built it, what happened here, why this reward, completion arc.
5. **Anti-pattern gate** — the named failure modes.

## The one rule

> **Nothing generated ships unreviewed.** A HARD-FAIL on any gate blocks the commit and returns the artifact to the generator with the specific fix. This is the non-negotiable backstop of headless procedural authoring.

Grounded in `procedural-generation` (the principles being tested) and `open-world-design` (the spatial anti-patterns). For the sibling check on *fidelity to a target* (concept art, a balance curve, lore canon) rather than *variety*, see `iteration-loop` — run both; they gate independent axes. Start at `REVIEW.md`.
