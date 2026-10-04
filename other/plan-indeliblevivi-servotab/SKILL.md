---
name: plan
description: "Create an implementation plan sized to settled work. Use when a multi-step change benefits from sequencing, file targets, and explicit verification."
---

# Plan

Create a plan that helps implementation, review, and recovery. Avoid plans that are longer than the work or split one coherent change into dozens of mechanical steps.

## Inputs

Before planning, establish:

- The requested outcome and acceptance criteria
- Relevant repository instructions
- Current implementation and nearby patterns
- Known constraints or decisions
- Verification commands or test locations

Inspect enough code to name realistic touchpoints. Do not invent exact file paths when the repository does not support them.

## Preserve the requested outcome

- Plan the complete usable outcome the user asked for, including necessary end-to-end integration, states, and verification.
- Treat `MVP`, prototype, proof of concept, scaffold, or partial slice as scope choices that require the user or governing specification to make them explicit.
- Use the least complex implementation that covers the full contract. Do not use “minimal” to drop behavior, integrations, or acceptance criteria.
- Order work by real dependencies. Preserve the user's or specification's sequence when it expresses product meaning; record and explain any necessary reorder instead of silently optimizing for the easiest first slice.

## Approved specifications

When an approved specification governs the work:

- Treat it as the authority for scope, settled semantics, and acceptance.
- When planning the full specification, cover its complete accepted scope, even when execution will span phases, PRs, or sessions.
- Keep the current phase or tranche inside that full plan. Never present a partial tranche as the implementation plan for the specification.
- In that full plan, map every normative requirement to a slice and verification outcome, and state every proposed scope or order delta explicitly.
- If the user explicitly requests only a tranche plan, label it `Execution Tranche` and link the applicable specification requirements, dependencies, and existing complete plan. If no complete plan exists, note that absence without creating one by default. Resolve only missing dependencies that block safe planning of this tranche; preserve other requirements without replanning or claiming to deliver them.

Use compact specification IDs or heading anchors rather than repeating the source document.

## Goal authority

- Before a plan changes product meaning, programme order, trust boundaries, or shared infrastructure, identify the applicable current authority and accepted goal.
- A plan may propose and explain a programme or scope delta, but recording the delta does not approve it. Direct current instructions, repository governance, or an explicitly adopted specification may provide the required authority.
- When authority for a material delta is unresolved, keep it as an explicit decision gate and preserve the accepted baseline in every executable slice.

## Choose plan depth

### Inline plan

Use for a moderate change that can be completed in the current session.

Use as few coherent steps as the dependencies need. Each step should produce a meaningful, testable increment.

### Durable plan

Use when:

- The work will span sessions,
- Several subsystems must coordinate,
- A migration or rollout exists,
- Another agent or developer may execute it, or
- The user explicitly requests a plan document.

Store it where the repository expects design or implementation plans. Do not create a new planning directory without checking local conventions.

## Plan structure

Include only what is useful:

1. **Goal and boundaries**
   - Intended behavior
   - Explicit non-goals
   - Material assumptions

2. **Implementation slices**
   - Outcome of the slice
   - Files or areas likely to change
   - Core logic or data-flow change
   - Tests or checks for that slice
   - Dependencies on earlier slices

3. **Cross-cutting concerns**
   - Compatibility or migration
   - Error handling
   - Security/privacy
   - Performance or concurrency
   - Rollback or feature flag, when applicable

4. **Acceptance verification**
   - Targeted tests
   - Broader checks justified by risk
   - Manual or visual verification where automation is not sufficient

## Granularity

A good task is independently understandable and verifiable. Prefer vertical slices over file-by-file chores.

Good:

- Add stale-cursor validation across backend mutation and pagination paths; cover it with regression tests.
- Introduce the new note artifact contract, update producers and consumers, then validate existing fixtures.

Weak:

- Open file A.
- Add import.
- Write ten lines.
- Run tests.
- Commit.

Do not include complete production code in a plan unless a subtle algorithm, schema, or protocol requires a precise example. Pseudocode and data shapes are usually enough.

## Choose the first executable path

For work crossing components, identify the shortest useful path from the real entry point, through the material state or boundary, to an observable result. Within accepted programme order, arrange an early run through that path before multiplying peer features around an untested assumption.

If one capability question could invalidate the implementation, settle it with the cheapest discriminating probe first. If the path is already understood, connect it directly; do not manufacture a separate spike. For a new product, establish the first real entry and state owner rather than planning every layer independently.

Name what the first run can establish and what remains. Saving and reopening through the selected command can reveal wiring and persistence defects that helper tests miss; it does not establish unrelated host behavior. Use an authorized surrogate when necessary and preserve its limits. An unavailable external step blocks only dependent work. Keep the rest of the accepted outcome in the existing plan and carry it through; this first run is an implementation ordering choice, not a smaller delivery contract.

## Plan review

Review the plan once against the requirements:

- Every acceptance criterion maps to a task or verification step.
- The plan covers the complete requested outcome rather than a scaffold or convenient subset.
- A full-spec plan keeps every accepted requirement visible. An explicitly requested tranche maps its applicable requirements and prerequisites, linking other accepted scope without replanning it.
- Dependencies are ordered correctly.
- Any narrowing, removal, deferral outside the plan, or reordering is an explicit specification delta rather than an implementation convenience.
- No hidden migration or compatibility issue is ignored.
- The plan does not add speculative infrastructure.
- The verification scope matches the risk.

Fix gaps directly. Do not dispatch a separate plan reviewer by default.

## Implementation handoff

When another agent or session will execute the plan, include:

- Current branch or workspace assumptions
- Commands needed to start
- Important files and repository guidance
- Known risks and stopping conditions
- Exact expected final report

Do not paste large source files into the plan.

## Exit behavior

- If the user asked for a plan only, stop after the plan.
- If the user asked for implementation, proceed into coherent, independently verifiable slices without waiting for ritual approval.
- Ask before proceeding only when the plan exposes an unresolved, material product or destructive decision.
