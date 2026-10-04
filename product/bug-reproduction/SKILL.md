---
name: bug-reproduction
description: Turn bug reports into reproducible steps and diagnostic plans. Use when Codex is asked to reproduce a bug, reduce a flaky issue, define observed versus expected behavior, isolate environment variables, or write a minimal reproduction.
license: MIT
---

# Bug Reproduction

## Core Workflow

1. Capture observed behavior, expected behavior, environment, version, inputs,
   frequency, and impact.
2. Reduce the report to the smallest repeatable steps or test case.
3. Identify missing data, logs, screenshots, config, feature flags, and recent
   changes.
4. Propose diagnostic checks that narrow scope without changing production
   state.
5. Convert the reproduction into a regression test target when possible.
6. State confidence and remaining unknowns.

## Safety Rules

- Do not run destructive steps or change production data to reproduce a bug.
- Do not expose private customer data in reproduction artifacts.
- Do not assume root cause until evidence supports it.

## Deliverable Shape

For bug reproductions, provide:

- Observed and expected behavior
- Environment and version
- Reproduction steps
- Minimal test case or fixture
- Diagnostic checks
- Suspected scope
- Regression test target
- Missing evidence

## References

- Read `references/bug-reproduction-checklist.md` when turning a bug report
  into reproducible steps.
