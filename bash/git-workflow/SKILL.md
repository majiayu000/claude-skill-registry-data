---
name: git-workflow
description: |
  End-user Git and GitHub workflow orchestration for the user's own repositories.
  Use when the user wants feature branches, commits, pull requests, PR review, merge, tags, or GitHub releases
  ("create a PR", "merge PR #42", "ship v1.2.0", "review this pull request").
  Uses workspace git + GitHub CLI (gh). Optional GitHub MCP can supplement but is not required.
  Not for LibrAgent product releases or internal repo maintenance.
  Triggers on: "PR 만들어줘", "브랜치 파서", "PR 머지", "릴리즈 태그", "create pull request", "merge PR".
---

# Git Workflow

Orchestrate **the user's repository** from branch → commit → PR → review → merge → release.

This is an **end-user daily developer** skill. It does not manage the LibrAgent application's own release process.

## Not This Skill

| Skill / tool | Use for |
| --- | --- |
| **release-manager** (dev skill) | LibrAgent maintainers shipping the product |
| **review-pr-comments** (dev skill) | Triage bot comments on LibrAgent PRs |
| **jules** / **Coding Expert** | Code changes inside the repo |
| **tool-installer** | Register GitHub MCP (optional extra) |

## Prerequisites

Inside the user's **workspace git repository**:

```bash
git --version
gh --version
gh auth status
```

If `gh` is missing or unauthenticated, guide the user to install [GitHub CLI](https://cli.github.com/) and run `gh auth login`.

GitHub MCP (if installed) can complement `gh` for rich PR diffs — prefer `git_workflow.py` for deterministic branch/merge/release steps.

## Path conventions

Replace `<skill-base-dir>` with this skill's absolute Base Directory.

## Security & confirmation

- **Confirm** before: force push, merge to default branch, release publish, branch delete
- **Never** commit secrets — scan staged diff for `.env`, keys, tokens
- Use **draft PRs** when the user asks for work-in-progress or confidence is low

## Workflow modes

| Mode | User intent | Flow |
| --- | --- | --- |
| **Feature** | "이 기능 만들어줘" + code already changed | branch → commit → push → PR |
| **Review** | "PR #N 리뷰" | view PR → diff (workspace/gh) → summary → optional comments |
| **Merge** | "PR #N 머지" | checks → confirm → merge |
| **Release** | "vX.Y.Z 릴리즈" | log since tag → notes → tag/release |

See [request-patterns.md](references/request-patterns.md).

## Standard procedure

### 1. Check environment

```bash
python "<skill-base-dir>/scripts/git_workflow.py" --action check_prereqs
python "<skill-base-dir>/scripts/git_workflow.py" --action repo_context
```

Record `default_branch`, `current_branch`, `origin`.

### 2. Branch strategy

Use [branch-strategy.md](references/branch-strategy.md). Default:

- Feature/fix: `feat/<short-slug>` or `fix/<short-slug>` from `default_branch`
- Ask if the user prefers `develop`, `main`, or trunk-based flow

```bash
python "<skill-base-dir>/scripts/git_workflow.py" --action create_branch --name feat/my-feature --base main
```

### 3. Commit & push

```bash
python "<skill-base-dir>/scripts/git_workflow.py" --action status
python "<skill-base-dir>/scripts/git_workflow.py" --action commit --message "feat: ..." --all
python "<skill-base-dir>/scripts/git_workflow.py" --action push
```

Run tests or lint **before** commit when the repo has known commands (package.json, Makefile, etc.).

### 4. Open PR

```bash
python "<skill-base-dir>/scripts/git_workflow.py" --action pr_create \
  --title "feat: short title" \
  --body "## Summary\n...\n## Test plan\n- [ ] ..." \
  --base main
```

Use `--draft` for WIP. Body template: [pr-template.md](references/pr-template.md).

### 5. Review PR

1. `pr_view` + `pr_checks`
2. Read diff: `gh pr diff N` or workspace file reads
3. Summarize risk, test gaps, breaking changes
4. Optional: post review via `gh pr review` (agent composes comment)

Do **not** auto-approve without user confirmation.

### 6. Merge PR

```bash
python "<skill-base-dir>/scripts/git_workflow.py" --action pr_checks --number 42
python "<skill-base-dir>/scripts/git_workflow.py" --action pr_merge --number 42 --method squash --delete-branch
```

Default merge method: **squash** unless the repo convention says otherwise. Confirm CI green (or user override).

### 7. Release

```bash
python "<skill-base-dir>/scripts/git_workflow.py" --action log_since_tag
python "<skill-base-dir>/scripts/git_workflow.py" --action release_create \
  --tag v1.2.0 \
  --title "v1.2.0" \
  --notes-file path/to/notes.md
```

Summarize `log_since_tag` into user-facing release notes. See [release-flow.md](references/release-flow.md).

## Script reference

| Action | Purpose |
| --- | --- |
| `check_prereqs` | git + gh auth |
| `repo_context` | branches, remote |
| `create_branch` | checkout new branch |
| `status` | dirty tree summary |
| `commit` | commit (--all to stage) |
| `push` | push current branch |
| `pr_create` | open PR |
| `pr_view` | PR metadata JSON |
| `pr_checks` | CI status |
| `pr_merge` | merge PR |
| `log_since_tag` | commits for release notes |
| `release_create` | GitHub release |

## Guidelines

- **User repo only** — not LibrAgent upstream unless that is the active workspace
- **gh first** — scripts wrap `gh` for repeatability; agent still explains each step
- **Inventory optional MCP** — GitHub MCP adds context, not required
- **English PR titles** — conventional commits preferred for OSS; match user locale in PR body if they prefer
- **Partial success** — report PR URL even if follow-up merge fails

## References

- [branch-strategy.md](references/branch-strategy.md)
- [pr-template.md](references/pr-template.md)
- [release-flow.md](references/release-flow.md)
- [request-patterns.md](references/request-patterns.md)
- [error-handling.md](references/error-handling.md)
