---
name: cost-speed-meter
description: Use when the user asks to measure command execution time or optimize a feedback loop. Records explicit measurements and recommends faster alternatives such as unit tests versus integration tests. It is opt-in; it does not run on every command.
---

# Cost & Speed Meter

Track execution time. Suggest faster paths. Prove optimizations worked.

Measure only commands the user asks to compare. Across sessions, the optional metrics file can show trends without adding noise or overhead to normal work.

## When to Use

- User asks to measure tests, builds, or lint commands
- User asks: "is this slow?", "how long did that take?", "what's the slowest operation?"
- User asks: "what's a faster way to do this?", "what's the quick feedback loop?"
- User is optimizing something — measure before, optimize, measure after to prove it worked
- Working across multiple repos — compare execution costs

## What It Tracks

| Operation | Tracked? | Example |
|-----------|----------|---------|
| `pytest`, `jest`, `cargo test`, `go test` | ✓ Tests | `45s` |
| `npm run build`, `cargo build`, `pip install` | ✓ Builds | `8s` |
| `ruff check .`, `eslint .`, `cargo clippy` | ✓ Lint | `2s` |
| `git push`, `git pull` | ✓ VCS | `3s` |
| Custom commands | ✓ Named in `.claude/metrics.json` | `custom:deploy` |

## Output

### Command Reports

On demand:

```
Use `skills/cost-speed-meter/meter.sh show` for current measurements or
`skills/cost-speed-meter/meter.sh report` for a weekly summary.
```

## Fast-Path Recommendations

Auto-detect patterns:

```
Full suite: pytest (45s)
Unit only: pytest -m 'not integration' (15s)

→ Recommendation: For quick feedback, use unit tests (3x faster)
  Use full suite before pushing.
```

Per-language:
- **Python:** `pytest -m 'not slow'`, `pytest tests/unit/`
- **Node:** `npm run test:unit`, `vitest --run` (vs jest)
- **Rust:** `cargo test --lib` (vs full + integration)
- **Go:** `go test ./...` (vs `go test ./... -v` with benchmarks)

## Metrics File (`.claude/metrics.json`, gitignored)

```json
{
  "repo": "code-to-docs",
  "timestamp": "2026-08-20T14:30:00Z",
  "operations": [
    {
      "name": "tests",
      "category": "test",
      "last_run_seconds": 45,
      "last_run_time": "2026-08-20T14:30:00Z",
      "run_count_7d": 12,
      "avg_7d": 43,
      "trend_7d": "+2s",
      "trend_pct": "+4.7%"
    },
    {
      "name": "unit_tests",
      "category": "test",
      "last_run_seconds": 15,
      "run_count_7d": 4,
      "avg_7d": 14
    },
    {
      "name": "build",
      "category": "build",
      "last_run_seconds": 8,
      "run_count_7d": 8,
      "avg_7d": 8.2,
      "trend_7d": "-0.5s"
    }
  ],
  "slowest_op": {
    "name": "tests",
    "seconds": 45,
    "reason": "integration tests (50 of 1000 tests)"
  },
  "recommendations": [
    "For quick feedback, run unit tests (15s vs 45s) — 3x faster",
    "Test suite grew 4.7% last week; check for new integration tests"
  ]
}
```

## How It Saves Tokens

**Feedback loops:** 
- Run fast path (unit tests 15s) instead of full suite (45s)
- 10 iterations per day × 30s saved = 5 min/day = fewer re-runs
- Fewer retries = fewer tokens

**Prevents wasted optimization:**
- Data-driven: you know tests are slow, not build (actual problem)
- Don't optimize wrong thing (wastes time, tokens)

**Team alignment:**
- Everyone sees same metrics
- "Let's optimize integration tests" (shared understanding)
- No "why is my machine slow?" guessing

## Integration with RTK

RTK compresses output noise.  
Meter tracks execution time.

```
You: pytest
RTK: filters output (-85% noise)
Meter: records 45s
Status: [METRICS: tests 45s] [RTK: -85% output]
```

No conflict, complementary.

## Per-Language Detection

Auto-detects test framework and suggests fast paths:

```python
# Python
if "pytest.ini" or "pyproject.toml" with [tool.pytest]:
  fast_path = "pytest -m 'not slow'"
  full_path = "pytest"
```

```javascript
// Node
if "vitest.config.ts" exists:
  fast_path = "vitest --run"  // unit only
  full_path = "vitest --run --include='**/*.integration.ts'"
```

```rust
// Rust
if "Cargo.toml" with [dev-dependencies]:
  fast_path = "cargo test --lib"  // unit only
  full_path = "cargo test"
```

## Behavioral Rules

- **Opt-in only** — never intercept or time unrelated commands
- **No alerts** — just data, no noise
- **Trends** — report 7-day moving average, flag +10% growth
- **Respect RTK** — if RTK is filtering, meter still gets accurate time
- **No command interception** — measurement is explicit and does not change command output
