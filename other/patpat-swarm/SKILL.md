---
name: patpat-swarm
description: Fan out isolated workers across slices or races and return one aggregated report. Use for /patpat-swarm, coverage matrices, parallel checks, or races with a declared selection rule.
disable-model-invocation: true
---

# Patpat Swarm

When invoked directly, read the [operating protocol](../patpat-loop/references/operating-protocol.md) and [execution graph](../patpat-loop/references/execution-graph.md) in full. Do not load the router.

Read [earned parallelism](../patpat-loop/principles/earned-parallelism.md) and apply the [swarm playbook](../patpat-loop/playbooks/swarm.md).

Read-only coverage may run in parallel. Every writable worker needs a separate Git worktree or host-enforced sandbox plus all earned-parallelism gates. Disjoint paths in one worktree are not isolation. If those gates fail, run serially and name missing lanes. Inherit the parent model unless the user named models. Do not invent coverage for a silent worker. The parent verifies the integrated result.

## Proof closure

Close repository mutations through:

- [`patpat-verify`](../patpat-verify/SKILL.md)
- [`patpat-review`](../patpat-review/SKILL.md)
