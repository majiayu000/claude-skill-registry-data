---
name: arch-design
description: "Design system architecture from approved requirements — quality attributes, style selection, arc42/4+1 views, ADRs. Use when: design architecture, new architecture, architect the system, system design, choose architecture, architectural design, create architecture, system structure."
license: CC-BY-SA-4.0
metadata:
  source: "agents/skills/architecture/arch-design.skill.md"
  tags: "architecture"
  core: "true"
  context_cost: "high"
---
# Architecture Design Skill

## Goal

Produce a complete, documented architecture for a system — from quality attribute
analysis through structural and behavioral design to documented decisions.
Technology choices are deferred until the architecture is stable. This skill is
technology-agnostic; specific technology decisions happen via adr-writer.skill.

---

## When to Use

- **Scenario 1 (New System)**: Greenfield architecture. Requirements exist and are approved (req-elicitation output). No existing system to constrain design choices.
- **New major subsystem**: Adding a subsystem with significant architectural impact.
- **Technology migration**: Redesigning architecture before selecting new technologies.

---

## Step 1 — Quality Attribute Analysis

```
Before designing structure, identify the quality drivers — the attributes that
will most constrain architectural choices.

For each quality attribute:
  Use Quality Attribute Scenario (QAS) format:
  Source     → who/what causes the stimulus
  Stimulus   → the event that occurs
  Environment → the operating conditions
  Artifact   → the part of the system affected
  Response   → what the system does
  Measure    → how we know it's acceptable

Priority the top 3-5 QAS that will DRIVE architectural decisions.
These become architecture fitness functions.

ISO 25010 Quality Attributes to assess:
  Performance efficiency:   response time, throughput, capacity, resource utilization
  Reliability:              availability, fault tolerance, recoverability, MTTR
  Security:                 confidentiality, integrity, accountability, authenticity
  Usability:                appropriateness, learnability, accessibility, error handling
  Maintainability:          modularity, reusability, analyzability, modifiability, testability
  Portability:              adaptability, installability, replaceability
  Compatibility:            coexistence, interoperability

Fill: templates/architecture/QUALITY_ATTRIBUTES_TEMPLATE.md before selecting styles.
```

---

## Step 2 — Architectural Style Candidates

```
Based on dominant quality attributes, consider these architecture styles:

Layered (N-Tier):
  Strengths: ease of modification, separation of concerns, testability
  Weaknesses: performance (pass-through layers), tight coupling across layers
  Use when: maintainability is dominant; general-purpose business applications

Event-Driven:
  Strengths: decoupling, scalability, auditability
  Weaknesses: complex event flows, eventual consistency, debugging difficulty
  Use when: loose coupling is critical; high throughput with asynchronous processing

Microkernel (Plugin):
  Strengths: extensibility, isolation, customizability
  Weaknesses: plugin API stability challenges, complex registry
  Use when: system must be extended by third parties; product with many variants

Space-Based:
  Strengths: extreme scalability, fault tolerance
  Weaknesses: data consistency challenges, implementation complexity
  Use when: very high load with unpredictable spikes; financial trading, ticketing

Service-Oriented / Service-Based:
  Strengths: domain-aligned, team independence, deployability
  Weaknesses: network latency, distributed transactions, operational overhead
  Use when: multiple independent business domains; multiple teams; independent scaling needs

Pipe-and-Filter:
  Strengths: composability, parallelism, testability
  Weaknesses: shared data stores create coupling; not suited for interactive systems
  Use when: data transformation pipelines; ETL; processing workflows

Decision: Document style choice with rationale in ADR.
Do NOT prematurely mix styles — pick a primary style and extend if needed.
```

---

## Step 3 — System Decomposition

```
Decompose the system into components based on:

Decomposition strategies:
  Business capability decomposition:
    Each component = one business capability
    Capabilities identified from use cases and domain model
    Components should be loosely coupled, highly cohesive

  Domain-Driven decomposition:
    Each component = one bounded context
    Uses ubiquitous language within each context
    Well-defined interfaces between contexts (context map)

  Layer-based decomposition (within a component):
    Presentation → Application Logic → Domain → Infrastructure
    Each layer with defined responsibilities

For each component, define:
  Name: [what it's called — using domain language]
  Responsibility: [what ONE thing it does — single reason to change]
  Owns: [data/state it owns exclusively]
  Collaborators: [other components it depends on, and WHY]
  Interface: [what it exposes to other components]
  Deployment boundary: [process / container / service]

Create system decomposition diagram (C4 Container or Component level).
Fill: templates/architecture/ARCHITECTURE_VIEWS_TEMPLATE.md (Component View section)
```

---

## Step 4 — Architectural Views (4+1 or arc42)

```
Create all relevant views:

LOGICAL VIEW — what the system IS (structure):
  Components and their responsibilities
  Key abstractions (major domain concepts as components)
  Component relationships and dependencies
  Diagrams: C4 Component, UML Component diagram

PROCESS VIEW — what the system DOES (behavior):
  Key use case flows through the architecture
  Concurrency model (threads, processes, async patterns)
  State transitions for stateful components
  Diagrams: Sequence diagram, Activity diagram, State diagram

DEVELOPMENT VIEW — how the system is BUILT (code organization):
  Module/package structure
  Layer boundaries and import rules
  Build dependencies
  Diagrams: Package diagram, Module dependency diagram

DEPLOYMENT VIEW — where the system RUNS (infrastructure):
  Physical nodes and containers
  Component-to-node assignment
  Network topology and communication paths
  Diagrams: C4 Deployment, UML Deployment diagram

SCENARIOS (4+1 '+1') — how views come together:
  Walk through 3-5 key use cases showing how all views interact
  Validate that the architecture satisfies the use cases
  These are the fitness function checks

Fill: templates/architecture/ARCHITECTURE_VIEWS_TEMPLATE.md (all sections)
```

---

## Step 5 — Interface Design

```
For every component boundary, define:

Interface contract:
  - Operations exposed (name, parameters, return type — no language syntax)
  - Pre-conditions: what must be true before calling
  - Post-conditions: what is guaranteed after calling
  - Error/exception scenarios: what happens when things go wrong
  - Protocol: synchronous call / async message / event / stream

Data contract:
  - Data structures exchanged at the boundary
  - Required vs optional fields
  - Valid value ranges and constraints
  - Versioning strategy (how will interface evolve?)

Communication style:
  Synchronous: caller blocks, expects immediate response
  Asynchronous: caller does not block (message queue, event bus, callback)
  Event: component emits event, others may react (no guaranteed recipient)

Document all interface contracts — implementation must match.
```

---

## Step 6 — Key Architecture Decisions

```
For every significant choice, write an ADR (use adr-writer.skill):

Mandatory ADRs:
  ADR-001: Primary architecture style choice and rationale
  ADR-002: System decomposition strategy (by capability, domain, layer)
  ADR-003: Communication pattern (synchronous vs async, protocol)
  ADR-004: Data ownership and storage strategy (per-component, shared)
  ADR-005: Security architecture (authentication/authorization approach)

Optional ADRs (write if non-obvious):
  ADR-NNN: Specific quality attribute tactic choices
  ADR-NNN: API style decision (REST, GraphQL, gRPC, events)
  ADR-NNN: Scalability approach
  ADR-NNN: Observability approach

Each ADR must include rejected alternatives with reasons — this is crucial
for future reviewers to understand why not to go back to a rejected option.
```

---

## Step 7 — Risk Identification

```
For each QAS (from Step 1), assess:
  Risk: "Does the architecture as designed achieve this QAS?"
  Sensitivity point: "What single design choice most affects this QAS?"
  Tradeoff point: "What two QASes compete for the same resource?"

Architecture risks (potential failures in the design):
  List with: description, likelihood (H/M/L), impact (H/M/L), mitigation approach

Architecture debt decisions (conscious shortcuts):
  List with: description, why accepted, how to address in future

Output: docs/architecture/ARCHITECTURE_RISKS.md
```

---

## Step 8 — Architecture Documentation

```
Compile into: docs/architecture/ARCHITECTURE.md or fill arc42 template

Minimum required sections:
  1. Introduction and Goals (from requirements)
  2. Constraints (technical, regulatory, organizational)
  3. Context and Scope (System Context diagram — C4 Level 1)
  4. Solution Strategy (architecture style + key decisions summary)
  5. Building Block View (decomposition — C4 Level 2/3)
  6. Runtime View (key scenarios as sequence/activity diagrams)
  7. Deployment View (C4 Deployment)
  8. Quality Concepts (how QAS requirements are addressed)
  9. Architectural Decisions (links to ADRs)
  10. Risks and Technical Debt
```

---

## Output Checklist

```
[ ] templates/architecture/QUALITY_ATTRIBUTES_TEMPLATE.md completed (top 5 QAS)
[ ] templates/architecture/ARCHITECTURE_VIEWS_TEMPLATE.md completed (all 4+1 views)
[ ] templates/architecture/CONTEXT_MAP_TEMPLATE.md completed (if domain-driven)
[ ] ADR-001 to ADR-005 written (use adr-writer.skill)
[ ] docs/architecture/ARCHITECTURE_RISKS.md written
[ ] At least one diagram per view
[ ] All component interfaces documented
[ ] Architecture validated against top 5 QAS (each must be satisfiable)
[ ] Human approval before proceeding to implementation planning
```

---

## Constraints

- Architecture must be documented BEFORE technology is selected
- Every component must have a single, clearly stated responsibility
- Every interface must be explicitly documented — no implicit coupling
- No orphan components — every component serves a documented use case
- Rejected alternatives must be documented in ADRs — prevents re-litigating decisions
- Architecture must satisfy ALL MUST-level quality attribute scenarios
- If a MUST QAS cannot be satisfied: escalate to human before proceeding

## Security & Guardrails

### Steps
## 1. Skill Security (Architecture Design)
- **Threat Model Prerequisite**: The agent is prohibited from finalizing the "Solution Strategy" (Step 4 of Documentation) without simultaneously invoking the `threat-model.skill.md`. A structural architecture designed without an adversarial mindset is fundamentally incomplete.
- **Authorization as a Core View**: The agent must not relegate User Identity and Access Management to a secondary "implementation detail." The Logical View and Process View must explicitly diagram how authentication flows through the system boundaries (e.g., Token exchange at the API Gateway, JWT passing to microservices).

### 2. System Integration Security
- **Zero-Trust Baseline Enforcement**: When defining the Deployment View (Step 4) and Network Topology, the agent must default to a Zero-Trust posture. It must explicitly reject any architectural diagram that implies "implicit trust" within the private network (e.g., microservices communicating over unencrypted HTTP just because they share a VPC).
- **Data Classification Anchoring**: Before selecting Data Ownership strategies (ADR-004), the agent must categorize the data flowing through the components. High-sensitivity data (PII, PCI) must influence the architecture style, potentially forcing a Microkernel or isolated Service-Oriented approach specifically to contain the compliance blast radius.

### 3. LLM & Agent Guardrails
- **Resume-Driven Design Bias**: The LLM often biases towards trendy, hyper-scalable architectures (like globally distributed Event-Driven Microservices) regardless of actual requirements. The agent must act as a strict counter-balance, using the Quality Attribute Scenarios (Step 1) as hard mathematical constraints to veto over-engineered patterns.
- **Security-Washing Detection**: The agent must verify that "Security" listed as a Quality Attribute isn't just a buzzword. If Security is stated as a priority but the resulting Architecture doesn't explicitly allocate components to KMS, WAFs, and Audit Logging, the agent must reject the design for failing its own fitness function.
