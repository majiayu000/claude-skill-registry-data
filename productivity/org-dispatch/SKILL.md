---
name: org-dispatch
owner: baseline
description: Run an org-team workflow — a flat pod of up to four peer Claude Code sessions claims lane-tagged slices of an approved spec over the baseline MCP channel and implements them concurrently, each in its own git worktree. Each peer DECIDES its own in-lane implementation choices in its own main context (Article X); only un-decidable or cross-lane forks escalate peer→lead→human (yield_fork for task-bound forks, ask_lead for free-form queries). Opt-in and OFF by default (velocity.org_mode.enabled). Graduates the retired sprint-dispatch prototype into the constitutionally-sanctioned org-team model (Article X — Multi-session coordinated workflows). Requires git.
---

# org-dispatch — run an org-team over the coordination channel

`org-dispatch` is the execution engine of the **org-team model**: a flat pod of up to four peer Claude Code sessions claims lane-tagged slices of an approved spec and implements them concurrently over the baseline MCP channel, each peer in its own git worktree, so per-feature wall-clock approaches the slowest lane instead of the sum. It is the multi-session counterpart to `swarm-dispatch` (which parallelizes components of one spec inside one session via bounded subagents).

It is governed by **Article X — Multi-session coordinated workflows** (a different axis from Article II, which governs intra-session delegation and is untouched). The load-bearing difference from the retired `sprint-dispatch` sandbox: **a peer decides its own in-lane implementation choices in its own main context** — it does not bounce every fork to the lead. Only un-decidable or cross-lane forks escalate.

## Gate: opt-in, off by default, git required

```
node .claude/skills/org-dispatch/org-mode.mjs gate   # wraps org-mode.mjs -> orgDispatchGate
```

If the gate refuses, **stop** — org mode is the opt-in fence (and worktree isolation requires git).

## The run loop (lead, in main context)

1. **Decompose into lanes.** Read the approved spec and its dependency DAG. Each lane is one channel task `{id, lane, write_set, depends_on, assignee?}` (`org-mode.toLaneTasks`). Write the tasks into the channel state and a durable plan (`harness/plan-store.createPlan`). A lane carries a domain tag the claiming peer inherits — its in-lane decision latitude. **No sprint manifest is required**: a lane is just a fully-specified task. The lead may also `enqueue_task` ad-hoc lanes at any time — peers can be handed tasks with no sprint in place; the pool is enabled by `velocity.org_mode.enabled` alone.
2. **Allocate: claim-any or directed.** Leave a lane's `assignee` unset for **claim-any** (the first free peer wins) — simplest, but one fast peer can monopolize the queue while others idle. Set `assignee` to a `peer_id` for a **directed** lane that only that peer may claim — this is the lead's control to spread load across the pod or hand a specific lane to a named peer. `claim_task` enforces it server-side (a non-assignee claim is rejected); the `task-available` push carries the assignee so a well-behaved peer skips a lane that is not its own.
3. **Select the pod** (`peer-select.selectPeerClass`): if human-launched peer sessions are registered on the channel, the flat pod (up to four) works the lanes; otherwise the lead spawns bounded `swarm-worker` subagents as the fallback execution surface. The lead is one of the four — flat for claiming, plus the arbitration + human-escalation hat.
3.5. **Isolate every peer before any lane is claimed.** For each peer, run `worktree.createPeerWorktree({rootDir, peer_id})`. It returns the peer's own working directory and branch (`org/<peer_id>`), or `{ok: false, reason}`. **A refusal stops the dispatch** — never fall back to running peers in the primary tree, because two peers in one checkout each see the other's half-finished edits as their own working tree, and the first commit carries both. Re-running for a peer that already has a tree returns the same path, so a resumed dispatch does not tear down live work.

4. **Coordinate mid-flight.** Peers `claim_task` (race-safe, single-winner), implement within their lane's `write_set`, `signal_done` to unblock dependents (pipeline, not a wave barrier).
   - **A peer is always a peer, and knows which peer it is.** A session connected as a peer never adopts the lead role and never declines a claimable lane on the belief that it is the lead, even if the same human also runs the workflow-lead session. The server bakes the session's `peer_id` and role into its instructions so it never guesses its identity.
   - **Completion is reliable, not push-only.** A pointer may reach a peer when a lane becomes claimable or done, and it may never arrive. The lead reconciles via `sprint_status` — its `all_done` flag is the authoritative, never-dropped completion check.
5. **In-lane decisions stay local.** A peer that meets an in-lane implementation choice (`classifyFork` → `decide`) decides it in its own main context and proceeds. It does NOT escalate routine implementation latitude.
6. **Escalation spine (peer→lead→human).** A peer that meets an un-decidable or cross-lane fork (`classifyFork` → `escalate`) escalates rather than guessing:
   - a **task-bound** un-decidable fork → `yield_fork(task_id, fork_desc)` (the lead records it via `yield-arbiter.recordYield`, arbitrates in main context, records the resolution, and re-dispatches);
   - a **free-form** question → `ask_lead(body)`, which the lead reads off `sprint_status`. The lead arbitrates in main context, and if the fork needs human judgment it escalates to the **human**, then routes the decision back with `answer_peer(message_id, answer)`.
7. **Audit, then land.** On each `signal_done`, diff the peer's worktree against the wave baseline and pass the changed paths through `swarm-dispatch/swarm_merge.mjs → auditChangedPaths({changed, writeSet})` — the same rule the swarm merge applies, so the two never drift. A violation **lands nothing and preserves the worktree** for inspection; report the offending paths and the lane's declared `write_set`. A clean audit applies the diff to the primary tree, then `worktree.removePeerWorktree({rootDir, peer_id})`. An empty `write_set` is a refusal, not a free pass.

8. **Round boundary.** When a wave of independent lanes completes, the lead commits between rounds so a dependent round forks from fresh HEAD.

## Constraints (what makes this constitutional — Article X)

- **Peers decide in-lane; they escalate out-of-lane.** A peer is a full Claude Code session = its own main context, so its in-lane implementation decisions are Article-II-internal to that session. A cross-lane or un-decidable fork escalates — never a guess across lanes.
- **The human is the final authority.** The escalation chain is peer→lead→human; consent gates (approve-spec / approve-swarm / grant-commit) stay structural and un-forgeable. No peer or lead path bypasses or self-satisfies a gate.
- **No new subagent.** Peers are sessions, not subagents; `swarm-worker` remains the only declared subagent. Each peer session may itself run its own subagents — a per-session property, orthogonal to this charter.
- **Live hooks govern every peer write.** The PreToolUse guards fire on peer writes exactly as for any session.
- **Off by default, git required.** `velocity.org_mode.enabled` is the fence; worktree isolation requires git.

## The live channel

The pod runs over the `baseline` MCP server registered in `.mcp.json` — a file-locked directory under `.claude/state/sprint/<channel_id>/`, so every session is on one machine and in one checkout. Peer tools: `claim_task`, `signal_done`, `yield_fork`, `ask_lead`; lead tools: `enqueue_task`, `release_task`, `answer_peer`, `sprint_status`, plus `acquire_lead` / `release_lead`, which hold one lead per channel (a second session that tries is refused, and the refusal names the holder). The free-form `ask_lead`/`answer_peer` pair is the peer→lead→human escalation channel; `sprint_status` is the lossless source of truth. A pointer naming a claimable lane may arrive from the host and shorten the wait, but it is an accelerator: it can be dropped, and nothing waits for one.

## Relationship to other tracks

- **swarm-dispatch** parallelizes components of one spec inside one session (bounded subagents, worktrees).
- **org-dispatch** parallelizes lanes of one spec across multiple peer sessions (the flat pod).
- The default 11-phase solo/swarm pipeline is unchanged; `org` is an added selectable track.
