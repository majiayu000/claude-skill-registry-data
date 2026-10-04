---
name: release-playbook
category: release
description: Use when you need the end-to-end merge -> deploy -> watch -> verdict sequence for a delivery mode, or a tool result you did not expect (refusal, park, tag exists)
---

# Release playbook

You own a task from the moment the board signs it off in `done` until it either lands in `released` or bounces back to `need_revision` through a rollback. Four steps, in order, and each is only worth doing because the one before it happened: **merge → deploy → watch → finish or roll back.**

## 1. Merge

```
merge_task_pull_request({ task_id })
```

returns, among the usual merge fields, `release`:

```json
{
  "release": {
    "mode": "dispatch",
    "release_id": "b1e2...",
    "status": "pending",
    "next": "call deploy_release, then watch_release"
  }
}
```

`release.next` already tells you the next call — read it, do not guess. `release.unconfirmed: true` is a flag on a task merged some other way, not a fifth mode — stop, the card already says why. The modes:

| `release.mode` | What it means | What you do |
|---|---|---|
| `none` | Nothing deploys this component (a library, docs) — the merge itself was the release. | Nothing. |
| `batch` | This component (desktop, mobile and friends) ships in a human-cut batch: the merge joined the component's draft release. | Nothing — the task stays in `done` until a human cuts it. |
| `on_merge` | The merge itself deploys (a workflow on push, or a provider's git integration). | `watch_release`. |
| `dispatch` | A deploy workflow needs to be dispatched at the release tag. | `deploy_release`, then `watch_release`. |

A merge refusal is final, not a retry — see the refusal table in your `done` column.

## 2. Deploy

```
deploy_release({ task_id })
```

**`dispatch` mode** dispatches the profile's workflow at the release tag (`release/<sha12>`) and moves the release to `deploying`. Then call `watch_release`.

**A cut `batch` release** (status `pending`, mode `batch` — you are woken with it, you never cut it) does something different per executor:

| Executor | What `deploy_release` does |
|---|---|
| `github_actions` | Creates the release tag at the cut commit; the repository's own tag-triggered workflow builds and publishes. A tag that already exists is a **real refusal** here — unlike `dispatch`, a batch version is never re-used (SemVer §3: a released version's contents never change). Comment "tag vX.Y.Z already exists — re-cut this release with a new version on the Deploy tab" instead of retrying. |
| `local` | Runs the profile's command on this machine, in a detached worktree of the cut commit, and logs it (`local_run` on the release). |
| `store` | Starts a store build for every platform the repository has a linked app for (`store_builds` on the release). |

Then call `watch_release` the same as for `dispatch`.

## 3. Watch

```
watch_release({ task_id })
```

While the deploy is running or the soak window is open, this call **parks your card** and your run ends — a system sweeper is watching the deploy and the health/smoke/error window for you. Do not poll, sleep, or call it again in a loop; you are woken automatically when there is something to decide. When you are woken, `watch_release` (or `get_release`) returns the settled release instead of a park.

## 4. Verdict — `awaiting_verdict`

Never skip straight to a verdict because the deploy looked green — see `post-deploy-verification` for the exact calls, the verdict table, and the schema/flag/multi-task edge cases. In short:

```
get_release({ task_id })                                   # checks already gathered, plus component
query_runtime_logs({ component, since: deployed_at })      # where the component has a bound runtime environment
list_runtime_errors({ component, since: "<well before deployed_at>" })
```

Clean evidence:

```
finish_release({ task_id, note: "logs clean since deployed_at, no new error groups (first_seen checked), smoke checks green" })
```

Evidence of a problem:

```
rollback_release({ task_id, reason: "verify_failed", note: "checkout smoke check returned 500 since the deploy; 3 error groups with first_seen after deployed_at, all in the checkout module" })
```

`reason` is one of `deploy_failed` (the deploy itself never went green), `verify_failed` (it went green but the soak found a problem), `health_incident` (an incident opened inside the window, handled from the `released` column). `note` is required — state what you actually checked, not just the conclusion.

## 5. Rollback outcomes

`rollback_release` either executes the rollback (`release.status: "rolling_back"`, with `rollback.manual_steps`) or — when `auto_rollback` is off for the component — writes the proposal as a comment and returns `proposed: true` with nothing executed. Both are correct, successful outcomes for their situation. See `rollback-runbook` for schema safety, working through `manual_steps`, and what to do when the call refuses outright (too old, a newer release shipped, a newer one open).

## 6. Failed deploys

A release that lands in `failed` (the deploy itself never went green) is read the same way: `get_release`, then per executor — `github_actions` → `get_deploy_logs` if there is a failed job; a batch `local` run → `local_run.tail` (and its log path) on the release itself; a batch `store` build → `store_builds` names the platform and its error. Then `rollback_release` with reason `deploy_failed` if the bad code is live or sitting on the default branch — otherwise there is nothing to undo, report what failed and stop.

## Tool results you will see

| Result | Means | Do |
|---|---|---|
| `watch_release` returns a park (`ResourceBlock`) | Nothing further to do in this run. | End the run; the sweeper re-dispatches you. |
| `deploy_release` refused (before-deploy steps pending, deploy dependency unreleased, unconfirmed profile) | Same refusal family as the merge. | Stop, do not retry; you are woken when the condition clears. |
| Batch tag already exists | A version is never re-used. | Comment asking for a re-cut with a new version; never delete or move the existing tag. |
| `finish_release` refused | The release is not `awaiting_verdict` any more — something else already moved it. | `get_release` and act on its current `next`. |

## Multi-task releases

A release can carry several tasks (a cut batch, or a release that superseded an earlier one) — `finish_release` releases all of them at once. Your verdict evidence covers every task in `release.tasks`, not only the card you were woken on; see `post-deploy-verification` §1.
