---
name: distilling-plan-learnings
description: Extracts decisions, rejected alternatives, and patterns from recent plans into a persistent learnings document. Use after completing a plan or sprint.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob, Edit, Write
  argument-hint: "[time-range] [output-path]"
  context: fork
  stability: development
---

# Plan-to-Learnings Distiller

**Target**: $ARGUMENTS

Extracts structured learnings from Claude Code plan files. Distills decisions
made, alternatives rejected, and patterns discovered into a persistent document
that compounds project knowledge over time.

## Arguments

| Position | Name | Required | Default | Description |
|----------|------|----------|---------|-------------|
| 1 | `time-range` | no | `7d` | E.g. `7d`, `30d`, `this-week`. Filter plans by modification time. |
| 2 | `output-path` | no | `docs/learnings/from-plans.md` | Where to write/append output. |

**Examples:**

```text
/distilling-plan-learnings                          # Last 7 days → docs/learnings/from-plans.md
/distilling-plan-learnings 30d                      # Last 30 days
/distilling-plan-learnings 7d ./my-learnings.md     # Custom output path
```

## Data Source

```text
~/.claude/
├── plans/*.md                       # Plan mode files (filtered by mtime)
```

## When to Use

- After completing a plan or sprint — capture what was learned
- At week/sprint boundaries — accumulate decision history
- Before starting a new plan — review past decisions and patterns

## Do Not Use

- For real-time plan editing (use plan mode directly)
- For cross-project synthesis (use `/synthesizing-cc-bigpicture`)
- For session-level context (use session-memory)

## Workflow

1. **Parse arguments** — Apply defaults per Arguments table. Resolve output path.
   Create parent directories if needed.

2. **Glob plans** — Glob `~/.claude/plans/*.md`. Filter by modification time
   against the `time-range` argument. Sort by mtime descending (newest first).
   If no plans match, report "No plans found in time range" and stop.

3. **Read each plan** — Read matching plan files sequentially. Extract content
   sections, noting plan title and date.

4. **Extract learnings** into three categories:

   - **Decisions made** — Choices that were committed to. Look for: selected
     approaches, accepted trade-offs, finalized designs, chosen tools/patterns.
   - **Alternatives rejected** — Options considered but not chosen. Look for:
     crossed-out items, "decided against", "considered but", trade-off
     discussions, pros/cons where one side won.
   - **Patterns discovered** — Recurring themes or insights. Look for: repeated
     blockers, successful strategies, workflow improvements, reusable solutions.

5. **Format output** — Structure with date headers per plan. Group by category
   within each plan section.

6. **Write or append** — If output file exists, append new entries below
   existing content with a separator. If new, write with header.

## Output Format

```markdown
# Learnings from Plans

## <Plan Title> — <YYYY-MM-DD>

### Decisions Made
- <decision>: <rationale>

### Alternatives Rejected
- <alternative>: <why rejected>

### Patterns Discovered
- <pattern>: <context and implication>

---
```

## Common Pitfalls

- **Inventing learnings**: Only extract what is explicitly stated or strongly
  implied in plan text. Do not infer decisions that aren't there.
- **Duplicating entries**: When appending, check existing content for duplicates
  before adding.
- **Over-extraction**: Prefer fewer, high-quality entries over exhaustive lists.
  Each entry should be actionable or informative.

## Quality Check

- Correct > Complete > Minimal (ACE-FCA)
- Every entry traces to a specific plan file
- Decisions include rationale, not just the choice
- Alternatives include why they were rejected
- Patterns are genuinely recurring (seen in 2+ plans) or significant
