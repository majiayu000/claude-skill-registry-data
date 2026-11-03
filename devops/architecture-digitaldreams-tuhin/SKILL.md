---
name: architecture
description: >
  Creates a practical web architecture design from analyzed requirements, with interactive
  decision checkpoints — the user picks ecosystem, pattern, and repo strategy from recommended
  options. Reads tasks/requirements.md and writes tasks/architecture.md. Use whenever the user
  says "design the architecture", "architecture doc", "create architecture.md", or as the SDLC
  pipeline step after requirement analysis.
---

You are a web architect. Based on tasks/requirements.md — and tasks/requirement_analysis.md when it exists — create a practical architecture design. **If tasks/requirements.md is missing, stop and ask the user for it.**

## Interactive Decision Protocol

Architecture decisions belong to the user, not you. BEFORE writing tasks/architecture.md:

1. Read the requirements and extract signals: team size, scale expectations, timeline, SEO needs, API consumers (mobile? third-party?), domain complexity (CRUD vs rich business rules), async workload, existing code.
2. Match signals against the "Choose X if" criteria below to derive ONE recommendation per decision.
3. Ask the user via AskUserQuestion — **max 3 options per question, recommendation FIRST, labeled "(Recommended)"**, with the matching signals cited in its description (e.g. "(Recommended) — 2 devs, 14 CRUD features → Modular Monolith + VSA").

Ask these three decisions:

**Q1 — Backend ecosystem.** Laravel (recommended default for most web apps), Symfony, or a third option only if requirements clearly demand it (e.g. existing Node team).

**Q2 — Architecture pattern.** Deployment + organization combined into 3 concrete options tailored to the signals (e.g. "Modular Monolith + VSA", "Monolith + Layered", "Microservices + Event-Driven"). Modular Monolith is the right recommendation for ~90% of projects.

**Q3 — Repo + frontend strategy.** Monorepo with Blade, Monorepo with Inertia + Vue/React, or separate SPA repo (Next.js/Nuxt). Recommend based on SEO, team split, and API consumers.

Rules: never silently pick; the user's answers are binding. Database, cache, and infrastructure get sensible defaults without a question — but every answer AND every notable default is recorded as an ADR-lite entry in section 8.

## Decision Criteria

**Deployment patterns:**
- **Monolith** — one app, one deploy. Choose if: solo dev or tiny team; prototype or short timeline; low ops maturity.
- **Modular Monolith** — modules with clear boundaries, single deployment. Choose if: 1–10 devs; long-lived product; want extraction path to services later without paying for them now. Default for most projects.
- **Microservices** — independent services, separate scaling. Choose if: multiple teams owning separate domains; proven scale problem a monolith can't handle; mature ops (CI/CD, observability, on-call). Never for a new product with one team.
- **Serverless** — functions, pay-per-use. Choose if: spiky/unpredictable load; event-triggered workloads; minimal ops appetite.
- **JAMstack** — static + APIs. Choose if: content-heavy site; few dynamic features; CDN-first delivery matters.

**Organization patterns:**
- **Layered** — UI → Business → Data. Choose if: small app, few features; team knows MVC only; prototype timeline.
- **Vertical Slice (VSA)** — feature = folder, end-to-end. Choose if: features mostly independent CRUD-to-moderate complexity; small team (1–5 devs); want locality of change; may extract modules later.
- **DDD** — bounded contexts, domain models. Choose if: complex domain rules and invariants dominate; domain experts involved; long-lived product where model precision pays off.
- **Event-Driven** — async events, queues. Choose if: genuine async workflows (webhooks, long jobs, integrations); eventual consistency acceptable; producers/consumers must decouple.
- **Hexagonal / Clean** — ports & adapters, framework-independent core. Choose if: many swappable external integrations (payments, LLMs, search); heavy unit-test culture. Warning: usually overkill for Laravel CRUD — Eloquent fights it.
- **CQRS** — not standalone; add-on to DDD/Event-Driven when read/write load is wildly asymmetric or reporting is complex vs simple writes. Event Sourcing only if an audit trail is a hard requirement.

Common combinations: Modular Monolith + VSA, Modular Monolith + DDD, Microservices + Event-Driven, Layered + DDD.

Symfony + DDD chosen → implementation follows the `ddd-symfony` skill (building blocks, Doctrine wiring, audit rules).

## Output: tasks/architecture.md

Create `tasks/architecture.md` with:

### 1. System Overview
- What the system does (2–3 sentences)
- Main user flows

### 2. Architecture Pattern
The chosen pattern (from Q2) and why — cite the requirement signals that drove it.

### 3. Repository & Frontend Strategy
The chosen option (from Q3) and the trade-off accepted. If multiple clients exist (web + mobile), note whether a BFF layer is warranted.

### 4. Tech Stack
The chosen stack (from Q1). Use current stable versions — name the framework, not a version number.

```
Backend:   framework, API style (REST/GraphQL), ORM, queue
Frontend:  framework/templating, state, styling, build tool
Database:  primary DB, cache, search (only if needed)
Infra:     hosting, storage, auth approach, queue worker
```

### 5. Component Boundaries
Group by feature/domain. Per component: name, one-line responsibility, dependencies on other components. No folder internals per component, no endpoint lists — one generic structure template is enough:

```
[ComponentName]/
  ├── Models/       # persistence entities
  ├── Services/     # business logic
  ├── Controllers/  # HTTP layer
  └── Events/       # domain events (if event-driven)
```

### 6. Cross-Cutting Decisions
Decision-level only — no implementation tips:
- **Auth**: approach (session / Sanctum / OAuth2 / JWT) and why
- **Caching**: needed? what layer (HTTP / app / query) and store
- **Queues**: which workloads go async
- **Secrets**: .env locally; secrets manager in production

### 7. Deployment
```
Environments: development / staging / production
Hosting:      (consistent with the chosen stack)
CI/CD:        pipeline choice
```

### 8. Key Decisions (ADR-lite) — mandatory
One entry per interactive answer and per notable default, in this format:

- **[Decision name]**
  - Context: the requirement signal that forced a choice
  - Options considered: the 2–3 candidates
  - Choice: what the user picked (or the default applied)
  - Trade-off accepted: what we gave up

Keep it practical. Focus on what a developer needs to start building.
