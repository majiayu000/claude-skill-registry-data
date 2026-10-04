---
name: patpat-plan
description: Design a falsifiable workflow for multi-phase repository work or a task with no safe narrow route. Use when several contracts or verification surfaces must be sequenced; remain read-only.
---

# Patpat Plan

When invoked directly, read the [operating protocol](../patpat-loop/references/operating-protocol.md) in full. Do not load the router.

Read [repository truth](../patpat-loop/principles/repository-truth.md), [sequence verifiable units](../patpat-loop/principles/sequence-verifiable-units.md), and apply the [bespoke workflow playbook](../patpat-loop/playbooks/bespoke-workflow.md).

Inspect enough repository evidence to name the contracts, dependencies, risks, and authoritative surfaces. Define one falsifiable completion predicate. Split work only at boundaries that can independently return to a verified state.

Remain read-only. Produce phases with verification and rollback hooks, unresolved facts, authority gates, and the smallest safe first unit. Hand implementation to the matching focused workflow or `patpat-run`; do not implement inside this skill.

## Mutation boundary

Remain read-only with respect to repository implementation and external delivery. Limit incidental verifier artifacts to the declared proof contract, clean them up, and hand any authorized mutation back to `patpat-loop`.
