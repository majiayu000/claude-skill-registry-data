---
name: memory-review
description: >
  Review all memory layers, detect stale/duplicate/conflicting entries,
  and propose promotions between layers. Use when the user says "clean up memory",
  "review what I've saved", "memory is getting messy", "what's in my memory",
  "organize my notes", "promote this to CLAUDE.md", "memory audit",
  or after a long session with many /remember calls.
  Do NOT modify any files without explicit user approval.
origin: adapted:NanmiCoder/cc-haha (remember.ts)
license: MIT
version: 1.0.0
compatibility: "yana-ai >= 0.14.0. Reads: CLAUDE.md, CLAUDE.local.md, auto-memory, L1/L2."
---

<!-- Adapted from cc-haha/src/skills/bundled/remember.ts (MIT). Core pattern: collect → classify → propose → await approval. Changes: adapted to yamtam memory layers (L1/L2/auto-memory), added Anti-Fake-Pass. -->

## When to Use

- Use when: auto-memory has grown large and needs pruning
- Use when: user wants to know what's been remembered across sessions
- Use when: entries feel stale or contradictory
- Use when: something important should move from auto-memory to CLAUDE.md
- Do NOT use: to auto-apply changes — this skill proposes only, never modifies

## Memory Layers (yamtam)

```
L1 atomic    core/memory/L1_atomic/       Permanent facts — highest trust
L2 session   core/memory/L2_session/      Session-scoped, auto-expires
Auto-memory  ~/.claude/projects/.../memory/  Claude Code auto-memory
CLAUDE.md    Project-level instructions
```

## Process

### Step 1 — Collect all layers

```bash
# Auto-memory
cat ~/.claude/projects/*/memory/MEMORY.md 2>/dev/null
ls ~/.claude/projects/*/memory/*.md 2>/dev/null | head -20

# L1 atomic
ls core/memory/L1_atomic/*.md 2>/dev/null | head -20

# L2 session
ls core/memory/L2_session/*.md 2>/dev/null | head -10

# Project-level
head -50 CLAUDE.md 2>/dev/null
```

### Step 2 — Classify each entry

For each entry, assign one of:
- **PROMOTE** — important enough to move up (e.g., auto-memory → CLAUDE.md)
- **DEMOTE** — too specific to stay at this level (e.g., CLAUDE.md → auto-memory)
- **ARCHIVE** — outdated, no longer relevant
- **MERGE** — duplicate of another entry, should be combined
- **CONFLICT** — contradicts another entry, needs resolution
- **OK** — no action needed

### Step 3 — Generate the report

Format:
```
MEMORY REVIEW — [date]
━━━━━━━━━━━━━━━━━━━━━
Total entries: X across Y layers

PROMOTIONS (N)
  ↑ [entry summary] — auto-memory → CLAUDE.md
    Reason: used in 3+ sessions, project-level fact

CLEANUP (N)
  🗑 [entry] — outdated (references v0.13, current is v0.16)
  ⊕  [entry A] + [entry B] — duplicates, merge into one

CONFLICTS (N)
  ⚠ [entry A]: "use /tmp for builds" vs [entry B]: "builds go to target/"
    Needs resolution: which is current?

AMBIGUOUS (N)
  ? [entry] — unclear if still relevant, ask user

NO ACTION (N entries)
```

### Step 4 — Await explicit approval

Present the full report. Do not modify any files.

Ask: "Which of these should I apply? (all / list numbers / skip)"

Only after confirmation: apply the approved changes.

## Anti-Fake-Pass

```
❌ Modifying CLAUDE.md or any memory file without user approval
❌ Marking entries as stale without evidence (check dates/context)
❌ Promoting entries to CLAUDE.md that are session-specific
❌ Skipping the conflict detection step
✅ Report shown in full before any change
✅ User explicitly approved each action before it was applied
✅ Conflicts flagged — never silently resolved
```
