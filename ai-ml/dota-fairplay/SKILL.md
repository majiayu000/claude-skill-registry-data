---
name: dota-fairplay
description: >
  Mandatory safety and fair-play gate for the Dota AI Coach project. Use
  whenever introducing a new live-game data source, adding a MatchState
  field, adding a computer-vision feature, adding an ML model feature,
  working with opponent information, working with replay data, or
  modifying live recommendations. Classifies every live data point and
  blocks anything a human player could not legitimately know during a
  live game — this is a correctness gate, not a style preference, and
  must be consulted before such changes are considered complete.
---

# Dota Fair Play

This project's core promise is that it coaches a player using only
information that player could legitimately have. Breaking that promise
turns a coaching tool into a cheat, even by accident — e.g. a "helpful"
feature that infers an unwarded enemy jungle position from a data source
the player couldn't see themselves. Apply this skill whenever a change
touches what the live application knows or acts on.

## The core rule

> If a human player can legitimately know something from their own game
> state or visible screen, the application may analyze it.
> If Dota intentionally hides it, the live application must not access it.

"Legitimately know" means through normal play: your own GSI-exposed state,
what's rendered on your screen (minimap, HUD, visible units), or public
information anyone could look up before the game starts. It does not mean
"technically retrievable" — memory reading, packet inspection, or network
extraction routinely expose game-engine state that Dota's fog-of-war design
deliberately withholds. This skill exists to make sure implementation
convenience never quietly substitutes for legitimate visibility.

## Classifying data

Every live data point used by this project must be classified into exactly
one of six categories, defined in full in
`references/classification-categories.md`:

- **LIVE_ALLOWED** — visible to the player right now via GSI/game state;
  safe for live use.
- **VISIBLE_SCREEN** — visible on screen but not exposed via GSI; safe for
  live use only if captured from what's actually rendered (e.g. computer
  vision on the player's own screen), never inferred from a hidden source.
- **PUBLIC_PREFLIGHT** — public information available before/outside the
  live game (patch notes, hero stats, prior public match history); safe to
  use for pre-game or draft-time features, not a backdoor for in-game
  hidden info.
- **POSTGAME_ONLY** — only becomes legitimately available after the match
  ends (e.g. full replay data revealing prior fog-of-war state); usable
  for post-game analysis, never fed into live recommendations.
- **SPECTATOR_ONLY** — available only through spectator/observer mode
  (which sees more than a player does); never usable for a live player-
  facing feature, even if technically present in a data feed.
- **FORBIDDEN** — not legitimately available to a player at any point
  through any sanctioned means; must not be captured, stored, or used at
  all, regardless of technical feasibility.

Read `references/classification-categories.md` before classifying
anything non-obvious — it has worked examples for the ambiguous cases
(e.g. "enemy item icons glimpsed briefly on your own screen" vs. "enemy
inventory pulled from a data source").

## Explicitly forbidden techniques and data

Regardless of classification, the following are never acceptable in this
project, full stop — they are means/ends that bypass the visibility rule
by construction, not judgment calls to weigh case by case:

**Techniques:**
- reading Dota 2 process memory
- DLL injection into the game process
- packet capture/manipulation of game network traffic
- automated input injection (mouse/keyboard macros controlling the client)
- automated ability casting
- automated item purchasing

**Data:**
- fog-of-war information the player's client hasn't revealed
- hidden/unobserved enemy locations
- unobserved enemy items (inventory not shown on the player's screen)
- hidden ward positions (wards the player hasn't seen placed or revealed)

If a proposed feature depends on any of these, the feature is not
"restricted" — it is out of scope for this project and should be redesigned
around legitimately visible data or dropped. See
`references/forbidden-techniques.md` for why each of these specifically
breaks fair play, including the subtler cases (e.g. why reading a value
via GSI is fine but reading the "same" value via memory is not, even
though the number is identical).

## Required documentation for every live feature

Every live-facing feature (data source, MatchState field, CV feature, ML
feature, or recommendation) must document these five fields — in code
comments, a design doc, or the PR description, whichever fits the
project's existing conventions:

- **source** — where the data physically comes from (GSI payload field,
  screen region via CV, static file, API call, etc.)
- **availability** — when this data exists (always, only during laning,
  only post-game, etc.)
- **visibility** — what a legitimate player can see that corresponds to
  this data, stated concretely (not "the player can infer this" — cite
  the actual screen element or GSI field)
- **fairPlayClassification** — one of the six categories above
- **justification** — a short explanation of why this classification is
  correct for this specific data point, especially if it's a non-obvious
  case

Template and examples: `references/feature-documentation-template.md`.

If you can't fill in `visibility` concretely, that's a signal the feature
may not be legitimate — stop and flag it rather than guessing.

## Required automated tests

Every live feature must have automated FairPlay tests asserting that:
1. its data source is classified correctly (matches one of the six
   categories, with no ambiguity);
2. it does not consume any FORBIDDEN or SPECTATOR_ONLY data;
3. POSTGAME_ONLY data never reaches a live recommendation path.

See `references/testing-fairplay.md` for concrete test patterns and how
this integrates with the existing `dotnet test` workflow referenced by
the `dota-gsi` skill.

## Relationship to other skills

This skill governs *what data may be used*; `dota-gsi` governs how raw
state is ingested/normalized into `MatchState`, and `dota-domain` governs
strategic reasoning once data is available. A GSI field, CV feature, or ML
feature must pass FairPlay classification before it's treated as a
legitimate input to the domain/strategy layer — fair-play classification
happens at the data-ingestion boundary, not after the fact.
