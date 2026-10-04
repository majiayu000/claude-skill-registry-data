---
name: superpowers-retro
description: >
  Use when asked to "weekly retro", "what did we ship", "engineering retrospective",
  "sprint summary", "ship report", or proactively at the end of a work week or sprint.
  Analyzes commit history, work patterns, and code quality metrics with persistent history
  and trend tracking.
---

> **DEPRECATED** — use `/retro` instead. This skill is a legacy alias and will be removed in a future cleanup.
# Engineering Retrospective

**Purpose:** Weekly engineering retrospective. Analyzes commit history, work patterns, and code quality metrics with persistent history and trend tracking.

---

## Arguments

| Argument | Window |
|---------|--------|
| `/retro` | Last 7 days (default) |
| `/retro 24h` | Last 24 hours |
| `/retro 14d` | Last 14 days |
| `/retro 30d` | Last 30 days |
| `/retro compare` | Current window vs prior same-length window |
| `/retro compare 14d` | Compare with explicit window |

---

## Step 1: Gather Raw Data

```bash
git fetch origin main --quiet 2>/dev/null || true
git config user.name
git config user.email
```

Run ALL in parallel:

```bash
# 1. All commits with timestamps, hash, author, files changed, insertions, deletions
git log origin/main --since="7 days ago" --format="%H|%aN|%ae|%ai|%s" --shortstat

# 2. Per-commit test vs total LOC breakdown
git log origin/main --since="7 days ago" --format="COMMIT:%H|%aN" --numstat

# 3. Commit timestamps for session detection
git log origin/main --since="7 days ago" --format="%at|%aN|%ai|%s" | sort -n

# 4. Files most frequently changed
git log origin/main --since="7 days ago" --format="" --name-only | grep -v '^$' | sort | uniq -c | sort -rn | head -20

# 5. PR numbers from commits
git log origin/main --since="7 days ago" --format="%s" | grep -oE '#[0-9]+' | sed 's/^#//' | sort -n | uniq | sed 's/^/#/'

# 6. Per-author hotspots
git log origin/main --since="7 days ago" --format="AUTHOR:%aN" --name-only

# 7. Per-author commit counts
git shortlog origin/main --since="7 days ago" -sn --no-merges

# 8. Test file count
find . -name '*.test.*' -o -name '*.spec.*' -o -name '*_test.*' -o -name '*_spec.*' 2>/dev/null | grep -v node_modules | wc -l

# 9. TODOs backlog
cat TODOS.md 2>/dev/null || echo "No TODOS.md found"
```

---

## Step 2: Compute Metrics

| Metric | Value |
|--------|-------|
| Commits to main | N |
| Contributors | N |
| PRs merged | N |
| Total insertions | N |
| Total deletions | N |
| Net LOC | +N / -N |
| Test LOC ratio | N% |
| Active days | N |
| Detected sessions | N |
| Avg LOC/session-hour | N |

Per-author leaderboard:

```
Contributor    Commits   +/-        Top area
You             N        +X/-Y     [dir-or-file]
[Name]          N        +X/-Y     [dir-or-file]
```

---

## Step 3: Commit Time Distribution

Show hourly histogram (local timezone):

```
HOURS:  00  01  02  03  04  05  06  07  08  09  10  11  12  13  14  15  16  17  18  19  20  21  22  23
COUNT:  N   N   N   N   N   N   N   N   N   N   N   N   N   N   N   N   N   N   N   N   N   N   N   N
        |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
```

Identify: peak hours, dead zones, bimodal vs continuous pattern, late-night coding.

---

## Step 4: Work Session Detection

Detect sessions using **45-minute gap** threshold:

| Session type | Threshold |
|-------------|-----------|
| Deep | 50+ minutes |
| Medium | 20-50 minutes |
| Micro | <20 minutes |

Calculate: total active coding time, average session length, LOC per hour.

---

## Step 5: Commit Type Breakdown

Categorize by conventional commit prefix:

| Type | Count | % |
|------|-------|---|
| feat | N | N% |
| fix | N | N% |
| refactor | N | N% |
| test | N | N% |
| chore | N | N% |
| docs | N | N% |

Flag if fix ratio exceeds 50%.

---

## Step 6: Hotspot Analysis

Top 10 most-changed files. Flag:
- Files changed 5+ times
- Test vs production file ratio
- VERSION/CHANGELOG frequency

---

## Step 7: PR Size Distribution

| Size | Lines changed | Count |
|------|--------------|-------|
| Small | <100 LOC | N |
| Medium | 100-500 LOC | N |
| Large | 500-1500 LOC | N |
| XL | 1500+ LOC | N |

---

## Step 8: Focus Score + Ship of the Week

- **Focus score:** % of commits touching the single most-changed top-level directory
- **Ship of the week:** Highest-LOC PR in the window

---

## Step 9: Team Member Analysis

For each contributor:

1. Commits and LOC
2. Areas of focus (top 3 directories)
3. Commit type mix
4. Session patterns (peak hours)
5. Test discipline (personal test LOC ratio)
6. Biggest ship

**For "You" (current user):** Deepest treatment — include all detail from above.

**For teammates:**
- What they shipped (2-3 sentences)
- **Praise** (1-2 specific things anchored in commits)
- **Opportunity for growth** (1 specific, constructive)

---

## Step 10: Week-over-Week Trends (if window >= 14d)

| Metric | Week 1 | Week 2 | Trend |
|--------|--------|--------|-------|
| Commits | N | N | ↑/↓/— |
| LOC | N | N | ↑/↓/— |
| Test ratio | N% | N% | ↑/↓/— |
| Fix ratio | N% | N% | ↑/↓/— |

---

## Step 11: Streak Tracking

```bash
# Team streak
git log origin/main --format="%ad" --date=format:"%Y-%m-%d" | sort -u | wc -l

# Personal streak
git log origin/main --author="<name>" --format="%ad" --date=format:"%Y-%m-%d" | sort -u | wc -l
```

---

## Step 12: Load History & Compare

```bash
ls -t .claude/retros/*.json 2>/dev/null
```

If prior retros exist: calculate deltas, include **Trends vs Last Retro** section.

If first retro: append "First retro recorded — run again next week to see trends."

---

## Step 13: Save Retro History

```bash
mkdir -p .claude/retros
today=$(date +%Y-%m-%d)
cat > ".claude/retros/retro-${today}.json" << 'EOF'
{
  "date": "YYYY-MM-DD",
  "window": "7d",
  "metrics": {...},
  "authors": {...},
  "tweetable": "...",
  "streak_days": N
}
EOF
```

---

## Step 14: Write the Narrative

Structure output as:

---

**Tweetable summary:**
```
Week of MMM DD: N commits (N contributors), +Xk/-Yk LOC, Z% tests, N PRs merged | Streak: Nd
```

### Summary Table
(from Step 2)

### Trends vs Last Retro
(from Step 12 — skip if first)

### Time & Session Patterns
(from Steps 3-4)

### Shipping Velocity
(from Steps 5-7)

### Code Quality Signals
- Test LOC ratio
- Hotspot analysis

### Your Week (personal deep-dive)
(from Step 9, current user only)

### Team Breakdown
(from Step 9, teammates)

### Top 3 Wins
Identify the 3 highest-impact things shipped.

### 3 Things to Improve
Specific, actionable, anchored in actual commits.

### 3 Habits for Next Week
Small, practical, realistic. Each takes <5 minutes to adopt.

---

## Compare Mode

1. Compute metrics for current window
2. Compute metrics for prior same-length window
3. Show side-by-side comparison with deltas
4. Brief narrative on biggest improvements and regressions
5. Save only current-window snapshot

---

## Tone

- Encouraging but candid — no coddling
- Specific and concrete — always anchor in commits
- Frame improvements as leveling up, not criticism
- Praise feels like something from a real 1:1
- ~3000-4500 words total

---

## Completion Status

- **DONE** — Full retro complete, narrative written, history saved
- **DONE_WITH_CONCERNS** — Retro done but data is thin
- **BLOCKED** — No git history available
- **NEEDS_CONTEXT** — Need repo access or git auth
