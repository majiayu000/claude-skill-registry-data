---
name: infra-kit.workflow.design
description: Design infrastructure changes with explicit requirements, SLOs, security controls, rollout safety, and operational ownership.
---

# Infrastructure Design

Use this skill when the user is designing or significantly changing infrastructure: new platform components, migrations, networking changes, CI/CD delivery patterns, data stores, clusters, or cross-cutting guardrails.

The goal is a design that is safe to ship and easy to operate.

This skill always produces two diagrams (Mermaid preferred):

- a **system diagram** (components and trust boundaries)
- a **flow diagram** (request/data/control flow for the primary use-case and one failure path)

## Outcomes

- Produce a concise design doc or ADR with clear requirements, constraints, and trade-offs
- Make reliability and security first-class (SLOs, threat model, least privilege)
- Specify rollout/rollback steps so changes are safe under real production constraints
- Ensure ownership: alerts, runbooks, on-call expectations, and ongoing costs

## Where This Fits In The Flow

- Use after intake when the change is non-trivial and needs explicit rollout/rollback and ownership.
- Use to produce the high-quality plan that becomes `infra-kit.workflow` `plan.md` and drives `tasks.md`.

## Output Rules

- Always write deliverables to one or more Markdown files in the repo (do not only respond in chat).
- If the design is large, split it into multiple files and keep each file focused and skimmable.
- Prefer a stable location such as `docs/infra-design/<topic>/`.
- Always include the required diagrams in the design doc:
- System diagram (Mermaid)
- Flow diagram (Mermaid)

## Workflow

1. Clarify scope: what is being built/changed and what is explicitly out of scope.
2. Capture requirements:
   - functional requirements
   - non-functional requirements: latency/throughput, availability, RTO/RPO, compliance, data residency
3. Define success metrics:
   - SLOs and key SLIs
   - error budget policy if relevant
4. Identify constraints:
   - team skill constraints
   - vendor/region constraints
   - budget constraints
   - migration constraints (downtime, cutover windows)
5. Propose 2-3 viable options.
6. Evaluate options with a consistent rubric:
   - reliability and failure modes
   - security posture (authN/Z, network boundaries, secrets, audit)
   - operational complexity (runbooks, incident response)
   - cost and capacity model
   - delivery risk (how hard to roll out/rollback)
7. Create the diagrams:
   - System diagram: components, dependencies, network boundaries, identities, data stores
   - Flow diagram: primary happy path plus at least one failure/retry/degraded path
8. Do a pre-mortem:
   - if this design fails in prod, what failed and why
   - list mitigations and detection signals
9. Write the plan to ship:
   - staged rollout
   - verification steps
   - rollback criteria and steps
   - deprecation plan for old paths
10. Close with open questions and the smallest next experiment that reduces uncertainty.

## Hallucination Guardrails

- Do not invent requirements, SLOs, or compliance constraints. Ask when unknown.
- Do not assume a cloud, region, or managed service unless the user states it.
- Prefer explicit unknowns over implicit guesses.

## Design Checklist

- Ownership: who runs it, who gets paged
- Observability: dashboards, alerts, logs, traces; signals detect the known failure modes
- Security: identity boundaries, least-privilege IAM, secrets handling, audit trails
- Reliability: dependency mapping, degraded mode, backpressure, retries/timeouts
- Data: backups, restore tests, retention, encryption, access patterns
- Change safety: canary/blue-green, feature flags, config rollout, rollback path
- Cost: steady-state cost, scaling behavior, non-prod strategy
- System diagram exists and matches the written design
- Flow diagram exists for the primary path and one failure path

## References
