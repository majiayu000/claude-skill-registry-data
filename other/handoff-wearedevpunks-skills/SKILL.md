---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
---

# Handoff

Write a compact handoff in the operating system's temporary directory, outside
the workspace. Tailor its next action to the user's requested receiving task.

For delivery work, follow the authoritative
[Delivery Handoff contract](../../../phases/delivery-phase/references/phase-handoff.md#phase-exit-and-delivery-handoff).
Resolve goal, bounds, Git identity and stable Context Pointers from durable
artifacts; retain exact blockers and explicit unknowns. The receiving task always
cold-routes from current authorities. The disposable Delivery Context Packet is
never persisted. This contract is separate from the scaffold CLI Post-Command
Handoff.

For other work, retain the next action, relevant durable artifact paths or URLs,
exact blocker and unknowns. Reference existing plans, issues, commits and diffs;
keep their bodies in their owning artifacts. Include only trigger-relevant
suggested skill pointers, and redact secrets and personal data.

Completion: the saved document names a provable next action or exact missing
proof, every required pointer has a stable identity and freshness rule, and the
receiving agent can distinguish completed mutations from remaining work. Return
the absolute handoff path and a concise continuation prompt.
