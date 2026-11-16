---
name: verification-before-completion
description: Verify a software change before reporting it complete. Use at handoff, after fixes, and whenever claiming that a build, test, or feature works.
---

# Verification Before Completion

1. Translate the request into observable acceptance criteria.
2. Inspect the final diff and working-tree status. Confirm only intended files changed and user work is preserved.
3. Run targeted tests first, then the appropriate broader test/build/lint/type-check commands from project conventions.
4. Exercise meaningful boundary and error paths not covered by automated tests.
5. Inspect exit codes and output. Investigate skipped, flaky, timed-out, or partially run checks.
6. Inspect generated artifacts and user-visible behavior when the task creates them.
7. Scan changed files for credentials, personal data, local paths, temporary files, and unrelated content.
8. Compare evidence with acceptance criteria and list anything unverified.

Report checks as **passed**, **failed**, **not run**, or **blocked**. State what each check proves and what it does not. Never fabricate coverage, benchmarks, test counts, security findings, or deployment status. A successful command is not proof of behavior it did not exercise.
