---
name: researchforge-results
description: Summarize a run's results — ranking, Pareto trade-offs, constraint violations, and rejected experiments — grounded strictly in recorded measurements. Use when the user asks how the experiments went or which variant won.
---

# Read and explain results

```bash
researchforge results show <run-id> --json
```

The JSON contains everything you may talk about: per-experiment measured
metrics, baseline deltas, constraint checks, the ranking, the Pareto
frontier over direction-inferable metrics, trade-off notes, and caveats.

How to summarize honestly:

- quote **only** numbers present in the JSON; never estimate, extrapolate,
  or fill gaps from memory — if a number is not recorded, say so;
- include the losers: rejected and failed experiments, with their recorded
  reasons, are first-class findings;
- surface every caveat the engine attached (including the one-off-result
  caveat) — a single full-benchmark win is *promising*, not *validated*;
- when candidates trade off (e.g. quality vs latency), present the frontier
  and let the user choose; do not silently pick for them.

For a visual overview, `researchforge dashboard` writes a self-contained
HTML dashboard (charts of every experiment vs the baseline, the trade-off
scatter with the constraint line, the funnel, and validation spread) to
`.researchforge/reports/dashboard.html` — offer `researchforge dashboard
--open` when the user wants to *see* the results; it is built from the same
recorded data and nothing else. For a *live* view while runs are in
progress, `researchforge serve --open` starts a local read-only monitor
(requires `pip install "researchforge[serve]"`).

If a candidate looks like a winner, the next step is the
researchforge-validate skill — repeated runs are what earn the word
"validated".

## Rules

- The Python engine is the boundary: never work around a validation error, a
  protected path, or an approval gate — fix the artifact or ask the user.
- Approvals belong to the user: never pass `--yes` or type a confirmation
  unless the user explicitly approved that step in this conversation.
- Ground every summary in stored data: quote only numbers returned by
  `--json` output or files under `.researchforge/` — never invent metrics.
