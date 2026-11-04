---
name: benchmark
description: Measure API latency, bundle size, and database query time, and compare them against saved baselines to catch performance regressions.
disable-model-invocation: true
argument-hint: "/benchmark [api|bundle|db] [--save]"
allowed-tools: "Read, Grep, Glob, Bash, Write, AskUserQuestion"
---

## Overview

Establishes performance baselines and detects regressions by comparing current measurements against stored reference values.

## When to Use

Run before and after a change that can move latency, bundle size, or query time, and save a baseline from a known-good commit first, since a comparison needs one.

| Invocation | Action |
|-----------|--------|
| `/benchmark` | Run all available measurement categories |
| `/benchmark api` | Measure API endpoint latency only |
| `/benchmark bundle` | Measure JS bundle size only |
| `/benchmark db` | Measure database query time only |
| `/benchmark --save` | Run all and save results as the new baseline |
| `/benchmark api --save` | Run API latency and save as baseline |

## Process

1. Parse the invocation into categories and the `--save` flag; with no category, run all three.
2. Confirm the target is local or staging, then record the runtime version, tool version, and date in GMT.
3. Measure each requested category per Measurement Categories below.
4. When `.claude/benchmarks/<project>.json` exists, compare per Comparison and flag regressions against the threshold table.
5. With `--save`, write the new baseline per Saving Baselines.

## Measurement Categories

### API Latency

1. **Detect available tools.** Check for load testing tools in order of preference:
   - `which k6`
   - `which wrk`
   - `which hey`
   - `which ab`
   - If none is installed, name the supported tools and ask whether to install one, per Rules. Never fall back to `curl` timing, which yields no p95 or p99.

2. **Identify endpoints.** Read route files or API documentation to find endpoints. Ask the user which endpoints to benchmark if the project has more than 10.

3. **Run measurements.** For each endpoint, measure:
   - p50 latency in milliseconds.
   - p95 latency in milliseconds.
   - p99 latency in milliseconds.
   - Requests per second.

4. **Report per endpoint:**

   | Endpoint | p50 | p95 | p99 | RPS |
   |----------|-----|-----|-----|-----|

### Bundle Size

1. **Build the project.** Run the build command from the project's scripts.

2. **Measure output.** For each output file in the build directory:
   - Raw size in bytes.
   - Gzipped size in bytes.

3. **Report:**

   | File | Raw | Gzipped |
   |------|-----|---------|

### Database Query Time

1. **Identify slow queries.** Look for query logging configuration in the ORM or database config.

2. **Run the test suite with query timing.** If the ORM supports query logging, enable it and capture execution times.

3. **Report queries exceeding 100ms:**

   | Query | Duration | Location |
   |-------|----------|----------|

## Baselines

Baselines are stored in `.claude/benchmarks/<project>.json` relative to the project root.

```json
{
  "timestamp": "2026-04-04T12:00:00Z",
  "api": {
    "GET /api/users": {"p50": 12, "p95": 45, "p99": 120, "rps": 850},
    "POST /api/orders": {"p50": 25, "p95": 80, "p99": 200, "rps": 420}
  },
  "bundle": {
    "main.js": {"raw": 245000, "gzipped": 78000},
    "vendor.js": {"raw": 890000, "gzipped": 210000}
  },
  "db": {
    "findUserById": {"p50": 2, "p95": 8}
  }
}
```

## Comparison

When a baseline exists, compare every measurement against it:

1. **Compute deltas.** For each metric, calculate the percentage change from baseline.

2. **Flag regressions.** A regression is any metric that worsened beyond the threshold:

   | Metric | Regression threshold |
   |--------|---------------------|
   | API p50 | > 20% slower |
   | API p95 | > 30% slower |
   | API p99 | > 50% slower |
   | Bundle raw size | > 10% larger |
   | Bundle gzipped size | > 10% larger |
   | DB query time | > 25% slower |

3. **Report with deltas:**

   | Metric | Baseline | Current | Delta | Status |
   |--------|----------|---------|-------|--------|
   | GET /api/users p50 | 12ms | 15ms | +25% | REGRESSION |
   | main.js gzipped | 78KB | 76KB | -2.6% | OK |

4. **Summary.** State total regressions found, total improvements, and unchanged metrics.

## Saving Baselines

When `--save` is passed:

1. Run all requested measurements.
2. Write results to `.claude/benchmarks/<project>.json`.
3. Create the `.claude/benchmarks/` directory if it does not exist.
4. If a baseline already exists, show the diff before overwriting.
5. Confirm the save to the user.

## Rules

- Benchmarks must run against a local or staging environment, never production.
- Report median, not mean. See the Benchmark Methodology section of [`../../standards/testing.md`](../../standards/testing.md).
- When no load testing tool is installed, state which tools are supported and ask whether to install one. Do not silently fall back to inaccurate methods.
- Bundle size measurements require a fresh build. Do not measure stale build artifacts.
- All timestamps in GMT.
- Never modify source code during benchmarking. This is a measurement-only skill.
- Include the runtime version, tool version, and measurement date in every report.

## Common Rationalizations

- "Staging is down, production is close enough": production load skews every percentile and the run adds load to real users. Wait for staging or run locally.
- "The build output from earlier is fine": a stale bundle measures the previous code. Rebuild, then measure.
- "curl timing is good enough without k6": a single-request timer has no p95 or p99. Name the supported tools and ask before installing one.
- "Mean latency reads cleaner": one outlier moves the mean. Report the median per the testing rule.
- "Just overwrite the baseline": saving over a regression hides it for every later run. Show the diff first.

## Red Flags

- Stop and ask for a staging or local URL when the only reachable target is production.
- Stop and rebuild when the build directory predates the last source change.
- Stop and ask which endpoints to measure when the route files list more than 10.
- Stop and revert when a source file changed during the run, since this skill measures only.

## Verification

- A report table exists for every requested category, with runtime version, tool version, and a GMT date.
- Every metric with a baseline carries a delta and an `OK` or `REGRESSION` status.
- The summary states the counts of regressions, improvements, and unchanged metrics.
- With `--save`, `.claude/benchmarks/<project>.json` holds the new timestamp, and the diff against the old baseline was shown.
- `git status` shows no source file changed by the run.

## Related Skills

- `/profile` -- Find the bottleneck behind a regression this skill flags.
- `/test` -- Run the test suite, which may include performance tests.
- `/ship checks` -- Check CI pipeline, which may include performance gates.
