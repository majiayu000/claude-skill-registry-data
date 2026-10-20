---
name: companion
owner: baseline
description: EXPERIMENTAL. Join or leave an org-team coordination channel as a session peer. `/companion on <channel_id> [peer_id]` registers this Claude Code session as a `pclass:"session"` peer and works the claim → execute → signal loop, escalating un-decidable forks to the lead (never deciding). `/companion off` deregisters. `/companion status` reports the current peer. Part of org mode (Article X), which is opt-in via `velocity.org_mode.enabled` and OFF by default. Use when a human launches a second session to act as a peer alongside a lead.
disable-model-invocation: true
---

# companion — be a session peer on an org-team channel

**Experimental.** This skill is part of org mode (Article X — multi-session coordinated workflows), which is **opt-in and off by default** (`velocity.org_mode.enabled`). The single-session workflow is unaffected by anything here.

It turns the current Claude Code session into a **session peer** on a coordination channel, so a feature can be worked by a small pod of real sessions instead of by one. Instead of pasting `register_peer` / `claim_task` / `signal_done` calls by hand, you type `/companion on <channel_id>`.

## The bounded-peer contract (Article X — non-negotiable)

A peer **decides in its own lane and escalates out of it**. When acting as a companion you SHALL:

- **Stay a peer.** You are a peer on this channel for the whole session, even if the same human also runs the lead session elsewhere. You SHALL NOT arbitrate yields, release or re-dispatch lanes, answer other peers, or **decline a claimable lane on the belief that you are the lead**. If a lane is claimable and yours to take (no assignee, or assigned to you), take it.
- **Know who you are.** You are the exact `peer_id` you registered as, and no other. Never infer identity from a task push — a `task-available` for a lane assigned to another peer is not yours, and a rejected claim does not mean you should change who you are.
- **Decide in-lane.** How to structure a function, which existing helper to reuse, where a boundary sits — those are yours to make, in your own main context. That is what makes a peer a peer rather than a worker.
- **Escalate out-of-lane.** A **cross-lane** choice (its answer changes another lane) or an **un-decidable** one (it needs design or product judgment) is not yours. Task-bound → `yield_fork(...)` and stop that lane. Free-form → `ask_lead(...)` and continue if you can. The lead answers via `answer_peer`; read it back with `sprint_status`.
- **Never send a free-form directive over the channel.** The message types are a closed set; coordination travels over it, judgment does not.

Execute a claimed lane **within its declared `write_set`** only. Every PreToolUse hook fires on your writes exactly as in a solo session.

## Prerequisites

1. **Org mode is enabled** for this repo (`velocity.org_mode.enabled` in `.claude/project.json`). Off → stop; the fence is closed by design.
2. **The `baseline` MCP server is loaded.** It ships registered in `.mcp.json`, so a normally-started session has it. Verify with `claude mcp list` (expect `baseline … Connected`). If the tools are missing, the session started before the server was registered — restart it.
3. **Same repo, same machine as the lead.** The channel is a file-locked on-disk directory under `.claude/state/sprint/<channel_id>/`. A peer elsewhere cannot see it.
4. **A git repository.** Org mode requires git.

No launcher and no special flags: a peer is an ordinary Claude Code session opened in the same repo.

## Subcommands

Parse the argument string. The first token is the subcommand (`on` | `off` | `status`).

### `/companion on <channel_id> [peer_id]`

1. Require `<channel_id>` (alphanumeric, `_`/`-`, at most 128 chars — it must satisfy the channel's `isSafeId`). If absent, stop and ask.
2. Choose `peer_id`: the second token if given, else `companion-1`. Same id rules.
3. Call `register_peer` with `{ channel_id, peer_id, pclass: "session", role: "peer", workspace: "." }`. Confirm `{ ok: true, registered: true }`.
4. Write the local marker `.claude/state/companion/<channel_id>.json` (create the dir if missing):
   ```json
   { "channel_id": "<channel_id>", "peer_id": "<peer_id>", "pclass": "session", "active": true, "registered_at": 0 }
   ```
   `off` and `status` find the active peer through this marker. `.claude/state/` is gitignored.
5. Enter the **claim loop**:
   - Call `sprint_status({ channel_id })` for authoritative state. Pick a `pending` lane with no assignee (or assigned to you) whose `depends_on` are all `done`, then `claim_task({ channel_id, peer_id, task_id })`. The handler re-checks atomically, so a lost race returns `claimed: false` — move to the next lane.
   - On a successful claim, execute that lane within its `write_set`, applying `code-structure` discipline.
   - On completion call `signal_done({ channel_id, peer_id, task_id })` and report the `unblocked` list it returns.
   - On an out-of-lane fork → `yield_fork(...)` (task-bound) or `ask_lead(...)` (free-form), per the contract above.
   - When no claimable lane remains, **do not stop — enter watch mode** so a lead re-dispatch is picked up with no human turn: run `node .claude/skills/companion/watch.mjs <channel_id> <peer_id>` with `run_in_background` and end the turn.
6. **Watch-mode re-invocation.** When the watcher exits, act on its JSON:
   - `{"wake":true,"task_id":…}` (exit 0) — a lane became claimable. Re-enter the claim loop, then **re-arm** the watcher and end the turn.
   - `{"wake":false,"reason":"companion inactive"}` (exit 2) — `/companion off` ran. Do not re-arm.
   - `{"wake":false,"reason":"heartbeat"}` (exit 3) — no work in the cap window. Re-arm and end the turn; this only keeps each turn bounded.
7. Report what you claimed, finished, and escalated. Once the watcher is armed the peer is hands-off.

### `/companion off [channel_id]`

1. Resolve the marker: the given `<channel_id>`, or the single active marker under `.claude/state/companion/` if only one exists (otherwise ask which).
2. Stop the claim loop. An armed watcher reads the marker's `active` flag each tick and exits `2` on the next poll, so it self-stops once step 3 runs — do not re-arm after that.
3. Set `"active": false` in the marker.
4. Call `leave_peer` with `{ channel_id, peer_id }`. It removes the peer from `peers[]` and returns `{ ok: true, removed: <bool> }` (idempotent).
5. Report: deregistered from the channel and marked inactive locally.

### `/companion status`

Read any markers under `.claude/state/companion/` and report `channel_id`, `peer_id`, `active`, `registered_at` for each. If none, report "no companion peer registered in this session."

## Optional: push dispatch

The shipped path above **polls** — `sprint_status` is the authoritative check, and the watcher blocks between ticks. That is deliberate: it depends on nothing outside the project.

A push-dispatch path used to exist via a sibling channel server. It needed a launch flag no consumer install can assume, so it was never part of the shipped path, and it retired in 0.26.0. Polling `sprint_status` is the whole peer path. A pointer naming a claimable lane may arrive from the host and shorten the wait, but nothing here waits for one.

If you are experimenting with push dispatch, treat it as research-preview tooling with the failure modes that implies. Nothing in the claim loop above changes: `sprint_status` remains the never-dropped completion check, and a lost push is recoverable by reconciling from it.

## Constraints

- **Decide in-lane, escalate out-of-lane** — re-read the Article X contract above. A peer that guesses a cross-lane answer defeats the model.
- **`off` deregisters via `leave_peer`** — it removes the peer from `peers[]` and marks the local marker inactive.
- **Experimental** — org mode is opt-in, off by default, and its surface may change. The single-session workflow is unaffected.
