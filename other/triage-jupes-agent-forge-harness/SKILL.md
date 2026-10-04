---
name: triage
description: Deadline management and capacity planning across epics and PRs. Use when the user runs /triage or wants deadline/capacity triage.
---

# /triage — Deadline Management & Capacity Planning

Classifies epics by deadline risk, reviews open PRs across repos, and creates bugs for failing CI.

## Usage
```
/triage
/triage --epic EPIC-7        # Triage a single epic
```

---

## Step 1 — Load All Epics

```bash
bd ready --type epic 2>/dev/null
bd ready --status in_progress --type epic 2>/dev/null
```

For each epic: `bd show <EPIC-ID>` to get due date, task count, completed count.

---

## Step 2 — Classify Each Epic

For each epic, calculate:
- **Total tasks**: child task count
- **Completed tasks**: closed child task count
- **Remaining tasks**: open + in-progress child tasks
- **Days until due**: (due date) - (today)
- **Velocity needed**: remaining tasks / days until due

Classify:

| Status | Criteria |
|--------|----------|
| **OVERDUE** | Due date has passed and epic is not closed |
| **AT RISK** | Due in <7 days with >30% tasks remaining, OR blocked tasks on critical path |
| **ON TRACK** | Due in ≥7 days with ≤30% remaining, OR no due date |
| **COMPLETE** | All tasks closed |

---

## Step 3 — Review Open PRs (all repos)

```bash
gh pr list --state open --json number,title,headRefName,statusCheckRollup,reviews,createdAt --limit 20
```

For each open PR, check:
- **CI status**: PASS / FAIL / PENDING
- **Review status**: approved / changes requested / awaiting
- **Age**: how many days old

Flag PRs that need attention:
- CI failing → create Beads bug (see Step 4)
- No review after 2+ days → flag for reviewer assignment
- Changes requested but no author response after 1+ days → flag

---

## Step 4 — Auto-Create Bugs for Failing PRs

For each PR with failing CI:

```bash
bd create \
  --type bug \
  --title "CI failing on PR #<n>: <pr title>" \
  --repo <repo> \
  --priority 1 \
  --acceptance "CI passes on PR #<n>"

bd comments add <new-bug-id> "design: CI failure detected by /triage. PR: #<n>. Failures: <ci check names>"
```

**Priority policy:** keep **`high`** for merge-blocking CI on important branches; use **`critical`** only when production or security is directly at risk. When re-ranking work, use `.claude/skills/beads-priority-assignment/SKILL.md`.

Only create if a bug for this PR doesn't already exist:
```bash
bd ready | grep -i "PR #<n>"   # Skip if already filed
```

---

## Step 5 — Capacity Summary

List all ready tasks by priority to help with planning:

```bash
bd ready | head -20
```

Count by priority:
- Critical: N tasks
- High: N tasks
- Medium: N tasks
- Low: N tasks

Identify any tasks blocked for more than 3 days — flag them as potential abandonment candidates.

---

## Output Format

```
## Triage Report — <date>

### Epics

🔴 OVERDUE (1)
  EPIC-3  "User permissions system"  due 2026-04-05  (6 days overdue)
           8/12 tasks complete  →  4 tasks remain

🟠 AT RISK (1)
  EPIC-5  "Dashboard redesign"  due 2026-04-18  (7 days)
           3/10 tasks complete  →  7 tasks remain  (needs ~1/day)
           ⚠ T-67 blocked (dependency on T-54)

🟢 ON TRACK (2)
  EPIC-7  "Settings page"  due 2026-04-25  (14 days)
           5/8 tasks complete  →  3 tasks remain
  EPIC-9  "API rate limiting"  no due date
           1/4 tasks complete

---

### PR Health (4 open)

  #17  feat(auth): refresh tokens         CI: PASS   ✓ Approved    (2 days old)
  #18  fix(dash): pagination              CI: FAIL   ← created T-71 bug
  #16  chore: update deps                 CI: PENDING (in progress)
  #15  feat(settings): user prefs         CI: PASS   ✗ Awaiting review (3 days)

  Action: Assign reviewer to #15

---

### Capacity (ready tasks)

  Critical: 1    High: 5    Medium: 8    Low: 3

  Longest-blocked:
  T-49  "Migrate to v2 API"  blocked 5 days  → consider deferring

---

### Actions Created
  T-71 [bug/high]  CI failing on PR #18: fix dashboard pagination
```
