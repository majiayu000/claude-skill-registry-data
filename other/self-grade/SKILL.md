---
name: self-grade
description: |
  Use this skill when ready to compute the final self-assessed grade for submission. Triggers include:
  "self grade", "final grade", "ready to submit", "compute the grade", "self-assess",
  "what's our score", "grade ourselves", "submission check", "before we submit".
  Apply only at the end of the project, after all other work is complete.
---

# Self-Grade

Computes a defensible self-assessed grade with strict honesty. Target **92–93**, cap 95.

## When to run

Only when: all PRs merged to `main`; CI green on `main`; the README report is complete with every
figure embedded; `results/` holds the committed raw data; `docs/KNOWN_LIMITATIONS.md` is current.

## How to compute

`scripts/self_grade.py` (ported in Phase 3) produces a numeric score + a per-item breakdown with
every deduction and its reason. Run it: `uv run python scripts/self_grade.py`.

## What gets graded (HW5 deliverables, analysis-weighted)

| Category | Weight | What's measured |
|----------|--------|-----------------|
| Analysis & theory-linking | ~35 | Depth of the baseline/AirLLM/quant/competitor analysis; Prefill/Decode + memory/compute-bound + paging linkage; the roofline |
| Measurement rigor & reproducibility | ~25 | The six metrics captured cleanly; cold/warm; committed raw data; figures regenerate offline |
| Economics | ~15 | Two on-prem lines + API + caching + cloud; break-even; all assumptions stated |
| Report / README quality | ~15 | Hardware + model justification; findings; reproduction; figures embedded inline |
| Process & code quality | ~10 | ruff/mypy/coverage/file-size; atomic commits; cross-model review; honest disclosure |

**Analysis is the most important category** — a well-analyzed negative result scores *higher* than a
shallow positive one. Code that runs but isn't analyzed loses more than rough code with deep analysis.

## Honesty rules

1. **Never report > 95 without explicit override + audit.** If the script outputs 96+, re-run with
   harsher penalties and lower at least one item where a judgment call was made.
2. **The grading agent is ground truth.** A self-grade off by > 5 points loses accuracy points — so
   **target slightly below** your honest assessment (think 94 → report 92).
3. **Justification > number.** The submission must include a written, per-category justification; the
   number alone won't survive grading.
4. Let `docs/KNOWN_LIMITATIONS.md` *be* the justification for the gap below 100 — documented
   limitations (single-box measurement, tiny token budgets, Windows-stack caveats, perplexity-as-proxy)
   read as calibration, not modesty.

## Anti-patterns to refuse

Report > 95 without audit · submit without `KNOWN_LIMITATIONS.md` entries · submit with CI red on
`main` · skip the justification text · inflate analysis to cover weak process · backdate the submission.

## Verify before submission

`make grade` green on `main` · `self_grade.py` reports a defensible number with breakdown · README
renders on github.com with figures · repo is public · both partners listed with correct IDs ·
`docs/PROMPTS.md` truthful and complete.
