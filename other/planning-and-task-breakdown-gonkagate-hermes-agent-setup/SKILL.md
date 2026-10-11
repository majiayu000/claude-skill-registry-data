---
name: planning-and-task-breakdown
description: "Break work into ordered, verifiable tasks for `hermes-agent-setup`. Use when you have a spec or clear requirements and need to turn them into implementable slices while preserving current shipped-runtime truth, GonkaGate/Hermes product invariants, dependencies, checkpoints, acceptance criteria, and explicit verification."
---

# Planning and Task Breakdown

## Overview

Decompose work into small, verifiable tasks with explicit acceptance criteria.
Good task breakdown is the difference between an agent that completes work
reliably and one that produces a tangled mess. Every task should be small
enough to implement, test, and verify in a single focused session.

For `hermes-agent-setup`, planning must stay anchored to repository truth:

- this repository ships `npx @gonkagate/hermes-agent-setup` as the public
  onboarding helper
- the public installer runtime is implemented
- the current CLI is a shipped entrypoint backed by runtime modules, checked-in
  launch qualification artifacts, and contract tests
- plans must preserve the current GonkaGate/Hermes product contract unless the
  task is explicitly about changing that contract

## When to Use

- You have a spec and need to break it into implementable units
- A task feels too large or vague to start
- Work needs to be parallelized across multiple agents or sessions
- You need to communicate scope and sequencing to a human
- The implementation order is not obvious
- A change crosses docs, CLI, packaging, tests, or mirrored skills and you need
  to keep repository truth aligned

**When NOT to use:** Single-file changes with obvious scope, when the spec
already contains well-defined tasks, when the request is still too ambiguous
and should go through `spec-first-brainstorming`, or when deep TypeScript/Node
execution sequencing belongs in `typescript-coder-plan-spec`.

## Repository-Specific Anchors

Before writing a plan, read the repository surfaces that define current truth:

- `AGENTS.md`
- `docs/specs/hermes-agent-setup-prd/spec.md`
- `README.md`
- `package.json`
- the relevant files under `docs/`, `src/`, `test/`, `.agents/skills/`, and
  `.claude/skills/`

Keep these invariants explicit in the plan whenever they matter:

- the intended public entrypoint is `npx @gonkagate/hermes-agent-setup`
- the installed primary bin is `hermes-agent-setup`
- the intended integration path is the named custom provider
  `gonkagate`
- the canonical GonkaGate base URL is `https://api.gonkagate.com/v1`
- secrets belong in `~/.hermes/.env`, not in `~/.hermes/config.yaml`
- shell profile mutation and arbitrary custom base URLs are out of scope for
  the public flow
- public positioning must stay truthful about current GonkaGate availability
  boundaries, including the non-U.S. launch positioning captured in
  `AGENTS.md`
- mirrored contributor skills under `.agents/skills/` and `.claude/skills/`
  must stay aligned

If a task changes package metadata, public CLI behavior, contributor skills, or
docs that describe shipped behavior, include `npm run ci` in the plan.

## The Planning Process

### Step 1: Enter Plan Mode

Before writing any code, operate in read-only mode:

- Read the spec and relevant codebase sections
- Identify existing patterns and conventions
- Map dependencies between components
- Note risks, scope boundaries, and repository-truth constraints

**Do NOT write code during planning.** The output is a plan document, not
implementation.

### Step 2: Identify the Dependency Graph

Map what depends on what:

```text
Repository truth / PRD contract
    |
    +- package metadata, bins, and CLI contract
    |       |
    |       +- runtime seams and constants
    |       |       |
    |       |       +- tests and verification
    |       |
    |       +- README, docs, and contributor guidance
    |
    +- Hermes/GonkaGate security and config invariants
    |
    +- mirrored contributor skills and contract tests
```

Implementation order follows the dependency graph bottom-up: lock the contract,
then build the behavior, then reconcile docs/tests/skills so they all describe
the same truth.

### Step 3: Slice Vertically

Instead of updating all docs first, then all code, then all tests, prefer one
complete slice at a time when possible.

**Bad (horizontal slicing):**

```text
Task 1: Rewrite all docs
Task 2: Implement all runtime helpers
Task 3: Update all tests
Task 4: Reconcile package and skill drift later
```

**Good (vertical slicing):**

```text
Task 1: Add one Hermes/GonkaGate contract slice and the tests that pin it
Task 2: Implement the CLI behavior for that slice
Task 3: Update README/docs/skills so shipped behavior stays truthful
Task 4: Run npm run ci and fix any drift across package, docs, and mirrors
```

Each slice should leave the repository in a more truthful, testable state than
before.

### Step 4: Write Tasks

Each task follows this structure:

```markdown
## Task [N]: [Short descriptive title]

**Description:** One paragraph explaining what this task accomplishes.

**Acceptance criteria:**

- [ ] [Specific, testable condition]
- [ ] [Specific, testable condition]

**Verification:**

- [ ] Typecheck passes: `npm run typecheck`
- [ ] Tests pass: `npm test`
- [ ] Full repo contract passes when needed: `npm run ci`
- [ ] Manual check: [description of what to verify]

**Dependencies:** [Task numbers this depends on, or "None"]

**Files likely touched:**

- `src/path/to/file.ts`
- `test/path/to/test.ts`

**Estimated scope:** [XS: 1 file | S: 1-2 files | M: 3-5 files | L: 5-8 files]
```

Use repository-real verification commands. If the task changes public contract
surfaces, packaging, release-facing docs, or mirrored skills, do not stop at
`npm test`; include `npm run ci`.

### Step 5: Order and Checkpoint

Arrange tasks so that:

1. Repository truth and public contract decisions are settled first
2. Each task leaves the system in a working state
3. Verification checkpoints occur after every `2-3` tasks
4. High-risk or high-reversal-cost work happens early

Add explicit checkpoints:

```markdown
## Checkpoint: After Tasks 1-3

- [ ] `npm run typecheck` passes
- [ ] `npm test` passes
- [ ] `npm run ci` passes when public contract surfaces changed
- [ ] README, AGENTS, docs, CLI, and tests still describe the same truth
- [ ] Review with a human before proceeding
```

## Task Sizing Guidelines

| Size   | Files | Scope                                            | Example                                                                       |
| ------ | ----- | ------------------------------------------------ | ----------------------------------------------------------------------------- |
| **XS** | 1     | One targeted doc, constant, or validation change | Tighten one contract literal in a skill or CLI message                        |
| **S**  | 1-2   | One focused component, test, or skill slice      | Adapt one mirrored skill and add its contract test                            |
| **M**  | 3-5   | One complete feature slice                       | Add one CLI onboarding step with tests and docs                               |
| **L**  | 5-8   | Multi-surface feature                            | Introduce one new Hermes config-management slice across code, docs, and tests |
| **XL** | 8+    | **Too large; break it down further**             | —                                                                             |

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

- [Current shipped-runtime truth that must stay accurate]
- [Hermes/GonkaGate security or product invariant that constrains the work]

## Task List

### Phase 1: Foundation

- [ ] Task 1: ...
- [ ] Task 2: ...

### Checkpoint: Foundation

- [ ] `npm run typecheck` passes
- [ ] Focused checks pass

### Phase 2: Core Slice

- [ ] Task 3: ...
- [ ] Task 4: ...

### Checkpoint: Core Slice

- [ ] `npm test` passes
- [ ] Core behavior or contract flow works

### Phase 3: Truthfulness and Release Surfaces

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

- **Safe to parallelize:** Independent documentation slices, tests for
  already-implemented behavior, and mirrored follow-up updates once the shared
  contract is fixed
- **Must be sequential:** Changes to package metadata, public CLI contract,
  Hermes/GonkaGate config semantics, or any step that redefines repository
  truth
- **Needs coordination:** Work that touches the same public files or mirrored
  skill pair; define the contract first, then parallelize the dependent slices

## Common Rationalizations

| Rationalization                                      | Reality                                                                                                                                       |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| "I'll figure it out as I go"                         | That is how you end up with a tangled mess and rework. Ten minutes of planning saves hours.                                                   |
| "The tasks are obvious"                              | Write them down anyway. Explicit tasks surface hidden dependencies and forgotten edge cases.                                                  |
| "Planning is overhead"                               | Planning is the task. Implementation without a plan is just typing.                                                                           |
| "The runtime already ships, so planning is optional" | Shipped repos still have contracts, release surfaces, and truthfulness requirements. Planning keeps changes aligned with the helper contract. |
| "I can hold it all in my head"                       | Context windows are finite. Written plans survive session boundaries and compaction.                                                          |

## Red Flags

- Starting implementation without a written task list
- Tasks that say `implement the feature` without acceptance criteria
- No verification steps in the plan
- All tasks are `XL` sized
- No checkpoints between tasks
- Dependency order is not considered
- Planning as if shipped behavior covers unsupported or unqualified scenarios
- Planning that stores GonkaGate secrets in `~/.hermes/config.yaml` or quietly
  changes product invariants without calling it out
- Updating only one of `.agents/skills/` or `.claude/skills/` for a mirrored
  skill change

## Verification

Before starting implementation, confirm:

- [ ] Every task has acceptance criteria
- [ ] Every task has a verification step
- [ ] Task dependencies are identified and ordered correctly
- [ ] No task touches more than about `5` files unless there is a stated reason
- [ ] Checkpoints exist between major phases
- [ ] The plan stays truthful to current `hermes-agent-setup` reality
- [ ] The plan preserves relevant repository invariants such as
      `gonkagate`, `https://api.gonkagate.com/v1`, and keeping secrets
      in `~/.hermes/.env`
- [ ] Mirrored skill changes update both `.agents/skills/` and
      `.claude/skills/` when applicable
- [ ] The human has reviewed and approved the plan
