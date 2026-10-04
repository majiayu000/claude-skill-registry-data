---
name: ci-triage_anthropic
description: Use when tests/CI/build/lint fails. Reproduce locally, minimize diffs, fix the root cause, and leave a crisp trail (commands + failing excerpt).
---
## Workflow

1) Reproduce the failure
Run the smallest command that reproduces it locally. If it only fails in CI, replicate the CI environment as closely as possible (OS, node/python version, env flags).

2) Pin the failure
Capture:
- the exact failing command,
- exit code,
- the shortest failing excerpt that proves the failure (avoid dumping megabytes).
- the CI job name and runner image/version when available.

3) Identify the smallest fix
Do not “fix” by broad reformatting or updating unrelated dependencies unless necessary.

4) Validate
Re-run the failing command, then the next nearest test target (unit suite or lint) to ensure no regressions.
If the failure is CI‑only, run the closest local equivalent and note the gap.

## Reporting

End with:
- What failed and why (one paragraph).
- What changed (files + intent).
- What ran (commands + pass/fail).
- If you changed versions, include the before/after.
- If CI‑only, include the most likely cause and the exact signal you used.
