---
name: supergraph
description: Meta-orchestrator — dispatches to the right skill for the task. Use before any non-trivial work.
mcp: codebase-memory-mcp
---

# supergraph

Graph evidence uses `codebase-memory-mcp` scoped by `CBM_PROJECT`. Orientation
loads `get_architecture` aspects `overview`, `layers`, `boundaries`, `clusters`,
and `hotspots`, plus validated `hubs`, `bridges`, and `test-gaps` recipes. If
optional graph evidence is unavailable, label it unavailable and use Serena or
filesystem evidence.

Dispatch to the right skill. 1% rule: if it *might* apply, invoke it.

## Priority

1. User CLAUDE.md / AGENTS.md (highest)
2. This skill set
3. Default system behavior

## Dispatch Table

| User intent | Skill to invoke |
|-------------|----------------|
| "start", "begin", unclear scope | `/supergraph:analyze` |
| "plan", "lên kế hoạch", explicit plan request | `/supergraph:plan` |
| "implement", "build", "execute" (plan saved) | `/supergraph:execute` |
| "fix bug", "debug", "why failing" | `/supergraph:fix` |
| "test", "TDD", "add tests" | `/supergraph:tdd` |
| "refactor", "clean up", "reorganize" | `/supergraph:plan` (then execute) |
| integration/e2e tests, after unit green | `/supergraph:integration` |
| "done?", "verify", before commit/PR | `/supergraph:verify` |
| "review", "merge", "PR", before merge | `/supergraph:review` |
| Need project context | `/supergraph:scan` |

## Adaptive Gate

- **< 20 lines, ≤2 files, no hub/bridge, complexity <10** → use `/supergraph:tdd` directly
- **≤5 files, clear requirement, no cross-boundary** → `/supergraph:plan` with lightweight tasks
- **>5 files, ambiguous, hub/bridge, cross-boundary** → `/supergraph:analyze` first, then plan

## User Instructions

"Add X" or "Fix Y" is the WHAT. Skills determine HOW. Never skip a skill because the task "feels simple."

## Red Flags (STOP if you catch yourself):

- "I'll just do it quickly" → pick a skill, follow it
- "I already know what to do" → skills evolve, load current one
- "This is too simple for a skill" → simple becomes complex fast

## Integration

All skills depend on `/supergraph:scan` being loaded first in the session.

## Subagent Guard

When dispatching subagents (executor, code-reviewer, plan-writer, plan-reviewer):
- Subagents get self-contained prompts — never session history
- Subagents do NOT trigger skills independently — this is the orchestrator's job
- Subagents report results back; orchestrator decides next step (fix, verify, review)
