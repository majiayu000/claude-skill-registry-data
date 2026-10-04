---
name: dota-item-recommender
description: >
  Governs item recommendation logic in Dota AI Coach — the
  candidate-generation/scoring/ranking/explanation pipeline, required
  context inputs (hero, role, facet, patch, bracket, minute, level, gold,
  inventory, purchase sequence, allied/enemy heroes, visible enemy items,
  damage/disable composition, power spikes, player comfort), the required
  structured output shape, and how survivorship/selection bias get
  avoided. Use whenever building, modifying, evaluating, or reviewing
  item recommendation logic, an item-scoring model, or anything that
  decides what item a player should buy next. A recommendation that
  reduces to "highest win-rate item" is a bug in this system, not a
  simplification — consult this skill before that shortcut ships.
---

# Dota Item Recommendation

## Core rule

> NextItem ≠ ItemWithHighestWinRate

An item's aggregate win rate collapses everyone who ever bought it —
every hero, every role, every patch, every game minute, every matchup —
into one number. The item that's statistically associated with winning
the most, on average, across all of that, is very often *not* the right
item for this specific hero, at this specific minute, against this
specific enemy lineup. Treating win rate as the recommendation is the
single most tempting shortcut in this domain, because it's cheap to
compute and looks like it's grounded in data — resist it. This is the
same principle `dota-domain` states generally ("never recommend an item
solely from item win rate"); this skill is where it becomes an actual
system design.

## Required context

A recommendation is only as good as the context it's conditioned on. The
full list, with reasoning for why each matters, is in
`references/context-inputs.md` — summary:

- **hero** and **role** — what the hero's kit needs, and what job they're
  doing (farm priority, initiation, utility) shape what's valuable at all.
- **facet** — a facet can shift a hero's kit enough to change item
  priorities (per `dota-domain`).
- **patch** — item costs, mechanics, and hero balance all shift by patch;
  a correct answer on one patch can be wrong two patches later.
- **bracket** — what's correct/achievable differs by skill level.
- **minute** and **level** — timing determines what's actually reachable
  and what the current power-spike window calls for.
- **gold** (current and near-future income) — a theoretically ideal item
  the player can't afford yet isn't a next-item recommendation.
- **current inventory** — recommending an item already owned, or one
  redundant with what's owned, is a correctness bug.
- **purchase sequence** — the order items were bought signals what
  problem the player has already tried to solve, and what's likely still
  needed.
- **allied heroes** — synergy and coverage: don't recommend redundant
  utility the team already has covered elsewhere.
- **enemy heroes** and **visible enemy items** — counters and threats are
  matchup-specific and time-varying; see `dota-fairplay`'s
  `VISIBLE_SCREEN` classification for what "visible enemy items" may
  legitimately include.
- **damage composition** and **disable composition** — of both teams;
  itemization should respond to what's actually threatening the player,
  not a generic profile.
- **power spikes** — whose window is active/imminent should inform
  urgency and choice (per `dota-domain`'s game-flow concepts).
- **player comfort** — a player's familiarity with an item build affects
  whether it's actually the right real-world recommendation, not just the
  theoretically optimal one.

Treat missing context as a real constraint on recommendation quality, not
something to silently paper over with a default — see
`references/context-inputs.md` for how to handle it.

## Pipeline: candidate generation → scoring → ranking → explanation

These four stages are kept structurally separate — not just
conceptually, but as distinct components with distinct responsibilities,
testable independently. Full detail in `references/pipeline.md`; summary:

1. **Candidate generation** — produces the set of items worth
   considering at all, given hero/role/inventory/gold-trajectory
   constraints. This stage's job is recall (don't miss a genuinely
   relevant item), not precision — over-inclusion here is cheap; a missed
   candidate can never be recommended no matter how good scoring is.
2. **Scoring** — assigns each candidate a score given the full context.
   This is where the actual "is this good, right now, for this
   situation" judgment happens, combining `dota-domain` strategic
   reasoning with any model-based scoring per `dota-ml`.
3. **Ranking** — orders scored candidates and selects what to surface
   (top item, ranked alternatives). Ranking can apply constraints scoring
   doesn't (e.g. diversity across alternatives, deduplication of
   near-equivalent items) without needing to re-touch scoring logic.
4. **Explanation** — produces human-readable reasoning for the top
   recommendation(s). See "LLM boundary" below — this stage may use an
   LLM; the prior three must not depend on one.

Keeping these separate means a scoring bug can be fixed without touching
ranking, and an explanation-quality issue never requires touching the
actual decision logic — see `references/pipeline.md` for why collapsing
these stages is a recurring temptation worth resisting.

## LLM boundary

**LLMs may explain recommendations but may not be the primary item
decision engine.** This is `dota-ml`'s "ML decides, LLM explains"
principle applied specifically here:

- Candidate generation, scoring, and ranking must be deterministic/
  model-based logic (rules, `dota-ml`-governed models) that can be
  tested, evaluated, and reasoned about independently of any LLM call.
- The explanation stage may use an LLM to turn the structured output
  (below) into natural-language reasoning for the player, but the LLM
  must not be asked to *decide* the item, re-rank candidates, or override
  the score/ranking it's explaining — its job is narration of an
  already-made decision, not the decision itself.
- If an LLM's explanation seems to justify a different item than what
  was actually recommended, that's a bug in the explanation stage, not a
  sign the LLM found a better answer — investigate why the structured
  reasoning (reasonCodes) didn't actually support the recommendation
  scoring produced.

## Required structured output

Every recommendation must be emitted in this shape — not just for the top
pick, but for the alternatives considered:

```
itemId:       the recommended item's identifier
score:        the scoring stage's output for this item (see pipeline.md
              for what this represents and how it's produced)
confidence:   how much the system trusts this score, given available
              context — see confidence-and-bias.md; not the same thing
              as the score itself
reasonCodes:  structured, enumerable reasons this item scored as it did
              (e.g. COUNTERS_ENEMY_BURST, FILLS_DISABLE_GAP,
              MATCHES_POWER_SPIKE_WINDOW, AFFORDABLE_NOW) — this is what
              the explanation stage consumes and what makes the
              recommendation auditable
alternatives: other candidates considered, each with their own score/
              reasonCodes, so the player (and any reviewer) can see what
              else was weighed and why it ranked lower
```

See `references/output-schema.md` for the full schema, reasonCode
taxonomy, and worked examples. Prefer this structured shape over free
text everywhere in the pipeline — per `dota-domain`'s general preference
for structured concepts over free-text assumptions, this is what makes
recommendations testable and what the explanation stage narrates rather
than invents.

## Avoiding survivorship and selection bias

Historical item data is skewed by who chose to buy what — see
`references/confidence-and-bias.md` for the concrete mechanisms (e.g.
players who bought an item disproportionately already had a favorable
game state, so raw purchase-outcome correlation overstates the item's
actual causal value) and how candidate generation/scoring should account
for this rather than naively fitting to observed purchase-outcome
correlations. This connects directly to `dota-ml`'s baseline-first and
leakage-testing discipline — a scoring model here is subject to the same
rules as any other model in this project.

## Relationship to other skills

- `dota-domain` — the strategic vocabulary (roles, damage types, power
  spikes, counters) this skill's context inputs and scoring logic are
  built on.
- `dota-ml` — governs how any model-based scoring is built, validated,
  and shipped (baseline-first, leakage tests, calibration); this skill
  governs what that model is *for* and how its output fits the
  recommendation pipeline.
- `dota-fairplay` — governs what "visible enemy items" and other live
  inputs may legitimately include; this skill's context inputs must
  respect that classification.
- `dota-architecture` — this skill's pipeline maps onto the
  Recommendation Engines / Recommendation Orchestrator layers; the
  four-stage separation here is a specific instance of "recommendation
  engines consume normalized features," not a competing structure.
