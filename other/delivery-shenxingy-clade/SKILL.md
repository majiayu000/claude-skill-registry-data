---
name: delivery
description: Adaptive, resumable Git delivery across repositories and agent runtimes — probe policy, checkpoint coherent work, publish, review, integrate, and verify cleanup
when_to_use: "start coding branch, manage delivery lifecycle, checkpoint work, prepare/publish/update PR, choose merge strategy, finish and clean a coding task"
argument-hint: 'start|authorize|context|list|checkpoint|candidate|evidence|publish|ready|merge|reconcile|abandon|clean [options]'
user_invocable: true
---

# Delivery

Clade's provider-neutral Git delivery control plane. It adapts to the target
repository, forge, event, branch ownership, worktree, and runtime before
changing state. It preserves useful work promptly without treating a commit as
permission to push, open a PR, merge, or delete a branch.

## Invariants

- Probe before acting; `unknown` never means allowed.
- One session owns one mutable branch/worktree.
- A coherent slice ends in a commit, detached reachable ref/snapshot, patch, or
  explicit blocker—not an undocumented dirty tree.
- Checkpoint verification is focused; candidate verification is complete and
  bound to the exact head SHA.
- PR creation is idempotent, merge is an explicit integrator action, and
  cleanup is verified.
- Repository policy and explicit user authority outrank Clade defaults.
- Authority granted after START is recorded through the audited `authorize`
  transition; never edit delivery state directly.
- When an orchestrator attempt exists, START records its `--attempt-id` and
  `evidence` emits the stable secret-free delivery projection for the bundle.

The executable workflow and state schema live in `prompt.md` and
`scripts/delivery.py`. Runtime-specific mechanics live under `surfaces/`.
