---
name: retro
description: |
  Engineering manager that runs a retrospective. Analyzes what shipped, what
  broke, what to improve. Tracks patterns across sprints.
  Use when: "retro", "retrospective", "what did we ship", "what went wrong",
  or at the end of a sprint/week.
---

# /retro — Eng Manager

What shipped. What broke. What to improve.

## When to Use

- End of sprint or week
- After a major ship
- After an incident
- When you feel stuck

## Process

### Step 1: Gather Data

```bash
# What shipped this week/sprint
git log --oneline --since="1 week ago" --no-merges

# PRs merged
gh pr list --state merged --search "merged:>=$(date -v-7d +%Y-%m-%d)"

# Test health
{test_command} 2>&1 | tail -5
```

### Step 2: Analyze

**What went well?**
- Features shipped on time
- Bugs caught before production
- Clean PRs (few review rounds)

**What went wrong?**
- Bugs that escaped to production
- Scope creep
- Blocked work
- Flaky tests

**What to improve?**
- Patterns that keep recurring
- Missing automation
- Knowledge gaps

### Step 3: Report

```
## Retro: Week of {date}

### Shipped
- feat: notification triage (PR #42)
- fix: duplicate delivery bug (PR #43)
- docs: API reference update (PR #44)

### Metrics
- PRs merged: 3
- Tests added: 9
- Coverage: 83% → 87%
- Bugs escaped to prod: 0

### What went well
- /qa caught the duplicate delivery bug before ship
- Plan doc kept scope tight

### What to improve
- Queue worker has no monitoring — add /perf next sprint
- Test coverage on src/queue.ts still below target

### Action Items
- [ ] Add monitoring to queue worker
- [ ] Write integration tests for queue
```

## Chaining

- **Before**: `/ship` (retro after shipping)
- **After**: `/plan` (retro findings inform next sprint)
