---
name: skill-creator-aggregate-benchmark-layout
description: |
  Fix for skill-creator's `aggregate_benchmark.py` silently producing an empty
  benchmark (0% pass rate, 0.00 delta, "0 ± 0" stats) when the eval workspace
  layout doesn't match what the script expects. Use when: (1) you ran
  aggregate_benchmark.py and got pass_rate=0 across configs even though your
  grading.json files clearly show passing assertions, (2) the benchmark.md
  output reads "Pass Rate | 0% ± 0% | 0% ± 0% | +0.00", (3) your eval workspace
  has grading.json directly under config dirs (e.g.
  iteration-1/eval-N/with_skill/grading.json) instead of run-1/grading.json,
  (4) your grading.json's summary block has passed/total/failed but no
  pass_rate float. Covers the run-N/ subdirectory requirement and the implicit
  pass_rate field requirement that aren't surfaced in the SKILL.md or schemas
  reference.
author: Claude Code
version: 1.0.0
date: 2026-05-02
---

# skill-creator: aggregate_benchmark.py layout requirements

## Problem

`scripts/aggregate_benchmark.py` (in the skill-creator skill bundle) silently
produces a benchmark with all-zero metrics if your eval workspace doesn't match
two specific structural requirements that aren't called out in the skill-creator
SKILL.md or `references/schemas.md`:

1. Each config directory needs a `run-N/` subdirectory; the script does not look
   for `grading.json` directly under the config dir.
2. The `summary` block in each `grading.json` must include a `pass_rate` float
   (passed ÷ total). The grader template shows `{passed, failed, total}` but the
   aggregator silently treats a missing `pass_rate` as 0.

When either is missing, the script produces output that *looks* clean — it
writes `benchmark.json` and `benchmark.md` with no errors — but every metric is
0 and the delta is `+0.00`. Easy to spend time chasing why your "improvement"
shows no signal when the truth is the script never read your grading files.

## Context / Trigger Conditions

- `python -m scripts.aggregate_benchmark <workspace>/iteration-N` reports
  `Delta: +0.00` (or similar all-zero summary) despite passing grading
- `benchmark.md` shows: `Pass Rate | 0% ± 0% | 0% ± 0% | +0.00`
- Your workspace looks like this (FAILS):
  ```
  iteration-1/
    eval-0-name/
      with_skill/
        grading.json     ← script ignores this
        outputs/
      old_skill/
        grading.json
  ```
- Your grading.json's summary looks like:
  ```json
  "summary": {"passed": 9, "failed": 0, "total": 9}   ← no pass_rate
  ```

## Solution

Match both requirements exactly:

### 1. Move grading.json into a `run-N/` subdirectory

```
iteration-1/
  eval-0-name/
    with_skill/
      run-1/
        grading.json     ← script reads this
      outputs/
    old_skill/
      run-1/
        grading.json
      outputs/
```

The script globs `config_dir.glob("run-*")` and skips any config dir that has
no `run-*` matches. A config dir with grading.json directly under it is treated
as "no runs found" and silently dropped.

### 2. Add `pass_rate` to the summary block

```json
{
  "eval_id": 0,
  "config": "with_skill",
  "expectations": [...],
  "summary": {
    "passed": 9,
    "failed": 0,
    "total": 9,
    "pass_rate": 1.0    ← required
  }
}
```

Compute it as `round(passed / max(total, 1), 4)`.

### 3. Fix script (one-liner if you have an existing flat layout)

```bash
WORKSPACE=/path/to/iteration-1
for d in "$WORKSPACE"/eval-*/; do
  for cfg in "$d"*/; do
    [ -f "${cfg}grading.json" ] || continue
    mkdir -p "${cfg}run-1"
    python3 -c "
import json, sys
g = json.load(open('${cfg}grading.json'))
s = g.get('summary', {})
s['pass_rate'] = round(s.get('passed', 0) / max(s.get('total', 1), 1), 4)
g['summary'] = s
json.dump(g, open('${cfg}run-1/grading.json', 'w'), indent=2)
"
  done
done
```

## Verification

Re-run aggregate_benchmark.py. Expect non-zero summary like:

```
Old Skill: 86.6% pass rate
With Skill: 100.0% pass rate
Delta: -0.13
```

(Note: the script's "Delta" sign is `config_a - config_b` in alphabetical order,
so a *positive* skill improvement may print as a *negative* delta. The
benchmark.md table is the authoritative source.)

## Notes

- The script also checks for `timing.json` adjacent to grading.json with
  `total_duration_seconds` and `total_tokens` — capture this from agent_run
  notifications when each subagent task completes. There's no other opportunity
  to get those numbers.
- The `expectations` array in grading.json must use field names `text`,
  `passed`, `evidence` (not `name`/`met`/`details`) for the eval viewer to
  render correctly.
- Each `run-N/` directory under a config supports multiple runs of the same
  eval for variance analysis — the standard `--max-iterations 5` workflow uses
  this. For a single run, `run-1/` is fine.

## References

- `aggregate_benchmark.py` source: `<skill-creator-bundle>/scripts/aggregate_benchmark.py`
  (lookups around lines 75-115 for the directory-walk logic)
- skill-creator workflow doc:
  `<skill-creator-bundle>/SKILL.md` — "Step 4: Grade, aggregate, and launch the viewer"
- schemas reference:
  `<skill-creator-bundle>/references/schemas.md`
