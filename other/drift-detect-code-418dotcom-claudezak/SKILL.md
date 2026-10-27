---
description: Detect system configuration drift - find stale rules, contradictions, and orphans
argument-hint: ""
allowed-tools:
  - Read
  - Agent
  - Glob
  - Grep
  - Bash(wc:*, find:*, date:*)
---

Self-monitoring command. Scans your entire Claude Code configuration for drift — stale rules, contradictions, orphaned files, and configuration inconsistencies.

## Steps

### Step 1: Scan system files (parallel)

Read all configuration sources simultaneously:
- `CLAUDE.md` — project instructions
- `.claude/memory.md` — active memory
- `.claude/knowledge-base.md` — learned rules
- `.claude/settings.json` — hooks configuration
- `.claude/command-index.md` — command registry (if exists)

### Step 2: Check for contradictions

**Within CLAUDE.md:**
- Are there conflicting instructions? (e.g., "always do X" and "never do X")
- Are there references to files or directories that don't exist?
- Are there references to commands or agents that aren't defined?

**Between CLAUDE.md and knowledge-base:**
- Does the knowledge base contain rules that contradict CLAUDE.md?
- Are there duplicate rules across both files?

**Between memory and reality:**
- Does memory reference tasks, files, or states that no longer exist?
- Are there "current focus" items that are clearly stale?

### Step 3: Check for orphans

Scan for:
- **Orphaned commands:** Files in `.claude/commands/` not referenced in command-index.md
- **Orphaned agents:** Agent definitions with no command or skill that invokes them
- **Orphaned skills:** Skills not referenced by any command, agent, or CLAUDE.md
- **Dead references:** Mentions of files, URLs, or paths that don't exist
- **Unused hooks:** Hook scripts that exist but aren't wired in settings.json

### Step 4: Check for staleness

- **Memory.md:** Is "Now" section from more than 3 days ago?
- **Knowledge-base entries:** Do any reference outdated tools, APIs, or patterns?
- **Daily notes:** Are there daily notes from 30+ days ago that should be archived?
- **Task Board:** Are there tasks that have been "in progress" for more than a week?

### Step 5: Check configuration health

- **settings.json:** Is it valid JSON? Are all hook scripts executable?
- **CLAUDE.md size:** Is it growing too large? (>500 lines is a warning)
- **Memory.md size:** Is it within limits? (<100 lines target)
- **Knowledge-base size:** Is it within limits? (<200 lines target)

### Step 6: Generate drift report

```markdown
# Drift Detection Report

**Date:** [date]
**Status:** [CLEAN / WARNINGS / ISSUES FOUND]

## Contradictions Found
- [contradiction with file references]

## Orphaned Items
- [orphaned file or reference]

## Stale Items
- [stale memory, task, or reference]

## Configuration Health
| Check | Status | Note |
|-------|--------|------|
| settings.json valid | Pass/Fail | |
| CLAUDE.md size | [lines] | [ok / warning] |
| memory.md size | [lines] | [ok / warning] |
| knowledge-base size | [lines] | [ok / warning] |
| Hook scripts executable | Pass/Fail | |

## Recommended Actions
1. [Specific fix]
2. [Specific fix]
3. [Specific fix]

---
Run monthly or when system behaviour feels off.
```

Output the status line and any critical issues. Offer to fix automatically if issues are simple.
