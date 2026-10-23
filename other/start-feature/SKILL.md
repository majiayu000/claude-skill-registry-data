---
name: start-feature
description: Use when a feature starts, before any code, to create the isolated worktree the rest of the pipeline runs in — plain git by default, with an optional local orchestrator for port allocation. One task, one worktree.
---

# start-feature

Step 0 of the pipeline (`WORKFLOW.md`). A feature gets its **own worktree**, so two tasks never share a
working copy and an unfinished change never leaks into an unrelated review.

## When
Before the first line of code on a new feature, fix or spike. Not for a one-line change on a branch
you're already on.

## Steps

### 1. Identify the work
1. **The project**: the git remote (`git config --get remote.origin.url`), or the repo root.
2. **The base branch** the feature starts from, read rather than assumed — starting from a stale base is
   discovered at merge, expensively.
3. **The branch name**, in the team's convention.

### 2. Create the worktree
1. `git worktree add <sibling-path> -b <branch>` from the base branch, in a **sibling folder**, never
   inside the current working copy.
2. **Check the worktree path is ignored** (or outside the repo), otherwise the next `git status` is
   unreadable.
3. **Copy the local environment file across unmodified** where the project needs one. Don't hand-edit it:
   an existing worktree of the same project is the reference for what it should contain.
4. **One task per worktree.** Two features in one worktree is the failure this step exists to prevent —
   the diffs mix, and the review sees both.

### 3. Ports, when the project serves something
Several worktrees of the same project can't bind the same port.
1. **Prefer a project that doesn't care** — a stack whose port is dynamic or aliased needs no allocation
   at all (`skills/portless-ready`).
2. Otherwise **allocate deterministically** and write the port into the worktree's own environment, so
   restarting doesn't reshuffle it.
3. **An orchestrator is optional here, never required.** Where a local tool manages tasks, ports and a
   dashboard, use it — but the plain-git path above must keep working on its own. A pipeline whose first
   step needs a tool nobody else has isn't shareable, and rule B forbids depending on one at runtime
   (`CONVENTIONS.md`).

### 4. Hand over to the pipeline
1. Go to `brainstorm` (1) then `spec` (2).
2. Record the checkpoint as each step clears (`WORKFLOW.md` §5).
3. **Don't remove the worktree by hand** at the end: `finish` (11) does it after the merge and updates the
   base branch.

## Output / checkpoint
An isolated worktree on a fresh branch off an up-to-date base, its environment file in place, its port
question settled, and the pipeline entered at step 1.

## Guardrails
- **Never start a second task in an existing worktree**, however small it looks.
- **Never create the worktree inside the current working copy**, and never in a temp folder that gets
  cleaned up under you.
- **Never hand-edit the copied environment file**; copy it as it is and check an existing worktree if
  unsure.
- **Never make this step depend on a local orchestrator.** Optional means the plain-git path is tested.
- Never branch off a base you haven't refreshed.

## Origin
Rewrite of `using-git-worktrees` from the framework this repo responds to: worktree isolation per task,
sibling folder, cleanup at the end. What's ours: one task per worktree stated as a guardrail rather than a
convention, the environment-file copy rule (a real recurring cost on our stacks), and the port question
kept as a *question* — an earlier version of this block called a local orchestrator's MCP tools directly,
which made step 0 undistributable and broke rule B. Corrected 2026-08-06.
