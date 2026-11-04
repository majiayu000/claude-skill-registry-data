---
name: state-machine-audit
description: Find and explain implicit state machines in an app or system. Use for “find all the implicit state machines,” lifecycle/state audits, interacting status flags, invalid state combinations, and hidden ordering or recovery rules. Not for automatically introducing a state-machine framework or merely drawing a known workflow.
license: MIT
---

# State Machine Audit

Discover the machines the system already implements but has not named. Start with code and observable behavior, not an idealized architecture. This is an audit unless implementation is requested.

## Find the machines

Inspect the relevant entrypoints, persistence, callers, tests, and operational paths. Look beyond status enums: boolean combinations, nullable fields, resource ownership, ordered calls, transactions, caches, timers, retries, cancellation, and background jobs often encode hidden state.

Group related values by the lifecycle they control. Include state held outside the process when it changes behavior: database records, queues, files, remote acknowledgments, and leases. Distinguish finite control states from payload data; do not enumerate every possible field value or invent a separate machine for every boolean.

For an “all” request, enumerate the inspected areas and exclusions. Keyword matches are leads, not evidence of complete coverage. If the app is too large for one pass, report a scoped inventory and what remains uninspected.

## Reconstruct the contract

For each important machine, identify:

- **State:** the owning component, state variables, initial state, and terminal or recurring states.
- **Transitions:** triggering events, guards, next state, and externally visible side effects.
- **Invariants:** what must remain true, including invalid combinations and forbidden transitions.
- **Recovery:** timeout, retry, cancellation, duplicate events, restart, partial failure, and concurrent actors where relevant.

Ground claims in code paths and tests. Label what is enforced, merely intended, inferred, or unknown. Absence of a transition in the code you inspected is not proof it cannot happen elsewhere.

Use a compact transition table or diagram when it clarifies the behavior. See [audit patterns](references/patterns.md) for examples and concurrency pitfalls.

## Prioritize the gaps

Focus on reachable invalid states, missing guards, duplicated authority, non-atomic transitions, lost work, repeated side effects, and recovery that cannot reach a valid state. For each significant finding, give code references, the triggering sequence or counterexample, observable impact, and the evidence still needed.

Distinguish a demonstrated defect from a plausible risk or ambiguous requirement. Rank by consequence and reachability, not diagram size. Keep harmless bookkeeping out of the headline findings.

## Recommend the smallest useful enforcement

Prefer one owning transition function, a clearer type, an enum replacing contradictory flags, a database constraint, or an invariant test when sufficient. Do not automatically add a framework, event sourcing, compatibility layer, or platform rewrite.

Connect findings to verification: transition tests, generated event sequences, fault injection, or model checking when the risk warrants it. Preserve the distinction between the reconstructed model and the running implementation. Use prove-it when asked to establish the claims, not as a reason to manufacture proof during a read-only audit.

Finish with the prioritized machine inventory, important findings, and coverage limits. Do not change code, publish findings, or contact upstream unless authorized.
