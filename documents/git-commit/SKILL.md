---
name: git-commit
description: "Use when asked to commit, save, or persist changes to Git. Handles atomic commits, branch safety, Conventional Commits format, and project style matching. Do NOT use for pushing, creating PRs, or branch management beyond safety checks."
metadata:
  author: Serghei Iakovlev
  version: "1.1"
  category: vcs
---

# Git Commit

## Workflow

### Step 1: Identify changes and group atomically

```bash
git status --short
git diff
git diff --cached
```

Each commit = one logical change. Split unrelated changes into separate commits.

| Situation                          | Commits   |
| ---------------------------------- | --------- |
| New service + its tests            | 1 commit  |
| New feature + unrelated config fix | 2 commits |
| Multiple files for one feature     | 1 commit  |

- If user says "commit all" - group into logical atomic commits
- If ambiguous - ask which files and grouping

### Step 2: Check branch safety (BLOCKING)

```bash
git branch --show-current
```

Protected branches: `main`, `master`, `develop`, `release/*`, `hotfix/*`.

**STOP if on a protected branch.** Do not commit. Do not proceed to Step 3. Instead:

1. Inform the user: "Cannot commit to `<branch>` - it is a protected branch."
2. Create a feature branch: `git checkout -b <type>/<kebab-description>`
3. Only then continue to Step 3.

If on a feature branch: proceed.

#### Branch naming convention

Format: `<type>/<kebab-case-description>`

| Type       | Use Case           | Example                            |
| ---------- | ------------------ | ---------------------------------- |
| `feat`     | New feature        | `feat/bill-reminders`              |
| `fix`      | Bug fix            | `fix/null-amount-validation`       |
| `refactor` | Code restructuring | `refactor/extract-payment-service` |
| `chore`    | Maintenance tasks  | `chore/update-dependencies`        |
| `docs`     | Documentation      | `docs/api-reference`               |
| `test`     | Test additions     | `test/payment-service-coverage`    |

### Step 3: Match project commit style

```bash
git log --format="%s" -20
```

Identify vocabulary, detail level, scope patterns. Mimic the project's phrasing while following Conventional Commits format.

See `references/commit-format.md` for type table, rules, and anti-patterns.

### Step 4: Stage and commit

```bash
git add <files>
git commit -m "<type>[scope]: <description>"
```

For multi-line messages:

```bash
git commit -m "<subject>" -m "<body>"
```

Subject line: imperative mood, under 72 chars, no period, English only. Body (if needed): wrap at 72 chars, explain what and why. The 72-char body wrap is a commit-message convention - `git log` and most CLI tooling render bodies as plain text in a narrow column. It does not generalize to PR descriptions (where GitHub renders soft line breaks as `<br>` and wrapping creates visible artificial breaks), CHANGELOG prose (which follows that file's own readability conventions, not this one), or other Markdown rendered as HTML.

Do not reference `docs/architecture.md`, `docs/decisions/`, section numbers, or ADR numbers in commit messages. Those belong in specs and plans, not in the git history.

### Step 5: Verify

```bash
git log --oneline -1
git show --stat HEAD
```

Report: commit hash, files changed, insertions/deletions.

## Error Recovery

| Error                 | Fix                                                               |
| --------------------- | ----------------------------------------------------------------- |
| "nothing to commit"   | Check `git status`, verify files have changes                     |
| Pre-commit hook fails | Read the error, fix the issue, create a NEW commit (do not amend) |
| Wrong files committed | `git reset --soft HEAD~1`, re-stage correctly, commit again       |

### Rewinding an unpushed protected branch

`git branch -f` refuses to move a branch that is checked out, and `git reset --hard` is banned here because it takes every uncommitted change in the tree with it, including a parallel session's. Detach first, then move the ref:

```bash
git branch "<type>/<description>" main   # name the commits before main stops pointing at them
git switch --detach origin/main
git branch -f main origin/main
git switch main
```

Verify: `git rev-parse main` equals `git rev-parse origin/main`, the new branch is ahead by the rewound commits, and `git status --short` still shows everything it showed before.

## Handoff

If the user also asked to create a PR, invoke the `creating-pr` skill after committing. Do not hand-roll `gh pr create` - the skill has a required template.
