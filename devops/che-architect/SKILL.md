---
name: "che-architect"
description: "Iteratively helps architect complete systems from business ideas. Covers stack, infra, modules, data modeling, buy vs build, and resource estimation."
---

# Che Architect (System Design & Strategy)

> **SHARED REFERENCES:**
> - ADR documentation: `architecture-strategy-expert` skill
> - Mermaid visualization: Use valid `mermaid` code blocks for user journeys, feature maps, C4 diagrams, and ERDs; keep labels clear and relationships explicit.
> - Database modeling: `database-design-expert` skill
> - Engineering principles: `engineering-contracts` (KISS, YAGNI, SOLID)

## §K PROJECT KNOWLEDGE STEP (planning — bootstrap)

Once the stack, modules and data model are agreed, ask: **which terms and conventions should be recorded
now?** Load with `che knowledge show --project <slug>`; if nothing exists, this is a **no-op** — skip it.
Scaffold a domain with `che knowledge scaffold --project <slug> --domain <domain>`, propose changes with
`che knowledge apply --ops @ops.json` (dry-run), show the diff, and gate on **keep / alter / revert**
before `--no-dry-run --confirm`. Full contract: `che-knowledge` skill §6.

This skill acts as a Strategic Technical Partner. It doesn't just write code; it designs the foundations of a system through an iterative dialogue with the user.

---

## §0 PURPOSE

To transform a high-level business vision into a comprehensive technical blueprint. It balances speed-to-market (Lean) with long-term maintainability.

---

## §1 ITERATIVE WORKFLOW (The 5-Step Design)

Do NOT generate the whole plan at once. Proceed step-by-step, asking for user feedback after each phase.

### Step 1: Discovery & Intent Capture
- **Goal**: Define the "Why" and the core vision.
- **Output**: 
  - **Intent Document** (`intent.md`): Vision, Problem Statement, Success Criteria, Constraints, and Non-Goals.
  - Core Personas.
  - **Macro Business Rules**: Key constraints and mandatory behaviors.
  - **Compliance & Privacy**: Initial assessment of PII and regulations.
  - **User Journey Map**: Mermaid User Journey diagram.
  - **Feature Map**: Visual map of features categorized by module.

### Step 2: Roadmap Planning
- **Goal**: Plan the phases and milestones.
- **Output**:
  - **Project Roadmap** (`roadmap.md`): 3-5 major phases (Foundation, Core, Enhancement, etc.) with goals, deliverables, and dependencies.
  - **Technical Stack**: Language/Frameworks (Accessibility/i18n ready).
  - **Security Profile**: Criticality assessment.
  - **Buy vs Build Matrix**.

### Step 3: Architecture & Modules
- **Goal**: Design the internal structure and boundaries.
- **Output**:
  - **Pattern Selection**: Monolith vs Microservices vs Serverless.
  - **Module Map**: Responsibility boundaries (Bounded Contexts) and internal components.
  - **C4 Diagrams (Context & Container)**: Mermaid diagrams showing high-level system interactions and container-level breakdown.
  - **C4 Diagram (Component)**: Deep dive into the most critical containers to show internal component relations.
  - **Macro Data Model (ERD)**: Mermaid Entity Relationship Diagram of core entities and their associations.
  - **Security & Privacy Design**: Data encryption, Auth flow, and RLS strategy.
  - **Architecture Decisions**: Key trade-offs documented as initial ADRs.

### Step 4: Infrastructure & Resource Estimation
- **Goal**: Plan the deployment, maintenance, and observability.
- **Output**:
  - **Cloud Provider**: AWS, Vercel, Railway, Supabase, etc.
  - **CI/CD Pipeline**: Deployment strategy (Blue/Green, Canary).
  - **Observability Strategy**: Logs, Metrics, and Tracing from day one.
  - **Operations & Support**: User support plan, incident response, and operational roadmap.
  - **Resource Estimation**: Estimated cost per month (low/high) and effort (Man-months/Sprints).

### Step 5: The Blueprint (Final Artifacts)
- **Goal**: Save the durable architecture and planning documentation to ensure long-term navigability.
- **Action**: Save the final artifacts to `$CHE_WORKSPACE_SHARED/projects/<slug>/`:
  - `intent.md`: The high-level "Why", Success Criteria, and Non-Goals (Specflow Phase 1).
  - `roadmap.md`: The phased timeline, feature map, and milestones (Specflow Phase 2).
  - `architecture.md`: The technical blueprint (C4, ERD, Security).
- **Action**: Create initial ADRs for critical decisions in `$CHE_WORKSPACE_SHARED/projects/<slug>/adr/`.
- **Navigability**: Ensure all future tasks can reference IDs defined in `roadmap.md`.

---

## §2 MANDATORY SECTIONS FOR ARCHITECTURE.MD

Every generated architecture document MUST include:
1. **Executive Summary**: 1-paragraph business vision.
2. **User Journey & Feature Map**: Visual flows and feature hierarchy.
3. **Tech Stack & Strategy**: Versions, choices, and reasoning (Buy vs Build, i18n, Accessibility).
4. **C4 Architecture Diagrams**: Context, Container, and Component levels.
5. **Data Modeling (ERD)**: Mermaid diagram of core entities.
6. **Security, Compliance & Privacy**: Threat modeling, regulatory mapping (GDPR/LGPD), and data protection.
7. **Infrastructure & Observability**: Deployment model and monitoring plan.
8. **Scalability & Performance**: How the system grows.
9. **Operations & Support**: How the system is maintained and how users are supported.
10. **Implementation Roadmap**: Phase 1 (MVP) vs Phase 2 (Growth).
11. **ADR Index**: Link to the detailed Architecture Decision Records.

---

## §3 QUALITY GATES
- **Simplicity Bias Check (engineering-contracts §1 — the touchstone)**: for each major decision (stack, pattern, module, data model), apply the ordered solution-selection rule and prefer the simplest candidate over the most complete/robust one. Record the simplest candidate chosen AND the capabilities deliberately deferred in `intent.md` (Non-Goals). Never recommend Kubernetes / Kafka / microservices / a DI container for a problem a monolith + 1 DB solves. Never overrides Security (§2).
- **KISS/YAGNI Check**: Avoid over-engineering. If the user asks for a simple app, don't recommend Kubernetes.
- **Portability Check**: Ensure the architecture isn't locked into a single vendor unless requested.
- **Cohesion Check**: Ensure modules have clear boundaries and low coupling.
