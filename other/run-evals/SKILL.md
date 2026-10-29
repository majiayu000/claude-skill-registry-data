---
name: run-evals
description: Run the software-factory eval suite from the repo root — deterministic stub mode (the CI PR gate), single-case filtering, full LLM-judge mode, baseline regression comparison, and trend-history appends. Use when asked to "run the evals", "check the eval baseline", before committing prompt/constitution/golden-case changes, or when investigating an eval regression.
---

# Run the evals

Run every command from the repo root. Golden cases live in `evals/golden/*.md`; the committed baseline is `evals/baseline.json`. See `evals/README.md` for the golden-case file format.

## Quick check — deterministic stub mode (start here)

```bash
npm run eval -- --stub
```

Runs the deterministic stub subset at zero model cost — the exact check CI runs on every PR (and the last step of `bash scripts/verify.sh`). Run it before committing any prompt, skill, constitution, or golden-set change. Stub mode never invokes the LLM judge. Exit code is non-zero if any case fails.

## Run a single case

```bash
npm run eval -- --stub --filter <id-substring> --no-judge
```

`--filter` keeps cases whose id contains the substring. The canonical smoke case is:

```bash
npm run eval -- --stub --filter local-small-first-green --no-judge
```

## Full run — real harness + LLM judge (local/nightly, costs money)

```bash
npm run eval
```

Runs all golden cases through the real model router with the LLM judge. Requires the provider CLIs/keys that `packages/config` routes to. Useful flags: `--no-judge` (skip the judge), `--judge-k <n>` (judge each case n times), `--plan-model <id>` / `--judge-model <id>` (pin models), `--report eval-report.json` (write the JSON summary), `--dir <path>` (alternate case directory). Flags not listed here are rejected.

## Baseline comparison (regression gate)

```bash
npm run eval -- --baseline evals/baseline.json
```

Prints `NOTE:` and `REGRESSION:` lines and exits 1 if the run regresses against the committed baseline. To intentionally refresh the baseline after an accepted change:

```bash
npm run eval -- --write-baseline evals/baseline.json
```

This preserves the existing `tolerance` and `budgets` fields. Commit the updated `evals/baseline.json` in the same PR and say why it moved.

## Trend history

```bash
npm run eval -- --report eval-report.json
npm run eval-history -- --report eval-report.json --history history.jsonl
```

`eval-history` appends a dated record to the JSONL history (flags: `--run-url`, `--date YYYY-MM-DD`). If the report file is missing it prints a skip message and exits 0.

## Reading the output

Each run prints a per-case table, then one summary line: `pass-rate P/T (…%) · route-accuracy …% (C/A) · est. cost $… · total latency …s`. Non-zero exit means a failed case or a baseline regression — fix or explain before committing.

## Readiness suite

```bash
npm run eval -- --stub --suite readiness
npm run eval -- --stub --suite readiness --baseline evals/readiness-baseline.json
npm run eval -- --suite readiness --readiness-model <id> --judge-model <id> --baseline evals/readiness-baseline.json
```

`--suite plan|readiness` selects the suite (default `plan`; any other value is rejected). The readiness suite runs `evals/readiness/*.md` through the `readiness_judge` route, and `--readiness-model <id>` pins the model for it. The stub run is also in `bash scripts/verify.sh` and CI. It prints accuracy, false-ready, false-not-ready, must-ask and judge-errors. Any rise in false-ready fails the baseline comparison; false-not-ready tolerates 0.10. Refresh with `--write-baseline evals/readiness-baseline.json`. Case format: `evals/README.md`.
