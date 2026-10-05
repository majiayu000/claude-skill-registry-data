---
name: worldbuilding-and-lore
description: Use when building a world bible and deciding how lore reaches the player — the iceberg principle (author the whole world, surface ~10%), environmental & item-description storytelling, an "alien but coherent" identity that survives procedural generation, deep history as faction-proxy pantheons, and ludonarrative harmony (mechanics that are the story). Also use to diagnose lore that info-dumps, feels generic-fantasy, or has gaps that read as contradictions rather than mystery. Triggers on "worldbuilding", "world bible", "lore", "iceberg", "environmental storytelling", "item descriptions", "show don't tell", "alien but coherent", "ludonarrative", "lore dump", "deep history", "mythology".
---

# Worldbuilding & Lore Delivery

How to author a deep, internally consistent world and deliver it through space and objects instead of exposition — and how to do that under procedural / AI generation without the world contradicting itself or collapsing into generic fantasy. The spine: **build the whole iceberg as frozen, typed, queryable canon, then generate only the leaves that read from it.**

## When to use this

- Authoring the world bible (cosmology, timeline, factions, geography, economy, magic laws)
- Deciding *how* lore reaches the player (item text, environment, aftermath vs. cutscene/dialogue)
- Defining the world's identity/register so generation doesn't drift toward Tolkien defaults
- Designing mythology and "deep history" that the player can actually feel
- Making each mechanic carry the theme (ludonarrative harmony) and answer a lore question
- Diagnosing info-dumps, "wiki voice", generic-fantasy regression, or unbounded ambiguity

## Scope

This skill owns **the world bible and lore *delivery*.** Adjacent concerns live in siblings:
- The *space* lore is delivered through → `open-world-design`
- *How* to generate content + the sameness problem → `procedural-generation`, `procgen-review`
- Keeping generated lore text coherent in voice → `ai-authored-content-coherence`
- Quests that carry lore → `narrative-and-quest-design`
- Visual register / readability of the alien look → `art-direction-and-readability`
- Mechanics whose lore you're justifying (loot, economy, death) → `rpg-systems`, `permadeath-and-lethality`
- "Interesting decisions" / ludonarrative theory → `game-design-fundamentals`, `systemic-emergent-design`

## How the pieces fit

- **`GUIDE.md`** — the *why*: five sub-domains (iceberg, environmental/item delivery, alien-but-coherent identity, deep history, ludonarrative harmony), each with exemplars, citations, a "test for" criterion, a named failure mode, and the procedural/AI-authoring implication.
- **`CHECKLIST.md`** — the *what to do*: Do/Don't + Test-for, grouped by sub-domain.

**Source & epistemic status.** Distilled from a deep-research synthesis (Hemingway's iceberg; Jenkins's four modes; Sanderson's & Jemisin's craft laws; Hocking's ludonarrative dissonance; FromSoftware/Morrowind/Elden Ring/RDR2 exemplars). The literary craft sources (1932–2018) predate LLM authors and assume a human who *holds* the iceberg in mind — so the **AI-authoring mitigations (frozen typed canon, generate-leaves-not-roots, validators-before-generators) are engineering hypotheses to test, not received best practice.** Source caveats are carried inline in `GUIDE.md §6`.

## The one idea to anchor on

> **Omission is only safe over a backbone that exists.** Hemingway: a writer who omits things he *knows* makes the reader feel them; one who omits what he *doesn't* know "only makes hollow places." For an LLM that fails by exactly that route, the fix is to make the submerged 90% an explicit, typed, frozen canon graph — then generate surface artifacts that only *read from* it. Never invent a backbone fact at the moment you write an item description.

Start with `GUIDE.md`, then apply `CHECKLIST.md`.
