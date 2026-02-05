---
name: spec-driven-translation
description: |
  Spec-driven source translation & modernization workflow for codebases.
  Use when asked to migrate/translate a project (e.g., framework/SDK/language upgrade),
  or when the user wants a structured, externally-validatable implementation loop
  with PRD + plans + checklists and iterative validation/remediation.
---

# Spec-Driven Translation

This Skill executes a documentation-first, validation-driven workflow to translate or modernize a codebase. It turns the existing source into a **Product Requirement Document (PRD)**, derives a **Project Specification**, **Implementation Plan**, and **Task Execution Checklist**, then iteratively implements the work in **externally-validatable** steps with a remediation loop until success.

> High-level flow (from the provided diagram):
> 1. **Ingest -> PRD**
> 2. **Plan translation** 
> 3. **Docs to guide AI** (Project Spec, Implementation Plan, Task Checklist)
> 4. **Iterative task loop** (choose task -> implement step -> run validation -> remediate w/ retry budget)
> 5. **Translated Source Code**

## Preconditions & Setup

1. Identify the **source tree** and the **target environment** (runtime, language, framework versions, build tools).
2. Ensure we have authority to read/write files and run the project’s build/test commands.
3. If needed, ask to install or enable required tools (build system, linters, test runner, package managers).

## Artifacts We Will Create

- `templates/PRD.md` -> filled as `Product_Requirement_Document.md`
- `templates/Project-Specification.md` -> `Project_Specification.md`
- `templates/Implementation-Plan.md` -> `Implementation_Plan.md`
- `templates/Task-Execution-Checklist.md` -> `Task_Execution_Checklist.md`

Keep these docs up-to-date as living sources of truth. They guide all subsequent steps.

## Step-by-Step Instructions

### 1. Ingest -> PRD
- Read the existing codebase (entry points, modules, configs, CI, tests).
- Extract **intent, behaviors, constraints, SLAs, non-functionals**, and integration points.
- Populate and save `Product_Requirement_Document.md` from `templates/PRD.md`.
- Call out **unknowns, risks, and assumptions** explicitly.

### 2. Plan Translation
- Define **target state** (language/framework versions, platform changes, build/test strategy, deployment).
- Fill in `Project_Specification.md` grounding every requirement in the PRD.
- Draft `Implementation_Plan.md` (milestones, work streams, sequencing, acceptance criteria).
- Create `Task_Execution_Checklist.md` (repeatable per-task DoD & safety checks).

### 3. Choose-Implement-Validate Loop
For each iteration:

1. **Choose next task**  
   - Use rubric (below) to pick a task that yields an **externally-verifiable** delta (e.g., unit test passes, binary builds, CLI works, endpoint responds).
   - Update the checklist with the task ID and success conditions.

    ```
    # Pick-Next-Task Rubric

    Score each candidate task 0–3 on:
    - External verifiability (clear test/build signal)
    - Risk isolation (blast radius if wrong)
    - Unblocks others (dependency breaker)
    - Knowledge gain (reduces uncertainty)
    - Effort (fit in one iteration)

    Choose the highest total; tie-break on verifiability.
    ```

2. **Implement a minimal, verifiable step**  
   - Make small changes scoped to one verifiable outcome.
   - Prefer creating/updating **tests** that encode the desired behavior.

3. **Validation**
   - Run validation.
   - Treat **builds/tests/lints/type-checks/formatters** as the external oracle of success.

4. **Remediation (bounded retries)**
   - On failure, capture logs; fix the smallest issue first; re-run validation.
   - Limit to a local retry budget (e.g., 3 attempts) before escalating:
     - Update docs with new facts found.
     - Re-plan or split the task if necessary.

5. **Commit**
   - When validation passes, commit with an evidence-rich message (what/why, tests affected, acceptance criteria met).
   - Append outcomes/notes to the Implementation Plan.

Repeat until the milestone is complete, then proceed to the next milestone.

### 4. Exit Criteria
- All tasks in the current milestone have green validation.
- The translated artifact(s) function under the target environment with documented acceptance evidence.
- PRD, Spec, Plan, and Checklist are updated to reflect reality.

## Pick-Next-Task Rubric (summary)

Prefer tasks that:
- Increase **test coverage** or convert implicit behavior into explicit tests.
- Deliver a **user-visible or CI-visible** signal (a test or build turns green).
- Reduce **coupling or blockers** for later tasks.
- Are reversible and low-risk when uncertain.

Full rubric in `scripts/pick-next-task.md`.

## Notes

- Keep docs concise but **always actionable**. Treat them as contracts with the validator.
- When in doubt, **shrink the task** until it’s externally verifiable within a single iteration.
- Prefer to **keep the human in the loop**, stopping for confirmation on assumptions or changes to the plan.
