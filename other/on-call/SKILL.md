---
name: on-call
description: On-call rotation setup with schedule, runbooks, and handoff notes
version: 0.1.0
execution-mode: side_effecting
argument-hint: "[--action schedule|handoff|status] [--week WEEK]"
category: governance-compliance
status: candidate
---
# On-Call

On-call rotation setup: schedule, runbook links, escalation contacts, and handoff notes. Keeps operational coverage organized and ensures smooth transitions between on-call shifts.

## When to Use
- Setting up or reviewing the on-call rotation
- Handing off on-call responsibility to the next person
- Checking who is currently on-call and their contact info
- Starting an on-call shift and need context on active issues

## Execution
### 0. Emit SKILL_INVOKE
Post SKILL_INVOKE to the bus before any stateful action.
```
Type: SKILL_INVOKE
To: all
Message: [skill=on-call] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

1. Parse `$ARGUMENTS` for `--action` (default: `status`) and `--week` (default: current week)
2. If `--action status`:
   a. Show current on-call person and their contact channels
   b. List active incidents or open alerts
   c. Show time remaining in current rotation
   d. Link to relevant runbooks
3. If `--action schedule`:
   a. Display the rotation for `--week` (or generate a new rotation)
   b. Show coverage gaps if any
   c. List holidays or PTO conflicts
4. If `--action handoff`:
   a. Summarize active issues from the outgoing shift
   b. List any alerts that fired and their resolution status
   c. Note ongoing investigations or watch items
   d. Record handoff timestamp and participants
   e. Write handoff notes to `_state/ops/handoffs/`
5. Link to escalation policy for reference

## Output Format
```
On-Call | action: {action} | week: {week}

Current On-Call: {name} ({channels})
Rotation Ends: {datetime}

Active Issues:
- {issue}: {status} (since {time})

Runbooks:
- {service}: {link}

{Handoff notes if --action handoff}

Next action: {recommendation}
```

## Skill Chains

### Mandatory

None — config management for schedule setup; no external state mutation.

### Advisory

- Active incident found → `[incident]` for incident management
- Need health check first → `[health]` for system status
- Setting up escalation → `[escalation-policy]` to define chains

## Authority

- **T1 (TRUSTED)**: May run
- **T2 (Active/High)**: May run
- **T3 (Medium)**: Operator approval (affects operations)
- **T4 (Probationary)**: May run read-only (view schedule; modify BLOCKED)
- **Operator**: Override any restriction
