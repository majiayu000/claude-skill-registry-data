---
name: kill-switch
description: Halt the desk through risk.kill_switch set or flatten_request, read state through risk.halt_status, and clear only through the human CLI path.
bots:
  - bot-02-risk
  - bot-00-chief
gates:
  - G-2
  - G-6
required_tools:
  - risk.halt_status
required_data: []
permissions:
  max_side_effect: read
  network: true
  filesystem: none
fixtures:
  - tests/fixtures/replay/smoke
---

# Kill Switch

## L1 - Summary

The kill switch halts the desk. RISK sets it with the `risk.kill_switch` tool (`set` or `flatten_request` only); CHIEF watches it with `risk.halt_status`. The switch can be set from the environment at start, from the `var/KILLSWITCH` file, or from an alert-channel command polled every cycle. Clearing is CLI-only with a human-signed record; no skill and no seat clears the switch.

```
threat seen -> RISK set (or file/env/alert trips it) -> halt: no new tickets
flatten_request -> in-flight orders settle, open positions close with reason
clear -> pumpgrok killswitch clear --by <human> --reason <text> only
```

## L2 - Method

1. S1 - Read the state first: call `risk.halt_status` to learn whether the desk is halted and which source tripped it (tool action, file, environment, or alert channel). CHIEF polls this every cycle.
2. S2 - Set on danger: RISK calls `risk.kill_switch` with `action=set` on a confirmed threat (suspected rug in inventory, daily-loss breach, integrity failure). The action enum accepts only `set` and `flatten_request`; `clear` is a validation error.
3. S3 - Flatten when exposed: with open positions, RISK uses `action=flatten_request` so the supervisor waits on the adapter barrier and closes every position with the kill reason instead of abandoning it.
4. S4 - Honor every source: a `var/KILLSWITCH` file present at start, the environment flag, or an alert-channel command all halt before the first ticket. Removing the file does not clear a tool-set switch.
5. S5 - Clear human-only: `pumpgrok killswitch clear --by <human> --reason <text>` with an approval record. Seats never clear; CHIEF requests, the human clears.

## Failure modes

| Symptom | Cause | Action |
|---|---|---|
| Switch set but tickets continue | A seat bypassing the halt read | Halt the run; every ticket path reads halt status first |
| Clear attempted by a seat | Misunderstood authority | Refuse; only the human CLI path with a signed reason clears |
| Order stuck ACCEPTED at halt | In-flight order during the trip | Reject at CONFIRMING with reason kill_switch; never fill into a halt |
| Positions left open after flatten | Barrier or adapter failure | Escalate to RISK; keep polling until every position reports closed |

## References

- Tools: `risk.kill_switch` (RISK-only grant; `set` plus `flatten_request`), `risk.halt_status` (every halted-seat read)
- CLI: `pumpgrok killswitch clear --by <human> --reason <text>` (sole clear path)
- Companion skills: `live-gate-procedure` (preconditions), `desk-incident-response` (halt playbooks)
