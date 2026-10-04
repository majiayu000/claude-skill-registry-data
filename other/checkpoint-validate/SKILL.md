---
name: checkpoint-validate
description: Validate agent checkpoint.json. Detect idle, fake completion, error recovery. Matches "checkpoint", "idle", "agent status"
user-invocable: true
argument-hint: <checkpoint-json-path>
allowed-tools: [Read, Bash, Glob]
---

# Checkpoint Validation

## CRITICAL RULES (NEVER VIOLATE)
1. **"Artifact exists" ≠ "completed"** — ONLY trust checkpoint.status == "completed"
2. **Never run 2 agents of the same role simultaneously** — confirm prior agent terminated before respawn

Validates agent checkpoint.json to detect idle/fake completion/error states.

## Input
- `$ARGUMENTS`: path to checkpoint.json

## Procedure

### Step 1: Read checkpoint.json
```
Read $ARGUMENTS
```

### Step 2: Status Determination

| checkpoint.status | Verdict | Action |
|-------------------|---------|--------|
| `"completed"` | Verify all expected_artifacts exist | All present → **PASS** / Missing → **FAKE COMPLETION** |
| `"in_progress"` | Check timestamp | Last update > 5min ago → **FAKE IDLE** / Recent → **WORKING** |
| `"error"` | Analyze error field | **ERROR** + output recovery suggestion |
| File missing | Agent never started | **NOT STARTED** — respawn immediately |

### Step 3: Artifact Verification (when completed)
```bash
# Check each expected_artifact exists and is non-empty
for f in <expected_artifacts>; do
  if [ ! -f "$f" ] || [ ! -s "$f" ]; then
    echo "FAKE: $f missing or empty"
  fi
done
```
- 0-byte file = fake artifact → **FAKE COMPLETION**

### Step 4: Output
```
[CHECKPOINT] Path: <path>
[CHECKPOINT] Agent: <agent_name>
[CHECKPOINT] Status: <status>
[CHECKPOINT] Phase: <phase>/<phase_name>
[CHECKPOINT] Completed: <completed_list>
[CHECKPOINT] In Progress: <in_progress>
[CHECKPOINT] Artifacts: <produced> / <expected>
[CHECKPOINT] Result: PASS / FAKE IDLE / FAKE COMPLETION / ERROR / NOT STARTED
[CHECKPOINT] Recovery: <specific recovery suggestion>
```

### Step 5: Recovery Actions

| State | Recovery |
|-------|----------|
| FAKE IDLE | Send "read checkpoint.json and continue" message once → still idle → respawn |
| FAKE COMPLETION | Respawn with missing artifact list (checkpoint injection) |
| ERROR | Resolve error cause, then respawn (env issues = Orchestrator fixes) |
| NOT STARTED | Spawn new agent immediately |

> **REMINDER**: Never trust "artifact exists = done". Only checkpoint.status == "completed" is truth.

## Gotchas
- A 0-byte checkpoint.json that exists is still a fake completion — always verify `status` field value
- "artifact file exists" does NOT mean completed — only trust `status=="completed"` in checkpoint
- Agents may write checkpoint with `in_progress` then crash — check timestamp staleness (>10min = likely dead)
