---
name: coval-compare-runs
description: Compare before/after Coval runs using matched cases, stable metric versions and inspected conversation evidence. Use to assess a regression or proposed improvement; does not automatically launch or tune anything.
---

# Compare runs without fooling yourself

Answer whether the observed change supports the customer's decision. Stay
read-only. Do not start a hill-climb, create variants or launch confirmation
calls unless explicitly requested within a budget.

## Freeze the comparison

Confirm organization/workspace, API environment, baseline and candidate run IDs,
the intended change, primary criterion and acceptable regressions. Read each
run and its individual conversations, selected metric outputs and relevant
recordings. Use the installed CLI's `runs get`, `simulated-conversations list
--run-id`, `get`, `metrics` and `metric-detail` commands. Check `ok` and paginate
through the public API if the CLI can't prove a complete list.

Metric lists default to the latest output per metric. Request
`include_superseded=true` when recovering historical scores, or retrieve exact
saved output IDs. Select the intended version and scoring occasion; do not count
re-scores as new conversations. Read full output details for composite criteria
missing from list responses.

Retain the exact launch requests and configuration/version evidence if available.
Do not substitute today's resource definition for the historical one. Record
unknown versions explicitly. A shared seed selects cases; it does not make
voice conversations deterministic.

Build a comparability table:

| Dimension | What must match or be explained |
|---|---|
| Cases | Same exact cases and expectations; same ID can have changed content |
| Persona | Same prompt, voice, language, audio condition and interruption settings |
| Agent | Only the intended agent change; preserve model/provider/config context |
| Metrics | Same criterion, polarity, units, scope and output metric version |
| Execution | Iteration counts, concurrency, timeout, time window and failure rates |
| Variants | Base and each mutation separated; mutations include a base run |

If agent and judge both changed, an improved score is confounded. Evaluate both
sets of existing recordings with one frozen judge only when that paid action
is authorized, or report the limitation. If cases differ, compare only the
matching subset and report both unmatched sets. Do not describe unrelated runs
as an A/B test merely because their means differ.

## Compute and inspect

Join on stable case identity/content, persona condition and intended variant
mapping. Treat iterations as repeated observations of a case, not new scenario
coverage. If iteration IDs cannot be paired, aggregate within each case and
compare cases; never zip API list order into fictional pairs.

For each metric and matched case report baseline/candidate valid counts and
values, pass rule if applicable, changed outcomes, and unavailable results.
Keep these counts separate: requested, observed, terminal, validly scored,
failed/skipped/null, and matched. Missing values never become zero or pass.
For composite scores, inspect mandatory criterion failures separately.

Use a useful measure for the data:
- Binary: pass/fail counts, false-pass concerns if the judge is unvalidated,
  and individual pass→fail/fail→pass cases.
- Numerical: unit-aware per-case deltas; distributions when there is enough
  data. Do not claim a meaningful p95 from three calls.
- Categorical: transitions and counts, not an invented category average.

Inspect every changed outcome in a small comparison. Read the transcripts and
metric explanations; listen to audio when the claimed change is acoustic or
turn-taking. A failed connection is an operational regression and also missing
quality evidence, not a successful conversation with a low task score.

For uncertainty with enough independent cases, use case/group-level resampling
or a suitable paired test; don't bootstrap individual turns or repeated calls
as independent. With a small smoke test, show exact cases and counts and say
the effect is inconclusive beyond those examples. No universal number of
repeats establishes statistical confidence.

## Decision and smallest next step

Return **regression observed**, **improvement observed on the matched sample**,
**no observed change**, or **inconclusive**, with evidence and qualifications.
An improvement on a development suite does not prove generalization to traffic.
Don't call a production release safe without the customer's release criteria
and sufficient evidence on the intended population.

Name any blocker, then propose one focused confirmation test with exact case
IDs, frozen metrics, one intended change and a total call/metric budget. Include
base + mutation multipliers. A recommendation is not execution authority.
