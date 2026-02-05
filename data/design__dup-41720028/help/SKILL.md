---
name: help
description: Assess system state and suggest what needs attention. Use when stuck, unsure what to work on, or need guidance. Reviews git, inbox, recent activity, suggests priorities.
allowed-tools: Read, Bash, Grep
---

# Help (System Assessment)

Deep assessment of workspace state. Identifies blockers, suggests priorities.

## When to Activate

- User says: "help", "what should I work on?"
- When stuck or unsure
- Returning after time away
- Multiple things competing for attention

## Process

### 1. Deep Context Check

**Git status:**
```bash
git status -sb
git log --oneline -5
git diff --stat
```

**Inbox:**
```bash
ls -lt inbox/session-summaries/*.md 2>/dev/null | head -5
ls inbox/ 2>/dev/null
```

**Decisions pending:**
```bash
ls decisions/*.md 2>/dev/null | head -10
```

**Schema/summary:**
```bash
cat .claude/tachikoma-summary.yaml 2>/dev/null
```

### 2. Report Findings

```
System Assessment (YYYY-MM-DD):

Git Status:
- Branch: [name]
- Uncommitted changes: [yes/no]
- Recent commits: [summary]

Inbox Status:
- Session summaries: [N files]
- Status: [Clean / Needs processing]

Pending Decisions:
- [N] decisions waiting for review
- [List key ones]

Tachikoma Summary:
- Last scan: [date]
- Observations: [key points]
```

### 3. Suggest Priorities

**If uncommitted changes:**
```
Priority 1: Git hygiene
- Uncommitted changes in [files]
- Review and commit before other work
```

**If inbox has items:**
```
Priority 1: Process inbox
- [N] session summaries from [dates]
- Run "learn" to update system
- Then "cleanup" to archive
```

**If pending decisions:**
```
Priority 1: Review decisions
- [N] tachikoma decisions pending
- Review and apply or reject
```

**If everything clean:**
```
System is healthy:
- Inbox clean
- Git clean
- No pending decisions

What do you want to work on?
```

### 4. Ask What User Wants

```
Based on this, what do you want to focus on?
```

## Difference from Start/Startup

- **start/startup:** Quick context, begin work
- **help:** Deep analysis, identify problems, suggest priorities

Use `help` when stuck or returning after time away.
