---
name: agy-conductor
description: Connect Antigravity (Agy) to Limen's symmetric peer-conductor protocol. Use when Agy must conduct, execute, review, split, observe, or harvest bounded Limen work through the authenticated conduct CLI or MCP surface.
---

# Agy Conduct Adapter

Follow `AGENTS.md` → **Peer Conductor Contract**. Conductor is a temporary capability, never a
rank. Preserve `agent: agy`; do not claim a master role, impersonate the initiator, or write the
`tasks.yaml` projection.

1. Run `./scripts/agy-clock.py`, then call `limen conduct capabilities` (or
   `conduct_capabilities`). Fail closed for new work when either live budget or broker access is
   unavailable.
2. Register the real Agy session with `limen conduct register --agent agy ...` or
   `conduct_register`. Include native run identity, capabilities, worktree, and protection status.
3. Submit a validated `WorkPacketV1` with `limen conduct submit --packet <file>`, or accept one
   assigned by the broker. Mutate only after its lease covers the repo, exact head, branch, path,
   worktree, and Agy scratch resource required by the work.
4. Before invoking an Antigravity subagent or other separate capacity, reserve a bounded child with
   `limen conduct split <parent-run> --packet <file>` or `conduct_split`. Hidden fanout is rejected,
   and every child must attenuate parent authority, scope, spend, deadline, retry, depth, and
   fanout.
5. Heartbeat the lease during work. Preserve scratch deltas, recheck remote heads before push, run
   the packet predicate, and report a schema-valid `RunReceiptV1` through `limen conduct report` or
   `conduct_report`.
6. Harvest child receipts with `limen conduct harvest`. Adopt only after the broker proves conductor
   absence. Never steal, cancel, signal, stash, reset, retune, or reap a protected human session.
