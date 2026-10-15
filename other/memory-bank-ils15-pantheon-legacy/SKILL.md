---
name: memory-bank
description: "Memory bank rules, structure, and optimization — complete guide to Pantheon memory management."
context: fork
globs: []
alwaysApply: false
---

# Memory Bank

Complete guide to Pantheon memory bank — structure, rules, optimization, and maintenance.

---

## Two-System Model

| System | Where | Owner | Lifetime | Purpose |
|--------|-------|-------|----------|---------|
| **Memory Bank** | `.pantheon/memory-bank/` | Team | Permanent, versioned | Project context: architecture, patterns, progress |
| **VS Code `/memories/`** | `.vscode/` or workspace | Agent | Session/repo scoped | Atomic facts, conversation plans |

---

## Memory Bank Structure

```
.pantheon/memory-bank/
├── 00-project.md           ← What is this project? (fill once)
├── 00-architecture.md      ← System design and agent hierarchy
├── 00-components.md        ← Component breakdown and ownership
├── 00-tech-stack.md        ← Tech stack, setup, environment
├── 01-active-context.md    ← Current sprint focus, decisions, blockers (MOST IMPORTANT)
├── 02-progress-log.md      ← What works, what's left, milestones (append-only)
├── _tasks/
│   ├── _index.md           ← Task master list
│   └── TASK0001-name.md    ← Individual task records
└── _notes/
    ├── _index.md           ← Notes index
    └── NOTE0001-topic.md   ← Architectural decisions, findings
```

### File Update Frequency

| File | Fill when | Update frequency |
|------|-----------|-----------------|
| `00-project.md` | Project start | Rarely |
| `00-architecture.md` | Project start | On significant changes |
| `00-components.md` | Project start | When components added/removed |
| `00-tech-stack.md` | Project start | On stack changes |
| `01-active-context.md` | Each sprint | Each sprint / major decision |
| `02-progress-log.md` | First completion | Append-only per milestone |
| `_tasks/` | Sprint tracking | Per task |
| `_notes/` | Significant findings | Per finding |

---

## Golden Rules

1. **Never create `.md` files outside `.pantheon/memory-bank/`** (except `README.md`, `CONTRIBUTING.md`)
2. **Never create `ANALYSIS_*.md`, `SUMMARY_*.md`, `STATUS_*.md`** anywhere
3. **`01-active-context.md` is the priority file** — keep it current
4. **`02-progress-log.md` is append-only** — never edit history
5. **`_notes/` decisions are immutable** — supersede, never edit

---

## Session → Active Context Graduation

```
During sprint:
  Athena writes plan → /memories/session/sprint-plan.md   (ephemeral)
  Agents track wip   → /memories/session/wip.md            (ephemeral)

At sprint close:
  @mnemosyne consolidates → .pantheon/memory-bank/01-active-context.md
                          → .pantheon/memory-bank/02-progress-log.md (appended)
```

---

## Who Writes What

| Content | Written by | Where |
|---------|-----------|-------|
| Project overview, architecture | Mnemosyne (at init) | `00-03.md` |
| Sprint context, decisions | Agent / Mnemosyne | `01-active-context.md` |
| Milestone completions | Any agent | `02-progress-log.md` (append) |
| Task records | Mnemosyne (on request) | `_tasks/TASK000X-*.md` |
| Architecture decisions | Mnemosyne (on request) | `_notes/NOTE000X-*.md` |
| Atomic facts | Any agent | `/memories/repo/` |
| Conversation plans | Athena / any agent | `/memories/session/` |

---

## Optimization: Compression Rules

### Problem: Memory bank files grow too large, wasting tokens on every load.

### Strategy: Lazy-load only what's needed

| Rule | Before | After |
|------|--------|-------|
| **Active context** | 500+ lines of history | 50 lines: current sprint only |
| **Progress log** | Everything since day 1 | Link to archived logs; keep last 50 lines |
| **Task records** | All tasks in one file | One file per task; archive completed |
| **Notes** | Long narrative | Bullet points with links to source |

### Compression Targets

- `01-active-context.md`: Keep under 100 lines. Archive old sprints to `_notes/`.
- `02-progress-log.md`: Keep last 20 entries. Archive older to `_notes/archive/`.
- `_tasks/`: Mark completed tasks `[x]`, move to `_tasks/archive/`.

### Commands

```
@mnemosyne Compress memory bank          # Audit and compress all files
@mnemosyne Archive completed tasks       # Move done tasks to archive
@mnemosyne Trim active context           # Keep only current sprint
```

---

## Anti-Patterns

### ❌ Session output as files
```
# Wrong
Create IMPLEMENTATION_SUMMARY.md
Create STATUS.md

# Right
@mnemosyne Append to 02-progress-log.md: [summary]
```

### ❌ Mandatory handoff after every phase
```
# Wrong: After every phase → handoff to @mnemosyne

# Right: Agent appends to 01-active-context.md directly
At sprint close → explicit @mnemosyne invocation
```

### ❌ Duplicating information
```
# Wrong: Stack in 00-project.md AND /memories/repo/stack.json

# Right: Atomic facts → /memories/repo/ (auto-loaded)
         Narrative context → 00-project.md (explicit read)
```

---

## Adopting in a Product

```bash
mkdir -p .pantheon/memory-bank/_tasks .pantheon/memory-bank/_notes
touch .pantheon/memory-bank/_tasks/.gitkeep .pantheon/memory-bank/_notes/.gitkeep
# @mnemosyne Initialize memory bank for this repository
```

Add to `.github/copilot-instructions.md`:
```markdown
Always read .pantheon/memory-bank/01-active-context.md before answering.
```
