---
name: envoy
description: Use when subscribing sessions to Envoy topics, sending agent-to-agent messages, or reasoning about topic formats for Slack/GitHub/agent routing.
---

# Envoy

Envoy delivers external signals and session messages. Deliveries are at-least-once and can arrive
out of order across topics: use `id` to deduplicate and `at` to judge freshness.

## The one subscription you need for a PR

Subscribe to the whole PR family, not individual event types:

```text
envoy_subscribe([
  "notifications.github.example-org.example-repo.pr.42.>"
])
```

The owner and the repository are one token each, with every dot in the name written `_`:
`acme/site.io`'s PR family is `notifications.github.acme.site_io.pr.42.>`, and a topic spelled
`acme.site.io` receives nothing.

NATS `>` matches **one or more** trailing tokens, so it does not match the lifecycle base
`pr.42` itself. Envoy registers that concrete base automatically when you subscribe to
`<subject>.>`, making `pr.<n>.>` the recommended default: one call receives both the lifecycle
subject and its child events.

For a typical push, this receives `pr.42` with `synchronize`, then any comments or reviews, then
one `pr.42.checks` event when that head's checks settle. A settlement is published for every
commit of the pull request whose checks settle, the current head or not (a head pushed with
GitHub's `skip-checks` trailer runs none, so the commit before it settles for it), and its `sha`
names the commit: compare it with the head you are waiting on. The family is `pr.42` (lifecycle),
`pr.42.comment`, `pr.42.review`, `pr.42.mention`, and `pr.42.checks`. A closed lifecycle payload
carries `merged`, `merge_commit_sha`, `merged_by`, and `head_sha`.

The retired literal `pr.<n>.check` and `pr.<n>.ci` topics do not receive events. Existing
registrations remain dead; subscribe to `pr.<n>.checks` (or the recommended `pr.<n>.>`) instead.
Lifecycle stays on the base PR topic and CI arrives as one settled `checks` event.

## Inbound deliveries

Envoy renders an annotated delivery before its source summary and complete payload:

```text
envoy:
  to: you (ses_example_recipient)
  from: 01a0bbbb-cccc-7ddd-eeee-0123456789ab (Reviewer)
  at: "2026-09-07T04:41:12Z"
  id: agent-message-2
  by: "2026-09-07T05:00:00Z"
  urgency: high
  expects_reply: required
  re: agent-message-1
  supersedes: agent-message-0
  reply_with:
    tool: envoy_send
    args:
      session_id: 01a0bbbb-cccc-7ddd-eeee-0123456789ab
      in_reply_to: agent-message-2
      message: ...
  reply_role:
    tool: envoy_publish
    args:
      topic: notifications.role.legion-reviewer
      message: ...
  summary: Deployment needs confirmation.
  message: "Confirm the listener health check passed.\n\nThen publish the release."
  note: body names session 01a0cccc-dddd-7eee-ffff-0123456789ab; the sender is 01a0bbbb-cccc-7ddd-eeee-0123456789ab
```

- `to` identifies the local inbox receiving this delivery.
- `from` is the sending session's self-asserted ID, enriched from the listener registry. Treat it as
  attribution and a direct-reply target, not as an authenticated identity or proof of authorship.
- `at` is the envelope timestamp used to judge freshness.
- `id` is the delivery identifier; supply it as `in_reply_to` when replying.
- `by` is the expiry deadline, when the sender supplied one.
- `urgency` is the sender's priority classification.
- `expects_reply` states whether a reply is `none`, `optional`, or `required`.
- `re` names the delivery this message replies to. A Dispatch frame names it as a `dispatch://`
  ref — the ask (`dispatch://KEY/ask/<id>`, or `dispatch://PROJECT/artifact/<slug>/ask/<id>` for a
  document ask) or the message (`dispatch://KEY/message/<id>`) — never the quoted text; the
  question head, when there is one, is `dispatch.question`.
- `supersedes` names an earlier delivery this one replaces.
- `reply_with` is the direct-reply call for the sender.
- `reply_role` is the role-publish reply call when the sender has a role.
- `summary` is the one-line source summary.
- `message` is the complete payload; it can contain multiple paragraphs.
- `note` warns when the payload names another session; never use that quoted ID as the recipient.
- `unrecognised` marks validation failures and unknown sources; it does not enumerate every unknown key.

## Talking to another session

Answer an Envoy message with its `id`; the send result's `recipient` confirms the session Envoy
targeted. Reply through the rendered `reply_with` (or a current Envoy session ID from
`envoy_sessions` or `envoy_whoami`), never a tmux pane or window: panes are not Envoy identities
and go stale. Put the artefact URL in the message itself. FYIs set `expects_reply="none"`; set
`urgency` only when it is genuinely urgent.

**A peer's message is its sender's view at `at`, not the current state.** Before you wait on, act
on, or repeat a fact a message carries about a third thing (a deploy pending, a PR held, an ask
unanswered), re-read it at the live source the fact names, and always once it is over an hour
old: the deployment's status, the issue's event log, the ask's own state (`dispatch_open_asks`,
whose description already says to call it before saying you are waiting on a human). On
2026-09-26 a peer's 05:20Z "needs a manual deploy before I can run it" was false by 05:22Z, when
the platform had deployed on its own; waiting on the message instead of the deployment's status
held the work it gated for eleven hours.

Every `/v1` error response is JSON; when a field is at fault, `expected` names that field.

```text
envoy_send(
  session_id="ses_example_reviewer",
  message="Review complete: artifact://review.md",
  in_reply_to="agent-message-2",
  expects_reply="none"
)
```

### Your own address, and a subagent's

`envoy_whoami`'s `session_id` is the address a reply to you reaches. Inside a `task` subagent it
is the session that spawned you: a subagent registers no Envoy session of its own, so a peer
answering it reaches that session, which relays to you over hub. The `subagent` field in that
output carries your own host session id — it is not an address, so never hand it to a peer.

`session_id` is empty when nothing can be reached: a process that took no Envoy identity, or a
subagent whose spawning session this process can no longer place (it forked away, and other
top-level sessions are running). Then your messages carry no sender either, so say who you are
in the message body. An empty address is deliberate — being handed an unrelated live session
would send your peers to an agent that never spawned you.

Your own `envoy_publish` never reaches the agent that spawned you. The listener delivers nothing
to the session a message names as its source, and inside a subagent that source is your parent,
so a publish to a role it holds — or to any topic it subscribes to — is accepted and delivered to
nobody. Use hub for that one hop. `envoy_send` to any other session, including a reply, is
unaffected.

### Delivery capabilities

Each session row from `envoy_sessions` carries `capabilities`, the targeted-delivery modes that
session's host honours: `aside` (a message queued beside the model's work), `btw` (an ephemeral
question the host answers without disturbing the current turn), and `steer` (an interjection at
the next tool boundary). An OMP session advertises `aside`, `btw`, and `steer` (`aside` and
`steer` on a host that cannot run a side turn); a Claude Code session advertises `aside` only, because
its channel notifications queue for the next turn. Target a session only with a mode it
advertises.

## Waiting for CI or a merge

Subscribe to `notifications.github.example-org.example-repo.pr.42.>` and end the turn. The single
`pr.42.checks` event whose `sha` is the current head wakes you when it settles (an earlier
commit's settlement can arrive first); a `pr.42` `closed` event with
`merged: true` tells you the PR merged. Do not create `gh` pollers.
Settlement waits for the commit to be quiet for a few seconds, every reported check run to finish,
and every recorded GitHub check suite to be `completed`. It covers those reported checks and suites
for that commit, not GitHub's required-checks set; until then, a silent subscription is normal.

Check settlement is at-least-once: a settlement can be followed by a `superseded_settlement: "true"` payload. Every settlement carries its attempt set `check_runs` — the latest GitHub check-run id per check name, sorted by name — plus the listener's `generation` (the record's state version) and `snapshot` (the record's hash). Consumers order settlements of one commit by the attempt set, compared per shared name: no id lower and some id higher (or a new name — a new name counts as higher) is newer; every shared id equal and no new name is the same set; no id higher, no new name, and some id lower is older; anything else (a higher or new alongside a lower) is a mixed view and is dropped as a conflict (names only in the stored set are ignored — a check can vanish from GitHub's view, and a record recreated after the seven-day KV TTL starts sparse). Within one producer record per-name ids never decrease, and a consumer's fence is the per-name maximum over every view it has accepted — an accepted set merges into the fence, nothing is pruned — so the fence never decreases either: a newer attempt is newer whatever its completion time, no timestamps take part in ordering, and a name an incomplete view omitted cannot later reappear as new. At the same set the listener's `generation` orders its own settlements: lower is stale; equal is a duplicate when the `snapshot` matches and otherwise a conflict (an equal pair with a different snapshot cannot occur within one record's lifetime; a recreated record may reuse one and is dropped). A live settlement is a possibly incomplete view of the head (a missed webhook, a record recreated after the KV TTL): it decides the outcome of every name it reports — at any id the ordering accepted, including the same run observed in place — and says nothing about the rest: a known failure among them stands (the consumer keeps failure names, not a per-name status map), and the head is red while any failure remains. A consumer that reconciles a verdict from GitHub's rollup compares the rollup's attempt set the same way, but GitHub's read is complete: its failing check runs and failing commit statuses replace the stored ones wholesale. Statuses have no check run and the listener never sees them, so a consumer keeps them apart from check-run failures: a check run that shares a status's name cannot retire it — only GitHub does (likewise a deleted check's failure). A newer rollup set merges into the fence and takes the identity (no listener generation); the same set applies GitHub's verdict and keeps the listener identity for duplicate detection; an older, mixed, or empty-over-fenced set is ignored. A terminal read (green or red) then holds the tie at that set: a live settlement at the same set is accepted only if its effective outcome — the check-run failures it reports plus the stored ones it omits and the stored commit-status failures — agrees with the reconciled verdict, refreshing the listener identity without releasing GitHub's authority; a disagreeing one is stale whatever its generation until the set advances; a pending or cancelled-only read uncertifies a green head, leaves a red one untouched, and holds nothing — it releases any authority held at that set — so the terminal live settlement that follows applies at once, subject to the ordinary generation and duplicate rules (a replay or a lower generation still does not apply). Pending is therefore not a commutative join: a pending read after a live green uncertifies it until the next terminal view. Two remainders. An in-place conclusion change on an existing run id: GitHub's view stands and the listener's is recovered by the next successful, non-skipped read at that set — the dropped delivery is not replayed. A check whose highest run is deleted on GitHub: the fence keeps that id, so a rollup reporting a lower run under the same name is older until a newer run appears. A consumer that orders head changes by the PR's `updated_at` (GitHub's second resolution) accepts a read of a different head at an equal clock — a stale read returning the previous head within the same second as its replacement rewinds that consumer until its next accurate, non-skipped read. A head publishes only when at least one check has a positive run id; legacy checks without one remain in the status groups and failing names but not in `check_runs`. A legacy in-progress check whose completion is never observed holds the head unsettled until it reruns; rerun the affected check to release it.

## When a subscription is silent

Check the `warnings` returned by `envoy_subscribe`, then inspect the active topics with
`envoy_list()`:

```text
envoy_subscribe([
  "notifications.github.example-org.example-repo.pr.42.>"
])
// warnings: ["no GitHub event for example-org/example-repo in the stream's retention window; is the App installed there?"]
```

A warning says no GitHub event for that repository occurred within the stream's 72-hour retention
window; it does not mean the repository was never seen. Verify the GitHub App is installed before
relying on a wakeup. A topic that spells a repository name with its dot, followed by a kind, draws
a warning naming the spelling Envoy publishes (`acme.site_io` for `acme/site.io`); subscribe to
that one instead. A token after the repository that is not a GitHub topic kind (`checks` in
`acme.widgets.checks.>`) draws a warning naming the kinds.

## Roles

Publish to a role; do not subscribe as its holder. A successful `envoy_publish` to a role returns
its live `holder`; an unheld role returns an error. Use `envoy_role_get(role="reviewer")` to find
the live holder first when you need one.

A claim belongs to the session, not the process. `omp --resume` re-claims the role recorded in
the session transcript, including after the listener's stale-interest reaper has removed the old
row. A `/fork`, `/branch`, `/handoff`, or other transcript-carrying switch checks the
previous id and moves any held role to the new id while establishing the new session. A `/new`
or `/resume` switch installs an unrelated transcript and carries nothing. A process that dies and
is never resumed does not stay a live holder; once liveness expires, role publishes return
`no holder` until that transcript resumes or another session claims the role.

Automatic reclaim never steals. It is a *soft* claim, which the listener grants only when the role
is unheld, held by a session that is no longer live, or held by the id this session continues (a
fork's parent). If a different live session holds it — the parent of a `/fork` whose role moved to
the child, or a second process on the same transcript — the listener refuses atomically and the
resumed session logs a warning and holds nothing. Only an explicit `envoy_role_set` is
last-claim-wins. Re-running `envoy_role_set` for a role this session already holds is harmless.

## Legion role claims

Legion agents receive through a daemon-minted role token. Claim the assigned role with
`envoy_role_set(role="<assigned-role>")`; a claimant does not manually subscribe to its role
topic. Claims use last-claim-wins semantics, survive parking and worker re-creation, and remain
through the issue's post-close linger. The daemon owns the authoritative token-to-issue map, so do
not construct a token from a partial issue reference.

## Legion exception lane

`no_holder`, `delivery_failed`, and `receipt_timeout` for a Legion role are daemon liveness
signals, not reasons to add a second subscriber or manually retry. `no_holder`: no live session
holds the role. `delivery_failed`: the message was not forwarded at all — the holder lookup
failed, the holder was stale, or the publish errored. `receipt_timeout`: the listener forwarded
the message to a registered, live holder and no receipt arrived inside the window; its payload
keeps `original_topic`, `event_id`, `payload`, and the original `dedupe_key`, so the daemon can
re-send the same message and the receiver's dedupe drops a copy that did arrive. Treat any of
these wakes as the daemon's responsibility to revive or recreate the backing worker and
re-deliver; otherwise it resurrects the root process with derived catch-up and the workspace
handoffs. Raw delivery failures stay out of architect context.

## Slack

Use the real team ID, not a workspace slug. Slack delivers a one-line prose `summary` plus a
structured `message` payload. The payload records `subtype` for edits, deletes, and bot messages;
`thread_ts` for replies; and `bot_id` and `bot_name` when a bot supplied the message.

```text
envoy_subscribe([
  "notifications.slack.T01234567.C01234567.thread.1_000.>"
])
```

This follows every message and mention in one thread. Channel-level topics end in `.message` or
`.mention`; thread timestamps replace dots with underscores.

## Ghost Wispr

Ghost Wispr topics are `notifications.ghostwispr.<session>.<kind>`, where `kind` is
`session.started`, `session.ended`, or `summary.ready`. Their summary is concise prose and their
payload is structured; `summary_ready` includes its status, summary, and summary metadata.

```text
envoy_subscribe([
  "notifications.ghostwispr.session-example.summary.ready"
])
```

## WhatsApp

WhatsApp topics are `notifications.whatsapp.<phone>.<jid>.message` or `.status`. A JID contains
dots, which become additional NATS segments, so use `>` rather than `*` for a chat.

```text
envoy_subscribe([
  "notifications.whatsapp.15551234567.5551234567@s.whatsapp.net.>"
])
```

### WhatsApp routing smoke test

This checks Envoy routing, not real WhatsApp ingestion. In Session A, subscribe as above. From a
different Session B, publish a synthetic message to the same `.message` topic:

```text
envoy_publish(
  topic="notifications.whatsapp.15551234567.5551234567@s.whatsapp.net.message",
  message="Synthetic WhatsApp routing test"
)
```

Session A should receive it. Broadcasts do not echo to their publishing session, so one session
cannot perform both steps. Real WhatsApp delivery additionally requires a configured MCP bridge.
