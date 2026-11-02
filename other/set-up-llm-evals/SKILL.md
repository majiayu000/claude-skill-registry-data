---
name: set-up-llm-evals
description: Use when an LLM feature ships on vibes — golden datasets in the repo, deterministic checks first, an LLM judge with a rubric calibrated against human labels, a small CI regression gate, a cost budget and a results history that survives a model or prompt change.
---

# Set Up LLM Evals

An eval is a test suite for behaviour you cannot assert with `===`. Without one, every prompt edit, model upgrade or retrieval tweak is a guess, and a regression is found by a user. This skill sets up the smallest harness that catches real regressions: a golden set in the repo, checks that run through the same seam as production, a gate in CI and a record over time.

## 1. Audit current state

Read `.claude/stack-profile.md` (`languages`, `tests`, `ci`, `ai`). If absent, detect per [stack-profile.md](../../core/_shared/stack-profile.md). Change nothing yet:

```bash
ls evals evals/datasets prompts config/llm.models.json 2>/dev/null
grep -rln "promptfoo\|inspect_ai\|braintrust\|deepeval\|ragas" . --include=*.json --include=*.yaml --include=*.toml --include=*.ts --include=*.py 2>/dev/null | grep -v node_modules | head
grep -rn "eval" .github/workflows 2>/dev/null | head
ls src/platform/llm 2>/dev/null                        # the seam: evals call the same code path as production
git log --oneline -- prompts config/llm.models.json | head   # prompt and model changes that shipped without an eval
```

Report: which features call a model, which have a golden set, whether any check runs in CI, prompt or model changes made without a result, and whether failures seen in production became cases.

## 2. Decide what to do

- No seam → run [build-llm-seam](../build-llm-seam/SKILL.md) first; an eval that bypasses the seam tests something that never runs in production.
- No golden set → create `evals/datasets/<task>-gate.jsonl` with 20 to 30 cases and the deterministic checks (steps 5–6). Judge later.
- Golden set but no gate → add the runner, thresholds and CI job (step 6).
- A judge exists but was never compared with human labels → calibrate it (step 7) before trusting any number it produces.
- Retrieval features → add the retrieval eval from [build-rag-pipeline](../build-rag-pipeline/SKILL.md) first.
- All present and `Verify` passes → "already in place".

## 3. Detect the track

| Signal | Branch |
|---|---|
| TypeScript service (default) | In-repo harness: [eval-code.md](./eval-code.md), runs with Vitest and `tsx`, calls the seam |
| Python service | Inspect AI (MIT): [eval-code.md](./eval-code.md#python-inspect-ai); the harness there is a port-free alternative |
| Existing `promptfooconfig.yaml` | Keep it; add the golden set and the gate rules around it. Do not run two harnesses for one task |
| Team wants a hosted UI, online scoring, shared experiment history | Braintrust or similar; keep the dataset files in the repo as the source of truth |

Why the default is a small in-repo harness rather than a tool: [eval-patterns.md](./eval-patterns.md#rule-the-harness-is-a-small-in-repo-runner-on-the-production-seam).

## 4. Install only what's missing

```bash
pnpm add -D vitest tsx                 # TypeScript (zod is already a dependency of the seam)
uv add --dev inspect-ai                # Python track
```

No other dependency: metrics are a few functions, results are JSONL.

## 5. Generate the seams

```
evals/
  datasets/<task>-gate.jsonl     # 20-30 frozen cases: the PR gate (deterministic only)
  datasets/<task>-full.jsonl     # 100+ cases: nightly and on prompt, model or config changes (judged)
  datasets/labels-<task>.jsonl   # human pass/fail labels for judge calibration
  lib/metrics.ts, lib/run.ts     # recall@k, MRR, kappa; runner, checks, gate
  gate.ts                        # CLI: run a dataset, apply thresholds, set the exit code
  thresholds.json                # floor, allowed drop vs baseline, budget per dataset
  history.jsonl                  # one line per recorded run (committed)
  results/                       # per-run JSONL (gitignored, CI artifact)
prompts/eval-judge.md            # the rubric, versioned like any prompt
```

Code: [eval-code.md](./eval-code.md). Dataset rules: every case has an `id`, an `input`, and expectations that a program can check (`must_contain`, `must_not_contain`, `must_match`). Seed it with real inputs (redacted), every production failure (each bug becomes a case), at least one injection attempt and, for RAG, an unanswerable question. Never put secrets or personal data in a dataset file.

## 6. Wire it up

1. Add tasks to the runner: `eval-gate` (`tsx evals/gate.ts <task>-gate`) and `eval-full` (`tsx evals/gate.ts <task>-full --judge`).
2. CI: run `eval-gate` on every PR that touches `prompts/`, `config/llm.models.json`, `src/platform/llm/` or the feature; run `eval-full` nightly and on release branches. The job needs the API key as a secret, so for fork PRs (no secrets available) it is skipped and non-blocking; the deterministic checks still run there through the unit tests (`pnpm vitest run tests/evals.test.ts`, fake adapter, no network). Job structure and SHA-pinned actions: [workflow-templates.md](../../infra/set-up-delivery-pipeline/workflow-templates.md).
3. Set `EVAL_RECORD=1` on the nightly job so each run appends to `evals/history.jsonl`; the gate compares the next run with the last recorded pass rate.
4. Add a budget per dataset in `thresholds.json`. The runner stops with an error when spend reaches it.

## 7. Verify

```bash
pnpm vitest run tests/evals.test.ts                  # runner, checks, budget stop and gate logic: no network
ANTHROPIC_API_KEY=… pnpm tsx evals/gate.ts tickets-gate; echo "exit=$?"   # one paid run
```

Expected: the unit tests pass. The gate run prints `{ total, passed, passRate, costUsd, baseline, problems }` and exits 0 when `passRate` is at or above `minPassRate` and not more than `maxDropVsBaseline` below the baseline, otherwise 1. Break a prompt on purpose (delete a rule), rerun, and see the exit code turn 1: a gate that cannot fail is decoration.

**Calibrate the judge** before relying on `--judge`: label 30 to 50 real outputs pass or fail by hand, run the judge on the same outputs, compute Cohen's kappa (`cohensKappa` in `lib/metrics.ts`). Below 0.6 the judge is not ready: tighten the rubric until it is. Repeat when the judge model or the rubric changes.

## References
- [eval-patterns.md](./eval-patterns.md): rules and why. [eval-code.md](./eval-code.md): all code.
- [llm-seam-ts.md](../_shared/llm-seam-ts.md): the harness calls the seam.
- [llm-security.md](../_shared/llm-security.md): injection cases belong in the set (LLM01).
- [stack-versions.md](../_shared/stack-versions.md): Inspect AI, promptfoo, Vitest lines.
