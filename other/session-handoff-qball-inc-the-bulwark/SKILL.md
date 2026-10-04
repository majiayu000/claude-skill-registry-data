---
name: session-handoff
description: Create consistent session handoff documents for context transfer between sessions. Use when closing a session, reaching 75% token consumption, or when user requests handoff. Ensures proper YAML headers for metrics collection, LF line endings, and complete documentation of progress, decisions, and next steps.
user-invocable: true
allowed-tools:
  - AskUserQuestion
  - Read
  - Write
version: 1.0.0
author: "Ashay Kubal @ Qball Inc."
---

# Session Handoff

Create handoff documents that enable seamless context transfer between sessions.

## Critical Requirements

### Line Endings

Use LF (Unix) line endings only. Never CRLF.
- Use the Write tool directly (handles line endings correctly)
- Never copy-paste from Windows clipboard
- If you see `^M` characters, rewrite the file

### File Naming

**Pattern**: `sessions/session_{N}_{YYYYMMDD}.md`

- `{N}`: Session number (integer, no leading zeros)
- `{YYYYMMDD}`: Date without separators

Examples: `session_5_20260104.md` (correct), `session_05_20260104.md` (wrong)

## Handoff Template

````markdown
# Session {N} Handoff

```yaml
session: {N}
date: {YYYY-MM-DD}
phase: "P{X} - {Phase Name}"
task: "P{X}.{Y} - {Task Name}"
status: {completed | in_progress | blocked}
tokens_end: "~{X}K ({Y}%)"
```

---

## Session Summary

{2-3 sentences on outcomes, not process. What was achieved?}

## What Was Accomplished

- [x] {Completed item with file path}
- [x] {Completed item with file path}
- [ ] {Incomplete item - carried forward}

## Files Created/Modified

| File | Action | Lines | Purpose |
|------|--------|-------|---------|
| {path} | Created | ~{N} | {Brief description} |
| {path} | Modified | +{N}/-{M} | {What changed} |

## Verification Status

| Check | Status | Notes |
|-------|--------|-------|
| Typecheck | {Pass/Fail/Skipped} | |
| Lint | {Pass/Fail/Skipped} | |
| Tests | {Pass/Fail/Skipped} | {X/Y if applicable} |

## Technical Decisions

### {Decision Title}
- **Decision**: {What was decided}
- **Rationale**: {Why}
- **Impact**: {What it affects}

## What's Next

1. {Specific actionable step}
2. {Next step}

## Blockers / Issues

{List blockers or "None"}

## Learnings

{Patterns discovered or "None"}
````

## Section Guidelines

### YAML Header (Required)

The YAML header enables metrics collection. All fields required:

| Field | Format | Example |
|-------|--------|---------|
| session | Integer | `session: 5` |
| date | YYYY-MM-DD | `date: 2026-01-04` |
| phase | Quoted string | `phase: "P1 - Foundation"` |
| task | Quoted string | `task: "P1.2 - Test Auditor"` |
| status | Enum | `status: completed` |
| tokens_end | Quoted string | `tokens_end: "~95K (48%)"` |

### Session Summary

Focus on **outcomes** not process. What was delivered?

Good: "Completed session-handoff skill with CRLF handling. Ready for use."
Bad: "I started by reading files, then thought about structure, then wrote..."

### What Was Accomplished

- Use `[x]` for complete, `[ ]` for incomplete
- Include file paths
- Be specific

### Technical Decisions

Document decisions that affect future work. Include rationale so future sessions understand WHY. Skip if no significant decisions.

### Blockers / Learnings

Always include these sections. Write "None" if empty - don't omit.

## Memory Reflection (Mandatory)

Before finalizing the handoff, perform a two-part memory reflection:

### Part 1: Session Learnings → Memory Candidates

Review the session for durable insights worth persisting to memory:
- Feedback from the user (corrections, confirmations, preferences)
- Technical decisions that affect future sessions (not just this task)
- Project context that would be lost without memory (deadlines, stakeholder constraints)

**Filter:** Only flag items that (a) will persist beyond this session, (b) haven't already been saved to memory during the session, and (c) aren't derivable from code/git.

**Present candidates to the user for approval before writing.** Do not silently update memory.

### Part 2: Supersession Check

Review existing memory entries against current project state:
- Has any memory been invalidated by work done this session?
- Are there memories that reference completed phases, old file paths, or reversed decisions?
- Can any two memories be merged into one?

**Present proposed removals/updates to the user for approval before modifying.**

## Quick Checklist

Before finalizing:

- [ ] File named `session_{N}_{YYYYMMDD}.md`
- [ ] YAML header complete and valid
- [ ] All sections present (even if "None")
- [ ] Next steps are specific and actionable
- [ ] No CRLF line endings
- [ ] Memory reflection Part 1: session learnings reviewed with user, saved if approved
- [ ] Memory reflection Part 2: existing memory checked for superseded entries

## Examples

For detailed examples of completed and in-progress handoffs, see [references/examples.md](references/examples.md).
