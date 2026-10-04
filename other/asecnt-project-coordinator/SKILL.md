---
name: ascent-task-coordinator
description: Multi-agent coordination pattern for Claude Code acting as Project Manager. Use when orchestrating background agents for feature implementation, when Claude Code should delegate rather than implement, or when running parallel investigation/implementation tasks. Provides task-list.json structure, progress tracking format, and agent role definitions. Keeps Claude Code in "coordinator mode" - dispatching work to specialized agents rather than writing code directly.
---

# Project Coordinator Skill

## Purpose

This skill enables Claude Code to operate as a **project manager** that coordinates multiple background agents to complete features. Claude Code should NEVER implement code directly—only dispatch, verify, and track progress.

## Process Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    COORDINATOR (Claude Code / Opus)             │
│                                                                 │
│  1. Read task-list.json                                         │
│  2. Find next eligible task (pending + deps complete)           │
│  3. Spawn background agent with minimal context                 │
│  4. Wait for completion                                         │
│  5. Run verification                                            │
│  6. Update progress-report.md                                   │
│  7. Repeat                                                      │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
   │ TypeScript  │     │   Swift     │     │    SQL      │
   │   Agent     │     │   Agent     │     │   Agent     │
   │  (Sonnet)   │     │  (Sonnet)   │     │  (Sonnet)   │
   └─────────────┘     └─────────────┘     └─────────────┘
```

## Task List JSON Structure

See `resources/task-list.schema.json` for full schema.

### Minimal Task Structure

```json
{
  "id": 9,
  "title": "Fix BUG-001: Blackout Dates",
  "status": "pending",
  "execution_mode": "delegate",
  "agent_type": "ascent-typescript-agent",
  "depends_on": [1],
  "files_to_modify": ["src/constraints/availability.ts"],
  "test_file": "tests/unit/blackoutDates.test.ts",
  "context_doc": "investigation-reports/bug-001-blackout-dates.md",
  "verification_cmd": "npm test -- --grep 'blackout'"
}
```

### Key Fields

| Field | Purpose |
|-------|---------|
| `status` | "pending", "in_progress", "complete", "failed" |
| `execution_mode` | "delegate" (spawn agent), "human" (skip), "coordinator" (do yourself) |
| `agent_type` | Which specialized agent to spawn |
| `depends_on` | Task IDs that must be complete first |
| `context_doc` | Path to investigation report or spec (agent reads this) |
| `verification_cmd` | Command to run after agent completes |

## Progress Report Format

Keep it lean. See `resources/progress-report.example.md`.

```markdown
# Progress: [Feature Name]
Updated: 2025-12-28 14:30

## Status: Batch 2 - P0 Fixes

## Completed
- [x] Task 1-8: Investigation (Batch 1)

## In Progress
- [ ] Task 9: Blackout Dates - in_progress (agent spawned 14:25)

## Up Next
- Task 10: Commitments

## Blockers
None
```

## Spawning Agents

When spawning a background agent, provide a **minimal prompt**:

```
Task 9: Fix BUG-001 - Blackout Dates

Context: Read investigation-reports/bug-001-blackout-dates.md

Files to modify:
- packages/engine/src/core/constraints/availability.ts
- packages/engine/src/core/types.ts

Test file to create:
- packages/engine/tests/unit/blackoutDates.test.ts

Approach: TDD - write failing tests first, then implement fix

When done, run: npm test -- --grep 'blackout'
```

DO NOT include:
- Full investigation report contents
- Implementation details
- Code snippets
- Anything the agent can read from files

## Verification Flow

```
Agent completes
      │
      ▼
Run verification_cmd
      │
      ├─── PASS ──→ Update status="complete", update progress-report.md
      │
      └─── FAIL ──→ Check error, decide:
                    - Retry with same agent
                    - Spawn different agent
                    - Flag for human review
```

## Batch Execution

Tasks can be organized into batches for parallel/sequential execution:

```json
"execution_strategy": {
  "batches": [
    {"ids": [1,2,3], "parallel": true, "name": "Investigation"},
    {"ids": [4,5], "parallel": false, "name": "Critical Fixes"}
  ]
}
```

- `parallel: true` → Spawn all agents at once
- `parallel: false` → Wait for each to complete before next

## File Organization

All artifacts belong in the feature folder. Structure:

```
features/1-in-progress/[feature-name]/
├── feature-brief.md              # Source of truth
├── task-list.json                # Agent-readable tasks
├── progress.md                   # Human-readable status
├── investigation-reports/        # Context gathering outputs
│   └── bug-001-[short-name].md
└── verification-reports/         # Test/review outputs
    └── integration-test-results.md
```

### Naming Convention

Pattern: `[task-id]-[type]-[short-name].md`

| Artifact Type | Pattern | Example |
|---------------|---------|---------|
| Investigation | `task-[id]-investigation-[topic].md` | `task-03-investigation-rest-days.md` |
| Implementation notes | `task-[id]-notes-[topic].md` | `task-09-notes-blackout-fix.md` |
| Verification | `task-[id]-verification-[scope].md` | `task-17-verification-integration.md` |
| Review | `task-[id]-review-[type].md` | `task-15-review-code.md` |

### Rules

- **No loose files** - Every artifact goes in a subfolder or is named with task ID
- **Feature folder only** - Never create files outside the feature folder
- **Link in progress.md** - If you create a file, add link to progress report
- **Prefer updating over creating** - Add to existing report rather than new file

### Token Efficiency

**Be extremely token efficient when creating artifacts:**

- **Not every task needs an artifact** - Only create artifacts when explicitly requested or when they provide essential context for future tasks
- **Minimize token output** - Use very brief summaries (2-3 sentences max) and 3-5 bullet points
- **Skip obvious details** - Don't document what's already clear from code or task description
- **Combine related artifacts** - Group multiple related findings into a single report rather than creating separate files
- **Focus on decisions and blockers** - Document why choices were made, not what was done (code shows that)

### Progress Report Links

When artifacts are created, add to progress:

```markdown
## Artifacts
- Task 3: [investigation-reports/task-03-investigation-rest-days.md]
- Task 17: [verification-reports/task-17-verification-integration.md]
```

## Resources

- `resources/task-list.schema.json` - JSON schema for validation
- `resources/task-list.example.json` - Minimal working example
- `resources/progress-report.example.md` - Lean format template
