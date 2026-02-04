---
name: goal-synthesis
description: Use when user says "synthesize goals", "show goals", "what are my goals", "update goals", "show non-goals", "what am I building", "project direction", or asks about the overall direction or intent of the project - generates two markdown files summarizing the user's goals based on approved story nodes (what the goals ARE) and rejected story nodes with notes (what the non-goals ARE).
disable-model-invocation: true
---

# Goal Synthesis Skill

Generate `goals.md` and `non-goals.md` in `.claude/data/goals/`.

## Workflow

### Step 1: Check Prerequisites

```bash
python .claude/scripts/story_tree_helpers.py prereq
```

**Exit early if:**
- `needs_goals_update` = false AND `needs_non_goals_update` = false (counts unchanged)
- No story data (`approved_count` = 0 AND `rejected_with_notes_count` = 0)

### Step 2: Spawn Parallel Agents

Launch agents for files that need updating (haiku model):

**Agent 1 (goals)** - Only if `needs_goals_update` is true:
- Query: `python .claude/scripts/story_tree_helpers.py approved`
- Read existing `.claude/data/goals/goals.md` for context (if exists)
- Write `.claude/data/goals/goals.md` with sections: What We're Building, Target User, Core Capabilities, Guiding Principles, Footer with timestamp

**Agent 2 (non-goals)** - Only if `needs_non_goals_update` is true:
- Query: `python .claude/scripts/story_tree_helpers.py rejected`
- Read existing `.claude/data/goals/non-goals.md` for context (if exists)
- Write `.claude/data/goals/non-goals.md` with sections: Explicit Exclusions (with rejection reasons), Anti-Patterns, YAGNI Items, Philosophical Boundaries, Footer with timestamp

### Step 3: Update Metadata

After agents complete, update the synthesis metadata:

```bash
python .claude/scripts/story_tree_helpers.py update-meta
```

This records current counts so future prereq checks can skip synthesis when nothing has changed.

## Key Rules

- Spawn agents in parallel, never sequentially
- Use Python sqlite3 module, NOT sqlite3 CLI
- Include rejection reasons in non-goals bullets
- Read existing files first to preserve accumulated context
- Always run update-meta after successful synthesis
