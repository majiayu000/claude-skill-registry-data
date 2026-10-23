---
name: portfolio-ledger
description: Read positions, exposure, and P&L from the append-only ledger with restart reconciliation and JSONL export, owned by JOURNAL with RISK reading.
bots:
  - bot-09-journal
  - bot-02-risk
gates:
  - G-2
required_tools:
  - portfolio.ledger_read
  - portfolio.exposure
  - portfolio.pnl
required_data: []
permissions:
  max_side_effect: read
  network: true
  filesystem: var
fixtures:
  - tests/fixtures/replay/smoke
---

# Portfolio Ledger

## L1 - Summary

The ledger is the desk's memory: every event appended once, hash-chained, never edited. JOURNAL owns reads for reports and reconciliation; RISK reads exposure and P&L for limit decisions. After any restart, reconcile from the chain before trusting a single number.

```
append-only events -> hash chain verifies -> exposure and P&L read -> reports and limits
restart -> reconcile from chain -> then read
```

## L2 - Method

1. S1 - Read through the tools: use `portfolio.ledger_read` for event history, `portfolio.exposure` for current exposure, and `portfolio.pnl` for realised and unrealised P&L. Never read the sqlite file directly when a tool exists.
2. S2 - Reconcile after restart: verify the hash chain (`seq` without gaps, every `prev_hash` matching) before serving numbers. A chain that does not verify stops reads until repaired from the last good snapshot.
3. S3 - Speak event types: the ledger carries the snake_case event kinds (order, fill, halt, kill, approval, journal_note, escalation). Filter by kind and ticket; never invent a kind.
4. S4 - Export as JSONL: snapshots and exports go to versioned JSONL views for reports and audits. Exports are derived views; the chain stays the single truth.
5. S5 - Separate writing from reading: seats write ledger events only through `journal.append` and `desk.event_emit` with kinds `journal_note` or `escalation`. Every other event type is appended by library code only.

## Failure modes

| Symptom | Cause | Action |
|---|---|---|
| Chain gap or hash mismatch | Crash mid-append or file tampering | Stop reads; reconcile from the last good snapshot; report to RISK |
| Direct sqlite reads in code | Bypassed tooling | Route through the portfolio tools; direct reads skip freshness and audit |
| Invented event kind | Typo or new-kind wish | Use the enumerated kinds; new kinds arrive via reviewed schema change |
| Seat writing non-journal events | Authority confusion | Refuse; only the adapter, engine, supervisor, or CLI append those kinds |

## References

- Tools: `portfolio.ledger_read`, `portfolio.exposure`, `portfolio.pnl` (ledger reads)
- Event vocabulary: ledger event kinds (`journal_note`, `escalation`, order and fill rows)
- Gate G-2: ledger rows back every receipted claim
- Companion skills: `desk-folders-and-journal` (layout plus append-only rule), `daily-report` (report rendering)
