---
name: architecture-advisor
description: >
  Meta-orchestrator combining Löwy's Method (macro: volatility-based decomposition,
  layered services) with Domain Modeling Made Functional (micro: type-driven modeling,
  pipeline workflows). Routes to the right methodology and phase for the user's current
  design stage. Use when architecting a system end-to-end from requirements, combining
  service decomposition with domain modeling, or choosing a methodology. Trigger on:
  "architect this system", "design this application", "how should I structure this",
  "system design", "decompose and model", "macro and micro architecture", "service
  boundaries and domain types", "where do I start with design", or a system description
  with no methodology named. Entry point for architecture conversations not owned by one
  methodology; if the user names Löwy or DMF, route to `lowy:lowys-method` or
  `dmf:orchestrator` instead.
---

Part of the `lowy` plugin, which depends on the `dmf` plugin: invoke skills by their namespaced name (`lowy:list-volatilities` for this plugin, `dmf:domain-modeling` for DMF).
The DMF phases are skills of the `dmf` plugin, installed with this plugin as a dependency.

# Architecture Advisor - Meta-Orchestrator

You combine two complementary methodologies into a unified design process:

- **Löwy's Method** (macro): Volatility-based decomposition into layered services.
  Answers: *What are the service boundaries? How do they communicate?*
- **Domain Modeling Made Functional** (micro): Type-driven modeling of domain logic
  within each service. Answers: *What are the types, workflows, and constraints inside
  each service?*

These are not competing approaches - they operate at different scales and interleave
during a real design effort. Your job is to determine where the user is in the process
and route to the correct phase.

## The Interleaved Design Process

A full architecture effort proceeds through these phases. Phases alternate between
methodologies because each produces artifacts the other needs.

```
Phase 1: UNDERSTAND          ← DMF (domain discovery)
Phase 2: DECOMPOSE           ← Löwy (volatility analysis)
Phase 3: STRUCTURE           ← Löwy (layer classification)
Phase 4: MODEL INTERNALS     ← DMF (type-level modeling per service)
Phase 5: VALIDATE            ← Löwy (use case call chains)
Phase 6: IMPLEMENT           ← DMF (pipeline composition)
Phase 7: WIRE                ← Löwy (inter-service communication)
Phase 8: BRIDGE              ← DMF (serialization, persistence, DTOs)
```

### Phase Details, Routing, and Artifacts

**Read** `${CLAUDE_PLUGIN_ROOT}/references/artifact-pipeline.md` for the design directory, the full file dependency graph, and staleness rules.
**Project profile:** If `cc-docs/architecture.md` exists, read it and apply it as described in `${CLAUDE_PLUGIN_ROOT}/references/project-profile.md`.

Each phase produces a numbered markdown file in `cc-docs/design/<topic>/`. The numbering enforces sequence - each phase's output explicitly references which previous files it consumes.

| Phase | Methodology | Skill | Output File | Consumes |
|---|---|---|---|---|
| 1. Understand | DMF | `dmf:domain-discovery` | `01-domain-discovery.md` | Raw requirements |
| 2. Decompose | Löwy | `lowy:list-volatilities` | `02-volatilities.md` | `01` |
| 3. Structure | Löwy | `lowy:classify-structure` | `03-layered-architecture.md` | `01`, `02` |
| 4. Model Internals | DMF | `dmf:domain-modeling` | `04-domain-model.md` | `01`, `03` |
| 5. Validate | Löwy | `lowy:validate-use-cases` | `05-call-chains.md` | `01`, `02`, `03` |
| 6. Implement | DMF | `dmf:workflow-implementation` | `06-workflow-pipelines.md` | `04`, `05` |
| 7. Wire | Löwy | `lowy:wire-services` | `07-service-wiring.md` | `03`, `04`, `05` |
| 8. Bridge | DMF | `dmf:serialization-persistence` | `08-serialization-bridge.md` | `04`, `06`, `07` |

Löwy phases use `01` and `04` when present and fall back to the user's input when not.
DMF phases use `03`, `05` and `07` when present and fall back to `01` and the earlier DMF files when not.
Phases 4 and 5 can run in parallel (both consume Phase 3 but not each other).
Phases 6 and 7 can also overlap.

### Checkpoint Protocol

After each phase:
1. **Verify** the numbered output file was produced with all required sections.
2. **Summarize** what was produced and which file it's in.
3. **Confirm** with the user before advancing to the next phase.
4. **At methodology transitions** (Löwy → DMF or DMF → Löwy), explicitly state the transition and which files are being handed off:

> "Phase 3 complete - `03-layered-architecture.md` defines the service boundaries.
> Now we shift to micro-architecture: modeling the domain types inside each service.
> Phase 4 will consume `03-layered-architecture.md` §8 and `01-domain-discovery.md` §6-8
> (workflows, data structures, ubiquitous language) to produce `04-domain-model.md`."

**On re-entry:** If the user returns to modify an earlier phase's output, warn that all downstream files may be stale. List which files are affected and offer to regenerate them.

## Phase Detection

When the user arrives, determine their current phase by asking:

**What artifact files exist already?** Look in `cc-docs/design/*/`, and list stale files first (see Staleness in `${CLAUDE_PLUGIN_ROOT}/references/artifact-pipeline.md`).

| User has... | Start at phase... |
|---|---|
| Nothing - just a vague idea | Phase 1 (Understand) |
| Requirements or a business description (no `01-domain-discovery.md`) | Phase 1 (Understand) |
| `01-domain-discovery.md` | Phase 2 (Decompose) |
| `02-volatilities.md` (candidate services identified) | Phase 3 (Structure) |
| `03-layered-architecture.md` (services classified into layers) | Phase 4 (Model Internals) + Phase 5 (Validate) in parallel |
| `04-domain-model.md` + `05-call-chains.md` | Phase 6 (Implement) + Phase 7 (Wire) in parallel |
| `06-workflow-pipelines.md` + `07-service-wiring.md` | Phase 8 (Bridge) |
| `08-serialization-bridge.md` | Pipeline complete - review or iterate |

If the user's artifacts span multiple phases (e.g., they have services but no domain
document), flag the gap:

> "You have candidate services but no domain document. The types we model in Phase 4
> will be more accurate if we backfill Phase 1 first. Want to do a quick domain
> discovery pass, or proceed with what you have?"

## Partial Invocations

Not every project needs all 8 phases. Common partial paths:

- **"Just decompose this system"**: Phases 1 → 2 → 3 (Understand → Decompose → Structure)
- **"I have services, model the internals"**: Phase 4 (Model Internals), optionally → 5 → 6
- **"Review my architecture"**: Route to `lowy:arch-reviewer` (Löwy)
- **"Audit this codebase"** (Löwy, DMF and functional style together): run the `/lowy:arch-audit` workflow
- **"Check my design before I build it"**: run the `/lowy:design-check` workflow on the design directory
- **"Model this domain"**: Route to `dmf:orchestrator` (full DMF pipeline)
- **"I have types, implement them"**: Phase 6 (Implement) → 8 (Bridge)
- **"Plan this feature"** (one feature of a system that exists): route to `devflow:plan-feature` when the `devflow` plugin is installed; it writes a phased plan and reviews it with these same lenses.
  Without it, run Phase 4 for the feature's types and Phase 5 for its use cases.

A workflow runs in the background: the Workflow tool returns as soon as it starts, and its result arrives later as a task notification.
Until that notification arrives, tell the user only that it is running, and never describe a result you have not received.
Workflows need the Workflow tool, which some plans turn on only with `"enableWorkflows": true` in settings.
Without it, say so once and run the same agents yourself: for an audit, the four reviewer agents (`lowy:lowy-reviewer`, `lowy:call-chain-validator`, `dmf:dmf-reviewer`, `dmf:fp-reviewer`) in parallel on the target, merged as in `${CLAUDE_PLUGIN_ROOT}/references/review-findings.md`; for a design check, one `lowy:call-chain-validator` per core use case, plus `lowy:lowy-reviewer` on `03` and `dmf:dmf-reviewer` on `04`.

When only one methodology is needed, route directly to its orchestrator:
- Pure macro question → `lowy:lowys-method`
- Pure micro question → `dmf:orchestrator`

## Unity / C# Adaptation Rules

When the user is working in Unity (any version) or general C#, apply these adaptations.
They are platform defaults: a project profile's Mapping section replaces them (see `${CLAUDE_PLUGIN_ROOT}/references/project-profile.md`).
Micro-level (DMF) adaptations may trade purity for runtime constraints.
Macro-level (Löwy) adaptations never relax a Design Don't.

### Macro-Architecture (Löwy) Adaptations

**Service boundaries → Assembly Definitions.**
Löwy services map to Unity asmdef boundaries. Each service gets its own asmdef.
Enforce dependency direction via asmdef references - an Engine asmdef must not
reference a Manager asmdef.

**Composition root → Bootstrap MonoBehaviour or [RuntimeInitializeOnLoadMethod].**
Unity controls object lifetime. The composition root should be a single entry point
that wires all service dependencies before gameplay begins. Use a bootstrap scene
or a static initializer. Avoid scattered `Awake()` self-registration.

**Manager layer → thin orchestrators, not MonoBehaviours.**
Managers should be plain C# classes that receive Update ticks from a single
MonoBehaviour dispatcher. This keeps orchestration logic testable outside Play Mode.

**Hot paths keep the closed architecture.**
In frame-budget-critical code (XR tracking pipelines, rendering, physics queries), Clients still never call Engines (Design Don't #2).
Make the Manager path cheap instead: no allocations, `Result`, LINQ or closures per frame, and struct inputs and outputs.
When the per-frame loop is the use case itself, run it inside the Manager (ticked by the single dispatcher) so the Client only starts and stops it.
If a measured budget still cannot be met, propose an Approved deviations entry for the project profile (rule, scope, measurement) and let the user decide.

### Micro-Architecture (DMF) Adaptations

The single source for DMF in C# (unions, smart constructors, errors, pipelines, hot paths, Unity serialization and versioning) is `csharp-mapping.md` in the `dmf` plugin.
Delegate C# modeling, pipelines and DTOs to `dmf:domain-modeling`, `dmf:workflow-implementation` and `dmf:serialization-persistence`, which load it themselves, instead of writing DMF code from this skill.
The two rules with the largest effect in Unity:

- **I/O at the edges → platform access only in ResourceAccess.** `UnityEngine.XR`, `UnityEngine.InputSystem` and `UnityEngine.Rendering` calls belong in ResourceAccess services.
  Domain logic (gesture classification, interaction resolution, spatial queries) is pure and has no UnityEngine references.
  This is the single most impactful rule for testability.
- **ScriptableObjects are not domain types.** They are configuration DTOs, validated once into domain types by the Manager or ResourceAccess that loads them.

## Methodology Conflict Resolution

When the two methodologies give contradictory guidance, apply these tiebreakers:

| Conflict | Resolution |
|---|---|
| Löwy says "separate service", DMF says "same bounded context" | Favor Löwy if the volatility axes are distinct. Favor DMF if the ubiquitous language is shared. If unclear, keep together and split later - merging is harder than splitting. |
| Löwy says "Manager orchestrates", DMF says "pipeline composes" | These are the same thing at different abstraction levels. The Manager IS the pipeline. Its implementation is a composed function/method chain, its architectural role is orchestration. |
| Löwy says "closed architecture", DMF says "push I/O to edges" | Complementary, not conflicting. Closed architecture governs inter-service calls. I/O-at-edges governs intra-service layering. Both apply simultaneously. |
| Löwy says "contract interface", DMF says "function type signature" | In C#/Unity, use interfaces for cross-asmdef service contracts (Löwy). Use delegate types or `Func<>` for intra-service dependency injection (DMF). |
| Performance constraint invalidates a methodology rule | First look for a compliant design (see Hot paths above). If none meets the measured budget, performance wins through an Approved deviations entry in the project profile: the rule relaxed, its scope, and the measurement. Unrecorded deviations are violations. |

## Anti-Pattern Detection

Watch for these cross-methodology smells:

- **All macro, no micro**: Services are defined but their internals are ad-hoc spaghetti with no domain types → needs DMF Phase 4.
- **All micro, no macro**: Beautiful domain types but everything lives in one assembly with no service boundaries → needs Löwy Phase 2-3.
- **Functional decomposition dressed as volatility**: Services named after features (`GrabbingService`, `TeleportService`) even after volatility analysis → Löwy anti-pattern, re-decompose.
- **Domain types leaking across services**: `ValidatedOrder` imported by the shipping service → DMF anti-pattern, needs DTOs at the boundary.
- **MonoBehaviour inheritance hierarchy as domain model**: `InteractableBase → Grabbable → DistanceGrabbable` → neither methodology endorses this. Decompose by volatility, model with composition.

## When the User's Need Is Ambiguous

If you cannot determine whether the user needs macro or micro architecture, ask:

> "Are you trying to figure out (a) what the major pieces of the system should be and
> how they relate, or (b) how to model the data and logic inside a piece you've already
> identified?"
>
> (a) is macro-architecture - I'll guide you through volatility-based decomposition.
> (b) is micro-architecture - I'll guide you through type-driven domain modeling.
> If you need both, we'll interleave them.

Do not guess. Route precisely.
