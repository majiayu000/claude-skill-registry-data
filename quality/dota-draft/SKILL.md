---
name: dota-draft
description: >
  Governs draft analysis and pick recommendation logic in Dota AI Coach —
  evaluating counters, synergies, lane matchups, team composition
  dimensions (damage distribution, control, initiation/counter-
  initiation, save, sustain, wave clear), objective-taking capability
  (Roshan, tower damage, high ground), scaling/tempo/farm requirements,
  execution difficulty, and personal comfort, combined into a final
  MetaStrength/DraftFit/LaneFit/PersonalComfort/RoleExperience/
  ExecutionFit pick score. Use whenever building, modifying, or reviewing
  draft-analysis logic, a pick/ban recommendation, or hero-suggestion
  features. A pick recommended purely from global counter statistics is a
  bug in this system — consult this skill before that shortcut ships.
---

# Dota Draft Analysis

## Core rule

**Never recommend a hero based only on global counter statistics.** A
counter statistic ("hero A wins X% against hero B globally") collapses
every patch, bracket, draft context, and itemization choice into one
number — exactly the same flaw `dota-item-recommender`'s core rule
guards against for items, and `dota-domain`'s counter/matchup guidance
already warns about in general. A pick that's a statistical counter on
paper can be wrong for this specific draft, this bracket, this patch, or
this player. Global counter stats are one input to `MetaStrength` (see
below), never the whole recommendation.

## What draft analysis must consider

Full reasoning for each is in `references/composition-dimensions.md` and
`references/objectives-and-scaling.md`; summary:

**Matchup-level:**
- **counters** — matchup-specific mechanisms (per `dota-domain`), not a
  bare statistic.
- **synergies** — concrete combos between kits, not just "picked
  together often" (per `dota-domain`).
- **lane matchups** — the specific lane assignment this pick implies,
  and whether it wins/survives that lane.

**Composition-level (both teams):**
- **damage distribution** — physical/magical/pure balance and whether
  the enemy can itemize against it (per `dota-domain`'s damage-type
  guidance).
- **control** — hard/soft disable coverage and quality (per
  `dota-domain`'s CC taxonomy).
- **initiation** and **counter-initiation** — who can reliably start a
  fight on favorable terms, and who can punish/disrupt the enemy's
  initiation.
- **save** — capacity to protect a threatened teammate (a distinct
  composition need from raw control or sustain).
- **sustain** — healing/lifesteal/regen capacity to win extended
  fights/sieges.
- **wave clear** — capacity to clear creep waves, which shapes tempo,
  farm safety, and split-push viability.

**Objective/scaling-level:**
- **Roshan** — composition's capacity to contest/secure Roshan safely
  (per `dota-domain`'s Roshan guidance).
- **tower damage** and **high ground** — capacity to actually close out
  a game once ahead (per `dota-domain`'s high-ground guidance) — a
  composition can dominate the open map and still lack the tools to
  finish.
- **scaling** and **tempo** — whether the composition wants to play fast
  or slow, and whether that matches the draft's realistic win condition
  (per `dota-domain`'s tempo/win-condition guidance).
- **farm requirements** — how many cores this composition needs fed, and
  whether the draft can realistically supply that farm (ties to
  `dota-domain`'s farm-priority guidance).

**Player-level:**
- **execution difficulty** — some heroes/compositions require precise
  mechanical or decision-making execution; a theoretically strong pick
  that the player can't execute is not a good real-world recommendation.
- **personal hero comfort** — familiarity with the specific hero, distinct
  from role experience (see below).

## Final pick score: six factors

The final pick recommendation combines six named factors — keep them
distinct and individually inspectable rather than collapsing them into
one opaque number. Full detail and combination guidance in
`references/pick-score-factors.md`; summary:

- **MetaStrength** — how strong the hero is in the current patch/bracket
  in general (this is where global stats belong — as one bounded input,
  never the whole answer).
- **DraftFit** — how well the hero fits the two compositions already
  forming (synergy with allies, counters/anti-synergy with enemies,
  composition-dimension coverage from the list above).
- **LaneFit** — whether the hero wins/survives its likely lane
  assignment given both teams' picks so far.
- **PersonalComfort** — this specific player's track record/familiarity
  with this specific hero.
- **RoleExperience** — this player's track record in the *role/position*
  being filled, distinct from comfort with the specific hero (a player
  can be a comfortable pos 1 player picking an unfamiliar pos 1 hero, or
  a familiar hero being asked to play an unfamiliar role).
- **ExecutionFit** — whether the hero's mechanical/decision-making
  execution demands match what this player can reliably deliver.

See `references/pick-score-factors.md` for why these stay separate
factors (each is independently useful, auditable, and can be weighted
differently depending on context — e.g. a coaching tool for a learning
player might weight PersonalComfort/ExecutionFit higher than a
tournament-prep tool would) rather than being pre-blended into a single
score before reaching the recommendation output.

## Patch-aware and bracket-aware analysis

Every factor above — especially MetaStrength, DraftFit, and LaneFit —
must be computed relative to the **current patch** and the **relevant
bracket**, not a generic/all-time view. See
`references/patch-and-bracket-awareness.md` for:
- why patch/bracket-blind analysis silently reproduces the same bias
  problem the core rule exists to prevent (an outdated or wrong-bracket
  "counter" is just a differently-flavored version of the same mistake);
- how to source patch-pinned and bracket-segmented data correctly, tying
  into `dota-data`'s patch-tagging and `dota-ml`'s leakage-avoidance
  discipline for any model-based component.

## Structured output and avoiding bias

Follow the same discipline `dota-item-recommender` establishes for items:
structured output (a scored/ranked candidate list with traceable reasons,
not a bare hero name), and explicit avoidance of survivorship/selection
bias in any historical-data-driven component (draft data is subject to
the same "players pick what they already believe is good" confound as
item purchase data — see `dota-item-recommender`'s
`confidence-and-bias.md` for the mechanism, which applies here
essentially unchanged). Reuse that skill's output-schema pattern
(score/confidence/reasonCodes/alternatives) for draft/pick
recommendations rather than inventing a parallel convention.

## Relationship to other skills

- `dota-domain` — the strategic vocabulary (counters, synergies, damage
  types, CC taxonomy, power spikes, win conditions) this skill's
  composition-dimension analysis is built on.
- `dota-item-recommender` — the sibling recommendation skill; shares the
  core-rule pattern (never recommend from a single global statistic), the
  structured-output convention, and the survivorship/selection-bias
  concerns.
- `dota-ml` — governs any model-based component of MetaStrength/DraftFit
  scoring (baseline-first, temporal validation, leakage tests); draft
  data is match data and subject to the same discipline as any other
  training signal in this project.
- `dota-data` — patch tagging and bracket segmentation for historical
  draft/matchup data come from this pipeline; MetaStrength/DraftFit must
  be computed from patch-pinned, correctly-segmented data, not a
  convenient all-time aggregate.
- `dota-fairplay` — draft-phase information (picks, bans) is generally
  public/`PUBLIC_PREFLIGHT` once locked in by game design, but any
  enemy-comfort/history data sourced externally should still be checked
  against FairPlay's classification system if there's any doubt about its
  legitimacy for live use.
