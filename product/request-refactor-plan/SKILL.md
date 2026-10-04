---
name: request-refactor-plan
description: "Side-route skill for planning refactors as safe, tiny-commit RFCs. Use when the user wants a structured refactor plan before implementation. Feeds approved refactor work back into /execute. Not for new-feature shaping or already-concrete implementation tasks."
sources:
  primary:
    - "Refactoring — Martin Fowler"
---

# Request Refactor Plan

This is a side-route skill for work that is primarily about restructuring code safely rather than shaping a new feature.

## Invocation Position

Use `/request-refactor-plan` when the user wants a refactor RFC, a tiny-commit migration path, or a safer way to reorganize code without jumping straight into implementation.

Do not use it when the work is still a product-shaping problem for `/write-a-prd`, or when the refactor task is already concrete enough to execute directly in `/execute`.

This skill will be invoked when the user wants to create a refactor request. You should go through the steps below. You may skip steps if you don't consider them necessary.

1. Ask the user for a long, detailed description of the problem they want to solve and any potential ideas for solutions.

2. Explore the repo to verify their assertions and understand the current state of the codebase.

3. Ask whether they have considered other options, and present other options to them.

4. Interview the user about the implementation. Be extremely detailed and thorough.

5. Hammer out the exact scope of the implementation. Work out what you plan to change and what you plan not to change.

6. Look in the codebase to check for test coverage of this area of the codebase. If there is insufficient test coverage, ask the user what their plans for testing are.

7. Break the implementation into a plan of tiny commits. Remember Martin Fowler's advice to "make each refactoring step as small as possible, so that you can always see the program working."

   Each commit should be a trivially safe step. Work backward from the final state — ask "what would make the last step trivially safe?" and plan commits that create those preconditions.

   Use these strategies to decompose safely:

   - **Reconcile Differences**: When two code paths need to be unified, plan commits that make them incrementally identical first, then a final commit that merges. Never plan a commit that merges two slightly-different implementations directly — the differences hide bugs.
   - **Isolate Change**: When modifying one part of a multi-part function, plan a commit that extracts the part first, then a separate commit that modifies the extracted unit. Extraction is low-risk; modification happens in constrained scope.
   - **Migrate Data**: When changing a data representation, plan commits that temporarily maintain both old and new formats. Shift writes to the new format first, then reads, then delete the old format. Every intermediate commit is independently verifiable.

8. Create a GitHub issue with the refactor plan. Use the following template for the issue description:

<refactor-plan-template>

## Problem Statement

The problem that the developer is facing, from the developer's perspective.

## Solution

The solution to the problem, from the developer's perspective.

## Commits

A LONG, detailed implementation plan. Write the plan in plain English, breaking down the implementation into the tiniest commits possible. Each commit should leave the codebase in a working state.

## Decision Document

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this refactor.

## Further Notes (optional)

Any further notes about the refactor.

</refactor-plan-template>

## Handoff

- **Expected input:** a refactor problem that needs safer sequencing and scope boundaries
- **Produces:** a GitHub issue with a tiny-commit refactor plan and testing decisions
- **May be informed by:** `/improve-codebase-architecture` when the refactor opportunity emerged from architecture exploration
- **Feeds back into:** `/execute` once the refactor plan is approved and ready to execute
