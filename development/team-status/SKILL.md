---
name: team-status
description: Displays CodeCrew status including project profile, agent team configuration, codebase index health, skill catalog stats, and recent task history.
---

# Team Status - Crew Dashboard

Shows the current state of CodeCrew for the active project.

## When to Activate

- User runs `/crew status`

## Status Report Sections

### 1. Project Overview

Read `.claude/crew-profile.md` and display:
```
Project: {name}
Type: {type} | Languages: {languages} | Frameworks: {frameworks}
Size: {files} files, {lines} lines
```

### 2. Codebase Index Health

Read `.claude/crew-index.json` and check:
```
Index: {file count} files, {symbol count} symbols | {FRESH|STALE|MISSING} | Last: {time ago}
```

**Health assessment:**
- FRESH: indexed within last session, all hashes valid
- STALE: indexed > 1 day ago or hash mismatches detected
- MISSING: index files don't exist → recommend `/crew init`

Quick staleness check: pick 3 random files from the index, compute their current hash, compare with stored hash. If any mismatch → STALE.

### 3. Agent Team

Read `.claude/crew-team.json` and `.claude/crew-config.json` (if exists) and display:

If the config has `"defaultMode": "lite"` or the last task in history used `"mode": "lite"`, show `Mode: LITE` otherwise `Mode: FULL`.

```
Mode: {FULL|LITE}
  Opus:   ceo
  Sonnet: vp-engineering, vp-quality, senior-dev, code-reviewer, debugger [standby: security-analyst, test-engineer]
  Haiku:  junior-dev, doc-writer [standby: devops-engineer]
```

### 4. Skill Catalog

Read `.claude/crew-skills.json` and display:
```
Skills: {relevant}/{total} for {detected stack} | Active: {list} | On-demand: {count} by task type
```

### 5. Agent Performance

Read `.claude/crew-history.json` (if exists, and has 3+ tasks) and aggregate per-agent stats:

```
Agent Performance (last 20 tasks):
  Agent            | Tasks | Success | Avg Confidence
  senior-dev       |    15 |    93%  | high
  debugger         |     8 |   100%  | high
  junior-dev       |    12 |   100%  | high
  code-reviewer    |     6 |   100%  | —
  vp-engineering   |     4 |   100%  | —
  doc-writer       |     3 |   100%  | high
```

Calculation:
- For each agent that appears in history `agents[]` arrays
- Count total tasks, count where `status: "success"`, average `confidence` values
- Sort by task count descending
- If fewer than 3 tasks in history: skip this section

### 6. Task History

Read `.claude/crew-history.json` (if exists) and display last 3 tasks:
```
Recent Tasks:
  1. [2026-04-04 12:00] bug-fix (moderate) → debugger + senior-dev → SUCCESS
  2. [2026-04-04 11:30] docs (trivial) → doc-writer → SUCCESS
  3. [2026-04-04 10:15] feature (complex) → vp-eng + senior-dev + test-eng → SUCCESS
```

If no history: "No tasks yet. Run /crew task to start."

## Missing Files Handling

If required files are missing:
- Missing everything → "Not initialized. Run /crew init"
- Missing index only → "Index missing. Run /crew reindex"
- Missing team config → "Team not configured. Run /crew init"
- Missing history → Normal (show "No tasks yet")
