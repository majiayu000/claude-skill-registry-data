---
name: coding-workflow
description: >
  Pre-implementation checklist, incremental development workflow, and code organization patterns.
  Use before starting implementation to ensure readiness and maintain quality throughout.
---

# coding-workflow

Pre-implementation checklist and incremental development workflow.

## how to use

- `/coding-workflow`
  Apply this workflow to all implementation work in this conversation.

- `/coding-workflow <task>`
  Run through the pre-implementation checklist for the given task.

## when to apply

Reference these guidelines when:
- starting a new feature or significant change
- unsure about approach before writing code
- working on unfamiliar codebase areas
- making changes that touch multiple files
- refactoring existing code

## rule categories by priority

| priority | category | impact |
|----------|----------|--------|
| 1 | pre-implementation | critical |
| 2 | incremental development | critical |
| 3 | code organization | high |
| 4 | change management | medium |

## quick reference

### 1. pre-implementation (critical)

**Before writing any code, verify**:
- [ ] understand the requirement (restate it in your own words)
- [ ] read existing code in the affected area
- [ ] identify all files that will change
- [ ] check for existing patterns to follow
- [ ] verify no duplicate implementation exists
- [ ] understand the test strategy
- [ ] identify potential breaking changes
- [ ] check for related open PRs or in-progress work

**Architecture check**:
- does this belong in an existing module or needs a new one?
- what are the dependencies? Will this create circular dependencies?
- is the change additive (safe) or modifying (riskier)?
- what's the rollback plan if something goes wrong?

### 2. incremental development (critical)

- make the smallest possible change that adds value
- compile/lint after every meaningful edit
- commit after each logical step (not at the end)
- test each change before moving to the next
- keep working code working; never leave things in a broken state

**Progression**:
1. make it work (correct behavior)
2. make it right (clean code, proper patterns)
3. make it fast (optimize only if needed, with measurements)

- resist the urge to refactor unrelated code while implementing
- if you discover technical debt, note it; don't fix it in the same PR
- prefer boring, proven solutions over clever ones

### 3. code organization (high)

- files should have a single responsibility
- group related code by feature, not by type (prefer `user/` over `controllers/`)
- keep files under 300 lines; split if larger
- functions should do one thing; keep under 30 lines
- extract shared logic only when used in 3+ places (Rule of Three)
- name things for what they do, not how they work
- put constants near usage, not in global files (unless truly global)

### 4. change management (medium)

- one concern per PR; don't mix features with refactoring
- write the PR description before or during implementation, not after
- if a change grows beyond expected scope, stop and reassess
- leave the codebase better than you found it, but within scope
- when in doubt, ask before implementing
