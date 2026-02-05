---
name: quality-gate-runner
description: |
  Orchestrate pytest/mypy/ruff/fab gates with consistent reporting format.
  Runs quality checks and produces standardized verification results.
  
  Use when working on development tasks.
metadata:
  version: "1.0.0"
  category: "development"
  priority: "critical"
---

# Quality Gate Runner

Orchestrate pytest/mypy/ruff/fab gates with consistent reporting format.

## Inputs

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `workcell_path` | string | Yes | - | Path to workcell to validate |
| `gates` | object | Yes | - | Gate configuration (code.test, code.lint, code.typecheck, fab.validate) |
| `fail_fast` | boolean | No | false | Stop on first failure |

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| `all_passed` | boolean | True if all gates passed |
| `results` | object | Per-gate results with exit codes and durations |
| `blocking_failures` | array | List of blocking failures requiring fixes |

## Usage

```bash
python scripts/quality-gate-runner.py [arguments]
```

---

*Generated from [`skills/development/quality-gate-runner.yaml`](../../skills/development/quality-gate-runner.yaml)*
