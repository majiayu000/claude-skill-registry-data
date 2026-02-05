---
name: execplans
description: Write and maintain self-contained ExecPlans (execution plans) that a novice can follow end-to-end; use when planning or implementing non-trivial repo changes.
---

# Codex Execution Plans (ExecPlans)

This skill describes how to author, discuss, and implement an execution plan
("ExecPlan"). An ExecPlan is a living design-and-delivery document that a
coding agent (or human) can follow to ship a demonstrably working change.

Treat the reader as a complete beginner to this repository. Assume they have:

- only the current working tree,
- only the single ExecPlan file you provide,
- no memory of prior plans,
- no external context.

The bar is high: the ExecPlan must be self-contained and sufficient for
end-to-end delivery, including validation and observable behaviour.

## When to use this skill

Use this skill when:

- you are asked to write an "execution plan", "design doc", "spec", or
  "implementation plan" for a meaningful change, or
- you are asked to implement work that is (or should be) guided by an ExecPlan,
  or
- the task has significant unknowns and would benefit from prototyping
  milestones to de-risk feasibility.

## Non-negotiable requirements (read first)

Every ExecPlan must satisfy all of the following:

- Fully self-contained: it contains all knowledge and instructions needed for a
  novice to succeed.
- Living document: it must be revised as progress is made, discoveries occur,
  and decisions are finalised; each revision must remain self-contained.
- End-to-end and observable: it must produce demonstrably working behaviour,
  not merely "code changes that compile".
- Plain language: define every term of art immediately, or do not use it.
- Outcome-focused: begin with why the work matters and how to observe success.
- Controlled delegation: the agent implementing the plan proceeds
  milestone-by-milestone within defined tolerances, escalating when those
  tolerances would be exceeded rather than improvising.

Autonomy without tolerances is unattended automation. The goal is predictable
outcomes, not maximum throughput.

## When to push back or escalate

Before accepting a task, evaluate whether an ExecPlan is the right approach.
Escalate or request clarification when:

- The task is underspecified and multiple interpretations lead to materially
  different implementations. Present the interpretations and ask which is
  intended.
- The task's scope is unbounded or unclear. Propose a bounded first milestone
  and ask if that captures the intent.
- The task conflicts with observable project conventions, existing tests, or
  documented constraints. Note the conflict and ask how to resolve it.
- The task requires changes to areas with high blast radius (auth, payments,
  data migrations, public APIs) without explicit acknowledgement of the risk.
  Name the risk and ask for confirmation.
- The task requests a pattern that experience suggests produces poor outcomes
  (e.g., "just make the tests pass" when the tests are wrong). State the
  concern and propose an alternative.

Pushing back is not failure; it is part of the agent's quality function.

## Approval gate (required before implementation)

An ExecPlan proceeds through two distinct phases:

1. Draft phase: the agent produces the ExecPlan but does not execute it.
2. Execution phase: the agent implements within tolerances, escalating on
   exceptions.

After completing the initial ExecPlan draft, present it to the user and await
explicit approval before beginning implementation. This gate exists because:

- The user may have constraints not yet captured.
- Tolerance thresholds may need adjustment.
- The proposed approach may conflict with work the agent cannot see.

Do not interpret silence as approval. Do not begin implementation until the
user explicitly confirms the plan or requests revisions.

If the user has previously established standing instructions (e.g., "implement
plans immediately for changes under 100 LOC"), those instructions override this
gate for qualifying work.

## Relationship to `PLANS.md`

If `PLANS.md` exists in the repo, follow it to the letter.

When authoring an ExecPlan:

- Read the entire `PLANS.md` file, then re-read anything you rely on.
- Start from the skeleton (included below) and flesh it out as you research.

When implementing an ExecPlan:

- Do not pause to ask what to do next; proceed to the next milestone.
- Stop and escalate when a tolerance threshold is reached.
- Keep all sections current, especially the mandatory living sections.
- Commit frequently and keep changes small and testable.

## Formatting rules (strict)

ExecPlans have a strict envelope to keep them easy to copy, review, and resume:

- Each ExecPlan must be one single fenced code block labelled as `md` that
  begins and ends with triple backticks.
- Do not nest additional triple-backtick fences inside the ExecPlan. When you
  need commands, transcripts, diffs, or code, present them as indented blocks
  inside the single fence.
- Use two newlines after every heading.
- Use correct Markdown syntax for ordered and unordered lists.

Exception:

- If you are writing an ExecPlan to a Markdown file where the entire file is
  only the ExecPlan, omit the outer triple backticks.

## How to write a good ExecPlan

Write in plain prose. Prefer sentences over lists. Avoid checklists, tables,
and long enumerations unless brevity would obscure meaning.

Anchor everything to observable outcomes:

- State what a user can do after the change.
- Provide the exact commands to run and the outputs to expect.
- Phrase acceptance as behaviour a human can verify.
  - Good: "Running `make test` passes and the new test
    `tests::feature_x::works` fails before and passes after."
  - Good: "Starting the server and requesting `/health` returns HTTP 200 with
    body `OK`."
  - Bad: "Added a `HealthCheck` struct."

Be explicit about repository context:

- Name files with full repository-relative paths.
- Name functions/modules precisely, as they appear in code.
- Include a short orientation paragraph if touching multiple areas so a novice
  can navigate confidently.

Be safe and idempotent:

- Steps should be re-runnable without damage or drift.
- If a step can fail halfway, say how to retry.
- If anything destructive is unavoidable, spell out backups/rollback.

Validation is not optional:

- Include instructions to run tests, lint, and any relevant runtime checks.
- Include expected outputs (even short ones) so a novice can tell success from
  failure.

Capture evidence:

- When steps produce output, include concise transcripts as indented examples.
- Keep evidence focused on what proves success.

## Mandatory living sections (always present)

ExecPlans must contain, and must keep up to date as work proceeds:

- `Constraints` (hard invariants that must not be violated)
- `Tolerances` (thresholds that trigger escalation when breached)
- `Risks` (known uncertainties with mitigations, identified upfront)
- `Progress` (with checkbox list and timestamps)
- `Surprises & Discoveries` (unexpected findings during implementation)
- `Decision Log` (every key decision with rationale)
- `Outcomes & Retrospective` (what was achieved and lessons learned)

If you change course mid-implementation:

- Document why in `Decision Log`.
- Reflect the implications in `Progress` (what changed, what remains).
- Update `Risks` if new uncertainties have emerged.

## Exception handling (manage by exception)

When a tolerance threshold is reached or a constraint would be violated:

1. Stop implementation immediately.
2. Document the situation in `Decision Log` with:
   - What threshold was reached or constraint threatened.
   - What options exist to proceed.
   - Trade-offs of each option.
3. Await explicit direction before proceeding.

Do not attempt to work around tolerances. They exist to catch situations where
human judgement is required.

## Prototyping milestones (encouraged when de-risking)

When requirements are challenging or unknowns are significant, include explicit
prototyping milestones:

- Label the milestone as prototyping.
- Keep prototypes additive, testable, and easy to delete or promote.
- Provide concrete run instructions and acceptance criteria that decide whether
  the prototype is kept or discarded.
- If exploring alternatives, keep them parallel only long enough to reduce
  risk, then retire one path with tests.

## Skeleton of a good ExecPlan

Copy the following skeleton when starting a new ExecPlan, then fill it in as
you research and implement.

```markdown
# <Short, action-oriented description>

This ExecPlan is a living document. The sections `Constraints`, `Tolerances`,
`Risks`, `Progress`, `Surprises & Discoveries`, `Decision Log`, and
`Outcomes & Retrospective` must be kept up to date as work proceeds.

Status: DRAFT | APPROVED | IN PROGRESS | BLOCKED | COMPLETE

If PLANS.md file is checked into the repo, reference the path to that file here
from the repository root and note that this document must be maintained in
accordance with PLANS.md.

## Purpose / Big Picture

Explain in a few sentences what someone gains after this change and how they
can see it working. State the user-visible behaviour you will enable.

## Constraints

Hard invariants that must hold throughout implementation. These are not
suggestions; violation requires escalation, not workarounds.

- Paths/modules this plan must not modify.
- Public interfaces that must remain stable.
- Compatibility requirements (language versions, platforms, targets).
- Security or compliance considerations that constrain approach selection.

If satisfying the objective requires violating a constraint, do not proceed.
Document the conflict in `Decision Log` and escalate.

## Tolerances (Exception Triggers)

Thresholds that trigger escalation when breached. These define the boundaries
of autonomous action, not quality criteria.

- Scope: if implementation requires changes to more than <N> files or <M> lines
  of code (net), stop and escalate.
- Interface: if a public API signature must change, stop and escalate.
- Dependencies: if a new external dependency is required, stop and escalate.
- Iterations: if tests still fail after <K> attempts, stop and escalate.
- Time: if a milestone takes more than <T> hours, stop and escalate.
- Ambiguity: if multiple valid interpretations exist and the choice materially
  affects the outcome, stop and present options with trade-offs.

Adjust these values based on the task. Small, well-understood changes warrant
tighter tolerances; exploratory work may need looser ones.

## Risks

Known uncertainties that might affect the plan. Identify these upfront and
update as work proceeds. Each risk should note severity, likelihood, and
mitigation or contingency.

    - Risk: <description>
      Severity: low | medium | high
      Likelihood: low | medium | high
      Mitigation: <how to prevent or reduce impact>

Risks differ from Surprises: risks are anticipated; surprises are not.

## Progress

Use a list with checkboxes to summarise granular steps. Every stopping point
must be documented here, even if it requires splitting a partially completed
task into two ("done" vs. "remaining"). This section must always reflect the
actual current state of the work.

    - [x] (2025-10-01 13:00Z) Example completed step.
    - [ ] Example incomplete step.
    - [ ] Example partially completed step (completed: X; remaining: Y).

Use timestamps to measure rates of progress and detect tolerance breaches.

## Surprises & Discoveries

Unexpected findings during implementation that were not anticipated as risks.
Document with evidence so future work benefits.

    - Observation: <what was unexpected>
      Evidence: <how you know>
      Impact: <how it affects this plan or future work>

## Decision Log

Record every significant decision made while working on the plan. Include
decisions to escalate, decisions on ambiguous requirements, and design choices.

    - Decision: <what was decided>
      Rationale: <why this choice over alternatives>
      Date/Author: <timestamp and who decided>

## Outcomes & Retrospective

Summarise outcomes, gaps, and lessons learned at major milestones or at
completion. Compare the result against the original purpose. Note what would be
done differently next time.

## Context and Orientation

Describe the current state relevant to this task as if the reader knows
nothing. Name the key files and modules by full path. Define any non-obvious
term you will use. Do not refer to prior plans.

## Plan of Work

Describe, in prose, the sequence of edits and additions. For each edit, name
the file and location (function, module) and what to insert or change. Keep it
concrete and minimal.

Structure as stages with explicit go/no-go points where appropriate:

- Stage A: understand and propose (no code changes)
- Stage B: scaffolding and tests (small, verifiable diffs)
- Stage C: implementation (minimal change to satisfy tests)
- Stage D: hardening, documentation, cleanup

Each stage ends with validation. Do not proceed to the next stage if the
current stage's validation fails.

## Concrete Steps

State the exact commands to run and where to run them (working directory).
When a command generates output, show a short expected transcript so the
reader can compare. This section must be updated as work proceeds.

## Validation and Acceptance

Describe how to start or exercise the system and what to observe. Phrase
acceptance as behaviour, with specific inputs and outputs. If tests are
involved, say "run <project's test command> and expect <N> passed; the new test
<name> fails before the change and passes after".

Quality criteria (what "done" means):

- Tests: <what must pass>
- Lint/typecheck: <commands and expected result>
- Performance: <any benchmarks or thresholds>
- Security: <any scans or review requirements>

Quality method (how we check):

- <CI command or manual verification steps>

## Idempotence and Recovery

If steps can be repeated safely, say so. If a step is risky, provide a safe
retry or rollback path. Keep the environment clean after completion.

## Artifacts and Notes

Include the most important transcripts, diffs, or snippets as indented
examples. Keep them concise and focused on what proves success.

## Interfaces and Dependencies

Be prescriptive. Name the libraries, modules, and services to use and why.
Specify the types, traits/interfaces, and function signatures that must exist
at the end of the milestone. Prefer stable names and paths such as
`crate::module::function` or `package.submodule.Interface`.

E.g., in crates/foo/planner.rs, define:

    pub trait Planner {
        fn plan(&self, observed: &Observed) -> Vec<Action>;
    }
```

## Revision note (required when editing an ExecPlan)

When you revise an ExecPlan, ensure changes are reflected across all relevant
sections. Append a short note at the bottom of the ExecPlan describing:

- what changed,
- why it changed,
- and how it affects the remaining work.

Update the Status field in the header when the plan's state changes.
