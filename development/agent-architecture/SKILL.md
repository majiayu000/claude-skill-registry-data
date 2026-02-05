---
name: agent-architecture
description: Prompt-native architecture patterns, agent orchestration, iteration loops, and state management for autonomous work.
triggers:
  - "agent.*native"
  - "prompt.*native"
  - "orchestrat"
  - "iteration loop"
  - "state management"
  - "handoff"
---

<objective>

Provide architectural guidance for prompt-native agent systems. This skill covers orchestration patterns, iteration loops, state management, and agent handoffs.

</objective>

<essential_principles>

## The Crew Philosophy

**Agents work, you orchestrate.** Spawn agents for heavy lifting, keep main thread light for decisions.

**State survives compaction.** All branch state lives in `.claude/branches/{branch}/state.json`.

**Handoffs are mandatory.** Every task completion creates a handoff. Knowledge persists.

**Iteration until done.** Use loops for tasks with verifiable completion criteria.

</essential_principles>

<routing>

## Task Routing

| Task | Resource |
|------|----------|
| Agent orchestration | `references/orchestration.md` |
| Iteration loops | `references/iteration-loop.md` |
| State persistence | `references/state-management.md` |
| Architecture patterns | `references/architecture/` |

## Workflows

| Workflow | Purpose |
|----------|---------|
| `loop.md` | Iteration loop for autonomous completion |
| `cancel-loop.md` | Graceful loop termination |
| `handoff.md` | Create context preservation documents |
| `compound.md` | Extract learnings into permanent knowledge |
| `triage.md` | Categorize and prioritize findings |

</routing>

<references>

## Domain Knowledge

### Core Patterns
- `orchestration.md` - Agent spawning patterns
- `iteration-loop.md` - Loop mechanics, completion promises
- `state-management.md` - Unified state format

### Architecture (`references/architecture/`)
- `architecture-patterns.md` - Prompt-native design
- `orchestrator-patterns.md` - Agent orchestration
- `system-prompt-design.md` - System prompts
- `mcp-tool-design.md` - MCP tool patterns
- `self-modification.md` - Self-modifying systems
- `refactoring-to-prompt-native.md` - Migration patterns
- `infrastructure.md` - Infrastructure patterns
- `architecture-checklist.md` - Review checklist

</references>
