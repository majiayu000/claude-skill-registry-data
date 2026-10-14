---
name: "yeet"
description: "Use only when the user explicitly asks to stage, commit, push, and open a GitHub pull request in one flow using the GitHub CLI (`gh`)."
agent:
  display_name: "Yeet"
  short_description: "Stage, commit, and open PR"
  default_prompt: "Prepare this branch for review: stage intended changes, write a focused commit, and open a PR."
---

## Prerequisites

- Require GitHub CLI `gh`. Check `gh --version`. If missing, ask the user to install `gh` and stop.
- Require authenticated `gh` session. Run `gh auth status`. If not authenticated, ask the user to run `gh auth login` (and re-run `gh auth status`) before continuing.

## Naming conventions

- Branch: `codex/{description}` when starting from main/master/default.
- Commit: `{description}` (terse).
- PR title: `[codex] {description}` summarizing the full diff.

## Workflow

- If on main/master/default, create a branch: `git checkout -b "codex/{description}"`
- Otherwise stay on the current branch.
- Confirm status, then stage everything: `git status -sb` then `git add -A`.
- Commit tersely with the description: `git commit -m "{description}"`
- Run checks if not already. If checks fail due to missing deps/tools, install dependencies and rerun once.
- Push with tracking: `git push -u origin $(git branch --show-current)`
- If git push fails due to workflow auth errors, pull from master and retry the push.
- Open a PR and edit title/body to reflect the description and the deltas: `GH_PROMPT_DISABLED=1 GIT_TERMINAL_PROMPT=0 gh pr create --draft --fill --head $(git branch --show-current)`
- Write the PR description to a temp file with real newlines (e.g. pr-body.md ... EOF) and run pr-body.md to avoid \\n-escaped markdown.
- PR description (markdown) must be detailed prose covering the issue, the cause and effect on users, the root cause, the fix, and any tests or checks used to validate.

## Bundled automation script

A bundled script at `scripts/yeet.ps1` (PowerShell) automates the full workflow:

```powershell
.\scripts\yeet.ps1 -Description "add dark mode toggle"
.\scripts\yeet.ps1 -Description "fix auth race" -Draft
```

Handles: branch creation (if on main), staging, commit, push, and PR open via `gh`. Uses `-DryRun` to preview without side effects.

To use as a project-local tool:

```powershell
cp <skill-path>/yeet/scripts/yeet.ps1 .ai_scripts/
.ai_scripts\yeet.ps1 -Description "my feature" -Draft -DryRun
```

## Cross-references

- **project-backup-status** — Run backup before yeeting to safeguard against push/PR failures.

- **anti-premature-termination** — Verify all completion criteria are met before opening the PR.

- **follow-existing-patterns** — Follow the repo's existing commit message and PR description conventions.
- **skill-loader** — Apply the capped selection policy when deciding which release-adjacent guardrails should also be active before pushing or opening PRs.
- **git-workflow-conventional-commits** — Ensure commits follow conventional format and are atomic before yeeting.
