---
name: fix-issues
description: Use when fixing software issues in a repository, including bug reports, failing tests, CI failures, compile errors, runtime errors, regressions, dependency problems, and requests such as "fix this issue", "resolve this bug", "make tests pass", or "address the failure". Guides Codex through issue triage, reproduction, root-cause analysis, scoped implementation, verification, and final handoff.
---

# Fix Issues

## Overview

Use this skill to turn an issue report or failure into a verified code change. Keep the fix narrow, evidence-driven, and aligned with the repository's existing tooling and style.

## Workflow

1. Capture the issue source:
   - Read the exact user request, linked issue, stack trace, failing command, PR comment, or CI log before editing.
   - If the issue points to GitHub and tools are available, inspect the issue, PR, checks, or review thread before inferring requirements.
   - If the referenced source is unavailable and guessing would risk the wrong fix, ask one concise blocking question.

2. Inspect the repository:
   - Check `git status --short` first and preserve unrelated user changes.
   - Read the closest README, build files, package manifests, test configuration, and affected source files.
   - Prefer fast searches with `rg` and inspect call sites before deciding where to patch.

3. Reproduce or localize the failure:
   - Run the narrowest relevant test, build, linter, script, or command first.
   - Capture the exact failing assertion, exception, compiler error, or behavior.
   - If the failure cannot be reproduced locally, create or update a focused test that encodes the reported behavior when practical.

4. Diagnose the root cause:
   - Trace from the observed failure to the responsible code path, data shape, version, configuration, or contract mismatch.
   - Prefer a fix that addresses the cause rather than hiding symptoms.
   - Note any assumption that is not proven by code, tests, or logs.

5. Implement the smallest durable change:
   - Follow local patterns and helper APIs instead of introducing new abstractions.
   - Avoid broad refactors, formatting churn, dependency upgrades, and public API changes unless the issue requires them.
   - Add or adjust tests when the bug is behavioral, regression-prone, or not already covered.

6. Verify:
   - Re-run the original failing command or closest equivalent.
   - Run broader relevant validation when the change touches shared behavior, build logic, dependencies, or user-facing workflows.
   - If validation cannot run, state the command attempted, the blocker, and the residual risk.

7. Handoff:
   - Summarize the root cause, changed files, and verification results.
   - Mention any remaining risk, skipped test, or follow-up only when it matters.
   - Do not claim the issue is fixed without either verification evidence or a clear caveat.

## Repository Defaults

- Use project-local wrappers first: `./gradlew`, `./mvnw`, `./kotlin`, `npm run`, `pnpm`, `yarn`, `uv`, `cargo`, or other checked-in scripts.
- For Kotlin Toolchain work, also use the `kotlin-toolchain` skill when available.
- For standalone `.main.kts` script issues, also use the `main-kts` skill when available.
- For GitHub Actions failures or PR review comments, prefer dedicated GitHub workflows when available, then return to this workflow for the code change.

## Fix Quality Bar

- The new or changed behavior is covered by a targeted test when a practical test harness exists.
- Existing public behavior is preserved unless the issue explicitly asks to change it.
- Error messages and edge cases are handled deliberately, not as incidental side effects.
- The final diff is easy to review and limited to files required for the fix.
