---
name: patpat-arena
description: Run isolated competing attempts at the same brief, pick a base, graft the strongest parts, and verify the synthesis. Use for /patpat-arena, competing designs, or when one attempt would lock the wrong shape.
disable-model-invocation: true
---

# Patpat Arena

When invoked directly, read the [operating protocol](../patpat-loop/references/operating-protocol.md) and [execution graph](../patpat-loop/references/execution-graph.md) in full. Do not load the router.

Read [earned parallelism](../patpat-loop/principles/earned-parallelism.md) and apply the [arena playbook](../patpat-loop/playbooks/arena.md).

Fan out writable attempts only after each worker has a separate Git worktree or host-enforced sandbox with its own Git index and process boundary. Disjoint files or directories in one worktree are not isolation. If isolation is unavailable, run one serial attempt and say so. Inherit the parent model unless the user named models.

Challenge each surviving candidate with the [arena playbook](../patpat-loop/playbooks/arena.md) before selection. Use a separate reviewer only when available, authorized, and within the earned worker budget; otherwise the parent performs the adversarial pass and reports that it was not independently attested. The parent owns pick, graft, verification, and any authorized delivery. Worker output is a candidate, not a completed change.

## Proof closure

Close repository mutations through:

- [`patpat-verify`](../patpat-verify/SKILL.md)
- [`patpat-review`](../patpat-review/SKILL.md)
