---
name: nexus-gatekeeper
description: "Use after implementation to block a task from advancing until a reality check passes. Spawns a reality-check agent (/qa-only, /doubt-driven-development), records PASS or NEEDS_WORK/FAIL in task-store.db, halts the pipeline on failure, and escalates repeated failures to the PD or council."
---

# nexus-gatekeeper

description: "Formalizes Reality Checker as a hard blocking gate in the task pipeline — a task cannot advance past implementation until the gate is cleared. After implementation, spawns the Reality Checker agent and parses its verdict: PASS sets gate_status=passed (downstream agents spawn), NEEDS_WORK or FAIL sets gate_status=failed and halts the pipeline. Writes gate records to task-store.db. In FAIL scenarios with consecutive failures, escalates to the PD or council. Best for teams that want enforcement-grade quality gates without relying on discipline — the gatekeeper makes the workflow self-governing. Also for: tracking recurring quality concerns across tasks and surfacing architectural issues from repeated gate failures."

## Protocol

1. **After implementation:** Spawn a reality-check agent (general-purpose + /qa-only, /doubt-driven-development; role file: agents-archive/generalist-2026-10-06/testing/testing-reality-checker.md) to assess
2. **Parse verdict:**
   - `PASS` → set `gate_status=passed`
   - `NEEDS_WORK` → set `gate_status=failed`, halt pipeline
   - `FAIL` → set `gate_status=failed`, halt pipeline, escalate
3. **Write gate record** to task store via `task-store` skill
4. **Halt on failed gate:** Do not spawn downstream agents until gate is cleared

## Reality-Check Verdict Reference

- `PASS` — ready to ship, no blocking issues
- `NEEDS_WORK` — significant issues remain, must address before proceeding
- `FAIL` — critical failure, do not continue

## Workflow

```
Implementation Agent
    │
    ▼
Reality-check agent (general-purpose + /qa-only)
    │
    ├─ PASS → ts-gate passed → spawn downstream agents
    │
    ├─ NEEDS_WORK → ts-gate failed → HALT
    │                    Report to user for remediation
    │
    └─ FAIL → ts-gate failed → HALT
                     Escalate to PD/council
```

## Integration with task-store

The gatekeeper reads from and writes to `~/.claude/task-store.db`:

```bash
# Check gate before spawning
gate=$(sqlite3 ~/.claude/task-store.db \
  "SELECT gate_status FROM tasks WHERE id='$task_id';")
if [ "$gate" = "open" ]; then
  echo "Gate not yet evaluated — run the reality check first"
elif [ "$gate" = "failed" ]; then
  echo "BLOCKED — gate failed, see gate_verifier and notes"
else
  echo "Gate passed — safe to advance"
fi
```

## Escalation Path

- Gate `failed` with `NEEDS_WORK`: Report to user with specific issues found
- Gate `failed` with `FAIL`: Escalate to PD or council if multiple consecutive failures
- Gate repeatedly `failed` for the same task: Add to project oversight as recurring quality concern
