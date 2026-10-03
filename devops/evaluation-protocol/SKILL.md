---
description: >
  Official scoring and audit protocol for Parallel Explore-Exploit branches.
  Preloaded into the ideator, solver, evaluator, auditor, and
  ablation-analyst agents; defines eval.json, the audit checklist, and what
  counts as a specification violation.
user-invocable: false
---

# Evaluation protocol

## Official scores

- The ONLY official score comes from executing
  `python3 <run>/task/evaluate.py <run>/iterations/iN/branches/bK/solution.py`.
- The evaluator transcribes the evaluator's stdout JSON **verbatim** into
  `branches/bK/eval.json`, adding only `branch` and `timestamp` fields. No
  smoothing, no re-runs hunting for a better number (one re-run is allowed
  only on infrastructure error, and must be noted).
- A crash still produces an eval.json: `{"score": null, "error": "..."}`.

## eval.json schema

```json
{"task": "digits", "metric": "accuracy", "score": 0.9852,
 "all_metrics": {"accuracy": 0.9852, "macro_f1": 0.9852, "n_test": 540},
 "constraint_ok": true, "violations": [], "runtime_sec": 0.08,
 "exit_code": 0, "branch": "b1", "timestamp": "2026-07-11T19:00:00"}
```

## Audit checklist (auditor writes branches/bK/audit.md)

Start the file with `VERDICT: PASS` or `VERDICT: FAIL`, then evidence per item:

1. **Test-data integrity** — solution never accesses test labels, never
   reconstructs the split to peek (search solution.py for the split recipe,
   label loading, or dataset re-download).
2. **No hardcoding** — predictions are computed from the input, not embedded
   constants/lookup tables keyed to the test set.
3. **Constraint compliance** — imports within the allowed list, runtime within
   budget, and every other task.md constraint (check eval.json `violations`).
4. **Log consistency** — solve.log shows the work that solution.py claims;
   eval.json score is plausible given the logged runs.
5. **Determinism** — seeds fixed; re-running would plausibly reproduce.

Any confirmed violation ⇒ `VERDICT: FAIL` with the violation list.
A FAIL branch is disqualified from Rank+Select regardless of score.
