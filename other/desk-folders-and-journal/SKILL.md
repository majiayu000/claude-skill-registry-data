---
name: desk-folders-and-journal
description: Standard directory layout and append-only journal conventions for PumpGrok. Ensures every Bot writes to the same predictable locations.
---

# Desk Folders and Journal

## Standard Layout
```
/workspace/trading-desk/
  ├── proposals/
  ├── briefs/
  ├── leads/
  ├── research/
  ├── journal/
  ├── incidents/
  ├── positions/
  ├── watch/
  ├── risk-limits.md
  └── desk.md
```

## Journal Rules
- Append only — never delete or overwrite
- Every entry must contain the ticket ID and UTC timestamp
- desk.md must always contain engagement level, wallet address (once connected), and daily loss limit
