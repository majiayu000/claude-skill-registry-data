---
name: development-task-planner
description: Plan development tasks into clear, low-risk, reviewable increments. Use when the user wants an implementation plan, breakdown of a coding task, sequencing for a feature or refactor, migration planning, validation strategy, or a roadmap that stays maintainable and easy to review.
---

# Development Task Planner

Turn ambiguous engineering work into a concrete implementation plan that is safe to execute, easy to review, and easy to evolve. Optimize for low-risk sequencing, clear ownership, explicit validation, and low human cognitive load.

Assume the plan will be followed strictly during implementation unless a human explicitly amends it.
Assume the implementation may be executed by a different agent in a fresh context window with no access to the prior conversation, so the plan must be self-sufficient.

## Planning Workflow

1. Establish scope.
   - Clarify the exact task, desired outcome, constraints, and what is out of scope.
   - Identify whether the ask is feature work, refactor, migration, bug fix, infrastructure work, or architecture change.
   - Prefer concrete deliverables over vague goals.

2. Identify the true change surface.
   - Find the core modules, state transitions, APIs, persistence, and tests that the task will affect.
   - Distinguish direct change points from incidental neighbors.
   - If the task is stateful or lifecycle-heavy, treat restart, retry, cancellation, and recovery as first-class planning concerns.

3. Define success before steps.
   - State the observable behavior that must be true when the task is done.
   - Define validation early: tests, checks, smoke paths, or user-visible outcomes.
   - Call out unknowns, assumptions, and risks before proposing execution order.

4. Slice the work into low-risk increments.
   - Prefer increments that keep the system working after each step.
   - Isolate schema/model changes from behavior changes when possible.
   - Separate foundational refactors from product behavior unless combining them is clearly safer.
   - Favor plans that are easy to review and revert.

5. Plan for amendment, not improvisation.
   - Make it explicit that implementation must stop if the plan becomes unsafe, impossible, or contradicted by the real codebase.
   - Require an amendment flow: surface the blocker, list options, give pros/cons, explain plan impact, and wait for a human decision.
   - If a better but non-essential design appears during implementation, require a `REVIEW_NOTE` rather than silent deviation.

6. Optimize for human maintainability.
   - Minimize how much context an engineer must hold at once.
   - Prefer plans that centralize risky logic, reduce change amplification, and keep ownership obvious.
   - Avoid plans that require many synchronized edits unless there is no safer alternative.

7. Make the plan self-contained for handoff.
   - Write the plan so a different agent can execute it without reconstructing intent from chat history.
   - Name the concrete target models, contracts, and boundaries instead of relying on shorthand from the conversation.
   - Include the semantic decisions that implementation depends on, especially when renames, capability boundaries, or lifecycle models are involved.
   - State exact target names for important types, fields, context keys, files, or artifact paths when those names matter to correctness.
   - State exact behavior for unsupported capabilities, missing data, and failure paths when implementation would otherwise have to guess.

8. Produce the plan.
   - Give a short ordered list of implementation steps.
   - For each step, make the purpose and dependency clear.
   - Add risks, validation, and any recommended sequencing constraints.

## Planning Principles

- Plan for the real dependency graph, not the order the idea was explained.
- Make the safest next step obvious.
- Keep steps independently verifiable where possible.
- Prefer plans that simplify later review, not just faster coding.
- If a task is too large for one safe pass, split it into phases instead of pretending it is one change.
- Make the document stand on its own for a fresh implementer with no conversational context.
- Eliminate hidden branches: if the plan intends one design, say "do X", not "do X or Y".
- Prefer imperative decisions over advisory wording when implementation should not choose among alternatives.

## Good Plan Qualities

A strong plan:

- defines done in observable terms
- identifies risky edges early
- keeps each step reviewable
- explains why the order matters
- includes validation strategy
- defines what should trigger an amendment
- reduces future maintenance burden, not just present effort
- is self-sufficient enough for another agent to execute in a clean window
- leaves no important term, rename, or target contract open to interpretation
- tells the implementer what to do when a capability is absent or a precondition is not met

## Anti-Ambiguity Rules

When the plan is meant for later implementation by another agent, apply these rules strictly:

- Do not present multiple design branches unless the human is explicitly being asked to choose.
- Do not use vague wording like "consider", "could", "might", "recommended", or "where possible" for core implementation decisions.
- Do not rely on a new implementer to infer the final naming of important types, fields, keys, endpoints, or artifacts.
- Do not describe a migration target with examples only; state the intended target contract directly.
- Do not leave failure behavior implicit. Say whether the system must warn, fail fast, retry, skip, or continue.
- Do not leave ownership implicit. Say which layer owns the contract, which layer adapts it, and which layer consumes it.
- Do not leave external surface changes implicit. If exports, persisted state, fixtures, or HTTP payloads change, say so directly.
- Do not leave cleanup as an unspecified follow-up. Name the legacy fields, shims, tests, or docs that must be removed or updated.

## Stateful-System Planning

For runners, async jobs, queues, orchestration, durable workflows, or any lifecycle-heavy feature, explicitly plan for:

- state ownership
- recovery and restart
- retry and idempotency
- cancellation and partial progress
- truthfulness of status, logs, and persisted state

Load `references/stateful-task-planning.md` when the task touches lifecycle-heavy code.

## Human Maintainability Rule

Plan so that a human can execute and later modify the change without reconstructing the whole system from scratch.

Ask:

- How many files will an implementer need open at once?
- Is there one obvious owner per step?
- Can each step be reasoned about locally?
- Will the final design lower or raise navigation cost?

Load `references/human-maintainability-planning.md` when maintainability and navigability matter as much as correctness.

## Review Alignment

Shape plans so they will review well later:

- centralize risky logic where possible
- avoid introducing extra sources of truth without a strong reason
- keep state writers and readers aligned
- prefer steps that make correctness easier to prove

Load `references/review-alignment.md` when you want the plan to line up tightly with a future code-review pass.

## Amendment Rule

The plan should say what happens if implementation cannot safely continue as written.

Good plans include:

- explicit stop conditions
- an amendment path requiring human choice
- expected places to record amended decisions
- guidance for when `REVIEW_NOTE` is appropriate instead of a plan change

Load `references/plan-amendments-for-planning.md` when you want the plan to support strict implementation control.

## Output Shape

Default output should include:

- a short objective
- assumptions or open questions
- ordered implementation steps
- key risks
- validation plan
- amendment triggers or amendment rule when relevant
- optional maintainability note when relevant
- enough semantic and architectural context that a new agent can implement from the plan alone
- exact target terminology for any renamed or newly introduced contract that affects more than one file or layer
- explicit unsupported-capability behavior when the design includes optional features or backend capabilities

## Avoid

- plans that are only a restatement of the user request
- steps that mix unrelated concerns without justification
- “refactor first” as a reflex when a smaller direct change is safer
- validation as an afterthought
- plans that are easy to write but hard for another engineer to execute
- plans that depend on remembered chat context instead of stating the needed decisions explicitly
- plans that leave the implementer to choose between competing shapes, names, or failure behaviors
- plans that describe the current problem in detail but leave the target implementation underspecified

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
