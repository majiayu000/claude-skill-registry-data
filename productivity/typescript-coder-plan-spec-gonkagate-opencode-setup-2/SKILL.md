---
name: typescript-coder-plan-spec
description: "Design coder-facing implementation plans for TypeScript and Node backends. Use whenever the task is to turn a backend change, approved spec, bug fix, refactor, or multi-step TS service task into ordered execution phases with dependencies, checkpoints, validation, and rollback notes; start from architecture and only pull in contract, runtime, data, state, or test topics when the plan truly depends on them, even if the user jumps straight to 'write the implementation plan' or starts coding too early."
---

# TypeScript Coder Plan Spec

## Purpose

Use this skill to turn an approved or mostly approved backend change into an
explicit implementation plan another coder can execute safely.

This skill owns:

- execution slicing and phase ordering
- dependency and checkpoint selection
- per-phase validation and proof expectations
- rollback or mitigation notes when sequencing risk matters
- explicit blockers, assumptions, and handoff cues

This skill does not own:

- unresolved architecture design
- TS-heavy modeling design
- code-writing
- standalone deep test-plan design
- read-only design review

If used from a project agent, let the agent own scope, user coordination, and
final decisions. This skill owns plan quality only.

## Expert Standard

Do not optimize this skill around generic planning recall.

Treat the usual moves as table stakes:

- break work into steps
- mention tests and rollback
- start with migrations when the schema changes
- avoid obviously risky ordering

That is table stakes, not specialist value.

This skill earns its use through a narrower and more demanding planning
discipline:

- start from ownership and dependency direction, not from a file list
- identify the hidden blocker or hidden compatibility window that would
  otherwise be flattened into a normal step
- choose phase boundaries that protect invariants, not just convenient task
  chunks
- refuse fake completeness when upstream design decisions are still missing
- stage risky contract, runtime, data, or state changes so rollback remains
  credible
- choose the smallest honest validation step per phase instead of generic
  reassurance
- compare the winning plan against the strongest tempting smaller and broader
  alternatives
- make artifact placement, handoff shape, and parallelism choices explicit
- keep assumptions, blockers, omissions, and confidence visible

If the plan changes only wording and not sequencing, phase boundaries, proof,
or risk handling, the skill is not doing enough yet.

If the answer could be swapped with `1. implement feature 2. add tests 3.
deploy`, it is far below the bar for this skill.

## Read These References When You Need Them

- `references/core-model.md`
  Use by default when the planning boundary may blur.
- `references/planning-workflow.md`
  Use for every non-trivial implementation plan.
- `references/seam-activation-matrix.md`
  Use when deciding which adjacent shared topics actually matter.
- `references/unfamiliar-backend-audit.md`
  Use when current codebase reality is still unclear.
- `references/execution-shape-and-artifacts.md`
  Use when the hard part is choosing `direct` versus `phased` versus
  `parallelized` execution, deciding whether the plan should live inline or in
  `docs/plans/`, or deciding whether a separate test-plan handoff is needed.
- `references/plan-pressure-test.md`
  Use when the first plan sounds plausible but generic, over-broad, or
  under-ordered.
- `references/stack-sensitive-checkpoints.md`
  Use when sequencing or validation depends on actual contract, runtime, data,
  state, or test semantics in this stack.
  This is the hard-skill layer that should make the plan sharper when exact
  stack mechanics actually change sequence or proof.

## Relationship To Shared Research

Start with the local method and references in this skill.

This skill should not own a separate umbrella deep-research prompt.

Load `references/core-model.md` by default.

Load `references/planning-workflow.md` for every non-trivial task.

Load `references/seam-activation-matrix.md` before pulling in extra topic
packs.

Load `references/execution-shape-and-artifacts.md` when deciding phase shape,
parallelism, or plan-artifact placement.

Start every real implementation plan from
`../_shared-hyperresearch/deep-researches/ts-backend-architecture.md`.

Then load only the shared topic files that change the plan:

- `api-contract`
  for request or response schemas, OpenAPI or publication coupling,
  compatibility-sensitive rollout, or serializer-visible changes
- `fastify-runtime`
  for plugin order, decorator scope, hooks, lifecycle, streaming, or
  startup/shutdown sequencing
- `prisma-postgresql`
  for migrations, constraints, backfills, query ownership, or
  transaction-sensitive rollout
- `redis-runtime`
  for key protocols, TTL semantics, scripts, cache or state migrations, or
  coordination semantics
- `runtime-workflow-state-machines`
  for durable workflow truth, transitions, timers, cancellation, recovery, or
  re-entry-safe sequencing
- `vitest-qa`
  when phase ordering depends on proof obligations, harness realism, or a
  separate test-plan handoff

Do not load untouched topics for completeness.

If an adjacent topic is not just influencing plan order but is still missing
its underlying design decision, hand off to the relevant neighbor skill
instead of pretending the plan can absorb it.

## Relationship To Neighbor Skills

- Use `ts-backend-architect-spec` when the main task is choosing architecture
  or ownership boundaries rather than sequencing already-chosen work.
- Use `api-contract-designer-spec`,
  `fastify-plugin-architecture-spec`, `prisma-postgresql-data-spec`,
  `redis-runtime-spec`, or `runtime-workflow-state-machines` when one
  technical seam still needs design decisions before planning can stabilize.
- Use `technical-design-review` when the proposed design needs read-only
  challenge before execution planning.
- Use `typescript-modeling-spec` when TS-heavy modeling choices are still
  undecided.
- Use `vitest-qa-tester-spec` when the proof portfolio is large enough to
  deserve a separate test plan.
- Use `typescript-coder` when the main task is implementation.
- Use `verification-before-completion` when the question is proof sufficiency
  at closeout rather than execution sequencing.

## Use This Skill For

- turning an approved spec, bug fix, refactor, or feature change into an
  ordered implementation plan
- phasing risky backend work across contract, runtime, data, state, and test
  surfaces
- deciding what must land first, what can run in parallel, and where
  checkpoints belong
- shaping refactor or migration work so rollback and validation stay credible
- producing a coder-facing plan another agent or engineer can follow

## Input Sufficiency

Do not fake a detailed implementation plan from one vague request.

Before making strong sequencing claims, confirm what you actually know:

- target change and desired outcome
- current ownership surfaces or modules involved
- which design decisions are already settled and which are still open
- touched risk seams: contract, runtime, data, state, validation
- known rollout, migration, or operational constraints
- current proving environment and reuse opportunities

If those facts are missing, say what is missing and downgrade the output to:

- blocker list
- pre-planning investigation steps
- or a conditional plan with explicit assumptions

Do not invent schema state, deploy order, or test harness capabilities.

## Core Planning Model

Treat the implementation plan as a control layer between approved design and
code execution.

The unit of planning is a `change slice`, not a file and not a generic to-do
item.

A good change slice:

1. changes one primary invariant, boundary, or dependency surface
2. has a clear reason it belongs before or after neighboring slices
3. exposes what it depends on and what depends on it
4. has a smallest honest validation step
5. has rollback or mitigation notes when the blast radius is real
6. stays executable without hiding unresolved design work inside it

Prefer phases over file inventories.

Prefer ordering by dependency and safety over ordering by convenience.

Prefer explicit blockers over imaginary certainty.

## Workflow

1. Frame the plan surface.
   - What is changing?
   - What is already decided?
   - What remains open enough to block honest planning?
2. Start from the architecture base.
   - Identify owners, consumers, composition-root touchpoints, and public
     surfaces.
   - Decide which changes are foundational versus dependent.
3. Activate only the touched seams.
   - Use `references/seam-activation-matrix.md`.
   - Pull in extra topics only when they change sequence, proof, or rollback.
4. Build candidate change slices.
   - Slice by invariant, ownership boundary, migration boundary, or rollback
     boundary.
   - Do not default to file-by-file tasks.
5. Choose the execution shape.
   - `direct` for tiny, reversible work with one clear surface.
   - `phased` by default for non-trivial work.
   - `parallelized` only when write scopes, dependencies, and validation
     checkpoints are explicit.
   - Use `references/execution-shape-and-artifacts.md` when this choice is not
     obvious.
6. Sequence the phases.
   - Put enabling boundaries before consumers.
   - Put safe schema or state introduction before strict enforcement or
     cleanup.
   - Put proof and rollback notes next to the slice they justify.
7. Attach validation.
   - Name the smallest honest validation step for each meaningful phase.
   - Escalate to a dedicated test-plan handoff when proof design becomes its
     own task.
8. Pressure-test and trim.
   - What is the strongest tempting smaller plan?
   - What is the strongest tempting broader plan?
   - What steps are duplicated, speculative, or blocked on missing design?
9. Emit the final plan.
   - Keep it ordered, explain why the order matters, and leave assumptions
     visible.

## Reasoning Obligations

For any non-trivial plan, make the answer survive all of these passes:

- `Primary change slice`
  Name the boundary or invariant each phase owns.
- `Dependency reason`
  State why this phase belongs where it does.
- `Active seam`
  State which adjacent topic, if any, changes the sequence or proof.
- `Failure if misordered`
  Name the regression, rollout risk, or ambiguity the ordering is preventing.
- `Validation`
  Name the smallest honest check that proves the phase landed safely.
- `Assumption boundary`
  Say what is observed, what is inferred, and what fact would change the plan.

If a step cannot satisfy those passes, fold it into another phase or drop it.

## Plan Quality Bar

Keep a phase only if all are true:

- it owns a distinct boundary, invariant, or dependency step
- it has a clear prerequisite or unlock reason
- it has a completion signal or validation step
- it does not hide unresolved design work
- rollback or mitigation is explicit when risk justifies it

Reject these weak patterns:

- file-by-file change logs presented as plans
- giant single steps like `implement feature`
- `add tests` with no proof ownership
- contract, migration, or state changes with no rollout order
- cleanup steps scheduled before the compatibility window is earned
- padding steps added only for completeness
- generic architecture advice where execution order should be

## Boundaries

Do not:

- redesign the system when the task is planning
- make missing architecture or modeling decisions implicitly
- write code or line-by-line patch instructions
- load every shared topic `just in case`
- present validation only as an end-of-plan afterthought
- promise rollout safety or proof strength without naming the actual checks
- flatten blocker resolution and executable work into the same phase list

## Escalate When

Escalate if:

- the design is still unstable enough that architecture or topic-specific spec
  work should happen first
- the proof portfolio becomes large enough to deserve a separate test plan
- the task turns into code-writing or detailed patch design
- current-state uncertainty is high enough that the honest next step is
  investigation, not sequencing

## Output Contract

Implementation-planning answers should normally use this structure:

- `Plan Surface`
- `Assumptions / Blockers`
- `Execution Shape`
- `Active Seams`
- `Implementation Plan`
- `Validation`
- `Rollback / Mitigations`
- `Confidence`

If the caller asked for a shorter answer, compress the same structure rather
than dropping blockers, order rationale, or proof obligations entirely.
