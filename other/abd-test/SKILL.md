---
name: abd-test
description: "ABD Testing agent: auto-detects the test framework, writes tests matching project style, runs the suite, and records a test artifact."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# ABD — Testing

Adopt the **Testing** role in the Agent-Based Development workflow.

Read the shared references before acting: [envelope and artifact rules](../../shared/envelope.md), [Git rules](../../shared/git-rules.md), [MVP gate](../../shared/mvp-gate.md).

**If `handoffs/` does not exist**, stop and tell the user to run the Planning skill (`abd-plan`) first — see [project-start.md](../../shared/project-start.md).

**Instructions:**

1. Use Read to read the latest plan artifact from `handoffs/plans/` and dev artifacts from `handoffs/dev/`.
2. Auto-detect the test framework: look for Jest or Vitest by checking `package.json`; pytest by checking `pyproject.toml` or `setup.py`; Go test by checking `go.mod`; PHPUnit by checking `composer.json`.
3. Use Glob with patterns `**/*.test.*`, `**/*_test.*`, and `tests/**/*` to read existing tests and match their style and patterns.
4. Write tests covering: happy path, edge cases, invalid input, error conditions, and all acceptance criteria listed in the plan artifact.
5. Use Bash to run the test suite and fix any failures before writing the artifact.
6. Use Write to create a test artifact at `handoffs/dev/{taskId}_testing_{unixTimestamp}.json` containing status and a test summary (framework detected, number of tests added, pass/fail counts, and any failures resolved).

Follow the output format in [envelope.md](../../shared/envelope.md) when reporting.
