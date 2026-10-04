---
description: Break a feature into a detailed implementation plan with bite-sized tasks
---

# Plan

Create a detailed implementation plan for "$ARGUMENTS". Break the work into bite-sized tasks (2-5 minutes each) with exact file paths, test strategy, and commit points.

## Prerequisites

None — this is the first phase of any development effort.

## Process

1. **Understand the feature:**
   - Clarify what "$ARGUMENTS" means — ask the user if ambiguous
   - Identify acceptance criteria and constraints
   - Determine scope boundaries

2. **Explore the codebase:**
   - Read relevant existing code, tests, and configuration
   - Identify files to create and files to modify
   - Understand existing patterns and conventions
   - Note dependencies and potential conflicts

3. **Break into tasks:**
   - Each task should take 2-5 minutes to complete
   - Each task produces a working, committable state
   - Order tasks so each builds on the previous
   - For each task specify: files to touch, steps, expected outcome

4. **Define test strategy:**
   - What tests need to be written?
   - What existing tests might break?
   - How to verify the feature works end-to-end?

5. **Write the plan** using the template from `plugins/development/shared/plan-template.md`

6. **Write the artifact** to `.metapowers/development/$ARGUMENTS/01-plan.md`

## Output

The implementation plan written to `.metapowers/development/$ARGUMENTS/01-plan.md`. Present a summary to the user highlighting:
- Number of tasks
- Key architectural decisions
- Test strategy
- Estimated complexity
