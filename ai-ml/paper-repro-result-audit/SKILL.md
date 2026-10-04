---
name: paper-repro-result-audit
description: Audit reproduced AI/ML paper results against the paper's claim map. Use after smoke or experiment runs when Codex must compare metrics, tables, figures, logs, seeds, confidence intervals, tolerances, and blockers to issue an evidence-grounded reproduction verdict without overstating success.
---

# Paper Repro Result Audit

## Overview

Use this skill to decide what the reproduction evidence actually supports. It audits results; it does not rerun experiments or repair code unless the user explicitly asks to enter a fix-and-rerun loop.

Read `references/patterns.md` before judging noisy metrics, multiple seeds, missing error bars, figure-only results, or partial reproduction.

## Inputs

- `claim_map.md/json` from `$paper-repro-claim-map`.
- `source_lock.md/json` and `env_smoke_report.md` if available.
- Experiment logs, result CSV/JSON/JSONL, tensorboard/wandb exports, generated figures, tables, checkpoints, command manifests, or notebook outputs.
- Optional user-provided tolerance rules.

## Workflow

1. Build the comparison table from the claim map:
   - claim id;
   - experiment id;
   - paper value;
   - reproduced value;
   - metric direction;
   - seed/repeat count;
   - variance/error bar;
   - source log/result file.
2. Normalize metrics before comparison:
   - align units, percentages, splits, dataset configs, macro/micro averaging, rounding, and higher/lower-is-better direction;
   - avoid comparing values from different dataset versions or checkpoints unless marked separately.
3. Apply tolerance:
   - use paper-reported confidence interval/error bars when available;
   - use user-provided tolerance when available;
   - otherwise use a clearly stated heuristic tolerance and mark it as inferred.
4. Distinguish outcome types:
   - exact or within reported uncertainty;
   - close but outside uncertainty;
   - outside tolerance;
   - not testable;
   - static/environment check only;
   - blocked before result.
5. Diagnose likely causes:
   - source mismatch, dependency drift, data split/version, random seed variance, hardware/CUDA nondeterminism, missing checkpoint, evaluator mismatch, command/config mismatch, insufficient repeats, or paper ambiguity.
6. Produce an audit report with claim-level verdicts and an overall verdict.

## Verdict Taxonomy

Use one of these for each claim:

- `reproduced`: result matches exactly or within stated uncertainty.
- `partially_reproduced`: direction or broad magnitude matches, but not all metrics/seeds/settings match.
- `close_outside_tolerance`: result is near but outside stated or inferred tolerance.
- `not_reproduced`: result contradicts the paper claim under comparable conditions.
- `not_testable`: required artifact, data, model, or method detail is missing.
- `static_check_only`: only repo/import/config checks ran.
- `blocked`: no comparable result due to environment/auth/license/resource blocker.

Overall verdict must be the minimum defensible claim. Do not let one successful smoke test upgrade the whole paper to reproduced.

## Output Contract

Create `result_audit.md` and, for structured runs, `result_audit.json`.

Required Markdown sections:

- `Audit Scope`
- `Input Artifacts`
- `Metric Normalization`
- `Claim-Level Comparison`
- `Variance and Tolerance`
- `Failures and Blockers`
- `Overall Verdict`
- `Recommended Next Actions`

Use this JSON shape:

```json
{
  "audit_scope": "",
  "overall_verdict": "partially_reproduced",
  "comparisons": [
    {
      "claim_id": "C1",
      "experiment_id": "E1",
      "paper_value": "",
      "reproduced_value": "",
      "metric": "",
      "direction": "higher_is_better",
      "tolerance": "",
      "seed_count": "",
      "verdict": "not_testable",
      "evidence_files": [],
      "diagnosis": ""
    }
  ],
  "blockers": []
}
```

## Guardrails

- Do not average incompatible runs.
- Do not hide failed seeds or failed rows in aggregate metrics.
- Do not compare against a paper table if the dataset split, checkpoint, or evaluator differs without marking it.
- Do not claim statistical significance unless the run count and method support it.
- Keep raw result files and logs referenced by path.

## Resources

- `references/patterns.md`: result-audit practices distilled from artifact evaluation, seed/statistical guidance, PaperBench/paper-replay-style verdicts, and reproduction report conventions.
