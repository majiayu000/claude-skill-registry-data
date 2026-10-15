---
name: ops
description: Operations surge mode — health-first, diagnose-then-fix, bus-visible at every state change. For incidents, fleet ops, and infrastructure recovery.
version: 1.0.0
execution-mode: side_effecting
argument-hint: "<system, incident, or ops task>"
category: governance-compliance
status: tested
providers:
  required: [bash, python]
---
# Ops Mode Activation

### 0. Emit SKILL_INVOKE
Post SKILL_INVOKE to the bus before any stateful action.
```
Type: SKILL_INVOKE
To: all
Message: [skill=ops] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

**Debounce rule**: post SKILL_INVOKE exactly once per skill invocation. If the
bus post fails (rate limit, network error), wait 6 seconds and retry — do not
retry in a tight loop. If a SKILL_INVOKE was already posted successfully within
the last 30 seconds for the same skill+session, skip the duplicate post. The
bus bridge enforces a 5-second minimum interval between posts from the same
client; rapid retries create noise and hit rate limits. (Origin: 2026-09-04 —
ops mode posted 4 SKILL_INVOKE messages in 18 seconds due to retry storm.)

### 0a. Admit explicit chains

When `/ops` is part of an explicit multi-skill route, follow
`rules/skill-chain-admission.md`. Gather the mandatory health and bus evidence,
then run `scripts/skill-chain-gate.py check` before the first fix or other
non-receipt side effect. `DENY` or `ERROR` is a hard stop.

You are operating in **OPS MODE** — maximum operational velocity with mandatory bus visibility and reversibility gates.

## Active Configuration
- **Tempo**: SURGE (ops problems don't wait; diagnose and act)
- **Autonomy**: Maximum — read, diagnose, fix, verify in one pass
- **Pipeline**: Health → Diagnose → Fix → Verify → Report

## Task
$ARGUMENTS

## Ops Pipeline

1. **Health sweep** — `[health]` + `[fleet-status]`; establish baseline before touching anything
2. **Diagnose** — `[log-tail]`, `[disk-check]`, `[circuit-status]`, `[process-check]` as needed
3. **Fix** — targeted, reversible action; post to bus BEFORE and AFTER each change
4. **Verify** — confirm fix worked; `[health]` again to close the loop
5. **Report** — `[incident]` if this was a real incident; `[sitrep]` to bus; update runbook if pattern is new

## Quick-Access Skills
- **Health**: `[health]`, `[fleet-status]`, `[machine-health]`, `[disk-check]`, `[uptime-check]`
- **Diagnose**: `[log-tail]`, `[log-analyze]`, `[circuit-status]`, `[process-check]`, `[port-map]`
- **Fix**: `[rollback]`, `[incident]`, `[kill-switch]`, `[launchd]`, `[docker-manage]`
- **Network**: `[tailscale-status]`, `[tunnel-check]`, `[ssl-check]`, `[dns-check]`
- **Report**: `[sitrep]`, `[alert-rule]`, `[status-page]`, `[runbook-write]`

## Rules
- **Read before write** — never modify state without reading current state first
- **Bus at every state change** — post STATUS before AND after any destructive operation
- **Verify before rollback** — confirm the issue is real; don't rollback speculatively
- **Reversibility gate** — for any destructive action (rm, reset --hard, DROP TABLE), stop and confirm unless explicitly pre-authorized
- **No force-push** to any branch under any circumstances
- **Incident-first** — if users are affected, open `[incident]` before fixing
- No Ollama on MBP

## Output Contract
End every session with:
1. Initial health state (what was broken)
2. Root cause (confirmed or suspected)
3. Fix applied (command / file / config changed)
4. Post-fix health state (confirmed working)
5. Runbook update needed? (yes/no)
6. Bus STATUS posted

Begin ops now.

## Skill Chains

### Mandatory (MUST pass before any fix)

- **`[health]`** MUST run first — establish baseline before touching anything
- **`[bus]`** MUST post STATUS before AND after any destructive operation (already in rules)

### Advisory

- **Diagnose**: `[log-tail]`, `[disk-check]`, `[circuit-status]`, `[process-check]`
- **Fix**: `[rollback]` (with `[deploy-health]` confirming), `[kill-switch]`, `[launchd]`, `[docker-manage]`
- **Verify**: `[health]` again to close the loop
- **Report**: `[incident]`, `[sitrep]`, `[runbook-write]`

## Authority

- **T1 (TRUSTED)**: May run ops with `[health]` baseline established
- **T2 (Active/High)**: May run ops with `[health]` baseline established
- **T3 (Medium)**: MUST get operator approval for destructive actions; may diagnose freely
- **T4 (Probationary)**: BLOCKED — cannot invoke this skill (incident response authority)
- **Operator**: Override any restriction — emergency ops allowed without pre-chain
