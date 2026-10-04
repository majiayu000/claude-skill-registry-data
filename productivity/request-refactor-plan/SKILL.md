---
name: request-refactor-plan
description: Create a Beads-first refactor plan through detailed interview, repo verification, alternatives, scope boundaries, testing decisions, and tiny working increments. Use when the user wants to plan a refactor, write a refactoring RFC, or turn a risky change into safe incremental work.
---

# request-refactor-plan

Create a durable Beads refactor plan before implementation starts. The plan should explain the problem, chosen solution, tiny working increments, test decisions, and explicit non-scope.

Do not implement the refactor while using this skill. Do not create an issue until the user has reviewed the plan.

## Process

### 1. Start with the user's problem

Ask for a long, detailed description of the problem, why it matters now, observed symptoms, affected workflows, current solution ideas, rejected approaches, constraints, risks, and success criteria. Keep interviewing until you can restate the problem and desired outcome in the user's language.

### 2. Load context before code

```bash
bd show <task-id>
```

Before source exploration, read:

- `knowledge/_shared.yaml`
- Relevant `knowledge/repos/*.yaml` files for the repo or sub-repo.
- Any provided alignment, PRD, plan, contract, or issue context.

If no relevant repo knowledge file exists, say so in the working notes.

### 3. Verify repository reality

Explore the codebase to confirm or correct the user's assumptions. Look for current module responsibilities, public interfaces, contracts, schemas, commands, integration points, existing tests, prior-art patterns, hidden coupling, migration concerns, and rollout risks.

Report what the repo confirms, what it contradicts, and what remains uncertain. Do not let the final plan rely only on the user's initial description.

### 4. Discuss alternatives

Ask whether the user considered other options, then present realistic alternatives:

- A smaller scoped refactor.
- A compatibility-preserving path.
- A replacement or simplification path, if plausible.
- A "do nothing yet" option when more evidence is needed.

For each option, summarize benefits, costs, risks, test impact, and why it is or is not preferred.

### 5. Interview the implementation in detail

Make the important decisions explicit:

- Which modules, interfaces, contracts, or behaviors will change.
- What data shape, API, command, or workflow changes are expected.
- What compatibility or migration behavior must be preserved.
- Which users, agents, scripts, or downstream systems depend on the current behavior.
- What observability, documentation, or rollout notes are needed.

Prefer stable names for modules and interfaces over exact file paths. Durable plans should survive file moves.

### 6. Define scope and non-scope

Write down exact in-scope behavior changes, module responsibilities, contract changes, migration steps, and expected tests. Also list tempting cleanup, adjacent features, unrelated rewrites, speculative abstractions, and deferred work as out of scope. If a boundary is ambiguous, ask the user to choose before filing the issue.

### 7. Assess tests before planning commits

Inspect existing coverage for the affected behavior. Identify current protective tests, missing behavior tests, similar prior-art tests, and commands that prove the repo still works. If coverage is insufficient, ask whether to include test-hardening commits at the start of the plan. Recommend tests of external behavior, not implementation details.

### 8. Plan tiny working increments

Break the implementation into the smallest useful commits. Each commit must leave the repo working, have a clear verification command or manual check, avoid mixing unrelated behavior/migration/cleanup/test changes, and be understandable on its own.

Use Martin Fowler's refactoring advice as the standard: each step should be small enough that the program is always visibly working.

### 9. Prepare the durable Beads issue

Use Beads as the default tracker. Choose an explicit priority (`P0` through `P4`, or the numeric equivalent). If priority is unclear, apply `.claude/skills/beads-priority-assignment/SKILL.md` and ask the user to confirm.

Create the issue only after the user approves the plan:

```bash
bd create --type feature --title "<refactor title>" --description "<full refactor plan markdown>" --priority <P0-P4> --repo .
```

Use `--repo ./repos/<repo-name>` for a registered sub-repo. Only create or link a GitHub issue when the user explicitly asks for a mirror; the Beads issue remains the source of truth.

## Durable Issue Template

Do not include exact file paths or code snippets anywhere in the issue body. Use module names, interface names, contracts, commands, behaviors, decisions, and risks.

<refactor-plan-template>

## Problem Statement

Describe the problem from the developer's perspective, including why the current design is painful or risky.

## Solution

Describe the chosen solution and why it is preferred over alternatives.

## Commits

Provide a long, detailed implementation plan in tiny increments. Each commit must include the intended behavior or structural change, why the step is safe, how to verify it, and confirmation that the repo remains working.

## Decision Document

Capture implementation decisions, including:

- Modules or responsibilities that will change.
- Interfaces, contracts, schemas, commands, or workflows that will change.
- Compatibility and migration decisions.
- Architectural tradeoffs and rejected alternatives.
- Interactions with downstream systems, agents, scripts, or users.

Do not include exact file paths or code snippets.

## Testing Decisions

Capture external behavior to test, modules or interfaces needing coverage, prior-art test patterns, test-hardening commits before risky structural changes, and required verification commands.

## Out of Scope

List the cleanup, features, rewrites, migrations, and adjacent problems that are intentionally excluded.

## Further Notes (optional)

Record open questions, assumptions, rollout notes, follow-up issue ideas, or risks that the implementer should keep visible.

</refactor-plan-template>
