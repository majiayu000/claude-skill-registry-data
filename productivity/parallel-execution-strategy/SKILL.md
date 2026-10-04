---
name: parallel-execution-strategy
description: Use when 3+ independent tasks are ready in .forge/tasks.yaml and multiple agents will work concurrently, when assessing file-conflict risk before dispatching parallel work, when planning branch and merge sequencing for a sprint, or when prior parallel runs have caused merge nightmares.
---

# Parallel Execution Strategy

## Overview

Plan parallel agent execution *before* dispatching — so two agents never edit the same file, so integration is verified between merges, and so the merge order is fixed in advance. Output is `.forge/parallel-plan.md` — dependency-free task groups, file-conflict risk per group, branching strategy (one branch per task), PR sequencing, agent isolation (separate worktrees), and integration-test cadence. Pairs with `planning-and-task-breakdown` (the source `tasks.yaml`) and `git-workflow` (the branch and PR mechanics).

## When to Use

- `.forge/tasks.yaml` has 3+ tasks marked ready and they appear independent
- Multiple engineers or agents are about to start work in the same week
- A prior parallel run caused merge conflicts at the end and the team wants a better plan
- A sprint is about to begin and capacity is "split N ways"

## When NOT to Use

- Only one task is ready — sequential is correct
- Tasks form a strict dependency chain — sequential is correct
- The team is two people working on the same file all day — coordinate live, no plan needed

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "We'll just merge at the end" | Merge conflicts at the end compound. Each agent's mental model of the codebase has diverged. Resolving 5 PRs simultaneously is 5x more work than resolving them in sequence. |
| "Agents can share files, git will sort it out" | Git produces unresolvable conflicts when two agents edit the same function with no shared context. The "resolution" is one engineer hand-merging both versions. |
| "We don't need integration tests between merges" | Silent integration failures accumulate. By PR 5, nobody knows which of the previous 4 PRs introduced the bug. |
| "Sequential is safer than parallel" | Sequential wastes parallelizable work. The cost of planning beats the cost of unparallelized execution. |
| "We'll figure out merge order as we go" | First-merger-wins creates rebase chaos. Set the order at dispatch time. |
| "One worktree is fine, agents can take turns" | Agents don't "take turns" — they overwrite each other's working tree state. Each agent needs isolation. |

## Red Flags

- Two ready tasks in `tasks.yaml` that both modify the same file
- Multiple agents about to start in the same git worktree
- No integration test gate between parallel groups
- A "merge day" scheduled at the end of the sprint to resolve everything at once
- Agents dispatched without knowing what the others are touching
- No documented merge order — every PR is "ready when ready"
- A task list that lists modules but not files (file-conflict risk can't be assessed)

## Core Process

### Step 1: Read `.forge/tasks.yaml` and identify dependency-free groups

A task is **dependency-free with another** if both:
1. Their `depends_on` lists do not transitively reference each other
2. Their `files` lists do not intersect

Group dependency-free tasks. Sequence groups by dependency depth.

```
Group 1 (ready now):     T-001, T-003, T-007
Group 2 (after Group 1): T-002, T-004
Group 3 (after Group 2): T-005, T-006
```

### Step 2: Assess file-conflict risk per group

For each group, build a matrix:

|  | T-001 | T-003 | T-007 |
|---|---|---|---|
| `src/auth/session.ts` | ✏️ | | |
| `src/api/users.ts` | | ✏️ | |
| `src/components/Button.tsx` | | | ✏️ |
| `src/types/index.ts` | ✏️ | ✏️ | |

Any row with two ✏️ marks is a conflict. Resolve before dispatch:
- **Split the task** — extract the shared file into its own prerequisite task
- **Sequence** — move one task into a later group
- **Designate a primary** — one task owns the file; the other rebases after

### Step 3: Assign branching strategy

- One branch per task: `task/T-001-session-refresh`
- All branches base off `main` (or the integration branch, if used)
- No long-lived feature branches for parallel work
- Every branch has the task ID and a one-line description in its name

### Step 4: Define PR sequencing and merge order

In `.forge/parallel-plan.md`:

```
Group 1 merge order:
  1. T-001 (touches shared types — must land first)
  2. T-007 (independent UI)
  3. T-003 (rebases on T-001's type changes)

Integration test gate runs between T-001 → T-007 and T-007 → T-003.
```

Merge order is fixed before dispatch. Agents know their PR's position in the queue.

### Step 5: Specify agent isolation

Each agent works in **its own worktree** (or its own clone):

```
~/work/main           # main worktree, integration testing
~/work/T-001          # agent A's worktree
~/work/T-003          # agent B's worktree
~/work/T-007          # agent C's worktree
```

`git worktree add -b task/T-001-session-refresh ~/work/T-001 main`

No agent ever runs in another agent's worktree. No agent ever runs in the main worktree during parallel work.

### Step 6: Set the integration-test cadence

Between every PR merge in a group:
- Pull the latest `main` into the integration worktree
- Run the full test suite (unit + integration + e2e on critical paths)
- Run any contract-conformance tests for the modules that changed
- If green: merge the next PR
- If red: pause dispatch, root-cause, and either revert or push a fix before continuing

Between groups:
- All PRs in the previous group merged and tested green
- The next group's worktrees rebased on the new `main`

### Step 7: Document the plan in `.forge/parallel-plan.md`

Sections:
- Groups and dependency order
- File-conflict matrix per group (resolved)
- Branch naming and base
- Merge order with rationale
- Worktree assignments
- Integration test cadence
- Fallback for conflicts that emerge mid-run

Prepend a `forge:meta` header (`generated_by: parallel-execution-strategy`, `generated_at: <ISO 8601 UTC with Z>`, `content_hash: <sha256 first 8 over THIS file's body, excluding the forge:meta block>`).

**Transitive depends_on:** `parallel-plan.md` builds on `tasks.yaml`, which itself depends on `prd.md`, `architecture.md`, and `contracts/*`. List the full transitive upstream set in `depends_on` (paths only — never hashes) AND capture each upstream's `content_hash` AT generation time in `generated_from`:

```
depends_on: [.forge/prd.md, .forge/architecture.md, .forge/contracts/*, .forge/tasks.yaml]
generated_from:
  .forge/prd.md: <prd.md's content_hash at this moment>
  .forge/architecture.md: <architecture.md's content_hash at this moment>
  .forge/contracts/auth-service.md: <hash>   # one entry per resolved glob match
  .forge/contracts/payment-service.md: <hash>
  .forge/tasks.yaml: <tasks.yaml's content_hash at this moment>
```

Listing only `[.forge/tasks.yaml]` is wrong — if `prd.md` changes but `tasks.yaml` hasn't been re-run yet, `parallel-plan.md` would appear UP_TO_DATE despite the chain being stale. See [forge-dependency-graph: co-output rule](../../references/forge-dependency-graph.md#co-output-rule).

## Verification

- [ ] `.forge/parallel-plan.md` written
- [ ] No two parallel agents touch the same file (matrix verified)
- [ ] Every parallel task has its own branch with the task ID in the name
- [ ] Every agent has its own worktree
- [ ] Merge order is documented for every group
- [ ] Integration test gate defined between every merge
- [ ] Fallback plan exists for mid-run conflict discovery
- [ ] Plan was reviewed before dispatch — no agent starts work until the plan is signed off
