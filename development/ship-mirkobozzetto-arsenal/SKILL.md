---
name: ship
description: Implement a clear request or an approved brief/proposal. Work solo, make the smallest sufficient change, verify the changed behavior, and stop. Ask before any delegation.
argument-hint: "<request or spec> [-r] [-w] [--tasks ids] [--no-commit] [--no-push] [--yolo]"
---

# Ship

Own the result, not a ceremony. A clear request is sufficient authorization
for its reversible, in-scope implementation. Do not ask whether to start.
Do not turn a small fix into a brief, proposal, interview, or document bundle.

## Execution policy

- Work solo. Ask before every proposed delegation, including reviews. State
  the independent scope and expected benefit. Auto mode never grants consent.
- Use the active model and configured routing. Do not inspect or tune models
  during an unrelated task. No hidden advisor or nested delegation.
- Read the relevant existing code, fix the cause, run the smallest meaningful
  behavioral check, and deliver. Reuse current evidence until code or inputs
  relevant to that evidence change. No routine full-file read-back.
- Keep backups and explicit approval for live data, destructive operations,
  publication, and deployment. A build target may install or deploy; inspect
  its actual effects instead of trusting its name.
- Stop on user interruption. A completed task is not reopened by a reminder.

Efficiency plugins such as Espresso are optional. Their automatic mode does
not waive Ship's per-delegation consent, solo mode, specialist/model choices,
artifact gates, verification or commit rules. Do not add a parallel team or
reviewer. Without the plugin, Ship behaves unchanged.

## Choose the shortest sufficient path

**Clear request:** identify the target and success condition from the request
and existing code. Ask only for a missing decision that materially changes the
result. Implement directly; no mandatory artifact files or step-by-step gates.

**Approved spec:** read the exact artifact once. Brief requires `ready`;
proposal requires explicit `Accepted`. Honor scope, dependencies, acceptance
criteria and non-goals. A shipped marker means done, not another run. On the
first run of a spec in a Git repository, work on its `branch` created from
`origin/<base>` (steps/step-00-init.md); a task that carries an issue is
read together with that issue's Pickup Directive.

**Another spec already running here:** with `-w`, do not implement in this
session. Create the spec's worktree, hand the run to a session opened there,
and return the worktree path and how to reach that session
(steps/step-00-init.md). One spec, one branch, one worktree, one pull
request: never a worktree per task. Without `-w` nothing changes.

**Long or resumed work:** load `steps/step-00-init.md` and maintain one
per-run `trace.md`. Existing contract/bundle files remain readable but are
not mandatory new outputs. Record completed units immediately. Native todo
is a projection of progress, not another authority to arbitrate against it.

**Every closed unit is committed and pushed at once** on the work branch,
never on `base` (steps/step-02-plan.md). The history is the record; one
catch-all commit at the end is a defect. `--no-commit` turns both off,
`--no-push` keeps the commits local.

**A finding outside the task** (a bug met on the way, a gap in a sibling
task, a missing capability) gets one line proposing an issue through the
`issue` skill, never a brief and never silent work on it. Then the task
continues.

## Commands and verification

One owner runs commands on a shared workspace/toolchain. Do not start a
second compiler while the first exists. A timeout is not process termination.
Use the existing job handle or `arsenal_status` before any retry.

- Prose/prompts/simple configuration: successful edits suffice unless a check
  was requested. Do not start model sessions, validators, or builds for them.
- Code: reproduce the relevant behavior and verify the fix. Use an existing
  targeted check or disposable smoke scenario. Ask before permanent new tests.
- Data migration: keep the backup and real-copy verification; do not replace
  them with a read-only reviewer saying PASS.
- In controlled OMP, mark a meaningful command with bash `verification:true`.
  The controller records exit status, not semantic correctness. A trivial
  successful command cannot prove a feature. Call `arsenal_finish` once done.
- Sandbox shell networking and out-of-root writes are refused. Report an
  unavailable capability; do not escape the controller through another tool.

## Verify external facts

Before stating an external fact (a version, an API, a price, a date, a
regulation, the behaviour of a tool or library, a person or company), search
first when the runtime offers web search: read the `websearch` skill and run
one quick search, then cite the source. One search per fact; `--deep` only on
request. Without web search, mark the claim unverified. Facts visible in the
repository or the request need no search.

## Optional branches

Load only when needed:
- `steps/step-01-ingest.md`: artifact formats and task filtering.
- `steps/step-02-plan.md`: complex dependencies and per-unit commit and push.
- `steps/step-03-engine.md`: user-approved delegation.
- `references/guardrails.md`: hazardous operations.
- `steps/step-06-finish.md`: durable status and requested Git delivery.

Flags: `-a/--auto` suppresses redundant questions, not safety/agent consent;
`-e/--economy` and `-m solo` retain solo; another `-m` requests a mode,
not a permission bypass. `--tasks` scopes to named spec tasks and completed
dependencies. `-r` resumes. `-w/--worktree` runs the spec in its own
worktree through a second session instead of this one, and is never implied.
Commit and push per closed unit are the default;
`--no-commit` turns both off, `--no-push` keeps commits local, `--commit` is
accepted for compatibility and changes nothing. `--yolo` requests relevant
safe checks, never live-data edits, deployment or a full suite unrelated to
the change.

Final response, in this order (steps/step-06-finish.md): result, exact
proof, material limitation, where to see it running, and as the last line
the next command. When the spec is fully shipped, the ready PR command
towards `base` with a one-word go question. A PR the user deferred in this
run is not offered again in it. No required HTML, no next-work expansion.
