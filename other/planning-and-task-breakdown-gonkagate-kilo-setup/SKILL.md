---
name: planning-and-task-breakdown
description: "Break work into ordered, verifiable tasks. Use when you have a spec or clear requirements and need to turn them into implementable slices with dependencies, checkpoints, acceptance criteria, and explicit verification; especially when the task feels too large to start, the implementation order is unclear, or parallel work may be possible."
---

# Planning and Task Breakdown

## Overview

Decompose work into small, verifiable tasks with explicit acceptance criteria.
Good task breakdown is the difference between an agent that completes work
reliably and one that produces a tangled mess. Every task should be small
enough to implement, test, and verify in a single focused session.

## When to Use

- You have a spec and need to break it into implementable units
- A task feels too large or vague to start
- Work needs to be parallelized across multiple agents or sessions
- You need to communicate scope to a human
- The implementation order is not obvious

**When NOT to use:** Single-file changes with obvious scope, when the spec
already contains well-defined tasks, when the request is still too ambiguous
and should go through `spec-first-brainstorming`, or when deep TypeScript/Node
backend sequencing belongs in `typescript-coder-plan-spec`.

## Repository-Specific Anchors

For `opencode-setup`, start by reading:

- `AGENTS.md`
- `docs/specs/opencode-setup-prd/spec.md`
- the relevant files under `docs/`, `src/`, and `test/`

Keep the current repository truth explicit while planning:

- do not plan as if the installer runtime already exists unless the task is
  specifically about building it
- preserve product and security invariants from `AGENTS.md`, especially around
  config targets, secret handling, and truthful scaffold status
- if the task changes contract, docs, packaging, or mirrored skills, include
  `npm run ci` in the checkpoint plan

## The Planning Process

### Step 1: Enter Plan Mode

Before writing any code, operate in read-only mode:

- Read the spec and relevant codebase sections
- Identify existing patterns and conventions
- Map dependencies between components
- Note risks and unknowns

**Do NOT write code during planning.** The output is a plan document, not
implementation.

### Step 2: Identify the Dependency Graph

Map what depends on what:

```text
Product contract / repo truth
    |
    +- docs and CLI contract
    |      |
    |      +- runtime entrypoints and reserved install surfaces
    |      |      |
    |      |      +- tests and verification
    |      |
    |      +- contributor-facing guidance
    |
    +- security invariants / config layering
```

Implementation order follows the dependency graph bottom-up: build foundations
first.

### Step 3: Slice Vertically

Instead of planning all docs first, then all code, then all tests, prefer one
complete slice at a time when possible.

**Bad (horizontal slicing):**

```text
Task 1: Update all docs
Task 2: Implement all runtime code
Task 3: Update all tests
Task 4: Reconcile everything later
```

**Good (vertical slicing):**

```text
Task 1: Add the new config contract and the tests that pin it
Task 2: Implement the CLI behavior for that contract
Task 3: Update README and security docs to match shipped behavior
Task 4: Run full verification and fix drift
```

Each slice should leave the repository in a more truthful, testable state.

### Step 4: Write Tasks

Each task follows this structure:

```markdown
## Task [N]: [Short descriptive title]

**Description:** One paragraph explaining what this task accomplishes.

**Acceptance criteria:**

- [ ] [Specific, testable condition]
- [ ] [Specific, testable condition]

**Verification:**

- [ ] Tests pass: [command]
- [ ] Build or contract checks pass: [command]
- [ ] Manual check: [description of what to verify]

**Dependencies:** [Task numbers this depends on, or "None"]

**Files likely touched:**

- `src/path/to/file.ts`
- `test/path/to/test.ts`

**Estimated scope:** [Small: 1-2 files | Medium: 3-5 files | Large: 5+ files]
```

For this repository, default to repo-real commands such as `npm run ci` when a
task changes the public contract or mirrored skill pack.

### Step 5: Order and Checkpoint

Arrange tasks so that:

1. Dependencies are satisfied first
2. Each task leaves the system in a working state
3. Verification checkpoints occur after every `2-3` tasks
4. High-risk or high-reversal-cost tasks happen early

Add explicit checkpoints:

```markdown
## Checkpoint: After Tasks 1-3

- [ ] Focused tests pass
- [ ] `npm run ci` passes when contract surfaces changed
- [ ] Docs and implementation still describe the same truth
- [ ] Review with a human before proceeding
```

## Task Sizing Guidelines

| Size   | Files | Scope                                | Example                                                      |
| ------ | ----- | ------------------------------------ | ------------------------------------------------------------ |
| **XS** | 1     | Single function or config change     | Tighten one CLI validation rule                              |
| **S**  | 1-2   | One component, test, or doc slice    | Add one skill contract test                                  |
| **M**  | 3-5   | One feature slice                    | Add one new installer capability with docs and tests         |
| **L**  | 5-8   | Multi-surface feature                | Introduce managed config writes across code, docs, and tests |
| **XL** | 8+    | **Too large; break it down further** | —                                                            |

If a task is `L` or larger, it should be broken into smaller tasks. An agent
performs best on `S` and `M` tasks.

**When to break a task down further:**

- It would take more than one focused session, roughly `2+` hours of agent work
- You cannot describe the acceptance criteria in `3` or fewer bullet points
- It touches two or more independent subsystems
- You find yourself writing `and` in the task title

## Plan Document Template

```markdown
# Implementation Plan: [Feature or Project Name]

## Overview

[One paragraph summary of what we are building]

## Architecture Decisions

- [Key decision 1 and rationale]
- [Key decision 2 and rationale]

## Repository Truth To Preserve

- [Current scaffold truth that must stay accurate]
- [Security or config invariant that constrains the work]

## Task List

### Phase 1: Foundation

- [ ] Task 1: ...
- [ ] Task 2: ...

### Checkpoint: Foundation

- [ ] Focused checks pass

### Phase 2: Core Changes

- [ ] Task 3: ...
- [ ] Task 4: ...

### Checkpoint: Core Changes

- [ ] End-to-end or contract flow works

### Phase 3: Truthfulness and Polish

- [ ] Task 5: ...
- [ ] Task 6: ...

### Checkpoint: Complete

- [ ] All acceptance criteria met
- [ ] `npm run ci` passes when required
- [ ] Ready for review

## Risks and Mitigations

| Risk   | Impact         | Mitigation |
| ------ | -------------- | ---------- |
| [Risk] | [High/Med/Low] | [Strategy] |

## Open Questions

- [Question needing human input]
```

## Parallelization Opportunities

When multiple agents or sessions are available:

- **Safe to parallelize:** Independent feature slices, tests for
  already-implemented features, documentation
- **Must be sequential:** Shared config contract changes, dependency chains,
  any step that redefines repository truth
- **Needs coordination:** Features that share a public CLI or config contract;
  define the contract first, then parallelize

## Common Rationalizations

| Rationalization                | Reality                                                                                      |
| ------------------------------ | -------------------------------------------------------------------------------------------- |
| "I'll figure it out as I go"   | That is how you end up with a tangled mess and rework. Ten minutes of planning saves hours.  |
| "The tasks are obvious"        | Write them down anyway. Explicit tasks surface hidden dependencies and forgotten edge cases. |
| "Planning is overhead"         | Planning is the task. Implementation without a plan is just typing.                          |
| "I can hold it all in my head" | Context windows are finite. Written plans survive session boundaries and compaction.         |

## Red Flags

- Starting implementation without a written task list
- Tasks that say `implement the feature` without acceptance criteria
- No verification steps in the plan
- All tasks are `XL` sized
- No checkpoints between tasks
- Dependency order is not considered
- Planning that contradicts `AGENTS.md` about current scaffold truth or
  security invariants

## Verification

Before starting implementation, confirm:

- [ ] Every task has acceptance criteria
- [ ] Every task has a verification step
- [ ] Task dependencies are identified and ordered correctly
- [ ] No task touches more than about `5` files unless there is a stated reason
- [ ] Checkpoints exist between major phases
- [ ] The plan stays truthful to current `opencode-setup` reality
- [ ] The human has reviewed and approved the plan
