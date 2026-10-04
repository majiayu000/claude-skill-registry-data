---
name: grill-with-codebase
description: Use when the user brings a task, ticket, or vague intent touching an existing codebase and wants interrogation to shape a buildable plan, or uses any 'grill' trigger phrases alongside a codebase context.
---

I have a task or intent, not a finished plan. Interview me one question at a time until the answers form a concrete plan. Resolve dependencies between decisions one-by-one. Give a recommended answer with each question.

Ask one question at a time. Wait for feedback before continuing.

Enact the plan only after I confirm it is concrete.

## Codebase is the ground truth

The task touches an existing codebase. Before the first question, read the affected code: files, modules, contracts, callers, data flow, tests, and nearby invariants. Ground every question and recommended answer in what the code actually does today, not generic best practice.

- If a question can be answered by exploring the codebase, explore the codebase instead of asking. Grill me only on the decisions the code can't settle on its own.
- When a question or recommended answer references existing code, cite the file path and line range so we both look at the same thing.
- When I propose a shape that contradicts an existing pattern, invariant, scope rule, or lifecycle in the code, surface the conflict with the decisive snippet before moving on.
- Verify every claim about current behavior against code you actually read this session. If you can't verify it, say so and go read it before continuing.

## From task to plan

Start by establishing the task's scope and success state, then rotate through these angles:

- **Scope & success**: what does "done" look like; what is explicitly out of scope; what existing behavior must not change?
- **Fit with existing patterns**: does the task follow the surrounding conventions, or does it silently introduce a new shape? Where does the new code live?
- **Data flow & persistence**: where does new data come from, where is it stored, who reads it, what scopes apply, what migrations are needed?
- **Invariants & lifecycle**: what must stay true; which existing subscriber/observer/lifecycle hooks does the task break or bypass?
- **Edge cases & failure modes**: null/empty inputs, concurrent writes, soft-delete, company scoping, partial failures, rollbacks.
- **Cross-module wiring**: who calls the changed code, who implements the contracts, what events/jobs fire, what breaks downstream.
- **Test impact**: what existing tests change; what new tests the task demands; what behavior would regress untested.

Record each decision. When every branch resolves, present the concrete plan: file-by-file changes, new artifacts, migrations, tests, and open risks. Ask for confirmation before enactment.

- One question at a time. Ask, wait, then next.
- Recommended answer: one line, no justification.
- This skill is read-only. The output is a plan, not a change.
