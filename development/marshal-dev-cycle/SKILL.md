---
name: marshal-dev-cycle
description: >
  Run a full development cycle on the fleet: decompose a goal into independent worker jobs, spawn
  them in isolated worktrees, verify what came back, gate the risky diffs through a review panel,
  integrate one at a time, and record every outcome including the rejections. Use when a coding
  goal has parallelisable parts you would otherwise do serially. Trigger on "delegate this",
  "fan this out", "run the fleet", "build this with marshal", "parallelise this work".
---

# Dev cycle on the fleet

You are the driver. You keep the planning, the review, and the merge decisions; the fleet types.
`marshal-orchestrate` has the tool mechanics. This is the loop, with the failure modes that have
actually cost runs.

## Input

Everything after the skill name is free text. Parse it into these, and resolve what is missing
rather than interrogating the user.

| Var | Shape | Missing -> |
|---|---|---|
| `GOAL` | the thing to build, prose or a path to a plan | Required. Without it everything downstream is a guess. |
| `WORKSPACE` | marshal workspace name | The repo you are in, via `list_workspaces`. |
| `CLIENT` | a name from `list_clients` | Pick by weight: a capable model for real work, a cheap one for mechanical edits. Pass the model explicitly if the config pins a variant you do not want. |
| `FANOUT` | int, jobs in parallel | As many as the decomposition yields with disjoint files. `max_concurrency` stays low; each agent CLI is heavy. |
| `TASK_KIND` | `build` / `test` / `docs` / `refactor` / `research` | Infer from `GOAL` and pass it on every spawn. Never omit it; it is what `routing` ranks on. |
| `PANEL` | `yes` / `no` | `yes` if the diff touches a public API, a migration, a security path, or leaves for a repo you do not own. |
| `BASE` | branch to spawn from | Current HEAD, after the commit in section 1. |

`GOAL` is the only one worth blocking on.

## 1. Preflight

- **Commit everything first.** Worktrees branch off a commit, so uncommitted work does not exist
  to the fleet. One spawn was cancelled 21s in because an entire package was uncommitted and the
  agent was about to edit a file with none of that layer in it.
- **Judge the last batch** before starting a new one. Unjudged runs pile up silently.
- `doctor` for auth. `list_workspaces` and `list_clients(workspace=...)`, then pass `workspace`
  on every later call so nothing routes to the wrong repo.

## 2. Decompose, and keep the jobs independent

- **Disjoint files per job.** Two jobs editing one file are isolated by worktrees and then
  collide at integrate. Sequence those into separate rounds.
- **Never fan out a dependency chain.** If B needs A, either integrate A and plan B against the
  new state, or `commit_run(A)` and spawn B with `base_branch` set to A's branch. Without
  `commit_run` the branch ref never moved and B sees only the spawn base.
- **Every prompt is self-sufficient.** Workers are headless and cannot ask anything. Goal,
  acceptance criteria, the minimal `context_files`, and the contract of anything that already
  exists: "this exists, import it, do not redefine it."
- Pass `task_kind` on every spawn. It is cheap and it is the only thing that makes `routing`
  mean something later.

## 3. Route

Pick clients on judgement until the ledger has earned the right to be cited. `routing` computes
every rate over judged runs only, so a history of recorded integrations and no recorded
rejections gives every client a perfect score and ranks nothing. It flags its own sample sizes; read them.

For any run whose product is a verdict or a report rather than a diff, have the agent write it to
a file in the worktree (`.marshal-artifacts/<name>.md`, which marshal harvests) and read it back
with `read_run_file`. Some CLIs truncate long final messages, and a truncated verdict looks like
a short one.

## 4. Spawn and monitor

`run_many(jobs, max_concurrency)`, then `status()`. A `running` record means "no outcome
recorded yet", not "still working". Read `agent_alive`: `false` means the process is gone and the
outcome is about to land, `null` means unknown, not dead.

States that are outcomes rather than faults: `empty` (exited 0 with nothing), text-only
`exited_clean` (research and review jobs, where the product is `text` and there is nothing to
integrate), and `verify_failed` (changes exist but the workspace gate rejected them; read
`verify_output` before deciding).

## 5. Verify

`exited_clean` describes the process, not the content.

1. `collect_run`, and branch on `produced`. Read **both** the uncommitted and the committed diff.
   An empty uncommitted section does not mean no work was done.
2. Read the diff yourself.
3. **Mutation-test any tests it wrote.** Invert the rule the task was about and re-run. One
   branch had 11 tests that all still passed after its central invariant was inverted; they sat
   behind a guard that never fired. A cheaper model's branch failed 6 of 9 on the same treatment.
   Model tier does not predict this, and a green suite is not evidence until you have tried to
   break it.
4. Workers overclaim. "Done" is a claim, not a result.
5. **If the diff is risky**, gate it through `marshal-panel` before integrating.

## 6. Integrate, one at a time

`integrate(run_id)` merges into the branch you have checked out. Outcomes: `merged`, `conflict`
(aborted, repo left clean), `blocked` (dirty or detached target; fix and retry, the work is safe
on its branch), `empty`, and `error` (read `message`, do not blindly retry). `base_branch_drift` is **not** a
status: it is a bool on an otherwise `merged` result, set when the run was spawned off a
different branch than the one you merged into. The merge landed; read both branches and decide
whether that is what you meant.

Never merge a second run before reviewing it. Worktree isolation means the target branch is
untouched until this step, and that is the only safety net there is.

## 7. Record the outcomes

`integrate` records `integrated`. Nothing records the other half.

```
set_outcome(run_id, "rejected", note="...")    # reviewed, wrong or off-scope
set_outcome(run_id, "abandoned", note="...")   # superseded, or the task was wrong
```

Add a note whenever the reason is not obvious from the diff. This is the input the routing table
is otherwise starved of, and the reason it can tell you nothing today.

## 8. Clean up

`clean(dry_run=true)` first, then `clean(scope="merged")` or `"finished"`. It never touches a
running run, and `finished` protects un-integrated `exited_clean` work you might still want.
`usage()` for cost, where `unavailable` is not the same as free.

## Invariants

- Commit before delegating.
- Workers are headless; the prompt is the entire context they get.
- Independent jobs only; sequence dependencies in rounds.
- `succeeded` is not `correct`.
- Integrate one run at a time, after reading the diff.
- Every non-integrated run gets a recorded outcome, or the measurement half stays dead.
