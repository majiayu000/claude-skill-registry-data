---
name: context-pressure
description: "Use when context passes ~60%, a context-percentage alert arrives, or a compaction/respawn decision is needed. PDs above 75%: finish the current task then /save-state. On-demand; moved out of CLAUDE.md."
---
# Context pressure

The harness auto-summarizes long context; no manual /compact nudging. In a PD session above 75%: complete the current task, then `/save-state`; at 80%: `/respawn-self` (Coords: `/coord-respawn-self`). Retention policy and rollback threshold: `{agency-root}/runbooks/context-pressure-management.md`; respawn rules: `{agency-root}/runbooks/respawn-contract.md`.
