---
name: github-pr-workflow
description: "GitHub PR lifecycle: branch, commit, open, CI, merge."
allowed-tools:
  - bash
  - read_file
enabled: true
related-skills: [github-auth, github-code-review]
license: MIT
author: Adapted from hermes-agent (Nous Research, MIT)
---

# GitHub Pull Request Workflow

Complete guide for managing the PR lifecycle. `gh` first, `git` + `curl`
fallback.

## Prerequisites

- Authenticated with GitHub (see `github-auth` skill)
- Inside a git repository with a GitHub remote

## 1. Branch & Commit

```bash
# Create feature branch
git checkout -b feature/add-login

# Make changes, commit
git add -A
git commit -m "feat: add login endpoint"

# Push
git push -u origin feature/add-login
```

## 2. Create PR

```bash
# With gh (interactive)
gh pr create

# With gh (inline)
gh pr create \
  --title "feat: add login endpoint" \
  --body "## Changes
- Add /api/login route
- Add JWT token generation
- Add tests

## Testing
\`\`\`bash
pytest tests/test_auth.py -v
\`\`\`" \
  --base main \
  --head feature/add-login

# With curl
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls \
  -d '{
    "title":"feat: add login endpoint",
    "body":"Add /api/login route with JWT",
    "head":"feature/add-login",
    "base":"main"
  }'
```

## 3. Check CI Status

```bash
# With gh
gh pr checks 42

# With curl (check runs)
curl -s "https://api.github.com/repos/$OWNER/$REPO/commits/$HEAD_SHA/check-runs" | python3 -c "
import sys, json
for r in json.load(sys.stdin)['check_runs']:
    print(f'{r[\"name\"]:30s} {r[\"conclusion\"] or r[\"status\"]}')
"

# With curl (statuses — legacy CI)
curl -s "https://api.github.com/repos/$OWNER/$REPO/commits/$HEAD_SHA/status" | python3 -c "
import sys, json
r = json.load(sys.stdin)
print(f'Overall: {r[\"state\"]}')
for s in r['statuses']:
    print(f'  {s[\"context\"]:30s} {s[\"state\"]}')
"
```

## 4. Update PR (push more commits)

```bash
# Make more changes
git add -A
git commit --fixup HEAD  # or regular commit
git push
# PR automatically updates
```

## 5. Review & Approve

```bash
# Request review
gh pr edit 42 --add-reviewer username

# Approve (as reviewer)
gh pr review 42 --approve --body "LGTM!"

# Request changes
gh pr review 42 --request-changes --body "See inline comments."

# Comment
gh pr review 42 --comment --body "Some suggestions."
```

## 6. Merge

```bash
# With gh
gh pr merge 42 --merge        # merge commit
gh pr merge 42 --squash       # squash merge
gh pr merge 42 --rebase       # rebase merge
gh pr merge 42 --squash --delete-branch  # squash + delete branch

# With curl
curl -s -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/42/merge \
  -d '{"merge_method":"squash"}'
```

## 7. Cleanup

```bash
# Delete local branch
git checkout main
git pull origin main
git branch -d feature/add-login

# Delete remote branch (if not auto-deleted)
git push origin --delete feature/add-login
```

## Full Workflow Example

```bash
# 1. Branch
git checkout -b fix/issue-42-login-timeout

# 2. Implement + test
# ... make changes ...
pytest tests/test_auth.py -v

# 3. Commit
git add -A
git commit -m "fix: increase login timeout to 30s (fixes #42)"

# 4. Push
git push -u origin fix/issue-42-login-timeout

# 5. Create PR
gh pr create --title "fix: increase login timeout (fixes #42)" --body "..." --base main

# 6. Check CI
gh pr checks

# 7. After CI passes + review approved
gh pr merge --squash --delete-branch

# 8. Cleanup
git checkout main && git pull
```

## Pitfalls

- **`fixes #42`**: auto-closes issue 42 on merge. Use `refs #42` to reference
  without closing.
- **Squash merge**: all commits become one. Branch history is lost. Best for
  small PRs.
- **Merge conflicts**: `git fetch origin && git rebase origin/main` to resolve
  before pushing.
- **Draft PR**: `gh pr create --draft` marks as WIP. Reviewers can't approve
  until marked ready.
- **Force push**: `git push --force-with-lease` (not `--force`) to avoid
  overwriting others' work on shared branches.
- **CI not triggering**: check if branch protection rules require specific
  status checks. Some CI only runs on certain branch patterns.
