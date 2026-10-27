---
name: research
description: Isolated codebase exploration that preserves your main context. Use when you need to understand code structure, trace call paths, or gather evidence before making changes. Spawns an explorer subagent.
---

# Research Skill

Explore the codebase without polluting your main context.

## When to use
- Need to understand how a module works before changing it
- Need to find where a pattern is used across the codebase
- Need to trace a call path end-to-end
- Need to gather evidence before proposing a plan

## Protocol

### Option A — Spawn an explorer subagent (recommended)
> "Spawn an explorer subagent to [describe the research goal]. Return a structured summary with: files examined, relevant symbols, call path trace, and key findings."

The explorer runs in read-only mode in isolated context — your main thread stays clean.

### Option B — Inline research (for quick lookups)

#### Find files matching a pattern
```bash
find . -name '*.ts' -path '*/auth/*' | head -20
```

#### Search for symbol usage
```bash
grep -rn --color=never 'functionName' --include='*.ts' . | head -30
```

#### Trace a call path
```bash
# 1. Find where the function is defined
grep -rn --color=never 'def functionName\|function functionName\|functionName =' . | head -10

# 2. Find all callers
grep -rn --color=never 'functionName(' . | grep -v 'def functionName\|function functionName' | head -20
```

#### Read a specific file section
Use file reading tools — do NOT cat the whole file.

## Research Output Format
After research, summarize findings:
```
## Research Summary: <topic>

### Files examined
- path/to/file.ts — reason

### Key symbols found
- SymbolName (file:line) — what it does

### Call path trace
Entry → ServiceA.method → ServiceB.method → DB query

### Key findings
1. Finding 1
2. Finding 2

### Open questions
- ?
```

## Rules
- Keep research scope tight — stop when you have enough evidence
- Do NOT modify files during research
- Save verbose intermediate output to `claude/tasks/research-notes.md` (not in main context)
