---
name: task-workflow
description: Core loop for executing tasks from the tasks.md board — claim, plan checkpoint, worktree, implement, quality gates, draft PR, bounded review-and-fix rounds, optional gated merge, human notification. Use whenever asked to work the task board, run the next task, or continue a task in progress.
---

# Task Workflow

The process for taking one task from `tasks.md` to a reviewed draft PR. One run
of this skill advances exactly one task as far as it can go, then stops.

## Board rules (non-negotiable)

1. **tasks.md has one writer.** All board edits (claims, status changes, plan
   comments) happen in the MAIN repo checkout, in manager context. Implementation
   agents working in worktrees NEVER edit tasks.md — their copy is stale by design.
2. **No agent-to-agent conversation.** Agents communicate only through artifacts:
   task status, plan comments on the board, the PR diff, and PR review comments.
3. **PRs are always draft, and merging is off by default.** Never mark a PR ready
   for review, never push to the base branch. Merge only when `AUTO_MERGE=gated`
   and every condition in step 9 holds — otherwise the human merges.
4. **Every stop notifies the human** (see Notification below).
5. **One driver at a time.** `/task-next` and `/task-auto` both claim "the first
   actionable task". Running both against one board is a claim race. Pick one.

## Knobs

`workflow/.env` at the repo root holds the developer's preferences. Read it at the
start of every run; missing or unparseable → use these defaults, always with
`AUTO_MERGE=off`. The `requirement-intake` skill creates the file on first run.

| key | default | effect |
|---|---|---|
| `PLAN_GATE` | `medium` | which plan sizes stop for approval |
| `AUTO_MERGE` | `off` | `off` \| `gated` — see step 9 |
| `MERGE_TARGET` | `develop` | branch a gated merge targets |
| `MAX_REVIEW_ROUNDS` | `3` | reviewer FAIL → fix → re-review cycles before `blocked` |
| `MAX_FIX_CYCLES` | `2` | gate failures fed back to the implementer, per round |
| `NOTIFY` | `osascript` | notification mechanism |

## Task format

```
- [ ] TASK-12 [backend] Add invoice export endpoint with test — status: todo
- [ ] TASK-13 Operator gets a daily digest of new replies — status: todo
      grouped by niche, each reply linked to its business page
```

- Tag in `[...]` selects the implementation agent (`backend`, `frontend`, …).
- **No tag = a requirement, not a task.** It goes to requirement intake first, and
  gets its tag from the resulting plan. Title on the line, description indented.
- Statuses: `todo → planning → (needs-answer) → plan-review → doing → review → done`,
  plus `blocked` (terminal until a human intervenes).
- Plan comments, questions, answers, and block reasons are indented lines under
  the task. Verbose artifacts live in `workflow/<TASK-id>-<slug>/` and are linked
  from the board, never pasted into it.
- The board header may contain a config block:
  ```
  <!-- task-agent:config
  plan_checkpoint: on
  -->
  ```
  `plan_checkpoint: off` skips steps 2–3 (trusted recipe tasks).

## The loop

### 1. Claim
Find the first actionable task, in priority order:
- a `review` task whose reviewer verdict was FAIL and whose round count is below
  `MAX_REVIEW_ROUNDS` → continue at step 8
- a `plan-review` task whose plan comment has an `approved: yes` line → continue at step 4
- a `needs-answer` task whose questions block has an `answered: yes` line →
  continue at the requirement-intake skill. **Without that line the task is not
  actionable** — it is waiting on a human, exactly like `plan-review`. Never
  resume it on the strength of an empty answer.
- a `doing` task (crashed/interrupted run) → resume at step 5 in its existing worktree
- a `planning` task (crashed/interrupted run) → restart its planning phase: the
  `requirement-intake` skill if untagged, step 2 if tagged
- the first `todo` task:
  - **untagged** → set `status: planning` and run the `requirement-intake` skill
    now, in this run, until it reaches its own stop (`needs-answer`,
    `plan-review`, or `doing`). Requirement intake is one phase, not a status to
    park in.
  - **tagged** → set `status: planning`, continue at step 2

No actionable task → report the board state and stop. If a task's tag is present
but matches no known agent, set `status: blocked` with reason `unknown tag`,
notify, and stop. A *missing* tag is never `unknown tag` — it is a requirement.

### 2. Plan
Read the task, relevant human docs (`docs/requirements.md`, `docs/conventions.md`,
and for `[frontend]` also `docs/ux_design.md`, `docs/information_architecture.md`
— only the ones that exist), and inspect the app via Laravel Boost MCP tools
(schema, routes, existing code) rather than assumptions. Produce a short plan:
files to touch, migration/route/test outline, open questions.

### 3. Plan checkpoint
Write the plan as indented comment lines under the task, set
`status: plan-review`, notify the human, and STOP:

```
- [ ] TASK-12 [backend] Add invoice export endpoint — status: plan-review
      plan:
      - migration: add exported_at to invoices
      - POST /invoices/{id}/export route + controller + Pest feature test
      approved:
```

The human edits the plan if needed and sets `approved: yes`. The next run picks
it up in step 1. (`plan_checkpoint: off` → skip straight to step 4.)

### 4. Workspace
From the main checkout: first confirm the base branch has no commits missing
from `origin` (`git log origin/<base>..<base>`). Unpushed commits would bleed
into the PR diff — push the base first if they are board/docs commits from
init; anything else → `blocked` for a human. Then:
```
git worktree add ../<repo-name>-worktrees/TASK-<n> -b task/TASK-<n>
```
Set `status: doing` on the board. All implementation happens inside the worktree.

Ensure `workflow/TASK-<n>-<slug>/state.md` exists in the MAIN checkout (create it
if intake never ran). It carries what the board should not:
```yaml
size: MEDIUM
round: 0
branch: task/TASK-31
worktree: /abs/path/to/my-store-worktrees/TASK-31
pr:
```

### 5. Implement
Delegate to the tag-matched agent (e.g. `backend`) with: the task line, the
approved plan, and the worktree path as working directory. The agent implements
the plan, writing tests alongside code, using Boost MCP for schema/route/docs
lookups. It must not touch tasks.md, other tasks' code, or the base branch.

**`workflow/` is gitignored, so it does not exist inside the worktree.** Pass the
plan and any delta files by ABSOLUTE path
(`/abs/path/to/my-store/workflow/TASK-31-reply-digest/plan.md`), never relative.
An agent that cannot find its plan invents one.

For a LARGE task, the same agent applies `architecture-delta.md` and
`system-model-delta.md` to `tasks/architecture.md` / `tasks/system_model.md`
inside the worktree, so the doc change is reviewed in the same PR as the code.

### 6. Gates
Inside the worktree, run in order, skipping tools that are not installed:
```
vendor/bin/pint --test
vendor/bin/phpstan analyse   (if phpstan present)
php artisan test
```
On failure: feed the exact failure output back to the implementation agent to
fix, then re-run the gates. **Maximum `MAX_FIX_CYCLES` (default 2).** Still
failing → set `status: blocked` with the last failure summary as an indented
comment, notify, leave the worktree intact for a human, and STOP.

### 7. Ship for review
Before committing, confirm the export rule (see `requirement-intake`): the PR body
carries the requirement text, the plan, and the assumptions; behavior changes that
an operator can see come with updated manual test cases.
```
git add -A && git commit -m "TASK-<n>: <task title>"
git push -u origin task/TASK-<n>
gh pr create --draft --title "TASK-<n>: <task title>" --body "<requirement + plan + assumptions + summary>. Closes from tasks.md TASK-<n>."
```
Set `status: review` with the PR URL as an indented comment, and record the PR in
`state.md`. Then continue at step 8.

### 8. Review rounds
Run the `review` skill against the PR (reviewer agent), writing its report to
`workflow/TASK-<n>-<slug>/review-<round+1>.md`. Then:

- **PASS** → continue at step 9.
- **FAIL** and `round < MAX_REVIEW_ROUNDS` → increment `round` in `state.md`, hand
  the findings back to the same implementation agent in the same worktree, then
  re-run step 6 and step 8. The board stays at `status: review` with an indented
  `round: <n>` comment.
- **FAIL** and `round >= MAX_REVIEW_ROUNDS` → `status: blocked` with the last
  review summary, notify, worktree intact, STOP. This is a human's job now.

Two rules keep rounds from running forever:

1. **Round 2 and later review the fixes, not the PR afresh.** The reviewer
   verifies the previous round's findings are resolved and looks for regressions
   introduced by the fixes. Nothing else.
2. **New findings unrelated to the previous round go to
   `workflow/TASK-<n>-<slug>/backlog.md`**, not into this PR. Report them in the
   final summary so the human can seed follow-up tasks.

### 9. Finish
`AUTO_MERGE=off` (default) → set `status: done`, note "ready for human merge",
notify, STOP. The PR stays draft.

`AUTO_MERGE=gated` → merge into `MERGE_TARGET` only if **every** condition holds:

- reviewer verdict is PASS
- `round <= MAX_REVIEW_ROUNDS`
- all gates green on the final commit
- the diff contains no migration
- the diff touches nothing under a path the project marks irreversible —
  by default anything matching `*/Sending/*`, `*/Shared/*`, `*/Billing/*`,
  `*/Payment/*`, plus any path listed in a board config `protected:` line
- `size` in `state.md` is not `LARGE`

Any condition failing → treat exactly as `AUTO_MERGE=off`, and say which condition
stopped it. Then:
```
gh pr ready <number> && gh pr merge <number> --squash --delete-branch
git worktree remove ../<repo-name>-worktrees/TASK-<n>
```
Set `status: done` with the merge commit, notify.

Never merge to the repository's default branch by this path, whatever
`MERGE_TARGET` says — if `MERGE_TARGET` resolves to the default branch, downgrade
to `AUTO_MERGE=off` and say so.

### 10. Notify
Every terminal state of a run (`needs-answer`, `plan-review`, `review`, `done`,
`blocked`) notifies the human. On macOS:
```
osascript -e 'display notification "TASK-<n> <status>: <PR URL or reason>" with title "task-agent"'
```
Elsewhere, print a clearly-marked summary line. `NOTIFY` in `workflow/.env` (or a
`notify: <shell command>` line in the board config) overrides the mechanism, with
the message as `$1`.

## Failure discipline

- Anything unexpected (git conflict, missing prerequisite, ambiguous task) →
  `blocked` with a reason on the board. Never guess past a blocker, never
  delete a worktree that contains unmerged work.
- A `blocked` task is a human's job. Do not retry it on later runs unless the
  human has reset its status.
- **`blocked` is also how a human takes a task back.** Setting a task to `blocked`
  makes every driver skip it permanently — safe to do while `/task-auto` is
  running, no need to stop the loop.
- A crashed run costs one phase, never the task: the board holds the status and
  `state.md` holds the round, branch, and worktree. Any driver resumes from there.
