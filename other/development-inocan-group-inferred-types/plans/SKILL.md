---
name: plans
description: Use when working on implementation phases, checking phase status, or planning work. Provides context for the structured planning system in .plans/ folder.
version: "1.1.0"
---

# Structured Planning System

This project uses a phased implementation approach. Plans are stored in `.plans/` as markdown files with YAML front matter.

## Phase Files Location

```
.plans/
├── README.md           # Schema documentation
├── 00-foundation.md    # Project setup, tokens, base layout
├── 01-threshold.md     # Hero section + scroll transition
├── 02-navigation.md    # Nav system + name-to-logo
├── 03-home-content.md  # Bio, latest, footer sections
├── 04-work-page.md     # Curated projects + archive
├── 05-about-page.md    # Bio + artist statement
├── 06-press-page.md    # Press grid + cards
└── 07-polish.md        # Performance, a11y, deployment
```

## Front Matter Schema

Each phase file has this structure:

```yaml
---
phase: 0                  # Numeric order (0-indexed)
title: "Phase Title"      # Human-readable name
status: draft             # draft | in-progress | blocked | review | complete
priority: P1              # P0 | P1 | P2 | P3
effort: medium            # small | medium | large | xlarge
dependencies: []          # Array of phase numbers
blockers: []              # Blocking issues
started: null             # ISO date
completed: null           # ISO date
owner: null               # Assignee
---
```

## Status Values

| Status | Meaning |
|--------|---------|
| `draft` | Defined but not actionable |
| `in-progress` | Active development |
| `blocked` | Cannot proceed |
| `review` | Needs verification |
| `complete` | Done and verified |

## Working with Phases

### Before Starting Work

1. Read the phase file to understand scope
2. Check dependencies are complete
3. Update status to `in-progress`
4. Add `started` date

### During Implementation

1. Follow tasks in order
2. Check off acceptance criteria as completed
3. Note any blockers discovered

### After Completing

1. Verify all acceptance criteria met
2. Update status to `complete`
3. Add `completed` date
4. Check if this unblocks other phases

## Commands

- `/plan-status` — View all phase statuses
- `/plan-next` — Get next actionable phase
- `/plan-start [phase]` — Begin a phase
- `/plan-complete [phase]` — Mark phase done

## Common Patterns

### Reading a Phase

```
Read .plans/01-threshold.md to understand the threshold implementation requirements.
```

### Updating Status

After completing work, edit the front matter:

```yaml
status: complete
completed: 2024-01-15
```

### Checking Dependencies

A phase is actionable when all items in its `dependencies` array have `status: complete`.

## Tips

- Don't skip phases — dependencies exist for a reason
- Update status immediately when starting/completing
- If blocked, document the blocker and move on
- Review acceptance criteria before marking complete
