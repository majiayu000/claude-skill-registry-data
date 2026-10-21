---
name: orquer-orchestrator
description: "Event-driven orchestrator instructions for coordinating subordinate agents inside Orquer. Use when acting as an orchestrator managing workers across panes. Enforces zero polling, passive waiting, task dispatching, and structured decision resolution via orquer msg."
---

# Orquer Orchestrator Protocol

As an **Orchestrator Agent** in Orquer, you supervise one or more subordinate agents working in separate dedicated workspaces.

## Cardinal Rules

1. **NO TERMINAL POLLING:** Never loop reading terminal output (`orquer pane read`) or guessing agent state every 50 seconds. The 50-second terminal watcher is deprecated and eliminated.
2. **PASSIVE EVENT-DRIVEN WAITING:** Always suspend execution on `orquer msg recv --wait`. Your process sleeps until a subordinate actively sends a notification.
3. **STRUCTURED DECISION RESOLUTION:** When a subordinate is blocked on a multiple-choice decision or question, it sends an `ask` message. You MUST answer it promptly using `orquer msg reply`.
4. **NEVER SPLIT THE ORCHESTRATOR TERMINAL:** The orchestrator workspace (🎯 Orchestrator) is a dedicated command deck. Never run `orquer pane split`. Always launch workers in their own dedicated workspace in the sidebar using `orquer workspace create --label "<name>" --no-focus`.

---

## Workflow Guide

### 1. Spawning and Assigning Work to a Subordinate

To launch a worker in a dedicated workspace (in the sidebar list, never splitting the orchestrator pane):
```bash
# 1. Create a dedicated workspace in the sidebar (never split!)
# Returns the initial pane ID of the new workspace (e.g. w2:p1)
NEW_PANE=$(orquer workspace create --label "worker-1" --no-focus | node -e "let s='';process.stdin.on('data',d=>s+=d).on('end',()=>console.log(JSON.parse(s).result?.root_pane?.pane_id||''))" 2>/dev/null || orquer workspace create --label "worker-1" --no-focus | grep -o '"pane_id":"[^"]*"' | head -1 | sed 's/.*:"//; s/"$//')

# 2. Start the worker agent in that workspace pane (or send command)
orquer pane send-text "$NEW_PANE" "my-worker-agent\n"

# 3. Dispatch the task explicitly via the message bus (from 'orchestrator')
orquer msg send --to "$NEW_PANE" --from orchestrator --type task --payload '{"goal": "Build authentication module", "spec": "OAuth2"}'
```

### 2. Waiting Passively for Updates (Zero CPU / Zero Polling)

Instead of sleeping or polling, enter passive wait for incoming messages:

```bash
# Block until any message arrives for the orchestrator
MESSAGE=$(orquer msg recv --recipient orchestrator --wait --json)
```

You can optionally set a maximum wait timeout (in milliseconds):
```bash
# Wait up to 5 minutes (300,000 ms)
MESSAGE=$(orquer msg recv --recipient orchestrator --wait --timeout-ms 300000 --json)
```

### 3. Handling Incoming Message Types

Parse the incoming JSON message:

```bash
MSG_TYPE=$(echo "$MESSAGE" | jq -r '.msg_type')
MSG_ID=$(echo "$MESSAGE" | jq -r '.id')
SENDER=$(echo "$MESSAGE" | jq -r '.from')
```

#### Case A: `ask` (Subordinate Needs a Decision)
The subordinate is blocked waiting for your input.
Inspect the question and available options:
```bash
QUESTION=$(echo "$MESSAGE" | jq -r '.payload.question')
OPTIONS=$(echo "$MESSAGE" | jq -r '.payload.options[]')
```

Evaluate the options, select the best choice, and reply:
```bash
# Reply to unblock the subordinate immediately
orquer msg reply --id "$MSG_ID" --choice "PostgreSQL"
```
Or shorthand:
```bash
orquer reply --id "$MSG_ID" --choice "PostgreSQL"
```

#### Case B: `progress` (Status Update)
The subordinate reported intermediate milestone progress. Log or review the update and resume waiting:
```bash
echo "Progress from $SENDER: $(echo "$MESSAGE" | jq -r '.payload')"
# Resume passive wait
```

#### Case C: `result` (Task Completed)
The subordinate has finished its assignment:
```bash
RESULT=$(echo "$MESSAGE" | jq -r '.payload')
echo "Task completed by $SENDER: $RESULT"
# Synthesize results or assign next task
```

#### Case D: `error` (Task Failed)
The subordinate encountered an unrecoverable failure:
```bash
ERR=$(echo "$MESSAGE" | jq -r '.payload')
echo "Task error in $SENDER: $ERR"
# Handle failure, retry, or abort
```

---

## Orchestrator Loop Pattern

```bash
while true; do
    MSG=$(orquer msg recv --recipient orchestrator --wait --json)
    if [ -z "$MSG" ] || [ "$(echo "$MSG" | jq -r '.message')" = "null" ]; then
        echo "Timeout reached or no messages."
        break
    fi

    TYPE=$(echo "$MSG" | jq -r '.msg_type')
    ID=$(echo "$MSG" | jq -r '.id')
    FROM=$(echo "$MSG" | jq -r '.from')

    case "$TYPE" in
        ask)
            Q=$(echo "$MSG" | jq -r '.payload.question')
            echo "Decision required for $FROM: $Q"
            # Decide choice...
            CHOICE="Option A"
            orquer msg reply --id "$ID" --choice "$CHOICE"
            ;;
        result)
            echo "Completed by $FROM: $(echo "$MSG" | jq '.payload')"
            break
            ;;
        error)
            echo "Error from $FROM: $(echo "$MSG" | jq '.payload')"
            break
            ;;
        progress)
            echo "Working: $(echo "$MSG" | jq '.payload')"
            ;;
    esac
done
```
