---
name: workflow-state-patterns
description: Hook-based state machine patterns for multi-phase workflows. Use when designing sequential workflows with quality gates.
allowed-tools: ["Read", "Write", "Grep", "Glob"]
---

# Workflow State Patterns

Multi-phase workflows need phase enforcement, session continuity, and quality gates. This pattern uses file-based state + hooks.

## Quick Start

1. Define phases: analyze → plan → execute → verify
2. Create state files on phase completion: `.workflow-phase-done`
3. Add PreToolUse hooks to check required state files
4. Add PostToolUse hooks to create state files

## Core Concept

```
Phase 1 → [POST HOOK] → .analysis-done
Phase 2 → [POST HOOK] → .plan-approved
Phase 3 → [PRE HOOK checks] → [POST HOOK] → .execution-done
Phase 4 → PASS: cleanup all / FAIL: preserve for retry
```

## State Files

| File | Purpose |
|------|---------|
| `.{workflow}-analysis-done` | Unlocks planning |
| `.{workflow}-plan-approved` | Unlocks execution |
| `.{workflow}-execution-done` | Marks modification complete |
| `.{workflow}-audit-passed` | Final success marker |

## Hook Template (Claude Code 1.0.40+)

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Task",
      "hooks": [{
        "type": "command",
        "command": "python3 scripts/workflow-gate.py",
        "timeout": 5
      }]
    }]
  }
}
```

Gate script checks `tool_input.subagent_type` and state files.

## Best Practices

1. **Prefix state files** - `.refactor-*`, `.migration-*`
2. **gitignore state files** - Don't commit workflow state
3. **Clean up on success** - Remove all state files on completion
4. **Preserve on failure** - Keep state for retry capability

## References

- [Complete Workflow Example](references/complete-workflow-example.md) - Full 4-phase implementation
- [Hook Details](references/hook-details.md) - Detailed hook configurations
