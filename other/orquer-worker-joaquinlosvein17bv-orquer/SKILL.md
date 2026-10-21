---
name: orquer-worker
description: "Instructions for subordinate/worker agents running inside Orquer panes. Enforces zero interactive terminal prompts, structured RPC questions via orquer msg ask, voluntary progress updates, and explicit task completion reporting."
---

# Orquer Worker Protocol

As a **Subordinate Worker Agent** running inside an Orquer pane, you carry out tasks delegated by the orchestrator.

## Cardinal Rules

1. **NEVER PRINT INTERACTIVE MENUS:** Strictly prohibited from rendering interactive CLI prompts (e.g. arrow-key selection, curses menus, inquirer prompts) to terminal stdout. The orchestrator does NOT scrape terminal screens.
2. **USE STRUCTURED RPC FOR DECISIONS:** Whenever you need a decision, confirmation, or choice among multiple options, you MUST invoke `orquer msg ask`.
3. **REPORT PROGRESS VOLUNTARILY:** Proactively send structured progress notifications to the orchestrator at key milestones.
4. **SIGNAL COMPLETION EXPLICITLY:** When your task finishes or encounters a blocker, send a `result` or `error` message.

---

## Workflow Guide

### 1. Identifying Your Context

When running inside an Orquer pane, your identity is set automatically in `$ORQUER_PANE_ID`:
```bash
echo "Running in pane: $ORQUER_PANE_ID"
```
All `orquer msg` commands will automatically use this ID as your `--from` identity.

### 2. Receiving Assigned Task

If you were spawned to wait for instructions:
```bash
TASK=$(orquer msg recv --recipient "$ORQUER_PANE_ID" --type task --wait --json)
GOAL=$(echo "$TASK" | jq -r '.payload.goal' 2>/dev/null || echo "$TASK" | grep -o '"goal":"[^"]*"' | head -1 | sed 's/.*:"//; s/"$//')
SENDER=$(echo "$TASK" | jq -r '.from' 2>/dev/null || echo "$TASK" | grep -o '"from":"[^"]*"' | head -1 | sed 's/.*:"//; s/"$//')
TARGET="${SENDER:-orchestrator}"
echo "Assigned goal: $GOAL from: $TARGET"
```

### 3. Requesting Decisions / Multi-Option Choices (`orquer msg ask`)

When you encounter multiple choices (e.g., architectural choices, package managers, database options, conflict resolution):

**DO NOT:** Print a prompt to the terminal or wait for interactive console keys.

**DO:** Call `orquer msg ask`:

```bash
# Ask the orchestrator to decide.
# This command pauses execution until the orchestrator replies, then prints the selected option.
CHOSEN_OPTION=$(orquer msg ask \
    --question "Which database engine should be used for this service?" \
    --option "SQLite" \
    --option "PostgreSQL" \
    --option "MySQL")

echo "Orchestrator selected: $CHOSEN_OPTION"
```

Or shorthand:
```bash
CHOSEN_OPTION=$(orquer ask \
    --question "Run tests before build?" \
    --option "yes" \
    --option "no")
```

If a timeout is desired:
```bash
CHOSEN_OPTION=$(orquer msg ask \
    --question "Proceed with migration?" \
    --option "yes" \
    --option "abort" \
    --timeout-ms 60000)
```

### 4. Sending Progress Updates

Keep the orchestrator informed as milestones complete:
```bash
orquer msg send --to "${TARGET:-orchestrator}" --type progress --payload '{"step": "database migration", "progress": "80%"}'
```

### 5. Reporting Final Result

When your work is done:
```bash
orquer msg send --to "${TARGET:-orchestrator}" --type result --payload '{
    "status": "completed",
    "summary": "Implemented auth service with JWT support",
    "files_changed": ["src/auth.rs", "src/models.rs"]
}'
```

### 6. Reporting Errors

If an unrecoverable error occurs:
```bash
orquer msg send --to "${TARGET:-orchestrator}" --type error --payload '{
    "error": "Integration test failed",
    "details": "Connection refused to redis:6379"
}'
```
