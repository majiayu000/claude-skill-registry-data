---
name: design-agent-interactions
description: Design or review multi-agent delegation, handoff, review, voting, fan-out, shared-artifact, and event contracts. Use when defining who may call whom, typed message envelopes, edge-specific authority, context sharing, retry ownership, aggregation, dissent, or interaction-level budgets.
---

# Design Agent Interactions

Turn every agent-to-agent edge into a typed, authorized, observable protocol.

## Workflow

1. Load the System Spec, member Agent Specs, data policy, and proposed graph.
2. Enumerate every permitted edge. Reject implicit peer access and undeclared callbacks.
3. Select the interaction mode and define typed input, result, failure, evidence, and correlation fields.
4. Compute edge authority as an intersection; never copy the caller's credentials or full capability set.
5. Minimize context. Send task-specific summaries, artifact references, provenance, and policy labels—not hidden instructions, credentials, or full history by default.
6. Assign ownership for timeout, retry, deduplication, cancellation, late results, and partial effects.
7. Define aggregation and disagreement rules in deterministic policy where possible.
8. Set per-edge call, token, tool, cost, and time budgets inside the system envelope.
9. Add contract, authorization, injection-propagation, duplicate-delivery, and dissent tests.

## Required Output

Produce an interaction table or policy with callers, callees, mode, schemas, authority maximums, data maximums, budgets, retry policy, failure behavior, and telemetry fields.

Read [the interaction standard](references/standard.md) and adapt [the examples](references/examples.md).

## Guardrails

- A delegation is not authorization.
- Artifact location is not permission to read it.
- A reviewer must not silently rewrite the producer's evidence.
- Voting does not turn correlated guesses into truth.
- Retried consequential effects require idempotency and explicit ownership.

## Completion Check

For every edge, identify the initiating principal, allowed data and authority, finite budget, typed outcomes, retry owner, and evidence needed to reconstruct the exchange.
