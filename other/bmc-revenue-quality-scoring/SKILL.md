---
name: bmc-revenue-quality-scoring
description: "Scores each Revenue Stream and its matching Customer Relationship on a -3 to +3 resilience scale — recurring/contractual vs. one-off/unpredictable — instead of raw size, to reveal how fragile a model's top line actually is before it's mistaken for strength."
---

# BMC Revenue Quality Scoring

## Purpose

Two business models with identical revenue totals can have completely
different resilience: one built on multi-year contracts, the other on
unpredictable one-off deals that require constant new selling effort to
replace. The BMC's Revenue Streams block, filled in as a simple list,
hides this difference entirely. This skill scores revenue quality
directly, using a rubric, so "how much revenue" and "how resilient is
this revenue" are answered as two separate questions — not conflated
into one number that looks reassuring but isn't. Use once Revenue
Streams has at least a first draft, ideally right alongside
`bmc-economic-prototyping`.

## Anchored in research

Directly grounded in Strategyzer's own published concept, ["Revenue
Resilience"](https://www.strategyzer.com/library/revenue-resilience) —
from Alexander Osterwalder's team, the same lineage as the BMC itself.
The underlying point (recurring revenue commands materially higher
valuation and is more resilient than one-off transactional revenue at
identical totals) is corroborated independently across
valuation-practice sources: recurring-revenue businesses are commonly
valued at meaningfully higher multiples of EBITDA than one-time-sale
businesses with identical earnings, precisely because the earnings are
more predictable.

## Method

1. **List every distinct revenue stream on the canvas separately** —
   don't blend "product sales" and "services revenue" into one line if
   they behave differently; each needs its own score.
2. **Score each stream from -3 to +3** using this rubric:
   - **+3** — fully contractual, multi-period revenue with automatic
     renewal (subscription, retainer, multi-year contract with
     auto-renew).
   - **+2** — strong repeat revenue with high historical renewal rates,
     but not contractually locked (a loyal customer who reorders
     predictably without a binding agreement).
   - **+1** — usage-based or metered revenue from an established,
     ongoing relationship (billed by consumption, but the relationship
     itself is durable).
   - **0** — mixed or genuinely uncertain — a new stream with no track
     record yet, or one that's part-recurring, part-opportunistic.
   - **-1** — opportunistic repeat business — customers come back, but
     unpredictably, with no structural reason they will.
   - **-2** — project-based or one-off revenue requiring significant new
     sales effort each time, even from existing customers.
   - **-3** — pure one-off, unpredictable, high-sales-effort
     transactions with no repeat mechanism at all.
3. **Weight each score by its share of total revenue** to get a blended
   Revenue Resilience Score: `Σ(stream score × % of total revenue)`.
   A model that's 80% one-off revenue (-2) and 20% subscription (+3)
   scores roughly -1, even if the subscription piece looks impressive on
   its own — the blended number reflects what the business actually is,
   not its best feature.
4. **Interpret the blended score:**
   - **+1.5 to +3** — genuinely resilient revenue base; a downturn or a
     slow sales quarter won't immediately threaten survival.
   - **0 to +1.4** — mixed; identify which specific streams are dragging
     the score down and treat converting them as a real priority, not a
     someday item.
   - **Below 0** — the business has to re-win a large share of its
     revenue every period; this is a structural fragility, not a
     temporary sales problem, and it should be named as such to
     stakeholders rather than framed as a growth challenge alone.
5. **For streams scoring negative that are still a large share of
   revenue, generate specific conversion ideas** — don't just flag the
   problem, propose the fix. Common conversions: project fees →
   retainer; one-time purchase → subscription with an ongoing
   consumable/service wrapped in; per-transaction fee → tiered
   membership. The pack's own pattern library has several ready-made
   patterns for exactly this: see `bmc-innovation-pattern-matching` and
   look specifically at the `financial.rev.*` pattern group in
   `../../references/bmc-innovation-pattern-library.md` (e.g. continuous
   learning / subscription-wrapped patterns) for structured conversion
   options rather than inventing one from scratch.
6. **Cross-check against Customer Relationships (the Hook Rule).** A
   stream scored +3 (contractual/recurring) should have a matching
   relationship type — ongoing, managed, or automated recurring
   engagement. If the Customer Relationships block still describes a
   purely transactional, one-touch interaction, that's a contradiction
   worth raising directly — see `bmc-canvas-diagnostic-reading`'s DR-01
   Hook Rule, which this check is a direct application of.

## What this skill does NOT do

- Doesn't replace a real financial model — the -3 to +3 scale is a
  fast diagnostic lens, not a substitute for `business-case-and-analysis/roi-npv-sensitivity-model`
  when the decision actually depends on precise numbers.
- Doesn't say a model with negative revenue quality is a bad business —
  some genuinely good businesses run on project/one-off revenue by
  nature (bespoke consulting, custom manufacturing); the score tells you
  the resilience profile to plan around, not a verdict on viability.
- Doesn't generate the conversion ideas in Step 5 for you beyond
  pointing at the pattern library — matching a specific pattern to a
  specific business still needs `bmc-innovation-pattern-matching`'s full
  method.

## Refinement notes

- What's the most common revenue-quality blind spot you see clients
  walk in with — where they think their revenue is more resilient than
  the scoring reveals?
- Which stream-conversion moves (project → retainer, product → 
  subscription) have you actually seen work in practice, and which ones
  sound good but fail with real clients?
- Is -3 to +3 the right scale width, or does your own practice use a
  finer or coarser one?

## Continue from here

- Use alongside: `bmc-economic-prototyping/SKILL.md` — score the streams
  this skill is pricing.
- Uses: `bmc-innovation-pattern-matching/SKILL.md` and
  `../../references/bmc-innovation-pattern-library.md`'s `financial.rev.*`
  patterns for conversion ideas.
- Cross-checks: `bmc-canvas-diagnostic-reading/SKILL.md`'s DR-01 Hook
  Rule.
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/bmc-source-material-notes.md` — source material background
- `../../references/bmc-resilience-heuristics-research.md` — selection and grounding notes for this skill and its siblings
- `../../references/bmc-innovation-pattern-library.md` — pattern library used for stream-conversion ideas
- `../../CLAUDE.md` — this pack's shared guardrails
