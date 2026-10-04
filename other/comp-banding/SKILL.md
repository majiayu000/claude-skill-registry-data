---
model_tier: inherit
name: comp-banding
description: "Use when designing levels, comp bands, equity-vs-cash, geo adjustments, or raise vs promotion vs market correction. Triggers on 'set our comp bands', 'is this raise market'."
status: active
tier: senior
domain: process
context_spine: [org-stage, customer-segment, regulatory-regime]
workspaces:
  - ops
packs:
  - ops-people
trust:
  level: professional
install:
  removable: true
---

# comp-banding

## When to use

- Levels and comp bands need a first pass (or an annual refresh) and the question is *what shape the ladder takes*, *where the bands sit*, and *how cash / equity trade*.
- A specific compensation decision crosses the desk (counter-offer, retention, market correction, promotion, geo move) and the question is *which lever is the right one*.
- A funding event, geo expansion, or org-stage transition makes the existing comp shape misfit reality.

Do NOT use as a payroll / equity-administration substitute (this skill produces the cognition; payroll / cap-table tools implement), as an individual-performance review (route to Q4 `perf-feedback-craft`), or for hiring-loop / sourcing design (separate skill area).

## Cognition cluster

- **Mental model 1 — First principles.** Strip every comp question to: *what behavior are we paying for, over what horizon, with what risk-bearing?* Cash pays for present effort; equity pays for future co-built value with risk; bonus pays for outcome-linked behavior. Mixing the levers without first-principles intent produces confusion. See [`mental-models.md`](../../../docs/contracts/mental-models.md) § 1.
- **Mental model 28 — Inversion.** *"What comp shape would force our best people to leave?"* Inversion surfaces the load-bearing risks (condensation at senior levels, equity refresh gaps, geo arbitrage that punishes loyalty).
- **Mental model 26 — Optionality.** Each comp lever preserves or forecloses future options. Above-band offers preserve hire optionality but foreclose internal-equity optionality. Equity-heavy mix preserves cash runway but forecloses people who need liquidity. Read every move as an optionality trade.
- **Mental model 21 — Second-order thinking.** A raise to one person ripples (perceived parity, retention pressure on peers, expectation-setting for next cycle). A band shift ripples (new-hire offers anchor higher, internal expectations re-anchor). Comp moves rarely stay isolated.
- **Context-spine — org-stage + customer-segment + regulatory-regime.** Read **org-stage** for what's affordable and credible (pre-seed: cash-light, equity-heavy; growth: cash-competitive at 50th–75th; late: cash-led, equity less load-bearing). Read **customer-segment** for which talent pool we compete in (enterprise sales needs enterprise pay shape). Read **regulatory-regime** for pay-transparency / disclosure obligations (EU directive, CA / CO / NY state laws).

## Cross-wing handoff

- Composed downstream of Q1 `org-design` — the level / band shape follows the structure decision; comp without a structure is rootless.
- Hands off to Q3 `onboarding-program` for the time-to-productivity expectation that comp shape implies.
- Hands off to O1 `unit-economics-modeling` for the OpEx impact of comp decisions on burn / runway.
- Composed when J1 `regulatory-regime` flags pay-transparency obligations.

## Procedure

### Step 0: Inspect intent before framing the comp question

Before designing or adjusting bands, name:

1. *What behavior are we paying for?* (retention, attraction at top of market, alignment to long-term outcome, performance leverage).
2. *Over what horizon?* (this quarter, this year, this 4-year vest cycle).
3. *Whose risk are we asking the person to bear?* (cash risk = ours; equity risk = theirs; bonus-on-outcome = shared).

The intent gates which lever moves; without it, comp decisions chase symptoms.

### Step 1: Design the level ladder

Levels are the spine; bands attach to levels, not the other way around:

1. **Ladder breadth** — name how many levels each track has (IC vs management; eng / design / PM / sales / ops separate or unified).
2. **Level criteria** — what behaviors and scope distinguish L4 from L5 from L6. Force concrete scope language, not adjective stacks ("strong" → "leads a 3–5 person workstream end-to-end").
3. **Dual-track parity** — IC vs management at equivalent levels should pay parity within a small band, or the IC track erodes silently.
4. **Skip-level distance** — a step from L4 to L5 is usually 12–24 months of demonstrated growth; smaller steps inflate the ladder.

A ladder where every adjective is "strong" is a placebo; force scope and behavior language.

### Step 2: Place the bands

For each level × function × geo, name:

1. **Cash band** — 25th / 50th / 75th / 90th percentile against a named market reference (one named comp dataset, e.g. Pave / Radford / OptionImpact, not "feels right").
2. **Equity band** — initial grant + refresh cadence. Equity in % of company at grant for early stage; in $ value or share count for later stage.
3. **Bonus / variable** — applies primarily to sales / GTM; not appropriate as standard for eng / product without an explicit reason.
4. **Total comp** — cash + (equity ÷ vest years) + expected bonus. Compare TC against market reference, not just base.

Where to sit: pre-seed / seed = below 50th cash, above 75th equity; Series A / B = 50th–75th cash, above 50th equity; growth = 50th–75th cash, 50th equity; late = 75th cash, below 50th equity.

### Step 3: Geo and remote shape

Pick one explicit policy; ambiguity here destroys trust:

1. **Same-band-everywhere** — single global band; expensive but stops geo arbitrage gaming.
2. **Tiered-by-geo** — 2–4 tiers (e.g. tier 1: SF/NYC; tier 2: other US metro; tier 3: rest of US; tier 4: EU; tier 5: rest of world). Document tier assignments transparently.
3. **Cost-of-living indexed** — per-city multiplier from a published index (Numbeo / similar). Most transparent but creates fairness debates for premium-cost low-pay cities.

A move within the same role across tiers needs a documented rule (re-band, hold harmless, partial adjust).

### Step 4: Decide the lever for a specific case

For a specific decision (raise, retention, market correction, promotion, counter-offer), pick exactly one primary lever:

1. **Promotion** — when scope has grown to the next level; comp follows level. Wrong lever for "retention without scope growth".
2. **Market correction** — when the person's comp drifted below band due to market movement; not contingent on performance. Apply to a cohort, not just the squeaky wheel.
3. **Retention / counter-offer** — when external pull risks loss; size the cost-of-loss honestly (re-hire cost, knowledge loss, team morale). Use sparingly; each one re-prices the next.
4. **Performance raise** — within band, for demonstrated above-expectation impact. Documented in performance evidence.
5. **Equity refresh** — for retention beyond initial vest; typically annual for high-impact talent past year 2.

Mixing levers ("a raise AND a promotion AND a refresh") confuses signal and inflates anchor for next cycle.

### Step 5: Validate the comp decision before emitting

Before producing the artifact, verify three things:

1. **Intent confirmed** — confirm Step 0 named the behavior, horizon, and risk-bearer; un-named intent means the lever is chosen on vibes and must be re-run.
2. **Lever-vs-symptom check** — assert the chosen lever in Step 4 matches the diagnosed root cause; using promotion for retention without scope growth is canonical mis-use and fails the check.
3. **Ripple sized** — verify the second-order ripple (peer parity, anchor for next-hire offers, internal-equity impact) is sized; un-sized ripples blow up at the next review cycle.

All three must pass. If any fails, return to the failing step.

### Step 6: Emit the comp artifact

Produce the comp-banding artifact for the leadership decision-maker and / or the specific compensation case file. For band-design exercises, emit the ladder + bands + geo policy + lever-decision tree. For individual decisions, emit the diagnosed root cause + chosen lever + ripple-sized impact.

## Related Skills

**WHEN to use this**

- First-pass level ladder + comp band construction.
- Annual comp refresh against market movement.
- Individual case decisions (raise, retention, promotion, geo move, counter-offer).
- Funding-event / org-stage transition comp re-shape.

**WHEN NOT to use this**

- Performance / individual-feedback work — route to [`perf-feedback-craft`](../perf-feedback-craft/SKILL.md) (Q4).
- Org / team structure decisions — route to [`org-design`](../org-design/SKILL.md) (Q1).
- Onboarding / time-to-productivity — route to [`onboarding-program`](../onboarding-program/SKILL.md) (Q3).
- Compensation-platform admin (Pave / Carta / Sequoia) — out of scope.

## When the agent should load this

- "Set our comp bands."
- "Is this raise market?"
- "Promotion or market correction?"
- "How do we handle geo for remote hires?"
- "Wie banden wir die Levels?"

## Output

1. **`level-ladder.md`** — tracks × levels × scope-and-behavior criteria × dual-track parity check.
2. **`comp-bands.md`** — level × function × geo × cash / equity / variable bands referenced to a named market dataset.
3. **`geo-policy.md`** — same-band / tiered / COL-indexed + tier assignments + move-across-tier rules.
4. **`lever-decision.md`** *(per-case)* — diagnosed root cause × chosen lever × ripple sizing × counter-anchor for next cycle.

## Gotcha

- "Strong" / "senior" / "leads" without scope is a placebo level ladder. Force concrete language.
- IC and management parity at equivalent levels matters more than people say; ICs notice within a quarter.
- Counter-offers always cost more than they look on paper; they re-anchor the next person who threatens to leave.
- Pay transparency laws are not optional and not consistent across geos; a band that looks fine in one state can be a posting violation in another.

## Do NOT

- Do NOT design bands without a named market reference dataset; "feels right" bands are unfalsifiable and erode trust.
- Do NOT promote as a retention tactic without genuine scope growth; this is the canonical inflation mechanism.
- Do NOT skip the ripple sizing; isolated comp moves are rare in practice.

## Runnable example

Series-B SaaS, 80 people, eng lead requests a 25 % raise for a senior eng with a competing offer.

- Step 0 — Intent: retention; horizon = next 12 months; risk = loss of person + 6 months re-hire cost.
- Step 1 — Ladder check: person is L5 senior; scope hasn't grown to L6 staff. Promotion is not the right lever.
- Step 2 — Band check: current cash sits at 55th percentile per Pave; competing offer is at 90th. Band ceiling for L5 is 75th. 25 % raise would push above the L5 band ceiling.
- Step 3 — Geo: person is remote tier 2; offer is remote tier 1. Tier-policy check: company policy allows tier 1 only on relocation; offer is staying tier 2.
- Step 4 — Lever: not promotion (no scope growth), not full retention to competing offer (breaches L5 band ceiling), not market correction (already at 55th). Recommended lever: partial cash raise to 70th of L5 band + equity refresh sized to span 3-year retention horizon + named scope-growth path with explicit L6 promotion criteria over next 12–18 months.
- Step 5 — Validate: intent named (retention with future scope growth as anchor); lever matches root cause without breaking ladder; ripple sized (two peer L5s are at 50th, will need parity correction within 6 months — budget that now).
- Step 6 — Emit lever-decision artifact for VP Eng + finance approval; document scope-growth path in the perf-feedback system for the next review cycle.
