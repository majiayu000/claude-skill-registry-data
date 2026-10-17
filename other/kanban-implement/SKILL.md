---
name: kanban-implement
description: 'Implement an approved kanban feature or bug, track tasks and verify the build. Use in implementation, or after an explicit start decision from planning/backlog or a FAIL/REJECT repair loop.'
---

# Kanban Phase 3 — Implement (Autonomous)

Argument: `<feature_name>`.

Execute the approved implementation plan for a feature, or the approved bug report's fix scope and regression strategy for a bug. If implementation requires a scope change, explain it and obtain the user's decision before revising the contract.

**Invoked through `kf run`?** If your prompt starts with `kf-run:`, you are a worker for this stage only: skip the "move to stage" step below, never run `kf stage` / `kf approve` / `kf archive` / `kf run`, never edit approved contract artifacts, do not commit, and end your final message with two lines exactly: `STATUS: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT` and `Summary: <one or two sentences>`. The main agent reads them and decides the transition.

---

## 1. Move to implementation

Read `kf status --change {feature_name}`. Move only when coming from planning or backlog with a valid approval, or when a FAIL/REJECT report requires a loop. If already in implementation, skip the move and resume existing tasks. If approval changed, stop and return to planning on the user's direction. Entering implementation from backlog requires the user's explicit start decision.

```bash
kf stage {feature_name} implementation
```

**Worktree:** when the project has `worktree.enabled` (default), entering implementation provisions a git worktree + a `.<tld>` domain for the item — `kf status --change {feature_name}` prints `Worktree:` (path), `Domain:` (`http://<feature>.<baseDomain>`) and the direct `127.0.0.1:<port>` fallback. **All code work happens inside that worktree on branch `kf/<feature>` — never on the user's main checkout.** Commit your changes there; the merge back is the human's call, not yours. `.works/` artifacts and `kf` commands keep working from inside the worktree (project root resolves through the git common dir). If domain DNS is not set up on the machine yet, the direct `127.0.0.1:<port>` URL always works; `kf worktree setup` (sudo, once) fixes the domain. A project `worktree-create.sh` hook may already have installed deps and seeded `.env` — check before re-installing.

Create tasks.md if missing: `- [ ] 1. ...` checkboxes mapping tasks to the approved test cases for a feature, or reproduction/acceptance/regression scope in the bug report for a bug. Preserve completed tasks on resume; add the required fix tasks when looping. Record the starting HEAD and pre-existing working-tree changes in a `## Baseline` section at the top of `tasks.md` so review can distinguish this work item's changes. When a worktree exists, the baseline HEAD is the `kf/<feature>` branch point, recorded from inside the worktree.

## 2. Work by dependency order

- Independent tasks → **parallelize via subagents**.
- Sequential / dependent tasks → main agent.

**Subagent prompt contract** — every subagent prompt must state:

- Task: the exact task + the TC it must satisfy
- Files to read: plan excerpt, reference files, repo conventions
- Files it may modify: explicit allowlist — nothing else
- Acceptance criteria: what "done" means, verifiable
- Constraints: no contract changes, no unrelated edits
- Context: `.works/implementation/{feature}/` path (and reports path when applicable)

**Subagent status protocol** — require every subagent to end with:

```text
Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
Summary: one or two sentences
Concerns/Blockers: (optional)
```

Treat `DONE_WITH_CONCERNS` and `BLOCKED` as not-done: resolve the concern or unblock before ticking the task.

## 3. Tick tasks as they land; gate on build

```bash
{build_command}
```

- PASS → continue.
- FAIL → analyze, fix, re-run.
- Failed again → STOP, show error, ask.

When all tasks ticked, run the FULL build (not just the touched module).

Do not modify the approved requirement, plan or test-case contract. Project-specific permissions for database operations and other external actions still apply.

---

## Done

All tasks done, build green, no test regressions. Hand off:

```text
Load the kanban-test skill and move the feature to testing.
```
