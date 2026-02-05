---
name: togaf-guidance
description: Guide users through TOGAF ADM phases with context-aware advice. Use when applying TOGAF methodology or understanding ADM phase activities.
allowed-tools: Read, Glob, Grep
---

# TOGAF Guidance

## When to Use This Skill

Use this skill when you need to:

- Understand which TOGAF ADM phase applies to your current work
- Get phase-specific activities and deliverables
- Learn about TOGAF methodology in practical terms
- Apply enterprise architecture governance

**Keywords:** togaf, adm, architecture development method, phase, business architecture, technology architecture, migration planning, implementation governance, architecture vision

## TOGAF 10 Overview

TOGAF (The Open Group Architecture Framework) provides a comprehensive methodology for developing enterprise architecture. The core is the **Architecture Development Method (ADM)** - an iterative cycle of 10 phases.

### The Four Architecture Domains

| Domain | Focus | Artifacts |
| --- | --- | --- |
| Business | Processes, capabilities, organization | Business process models, capability maps |
| Data | Information assets, data management | Data models, data flow diagrams |
| Application | Applications and their interactions | Application portfolio, integration diagrams |
| Technology | Infrastructure and platforms | Technology standards, deployment diagrams |

## ADM Phases

### Preliminary Phase

#### Purpose

Establish the architecture capability within the organization.

#### Key Activities

- Define architecture principles
- Establish governance framework
- Select tools and methods
- Define scope of architecture work

#### Deliverables

- Architecture principles catalog
- Organization model for EA
- Tailored architecture framework

#### When you're here

Starting a new EA initiative or formalizing existing practices.

---

### Phase A: Architecture Vision

#### Purpose

Create a high-level vision aligned with strategic goals.

#### Key Activities

- Identify stakeholders and concerns
- Define architecture scope
- Create high-level vision
- Obtain approval to proceed

#### Deliverables

- Architecture vision document
- Stakeholder map
- Statement of architecture work

#### When you're here

Beginning a new architecture project or major initiative.

---

### Phase B: Business Architecture

#### Purpose

Develop the business architecture to support the vision.

#### Key Activities

- Model current business processes
- Define target business capabilities
- Identify gaps and opportunities
- Align with business strategy

#### Deliverables

- Business architecture document
- Process models
- Capability assessment

#### When you're here

Understanding business needs before technical solutions.

---

### Phase C: Information Systems Architecture

#### Purpose

Define data and application architectures.

#### Sub-phases

- **Data Architecture**: Information assets, data models, data governance
- **Application Architecture**: Application portfolio, integrations, APIs

#### Key Activities

- Model current and target data architecture
- Define application components and interactions
- Identify data-related gaps

#### Deliverables

- Data architecture document
- Application architecture document
- Integration specifications

#### When you're here

Designing the systems that support business capabilities.

---

### Phase D: Technology Architecture

#### Purpose

Define the technology infrastructure.

#### Key Activities

- Define technology standards
- Model infrastructure components
- Plan platform capabilities
- Address non-functional requirements

#### Deliverables

- Technology architecture document
- Infrastructure diagrams
- Technology standards catalog

#### When you're here

Selecting platforms, infrastructure, and technology standards.

---

### Phase E: Opportunities & Solutions

#### Purpose

Identify implementation approaches and projects.

#### Key Activities

- Consolidate gaps from B, C, D
- Group into work packages
- Evaluate build vs buy vs reuse
- Identify transition architectures

#### Deliverables

- Implementation factor assessment
- Work package definitions
- Transition architecture descriptions

#### When you're here

Planning how to get from current to target state.

---

### Phase F: Migration Planning

#### Purpose

Create detailed implementation roadmap.

#### Key Activities

- Prioritize projects
- Estimate resources and timelines
- Define migration approach
- Create implementation roadmap

#### Deliverables

- Implementation and migration plan
- Architecture roadmap
- Transition architecture details

#### When you're here

Creating the execution plan with timelines and dependencies.

---

### Phase G: Implementation Governance

#### Purpose

Oversee architecture implementation.

#### Key Activities

- Provide architecture oversight
- Conduct architecture compliance reviews
- Handle change requests
- Ensure implementation matches design

#### Deliverables

- Architecture compliance assessments
- Change requests
- Implementation guidance

#### When you're here

Projects are executing; ensuring they follow the architecture.

---

### Phase H: Architecture Change Management

#### Purpose

Manage changes to the architecture over time.

#### Key Activities

- Monitor technology changes
- Assess business changes
- Determine if new ADM cycle needed
- Maintain architecture relevance

#### Deliverables

- Architecture change requests
- Updated architecture documentation
- Recommendations for new cycles

#### When you're here

Maintaining and evolving the established architecture.

---

### Requirements Management

#### Purpose

Manage architecture requirements throughout all phases.

**Note:** This is a cross-cutting activity, not a sequential phase. Requirements management operates continuously across all ADM phases.

#### Key Activities

- Identify requirements
- Baseline requirements
- Monitor baseline
- Handle requirement changes

#### Deliverables

- Requirements repository
- Impact assessments
- Requirement changes log

---

## Phase Identification Guide

Not sure which phase you're in? Ask these questions:

1. **Are you starting fresh with EA?** → Preliminary Phase
2. **Defining scope and getting buy-in?** → Phase A
3. **Understanding business needs?** → Phase B
4. **Designing systems and data?** → Phase C
5. **Selecting technologies?** → Phase D
6. **Identifying projects?** → Phase E
7. **Planning implementation?** → Phase F
8. **Overseeing execution?** → Phase G
9. **Maintaining/evolving?** → Phase H

## Practical Application

### For Small Projects

You don't need all phases for every project. A minimal cycle:

1. **Vision** (A): What are we trying to achieve?
2. **Solution** (C/D): What's the technical approach?
3. **Plan** (F): How do we get there?
4. **Execute** (G): Build it right

### For Large Initiatives

Follow the full cycle with appropriate rigor:

- Formal stakeholder management
- Complete documentation
- Governance checkpoints
- Architecture review boards

## Memory References

For detailed phase information, see `references/togaf-overview.md`.

## Version History

- **v1.0.0** (2025-12-05): Initial release
  - Complete ADM phase documentation (Preliminary through H)
  - Requirements Management (cross-cutting)
  - Phase identification guide
  - Practical application for small and large projects

---

## Last Updated

**Date:** 2025-12-05
**Model:** claude-opus-4-5-20251101
