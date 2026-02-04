---
name: coihuin-compress
description: Context compression for long coding sessions. Creates checkpoints (state snapshots) and maintains them as you work.
---

# Coihuin Compress

Context compression at natural breakpoints, not reactive to token limits.

## Workflow

```
Session 1 (new work):
  → "checkpoint" → creates new checkpoint
  → chkcc current <checkpoint> → set as current

Session 2+ (continuing):
  → Read checkpoint file
  → chkcc current <checkpoint> → set as current
  → work + continuous maintenance
  → "archive" when done
```

## Continuous Maintenance

**This is the core principle.** Don't wait for "delta" commands. Update the checkpoint as you work:

| When This Happens | Update This Section |
|-------------------|---------------------|
| Decision made | → Decisions |
| File created/modified/deleted | → Artifact Trail |
| Task completed | → Play-By-Play, Current State |
| Blocker hit | → Breadcrumbs, Next Actions |
| Direction changes | → Session Intent, Next Actions |

**Update immediately, not in batches.** Small, frequent updates keep the checkpoint alive in your working memory.

## Checkpoint States

| State | Location | Meaning |
|-------|----------|---------|
| **current** | `checkpoints/active/` | The ONE checkpoint being actively worked on |
| **active** | `checkpoints/active/` | In-progress work (not immediate focus) |
| **archived** | `checkpoints/archive/` | Completed work |

```bash
chkcc current <checkpoint>  # Set as current
chkcc current               # Show current
chkcc current --clear       # Clear current
chkcc status                # Show all active with summaries
```

## Operations

### Checkpoint

Create new state snapshot.

**Trigger**: "checkpoint", "create checkpoint"

**How**:
1. Read `checkpoint-format.md` for structure
2. Extract "What Must Survive" from conversation
3. Generate checkpoint following the format
4. Save to `checkpoints/active/<name>.md`
5. Update `checkpoints/active/INDEX.md`

### Delta (Explicit)

Force a structured update when you want visibility into what changed.

**Trigger**: "delta", "update checkpoint"

**How**:
1. Add `## Delta: <timestamp>` section to checkpoint
2. Summarize what changed since last delta
3. Update main sections with current state

Note: With continuous maintenance, explicit deltas are less necessary. Use when you want a clear marker of progress.

### Archive

Complete work and move to historical storage.

**Trigger**: "archive"

**How**:
1. Capture outcome from user:
   > What was achieved? Any learnings worth preserving?
2. Add `## Completion` section with status, outcome, learnings, date
3. Move to `checkpoints/archive/`
4. Update `checkpoints/active/INDEX.md`
5. Learnings auto-extracted to `checkpoints/LEARNINGS.md`

**Validation**: Cannot archive checkpoints with active children (use `--force` to override).

## Fork Detection

When work diverges into parallel streams, offer options:

**Strong signals** (any one suggests fork):
- User says work is unrelated
- Different issue/ticket involved
- Fundamental context switch

**Weak signals** (two+ together suggest fork):
- Working in entirely different files
- Scope expanding beyond original intent
- New dependencies unrelated to current work

**When detected**, present options:
- A) Create separate checkpoint (sets `parent` for lineage)
- B) Continue with current (expand scope)
- C) Set aside divergent work

**Not a fork**: Trivial fixes, config changes, supporting changes for main work.

## Directory Structure

```
checkpoints/
├── active/
│   ├── INDEX.md
│   └── chk-*.md
├── archive/
│   └── chk-*.md
└── LEARNINGS.md          # Accumulated insights from archives
```

## Reference Files

| File | Purpose |
|------|---------|
| `checkpoint-format.md` | Checkpoint structure specification |
| `index-format.md` | INDEX.md structure specification |
| `LEARNINGS.md` | Accumulated learnings from archived checkpoints |

## Priority Hierarchy (token pressure)

1. **Must Keep**: Problem, session intent, decisions, current state, next actions
2. **Should Keep**: Recent artifacts, recent play-by-play, technical context, breadcrumbs
3. **Can Summarize**: Older play-by-play, completed artifacts, historical decisions

## Quality Self-Check

Before finalizing updates, verify:

1. **Problem Clarity**: Could a fresh agent understand without the conversation?
2. **Decision Rationale**: Is the "why" captured, not just the "what"?
3. **State Specificity**: Concrete progress, not vague status?
4. **Action Actionability**: Can someone execute Next Actions immediately?
5. **Fresh Agent Test**: Loading this cold, would you know exactly what to do?
