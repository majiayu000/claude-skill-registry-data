---
name: ai-authored-content-coherence
description: Use when keeping AI-authored or procedurally-generated content coherent at scale — single voice across a corpus, a machine-readable lore bible with a "never violate" list, generate-then-rationalize causation, recurring thematic domains so generated figures cohere into arcs, the oatmeal/sameness problem, and the self-review pass that flags drift and duplication. The crux skill for headless / AI-authored games. Triggers on "AI-authored content", "keep it coherent", "single voice", "lore bible", "the LLM contradicts itself", "10,000 bowls of oatmeal", "generated content feels samey", "self-review pass", "narrative consistency at scale".
---

# AI-Authored Content Coherence

How to keep content an AI or procedural engine generates **coherent at scale** — one voice, no retcons, figures and events that cohere into arcs rather than dissolving into interchangeable mush. This is the crux discipline for a headless / AI-authored game, and it is **the least solved** — treat its rules as engineering hypotheses to de-risk early, not settled law.

## When to use this

- Designing the generation pipeline for lore, history, NPCs, items, quests
- Writing the voice spec / style corpus and the machine-readable lore bible
- Building the self-review / coherence pass over generated batches
- Diagnosing generated content that feels samey, contradicts itself, or drifts in voice

## Scope

This skill owns **coherence of generated content** (mostly non-visual). Adjacent siblings:
- The generator itself + the sameness problem → `procedural-generation`
- The review pass that gates a batch → `procgen-review` (this skill's self-review pass *is* that gate)
- Visual coherence / house style (the visual analogue) → `art-direction-and-readability`
- The lore the bible encodes → `worldbuilding-and-lore`
- Quests generated over world state → `narrative-and-quest-design`

## How the pieces fit

- **`GUIDE.md`** — the *why*, with exemplars and citations. **Heavily flagged:** this topic's verification phase largely failed (session limit), so nearly all rules are **sourced but unverified**. The sources themselves are strong (Compton; Grinblat & Bucklew / Caves of Qud; LLM-consistency papers).
- **`CHECKLIST.md`** — the *what to do*: Do/Don't plus "Test for" criteria for a generator, a corpus, and a self-review pass.

## The one idea to anchor on

> **Mathematical uniqueness is not perceived variety.** A generator can emit endless mathematically-distinct artifacts that players still read as one undifferentiated mass (the "10,000 bowls of oatmeal"). Coherence-at-scale is won by a shared voice + a never-violate fact bible + recurring thematic domains + an explicit self-review pass — *and even then, coherence at full open-world scale is unsolved. De-risk with the oatmeal/fanfic tests from day one.*

⚠️ **Verification note:** Built from a deep-research pass whose verification phase was cut short by a session limit; the synthesis step also partly failed. Almost every rule here is **sourced but unverified** — strong, well-cited defaults that should be re-verified, not treated as confirmed. See the banner in `GUIDE.md`.

Start with `GUIDE.md`, then apply `CHECKLIST.md`.
