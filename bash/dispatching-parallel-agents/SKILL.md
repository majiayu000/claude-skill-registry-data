---
name: dispatching-parallel-agents
description: Launch parallel subagents for independent Godot work — use when 2 or more tasks have no shared files or sequential dependency.
---

# Godot Dispatching Parallel Agents

## Independence Check

Tasks are parallel-safe when they:
- Touch different `.gd` files
- Touch different `.tscn` scenes
- Do not share autoloads being mutated

Tasks require sequential execution when:
- One creates a class the other imports
- Both modify the same scene file
- One adds a signal the other connects to

## Dispatch

Launch all independent agents in one message. Each agent needs:

```
Task: <specific task from plan>
Scene: res://scenes/<scene>.tscn
Script: res://scripts/<script>.gd
Nodes: <NodeName1>, <NodeName2>
AgentBridge: available — use bash ${CLAUDE_SKILL_DIR}/../runner/scripts/godot-exec.sh
  --execute / --log / --save-all / --play / --stop
Skills: godot:coder, godot:verification-before-completion
Success criteria: <exact expected outcome — e.g., "res://scripts/player.gd exists, --log shows zero errors">
```

## After All Complete

1. `bash ${CLAUDE_SKILL_DIR}/../runner/scripts/godot-exec.sh --log 200` — detect any conflicts
2. `bash ${CLAUDE_SKILL_DIR}/../runner/scripts/godot-exec.sh --save-all` then verify each modified scene with `--execute`
3. Invoke `godot:verification-before-completion` on the full project
4. Invoke `godot:requesting-code-review`
