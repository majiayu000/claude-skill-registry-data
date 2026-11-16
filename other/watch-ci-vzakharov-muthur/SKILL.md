---
description: Watch an in-flight GitHub Actions run for the current ref incrementally — a push-triggered run, an on-demand test dispatch, or a deploy lane — surfacing failures as they happen so the agent can push fixes mid-run with the commit skip marker. Use when the user says "watch ci", "wait for ci", or equivalents. A run has to be dispatched or pushed for there to be anything to watch.
---

Watch the latest GitHub Actions run for the current ref incrementally. As
individual jobs fail, surface them so the agent can fix the underlying issues
and **push each fix immediately with `[no ci]`**. When the run reaches a
terminal state, if any mid-run fixes landed push one final empty commit (no
`[no ci]`) to retrigger with everything baked in.

**Which runs there are to watch.** Every workflow is triggered by a push or a
dispatch, so if the project's CI doesn't run on feature-branch pushes, this
skill has no subject until something is dispatched. Typically:

- a **push-triggered run** on the branch, where the project's CI is configured
  that way;
- an **on-demand dispatch** — but `/test-on-gh` (if hydrated) already blocks for
  its result, so reach for this mainly to re-attach to a dispatch you left
  running (e.g. a fresh session picking up a branch);
- a **scheduled/nightly run** — usually watched from the trunk, and a red one is
  a tracking issue rather than a branch to fix;
- a **deploy lane** run — the ship plumbing, not a test run.

If there is no run for the current ref, say so and stop — don't push an empty
commit hoping to conjure one.

This skill acts **autonomously mid-run**: no user-confirmation gate before
applying fixes, and it pushes those fixes itself.

## Why mid-run commits are safe (with `[no ci]`)

(`[no ci]` here is GitHub's own commit-message skip marker, unrelated to
`/finalize`'s `no vet` flag despite `no ci` being one of that flag's accepted
spellings.)

A workflow with `concurrency: cancel-in-progress: true` cancels its in-flight
run when you push to the same ref. A commit whose message contains `[no ci]`
does not schedule a new workflow run, so the concurrency cancellation never
fires. (On a ref where a push schedules nothing anyway, the marker simply has
nothing left to suppress.)

Why push immediately instead of staging locally:

- The operator usually watches the branch from a different machine than the
  agent's VM — pushing makes the work visible in real time.
- A context wipe / handoff mid-run doesn't lose accumulated fixes.
- The diff is the record of what the agent did; "in working tree only" leaves no
  trace.

## Step 1: Tick loop

Repeatedly call `scripts/ci-watch-tick.sh` as a synchronous `Bash` with a
generous timeout (e.g. 120000ms). The script handles its own sleep via the
`MUTHUR_INTERVAL` env var (default 60s) and tracks "time since last tick" in
`.git/ci-watch-state.json` — so if you spent 3 minutes fixing the previous
batch, the next tick skips its sleep and snapshots immediately.

Each tick exits with one of:

- `0` — the tick succeeded. Inspect the final printed line
  (`overall=<status>/<conclusion>`) to disambiguate:
  - `overall=in_progress/-` (or any non-`completed` status) — run still in
    progress, no new failures this tick.
  - `overall=completed/success` — run finalized green.
- `10` — run still in progress, but one or more jobs failed terminally since the
  previous tick. The script prints logs for each newly-failed job (deduped
  across ticks via the state file).
- `20` — run completed with failure / cancelled / timed_out.

After each tick:

- **Exit 0, in progress** → call the next tick.
- **Exit 0, `overall=completed/success`** → Step 2a.
- **Exit 10** (in progress, new failures) →
  - For each newly-failed job, locate the source files referenced by the
    failure, propose a concrete fix, and **apply it directly** to the working
    tree. Do not ask the user — mid-run autonomy is the point of this skill.
  - **Commit and push the fix with `[no ci]` in the commit subject.** One commit
    per logical fix is fine; batching multiple fixes from a single tick into one
    commit is also fine. Example:
    `git commit -m "fix: address flaky timeout on the upload path [no ci]"` then
    `git push`. Do NOT run `./scripts/vet.sh` between ticks — that's deferred to
    the terminal step.
  - Maintain a running fix log in conversation memory:
    ```
    - <job name>: <root cause> → <commit sha>
    ```
  - Call the next tick.
- **Exit 20** → Step 2b.

The tick prints the last 200 lines of each failed job's log inline and tees the
complete log under `.git/ci-watch-logs/` — read the full file when the excerpt
cuts off the actual error.

## Step 2a: Terminal success

- No mid-run fixes were pushed → report green and resume the enclosing context
  (current task, etc.).
- Mid-run fixes WERE pushed but the run still passed (rare) → report green, list
  the accumulated fix commits, surface them to the user. They're already on the
  remote; no further action needed.

After reporting green (both sub-cases): **end the turn** so the session reads as
idle, not pinned as "working" — don't start a background process. Tell the
operator they can run **`/check-merge`** when they return to see whether the
branch's merge target moved out from under it or the PR landed. (`/check-merge`
is stateless, so it's ready to run any time — there's nothing to record here
first.)

## Step 2b: Terminal failure

Print a structured summary:

```
Run finalized: failure (<url>)
Mid-run fixes pushed (with [no ci]):
  - <job> | <cause> | <commit sha>
Unaddressed failures (if any):
  - <job> | <reason agent couldn't fix> | <log excerpt>
```

Then branch:

- **Fixes pushed AND no unaddressed failures** → run `./scripts/vet.sh` to
  verify the accumulated branch is clean. If green, re-dispatch (`/test-on-gh`
  with the same selectors, if hydrated) or, on a lane where a push does schedule
  a run, push a single empty commit to schedule a fresh run with all the fixes
  baked in — e.g.
  `git commit --allow-empty -m "ci: retrigger with accumulated fixes from run <url>"`.
  **The retrigger commit message must NOT contain the literal skip marker (the
  `[no ci]` / `[skip ci]` characters) anywhere — not even in prose like "after
  [no ci] fixes".** GitHub scans the whole message and will skip the run, so the
  retrigger silently does nothing (symptom: `ci-watch-tick` reports "No CI run
  found for HEAD …"). Refer to it as "the skip marker" or "skip-marked commits"
  instead of writing the characters. Skill ends. Does NOT auto-re-invoke (risks
  an infinite loop on persistent infra failures); the user can chain `/watch-ci`
  again if they want.
- **Fixes pushed BUT unaddressed failures remain** → run `./scripts/vet.sh` to
  verify the partial fixes. Surface the unaddressed failures with proposed fixes
  or questions for each. The user decides whether to push the retrigger empty
  commit + address the rest manually, or hand off elsewhere. Skill ends without
  retriggering.
- **No mid-run fixes ever applied** (run failed non-actionably — flake, infra,
  an environment issue the agent couldn't act on) → report the failure, name
  what made it non-actionable, and stop. Don't push a retrigger hoping a flake
  clears; say plainly that the run failed for a reason this skill can't fix and
  let the operator decide.
