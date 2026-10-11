---
name: architect
description: Turn a set of functional and non-functional requirements into high-level architecture options, recommended designs, and explicit tradeoffs. Use when Codex needs to shape a new system or feature, compare architectural approaches, define major components and boundaries, map requirements to design decisions, or recommend a practical architecture before detailed implementation begins.
---

# Architect

## Overview

Use this skill to translate requirements into a clear, decision-oriented architecture proposal. Focus on the main technical drivers, identify the few design choices that matter most, and produce a design that is easy to reason about, challenge, and evolve.

Prefer a small number of credible options over a large list of generic patterns. Make assumptions explicit and tie recommendations back to the stated requirements.

## Workflow

### 1. Frame the problem

Start by identifying:

- the product or system goal
- the primary users or actors
- the most important functional requirements
- the most constraining non-functional requirements
- the current environment, if this is an extension of an existing system

If requirements are incomplete, proceed with reasonable assumptions and label them clearly. Only stop to ask questions when a hidden choice would materially change the design.

### 2. Identify architecture drivers

Distill the requirements into the handful of drivers that should shape the design, such as:

- scale, latency, throughput, or burstiness
- reliability, availability, disaster recovery, or offline tolerance
- security, privacy, compliance, or data residency
- delivery speed, team size, ownership boundaries, or operational maturity
- integration constraints, legacy dependencies, or vendor preferences
- cost sensitivity and expected growth

Separate hard constraints from preferences.

### 3. Define the system scope and boundaries

Describe what is in scope for the design and what external systems or actors it depends on. Identify:

- client surfaces and entrypoints
- core services or modules
- data stores and major data domains
- external integrations
- trust boundaries and privileged components
- operational concerns such as queues, caches, schedulers, or observability systems

When working from an existing repo, anchor the design in the current codebase instead of proposing a rewrite by default.

### 4. Generate architecture options

Produce one to three viable approaches. For each option, capture:

- a short description of the approach
- where the main responsibilities live
- how it satisfies the top requirements
- its main tradeoffs, risks, and failure modes
- where it is overbuilt or underpowered

Avoid fake diversity. Only present distinct options when the tradeoffs are real.

### 5. Recommend a design

Choose a preferred option and explain why. The recommendation should include:

- the proposed component model
- key interfaces or communication paths
- data ownership and storage choices
- deployment shape at a high level
- security and identity considerations
- scalability and reliability approach
- operational model, including observability and failure handling

Tie each major design choice back to a requirement or constraint.

### 6. Map requirements to design decisions

Show how the recommendation addresses:

- each critical functional requirement
- each critical non-functional requirement
- important tradeoffs that remain unresolved
- assumptions that should be validated early

Be explicit about gaps where the design only partially satisfies a requirement.

### 7. Suggest next steps

Close with the most useful follow-on artifacts, such as:

- a Mermaid diagram
- an API or domain model sketch
- a data flow or threat model
- a phased delivery plan
- a proof-of-concept recommendation
- key decisions that need stakeholder confirmation

## Output Rules

Default to this structure:

1. Problem framing
2. Architecture drivers
3. Candidate options
4. Recommended architecture
5. Requirement mapping
6. Risks, assumptions, and next steps

Prefer concise prose with short lists where the content is inherently comparative. If helpful, include a Mermaid diagram for the recommended design.

Do not over-specify implementation details unless the user asks for them.

Do not recommend microservices, event-driven designs, or complex infrastructure by default. Earn complexity through requirements.

Call out when a simpler design is the better choice.

## Design Heuristics

- Start simple and add complexity only where the requirements demand it.
- Keep boundaries aligned with ownership, change rate, and trust boundaries.
- Prefer explicit data ownership over shared mutable state.
- Favor designs that are operable by the team that has to run them.
- Highlight the cost of coordination, not just the cost of compute.
- Treat security, observability, and failure handling as first-class architecture concerns.
- When non-functional requirements conflict, say so directly and explain the tradeoff.

## Example Requests

- Design a high-level architecture for a multi-tenant SaaS platform with audit logging and SSO.
- Given these functional and non-functional requirements, recommend a practical architecture for an internal workflow system.
- Compare a monolith, modular monolith, and microservice approach for this product and recommend one.
- Use this repo and these requirements to propose the next-stage architecture without rewriting everything.
