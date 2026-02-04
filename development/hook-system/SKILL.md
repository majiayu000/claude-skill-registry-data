---
name: hook-system
description: Claude Code Hook system entry point. Guides you to the right skill based on your needs.
allowed-tools: ["Read"]
---

# Hook System Guide

**Entry point** for Claude Code Hook system. Routes to appropriate skills.

## What are Hooks?

Scripts that auto-execute at specific events during Claude Code sessions.

```
User Input → [UserPromptSubmit Hook] → Claude Processing
          → [PreToolUse Hook] → Tool Execution → [PostToolUse Hook]
          → Claude Response → [Stop Hook] → End
```

## Skill Selection Guide

| Question | Skill |
|----------|-------|
| **What can** hooks do? | `hook-capabilities` |
| Need **pattern/implementation** examples | `hook-capabilities` → references |
| Need **templates** for quick start | `hook-templates` |
| Want to **call LLM** from hooks | `hook-sdk-integration` |
| Need **cost optimization** | `hook-sdk-integration` |
| Want **background execution** | `hook-sdk-integration` |

## Quick Decision Tree

```
Hook Question
    │
    ├─ "What's possible?" ──────→ hook-capabilities
    │
    ├─ "How to implement?" ─────→ hook-capabilities/patterns-detailed.md
    │
    ├─ "Need templates?" ───────→ hook-templates
    │
    ├─ "LLM evaluation?" ───────→ hook-sdk-integration
    │
    └─ "Real project examples?" → hook-capabilities/real-world-examples.md
                                  hook-sdk-integration/real-world-projects.md
```

## Hook Skills Architecture

```
                    hook-system (You are here)
                         │ Entry Point
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
   hook-capabilities  hook-templates  hook-sdk-integration
   ┌─────────────┐   ┌────────────┐   ┌─────────────────┐
   │ WHAT/WHY   │   │ HOW       │   │ ADVANCED       │
   │ • Events    │   │ • Gate    │   │ • LLM calls    │
   │ • Patterns  │   │ • Side Fx │   │ • Background   │
   │ • Debugging │   │ • Orch.   │   │ • Cost optim.  │
   └─────────────┘   └────────────┘   └─────────────────┘
         │                                    │
         └──────────► workflow-state-patterns ◄┘
                      (Multi-phase flows)
```

## Related Skills

| Skill | Role | When to Use |
|-------|------|-------------|
| `hook-capabilities` | Events, patterns, debugging | **First stop** - understanding what's possible |
| `hook-templates` | Gate/Side-effect/Orchestration templates | **Implementation** - copy-paste ready code |
| `hook-sdk-integration` | SDK/CLI LLM calls | **Advanced** - AI evaluation in hooks |
| `workflow-state-patterns` | State-based multi-phase workflows | **Complex** - chained automation with gates |

## Core Concepts

### Activation Reliability

| Method | Success Rate | When to Use |
|--------|--------------|-------------|
| **Hook** | **100%** | Forced automation |
| Hook + Forced Eval | **84%** | Skill activation |
| Skill (default) | ~20% | Simple suggestions |
| MCP (all tools) | ~13% | Many tools loaded |
| MCP (Tool Search) | ~43-88% | Enable `enableToolSearch` |

### Events (10 types)

| Event | Can Block | Use For |
|-------|-----------|---------|
| SessionStart | ❌ | Initialization |
| UserPromptSubmit | ✅ | Context injection |
| PreToolUse | ✅ | Gate (block/modify) |
| PostToolUse | ❌ | Side Effects |
| Stop | ✅ | Termination control |

### Data Passing

```bash
# Passed via stdin JSON (NOT environment variables!)
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id')
```

### Blocking

```bash
exit 0   # Allow
exit 2   # Block (stderr → feedback to Claude)
```

### MCP Tool Search

Enable for better tool selection (13% → 43%+):

```json
{
  "mcpServers": {
    "my-server": {
      "command": "...",
      "enableToolSearch": true
    }
  }
}
```

## References

- [Detailed Skill Selection Guide](references/skill-map.md)
