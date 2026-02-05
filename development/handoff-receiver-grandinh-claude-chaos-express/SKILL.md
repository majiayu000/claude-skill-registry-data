---
name: handoff-receiver
description: Parse and execute incoming handoffs from Cursor following the normalized handoff schema with mixed-capability phases (analysis and write-capable)
schema_version: 1.0
---

# Handoff Receiver Skill

## Purpose

Parse and execute incoming handoffs from Cursor following the normalized handoff schema.

## Capability

**MIXED CAPABILITY:**
- **Phases 1-2 (Parse & Validate):** ANALYSIS-ONLY - Can run in any DAIC mode
- **Phases 3-4 (Execute & Update):** WRITE-CAPABLE - Requires IMPLEMENT mode

**Note:** The skill is configured in skill-rules.json as WRITE-CAPABLE with allowedModes: ["IMPLEMENT"] to ensure proper gating. When invoked outside IMPLEMENT mode, it will only execute phases 1-2 (read-only operations).

## When to Use

- User says "check handoffs", "what did Cursor hand off", or "execute handoff"
- Starting work on a branch that has a recent handoff entry
- After Cursor creates a task and hands it to Claude

## Workflow

### Phase 1: Parse & Present (ANALYSIS-ONLY)

1. Read `docs/ai_handoffs.md`
2. Parse YAML entries using normalized schema (schema_version 1.0)
3. Find latest entry where `to: claude`
4. Display to user:
   - `from`: who sent it
   - `timestamp`: when
   - `issue_id` and `branch`: context
   - `completed`: what Cursor did
   - `next`: what Claude should do
   - `context_files`: relevant docs to read

### Phase 2: Validate (ANALYSIS-ONLY)

5. Check for clear acceptance criteria in `next` tasks
6. If missing, propose concrete criteria and ask user to confirm
7. Verify `context_files` paths exist
8. Check `repo_state` if present (validate branch, warn about dirty_files)

### Phase 3: Execute (WRITE-CAPABLE - requires IMPLEMENT mode)

9. User must approve execution (say "yert" or similar)
10. Read any `context_files` referenced in the handoff
11. Execute `next` tasks in logical order following DAIC workflow
12. Track what was completed with file paths

### Phase 4: Update Handoff (WRITE-CAPABLE - requires IMPLEMENT mode)

13. Update the handoff entry's `completed` field with:
    - Tasks completed from original `next` list
    - File paths touched
    - Any caveats or partial completions
14. Preserve all original handoff data (don't delete/reformat)

## Schema Compatibility

Supports both schemas for backward compatibility:
- **Read**: Accepts `from_agent`/`to_agent`/`needed` OR `from`/`to`/`next`
- **Write**: Always uses normalized schema (`from`/`to`/`next` + `schema_version`)

## Example Invocation

```
User: "Check if Cursor handed anything off"
Assistant: [Reads docs/ai_handoffs.md, finds latest to:claude entry, displays]

User: "Execute it"
Assistant: [Requires IMPLEMENT mode] "I need to be in IMPLEMENT mode to execute handoff tasks. Say 'yert' to approve."

User: "yert"
Assistant: [Executes tasks, updates completed field]
```

## Safety Rules

- **Never execute** handoff tasks outside IMPLEMENT mode
- **Always validate** repo_state before writes if present
- **Preserve** historical handoff entries (append, never delete)
- **Log** any issues in context/gotchas.md if handoff is malformed

## Integration with cc-sessions

This skill respects cc-sessions DAIC workflow:
- **DISCUSS/ALIGN**: Can parse and display handoffs (Phase 1-2)
- **IMPLEMENT**: Can execute tasks and update completed field (Phase 3-4)
- **CHECK**: Should not modify handoffs

When in IMPLEMENT mode, this skill follows approved todos from the task manifest.
