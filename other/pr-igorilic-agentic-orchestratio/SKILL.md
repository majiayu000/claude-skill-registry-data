---
name: pr
description: >
  Create a pull request (GitHub) or merge request (GitLab) with conventional
  description, test summary, and checklist. Auto-detects platform.
  Triggers on: create pr, create mr, pull request, merge request, push and pr.
---

## PR/MR Creation

### Step 1: Detect Platform
- `.gitlab-ci.yml` or gitlab remote → `glab mr create`
- Otherwise → `gh pr create`

### Step 2: Gather Info
- Branch name, extract ticket ID if present (e.g., `feature/PROJ-123-desc`)
- Base branch from `origin/HEAD`
- Commits since branching
- Changed files summary
- Test status from `make test`

### Step 3: Generate Body
Include: Summary (from commits), Ticket link, Changes, Testing status, Checklist
(tests added, docs updated, no breaking changes, conventional commits, self-reviewed).

### Step 4: Push + Create
```bash
git push -u origin "$BRANCH"
# GitHub: gh pr create --base "$BASE" --title "..." --body "..."
# GitLab: glab mr create --source-branch "$BRANCH" --target-branch "$BASE" ...
```

### Step 5: Output
Display URL and remind to request reviewers / link ticket.
