---
name: eval-harness
description: |
  Use this skill when building, running, or reasoning about the project's evals — the layer
  that proves the benchmark *behaves correctly* (the analysis is sound and evidenced), distinct
  from tests that prove the code *runs*. Triggers: "eval", "structural eval", "validity check",
  "is the analysis sound", "prove the result", "figure has backing data", "does the harness
  capture everything". Apply whenever a change could affect whether the system produces *valid,
  evidenced* results, not just whether it executes.
---

# Eval Harness (validity beyond tests)

Tests prove the code *runs*; **evals** prove the system produces **valid, evidenced** results
(`CLAUDE.md §5`, D11). HW5 has **no behavioural-LLM evals** (there's no debate/agent to judge) —
instead two things carry validity: keyless **structural evals** in CI, and the **committed Tier-2
measurement evidence**.

## Layer 1 — structural evals (keyless, deterministic, in CI)

Code-based invariants on mocked/fixture data. Live under `tests/evals/structural/`, run on every
push, no GPU/key/network. Each must hold on **every** run (`pass^k = 100%`):

1. **harness-captures-all-fields** — a `mock`-runner `RunResult` has every schema field populated
   (TTFT, ITL series, TPOT, peak VRAM, both RAM numbers, GPU energy, runtime, phase); the baseline
   OOM case sets `ok:false` + `error`.
2. **breakeven-monotonic** — cumulative on-prem and API cost curves are non-decreasing in volume; the
   crossover (if any) is unique.
3. **roofline-points-correct** — each operating point's achieved FLOP/s and arithmetic intensity are
   recomputed from `(param_count, throughput, bytes/weight)` and match the plotted value; AirLLM-FP16
   lands on the NVMe ceiling, NF4-warm on PCIe/RAM.
4. **figure-has-backing-data** (`scripts/check_raw_data.py`) — every figure in `figures/` traces to
   rows in `results/`; no figure without raw numbers.
5. **report-complete** (`scripts/check_report.py`) — the README has every required section + every
   referenced figure actually embedded.

## Layer 2 — measurement evidence (Tier-2, hardware-bound, committed)

The real model runs can't be reproduced in CI. Validity comes from **committing the raw JSON** under
`results/` plus the exact commands, pinned env, and driver/CUDA versions. A **negative result** (AirLLM
loses) is fully evidenced this way — the evidence trail matters more than the outcome.

## How to run

```bash
uv run pytest tests/evals/structural -v      # keyless, fast — what CI runs
uv run python scripts/check_report.py        # README completeness
uv run python scripts/check_raw_data.py      # figure ↔ raw-data backing
```

## The discipline (non-negotiable)

A failing structural eval means the analysis pipeline is wrong — **fix before merge**. A result that
can't be backed by committed raw data is **not reported**, or is honestly flagged in
`docs/KNOWN_LIMITATIONS.md`. Never delete an eval to make the suite green; never plot a number without
its backing row.
