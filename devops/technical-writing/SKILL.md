---
name: technical-writing
description: "Use when the work produces a document that must be understood by someone who was not there when the system, procedure or decision was made, and that stays in the repository after the work merges: a README, an architecture or system document, an ADR, a runbook, an onboarding guide, an API guide, a migration note. Not for the working documents of a piece of work (boards, specs, plans and reports belong to the skills that produce them) and not for persuasive prose."
---

# Technical writing

**The reader arrives with a question; the document reduces the uncertainty around it** until the reader can understand the system, make the decision, or perform the action. The structure, the constraints, the decisions, the evidence and the consequences are made visible, without making the engineering look simpler than it is.

## Mindset

- **One reader, one question.** "How do I run this?", "why does this service depend on this database?" and "what do I do when the deployment fails?" are three documents. Name the reader and the question first, answer first, let background follow.
- **Draw the structure before writing**, through the `write-diagrams` skill, picking from its catalog by the reader's question. A concept with components, ordering, states, ownership or dependencies is drawn, never narrated.
- **State where a responsibility ends.** For each significant component: what it owns, consumes, produces, depends on, deliberately does not do, and what can change without affecting it. Never "handles" or "manages".
- **Start decisions from constraints.** Problem, constraints, alternatives, decision, consequences. "Data cannot leave the organisation, therefore inference runs inside its infrastructure" is a design; "the system uses Kubernetes and llama.cpp" is inventory.
- **Preserve the reasoning a future engineer would otherwise rediscover**, for the decisions whose reversal would need it and only those: the problem, the plausible options, the constraint that mattered, what was chosen and rejected, what it costs, what it makes possible, what remains unresolved.
- **Keep fact, constraint, decision and consequence apart**, each stated as what it is.
- **Say what is hard and why, and no more.** A named risk gets discussed; an adjective gets nodded past.

## Flow

1. **Name the reader and the question, and choose the document type below.**
2. **Write it in the repository**, never in aiview's data home, and read it rendered. Durable documents live next to what they describe, under stable names (`README.md`, `docs/architecture.md`, `docs/runbook.md`); point-in-time material under dated names.
3. **Verify every actionable claim at writing time**: commands, paths, ports, configuration, API behaviour, procedures, versions. What cannot be verified is qualified or removed.
4. **Cut what does not change the reader's understanding, decision or action**: repetition, history, technology inventory, unsupported adjectives, prose that duplicates a diagram.

**When the system changes in a way that invalidates the document, the document changes in the same commit.**

## Document types

| Type | Reader's question | Shape | Diagram, from the `write-diagrams` catalog |
| --- | --- | --- | --- |
| README | "What is this and how do I run it?" | What it is, requirements, run, repository map | Usually none. A README that needs one is an architecture doc wearing a README's name. |
| Architecture / system doc | "How does this work?" | Constraints, structural diagram, components, flows, decisions, consequences | Container or component; sequence for the flows that matter; dependency graph where import direction is a rule. |
| ADR | "Why is it like this?" | Context, constraints, alternatives, decision, consequences | Option comparison: the alternatives side by side, the deciding trade-off under them. |
| Runbook | "It's broken. What do I do?" | Preconditions, procedure, expected result, failure branches, rollback | User flow for the operator's path, state machine when the system has modes. |
| Onboarding | "Where do I start?" | System map, reading path, first task, deeper references | System context or container as the map; user flow for the first task. |
| API guide | "How do I call this?" | Working example, interaction flow, authentication, errors, reference | Sequence, for any handshake or multi-step call. |
| Migration note | "What changed and what must I do?" | What changes, before and after, migration order, failure and rollback | Phasing: what moves first; before and after as two small diagrams when the contrast is the point. |

## Core test

**Before publishing: can a competent engineer who did not build this system understand its structure, boundaries, constraints, important decisions, consequences and next action without asking anyone?** If not, the document is not finished.
