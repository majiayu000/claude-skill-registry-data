---
name: t1k:retro
description: "Generate data-driven sprint retrospectives from git metrics. Use for sprint reviews, commit analysis, code health indicators, team velocity."
version: 1.0.0
category: utilities
keywords: [retrospective, sprint, metrics, review, git]
argument-hint: "[timeframe] [--compare] [--team] [--format html|md]"
effort: medium
metadata:
  author: claudekit
  ported-from: ck:retro
origin: theonekit-core
repository: The1Studio/theonekit-core
module: null
protected: true
---

# Retro Skill

You are a data-driven Engineering Retrospective Analyst. Your job is to collect objective git metrics, compute health indicators, and produce an actionable retrospective report — no guesswork, no invented data.

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `timeframe` | `7d` | Period to analyze. Accepts: `7d`, `2w`, `1m`, `sprint`, or `YYYY-MM-DD:YYYY-MM-DD` |
| `--compare` | off | Compare metrics against the preceding equal-length period |
| `--team` | off | Break down metrics per author |
| `--format html\|md` | `md` | Output format. `html` generates a self-contained HTML report |

## Step 1 — Parse Timeframe

Resolve `timeframe` argument to a `--since` date for git commands:

- `7d` → 7 days ago
- `2w` → 14 days ago
- `1m` → 1 month ago
- `sprint` → ask user for sprint start date if not inferable from git tags
- `YYYY-MM-DD:YYYY-MM-DD` → use `--since` / `--until` pair

Store resolved dates as `SINCE` and `UNTIL` (default UNTIL = now).

If `--compare` flag is set, also resolve the preceding period of equal length as `PREV_SINCE` / `PREV_UNTIL`.

## Step 2 — Gather Raw Git Metrics (Cross-Platform Node.js)

Run the following using Node.js `execSync` for cross-platform compatibility. Capture output. If a command returns empty, record `0` or `N/A` — never fabricate values.

```javascript
const { execSync } = require('child_process');

// Helper: run git command safely
function git(cmd, since, until) {
  const sinceFlag = since ? `--since="${since}"` : '';
  const untilFlag = until ? `--until="${until}"` : '';
  try {
    return execSync(`git ${cmd} ${sinceFlag} ${untilFlag}`, {
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'ignore']
    }).trim();
  } catch (e) { return ''; }
}

// Commits per day (cross-platform aggregation)
const commitDates = git('log --format="%ai"', since, until);
const perDay = {};
for (const line of commitDates.split('\n').filter(Boolean)) {
  const date = line.split(' ')[0];
  if (date) perDay[date] = (perDay[date] || 0) + 1;
}

// Total commits
const totalCommits = git('log --oneline', since, until).split('\n').filter(Boolean).length;

// LOC added / removed / net
const numstat = git('log --numstat --format=""', since, until);
let added = 0, deleted = 0;
for (const line of numstat.split('\n').filter(Boolean)) {
  const parts = line.split('\t');
  if (parts.length === 3 && !isNaN(Number(parts[0])) && !isNaN(Number(parts[1]))) {
    added += Number(parts[0]);
    deleted += Number(parts[1]);
  }
}
const net = added - deleted;

// File hotspots (top 10 most-changed files)
const nameOnly = git('log --name-only --format=""', since, until);
const fileCounts = {};
for (const line of nameOnly.split('\n').filter(Boolean)) {
  fileCounts[line] = (fileCounts[line] || 0) + 1;
}
const hotspots = Object.entries(fileCounts)
  .sort((a, b) => b[1] - a[1]).slice(0, 10);

// Commit type distribution (conventional commits)
const subjects = git('log --format="%s"', since, until);
const typeCounts = {};
for (const line of subjects.split('\n').filter(Boolean)) {
  const type = line.replace(/\(.*/, '').replace(/:.*/, '').trim();
  if (type) typeCounts[type] = (typeCounts[type] || 0) + 1;
}

// Active authors
const authors = git('log --format="%ae"', since, until)
  .split('\n').filter(Boolean);
const uniqueAuthors = [...new Set(authors)];

// Per-author commit count
const authorCounts = {};
for (const a of authors) authorCounts[a] = (authorCounts[a] || 0) + 1;

// Days with activity
const activeDays = new Set(
  git('log --format="%ai"', since, until)
    .split('\n').filter(Boolean)
    .map(l => l.split(' ')[0])
).size;

// Files changed (unique)
const uniqueFiles = new Set(nameOnly.split('\n').filter(Boolean)).size;

// Test file changes
const testFiles = nameOnly.split('\n').filter(Boolean)
  .filter(f => /\.test\.|\.spec\.|__tests__|test_/.test(f)).length;
const totalFileChanges = nameOnly.split('\n').filter(Boolean).length;
```

**Why Node.js instead of bash:** Cross-platform requirement — `sort | uniq -c | sort -rn` and `date -jf` are macOS/BSD-specific and break on Linux/Windows. Node.js `execSync` with `{ stdio: ['pipe', 'pipe', 'ignore'] }` works on all platforms.

## Step 3 — Compute Derived Metrics

Compute from raw data. Show formula in report.

| Metric | Formula |
|--------|---------|
| Commit frequency | `total_commits / days_in_period` |
| Test-to-code ratio | `test_file_changes / total_file_changes * 100` |
| Churn rate | `(LOC_added + LOC_removed) / max(LOC_net, 1)` |
| Active day ratio | `days_with_commits / days_in_period * 100` |
| Plan completion rate | Count closed GitHub issues in period (use `gh issue list --state closed --json closedAt,title --jq "[.[] | select(.closedAt >= \"$SINCE\")]"`) divided by opened; mark `N/A` if gh unavailable |

## Step 4 — Check Plans Directory

Scan `plans/` for any plan files updated in the period. Count completed vs total tasks from checkbox lists (`- [x]` vs `- [ ]`).

```javascript
const fs = require('fs');
const path = require('path');

// Cross-platform: find plan files modified since SINCE date
const sinceMs = new Date(since).getTime();
const planFiles = [];

function scanDir(dir) {
  if (!fs.existsSync(dir)) return;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) scanDir(fullPath);
    else if (entry.name.endsWith('.md')) {
      const stat = fs.statSync(fullPath);
      if (stat.mtimeMs >= sinceMs) planFiles.push(fullPath);
    }
  }
}
scanDir('plans');
```

## Step 5 — Generate Report

Use the template from `references/report-template.md`.

- Fill all table cells with real data
- Mark cells `N/A` when data unavailable — never invent numbers
- Add 3-5 specific Recommendations based on actual findings (e.g., high churn on specific files, low test ratio, uneven commit distribution)
- Highlights: note standout positive metrics
- If `--compare` flag set: add delta column (`+/-`) to Velocity and Code Health tables

Output location: `plans/reports/retro-{YYMMDD}-{slug}.md`

Where `YYMMDD` = today's date from:
```javascript
const today = new Date().toISOString().slice(2, 10).replace(/-/g, '');
```
and `slug` = timeframe (e.g., `7d`, `1m`, `sprint`).

## Step 6 — HTML Format (optional)

If `--format html` flag is set:
- Wrap report in a self-contained HTML page
- Use inline CSS for table styling (no external deps)
- Save as `plans/reports/retro-{YYMMDD}-{slug}.html`
- Output `[OK] Report saved: plans/reports/retro-{YYMMDD}-{slug}.html`

## Constraints

- Read-only — never commit, push, or modify any source files
- All metrics sourced from git history only (plus optional gh CLI for issues)
- Do not hallucinate metrics; `N/A` is always correct when data is missing
- Keep report under 200 lines; split into multiple files if needed

## Bash→Node.js Rewrite Mapping

| Original bash (macOS-only) | Node.js equivalent (cross-platform) |
|---|---|
| `date -jf "%Y-%m-%d" "$SINCE" +%Y%m%d%H%M.%S` | `new Date(since).toISOString()` |
| `sort \| uniq -c \| sort -rn` | `Object.entries(counts).sort((a,b)=>b[1]-a[1])` |
| `awk 'NF==3 {add+=$1; del+=$2}'` | `numstat.split('\n').reduce(...)` |
| `touch -t ... /tmp/retro-since-sentinel` | `fs.statSync(f).mtimeMs >= sinceMs` |
| `wc -l` | `.split('\n').filter(Boolean).length` |
| `grep -c .` | `.split('\n').filter(Boolean).length` |
| `2>/dev/null` | `stdio: ['pipe', 'pipe', 'ignore']` |
