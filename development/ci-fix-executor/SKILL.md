---
name: ci-fix-executor
description: "Diagnose and fix CI failures on PRs — automated test failure analysis and code fixes."
version: 0.1.0
---

# CI Fix Executor

Diagnose and fix CI failures so PRs can pass without manual debugging.

## JTBD (Jobs To Be Done)

### Primary Job
When CI has failed on a PR and I need the failure diagnosed and fixed,
I want automated diagnosis, targeted fix generation, and local validation,
so the PR can pass CI without me manually parsing log output.

### Secondary Jobs
- When a CI failure is blocking a merge and I need a quick targeted fix rather than a full investigation.
- When CI logs are long and noisy and I need the root cause extracted and acted on.
- When `qa-critic` identified a flaky test pattern and I need to fix the underlying cause.

### This Skill Is For
- CI failures on PRs (GitHub Actions, CircleCI, or generic CI systems)
- 5 failure categories: lint errors, test failures, build failures, deploy failures, dependency conflicts
- Generating minimal targeted fixes (not refactors)
- Local validation before re-triggering CI

### This Skill Is NOT For
- Writing new tests from scratch; use `test-planner`
- Investigating flaky tests without a current CI failure; use `qa-critic`
- Performance optimization; use `perf-critic`
- Refactoring code that happens to be near the failure

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|---|---|---|
| Lint failure on PR | Executor parses lint output, identifies violations, applies auto-fix or generates targeted changes | A minimal diff fixing lint violations |
| Test failure on PR | Executor identifies the failing assertion, determines if test or implementation is wrong, generates targeted fix | A fix for the root cause (implementation fix or test correction with justification) |
| Build failure | Executor parses build output, identifies missing imports/config/deps, generates fix | A buildable state with the minimum change needed |
| Deploy failure | Executor identifies env/config/permission issues from deploy logs | Config fix or clear escalation with diagnosis |
| Dependency conflict | Executor resolves version constraints, updates lockfile | Resolved dependency tree |

### When to Escalate
- If the same fix approach fails twice, STOP and escalate to the user with full diagnosis
- If the failure appears to be a fundamental architecture issue, escalate to `test-planner`
- If the test is wrong but the behavior change was intentional, escalate to the user for confirmation

### Paired With
- `test-planner` (optional upstream): provides testing strategy context
- `qa-critic` (downstream): reviews the fix for correctness and test health impact
