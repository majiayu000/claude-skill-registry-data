---
name: creating-a-plan
description: Creates a comprehensive easy to follow plan for building out a design. Use when creating an implementation plan from a design.
---

## Overview

Write a comprehensive implementation plan

- Assume the implementor has zero context for the codebase
- Assume the implementor is a skilled developer
- Document everything they would need to know
  - files that will be touched
  - useful reference code, unit tests, and docs
  - how to test changes
- Save all markdown docs next to the provided design
- Construct the plan as bite-sized tasks

## Plan structure

- Write the plan to `plan.md` next to the design
- Fill out the [plan template](./PLAN.md)

## Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Task Batches

- Group tasks into coherent batches
- Write each batch to its own file, `batch-<number>.md`, next to the plan and design
- Use the [batch template](./BATCH.md)
- Always use exact file paths
- Always use code snippets and not ambiguous instructions like "add validation"
- Always use exact commands with expected output
- Batches should be incremental and build on each other. Batch 1 must be implemented before batch 2

**REMEMBER**:
- DRY
- YAGNI
- TDD
- frequent commits
