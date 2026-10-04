---
name: agile-github-task-from-diff
description: Create a GitHub Task (sub-issue) from the current git diff vs main and link it as a sub-issue of a parent Feature in the local GitHub SmoothAiStockAnalysis. Use when Codex needs to summarize branch changes into a horizontally sliced task with acceptance criteria and create it via `gh`.
models:
  claude: sonnet      # medium-complexity; diff analysis + issue authoring across layers
  copilot: auto
  codex: gpt-5.4
---

# Task From Diff

## Overview

Generate a GitHub **Task** issue from the current branch diff versus main. The task is horizontally sliced — scoped to one technical layer (backend, tests, docs, ai-tooling, config) — and added to the local GitHub Project as a sub-issue of a vertically sliced parent **Feature** issue.

## Workflow

1. Ensure the repo has an up-to-date `origin/main` (or override the base ref).
2. Run a dry run to review the generated title, body, and acceptance criteria.
3. Create the task issue, add it to the project, and optionally link it as a sub-issue of the Feature.
4. Rename the current branch to match the `<type>/<issue>-short-description` naming standard using the newly created issue number — see [Rename Branch After Creation](#rename-branch-after-creation).

## Script

Use `scripts/create_github_task_from_diff.py`.

```bash
# Preview (dry run)
python3 .agents/skills/agile-github-task-from-diff/scripts/create_github_task_from_diff.py --dry-run

# Create task, add to project #1, link as sub-issue of Feature #42 (number or issue URL)
python3 .agents/skills/agile-github-task-from-diff/scripts/create_github_task_from_diff.py --feature-issue 42

# Combine flags from the Inputs table as needed, e.g.:
python3 .agents/skills/agile-github-task-from-diff/scripts/create_github_task_from_diff.py \
  --feature-issue 42 --base-ref main --title "Add persistence layer tests" --open
```

## Inputs

| Flag | Default | Description |
|------|---------|-------------|
| `--feature-issue` | _(none)_ | Parent Feature issue — accepts an issue **number** (`42`) or a full GitHub issue **URL** (`https://github.com/.../issues/42`). When set, the task is linked as a sub-issue. |
| `--title` | _(generated)_ | Override the auto-generated task title. |
| `--repo` | _(from remote)_ | GitHub repo as `owner/repo`. Auto-detected when omitted. |
| `--project` | `1` | GitHub project number under the org. |
| `--no-project` | — | Create the issue only; skip adding it to any GitHub SmoothAiStockAnalysis. |
| `--org` | _(repo owner)_ | GitHub org that owns the project. Defaults to the repo owner detected from the git remote. |
| `--label` | `task` | Label applied to the created issue. |
| `--base-ref` | `origin/main` → `main` | Override base ref for the diff. |
| `--dry-run` | — | Print output without creating anything. |
| `--open` | — | Open the created issue in the browser. |

## Behavior

- Computes the diff from merge-base between `HEAD` and the base ref.
- Classifies the diff into **horizontal layers**: `backend`, `tests`, `documentation`, `ai-tooling`, `config`, `general`.
- Builds a title from the detected layers and affected top-level areas.
- Generates an acceptance criteria checklist based on touched paths.
- Creates the issue via `gh issue create`.
- Adds the issue to the GitHub Project via `gh project item-add`.
- Links the issue as a sub-issue of the parent Feature via the GitHub REST API (`gh api POST /repos/.../sub_issues`).

## Rename Branch After Creation

After the task issue is created, rename the **current local branch** so it conforms to the
`<type>/<issue>-short-description` standard enforced by the
[`git-commit-push-pr`](../git-commit-push-pr/SKILL.md) skill and `.agents/rules/git/git-policy.instructions.md`
(the source of truth). This guarantees the downstream PR title and `Closes #<issue>` link can be derived
from the branch name.

The script prints a ready-made suggestion after creating the issue (`Suggested branch rename: git branch -m <type>/<issue>-<slug>`) — it derives `<type>` from the dominant horizontal layer, `<issue>` from the new issue number, and the slug from the task title. Run that command (no commit/push is performed by this skill). Override the `<type>` if the diff is better described by `fix`/`refactor` than the layer mapping suggests.

Notes:

- **Skipped on `--dry-run`** — nothing is created, so there is no issue number to rename against.
- If a conforming `<type>` or slug cannot be determined, **stop and ask the user** — do not guess, matching the format-enforcement rule in `git-policy.instructions.md`.
- If the branch was already pushed, the rename stays local; the subsequent `git-commit-push-pr` run pushes the renamed branch (its `--issue` handling parses the same number back out of the branch name).

## Vertical vs Horizontal Slicing

| Concept | Owner | Description |
|---------|-------|-------------|
| **Feature** (parent) | Product | Vertically sliced — one complete user-facing capability across all layers. |
| **Task** (this skill) | Engineer | Horizontally sliced — one technical layer of work from the diff (e.g. just the backend changes, or just the test changes). |

## Requirements

- `gh` CLI authenticated with a token that has `repo` and `project` scopes.
- `git` available in the repo.
- The `task` label must exist in the target repo (create with `gh label create task --color 0075ca`).

## Troubleshooting

- If `gh issue create` fails, run `gh auth status` to verify authentication.
- If `gh project item-add` fails, ensure your token has the `project` scope (`gh auth refresh -s project`).
- If the sub-issue API call fails, the script prints a fallback message; link manually in the GitHub UI.
- If the diff is empty, ensure your branch contains changes against main or override `--base-ref`.
