---
name: cf-status
version: 1.0.0
author: Ashay Kubal @ Qball Inc.
description: Display CLEAR session status, token usage, and context health. Use when the user asks for session status, token consumption, or context integrity checks.
user-invocable: true
allowed-tools:
  - Bash
  - Read
---

> **CLI Usage:** When unsure about a CLI's interface or flags, run it with `--help` first. Do NOT attempt to discover functionality by reading plugin source code — doing so leads to incorrect execution from assumptions made without context of the holistic flow.

# CLEAR Status

Reads CLEAR state files and displays a formatted summary of the current session, token usage, active workpackage, and context health. Provides token threshold warnings to guide session lifecycle decisions.

---

## When to Use This Skill

**Load this skill when the user request matches ANY of these patterns:**

| Trigger Pattern | Example User Request |
|-----------------|---------------------|
| Asking for session status | "Show me the current session status" |
| Checking token usage or consumption | "How much of my token budget have I used?" |
| Verifying context health or loaded state | "Is all the required context loaded?" |
| General CLEAR status inquiry | "What's the CLEAR status?" |

**DO NOT use for:**
- Initializing CLEAR in a project (use `/cf-init` instead)
- Reloading or syncing context (use `/cf-reload` instead)
- Debugging hook or plugin issues (use `/cf-debug` instead)

---

## Usage

`/cf-status` -- No arguments required. Reads state from `.clear/` in the current project.

---

## Instructions

### Step 1: Pre-flight Check

Verify CLEAR is initialized by checking for `.clear/config/clear-manifest.yaml`.

```bash
if [ -f ".clear/config/clear-manifest.yaml" ]; then
  echo "INITIALIZED"
else
  echo "NOT_INITIALIZED"
fi
```

If NOT initialized, display: "CLEAR is not initialized in this project. Run `/cf-init` to set up CLEAR." and stop.

### Step 2: Read State Files and Display Output

Read `.clear/state/session.json` for session data (`clearSessionNumber`, `sessionId`, `startTime`, `tokenUsage.*`). Read `.clear/state/sync-state.json` (optional) for active work context (`workpackage.displayId`, `workpackage.title`, `plan.activePhaseDisplayId`). Note: `PlanSummary` in sync-state has no `name` field by design — plan identity is carried by `master-plan.yaml`; the sync summary tracks active phase + progress + blockers only.

```bash
SESSION_STATE=$(cat .clear/state/session.json 2>/dev/null)
if [ -z "$SESSION_STATE" ]; then
  echo "Error: Could not read session state"
  exit 1
fi

SYNC_STATE=$(cat .clear/state/sync-state.json 2>/dev/null || echo '{}')

echo "$SESSION_STATE" | jq -r '
  "CLEAR Status",
  "============",
  "",
  "Session",
  "  Number:     \(.clearSessionNumber // "unknown")",
  "  ID:         \(.sessionId // "unknown")",
  "  Started:    \(.startTime // "unknown")",
  "  Prompts:    \(.tokenUsage.promptCount // 0)",
  "",
  "Token Usage",
  "  Tokens:     \(.tokenUsage.cacheReadTokens // 0 | tostring | gsub("(?<=[0-9])(?=([0-9]{3})+$)"; ",")) (\((.tokenUsage.estimate // 0) * 100 | floor)%)",
  "  Method:     \(.tokenUsage.method // "unknown")",
  "  Thresholds: 60% warning | 75% critical | 85% emergency"
'

echo "$SYNC_STATE" | jq -r '
  if .workpackage.displayId then
    "",
    "Active Work",
    "  Workpackage: \(.workpackage.displayId) - \(.workpackage.title // "unknown")",
    "  Phase:       \(.plan.activePhaseDisplayId // "unknown")"
  else empty end
'
```

### Step 3: Context Health Check

```bash
ISSUES=""

WP_ID=$(echo "$SYNC_STATE" | jq -r '.workpackage.systemId // empty')
if [ -n "$WP_ID" ] && [ ! -d ".clear/workpackages" ]; then
  ISSUES="${ISSUES}\n  - Workpackages directory not found"
fi

if [ ! -f ".clear/plans/master-plan.yaml" ]; then
  ISSUES="${ISSUES}\n  - master-plan.yaml not found"
fi

LINKS=$(echo "$SYNC_STATE" | jq -r '.links.workpackageKnowledge | length // 0')
if [ "$LINKS" = "0" ] && [ -n "$WP_ID" ]; then
  ISSUES="${ISSUES}\n  - No knowledge entries linked to active workpackage"
fi

if [ -z "$ISSUES" ]; then
  echo ""
  echo "Context Check: All required context successfully loaded"
else
  echo ""
  echo "Context Check: Missing items detected"
  echo -e "$ISSUES"
fi
```

### Step 4: Token Threshold Warning

Based on the token usage percentage, append one of:
- Below 60%: No additional message
- 60-75%: "Warning: Consider wrapping up current task"
- 75-85%: "Critical: Begin handoff preparation"
- Above 85%: "Emergency: Stop new work, finalize handoff immediately"

> **Threshold source-of-truth**: Defaults are 60% / 75% / 85% (warning / critical / emergency). Configurable per project via `.clear/config/session-management.yaml`. The session-monitor hook reads thresholds from `.clear/state/session.json` (`.thresholds.*`), which is initialized from the config file on session start. See `session-management` skill for the configuration schema.

---

## Completion Checklist

Before returning to the user, verify:

- [ ] Pre-flight check determined initialization status
- [ ] Session state displayed with number, ID, start time, and prompt count
- [ ] Token usage displayed with percentage and tracking method
- [ ] Context health check completed with pass/fail indicators
- [ ] Token threshold warning included if usage exceeds 60%
