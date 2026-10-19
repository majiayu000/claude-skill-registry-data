---
name: classify-structure
description: >
  Classify services into Löwy's architectural layers (Client, Manager, Engine, ResourceAccess,
  Resource, Utility) and validate naming conventions. Use when the user needs to determine which
  layer a service belongs to, apply the Four Questions (who/what/how/where), name services using
  the two-part naming convention, check the Design Don'ts list, or validate that a proposed
  architecture follows closed-architecture rules. Trigger on: "which layer", "Manager or Engine",
  "is this a Utility", "naming convention", "Design Don'ts", "closed architecture", "cappuccino
  machine test", "Four Questions", "almost expendable", "Managers-to-Engines ratio", or any
  request to review or classify components in a layered architecture.
---

# Layer Classification & Structure

**Read** `${CLAUDE_PLUGIN_ROOT}/references/structure.md` before classifying.
If `cc-docs/architecture.md` exists, read it and apply it as described in `${CLAUDE_PLUGIN_ROOT}/references/project-profile.md`.

You are helping the user assign services to the correct architectural layer
and validate that the resulting structure follows The Method's constraints.

## The Four Layers + Utilities Bar

```
┌─────────────────────────────────────────┐  ┌────────────┐
│  CLIENT LAYER          (Who)            │  │            │
├─────────────────────────────────────────┤  │ UTILITIES  │
│  MANAGERS              (What)           │  │ (vertical) │
│  ENGINES               (How-business)   │  │            │
├─────────────────────────────────────────┤  │ Security   │
│  RESOURCE ACCESS       (How-access)     │  │ Logging    │
├─────────────────────────────────────────┤  │ Pub/Sub    │
│  RESOURCES             (Where)          │  │ Hosting    │
└─────────────────────────────────────────┘  └────────────┘
```

## Workflow

### Step 1: Apply the Four Questions
For each candidate service, ask:

| Question | Layer | Test |
|---|---|---|
| **Who** interacts with the system? | Client | Is this a consumer - UI, API, timer, external system? |
| **What** behavior does the system provide? | Manager | Does this orchestrate a family of use cases? |
| **How** does the system perform business activities? | Engine | Is this an interchangeable strategy - calculation, search, validation, transformation? |
| **How** does the system access resources? | ResourceAccess | Does this expose atomic business verbs (Credit, Debit, Transfer) for a resource? |
| **Where** does state reside? | Resource | Is this a database, file system, cache, external system? |

If a service answers multiple questions, investigate - it may need to be split.

### Step 2: Apply Naming Conventions

| Type | Suffix | Prefix rule | Examples |
|---|---|---|---|
| Manager | `Manager` | Noun = encapsulated use case volatility | `AccountManager`, `MembershipManager` |
| Engine | `Engine` | Noun for the activity performed; gerunds allowed here and only here | `CalculatingEngine`, `SearchEngine`, `RegulationsEngine` |
| ResourceAccess | `Access` | Noun = associated resource/data | `MembersAccess`, `PaymentsAccess` |

**Red flags in names:**
- Gerund prefix on a Manager or ResourceAccess → functional decomposition smell
- Verb prefix on anything → functional decomposition smell
- Domain entity as prefix on an Engine → domain decomposition smell

### Step 3: Validate Structure Constraints

**Closed architecture rules (default):**
- Call DOWN to adjacent layer only
- NEVER call up
- NEVER call sideways within same layer

**Permitted relaxations:**
- Utilities are cross-cutting - any component may call any Utility
- Managers may call ResourceAccess directly (skipping Engines when no Engine is needed)
- Managers may call Engines (orthogonal plane, not truly sideways)
- Managers may queue calls to other Managers (goes through queue → ResourceAccess → queue listener Client → receiving Manager)
- A Manager must not queue to more than one other Manager in the same use case

### Step 4: Run the Design Don'ts Checklist
See `${CLAUDE_PLUGIN_ROOT}/references/structure.md` §8 for the full list. Key violations to check:

1. Client calls multiple Managers in same use case
2. Client calls Engines directly
3. Manager queues to >1 Manager in same use case
4. Engines receive queued calls
5. ResourceAccess receives queued calls
6. Clients publish system events
7. Engines publish events
8. ResourceAccess publishes events
9. Resources publish events
10. Engines/ResourceAccess/Resources subscribe to events
11. Engine calls another Engine
12. ResourceAccess calls another ResourceAccess

### Step 5: Validate Ratios and Expendability

- **Count check:** 2–5 Managers, 2–3 Engines, 3–8 RA/Resources, ~6 Utilities
- **Golden ratio:** 1M→0–1E, 2M→1E, 3M→2E, 5M→3E, 8+M → suspect
- **Expendability test for each Manager:** Would changing this Manager require significant rework of Engines or Resources? If yes → Manager is too coupled, likely doing too much
- **Utility classification:** If any component is proposed as a Utility, **read `references/utility-definition.md`** and apply the decision flowchart. Key distinctions: a Utility must be a *service* (not a library), must encapsulate infrastructure volatility, and must pass the cappuccino machine test. Functional libraries (`Result<T>`, extension methods, guard clauses) are NOT Utilities - they are shared code dependencies with no architectural standing.

### Step 6: Check for Subsystem Need
See `${CLAUDE_PLUGIN_ROOT}/references/structure.md` §9:
1. Exhaust flat decomposition first
2. If service count exceeds ~24 building blocks, partition into subsystems
3. Limit Managers per subsystem to three
4. Each subsystem must deliver independent business value

## Output Format

**Read** `references/output-template.md` and follow the template exactly.

Save the output as **`03-layered-architecture.md`** in the design directory `cc-docs/design/<topic>/` (see `${CLAUDE_PLUGIN_ROOT}/references/artifact-pipeline.md` for choosing `<topic>`).

**Input file:** `02-volatilities.md` §5 (candidate services) + §2 (core use cases). Also reference `01-domain-discovery.md` for bounded context mapping.
If `01-domain-discovery.md` does not exist, write `TBD (no 01)` in the §8 Bounded Context(s) column and say so.

**Output file:** `03-layered-architecture.md` - consumed by Phase 4 (`dmf:domain-modeling`), Phase 5 (`validate-use-cases`), and Phase 7 (`wire-services`).

Produce the complete document per the template: layer diagram, classification table, naming validation, ratio validation, Design Don'ts checklist, closed architecture rules, subsystem assessment, and service→bounded context mapping.

Flag any Design Don't violations or naming issues.
