---
name: dota-domain
description: >
  Dota 2 strategic domain knowledge for this project. Use whenever working with
  heroes, roles, positions, lanes, items, facets, talents, damage types, crowd
  control, power spikes, tempo, farm priority, win conditions, Roshan, high
  ground, buyback, item timings, team fights, draft, counters, synergies, or
  matchups — whether in code, ML features, recommendation logic, or discussion.
  Ensures software and ML decisions make sense from a real Dota 2 strategic
  perspective, not just from raw stats.
---

# Dota 2 Domain Knowledge

Apply this skill whenever a task touches Dota 2 strategy or game concepts —
designing a data model, writing a recommendation heuristic, choosing ML
features/labels, or reviewing whether an output is strategically sound.

## Core principle: context beats aggregate stats

A hero or item's global win rate is a weak, often misleading signal in
isolation. The same hero can be excellent in one draft and a liability in
another. Any recommendation-shaped decision (hero pick, item build, timing
advice) must be evaluated against the actual situation, not a single number.

**Never** recommend a hero solely from global win rate.
**Never** recommend an item solely from item win rate.

Instead, ground recommendations in as many of these as are available:

- the hero and their kit (see `references/heroes-and-roles.md`)
- role/position being played (pos 1-5 carry different priorities)
- current patch (balance changes shift what's good)
- skill bracket (a herald-tier read differs from an immortal-tier read)
- player comfort/experience with the hero — a worse hero played well often
  beats a stronger hero played poorly
- game minute / game state (early laning vs. late-game teamfight phase)
- the draft — both teams' picks, not just your own
- current items already owned and gold available
- observed threats — specific enemy heroes, their items, and their capability
  (e.g. "do they have a burst combo that kills me from full HP?")

If the surrounding code or a caller wants a recommendation, check whether
enough context is present to reason about it this way. If it isn't, that's a
missing-input problem to raise, not something to paper over with a global
average.

## Separate mechanics from strategy

Mechanics = objective, ruleset facts: what an item does, a hero's base stats,
how buyback cost scales, whether a spell pierces spell immunity.

Strategy = situational judgment built on top of mechanics: whether buying
that item *now* is correct, whether a fight is winnable, whether to push high
ground.

Keep these separate in code and in reasoning:
- Mechanical facts belong in structured data (see `references/data-model.md`),
  not hardcoded into strategic logic.
- Strategic logic consumes mechanical facts plus game state; it should not
  need to re-derive or guess at mechanics.

This mirrors the GSI layering in this project (see the `dota-gsi` skill):
raw state flows up into a normalized `MatchState`; strategic reasoning is a
separate layer built on top of it, never mixed into ingestion/normalization.

## Prefer structured domain concepts over free text

When representing hero roles, damage types, CC types, item timings, draft
state, etc. in code, ML features, or prompts, use structured, enumerable
concepts (e.g. a `Position` of 1-5, a `DamageType` enum, a `CrowdControlType`
enum) rather than ad hoc free-text strings. Structured concepts are testable,
composable, and prevent subtle inconsistency (e.g. "carry" vs "hard carry" vs
"pos 1" meaning the same thing three different ways in three places).

## Reference files

Load these as needed — don't pull them into context for tasks that don't
need the detail:

- `references/heroes-and-roles.md` — roles, positions, lanes, hero
  archetypes, damage types, crowd control taxonomy
- `references/game-flow.md` — power spikes, tempo, farm priority, item
  timings, Roshan, high ground, buyback, team fights, win conditions
- `references/draft-and-matchups.md` — draft phases, counters, synergies,
  matchup reasoning, facets and talents
- `references/data-model.md` — suggested structured representations for
  these concepts in this project's domain layer, and how they relate to the
  GSI `MatchState`/`DomainEvents` pipeline
