---
name: plan-tree-workflow
description: Use when creating, executing, resuming, reviewing, or compacting a complex multi-stage plan that must survive context compaction, agent handoff, or staged commits. Organizes work as a repo-local execution tree under tasks/{task_name}_{YYYYMMDD_HHmm}/ with tree.yml, uniform node files, evidence, validation records, active-node state, gates, and commit slices.
metadata:
  short-description: Manage complex work as a resumable plan tree
---

# Plan Tree Workflow

Use this skill for complex work where progress cannot live only in chat context. The output is a repo-local execution tree: `tree.yml` is the authoritative state index, and every plan node uses the same five-section template.

## Core Rule

A complex plan is a recoverable execution tree:

- `tree.yml` stores global state, active node, node paths, and resume commands.
- Every node file has exactly these sections: `Intent`, `Plan`, `State`, `Evidence`, `Gate`.
- Bulky logs, RCA, screenshots, rollout analysis, and test records go under `evidence/` or `validation/`, not inside node files.
- Before compaction, pause, handoff, or final response after substantial work, update `tree.yml` and the active node `State`.
- A node is not `done` until its `Gate` records the verification result and commit slice.

## Layout

Create one folder per plan:

```text
tasks/{task_name}_{YYYYMMDD_HHmm}/
  tree.yml
  nodes/
    root.md
    01-stage-name.md
    02-stage-name.md
  evidence/
  validation/
```

Use `assets/tree.yml` and `assets/node.md` as templates when starting a new plan tree.

## Node Template

All nodes, including `root.md`, use the same shape:

```markdown
# Node: {node_id}

## Intent

What this node solves, the key constraints, and the desired end state.

## Plan

- Ordered local steps or child nodes.

## State

status: pending
last: none
next: define first concrete action
blocker: none

## Evidence

- none

## Gate

- verification: pending
- commit: pending
- include: pending
- exclude: pending
```

Keep `State` short. Detailed reasoning belongs in `Evidence`.

## Status Values

Use only:

- `pending`: known but not expanded enough to execute.
- `ready`: clear enough to start.
- `in_progress`: currently active.
- `review_ready`: implementation done, awaiting review, verification, or commit.
- `done`: gate passed and commit slice recorded.
- `blocked`: cannot proceed without a decision or missing dependency.

There must be at most one `in_progress` node unless the user explicitly asks for parallel implementation.

## Start A Plan

1. Create the plan folder under `tasks/{task_name}_{YYYYMMDD_HHmm}/`.
2. Create `tree.yml`, `nodes/root.md`, and child node files.
3. In `tree.yml`, set `active` to `root` or the first executable node.
4. In `root.md`, define the global problem, root contract, decomposition, and global gate using the same five sections.
5. Mark only nodes with sufficient scope and gate as `ready`; leave vague nodes `pending`.

Do not create an extra outer master document unless the user explicitly asks for one. The plan folder is the unit.

## Execute A Node

Before editing production code:

1. Read `tree.yml`.
2. Read the active node.
3. Confirm the node `Intent`, allowed scope in `Plan`, and `Gate`.
4. Update the active node `State` with the intended next action if it is stale.

During work:

- Put task-local notes, RCA, logs, or command output summaries in `evidence/` or `validation/`.
- Keep node files compact and operational.
- If implementation reality invalidates the plan, update the node before continuing.

When a node is complete:

1. Record verification command and result in `Gate`.
2. Record the commit slice: message, include paths, exclude paths.
3. Set node status to `done` in both node `State` and `tree.yml`.
4. Move `active` to the next executable node.

## Resume Protocol

On resume, compact recovery, or handoff, do not reread the whole plan first.

Read only:

1. `tree.yml`
2. the active node path from `tree.yml`
3. `git status --short`
4. `git diff --stat`

Expand to sibling nodes, evidence, full diffs, or code only if those four inputs are inconsistent or insufficient.

## Review Protocol

For review, lead with state integrity:

1. Does `tree.yml` match node `State`?
2. Is there exactly one active/in-progress node?
3. Does every `done` node have a verification result and commit slice?
4. Does the diff match the active node's intended scope?
5. Are blockers or semantic gaps recorded instead of hidden in chat?

Then review implementation correctness.

## Compaction And Handoff

Before stopping substantial work:

- Update `updated_at` in `tree.yml`.
- Update active node `State.last`, `State.next`, and `State.blocker`.
- Add or update a short `validation/` record if commands were run.
- Make sure the final response names the plan folder and active node.

The goal is that the next agent can continue from the folder without reconstructing state from conversation history.
