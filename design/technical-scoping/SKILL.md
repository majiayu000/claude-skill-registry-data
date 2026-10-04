---
name: technical-scoping
description: >
  Transforms a macro-scoping document into a complete technical specification: API contracts,
  data model, security, idempotency, rollout strategy, and observability plan.
  Use this skill whenever a user has a macro-scoping document and needs to go technical, or mentions
  API contracts, data model design, NestJS architecture, Keycloak roles, job/cron design,
  migration strategy, or asks "comment on implémente ça ?", "on passe au technique",
  "cadrage micro", "spec technique", "définition technique".
  Always trigger after a macro-scoping document has been produced.
---

## Purpose

Turn a macro-scoping document into a complete technical specification that developers can
execute without ambiguity. After this document, the ticket breakdown should be trivial.

## Inputs to collect

Before producing the document, make sure you have:

- The macro-scoping document (or a clear summary of the feature)
- Non-functional constraints (SLA, security requirements, expected volumes)
- The CIDF ticket number (`CIDF-XXXX`) — the tracking ticket on the **CIDF board** (board de cadrage, accessible au TL, CTO et client).
  It is usually present in the macro-scoping document. If not, ask the user for it or mark it as "à créer".

**Deadline is NOT an input.** Never ask for or mention a deadline in the technical specification.
Deadlines are produced by the ticket breakdown / chiffrage phase that follows.

### Mandatory — ask before writing

Never produce the technical specification from the macro-scoping document alone.
Before starting Step 1, ask the user:

- Are there known non-functional constraints not covered in the macro-scoping?
  (expected volumes, SLA, specific security requirements)
- Are there architectural decisions already made that constrain the solution?
  (specific library, existing pattern to follow, forbidden approach)
- Are there any open questions from the macro-scoping that must be resolved before
  technical design can begin?

Only proceed once these questions have been answered or explicitly deferred.

## Step 1 — Explore the repository

Before writing anything, explore the repository to identify impacted components.

Search through:

- `apps/` — identify relevant applications (API, frontend, jobs, runners, IDP, keycloak-import)
- `libs/` — identify relevant libraries (databases, grants, young, partners, wallets, agents,
  offers, taxonomies, processes, etc.)

For each potentially impacted component, note:

- Its current role in the architecture
- Why it is likely affected by this feature

**Present the detected scope to the user and wait for their explicit validation before proceeding.**

Use this exact format when presenting:

```
## Périmètre détecté

| Composant | Chemin | Raison probable |
|-----------|--------|-----------------|
| ...       | ...    | ...             |

Est-ce que ce périmètre te semble correct ? Des composants à ajouter ou retirer avant que je continue ?
```

Do not proceed to Step 2 until the user confirms.

## Step 2 — Produce the technical specification

Once the scope is validated, read `assets/template.md` and produce the full specification in French.

**Section-specific guidance:**

- **Répartition des responsabilités**: use a table. Be strict and explicit about what each
  component does NOT do. This prevents responsibility bleed during implementation.

- **Stratégie d'idempotence**: always answer — what happens if the job runs twice? If it crashes
  mid-run? If the cron fires simultaneously on two pods?

- **Gestion des erreurs**: distinguish technical failures (network, timeout, DB) from business
  failures (entity not found, rule violation). Define retry strategy for each.

- **Options techniques**: if there are meaningful architectural choices, present 1–2 options
  with explicit trade-offs and a clear decision. Write a short ADR if the decision is
  structurally significant for the codebase.

- **Stratégie de migration**: always separate migration from feature. A migration is not the feature.

- **Questions ouvertes**: never skip this section. Surface all remaining uncertainties, even minor ones.

## Output format

Produce the document in French using `assets/template.md`. No ticket breakdown here — just the plan.

## Golden rules

- No exhaustive Jira breakdown — just the architectural and technical plan.
- After reading this document, developers must know exactly where to put the code.
- Responsibilities must be unambiguous — no grey zones.
- Risks and uncertainties must be explicit.
- After this document, ticket estimation should be reliable.
