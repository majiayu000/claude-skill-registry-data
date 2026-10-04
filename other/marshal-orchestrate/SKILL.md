---
name: marshal-orchestrate
description: >
  Drive a fleet of headless agents through Marshal's MCP server: decompose a goal into
  independent tasks (implementation, research, review, audit, summarise), run them in parallel in
  isolated git worktrees, collect each run's product (diff or text), and integrate the good diffs.
  Use when you have multi-part work to delegate to worker agents (Cursor, OpenCode, Codex,
  Antigravity, Claude Code) instead of doing it all yourself. The engine is mechanism; this
  playbook is the judgment - decomposition, prompt-writing, and merge decisions live here.
---

# Driving the Marshal fleet

You are the **driver**. You keep the expensive thinking - planning, review, merge decisions - and
Marshal spawns cheaper or specialized worker agents that each execute one task autonomously in its
own git worktree. Your job is to decide *who works, on what, with how much context, and whether the
result was worth keeping.* Marshal is a **fleet primitive**, not a diff factory: a run's product may
be a DIFF or TEXT. Marshal is exposed as MCP tools; the loop is **plan → spawn → monitor →
collect → (integrate when there is a diff).**

## Targeting a workspace (when the server has more than one repo)
One Marshal server can be wired to several repos at once. Call `list_workspaces` first to see them
(name, path, `configured`, `client_count`). **Every action tool takes an optional `workspace`** -
pass a name to target that repo; omit it to use the default (primary) workspace. Workspaces are
fully isolated: each has its own clients (`list_clients(workspace=...)`), its own worktrees, its own
run ledger.
- Each run record you get back carries a `workspace` field. When you later `collect_run`,
  `integrate`, or `cancel_run`, pass that same `workspace` so the call routes to the right repo (it
  still resolves correctly if you omit it - the id is looked up across workspaces).
- `status()` with no `workspace` lists runs across **all** workspaces (each tagged); pass a name to
  scope to one.
- `run_many` accepts optional per-job `workspace` — one call can fan out across registered repos
  under a shared `max_concurrency`. Call-level `workspace` is the default for jobs that omit it.
  Ledgers stay per-workspace (no merged usage across repos).
- Need a repo that isn't registered yet? Registration is an **operator decision**: the
  `add_workspace(name, path, scaffold?)` tool is disabled by default and only works when the server
  was started with `MARSHAL_ALLOW_MCP_WORKSPACE_REGISTRATION=1`. If your call is refused, do NOT
  retry or look for another way in - report the exact command to the user instead:
  `marshal workspace add <name> <path>`. It hot-reloads into the running server (no reconnect), so
  you can continue as soon as they've run it. When the server does permit the tool, pass
  `scaffold=true` to drop a starter `fleet.config.yaml` if the repo has none; then check
  `list_clients(workspace=name)` and have the user fill in clients before routing real work.

If `list_workspaces` shows only `default`, ignore all of this: it behaves exactly like the
single-repo server.

## 0. Know your clients
**Run `doctor` before the first batch** (read-only). It now verifies *auth*, not just that a CLI is
on PATH: a logged-out backend that still answers `--version` is reported `CLI present but not
authenticated` (with the login command), instead of a green "available" that then dies one second
into a real run. Treat a backend's login as standing setup you confirm up front — cheap to check,
expensive to skip across a whole fan-out.
Call `list_clients` to see the configured workers (name, backend, model, permission,
`permission_fidelity`). Each client is a routing choice the user set up (a cheap bulk worker, a
careful reviewer, etc.). You route tasks to clients **by name** - you never choose backends
directly. Use `permission_fidelity` when routing sensitive work (it is resolved from that
client's `(backend, permission)` — a `yolo` client is never `enforced-denies`):
- `enforced-denies` — this client's tier has a backend/Marshal restriction beyond the worktree
  (still not a sandbox; prefer these for secrets-adjacent or destructive-risk tasks).
- `boundary-only` — treat as worktree isolation only; do **not** assume a deny guarantee
  (Command Code, Goose, Antigravity, Claude Code). Doctor warns on these backends' safe-edit.
- `unrestricted` — `permission: yolo`; deny/sandbox overlay dropped by design. Do **not** route
  sensitive work here.
To decide *which* client a task should go to (by task weight - heavy/standard/light - and cost),
see [`docs/model-playbook.md`](../../docs/model-playbook.md).

## 1. Plan - decompose into INDEPENDENT tasks
Split the goal into tasks that can run in parallel **without colliding**. Tasks may be write work
(implementation) or read-and-reason work (research a question across sources, review a diff, audit a
codebase, summarise) - Marshal runs the agents either way; the product is a diff or text.
- For write tasks: give each a disjoint set of files where possible. Two tasks editing the same file
  will conflict at integrate time - separate their scope or run them in different rounds.
- Size each task so one worker can finish it autonomously. Workers are **headless: they cannot ask
  you anything mid-run.** The prompt must contain everything needed to finish.
- Write a self-contained prompt per task: the goal, acceptance criteria, and the *minimal* files and
  context the worker needs. The worker sees only what you give it plus its worktree - not your whole
  session. Scope tightly; that is the point (less drift, less token waste).
- When you know the intended file scope, pass `context_files` on the task so the worker sees only
  what it needs.

**Never fan out a dependency chain in one `run_many`.** Marshal shines on *independent* work. If task
B needs A's output, batching them in parallel makes each branch off the same base, blind to the
others - they re-invent the same scaffolding and collide at integrate. For sequential work, do one of:
- **Rounds (simplest):** integrate A into your branch (when A produced a diff), then plan B against
  the new state. For text-only A, read `collect_run` / `text` and put the findings in B's prompt.
- **Pass a report forward with artifacts (multi-round review/fix loops):** tell A in its goal to
  write its findings to `.marshal-artifacts/<name>.md` in its worktree. Marshal harvests that when
  the run ends, so it survives the worktree, and `get_run(A)` lists it under `artifacts`. Then spawn
  B with `artifacts_from: [A_run_id]` and it lands read-only at
  `.marshal-context/artifacts/<A_run_id>/`. **Say in B's goal that the file is there** - the copy is
  not announced to the agent by itself. Prefer this over pasting a long report into B's prompt: it
  keeps prompts short, and the next round reads what A actually wrote instead of your summary of it.
- **Chain off A's branch (no integrate yet):** `commit_run(A)` freezes A's work as a commit on its own
  branch (your branch stays untouched), then `spawn`/`run_agent` B with `base_branch` = A's branch so B
  builds on A's actual output. Without `commit_run`, basing B on A's branch sees only the spawn base -
  the agent leaves its work uncommitted, so the branch ref never moved.
- **When dependence is unavoidable, ship the contract in the prompt:** the exact signatures/imports of
  the foundation plus "this already exists - import it, do not redefine it."

## 2. Spawn
- One task: `run_agent(client, goal, task_id?)`.
- Several independent tasks: `run_many(jobs, max_concurrency?)`, where `jobs` is a list of
  `{client, goal, task_id?, workspace?}`. They run in parallel, each in its own worktree, capped at
  `max_concurrency` (default 4 - each agent CLI is heavy; do not uncap a large fan-out). Per-job
  `workspace` fans out across registered repos in one call; omit it to use the call-level default.
- Every run returns a record with a unique `run_id`, its `worktree`, `status`, `cost_usd`, and
  `workspace`.

## 3. Monitor
- `status()` lists every run with status + cost; `get_run(run_id)` fetches one.
- A `running` record means "no outcome recorded yet", which is not the same as "the agent is
  working". Read `agent_alive` to tell them apart: `true` = still working, `false` = the process is
  gone and the outcome is about to be written (re-read shortly), `null` = unknown, **not** dead.
  Do not probe the pid yourself — a pid alone is not an identity, since the OS reuses them.
- A run ends in `exited_clean`, `empty` (exited 0 with neither text nor file changes - an outcome,
  not a fault; nothing to integrate), `failed`, `timed_out`, `cancelled`, or `verify_failed` (file
  changes exist but the workspace's `verify:` gate rejected them - collect the diff and read the
  record's `verify_output` before deciding; not an integration candidate as-is). Only
  `exited_clean` runs with a diff are integration candidates; text-only `exited_clean` work lives
  in `text` (see collect). When the workspace configures a `verify:` command, `exited_clean` also
  means that gate passed for runs that had changes.

## 4. Collect - review before you trust
- `collect_run(run_id)` returns the run's product read-only. Branch on `produced`:
  - **`diff`** — uncommitted (`changed_files`, `diff`) and/or committed
    (`committed_changed_files`, `committed_diff`, `commit_count`) file changes. Read both sections.
    An empty uncommitted diff does **not** mean no work — check the committed section too.
  - **`text`** — no file changes; the agent's final message is the artifact (`text` on the result).
    This is the expected product of research/review/audit/summarise runs. Do **not** treat it as
    failure, and do not integrate.
  - **`nothing`** — neither text nor file changes (matches run status `empty`).
- `exited_clean` means "the process exited cleanly," not "the work is correct."
- Reject work that is wrong or off-scope by not integrating it: the worktree stays isolated and main
  is untouched. Then **record it** (step 6) - not integrating is invisible on its own, and an
  unrecorded rejection is a run that looks like nobody ever reviewed it.
- **When your own read isn't enough** - a migration, a public API, a security-sensitive path -
  `run_team(name, target="run", run_id=...)` puts the same diff in front of several independent
  read-only reviewers (each a different model, each holding one lens) and hands you their reports.
  It computes no verdict: you still collect the objections and decide. See
  `marshal-adversarial-review`, and `list_teams()` for the declared panels.

## 5. Integrate - merge the good diffs
`integrate(run_id, cleanup?)` merges the run's branch into the branch you currently have checked out.
Only for runs whose product is a diff. Handle the outcome:
- `merged` - landed; `merged_into` and `changed_files` say what/where. Pass `cleanup=true` to remove
  the worktree when you're done with it.
- `conflict` - the merge was aborted and the repo left clean; `conflicts` lists the files. Resolve by
  re-planning the task (or integrating the other runs first), then retry.
- `blocked` - the target checkout is dirty/colliding or on a detached HEAD; nothing changed. Fix the
  target (commit/stash your edits, check out a branch) and retry - the work is safe on its branch.
- `empty` - no file changes to merge (an outcome, not a fault; common for text-only runs).
- A `failed` run has two possible meanings: the agent/backend failed, or the run was **orphaned at
  startup** because the process supervising it died before an outcome was recorded. Read `error` to
  tell them apart - an orphan says so, and its work may still be sitting in the worktree.
- `error` - a git operation failed in a way that needs a human (read `message`); do not blindly retry.
- `base_branch_drift` (on `merged`) - the run was spawned from a different branch than the one you
  currently have checked out (`message` names both). The merge **still landed**; this is a warning,
  not a block. Integrating into a different branch is sometimes deliberate — read the branches and
  decide whether the result is what you intended.

Integrate **one run at a time**, reviewing each. Worktree isolation means main is never touched until
this step.

## 6. Record the outcome - what you rejected, not just what you merged
`integrate` records `integrated` for you. Nothing records the other half, so **call
`set_outcome(run_id, "rejected"|"abandoned"|"advisory", note?)` on every run you decide not to
merge**:
- `rejected` - you reviewed it and the work was wrong, off-scope, or worse than a sibling's.
- `abandoned` - you gave up on it (superseded, no longer needed, the task was wrong).
- `advisory` - it produced findings you USED and there was nothing to merge (a read-only review,
  audit, or plan panel). Reach for this instead of `abandoned` there: `abandoned` reads as giving
  up, and counts against a reviewer's integration rate for merges it could never have produced.

Why it matters: declining to integrate leaves **no trace**, so a run you reviewed and threw away is
indistinguishable from one nobody has looked at. `routing` computes every rate over *judged* runs
only (the integration rate over the judged runs that could have merged - `advisory` ones are kept
out of it) - if you record integrations and never rejections, it reports a 100% success rate for
every client and tells you nothing.

Add a `note` when the reason is not obvious from the diff; it is what your future self reads out of
`routing`. `integrated` is sticky (a merge commit is a fact, not an opinion) - trying to overwrite
it returns `conflict` and changes nothing.

Then `routing(task_kind?)` pays it back: it reports which client's work you actually kept for this
kind of task, ranked, with the sample size attached to every rate. Read it **before** step 1 on
your next fan-out instead of guessing from model names. It ranks on integration rate first and only
breaks ties on measured cost, so a backend that reports no cost is never scored as if it were free.

Ranking is **per `task_kind`** — pass the filter for the work you are about to fan out. Without it
you get every kind at once, each with its own #1 in `recommended_by_task_kind`, and `recommended`
is `null`: a client that tops your `docs` history has no measured claim on a `refactor`.

## 7. Clean up - reclaim the worktrees
A long session leaves a worktree + branch per run. When you're done, `clean(scope?, dry_run?)` tears
them down in one call (the usage ledger and run-state history are kept; only the disk-heavy worktrees
and branches go). It **never** touches a running run. Scopes:
- `merged` - only runs you already integrated. Safest.
- `finished` (default) - merged runs plus failed/timed_out/cancelled/empty/verify_failed ones;
  **protects un-integrated `exited_clean` runs** (a candidate you might still want to review). A
  `verify_failed` run's worktree holds reviewable work - collect/review it before cleaning.
- `all` - every finished run, including un-integrated exited_clean work.

Scope-mode cleans also reap **orphans** automatically - worktree dirs whose run record was pruned or
corrupted (they are invisible to ledger-driven cleanup and would otherwise leak on disk forever);
they show up under `orphans_removed`.

Run `clean(dry_run=true)` first to see what would go, or `clean(run_ids=[…])` to tear down specific
runs. Don't clean a run whose work you haven't collected/integrated unless you're sure you're done
with it.

## Cost
`usage()` shows per-provider cost (totals and by backend/client/model, with `$/run` and
`$/succeeded`). Every figure is tagged by `source` (native / admin-api / unavailable) -
never treat `unavailable` as free. To compare routing strategies head-to-head on a real task, use the
**marshal-benchmark** skill.

## Invariants to respect
- When several repos are wired, pick the right `workspace` per call; a run integrates into **its own**
  workspace's repo, never another.
- Workers are headless - prompts must be self-sufficient (no questions are possible).
- Review what a run produced before integrating; `exited_clean` is not `correct`. Text-only runs
  need no integrate; `empty` is an outcome, not a failure.
- Keep tasks independent to avoid merge conflicts; **never fan out a dependency chain** - sequence it
  in rounds, or chain off a committed branch with `commit_run` + `base_branch`.
- Confirm backends are authenticated (`doctor`) before the first batch, not after a wasted run.
- Worktree isolation is the safety net - main is untouched until you integrate.
- Clean up finished runs with `clean` when done; it never removes a running run or the usage ledger.
