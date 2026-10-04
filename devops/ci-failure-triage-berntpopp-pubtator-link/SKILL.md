---
name: ci-failure-triage
description: Use when GitHub Actions or local quality gates fail and the root cause is not already isolated.
---

# CI Failure Triage

Follow `AGENTS.md` first.

## Workflow

1. Identify the failing job, command, and first meaningful error; avoid chasing downstream failures first.
2. Reproduce locally with the closest Makefile target, usually `make ci-local` or the focused target named in the job.
3. Classify the failure as formatting, lint, typecheck, test, Docker, dependency, or infrastructure.
4. Fix the root cause in the narrowest file set and avoid weakening checks unless the check itself is demonstrably wrong.
5. Re-run the focused failing command, then the broader gate that failed.
6. Before handoff, report the exact command results and whether `make ci-local` passes.
