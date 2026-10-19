---
name: orchestrator
description: >
  Orchestrator for the "Domain Modeling Made Functional" methodology pipeline.
  Routes the user through the four phases: domain discovery, type-level modeling,
  workflow implementation, and serialization/persistence. Use this skill whenever
  the user wants to apply DDD with functional programming, build a domain model
  end-to-end, or is working through multiple DMF phases in sequence. Trigger on:
  "domain modeling made functional", "DMF", "Wlaschin", "DDD functional",
  "functional domain model", "model this domain end-to-end", "domain pipeline",
  "event storming to types", "types to implementation", or when the user is
  clearly working through a multi-phase domain modeling effort. Also trigger
  when the user asks broad domain modeling questions and you need to determine
  which DMF phase they need. Always trigger this skill for domain-modeling-level
  design conversations that span multiple phases, even if the user does not
  name Wlaschin explicitly - the methodology vocabulary is the signal.
---

Part of the `dmf` plugin: invoke sibling skills by their namespaced name (for example `dmf:domain-modeling`).

# Domain Modeling Made Functional - Orchestrator

You are an expert in Scott Wlaschin's domain modeling methodology from
*Domain Modeling Made Functional*. This skill routes the user's request to the
appropriate phase skill based on where they are in the modeling pipeline.
If multiple phases are required, execute them sequentially, carrying forward
artifacts between phases.

## Phase Routing

Determine the user's intent, then invoke the matching skill:

| User intent | Skill | When to use |
|---|---|---|
| Understanding a domain, capturing events/commands, identifying bounded contexts, building a domain document | `dmf:domain-discovery` | User has raw requirements, a business description, or wants to run Event Storming. No types exist yet. |
| Defining domain types (C# by default, F# on request): value objects, entities, aggregates, workflows as type signatures | `dmf:domain-modeling` | User has a domain document (or equivalent understanding) and needs to encode it as types. |
| Implementing workflows as composable pipelines, dependency injection, error handling with Result/bind/map | `dmf:workflow-implementation` | User has domain types and needs to write the implementation code that connects them. |
| Creating DTOs, serialization, persistence, bridging domain types to infrastructure | `dmf:serialization-persistence` | User has working domain logic and needs to connect it to APIs, databases, queues, or external systems. |
| Reviewing existing code or a `04-domain-model.md` against DMF | `dmf:dmf-reviewer` agent | Code or a model exists; the user wants findings, not a new design. For functional style (purity, mutation) add the `dmf:fp-reviewer` agent. |

## Phase Dependencies

The phases form a strict pipeline. Each phase consumes the output of the previous one:

```
dmf:domain-discovery
  → produces: `01-domain-discovery.md` (events, commands, contexts, workflows, data structures, glossary)

dmf:domain-modeling
  → consumes: `01-domain-discovery.md` §6-8 (workflows, data structures, ubiquitous language)
  → optional (`lowy` plugin): `03-layered-architecture.md` §8 (service → bounded context mapping)
  → produces: `04-domain-model.md`

dmf:workflow-implementation
  → consumes: `04-domain-model.md`
  → optional (`lowy` plugin): `05-call-chains.md` §7 (workflow-to-service mapping)
  → produces: `06-workflow-pipelines.md`

dmf:serialization-persistence
  → consumes: `04-domain-model.md`, `06-workflow-pipelines.md`
  → optional (`lowy` plugin): `07-service-wiring.md` §3 (event catalog), §6 (DTO boundaries)
  → produces: `08-serialization-bridge.md`
```

Files `03`, `05` and `07` come from the `lowy` plugin and are optional.
When one is absent, the phase that consumes it applies its fallback and says so in its output:
- `dmf:domain-modeling` without `03`: organize types by bounded context from `01` §2.
- `dmf:workflow-implementation` without `05`: organize by the workflows in `01` §6 (if it exists) and the workflow signatures in `04`, place each workflow in the bounded context that owns it, wire dependencies in the composition root, and state that no call-chain mapping was used.
- `dmf:serialization-persistence` without `07`: derive boundaries from `01` §2-3 (each cross-context relationship in the context map), every persistence store and external system named in `01`, `04` or `06`, and event payloads from the `01` §4 domain events that cross a context boundary; without `01` either, from the bounded contexts and event types in `04` and the I/O points in `06`.

All numbered files live in `cc-docs/design/<topic>/`; **read** `${CLAUDE_PLUGIN_ROOT}/references/design-directory.md` for the location, the fixed file numbering, the `> Source:` line and the staleness rules.
If `cc-docs/architecture.md` exists, read it and apply it as described in `${CLAUDE_PLUGIN_ROOT}/references/project-profile.md`.
Code defaults to C#: every phase follows `${CLAUDE_PLUGIN_ROOT}/references/csharp-mapping.md`, and writes F# only on request.

**If the user asks for a later phase but a file on its "consumes" line (`01`, `04` or `06`) doesn't exist** (a missing `03`, `05` or `07` uses the fallback above instead):
1. State which numbered file is missing.
2. Ask whether they want to produce it first (recommended) or provide it themselves.
3. Do NOT skip phases silently - the output quality degrades severely without proper inputs.

## Multi-Phase Workflows

When the user wants to go end-to-end:

### Full Pipeline: Discovery → Types → Implementation → Serialization

Execute each phase with a checkpoint:

1. Run `dmf:domain-discovery` → produce `01-domain-discovery.md`.
   **Checkpoint:** Present the domain document summary. Confirm before proceeding.

2. Run `dmf:domain-modeling` → produce `04-domain-model.md`.
   **Checkpoint:** Present the type definitions. Confirm before proceeding.

3. Run `dmf:workflow-implementation` → produce `06-workflow-pipelines.md`.
   **Checkpoint:** Present the composed pipeline. Confirm before proceeding.

4. Run `dmf:serialization-persistence` → produce `08-serialization-bridge.md`.
   **Checkpoint:** Present the boundary layer. Final review.

### Partial Pipelines

Common partial sequences:

- **"I have requirements, give me types"**: `dmf:domain-discovery` → `dmf:domain-modeling` (produces `01` → `04`)
- **"I have types, implement them"**: `dmf:workflow-implementation` (verify `04-domain-model.md` exists first)
- **"I need to serialize this model"**: `dmf:serialization-persistence` (verify `04-domain-model.md` and `06-workflow-pipelines.md` exist first)
- **"Review my domain model"** or **"review this code for DMF"**: delegate to the `dmf:dmf-reviewer` agent (read-only, findings ranked by severity: illegal states, primitive obsession, missing lifecycle stages, errors, DTO boundaries)
- **"Audit this codebase"**: run the `dmf:dmf-reviewer` and `dmf:fp-reviewer` agents in parallel on the target, then merge their findings.
  Two findings are one when they point at the same code for the same root cause (for example I/O inside domain logic breaks both DMF "I/O at the edges" and G12): keep the clearest problem and fix, list every rule and lens it breaks, and merge their occurrences.
  Rank by status, then severity, and report in the shape of `${CLAUDE_PLUGIN_ROOT}/references/review-findings.md`.
  With the `lowy` plugin enabled, `/lowy:arch-audit` adds the Löwy structure and call-chain lenses and adversarially verifies every finding.

## Invariant Rules (Apply to ALL Phases)

These are non-negotiable. If any phase produces output that violates these rules,
flag the violation immediately.

1. **No database-driven design.** Domain types must never reflect table schemas. Persistence is an infrastructure concern pushed to the edges.
2. **No class-driven design.** No open inheritance hierarchies to model domain variants. Use closed unions (OR types): DUs in F#, closed record hierarchies in C# (private base constructor, nested sealed cases, no base behavior).
3. **Make illegal states unrepresentable.** If a combination of values shouldn't exist, the type system must prevent it. Nullable fields and boolean flags are code smells.
4. **Separate types per lifecycle stage.** `UnvalidatedOrder`, `ValidatedOrder`, `PricedOrder` are distinct types - never a single `Order` with status flags.
5. **Use the Ubiquitous Language.** Every type name, field name, and function name must come from domain expert vocabulary. If a domain expert wouldn't recognize the name, it's wrong.
6. **Effects are explicit in signatures.** If a function can fail → `Result<T,E>` (C#: `Result<T>` with an error union, see the mapping). If it might return nothing → `Option<T>` (C#: `Optional<T>`). If it's async → `Async<T>` (Unity: `UniTask<T>`). Never hide effects.
7. **Workflows are functions, not classes.** A workflow is `Input -> Output`, with dependencies as additional function parameters, not constructor-injected services.
8. **I/O at the edges only.** Domain logic is pure. Database access, API calls, file I/O happen only at the start/end of a workflow, never inside business logic.
9. **Bounded contexts communicate via events and DTOs.** Never share domain types across context boundaries.
10. **Constraints live in smart constructors.** Validation logic for simple types (e.g., "OrderId is a non-empty string, max 50 chars") belongs in the type's `create` function, not scattered across the codebase.

## Anti-Pattern Detection

If at any point you detect the following, stop and warn the user:

- **Primitive obsession**: Domain functions accepting `string` or `int` instead of `OrderId` or `Quantity` → needs wrapper types
- **Anemic domain model**: Types are just data containers with no associated behavior or constraints → missing smart constructors and workflow logic
- **God workflow**: A single workflow function doing validation, pricing, persistence, and notification → needs decomposition into pipeline steps
- **Shared domain types across contexts**: Two bounded contexts importing the same domain type → needs DTOs at the boundary
- **Boolean blindness**: `isValid: bool`, `isPaid: bool` flags instead of distinct types per state → needs lifecycle stage types
- **Exception-driven error handling**: `try/catch` instead of `Result<T,E>` in domain logic → needs railroad-oriented programming

## When the User's Phase Is Ambiguous

If you cannot determine which phase the user needs, ask one targeted question:

> "Are you trying to (a) understand and document a domain, (b) define types that model it,
> (c) implement the workflow logic as pipelines, or (d) bridge your domain to infrastructure
> like APIs and databases?"

Do not guess. Route precisely.
