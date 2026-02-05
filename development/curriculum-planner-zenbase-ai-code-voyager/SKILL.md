---
name: curriculum-planner
description: |
  Generates sequences of high-leverage tasks that increase understanding and improve the code. Use when:
  - "what should I work on next?" - suggests prioritized tasks
  - "create a plan for this repo" - generates a curriculum
  - "what's the roadmap?" - shows curriculum overview
  - "help me onboard to this codebase" - creates learning tasks
  - "plan a refactor" - structures improvement work
  - "prioritize these features" - organizes work into tracks
  - "make an onboarding plan" - creates a learning path
  - "create a learning path for this repo" - sequences learning tasks
  - "roadmap this refactor" - plans improvement work
  - "write the curriculum to disk" - persists plan artifacts
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Repo Curriculum Planner

Generates structured learning/improvement plans based on repo state and session brain.

## Two Usage Modes

### Mode 1: Propose in Chat (default)

When a user asks for planning help, **propose tasks directly in the conversation** without writing files. This is the default behavior for quick suggestions.

Examples:
- "what should I work on next?" → Suggest 2-3 high-priority tasks in chat
- "what's the roadmap?" → Describe the plan conversationally
- "help me prioritize" → Discuss tradeoffs and recommend order

### Mode 2: Write Artifacts to Disk

Only write to `.claude/voyager/` when the user **explicitly asks** to persist the plan:
- "write the curriculum to disk"
- "save this plan"
- "generate curriculum files"
- "materialize the plan"

This writes:
- `.claude/voyager/curriculum.json` — structured task backlog
- `.claude/voyager/curriculum.md` — human-readable plan

## Trigger Phrases

Use this skill when you hear:
- "what should I work on next?"
- "create a plan"
- "what's the roadmap?"
- "help me onboard"
- "plan the work"
- "prioritize features"
- "what tasks remain?"
- "make an onboarding plan"
- "roadmap this refactor"

## On-Disk Plan Artifacts

When persisted, the plan lives at:
- `.claude/voyager/curriculum.json` — structured JSON with full task details
- `.claude/voyager/curriculum.md` — rendered Markdown for human review

To refresh an existing plan, run:
```bash
voyager curriculum plan
```

To preview without saving:
```bash
voyager curriculum plan --dry-run
```

## Task Structure

Each task includes:
- `id` — unique identifier (e.g., `t01`)
- `title` — short action-oriented title
- `why` — rationale for the task
- `estimated_scope` — `trivial`, `small`, `medium`, or `large`
- `acceptance_criteria` — how to know it's done
- `suggested_files` — where to look
- `commands_to_run` — verification commands
- `depends_on` — prerequisite task IDs
- `status` — `pending`, `in_progress`, `done`, or `blocked`

## Updating Task Status

Edit `curriculum.json` directly to update task status:
- Change `"status": "pending"` to `"in_progress"` when starting
- Change to `"done"` when complete

See `reference.md` for implementation details and schema reference.
