---
name: milestone-tracker
description: Track GitHub milestone progress and issue completion. Use when user asks about milestone status, how many issues done, sprint progress, or completion percentage.
allowed-tools: Bash, Read
---

# Milestone Tracker Skill

## Purpose

Automatically fetch and summarize milestone progress when the user asks about completion status, remaining work, or sprint metrics. This is a read-only skill.

## When Claude Should Use This

- User asks "milestone progress?"
- User asks "how many issues left?"
- User asks "completion percentage"
- User asks "what's left in the sprint?"
- User mentions milestone tracking

## Instructions

### List Milestones

```bash
gh api repos/rollercoaster-dev/monorepo/milestones --jq '.[] | {number, title, open_issues, closed_issues, due_on, state}'
```

### Get Specific Milestone

```bash
gh api repos/rollercoaster-dev/monorepo/milestones/<number>
```

### Get Issues in Milestone

```bash
gh issue list --milestone "<milestone-name>" --state all
```

### Calculate Progress

```
Completion % = (closed_issues / (open_issues + closed_issues)) * 100
```

## Current Milestones

### OpenBadges Badge Generator (#14)

- **Issues:** #108-#128 (21 issues)
- **Tracks:** Key management, baking, verification, E2E tests

**Dependency Tracks:**

- Track A (Keys): #108 → #109 → #110 → #111 → #112 → #113
- Track B (PNG Baking): #114 → #115 → #116
- Track C (SVG Baking): #114 → #117 → #118
- Track D (Unified Baking): #116 + #118 → #119 → #120
- Track E (Verification): #121 → #122 + #123 → #124 → #125 → #126
- Track F (E2E + Docs): All above → #127 → #128

## Output Format

```markdown
## Milestone: <name>

**Progress:** X/Y issues (Z%)
**Due:** <date or "No due date">

### By Status

- Done: <count>
- Blocked: <count>
- In Progress: <count>
- Not Started: <count>

### Recently Completed

- #X: <title>
- #Y: <title>

### Up Next (Unblocked)

- #A: <title>
- #B: <title>

### Blocked

- #C: <title> - Waiting on #X
```

## Progress Bar

Generate visual progress:

```
[████████░░░░░░░░░░░░] 40% (8/20)
```
