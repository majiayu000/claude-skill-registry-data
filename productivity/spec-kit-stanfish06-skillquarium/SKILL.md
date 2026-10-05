---
name: spec-kit
description: Runs the Spec-Kit (GitHub SDD) artifact pipeline — constitution, spec, clarify, plan, tasks, analyze, implement — using its templates. Use when a feature needs a versioned spec/plan/tasks set under specs/NNN-feature/, when requirements must be pinned before any code, or when checking spec-plan-tasks consistency before implementing.
---

# Spec Kit

## Overview

A distillation of [github/spec-kit](https://github.com/github/spec-kit) — templates and
method only, no CLI, no install. Specifications are the primary artifact; code is their
expression. You maintain software by evolving the spec, not by patching code and hoping
the doc catches up.

The value is not the folder structure. It is that **the templates constrain the model**:
they forbid implementation detail in the spec, force `[NEEDS CLARIFICATION]` instead of a
plausible guess, and gate the plan behind explicit simplicity checks. Fill the templates
faithfully and the constraints do the work.

## When to Use

- A feature or project needs a durable, reviewable spec that outlives the session
- Requirements are vague, and guessing would cost more than asking
- The work spans multiple sessions, agents, or people and needs one source of truth
- You want traceability: every task back to a requirement, every requirement back to a user story
- Before implementing, to check spec/plan/tasks actually agree

**When NOT to use:** one-line fixes, typo corrections, exploratory spikes you intend to
throw away. For a lighter-weight spec habit without the artifact tree, use
`spec-driven-development`. For task sizing and dependency mechanics, `planning-and-task-breakdown`
is canonical.

## Artifacts

Everything for one feature lives in one directory, committed to the repo:

```text
.specify/memory/constitution.md   # project-wide, written once, amended rarely
specs/NNN-feature-name/
├── spec.md                       # WHAT and WHY — no tech stack
├── checklists/requirements.md    # quality gate for spec.md
├── plan.md                       # HOW — stack, structure, constitution gates
├── research.md                   # optional: option comparisons, benchmarks
├── data-model.md                 # optional: entities and relationships
├── contracts/                    # optional: API/event contracts
└── tasks.md                      # executable task list, grouped by user story
```

`NNN` is the next free 3-digit number in `specs/`. Derive the slug from the feature
description in action-noun form (`add-user-auth`, `fix-payment-timeout`). The spec
directory and the git branch name are independent — matching them is a choice, not a rule.

Templates live in `templates/` next to this file. Copy, don't paraphrase:

| Template | Purpose |
|---|---|
| `templates/spec-template.md` | Feature spec: prioritized user stories, FRs, success criteria |
| `templates/plan-template.md` | Implementation plan: technical context, gates, structure |
| `templates/tasks-template.md` | Task list organized by user story, with `[P]` parallel markers |
| `templates/constitution-template.md` | Project principles that every plan is checked against |
| `templates/checklist-template.md` | Generic checklist shell for any quality gate |

## The Pipeline

```
CONSTITUTION ─→ SPECIFY ─→ CLARIFY ─→ PLAN ─→ TASKS ─→ ANALYZE ─→ IMPLEMENT
   (once)          │          │         │        │         │
                   └──── quality checklist ──────┴─── read-only audit
```

Each phase reads the artifacts before it. Do not skip forward; a plan built on an
unclarified spec produces tasks that implement the wrong thing efficiently.

### 0. Constitution (once per project)

Copy `templates/constitution-template.md` to `.specify/memory/constitution.md` and fill in
the principles this project will not negotiate. Spec Kit ships five example principles —
library-first, CLI interface, test-first, integration testing, and one project-defined slot —
but the point is that *you* choose them. What matters is that they are few, concrete, and
testable at plan time.

Give it a version and a ratification date. Amendments require a rationale and a
compatibility note; principles are meant to be stable across features.

### 1. Specify

Copy `templates/spec-template.md` to `specs/NNN-slug/spec.md` and fill it from the feature
description.

Rules that make this phase work:

- **WHAT and WHY only.** No languages, frameworks, APIs, or code structure. If you catch
  yourself writing "using React," you are in the plan phase.
- **Written for a non-technical stakeholder.** They should be able to approve it.
- **User stories are prioritized (P1, P2, P3) and independently testable.** Each one, built
  alone, must be a viable slice that delivers value. P1 alone is the MVP.
- **Make informed guesses; record them.** Reasonable defaults (standard auth, industry
  retention periods, user-friendly error handling) go in the Assumptions section, not into
  a question.
- **At most 3 `[NEEDS CLARIFICATION: specific question]` markers.** Use them only where no
  reasonable default exists and the choice moves scope. Priority order: scope >
  security/privacy > UX > technical detail.
- **Success criteria are measurable and technology-agnostic.** "Users complete checkout in
  under 3 minutes" — not "API p95 under 200ms."

Then write `specs/NNN-slug/checklists/requirements.md` from
`templates/checklist-template.md` with these items, and actually run them against the spec:

```markdown
## Content Quality
- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] All mandatory sections completed

## Requirement Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable
- [ ] Success criteria are technology-agnostic
- [ ] All acceptance scenarios are defined
- [ ] Edge cases are identified
- [ ] Scope is clearly bounded
- [ ] Dependencies and assumptions identified

## Feature Readiness
- [ ] All functional requirements have clear acceptance criteria
- [ ] User scenarios cover primary flows
- [ ] Feature meets measurable outcomes defined in Success Criteria
- [ ] No implementation details leak into specification
```

Fix and re-check, up to three passes. If items still fail, record them in the checklist
notes and say so rather than marking them green.

### 2. Clarify

Before planning, scan the spec for ambiguity across this taxonomy and mark each area
Clear / Partial / Missing:

functional scope and out-of-scope · user roles · entities, identity, lifecycle · data volume ·
critical journeys · error/empty/loading states · accessibility and localization · performance ·
scalability · reliability · observability · security and privacy · compliance · external
services and their failure modes · import/export formats · negative scenarios · rate limiting ·
concurrency conflicts · technical constraints · rejected alternatives · glossary consistency ·
acceptance-criteria testability

Ask **at most 5** questions, highest impact first, each with 2–4 concrete options and their
implications in a table plus a custom option. Present them together, wait for answers, then
write the answers back into the spec body — into the requirement or scenario they affect,
not into a dangling Q&A appendix.

If the user chooses to skip clarification (a spike), proceed but say plainly that rework
risk goes up.

### 3. Plan

Copy `templates/plan-template.md` to `specs/NNN-slug/plan.md`. This is where technology
appears for the first time.

Fill Technical Context — language/version, dependencies, storage, testing, target platform,
project type, performance goals, constraints, scale. Anything genuinely unknown stays
`NEEDS CLARIFICATION` rather than becoming an invented number.

Then run the **Constitution Check** gate, deriving the gates from the project's own
constitution. Typical shapes:

```markdown
### Simplicity Gate
- [ ] Using ≤3 projects?
- [ ] No future-proofing?

### Anti-Abstraction Gate
- [ ] Using the framework directly, not wrapping it?
- [ ] Single model representation?

### Integration-First Gate
- [ ] Contracts defined?
- [ ] Contract tests written?
```

A failed gate is not a blocker — it is a debt you must name. Record it in the Complexity
Tracking table with the violation, why it is needed, and why the simpler alternative was
rejected. An empty justification means go back and simplify.

Keep the plan high-level and readable. Code samples, detailed algorithms, and long schemas
belong in `research.md`, `data-model.md`, or `contracts/`, not inline.

Re-check the gates after the design is filled in. Design drift is the usual way a passing
gate quietly becomes a failing one.

### 4. Tasks

Copy `templates/tasks-template.md` to `specs/NNN-slug/tasks.md`. Derive tasks from the
plan, the data model, and the contracts — not from imagination.

Structure, which is the whole point of this template:

- **Phase 1 Setup** — project init, tooling
- **Phase 2 Foundational** — the blocking prerequisites. No user story starts until this is done.
- **Phase 3+ One phase per user story, in priority order.** P1 is labeled MVP. Each phase
  ends with a checkpoint: that story works and is testable on its own.
- **Final phase Polish** — cross-cutting cleanup, docs, hardening

Task format: `[ID] [P?] [Story] Description with exact file path`. `[P]` means it touches
different files from its siblings and can run in parallel. `[US1]` maps it back to a user
story for traceability.

Ordering within a story: tests (if requested) → models → services → endpoints → integration.
Tests are optional in Spec Kit's template — include them when the spec asks, or when the
constitution mandates test-first, in which case they must be written and observed failing
before implementation.

### 5. Analyze

A read-only audit across `spec.md`, `plan.md`, and `tasks.md`. **Modify nothing.** Produce
findings, then offer a remediation plan the user approves before anything is edited.

Build the inventories first — every FR-### and SC-###, every user story, every task and
what it maps to — then run the passes:

| Pass | Looks for |
|---|---|
| Duplication | Near-identical requirements that should be consolidated |
| Ambiguity | "fast", "scalable", "secure", "intuitive" without a number; leftover TODO/`???` |
| Underspecification | Requirements with a verb but no measurable object; tasks citing files that appear nowhere in the plan |
| Constitution alignment | Anything conflicting with a MUST principle |
| Coverage gaps | Requirements with zero tasks; tasks tracing to no requirement |

Severity: constitution conflicts are **CRITICAL** by definition — resolve them by changing
the spec, plan, or tasks, never by reinterpreting the principle. Cap the report at ~50
findings and summarize the overflow.

### 6. Implement

Work the tasks in order, respecting phase gates and checkpoints. Stop at each user-story
checkpoint and verify that story independently before moving to the next priority.

Follow `incremental-implementation` for the execution loop and `test-driven-development`
when the constitution mandates test-first. Use `context-engineering` to load only the spec
sections and source files each task needs.

When implementation reveals the spec was wrong: **update the spec first, then the plan,
then the code.** Fixing code while leaving the spec stale reinstates exactly the drift this
method exists to eliminate.

## Why the Templates Work

The templates are prompts that constrain output. Preserve these constraints when you adapt
them — dropping them is how the method degrades into ordinary documentation.

1. **No premature implementation detail** — keeps the spec stable while technology churns
2. **Mandatory uncertainty markers** — replaces plausible-but-wrong guesses with a question
3. **Checklists as unit tests for the spec** — forces systematic self-review
4. **Gates with justification tables** — makes complexity accountable instead of invisible
5. **Hierarchical detail** — the plan stays readable; depth moves to sub-documents
6. **Contracts and tests before source** — testability is designed in, not retrofitted
7. **No speculative features** — every feature traces to a user story with acceptance criteria

See `references/philosophy.md` for the reasoning behind these.

## Red Flags

- Tech stack named in `spec.md`
- More than 3 `[NEEDS CLARIFICATION]` markers, or zero in a genuinely vague request
- Success criteria phrased as internal metrics (cache hit rate, TPS) rather than user outcomes
- User stories that cannot be built or tested independently
- `tasks.md` written from the spec while skipping the plan
- A failed constitution gate with an empty Complexity Tracking row
- `analyze` editing files instead of reporting
- Code changed to fix a problem the spec still describes incorrectly

## Verification

Before implementation:

- [ ] `constitution.md` exists and the plan's gates derive from it
- [ ] `spec.md` passes its requirements checklist with no unresolved markers
- [ ] Every user story has a priority and an independent test
- [ ] Success criteria are measurable and technology-agnostic
- [ ] `plan.md` records the structure decision and justifies every gate violation
- [ ] `tasks.md` covers every functional requirement, and every task traces to one
- [ ] `analyze` found no CRITICAL findings, or they were resolved in the artifacts
- [ ] All artifacts are committed
