---
name: repo-intelligence-brief
description: >
  Inspect a GitHub or local repository and produce a compact Codex-ready
  architecture/task brief. Use for repo onboarding, weekend project selection,
  fork analysis, setup discovery, extension ideas, or turning a source repo
  into a useful build plan.
---

# Repo Intelligence Brief

Use this to turn a repo into a practical Codex work unit.

## Intake

If the repo is remote, prefer a shallow clone into a bounded `sources/` or
`vendor/` folder. Inspect before installing.

Run:

```bash
scripts/repo_snapshot.sh <repo>
```

Then read:

- README and docs index
- package manifests and lockfiles
- entry points
- tests and CI config
- license

## Output

```md
# Repo Intelligence Brief

## What It Is
## Why It Matters
## Architecture
## Setup Commands
## Extension Points
## Useful Patterns To Steal
## Risks And Trust Notes
## First Three Codex Projects
## Smallest Valuable Build
```

## Rules

- Mark unverifiable trend claims as unverified.
- Do not run install scripts until the source-intake safety pass is complete.
- Keep the brief under 1200 words unless the user asks for deep research.
- Prefer actionable project ideas over generic summaries.

Use `$sandbox-source-intake` first when a repo asks for broad permissions,
downloads binaries, or has suspicious install instructions.

## Validation

- README, license, manifests, entry points, tests/CI, and docs index were checked when present.
- Setup commands are marked inspect-only unless actually run.
- Trend or popularity claims are verified or labeled unverified.
