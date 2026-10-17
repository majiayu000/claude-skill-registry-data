---
name: benchmark
description: "Run each collector script against its fixture, measure time and output size, detect regressions. Trigger: /benchmark"
trigger: /benchmark
---
# /benchmark

Performance and correctness regression detection for collector scripts.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What this is for

- Scripts that error on their own fixture
- Output size anomalies (empty or bloated JSON)
- Execution time regressions
- **Read-only skill.** No code changes.

## What You Must Do When Invoked

### Step 1

`-ProjectDir` target

### Step 2

Run collector: execute each script against its fixture, capture time + output + exit code

### Step 3

Report failures, anomalies, slow scripts

### Step 4

Write `benchmark-report.md`

## Usage

```
/benchmark                # interactive
/benchmark <dir>          # scan project
/benchmark -help
```

During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).