---
name: catch-up
description: Reads session notes to provide context about recent work, decisions, and current state of the homelab repository. Use this skill when starting a new session, when asked about recent work, or when context is needed about previous sessions.
allowed-tools: Read, Grep, Glob
---

# Catch-Up Skill

## Purpose
Provides comprehensive context about recent work in the homelab repository. This ensures continuity across sessions and helps answer questions about what's been done recently.

## When to Use
- User asks: "What have we been working on?"
- User asks: "Catch me up" or "What's the current state?"
- User asks: "Review recent sessions"
- When context is needed about previous decisions or implementations
- At the start of a new session when user seems to be continuing previous work

## File Structure

```
.claude/notes/
├── CURRENT.md              # Last 3-5 sessions + current state (ALWAYS readable)
├── REFERENCE.md            # Stable: gotchas, patterns, architecture
└── sessions/               # Archived sessions (grep for historical lookups)
    ├── 2025-12-26-monitoring-stack-fixes.md
    ├── 2025-12-27-velero-alertmanager.md
    └── ...
```

## Instructions

### 1. Read CURRENT.md (Primary Context)

```
File: /Users/imcbeth/homelab/.claude/notes/CURRENT.md
```

This file is designed to always be readable (under token limits) and contains:
- Current state summary
- Last 3-5 sessions with full detail
- Session archive index

### 2. Extract Key Information

From CURRENT.md, identify:
- **Current State:** What's deployed, pending work, blockers
- **Recent Sessions:** Last 3-5 sessions with completed work, PRs, issues resolved
- **Next Steps:** Phase priorities from TODO.md

### 3. For Historical Lookups

If user asks about specific historical topics (e.g., "What did we do with Velero?"):

```bash
# Search archived sessions
grep -r "Velero" .claude/notes/sessions/
```

### 4. For Patterns/Gotchas

If user needs reference information:

```
File: /Users/imcbeth/homelab/.claude/notes/REFERENCE.md
```

Contains:
- Known gotchas and solutions table
- Common patterns (multi-source ArgoCD, Kustomization, Sealed Secrets)
- Sync wave order
- Architecture diagrams

## Output Format

Provide a **concise but comprehensive** summary:

```
## Recent Work Summary

**Current State:**
- [What's deployed and working]
- [Phase priorities]

**Last 3 Sessions:**
1. [Date] - [Session Name]: [Key accomplishments]
2. [Date] - [Session Name]: [Key accomplishments]
3. [Date] - [Session Name]: [Key accomplishments]

**Important Context:**
- [Key decisions/architecture notes]

**Next Steps:**
- [Priorities from TODO.md]
```

## Examples

**User**: "What have we been working on?"
**Action**: Read CURRENT.md, summarize last 3-5 sessions with focus on accomplishments and current state

**User**: "What monitoring changes did we make?"
**Action**: Read CURRENT.md, grep sessions/ for "monitoring", provide focused technical context

**User**: "Catch me up"
**Action**: Read CURRENT.md, provide comprehensive summary of recent work, current state, and next steps

**User**: "What are the known gotchas for this repo?"
**Action**: Read REFERENCE.md, summarize the gotchas table

## Notes

- CURRENT.md is designed to always be readable in one Read call
- Use grep on sessions/ only when historical context is needed
- REFERENCE.md is stable and rarely needs to be read in full
- Include PR numbers and status for easy reference
- Highlight any user action items that are pending
