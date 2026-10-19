---
name: review-multi-agent-readiness
description: Perform an evidence-based design or launch review for a multi-agent system. Use when auditing a System Spec, architecture justification, composition manifest, interactions, dynamic membership, durability, evals, security, operations, or making a go, conditional-go, or no-go recommendation.
---

# Review Multi-Agent Readiness

Review the composition independently of member approval and require evidence for every readiness claim.

## Workflow

1. Inventory the System Spec, architecture decision, Agent Specs, policies, manifests, risk assessment, threat model, eval reports, operational artifacts, and approvals.
2. Collect the output of the project's own validation tooling or CI for member and system specifications, the interaction graph, evals, and release gates; treat it as evidence, and record its absence as a finding.
3. Verify multi-agent necessity against deterministic and single-agent baselines.
4. Review membership pinning, graph allowlists, edge authority, data flow, shared state, budgets, termination, and exact provenance.
5. Review dynamic or recursive behavior for admission, depth, fan-out, integrity, quarantine, and reproducibility controls.
6. Review durability for replay, retries, idempotency, approvals, cancellation, compensation, and in-flight upgrades.
7. Map each critical risk to implemented controls, passing eval evidence, monitoring, runbook, and owner.
8. Verify system SLOs, capacity, privacy, incident response, rollback, and change governance.
9. Issue findings by severity, distinguish blockers from improvements, and give a go, conditional-go, or no-go recommendation with conditions and expiry.

## Required Output

Produce an evidence index, findings with file and line references, unverified claims, residual risks, launch conditions, owner and due date for each blocker, and decision rationale.

Read [the readiness standard](references/standard.md) and use [the examples](references/examples.md).

## Guardrails

- Approved members do not imply an approved composition.
- A document's existence is not evidence that its controls work.
- Warnings about critical risk, placeholder evals, missing owners, or unbounded execution are blockers.
- Do not weaken a gate merely to produce a go recommendation.

## Completion Check

Every material claim must point to a contract, implementation, test or eval result, telemetry signal, accountable owner, and recovery procedure—or be reported as unverified.
