---
name: apply
description: Execute one approved feature or an ordered feature queue through implementation, verification, recovery, and truthful closeout while preserving repository ownership and harness-native execution choices.
---

# Apply

Use this skill after proposal authoring has produced approved, executable work. It defines portable
lifecycle outcomes and safety invariants; the active harness remains responsible for its own tools,
workers, state, scheduling, and command surface.

## Select the mode

- For a single feature, read [references/single.md](references/single.md).
- For multiple features, read [references/queue.md](references/queue.md) and
  [references/dependency-and-concurrency.md](references/dependency-and-concurrency.md).

Load the remaining references when their concern becomes active:

- [references/work-decomposition-and-accountability.md](references/work-decomposition-and-accountability.md)
  for capability assignment, ownership, and safe parallel work.
- [references/recovery.md](references/recovery.md) after interruption or uncertain prior progress.
- [references/workflow-lease.md](references/workflow-lease.md) when mutable resources need
  coordinated ownership across sessions or harnesses.
- [references/completion.md](references/completion.md) before any terminal outcome or completion
  claim.

## Universal invariants

1. Resolve authoritative proposal and issue state before editing.
2. Honor explicit dependencies and isolate every mutable-resource conflict.
3. Give each bounded task one accountable owner and an exact verification recipe.
4. Reconstruct interrupted work from durable evidence, never conversation memory alone.
5. Require fresh verification, issue-state updates, archive, and persistence when the repository's
   completion contract requires them.
6. Preserve harness choice: specialist, generalist, direct, serial, and safely parallel execution
   can all conform when they produce the same lifecycle outcomes.
