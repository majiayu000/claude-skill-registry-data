---
name: status
description: Report git state, ready work, blocked items, and PR health. Use when the user runs /status or wants a workspace snapshot.
---

# /status — Workspace State

Shows git state, ready work, blocked items, and PR health.

## Usage
```
/status              # Standard status view
/status --deep       # Full triage (runs /triage)
```

---

## Output Sections

### 1. Git State

```bash
git status --short
git log --oneline -5
git branch -vv
```

Show:
- Current branch and tracking status (ahead/behind remote)
- Uncommitted changes (staged + unstaged)
- Last 5 commits
- Any stashes: `git stash list`

### 2. Ready Work

```bash
bd ready || echo "⚠ Beads unreachable — start the Dolt server: bd dolt start (then re-run /status)"
```

Display top 5 unblocked, unclaimed tasks sorted by priority.
Format:
```
READY WORK
  T-42  [high]  Add refresh token rotation  (feat)
  T-45  [med]   Update user profile UI      (feat)
  T-48  [low]   Clean up unused imports     (chore)
```

### 3. In-Progress Work

```bash
bd list --status=in_progress
```

Show tasks currently claimed/in-progress.

### 4. Blocked Items

Identify blocked tasks (dependency not yet closed, or `status: blocked`):
```bash
bd blocked
```

For each blocked item, show what it's waiting on.

### 5. PR Health

```bash
gh pr list --state open --json number,title,state,statusCheckRollup,baseRefName --limit 10
```

For each open PR:
- PR number, title, base branch
- CI status (PASS / FAIL / PENDING)
- Review status

Also check recently merged PRs:
```bash
gh pr list --state merged --limit 3 --json number,title,mergedAt
```

---

## Standard Output Format

```
GIT STATE
  Branch: feat/T-42-refresh-tokens → main (2 ahead, 0 behind)
  Clean: yes
  Last commit: abc1234 feat(auth): add token expiry check

READY WORK (3 tasks)
  T-45  [high]   Implement user settings page
  T-48  [med]    Fix pagination bug on dashboard
  T-51  [low]    Update API docs

IN PROGRESS (1 task)
  T-42  [high]   Add refresh token rotation  (you)

BLOCKED (1 task)
  T-49  waiting on T-45 (not started)

OPEN PRS (2)
  #17  feat(auth): refresh tokens  CI: PASS   ← ready to merge
  #15  fix(dash): pagination       CI: FAIL   ← needs attention

MERGED (last 3)
  #14  chore: update deps    (2 days ago)
  #13  feat(api): rate limit  (4 days ago)
  #12  fix(auth): token exp   (1 week ago)
```

---

## `--deep` Flag

When `--deep` is passed: run `/triage` for full deadline and capacity analysis.

---

## Error Handling

- If `bd` errors (Dolt server down): surface it loudly and tell the user to run `bd dolt start`, then re-run `/status`. Do NOT silently skip Beads sections. Only if `bd` is genuinely not installed, note "(bd not installed)".
- If `gh` is not installed: skip PR sections, note "(gh CLI not configured)"
- If not in a git repo: report error and stop
