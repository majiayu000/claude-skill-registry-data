---
name: patpat-change
description: Implement one bounded repository change with a small diff and explicit proof. Use for clear features, localized refactors, and requested fixes after the root cause or design is known.
---

# Patpat Change

For clear, bounded, reversible local work without delivery intent, use this skill and its relevant references. Otherwise read the [operating protocol](../patpat-loop/references/operating-protocol.md) and [execution graph](../patpat-loop/references/execution-graph.md) in full before acting. Escalate on uncertainty, security, auth, billing, secrets, architecture, cross-cutting work, or delivery intent. Do not load the router or reread unchanged instructions already loaded in this session.

Read [smallest safe change](../patpat-loop/principles/smallest-safe-change.md), [preserve safety](../patpat-loop/principles/preserve-safety.md), and [proof over proxy](../patpat-loop/principles/proof-over-proxy.md). Apply the [bounded change playbook](../patpat-loop/playbooks/bounded-change.md).

For a behavior-preserving rename, move, extraction, inline, or deduplication, apply the [behavior-preserving refactor playbook](../patpat-loop/playbooks/behavior-preserving-refactor.md). When the user requests test-first work or a cheap deterministic regression target exists, apply [regression first](../patpat-loop/playbooks/regression-first.md).

When regression-first applies, observe fail-before (or an explicit why-not) and report fail-before and pass-after on the same check; do not silently skip.

For an explicit visual migration or pixel-equivalence claim, apply the [visual equivalence playbook](../patpat-loop/playbooks/visual-equivalence.md) without weakening its baseline or comparison harness.

Inspect version-control state and nearby contracts before editing. Define Claim, Surface, Action, Expect, and Cleanup. Make one coherent repository-native patch. Avoid unrelated cleanup, speculative abstractions, new dependencies, and public interface changes unless the objective requires them.

Do not claim completion from generation, compilation, or tests alone when the changed behavior has an observable surface.

## Proof closure

Define the five-field proof contract before any mutation. Close mutating work with:

- Always: [`patpat-verify`](../patpat-verify/SKILL.md), using authoritative evidence.
- When required: [`patpat-review`](../patpat-review/SKILL.md) for delivery intent, auth/security/billing/secrets, architecture or cross-cutting scope, durable-run completion, land/merge, or another operating-protocol review gate.

For clear, bounded, reversible local work with none of those review requirements, proceed from verification to REPORT without independent review.
