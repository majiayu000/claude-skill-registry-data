---
name: scenario
version: 1.0.0
description: '[Planning] Use when a workflow step or the user asks for adversarial scenarios: failure modes, data integrity, state boundaries, access risks.'
argument-hint: '[owning artifact, scope brief, or explicit milestone]'
disable-model-invocation: false
---

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:START -->

> **[BLOCKING]** Run phases in order; update task tracking before and after each phase.
> **[BLOCKING]** Every completed or skipped phase needs concise evidence or a reason.

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:END -->

## Quick Summary

**Goal:** Turn one selected embedded outcome slice, explicit roadmap milestone, framework/library scope, or explicitly accepted isolated change into an adversarial, observable scenario set that exposes data corruption, misleading states, access leaks, and recovery gaps before an implementation plan can be approved.

**Summary:**

- Resolve the owning decomposition block, explicit roadmap milestone, framework technical scope, or EXEMPT scope and stable plan directory; block when the applicable upstream scope is missing or unapproved. The embedded branch does not require a product roadmap.
- Derive scenarios from the user journey and source-of-truth state, then stress refresh/replay, invalid input, concurrency, deletion, lifecycle, access, partial failure, and evidence hygiene.
- Map every high-impact scenario to an invariant, expected outcome, prevention/detection expectation, and TC/evidence; ask the owner about material choices.
- Write `{plan-id}/scenario-analysis.md` under the plans root (default `plans/`; a `docsRoots.plans.path` entry in `docs/project-config.json` overrides the path) and mark the Scenario Gate PASS or BLOCKED; `/plan` cannot cook from a blocked gate, and an EXEMPT plan still needs this artifact.
- **Main steps:** resolve inputs/branch → reconstruct the selected journey and source of truth → generate adversarial scenarios → resolve owner decisions → write the analysis → run the Scenario Gate → hand off to `/plan` or record a conditional skip.

**Workflow:** 0) resolve inputs → 1) reconstruct scope → 2) generate adversarial scenarios → 3) resolve decisions → 4) write artifact → 5) run Scenario Gate → 6) hand off to `/plan`.

**Key Rules:**

- Scenarios describe situations and expected outcomes, not framework or database solutions.
- A happy path alone is never sufficient for persistent/stateful work.
- High-impact scenarios without evidence or an owner decision block the plan.
- Never put secrets, real payment data, tokens, or personal data in scenario/evidence artifacts.

## Mission

<request>$ARGUMENTS</request>

## Required Context

**MUST ATTENTION READ** `.claude/skills/shared/product-roadmap-contract.md` and `references/scenario-template.md` before analysis. Also read `docs/project-config.json`, `docs/project-reference/docs-index-reference.md`, and `docs/project-reference/lessons.md` when present. Use the active plan context to resolve the output directory.

## Phase 0: Resolve Inputs

Find the active owning artifact/scope brief from `$ARGUMENTS`, `## Plan Context`, or the explicit milestone in the product-roadmap artifact (default `docs/product-roadmap.md`; `docsRoots.productRoadmap.path` in `docs/project-config.json` overrides). Classify applicability first, then confirm:

- for embedded large-idea work, the parent PBI/spec has a complete `large_idea_decomposition` block, exactly one stable slice is selected, and its `outcome_slices`, dependencies, non-goals, risks/evidence, and deferred owners are readable;
- for explicit-roadmap work, the roadmap exists and is approved and exactly one milestone is selected;
- for a framework/library change, the technical scope brief names affected carriers, operational risks, evidence owners, and commands;
- for an isolated change, the scope brief contains the shared contract's explicit `Roadmap Applicability: EXEMPT` block with reason and accepting owner, and no roadmap or milestone is fabricated;
- the owning artifact/scope brief states actor or technical owner, outcome, in-scope behavior, non-goals, terms, source of truth, and evidence;
- scenario output has a concrete plan directory. Derive `plan-id` from the owning scope's parent directory; if a required scope artifact is not under `{plan-id}/` in the plans root (default `plans/`; `docsRoots.plans.path` in `docs/project-config.json` overrides), stop `BLOCKED` and route to the explicit roadmap writer only for the explicit roadmap branch, or to the owning decomposition/framework/EXEMPT scope step otherwise.

If any applicable input is missing, stop `BLOCKED` and route to its owning branch. Do not infer a slice, milestone, technical outcome, or boundary from a screen, PBI title, or plan filename. If an embedded scope has no replay/state/ownership/recovery/evidence risk that needs adversarial analysis, record the conditional skip reason and do not create a standalone roadmap or scenario artifact.

## Phase 1: Reconstruct the User Journey

Write the selected slice/milestone/technical outcome as an observable sequence:

`actor intent → input/action → business state change → user-visible outcome → persisted/reopened truth → later action`

Name states, transitions, ownership boundaries, and non-goals. Highlight terms that could be interpreted more than one way. Use existing Feature Specs, PBIs, or code only as evidence for an existing product; the scope brief remains the product boundary.

## Phase 2: Generate Adversarial Scenarios

Derive situations from the actual journey, not a canned count. Cover applicable dimensions:

| Dimension | Questions to ask |
| --- | --- |
| Persistence / replay | What happens after refresh, reopen, retry, duplicate submit, or redeploy? |
| Validation / corruption | Can invalid input replace valid data or create a misleading partial record? |
| Concurrency | What if two tabs/actors edit or submit the same item at once? |
| Lifecycle / state | Can a state be skipped, reversed, or confused with a later state such as published/delivered? |
| Ownership / access | Can an unauthenticated, non-owner, or other store/tenant read or mutate it? |
| Deletion / relationships | Does deletion leave orphaned variants, assets, references, or history? |
| Partial failure / recovery | What if a dependent action succeeds halfway, times out, or is repeated? |
| Evidence / operations | Can completion evidence hide failure or expose secrets/sensitive data? |

For each scenario assign `SCN-{MILESTONE}-{NNN}`, severity (`Critical`, `High`, `Medium`, `Low`), trigger, precondition, expected business outcome/invariant, bad outcome, prevention/detection expectation, owner, and TC/evidence mapping. Use one concrete digital-catalog example only when it clarifies a non-obvious pattern; do not force irrelevant dimensions.

## Phase 3: Decision and Risk Gate

Use `AskUserQuestion` for each material choice the scenario analysis cannot resolve, such as conflict policy, deletion semantics, status meaning, audit/history expectations, access boundary, or acceptable recovery behavior. Present 2–4 concrete options and a recommendation. Record each decision as `confirmed`, `deferred`, or `blocked`.

A scenario may be deferred only when the owning decomposition block or explicit roadmap names the deferred item and its owner/follow-up artifact. “AI will handle it later” is not a decision.

## Phase 4: Write the Scenario Artifact

Write `{plan-id}/scenario-analysis.md` under the plans root (default `plans/`; `docsRoots.plans.path` in `docs/project-config.json` overrides) incrementally using `references/scenario-template.md`, beside the resolved scope handoff when the selected branch requires a scenario artifact. Cite the owning decomposition/spec/PBI, explicit roadmap/scope brief, or framework technical brief and any existing spec/code evidence. Keep implementation choices out; record the expected behavior or operational proof that the future plan must protect.

## Phase 5: Scenario Gate

Mark the artifact `PASS` only when:

1. every high-impact scenario has a single expected business outcome or invariant;
2. every high-impact scenario maps to a planned TC, evidence item, or an explicitly approved non-goal/deferred owner;
3. all material choices have an owner status and no unresolved `blocked` decision is hidden;
4. evidence is observable, repeatable, and redacted.

Otherwise mark `BLOCKED`, name the missing decision/evidence, and stop before `/plan`.

## Phase 6: Handoff

Pass the scenario artifact path and scenario IDs to `/plan`. The implementation plan must map phases to the selected slice, explicit milestone, framework boundary, or EXEMPT scope, plus non-goals, scenario IDs, TC IDs, commands, and evidence. `/plan --mode=validate` asks the owner to confirm remaining material choices when that gate is selected.

## Output

Report:

- applicability branch, owning artifact/slice or explicit roadmap/milestone, and scope handoff path when applicable;
- scenario count by severity and covered dimensions;
- high-impact scenario IDs and evidence/TC mappings;
- confirmed/deferred/open decisions;
- Scenario Gate status;
- plan handoff or blocker.

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Turn one selected embedded outcome slice, explicit roadmap milestone, framework/library scope, or explicitly accepted isolated change into an adversarial, observable scenario set that exposes data corruption, misleading states, access leaks, and recovery gaps before an implementation plan can be approved.
**IMPORTANT MUST ATTENTION Main steps:** resolve the applicable scope → reconstruct the journey and source of truth → generate adversarial scenarios → resolve owner decisions → write the analysis → run the Scenario Gate → hand off to `/plan` or record the conditional skip.
**IMPORTANT MUST ATTENTION** run resolve → journey → scenarios → decisions → write → gate → plan handoff in order.
**IMPORTANT MUST ATTENTION** derive scenarios from the journey and source-of-truth state; test replay, persistence, validation, concurrency, lifecycle, access, deletion, recovery, and evidence as applicable.
**IMPORTANT MUST ATTENTION** map high-impact scenarios to expected outcomes and TC/evidence or an approved deferred owner/follow-up artifact.
**IMPORTANT MUST ATTENTION** ask the owner about material decisions; a deferred non-goal must name its owner and follow-up artifact.
