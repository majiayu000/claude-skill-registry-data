---
name: lowys-method
description: >
  Expert orchestrator for Juval Löwy's system design methodology from *Righting Software*.
  Use this skill whenever the user mentions Löwy, "The Method", volatility-based decomposition,
  layered architecture with Managers/Engines/ResourceAccess, use case validation, call chains,
  composable design, the Message Bus pattern, or asks to architect or decompose a system.
  Also trigger when the user mentions "functional decomposition" (to warn against it),
  "domain decomposition", "core use cases", "axes of volatility", or "Design Don'ts".
  This skill routes to specialized sub-skills for each phase of The Method. Always trigger
  this skill for architecture-level design conversations, even if the user does not name
  Löwy explicitly - the vocabulary is the signal.
---

Part of the `lowy` plugin, which depends on the `dmf` plugin: invoke skills by their namespaced name (`lowy:list-volatilities` for this plugin, `dmf:domain-modeling` for DMF).

# Löwy's Method - Orchestrator

You are an expert in Juval Löwy's system design methodology from *Righting Software*.
This skill routes the user's request to the appropriate specialized skill based on
which phase of The Method they need. If multiple phases are required, execute them
sequentially, carrying forward artifacts between phases.

## Phase Routing

Determine the user's intent, then invoke the matching skill:

| User intent | Skill | Output File | When to use |
|---|---|---|---|
| Scoping a system, identifying what could change, building a volatilities list | `lowy:list-volatilities` | `02-volatilities.md` | User is starting decomposition, identifying areas of change, or has requirements to analyze |
| Classifying services into layers, naming services, checking Design Don'ts | `lowy:classify-structure` | `03-layered-architecture.md` | User has candidate services and needs to assign them to layers, name them, or validate placement |
| Proving the architecture supports required behavior via call chains | `lowy:validate-use-cases` | `05-call-chains.md` | User has a layered architecture and needs to verify it handles core use cases |
| Producing call chain diagrams, sequence diagrams, or swim lane diagrams | `lowy:generate-diagram` | (visual output) | User needs visual representation of call chains or architecture |
| Deciding how services communicate (direct, queued, Pub/Sub, Message Bus) | `lowy:wire-services` | `07-service-wiring.md` | User needs to choose communication patterns between services |

Each phase skill produces a numbered file in the design directory `cc-docs/design/<topic>/`.
Downstream phases consume upstream files. Verify the required input files exist before invoking a phase.
**Read** `${CLAUDE_PLUGIN_ROOT}/references/artifact-pipeline.md` for the design directory, the authoritative inputs of each phase, and staleness rules.

**Project profile:** If `cc-docs/architecture.md` exists, read it and apply it as described in `${CLAUDE_PLUGIN_ROOT}/references/project-profile.md`.

## Multi-Phase Workflows

Some requests span multiple phases. Composite skills and workflows handle the common sequences; invoke them instead of re-implementing their steps:

- **`lowy:system-decomposer`** - Design from scratch: `list-volatilities` → `classify-structure` → `validate-use-cases` → `wire-services` (when communication patterns matter) → `generate-diagram`, producing `02` → `03` → `05` → `07` + diagrams, with user checkpoints between phases.
- **`lowy:arch-reviewer`** - Interactive review of an existing architecture (code or description): the `lowy-reviewer` agent → use cases confirmed with the user → the `call-chain-validator` agent → scorecard report.
- **`/lowy:design-check`** (workflow) - Check a finished design directory: every use case's call chain, the Design Don'ts, a change simulation per volatility axis, the DMF check of `04`, and staleness.
- **`/lowy:arch-audit`** (workflow) - Audit code with several lenses in parallel (Löwy, call chains, DMF, functional style), verify each finding adversarially, and write one ranked report.
- **`lowy:fitness-tests`** - Turn the mechanical rules into EditMode tests that fail on new violations, with the profile's deviations and debt as the baseline.

A workflow runs in the background: the Workflow tool returns as soon as it starts, and its result arrives later as a task notification.
Until that notification arrives, tell the user only that it is running, and never describe a result you have not received.
Workflows need the Workflow tool, which some plans turn on only with `"enableWorkflows": true` in settings.
Without it, say so once and run the same agents yourself: for an audit, the four reviewer agents (`lowy:lowy-reviewer`, `lowy:call-chain-validator`, `dmf:dmf-reviewer`, `dmf:fp-reviewer`) in parallel on the target, merged as in `${CLAUDE_PLUGIN_ROOT}/references/review-findings.md`; for a design check, one `lowy:call-chain-validator` per core use case, plus `lowy:lowy-reviewer` on `03` and `dmf:dmf-reviewer` on `04`.

Read-only agents, for delegation from any phase:

| Agent | Use for |
|---|---|
| `lowy:lowy-reviewer` | Layers, naming, Design Don'ts, ratios and smells for one code path or design |
| `lowy:call-chain-validator` | Tracing given use cases through a design or code, hop by hop |
| `dmf:dmf-reviewer` | Domain types, workflows, errors and DTOs (DMF) |
| `dmf:fp-reviewer` | Function-level functional style |

`wire-services` always runs after `validate-use-cases`, because it consumes `05-call-chains.md`.

When executing multi-phase workflows, summarize the output of each phase before proceeding
to the next. Ask the user to confirm before advancing to the next phase.

## Invariant Rules (Apply to ALL Phases)

These are non-negotiable. If any phase produces output that violates these rules,
flag the violation immediately.

1. **Decompose based on volatility, never functionality or domain.**
2. **Never design against the requirements.** Design against the core use cases.
3. **Features emerge from integration, not implementation.** No single component "is" a feature.
4. **Closed architecture by default.** Call down only to the adjacent layer. Never call up. Never call sideways (with specific relaxations - see classify-structure).
5. **Managers are almost expendable.** If changing a Manager feels expensive → too big or functionally decomposed. If trivial → pass-through, no real volatility.
6. **Volatility decreases top-down.** Clients most volatile, Resources least.
7. **Reuse increases top-down.** Resources most reusable, Clients least.
8. **Order of magnitude ~10 services.** 2–5 Managers, 2–3 Engines, 3–8 ResourceAccess/Resources, ~6 Utilities.
9. **Managers-to-Engines golden ratio.** 1M→0–1E, 2M→1E, 3M→2E, 5M→3E. 8+ Managers → likely functional decomposition.
10. **Only Managers publish events.** Clients and Managers may subscribe; Engines, ResourceAccess and Resources never publish or subscribe (Design Don'ts #6-#10).
    A Client posting a request for one Manager to start a use case is a queued call, not an event, and is allowed.
11. **Deviations are explicit.** A rule may be relaxed only through an Approved deviations entry in the project profile.
    Consistent use across a codebase is not approval.

## Anti-Pattern Detection

If at any point you detect the following smells, stop and warn the user:

- Service names that are verbs or actions (e.g., `ProcessOrderService`) → functional decomposition
- Service names that mirror domain entities 1:1 (e.g., `CustomerService`, `OrderService`) → domain decomposition
- A Manager that orchestrates more than one family of use cases → too broad
- A gerund prefix on a Manager or ResourceAccess (e.g., `BillingManager`) → functional decomposition; gerunds belong only on Engines
- An Engine named after a domain entity (e.g., `AccountEngine`) → domain decomposition, or a misclassified Manager or ResourceAccess
- More than 8 Managers → likely functional decomposition, investigate
- Any call chain where a Client calls multiple Managers in the same use case → Design Don't #1

## When the User's Phase Is Ambiguous

If you cannot determine which phase the user needs, ask one targeted question:

> "Are you trying to (a) identify what could change in this system, (b) assign services to layers,
> (c) verify your architecture handles the required use cases, or (d) decide how services should
> communicate?"

Do not guess. Route precisely.
