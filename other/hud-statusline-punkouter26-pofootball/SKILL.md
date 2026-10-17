---
name: hud-statusline
description: "Configures Claude Code's statusline to display Unity workflow state — current phase, active agent, files modified, and session duration."
alwaysApply: false
---

# HUD / Statusline Integration

Guidance for commands and agents to update Claude Code's statusline with real-time Unity workflow state.

## Statusline Format

The recommended statusline format for Unity workflows:

```
[Phase: Execute] [Agent: unity-coder] [Modified: 5 files] [12m]
```

Fields:
- **Phase** — current workflow phase: Clarify, Plan, Execute, Verify, Done
- **Agent** — currently active sub-agent (or "main" if no agent is running)
- **Modified** — count of unique files edited this session (from session-edits.txt)
- **Duration** — elapsed session time in minutes

## Reading Session State

Statusline data comes from the hook state directory at `/tmp/unity-claude-hooks/`:

| File | Content | Updated By |
|------|---------|-----------|
| `session-edits.txt` | One file path per line (may have duplicates) | `track-edits.sh` |
| `gateguard-reads.txt` | One file path per line | `track-reads.sh` |
| `session-state.json` | Branch, phase, workflow context | `session-save.sh` |
| `session-start-time` | Unix timestamp | `session-restore.sh` |
| `session-cost.jsonl` | One JSON object per tool call | `cost-tracker.sh` |

### File Count

```bash
EDIT_COUNT=0
if [ -f "/tmp/unity-claude-hooks/session-edits.txt" ]; then
    EDIT_COUNT=$(sort -u "/tmp/unity-claude-hooks/session-edits.txt" | wc -l | tr -d ' ')
fi
```

### Session Duration

```bash
DURATION_MINS=0
if [ -f "/tmp/unity-claude-hooks/session-start-time" ]; then
    START=$(cat "/tmp/unity-claude-hooks/session-start-time")
    NOW=$(date +%s)
    DURATION_MINS=$(( (NOW - START) / 60 ))
fi
```

## Integration Points

### Commands

Commands with phase gates (like `/unity-workflow`) should update the statusline at each transition:

```
Phase 1: Clarify  → statusline: [Phase: Clarify]
Phase 2: Plan     → statusline: [Phase: Plan]
Phase 3: Execute  → statusline: [Phase: Execute] [Agent: unity-coder]
Phase 4: Verify   → statusline: [Phase: Verify] [Agent: unity-verifier]
Done              → statusline: [Phase: Done] [Modified: N files] [Xm]
```

### Agents

When a command spawns a sub-agent, the statusline should reflect which agent is active. The agent field updates when:
- A new Agent tool call is made
- The agent completes and returns control to the command

### Ralph Mode

During `/unity-ralph`, the statusline should show iteration progress:

```
[Ralph: 3/10] [Agent: unity-verifier] [Fixed: 5] [12m]
```

### Team Mode

During `/unity-team`, the statusline should show parallel agent status:

```
[Team: build] [Agents: 3 running] [Modified: 8 files] [5m]
```

## Cost Tracking Display

If the cost tracker is active (strict profile), the statusline can optionally show token usage:

```
[Phase: Execute] [Modified: 5 files] [12m] [Calls: 47]
```

Read from `session-cost.jsonl`:

```bash
CALL_COUNT=0
if [ -f "/tmp/unity-claude-hooks/session-cost.jsonl" ]; then
    CALL_COUNT=$(wc -l < "/tmp/unity-claude-hooks/session-cost.jsonl" | tr -d ' ')
fi
```
