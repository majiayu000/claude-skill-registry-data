---
name: subagent-driven-development
description: Dispatch parallel subagents for independent Godot tasks — use when a plan has tasks with no shared files or sequential dependency.
---

# Godot Subagent-Driven Development

Execute a plan by dispatching a fresh subagent per task, with two-stage review after each: spec compliance first, then code quality.

**Core principle:** Fresh subagent per task + two-stage review = high quality, fast iteration.

## The Process

1. **Read plan file once** — extract all tasks with full text and context
2. **Create TodoWrite** with all tasks
3. **Per task:**
   - Dispatch implementer subagent with full task text + Godot context
   - Answer any questions before letting them proceed
   - After implementation: dispatch spec compliance reviewer
   - After spec ✅: dispatch code quality reviewer
   - After quality ✅: mark task complete in TodoWrite
4. **After all tasks:** invoke `godot:requesting-code-review`

## Context to Provide Each Subagent

Every dispatched subagent must receive:
- Full task text from the plan (don't make them read the plan file)
- Scene path(s) and node names they will touch
- AgentBridge command: `bash ${CLAUDE_SKILL_DIR}/../runner/scripts/godot-exec.sh`
- Skills to use: `godot:coder`, `godot:verification-before-completion`
- Success criteria (exact expected state — e.g., "--log shows zero errors, node X exists")

## Dispatch Template

```
Implement Task N from the plan:

<paste full task text here>

Scene: res://scenes/<scene>.tscn
Nodes involved: <NodeName1>, <NodeName2>
AgentBridge: bash ${CLAUDE_SKILL_DIR}/../runner/scripts/godot-exec.sh
  --execute / --log / --save-all / --play / --stop
Skills to use: godot:coder, godot:verification-before-completion
Success criteria: <exact expected state>
```

## Handling Implementer Status

**DONE:** Proceed to spec compliance review.

**DONE_WITH_CONCERNS:** Read concerns. If about correctness, address before review. If observational, note and proceed.

**NEEDS_CONTEXT:** Provide missing context and re-dispatch.

**BLOCKED:** Assess — provide more context, use a more capable model, or break the task into smaller pieces.

## Two-Stage Review

**Stage 1 — Spec compliance:** Does the implementation match the plan task exactly? No missing requirements, no extras.

**Stage 2 — Code quality:** Is the implementation well-built? Clean GDScript/C++, no magic numbers, proper error handling.

If either reviewer finds issues: implementer fixes → reviewer reviews again → repeat until ✅.

**Never start code quality review before spec compliance is ✅.**

## Independence Check

Tasks are independent when they touch:
- Different `.gd` / `.cpp` files
- Different `.tscn` scenes
- No autoloads being mutated by both

Tasks are NOT independent when:
- One creates a class the other imports
- Both modify the same scene
- One adds a signal the other connects to

## After All Tasks

1. `bash ${CLAUDE_SKILL_DIR}/../runner/scripts/godot-exec.sh --log 200` — check for conflicts
2. Verify each modified scene with `--execute`
3. Invoke `godot:requesting-code-review`

## Red Flags

- Never dispatch implementation subagents in parallel (conflicts on shared scenes/files)
- Never skip spec compliance review
- Never start code quality review before spec compliance ✅
- Never make subagents read the plan file — provide full task text directly
- Never proceed while a reviewer has open issues
