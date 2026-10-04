---
name: modular-monolith-decomposer
description: Decomposes a system description into Modular Monolith modules using Domain-Driven Design (DDD) principles. Produces a bounded context map, data ownership table, external integration boundaries, cross-module communication patterns, a ready-to-use directory structure, and an architectural decision log. Use when the user says "which modules should I create", "modular monolith decomposition", "map bounded contexts", "identify modules from PRD", "structure this codebase", "DDD module mapping", "data ownership", "find module boundaries", "how to organize my modules", or provides any system description (PRD, requirements, informal explanation) and wants to implement it as a Modular Monolith. Do NOT use for Event Storming artifact creation (use event-storming skill), microservices decomposition, or general architectural Q&A without a concrete system description to analyze.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Modular Monolith Decomposer

Analyzes a system description and decomposes it into modules for a Modular Monolith architecture using DDD principles. Produces a complete module map, data ownership table, directory structure, and architectural report — then offers to scaffold the files.

---

## Instructions

### Step 1: Acknowledge and Clarify

Briefly confirm what you received (e.g., "Analisando a descrição como Modular Monolith com DDD...").

Ask one clarifying question only if the input cannot yield at least 3 distinct entities or processes. If the description is sufficient, go directly to Step 2.

If the user provides only a domain name with no details, ask: "Can you describe the main entities, workflows, or data involved? A paragraph is enough."

### Step 2: Identify Bounded Contexts

Scan the input for cohesive business concepts that share:

- Internal consistency (they belong together naturally)
- A clear external boundary (they don't bleed into other concerns)
- An identifiable owner (one team could be responsible)

Group related concepts into candidate Bounded Contexts using the pattern: **[concept cluster] → [context name]**

Rules to apply:

- One Bounded Context = one module. Do not split a context into multiple modules.
- Name contexts as nouns in kebab-case: `licenses`, `billing`, `auth`, `contracts`.
- If two concepts share the same aggregate root and lifecycle, keep them in one context.
- If two concepts evolve at different rates or have different business owners, split them.
- When uncertain, apply Conway's Law: split by team boundary, not by technical layer.

### Step 3: Map Data Entities to Modules

For each entity, aggregate, or table mentioned in the input:

1. Assign exactly one owning module — no entity can be owned by two modules.
2. If another module needs that data, it must go through the owning module's public interface (API, facade, or event) — never direct DB access.

Build this table:

```
| Entity / Table      | Owning Module | Notes                        |
|---------------------|---------------|------------------------------|
| [EntityName]        | [module]      | [core aggregate / sub-entity]|
```

If an entity is split across multiple current modules in the description, document the decision and which module wins ownership.

### Step 4: Identify External Integrations

Flag every external system mentioned (third-party APIs, SaaS platforms, webhooks, payment gateways, LMS, CRM):

- Each external system → one isolated module under `integrations/<system-name>/`
- Integration modules contain only the adapter/client code — no business logic lives here
- Business logic that drives the integration lives in the core module that owns the workflow
- Cross-cutting concerns (retry policy, auth tokens) go in `integrations/shared/` if reused

### Step 5: Apply Modular Monolith Rules

Enforce these constraints against the modules found:

**Rule 1 — No shared tables.** Each table belongs to exactly one module. Violations must be resolved by assigning clear ownership and defining an access interface.

**Rule 2 — No direct cross-module imports.** Modules expose a public `index` file. Internal files are private.

**Rule 3 — Cross-module side effects use events or facades.** Use async events for fire-and-forget (e.g., notifications). Use sync facades for queries where the caller needs a response.

**Rule 4 — Shared utilities live in `shared/`.** Domain-agnostic code (types, base classes, event bus) belongs in a shared kernel, not inside any domain module.

For each cross-module dependency detected, record: who needs what, from whom, and via which pattern (sync or async).

### Step 6: Classify Core vs Support

Split all modules into two categories:

**Core (business differentiators):** Encodes rules that directly generate value. Changing these changes the business model. These modules are what makes the product unique.

**Support (cross-cutting capabilities):** Enable core modules but don't encode business rules. Could theoretically be replaced by a third-party service without changing the business logic.

Present as:

```
Core:    [module-a], [module-b], [module-c]
Support: [module-d], [module-e]
Integrations: integrations/[system-a], integrations/[system-b]
```

### Step 7: Generate the Decomposition Report

Output the full report in this exact structure:

---

#### Module Decomposition Report

**Architecture Style:** Modular Monolith
**DDD Approach:** Bounded Context per module — data ownership enforced at module boundaries

##### Classification

```
Core:         [comma-separated]
Support:      [comma-separated]
Integrations: [comma-separated]
```

##### Data Ownership Table

```
| Entity / Table      | Owning Module | Notes |
|---------------------|---------------|-------|
```

##### Module Details

For each module:

```
#### `<module-name>` [Core | Support | Integration]

**Responsibility:** [one sentence describing what this module knows and decides]
**Owns:** [entities/tables]
**Exposes:** [public interface — events emitted, facade methods, REST endpoints]
**Depends on:** [module → pattern (sync/async), what it accesses]
**External system:** [only for integration modules]
```

##### Cross-Module Communication Map

```
| From Module  | To Module   | Data / Event           | Pattern    |
|--------------|-------------|------------------------|------------|
| [module]     | [module]    | [what is communicated] | sync/async |
```

##### Directory Structure

Adapt to only the modules actually found — do not invent modules:

```
src/
├── modules/
│   ├── [module-a]/
│   │   ├── domain/
│   │   ├── application/
│   │   ├── infrastructure/
│   │   └── index.ts          # public interface — only this file is importable by other modules
│   └── [module-b]/
│       └── ...
├── integrations/
│   └── [system-name]/
│       ├── client/
│       └── index.ts
└── shared/
    ├── events/
    └── types/
```

If the user's stack uses a different language, adapt the file extension (`index.py`, `mod.rs`, etc.). Ask only if ambiguous.

##### Architectural Decisions

For each non-obvious boundary decision, document:

```
**Decision:** [what was decided]
**Reason:** [why — which DDD or Modular Monolith rule drove it]
**Alternative considered:** [what else was possible and why it was rejected]
```

---

### Step 8: Offer File Creation

After presenting the report, ask:

> "Quer que eu crie a estrutura de diretórios no projeto? Posso gerar os diretórios, o `index.ts` (ou equivalente) de cada módulo, e um `CONTEXT.md` por módulo com o resumo acima."

If the user confirms:

1. Ask for the root src path if not obvious from the context (e.g., `src/`, `app/`, `lib/`).
2. Create `src/modules/<module-name>/` for each core/support module with the subdirectory structure above.
3. Create `src/integrations/<system>/` for each integration module.
4. Create `src/shared/events/` and `src/shared/types/`.
5. Inside each module, create `CONTEXT.md` with the module's section from the report (responsibility, ownership, communication).
6. Create `ARCHITECTURE.md` at the src root with the full Decomposition Report.

If the project has an existing directory structure that differs, adapt to it — do not overwrite or restructure existing code.

---

## Examples

### Example 1: Educational Platform

**User says:** "Schools buy license pools for students to access courses. We integrate with HubSpot for CRM and Moodle for course delivery. There are pricing tiers and contract amendments."

**Actions:**

1. Bounded Contexts identified: `licenses`, `students`, `billing`, `contracts`, `auth`, `notifications`, `audit`
2. Data ownership: `LicensePool` + `StudentLicense` → `licenses`; `PricingRange` → `billing`; `ContractAmendment` → `contracts`
3. Integrations: `integrations/hubspot`, `integrations/moodle`
4. Cross-module: `licenses` emits `license.expired` event → `notifications` consumes async; `students` reads identity from `auth` via sync facade
5. Core: `licenses`, `billing`, `contracts`, `students` — Support: `auth`, `notifications`, `audit`
6. Directory structure generated with 7 module dirs + 2 integration dirs
7. User confirms file creation → `CONTEXT.md` per module + `ARCHITECTURE.md` at root

### Example 2: E-commerce System

**User says:** "Orders, products, inventory, users, payments via Stripe, email notifications."

**Actions:**

1. Contexts: `orders`, `products`, `inventory`, `payments`, `auth`, `notifications`
2. Data ownership: all entities cleanly separated; `orders` owns `OrderItem` (not `products`)
3. Integration: `integrations/stripe`, `integrations/email-provider`
4. Cross-module: `orders` → checks stock via sync facade on `inventory`; `orders` → emits `order.placed` → `notifications` async; `payments` → emits `payment.confirmed` → `orders` async
5. Core: `orders`, `products`, `inventory`, `payments` — Support: `auth`, `notifications`
6. Decision documented: `OrderItem` stays in `orders` (not `products`) because its lifecycle is owned by the order, not the product catalog

---

## Troubleshooting

### Problem: Input is too vague

Ask: "Pode descrever as entidades principais, os fluxos de negócio, ou quais dados o sistema gerencia? Um parágrafo é suficiente para começar."

### Problem: Entity ownership is ambiguous

Apply this tiebreaker: **who creates this data, and who is accountable when it's wrong?** That functional owner becomes the module owner.

If two modules both "need" full ownership, it's a sign the entity should be split (e.g., `order-summary` in `reporting` vs full `Order` in `orders`).

### Problem: User wants microservices

Respond: "This skill is optimized for Modular Monolith decomposition where all modules share a single deployable. For microservices, the boundary rules are similar but each module becomes an independent service with its own DB. Want me to proceed with Modular Monolith and annotate which modules are natural candidates for future service extraction?"

### Problem: User has an existing codebase, not a PRD

Accept any input: existing code structure, README, architecture diagram description, or free-form explanation. Apply Steps 2–7 as-is. In Step 8, check the existing directory structure before creating files and offer to migrate rather than create from scratch.
