---
name: live-gate-procedure
description: The documented separate procedure for the nine live preconditions; nothing in it flips a flag and paper confirmation never counts as live proof.
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

# Live Gate Procedure

## L1 - Summary

Going live requires nine preconditions, checked by a separate procedure owned by RISK with CHIEF witnessing. Nothing in this skill flips a flag, moves funds, or signs anything: it only reads `risk.halt_status` and the precondition evidence. `pumpgrok live confirm` is operator-only and stays refused until every precondition reports met.

```
precondition evidence collected -> RISK checks nine ids -> any unmet -> refused, stay paper
all nine met                   -> operator-only confirm path (outside this skill)
```

## L2 - Method

1. S1 - Read the gate state: call `risk.halt_status` to confirm whether the desk is halted and why. A halted desk cannot begin the live procedure at all.
2. S2 - Walk the nine preconditions in order: minimum paper days, performance thresholds on paper-only ledgers, replay ledgers excluded from metrics, no live implementation shipped, and the remaining gate ids. Each reports met or unmet with its evidence pointer.
3. S3 - Reject replay ledgers for metrics: any ledger whose events carry `source=replay` is refused for the paper-days and performance preconditions. Only `source=paper` rows count.
4. S4 - Record the verdict: RISK appends the check outcome as a journaled verdict with per-precondition status. An unmet precondition names its remediation, never a waiver.
5. S5 - Hand to the operator: only when all nine read met does RISK report readiness to the human operator. The confirm action itself is outside every skill and every seat.

## Failure modes

| Symptom | Cause | Action |
|---|---|---|
| Paper metrics include replay rows | Ledger path or source tag misconfiguration | Refuse; fix the source tagging; re-check |
| Precondition unmet | Insufficient paper history or a failed threshold | Report the remediation; stay in paper; never waive |
| Halt active | Kill switch set or daily-loss breaker tripped | Clear only through the CLI path with a human-signed record |
| Pressure to skip the procedure | Urgency around a market move | The procedure is the trade; skipping it is a safety incident |

## References

- Tool: `risk.halt_status` (halt state read)
- Gates: G-2 (approvals), G-6 (single-send discipline carries into any live future)
- Companion skills: `kill-switch` (halt mechanics), `desk-incident-response` (halt playbooks)
