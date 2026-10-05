---
name: desk-post-trade-review
description: Append-only journaling and structured review of every completed ticket. Separates process grade from outcome grade.
---

# Desk Post-Trade Review

## Journal Entry Schema
```
TICKET: SOL-YYYYMMDD-NNN
Mint: ...
Entry / Exit Time: ...
Size: ...
Realised P&L: ...
Process Grade: A / B / C / F
Outcome Grade: Win / Scratch / Loss
What Went Well: ...
What Broke: ...
Action Items: ...
```

## Rules
- Append only — never delete or overwrite
- Process grade is independent of outcome
