---
name: assessing-delivery-performance
kind: skill
status: ready
provenance:
  principles:
  - P036
  - P056
  - P067
  - P105
  - P003
  - P004
  claims:
  - C00037
  - C00038
  - C00039
  - C00040
  - C00041
  - C00044
  - C00045
  - C00046
  - C00047
  - C00064
  - C00031
  - C00032
  evidence:
  - E00022
  - E00023
  - E00024
  - E00025
  - E00026
  - E00029
  - E00030
  - E00031
  - E00032
  - E00043
  - E00016
  - E00017
  source_anchors:
  - 9d4b1cf206e5-c0002
  - 9d4b1cf206e5-c0003
  - 9d4b1cf206e5-c0001
  authored_from_digest: 16cd9e421e52c53210fd92811298cebad55b3c2ef988b3557a0cd741a6aaddfc
---

# Assessing delivery performance

## Purpose

Measure how well a team delivers software using the four key metrics, and read the result
correctly: throughput and stability are pursued **together**, because the research finds no
trade-off between delivery speed and reliability (P001). The job of this skill is to turn a vague
"are we fast / are we safe?" question into a small, defensible scorecard and a single highest-leverage
next move — never to bless trading one dimension away for the other.

## When to use

- A team wants to measure or improve software delivery performance and does not yet have an
  agreed metric set.
- Leadership wants to justify investment in delivery capability, or treats delivery as an IT cost
  rather than a competitive capability.
- A team believes it must choose between moving fast and staying stable, and wants that framing
  tested against the evidence.
- A team submits its current dashboard or KPIs for review (the `review` mode) or asks whether it
  meets a performance bar (the `validate` mode).

Do **not** use it where a regulated context mandates a specific external metric set that overrides
team metrics — surface the conflict and defer to the accountable owner.

## Procedure

1. **Anchor on the four key metrics.** Capture exactly four, two per dimension (CL016):
   - *Throughput* — **deployment frequency** and **lead time for changes** (commit to running in
     production).
   - *Stability* — **change failure rate** (share of changes that need remediation) and **time to
     restore service** after a failure.
   Reject substitutes that measure activity rather than outcome (e.g. story points, raw commit
   counts); they do not capture delivery performance.
2. **Establish the current baseline.** Get a real number or honest estimate for each of the four.
   If a metric cannot be measured at all, that gap *is* the first finding — you cannot improve what
   is invisible.
3. **Read throughput and stability together, never in opposition.** State both dimensions in one
   verdict. If a team is fast but unstable, or stable but slow, name it as an imbalance to close —
   not as a deliberate, acceptable trade. The data shows the highest performers achieve superior
   throughput **and** stability at once (CL017); a recommendation to sacrifice one for the other
   contradicts the evidence and is a forbidden output.
4. **Connect to outcomes when justifying investment.** When the question is "why fund this?",
   ground it in the finding that delivery performance statistically predicts organisational
   outcomes — profitability, productivity, market share — so it is a competitive capability, not a
   cost centre (CL018). Frame it as predictive/correlational evidence, not a guarantee.
5. **Name one highest-leverage move.** Diagnose which single metric is the binding constraint and
   route to the capability that moves it, citing the sibling skill:
   - Long lead time or low deploy frequency → smaller batches, trunk-based work, automated pipeline
     (`designing-deployment-pipelines`).
   - High change failure rate → progressive delivery and tested rollback
     (`planning-progressive-delivery`).
   - Slow time to restore → reliability targets, symptom/burn-rate alerting, sustainable on-call
     (`defining-slos-and-error-budgets`, `reducing-toil-and-on-call-load`).
6. **For `compare` requests,** score each option against all four metrics plus a stated context
   (team size, coupling, risk), and recommend the one that improves throughput without trading
   away stability, with the qualification that the bands are context-relative.

## Inputs

- The delivery question in scope and how the team measures today (dashboards, KPIs, or "nothing").
- Context on the system and team: architecture and coupling, team size, deployment process,
  production vs pre-production.
- Whether the ask is to advise, review an existing metric set, validate against a bar, or compare
  options.

## Output

A four-metric scorecard (current state per metric, with gaps named where a metric is unmeasured),
a combined throughput-and-stability verdict, and one highest-leverage next move tied to a sibling
skill. For `validate`, a pass-or-gap line per metric. Every recommendation names P001 and flags
that speed and stability rise together.

## References

- `references/dora-four-key-metrics-reference.md` — the four metrics, their dimension, and what
  each measures.
- Sibling skills: `designing-deployment-pipelines`, `planning-progressive-delivery`,
  `defining-slos-and-error-budgets`, `reducing-toil-and-on-call-load`.

## Provenance

Derived from principle P001 (claims CL016, CL017, CL018; evidence EV016–EV018) in
`accelerate-the-scien-7241289b` (rights: distillation-only — paraphrase, no verbatim quotation).
The four-metric framing and the no-trade-off finding are correlational results of the State of
DevOps survey program; this skill states them as such and does not promise causation.
