---
name: dota-postgame
description: >
  Governs post-game analytics in Dota AI Coach — analyzing laning, farm,
  item timings, deaths, teamfights, objectives, buyback, power spikes,
  turning points, and recommendation adherence after a match ends, using
  full match/replay data now legitimately available. Use whenever
  building, modifying, or reviewing post-game analysis, a match report,
  or any feature comparing a player's performance to a reference group.
  This is where POSTGAME_ONLY data (per dota-fairplay) is meant to be
  used — but it comes with its own discipline: distinguishing
  correlation from causality, respecting sample size, and surfacing a few
  real insights instead of a wall of statistics. A report that claims an
  item won the game because it was bought before winning is a bug here,
  not a stylistic choice.
---

# Dota Post-Game Analytics

## What this skill governs, and why post-game is different from live

Once a match ends, full replay data legitimately reveals what fog-of-war
hid during play — this is exactly `dota-fairplay`'s `POSTGAME_ONLY`
category, and post-game analysis is where that data is *meant* to be
used (unlike live features, which must never touch it — see
`dota-fairplay` and `dota-ml`'s critical rule). That freedom comes with a
different kind of discipline than live coaching: without the tight
attention/time constraints `dota-live-coach` operates under, it's
tempting to show *everything* the data reveals. Resist that — a report
overflowing with statistics is not more useful than a live coach that
spams messages, just slower to become useless.

## What to analyze

- **laning** — lane outcome and its drivers (per `dota-domain`'s lane
  guidance).
- **farm** — farm efficiency relative to role/farm-priority expectations
  (per `dota-domain`'s farm-priority guidance).
- **item timings** — when key items actually completed vs. what timing
  would have been competitive (per `dota-domain`'s item-timing guidance).
- **deaths** — context around each death (was it a reasonable risk, a
  positioning error, a forced trade) rather than just a death count.
- **teamfights** — outcome drivers (per `dota-domain`'s team-fight
  guidance — initiation, target priority, resource state).
- **objectives** — Roshan, tower, high-ground-related decisions and
  outcomes (per `dota-domain`).
- **buyback** — buyback usage/availability at key moments (per
  `dota-domain`'s buyback guidance).
- **power spikes** — whether the player's power-spike windows were used
  effectively, and whether the enemy's were defended against.
- **turning points** — specific moments where the game's trajectory
  measurably shifted, and what drove them.
- **recommendation adherence** — whether the player followed the live
  coach's recommendations (per `dota-live-coach`/`dota-item-recommender`)
  and, where they didn't, whether that deviation helped or hurt — see
  `references/recommendation-adherence.md` for why this needs particular
  care to analyze fairly.

Full analytical guidance for each is in `references/analysis-dimensions.md`.

## Correlation, association, and causality — and why the distinction is mandatory

**Never claim an item caused a win simply because the player bought it
before winning.** This is the single most common and most misleading
mistake a post-game analytics feature can make, and it's worth being
explicit about the three distinct claims involved, since conflating them
is exactly how a false-causal claim slips through:

- **Correlation** — two things co-occurred (item X was in the build,
  the game was won). This is the weakest claim and the easiest to
  measure — and the one most likely to be accidentally presented as if
  it were the strongest.
- **Association** — a statistical relationship holds across a reference
  group (players who bought item X in similar situations won more often
  than those who didn't) — stronger than a single-game correlation, but
  still not causal, because of the same selection-bias mechanism
  `dota-item-recommender`'s `confidence-and-bias.md` already documents
  (players who bought X may have already been in a more favorable
  situation for reasons unrelated to X itself).
- **Causality** — X actually changed the outcome. This is rarely
  directly measurable from observational match data alone (no
  randomized experiment, no controlled counterfactual) — treat causal
  language as something this system almost never gets to use without
  strong, explicit justification, and default to correlation/association
  framing instead. See `references/correlation-vs-causality.md` for
  concrete phrasing guidance and the specific mechanisms that make
  causal claims from this kind of data unreliable.

**Every insight surfaced must be labeled with which of these three it
actually is**, in the language used to present it to the player, not
just in an internal data model — a report that computes the distinction
correctly but presents everything in causal-sounding language ("buying
X won you the game") has still made the mistake this rule exists to
prevent.

## Sample size and confidence

Always consider sample size and confidence before surfacing a
comparison or a claimed pattern. A single game (or a handful of games)
is a very weak basis for any "you tend to..." statement — see
`references/sample-size-and-confidence.md` for concrete guidance
(minimum sample thresholds by claim type, how to communicate uncertainty
to the player, and reuse of `dota-item-recommender`'s/`dota-ml`'s
Bayesian-shrinkage discipline for small-sample player-specific
estimates).

## Prioritize 1-3 actionable insights

Post-game analysis can compute dozens of statistics; the report should
surface **1-3 actionable insights**, not all of them. This is the
post-game analog of `dota-live-coach`'s core rule (hundreds of variables
analyzed, 1-3 actions shown) — the underlying reasoning is the same
(a player who's shown everything learns to ignore all of it), just
applied to a report instead of a live message stream. See
`references/insight-selection.md` for how to select which 1-3 insights
actually make the cut, and where the rest of the computed statistics
should live (available on request/drill-down, never as the report's
primary presentation).

## Comparison groups

Compare the player primarily against players matching, in priority
order:
1. **same hero**
2. **same role**
3. **same bracket**
4. **same patch**

See `references/comparison-groups.md` for why this ordering matters, how
to handle a comparison group that's too sparse at the narrowest level
(fall back gracefully, don't silently widen without saying so), and how
this connects to `dota-data`'s patch/bracket data requirements and
`dota-draft`'s patch-and-bracket-awareness discipline (the same
underlying principle applied to post-game comparison instead of draft
scoring).

## Relationship to other skills

- `dota-fairplay` — `POSTGAME_ONLY` data is legitimately usable here;
  this skill governs using it responsibly, not whether it's allowed.
- `dota-domain` — the strategic vocabulary every analysis dimension is
  built on.
- `dota-item-recommender` — shares the survivorship/selection-bias
  mechanism and the general discipline of not trusting raw outcome
  correlation; `recommendation-adherence.md` ties directly to that
  skill's output.
- `dota-live-coach` — the 1-3-insight rule is this skill's version of
  that skill's core rule, applied to a different medium.
- `dota-data` / `dota-ml` — comparison-group data must be patch-tagged
  and bracket-segmented per `dota-data`'s pipeline rules, and any
  model-based insight-generation is subject to `dota-ml`'s full
  discipline (baseline-first, leakage tests don't apply the same way
  post-game since this data is legitimately available, but calibration
  and sample-size discipline absolutely still do).
