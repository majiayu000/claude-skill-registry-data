---
name: researchforge-doctor
description: Check that ResearchForge's dependencies (git, Python, optionally Docker) are available and explain any failures. Use when setup fails, before starting a project, or when the user asks whether their machine is ready.
---

# Diagnose the ResearchForge environment

```bash
researchforge doctor --json
```

Each entry has `name`, `ok`, `required`, `detail`, and an optional `hint`.

- All required checks pass → say the environment is ready and continue.
- A required check fails → explain the failure in plain language, show the
  `hint`, and stop: later commands will refuse to run. Do not try to work
  around a failed required check.
- An optional check fails (e.g. Docker) → note the limitation: experiments
  fall back to `.venv` mode, which is dependency isolation, not a security
  sandbox — only trusted repositories should be run there.

If skills seem out of date or missing, `researchforge claude status --json`
reports the installed/modified/missing state of each skill and
`researchforge claude install` refreshes unmodified ones.

## Rules

- The Python engine is the boundary: never work around a validation error, a
  protected path, or an approval gate — fix the artifact or ask the user.
- Approvals belong to the user: never pass `--yes` or type a confirmation
  unless the user explicitly approved that step in this conversation.
- Ground every summary in stored data: quote only numbers returned by
  `--json` output or files under `.researchforge/` — never invent metrics.
