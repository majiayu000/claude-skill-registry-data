---
name: design-multi-agent-system
description: Design, justify, scaffold, or refactor a governed multi-agent system. Use when choosing an architecture, defining a System Spec, composing existing Agent Specs, comparing a multi-agent design with a simpler baseline, or deciding whether static or dynamic membership is appropriate.
---

# Design a Multi-Agent System

Design the system as an explicit composition contract built on individually governed agents.

## Workflow

1. Inspect repository instructions, Agent Specs, risk assessments, evals, and existing system contracts.
2. Establish a deterministic or single-agent baseline. State the measurable benefit that requires multiple agents.
3. Select the simplest topology that provides that benefit. Treat topology, membership, and interaction edges as policy.
4. Choose static membership by default. Use dynamic membership only when runtime discovery creates material value and an authenticated registry plus admission policy can enforce compatibility.
5. Define the System Spec: owners, version, execution class, governance tier, justification, topology, pinned members, restrictions, interactions, system budgets, state owner, and termination states.
6. Ensure the system class and tier are never below any member or enabled path.
7. If the project provides scaffolding tooling, use it, replace every placeholder, and inspect generated policies.
8. Validate the System Spec and render its interaction graph with the project's own validation tooling or CI; resolve contract errors before runtime implementation.
9. Record rejected designs and open product decisions instead of inventing policy.

## Required Output

Produce a versioned System Spec, architecture decision, explicit member and edge policies, termination policy, system risk assessment, and evaluation entry point.

Read [the system design standard](references/standard.md) before choosing a topology. Use [the examples](references/examples.md) to compare fixed and dynamic designs.

## Guardrails

- Do not add agents merely to improve prompt separation.
- Do not infer authority from an agent role or a successful handoff.
- Do not allow arbitrary peer calls outside the declared graph.
- Do not approve dynamic membership without admission, integrity, and manifest controls.
- Do not claim readiness from member-level tests alone.

## Completion Check

Another engineer must be able to explain why the system is multi-agent, which exact composition is approved, who may call whom, how work ends, and when the design should collapse back to a simpler baseline.
