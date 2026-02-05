---
name: expansion-evaluation
description: >-
  Manage the SoNash expansion evaluation process for reviewing ~280 feature and
  technical ideas across 21 modules. This skill should be used when the user
  wants to evaluate expansion ideas, track progress, make decisions, or resume
  an evaluation session. Supports commands: begin, evaluate, status, decide,
  questions, push-to-roadmap, end.
---

# Expansion Evaluation Skill

## Purpose

This skill manages a structured, resumable process for evaluating SoNash
expansion ideas from 21 modules (12 feature + 9 technical). It maintains state
across sessions and enables flexible navigation between modules and ideas.

## When to Use

- User wants to evaluate expansion ideas
- User says "expansion", "/expansion", or references the expansion docs
- User wants to check progress on expansion evaluation
- User wants to resume a previous evaluation session

## Command Reference

| Command                            | Description                         |
| ---------------------------------- | ----------------------------------- |
| "/expansion begin"                 | Initialize or resume evaluation     |
| "/expansion evaluate [module]"     | Jump to a specific module           |
| "/expansion evaluate [module] [n]" | Jump to specific idea in module     |
| "/expansion status"                | Show progress and recent decisions  |
| "/expansion decide [action]"       | Record decision for current idea    |
| "/expansion questions"             | Review open questions               |
| "/expansion push-to-roadmap"       | Push staged decisions to ROADMAP.md |
| "/expansion end"                   | Save checkpoint and commit          |

### Decision Actions

Use with "/expansion decide":

- `accept [milestone] [reason]` - Stage idea for ROADMAP (NOT pushed
  immediately)
- `defer [reason]` - Good idea, but not now
- `reject [reason]` - Doesn't fit vision/scope
- `merge [roadmap-item] [reason]` - Already in ROADMAP, enhance existing
- `discuss` - Mark for further discussion

## ROADMAP Integration Process

**CRITICAL: Decisions are STAGED, not immediately pushed to ROADMAP.md.**

### Why Staged?

1. Prevents ROADMAP churn during evaluation
2. Allows batch review before committing
3. User maintains control over when changes are made
4. Enables course correction before integration

### Workflow

1. During evaluation, accepted ideas are logged in tracker's "Staged for
   ROADMAP" section
2. User can review staged items anytime with "/expansion status"
3. User explicitly requests "/expansion push-to-roadmap" when ready
4. Only then are items added to ROADMAP.md and committed
5. After push, staged items move to "Accepted Ideas Summary"

### Push Command

```
/expansion push-to-roadmap
```

1. Read all items from "Staged for ROADMAP" section
2. Present summary for user confirmation
3. On confirmation, add items to appropriate ROADMAP.md sections
4. Move items from "Staged" to "Accepted Ideas Summary"
5. Commit both files with descriptive message

## Foundational Decisions (Resolved 2026-01-21)

These decisions guide ALL module evaluations:

### Architecture

- **Offline priority:** Per-feature decision (not blanket policy)
- **Encryption:** Mandatory maximum for all step work
- **Native wrapper:** Deferred (focus on PWA first)

### Features

- **Nashville scope:** Nashville-first, abstracted (city as parameter)
- **Sponsor model:** Push only (sponsee sends snapshots)
- **Meeting finder:** Explore automation scripts

### Technical Tooling

- **IndexedDB:** Dexie.js (rich queries, React hooks, encryption addon)
- **PDF generation:** @react-pdf/renderer (React components, lazy-loaded)
- **Analytics:** Minimal custom (Tier 1 anonymous + Tier 2 opt-in)

### Process

- **Evaluation order:** Hybrid dependency-grouped (7 phases)
- **ROADMAP integration:** Staged with explicit push

## Approved Evaluation Order

7-phase dependency-grouped flow:

| Phase | Modules             | Focus                    |
| ----- | ------------------- | ------------------------ |
| 1     | T4 → F4 → T1 → T3   | Core Privacy Foundation  |
| 2     | F1 → T2 → F5 → F9   | Core Features            |
| 3     | F2 → F7 → T5        | Sponsor & Sharing        |
| 4     | F3 → F6             | Local & Knowledge        |
| 5     | F10 → F8            | Safety & Personalization |
| 6     | T7 → T6             | Quality & Operations     |
| 7     | F11 → T8 → F12 → T9 | Future Vision            |

## Core Workflow

### Begin Session

```
/expansion begin
```

1. Read `docs/EXPANSION_EVALUATION_TRACKER.md`
2. Display current progress summary
3. Show Quick Resume context from previous session
4. Suggest next module based on evaluation order
5. Show any staged items awaiting ROADMAP push

### Evaluate Module

```
/expansion evaluate T4
/expansion evaluate F1 5
```

1. Load the specified module content from expansion docs
2. Check ROADMAP overlap for each idea (FIRST!)
3. Present ideas one at a time with evaluation criteria
4. Discuss feasibility, dependencies, user benefit
5. Record decisions incrementally in tracker
6. Stage accepted items (do NOT push to ROADMAP yet)

### End Session

```
/expansion end
```

1. Update tracker with all decisions made
2. Set "Quick Resume" section with context for next session
3. List any new open questions
4. Remind user of staged items count
5. Commit tracker changes to git

## Evaluation Criteria

For each idea, assess:

| Criteria        | Question                                     |
| --------------- | -------------------------------------------- |
| ROADMAP Overlap | Already planned? Partially covered? New?     |
| Offline Need    | Does this feature need offline support? (Q1) |
| Encryption      | Does this touch sensitive data? (Q3)         |
| Feasibility     | Can we build with current stack?             |
| Dependencies    | What modules/features must exist first?      |
| User Benefit    | How much value does this provide?            |
| Effort          | S/M/L/XL estimate                            |

## State Management

Primary state file: `docs/EXPANSION_EVALUATION_TRACKER.md`

The tracker maintains:

- Quick Resume section with last session context
- Foundational Decisions reference
- Approved Evaluation Order (7 phases)
- Module progress tables with phase assignments
- Staged for ROADMAP section (pending push)
- Decision log per module
- Cross-reference table (F↔T dependencies)

## File Locations

| File                                           | Purpose                     |
| ---------------------------------------------- | --------------------------- |
| `docs/EXPANSION_EVALUATION_TRACKER.md`         | Main state/progress tracker |
| `docs/SoNash Expansion - Technical Modules.md` | T1-T9 parsed modules        |
| `docs/SoNash Expansion - Module N - *.md`      | F1-F12 feature modules      |
| `ROADMAP.md`                                   | Target for accepted ideas   |

## Implementation Notes

1. **Always read tracker first** - Check current state before any action
2. **Update tracker incrementally** - Don't batch updates within a session
3. **Stage, don't push** - Accepted items go to staging, not ROADMAP
4. **Preserve discussion context** - Log key points in tracker
5. **Track dependencies** - Note when ideas depend on other modules
6. **Allow flexibility** - User can jump to any module at any time
7. **Remind about staged items** - On "/expansion end", show count of staged
   items
