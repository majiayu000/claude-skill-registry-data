---
name: bg
disable-model-invocation: true
description: "Background task router that spawns an agent with run_in_background: true. Use when typing '/bg <task>' or 'ctrl+b' to run a task in the background, or when mentioning 'background task', 'run in background', or 'defer this task'."
triggers:
  - "/bg"
  - "[bg]"
scope: harness
invocation: ability
---

# Background Task Router

## Usage

- `/bg <task>` — type the slash command followed by the task
- `[bg] <task>` — inserted automatically by `ctrl+b` keybinding, then submit

## Behavior

1. Strip `/bg ` or `[bg] ` prefix
2. Spawn immediately:
   ```
   Agent({
     description: "<3-word task>",
     prompt: "<task> — Caveman terse output. Return result only.",
     run_in_background: true
   })
   ```
3. Output one line: `→ BG: <3-word task>`
4. Return to main thread immediately. Do not wait. Do not narrate.

## Rules

- Never block main thread waiting for the spawned agent.
- Never output more than one confirmation line.
- Ambiguous task = spawn anyway. Background agents can resolve in context.
- Multiple `[bg]` prefixes in one message = multiple parallel spawns (one Agent call per task).
- Always use `run_in_background: true`. Never omit it.

## Session Notes

### 2026-04-27
- session: 1m | peak ctx: 43% | compacts: 0
- tools: Bash×15, Read×12
- corrections: none
- errors: none

### 2026-04-26
- session: 7m | peak ctx: 0% | compacts: 0
- tools: Bash×15, Read×9, Write×4, Agent×1, ToolSearch×1, ExitPlanMode×1, Edit×1
- corrections: none
- errors: none

### 2026-04-25
- session: 12m | peak ctx: 14% | compacts: 0
- tools: Bash×10, Read×9, Write×4, Edit×3, ToolSearch×1, ExitPlanMode×1
- corrections: none
- errors: none

### 2026-04-25
- session: created alongside tokenmaxxing skill | peak ctx: 18% | compacts: 0
- tools: Write×1
- corrections: none
- errors: none
- notes: works standalone without tokenmaxxing mode active. ctrl+b `[bg]` prefix is the primary trigger path.
