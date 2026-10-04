---
name: create-pr
description: >-
  Create a GitHub pull request with gh, target the correct base branch, push only
  committed work, and bind related issues via Fixes/Closes keywords. Use when asked
  to create a PR, open a pull request, push and open PR, link/bind/associate an
  issue to a PR, add Fixes #N, or close issues on merge.
---

# Create PR and Bind Issues

Open a reviewable PR from the current branch and attach the right GitHub issues so merge auto-closes them.

## Preconditions

- Only **committed** changes go into the PR. Leave uncommitted/WIP files out (or ask before committing).
- Do **not** update git config, force-push, or skip hooks unless the user explicitly asks.
- Prefer `gh` for all GitHub operations.

## Resolve base branch

**If the user names a base** (e.g. `dev/0.8.x`, `main`) → use that exactly.

**If the user does not name a base** → use the **latest `dev/<version>`** branch on `origin` (semver; treat `.x` as the highest patch for that minor). Do **not** hardcode a version.

```bash
git fetch origin 'refs/heads/dev/*:refs/remotes/origin/dev/*'
python .agents/skills/create-pr/scripts/resolve_dev_base.py
# → e.g. dev/0.8.x
```

Use the printed name as `<base>` everywhere below (`git log`, `git diff`, `gh pr create --base`).

## Workflow

### 1. Inspect branch state (parallel)

After resolving `<base>`:

```bash
git status
git diff
git rev-parse --abbrev-ref HEAD
git status -sb
git fetch origin <base>
git log --oneline origin/<base>..HEAD
git diff --stat origin/<base>...HEAD
gh pr list --head <current-branch> --json number,title,url,state,baseRefName
```

### 2. Decide branch / PR shape

| Situation                                          | Action                                                                                               |
| -------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Open PR already exists for this head               | Update it (`gh pr edit`) or push; do not open a duplicate                                            |
| Head branch was merged earlier; new commits remain | New PR from same or cleaner branch is OK; confirm `origin/<base>..HEAD` is only the intended commits |
| Mixed concerns on one branch                       | Prefer a clean branch from `origin/<base>` + cherry-pick (or ask) before opening                     |

### 3. Push, then create

```bash
git push -u origin HEAD
gh pr create --base <base> --title "<title>" --body "$(cat <<'EOF'
## Summary
- <1-3 bullets: why / user-visible effect>

Fixes #<issue>

## Test plan
- [ ] <concrete checks>

EOF
)"
```

On Windows PowerShell, use a here-string for `--body` instead of bash HEREDOC:

```powershell
gh pr create --base $base --title "..." --body @"
## Summary
- ...

Fixes #1234

## Test plan
- [ ] ...
"@
```

Title/body style: match recent repo commits (`fix(scope): …`, `feat(scope): …`). Include issue number in title only if helpful; **always** put a closing keyword in the body (see below).

Return the PR URL when done.

### 4. Bind relevant issues

Always attach issues the PR actually resolves or substantially addresses.

1. Infer candidates from: user message, branch name (`fix/1641-…`), commit messages (`(#1641)`), and `gh issue list` / `gh issue view` when needed.
2. Put closing keywords in the PR body (preferred) or add them via:

```bash
gh pr edit <number> --body "$(…updated body with Fixes #N…)"
```

3. Verify link: `gh pr view <number> --json body,closingIssuesReferences` (or check the issue sidebar on GitHub).

Keyword details and multi-issue examples: [references/issue-linking.md](references/issue-linking.md).

### 5. After create (optional)

- If the user only asked to bind an existing PR: skip create; edit body / confirm closing references.
- Do not push again unless new commits were added.

## Quick checks before opening

- [ ] Diff vs base matches the intended fix only
- [ ] No secrets / generated noise unless intentional
- [ ] At least one `Fixes` / `Closes` / `Resolves` line when an issue exists
- [ ] Base is user-specified **or** latest `dev/<version>` from `resolve_dev_base.py`
