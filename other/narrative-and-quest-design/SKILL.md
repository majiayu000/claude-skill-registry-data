---
name: narrative-and-quest-design
description: Use when designing quests, reactivity, and factions — quest structure beyond fetch-and-return, branching that honors player choice, reactivity systems on a budget (the "facts database"), procedural/radiant quests as a supplement to hand-authored ones, and faction allegiance dilemmas. Also use to diagnose quests that feel like filler or a world that ignores what the player did. Triggers on "quest design", "fetch quest", "branching", "reactivity", "facts database", "radiant quests", "factions", "choices and consequences", "the world doesn't react to me".
---

# Narrative & Quest Design

How to build quests that react to the player and factions that force real allegiance choices — and how to do it on a generation budget without quests collapsing into filler. The spine here is a **reactivity substrate** (a facts database) that both hand-authored and AI-generated quests read and write.

## When to use this

- Designing a quest, a quest line, or the quest-generation system
- Building the reactivity layer (state tracking, branching, consequences)
- Deciding what to hand-author vs. generate (radiant/procedural quests)
- Designing factions with competing goals and exclusive membership
- Diagnosing filler quests or a world that doesn't acknowledge player actions

## Scope

This skill owns **quests, reactivity, and factions**. Adjacent concerns live in siblings:
- The *space* quests sit in → `open-world-design`
- *How* to generate content + the sameness problem → `procedural-generation`, `procgen-review`
- Keeping generated quest text coherent in voice/lore → `ai-authored-content-coherence`
- Lore the quests carry → `worldbuilding-and-lore`
- Progression/economy rewards → `rpg-systems`
- General "interesting decisions" theory → `game-design-fundamentals`

## How the pieces fit

- **`GUIDE.md`** — the *why*, with exemplars and citations. **§1–2 (the facts-database reactivity substrate) are verification-confirmed.** The headline design doctrines (no-fetch-quest, radiant-as-supplement, faction dilemmas) are **sourced but unverified** — see the verification banner.
- **`CHECKLIST.md`** — the *what to do*: Do/Don't plus "Test for" criteria for a quest, a generator, or a faction set.

## The one idea to anchor on

> **Reactivity reduces to a testable condition over named facts.** Every branch, consequence, and faction state should be a boolean check against a single canonical fact store — that is the literal mechanism The Witcher 3 shipped, and it is what lets a headless agent author *and* generate quests over one world-state representation.

⚠️ **Verification note:** Built from a deep-research pass whose verification phase was cut short by a session limit. The reactivity-architecture core (GUIDE §1–2) is confirmed 3-0; the quest-quality and faction doctrines (§3–5) are sourced-but-unverified. One claim was actively **refuted** — see §6, "Do not encode."

Start with `GUIDE.md`, then apply `CHECKLIST.md`.
