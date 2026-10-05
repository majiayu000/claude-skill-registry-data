---
name: legion-controller
description: Use when handling Legion controller wakes for root-issue triage, keeping the admission slots full from `todo` issues, the daily report, architect escalation, resync healing, or human interaction.
---

# Legion Controller

The controller is the one persistent, wake-driven session for a Legion project. It keeps the
project's admission slots full with the highest-priority work, and makes triage, escalation, and
human-interaction judgments; it never does phase-worker work or routes raw events into an
architect.

## Start and claim the controller role

The Legion extension claims `legion-<project>-controller` and registers controller readiness
with the daemon during session startup. Do not handle a wake unless that startup succeeded.

The daemon runs the controller as an interactive OMP terminal session in its private tmux
server (the pane runs plain `omp`, not `--mode rpc`, and no `legion worker-shim`; the operator reaches
it with `tmux -L legion-<project> select-window -t <window id> \; attach -t legion-<project>`,
the window id being `controllerLocator.tmuxWindowId` in `legion state --json` — every window
opens detached, so a bare `attach` lands on whichever window is current). The operator may attach and
type into this session at any time. The pane carries no GitHub credential: its GitHub token
variables are emptied, and both `legion gh -- <args>` and `legion threads resolve` are refused.
The controller reads Dispatch and applies its controller capability with `legion status <KEY>
<status>`; it never reads GitHub or merges a pull request.

For an interactive takeover from a hand-started OMP session, start OMP with
`LEGION_CONTROLLER_SECRET` (or `LEGION_CONTROLLER_SECRET_FILE`, a path to a file holding it),
`LEGION_DAEMON_URL`, `LEGION_STATE_DIR` (the daemon's state directory), and `LEGION_GRANT_FILE`
(an absolute path to a file only you can read, under a 0700 directory; the extension writes
each command's grant there and every `bash` call is blocked without it) in its environment. Do
not set `LEGION_CONTROLLER=1` — that marker is the daemon pane's own, and a session carrying it
claims at startup and reports its transcript as the pane's. Then run:

```text
/legion-claim-controller
```

The command resolves the project from daemon state, claims the Envoy role for the current
session, and posts readiness before controller commands can act. From then on this session's
shell commands are wrapped with a controller grant, but the grant holds no GitHub credential;
`legion status <KEY> <status>` works through the controller secret in this session's environment
(`LEGION_CONTROLLER_SECRET` or its `_FILE`), not the grant — if it fails, that is the variable to check.
The takeover moves the role
and the daemon's recorded session id to this session; it never replaces the transcript the
daemon recorded for its own pane, so a later respawn of that pane resumes the pane's own
conversation, not yours. Never pass a secret as a command argument or copy it into a transcript.
The claim is kept alive automatically afterwards: the Envoy registration heartbeat re-asserts it
and re-posts readiness whenever the listener loses sight of this session, so
`/legion-claim-controller` is the manual override, not a routine step after a listener restart.

Two limits of a takeover session. It caches the controller secret it started with: after the
daemon respawns its own pane the secret rotates, every `bash` call in the takeover session then
fails with a 403 from the grant mint, and the fix is to start a fresh OMP with the new secret,
not to retry. And the role does not follow `/new` or `/fork` in a takeover session — without
`LEGION_CONTROLLER=1` the new session is not a Legion session to the extension — so after either
command run `/legion-claim-controller` again.

This handshake lets the daemon redeliver held controller work. It does not turn the controller
into a state holder: daemon state and the Dispatch project remain authoritative.

### Started by the operator

When the daemon cannot open a terminal for you — the Go daemon, under either runtime, since it
launches no controller — nobody launched your
pane: the operator ran `legion controller start --config controller.yaml [--daemon-url <url>]` on
their own machine, and you are that foreground OMP session. The command fetched a fresh controller
secret from the daemon with the operator's token, wrote it to a 0600 file under `LEGION_STATE_DIR`
(`~/.local/state/legion/<project>-controller` by default) beside the `gh` shim and the `legion`
launcher, and started you with `LEGION_CONTROLLER=1` and the same environment a tmux controller pane
carries, so nothing changes in how you handle wakes. The extension registers on
`/legion/v1/claims/register` with the
secret, claims the role, then subscribes to `notifications.legion.<project>.controller`, where the
Go daemon publishes the rows marked from the Go daemon in the wake routing table. The daemon records
you as `controllerLocator: {runtime, external: true, sessionId, registeredAt}`, `runtime` being the
daemon's own (`kubernetes`, or `tmux` under the Go daemon). The TypeScript daemon reads your
liveness from the Envoy role registry (the holder of
`legion-<project>-controller` and its `last_seen`), not from a pane: keep the session running.
Exiting it leaves the project without a controller until the operator runs the command again —
the TypeScript daemon logs `controller not registered; run legion controller start` once per
boot-timeout interval and launches nothing itself. `legion state` and `legion status <KEY>
<status>` work here over `LEGION_DAEMON_URL`. A second `legion controller start` replaces you: it
mints a new secret, so your grants stop working and the role moves to the new session.

### What happened before you started (Go daemon)

The Go daemon's controller topic is a wake for a session that is running when it is published.
Envoy hands an Oh My Pi session no retained copy of a notice published before it subscribed, so a
hold, a tree architect's failed claim, a new triage root, or a freed slot from while no controller
ran never arrives as a wake. `legion controller start` opens your first turn with a start message
(`Legion controller start: …`), so every start and restart runs this procedure with nothing typed.
At every start, after the claim recheck ([Turn discipline](#turn-discipline)) and before anything
else:

1. Read `legion state --json` and handle each issue whose `issues.<KEY>.phase` is `held` (its
   `issues.<KEY>.holdReason` is `escalated` when its architect sent it to you, and absent while the
   architect is still deciding or while its tree lingers or is closed, where the hold waits for the
   tree's re-admission and needs nothing from you), and each tree root whose
   `issues.<KEY>.architect.state` is `failed` and whose `issues.<KEY>.phase` is not `done`, exactly
   as the matching wake below. A parked tree (root phase `done`: it lingers or is closed) needs
   nothing from you: a failed architect ignores the park and reads `failed` until the tree closes.
2. List the project's triage issues handed to Legion with
   `dispatch_issues({project, status: "triage", label: "legion", limit: 250, offset: 0})`.
   When its first line ends `(showing 1-250 of N)`, read the next page with `offset: 250`, and so
   on until you have all N rows. The rows show no parent, so open each row with `dispatch_read`
   and follow `Links:` up through each `child_of` parent (a `child_of` under `Referenced by:` is a
   child of this issue, not its parent). Leave a child that has an ancestor in `admission.active`
   or `admission.waiting`: that tree's architect owns it. Triage every other row as a root,
   children outside a live tree included, when `legion state --json` does not record it under
   `issues`. A root recorded there and now in `triage` is work the daemon holds that a human
   pulled back: never re-admit it yourself; name it in your summary to the human ("<KEY> was
   pulled back to triage; what do you want?").
3. Fill the free admission slots ([Keeping the slots full](#keeping-the-slots-full-go-daemon)).
4. Post the day's report when this is your first turn of the UTC day
   ([Daily report](#daily-report-go-daemon)).

The issue record and Dispatch are the truth; the topic is the wake.

### Issues handed to Legion (Go daemon)

The Go daemon works only the issues handed to it with the Dispatch label `legion` (in any case),
since its project may be shared with humans and other agents. It never admits a root in `todo`
without the label, and wakes you for a root in `triage` only while the root carries it and is
unrecorded: on its creation with the label, and on each change to it after that while it stays
in triage, the change that adds the label included (the dashboard creates an issue without
labels, so a human adds it from the issue header). Two parties hand work over: a person, who sets
the label from the issue header, and you, when you fill a free slot (below). You label an issue
only when you take it or file it for Legion, so the label means Legion has the issue or had it.
A person's label is their decision: never take it off. A child needs no label: it runs under its
tree's architect once its root is admitted. `legion status <KEY> todo` admits a root, or a child
outside a live tree (admitted as a root of its own), only while it carries the label, so an issue
you hand over or file for Legion to run carries it first (`labels` in `dispatch_issue_update` or
`dispatch_issue`). Taking the label off a waiting root drops it from the waiting line; taking it
off an admitted tree does not stop it.

## Trees waiting on a root claim (Go daemon)

A Go root architect whose claim on its root issue was refused starts nothing and waits, holding
its slot, until the claim is free; nothing tells it when a session holder lets go without
replying. So every turn rechecks them ([Turn discipline](#turn-discipline)), the daemon's `tick`
included, which comes on its interval even with every slot taken: read each root in
`admission.active` whose `issues.<KEY>.phase` is still `admitted` with `dispatch_read`. When its
`Claimed by:` line is `nobody` or ends `· not running`, tell that tree's architect to claim again
with `envoy_publish` to `notifications.role.` followed by its claim token,
`issues.<KEY>.architect.locator.claim` in `legion state --json`. A claim that is its architect's
own, or one that still holds, needs nothing.

## Keeping the slots full (Go daemon)

Picking the next work is your job: nobody hand-feeds issues to Legion. Keep every admission slot
filled with the highest-priority concrete issue Legion can take. The unit of Legion work is a
leaf, an issue with no children, never an umbrella that holds other issues.

**When.** At every start (step 3 above), and on each of the Go daemon's walk wakes. The daemon
sends each only while a controller is registered, and none while one of the same kind is still
unsent:

- `slot-free on <KEY>`: the daemon released `<KEY>`'s slot, because its tree finished or left the
  workflow, and the slot is free by **How many** below.
- `todo on <KEY>`: `<KEY>`, an issue nobody handed to Legion, changed while in `todo` and a slot
  was free, so it may be a new candidate. The daemon holds it back half a minute and folds the
  events of that window into it. Walk the whole list, not only `<KEY>`.
- `tick on <PROJECT>`: the daemon's periodic wake, a minute after it starts and then every
  `controller_wake_interval_seconds` (an hour by default), whatever the slots. An earlier walk
  that found nothing, a day with no event, and [a tree waiting on a root
  claim](#trees-waiting-on-a-root-claim-go-daemon) all get a turn from it.

**Scope first.** The scope the deployment instructions state decides which issues are candidates
at all, before anything below. When they say you hand Legion no issue yourself, or that Legion
runs only issues someone else sets to `todo`, the walk takes nothing: stop here, whatever slots
are free. When they narrow the scope (a repository, a kind of change), a candidate outside it is
skipped (the last row of the table below). With no scope stated, every issue of the project is in
scope.

**How many.** Read `legion state --json`. The free slots are `admission.cap` minus the roots in
`admission.active` and in `admission.waiting` (a waiting root takes the next slot before anything
you add). With none free, stop.

**Candidates.** The project's open `todo` issues, roots and children alike, that have no children
at all and do not carry the `legion` label. Ready work is `todo` (`skill://dispatch`, "Choosing
what to work on"): take the top ready issue, highest priority first, then board rank. An issue that
waits on a deploy or a decision belongs in `backlog`, so the walk takes nothing from `backlog` or
`triage`. The Go daemon runs
only labelled roots, so every root it ran since the daemon required the label carries it: a
labelled root in `todo` is the daemon's to admit or queue, one in `triage` is yours to triage
(step 2 above), and one anywhere else was parked by Legion or by a person. A child you take becomes
a root of its own: the daemon admits a labelled `todo` child whose tree Legion does not run as a
new tree. The `dispatch_issues` rows show no labels and no children, so the listing below filters
neither: both are checked on each candidate (the table's first rows). List the `todo` issues one
priority at a time, `priority: [0]` first, then `[1]`, `[2]`, `[3]`, and `[null]` (no priority)
last, keeping the listing's order within each, which is the board's rank:

```text
dispatch_issues({ project: "<PROJECT>", status: "todo", priority: [0], limit: 250, offset: 0 })
```

When the first line ends `(showing 1-250 of N)`, the next page is `offset: 250`, then `500`. Read
pages only as far as you need: stop listing once the free slots are filled. `<PROJECT>` is the
Dispatch project key, the prefix of this deployment's issue keys (`PROJ-12` → `PROJ`), which is
also `daemon.project` in `legion state --json`: the project key exactly as `legion.yaml` writes it.
A row that shows `claimed by …` and does not end its claim with `· not running` (the route, when
the row shows one, comes after the claim) is claimed, as the table below says: skip it without
reading it.

**Walk.** Take the remaining rows in that order until the free slots are filled. Read each one with
`dispatch_read({ issue: "<KEY>" })` and skip it when any of these holds. `dispatch_read` shows only
the issue's last 10 events, so the rows that read `Events:` are best-effort: the pull-request row
leans on `External links:`, and the label row is the one that never depends on history.

| Skip when | How you check it |
|---|---|
| It carries the `legion` label | `Labels:` lists `legion`, in any case. Legion has the issue or had it, as **Candidates** above says. |
| It has any child | `dispatch_read({ ref: "dispatch://<KEY>/children" })` lists any child, open or `done`. It is an umbrella, and a finished umbrella is still no leaf. That also skips an issue whose only child is done, which is accepted. Its open children are candidates themselves, each in its own place in the order. |
| An ancestor is Legion's | Follow `Links:` up through each `child_of` parent, reading each one, and skip when any ancestor carries the `legion` label or is recorded under `issues` in `legion state --json`, whatever its status: a Legion tree, running or parked, owns its children. An ancestor's claim or route does not skip the issue: a coordinator holding an umbrella files `todo` leaves for others to pick up, and the claim on the issue itself is what keeps two sessions off the same work. A `child_of` under `Referenced by:` is a child of this issue, not its parent. |
| Someone is designing it | `Open asks:` lists any ask, a `Spec approval: awaiting …` line shows the spec waits on a human, or `Events:` show an `artifact.version` or an `ask.opened` from the last seven days: a session or a person is shaping it even when nobody claims or routes it. |
| Legion ran it without the label now on it | `legion state --json` records it under `issues`, whatever its status, or `Events:` show a status write by `session legion-daemon:<PROJECT>`, the daemon's actor on every `legion status` (yours included) and on its own `in_progress` at admission. That covers a root a person took the label off, and one that ran before the daemon required the label and never had it. Name each one you skip for this in your summary. The walk never sends a root Legion already ran back into Legion: a person does that with the label and `todo`, and you do it only when a wake below says to (`worker-died`, closed-tree activity). |
| A running session or a person claims it | `Claimed by:` names anyone and does not end `· not running`. `· liveness unknown` counts as claimed: the agent registry could not be read, so nothing says the holder stopped. A claim ending `· not running` has lapsed, and the issue is free. |
| Its route reaches a running session | `Route:` names a route with nothing after it, or with `(held by …)`. `(nobody holds it right now)` and `(that session is not running right now)` reach nobody; `(the Envoy listener did not answer, …)` counts as reaching someone. `Route: none` is free. |
| A pull request is linked or named | `External links:` lists a pull request (kind `github_pr`, or a URL ending `/pull/<n>`), or a comment or message among `Events:` names one. You cannot read GitHub, so an open, merged, or closed pull request all count. A person who wants Legion on it anyway hands it over themselves: the label, then `todo`. |
| Its assignee is working it | `Assignee:` names a person who holds the claim (the row above), or whose own comment or message among `Events:` says they are working on it. The assignee alone is who answers the issue's questions, not who works it. |
| It is outside this deployment's scope | Read the scope the deployment instructions state against the title and, when the title does not settle it, the spec (`dispatch_doc_read({ issue: "<KEY>" })`). When in doubt, skip it. With no scope stated, every issue of the project is in scope. |

**Take.** For each candidate that passes, in order:

1. Add the label and keep the labels it has, which `Labels:` lists (`none` is no labels). `labels`
   replaces the whole set, so a label you leave out is removed.

   ```text
   dispatch_issue_update({ issue: "<KEY>", labels: ["<each current label>", "legion"] })
   ```

2. It is already in `todo`, so the label admits it: the daemon records it and gives it the free
   slot, or queues it in `admission.waiting`. It needs no status write.
3. Post one short comment that says Legion took it, who is asked at its design gate, and how to
   undo the take, naming the assignee with the sentence [New issue triage](#new-issue-triage)
   step 4 gives (which follows the design gate policy):

   ```text
   dispatch_comment({ issue: "<KEY>", body: "Legion took this issue: it was the highest-priority open issue nobody else was working on. Assigned to <login>, who will get this tree's questions and its design approval. To stop Legion, move the issue to backlog. To keep Legion off it for good, also take the legion label off; taking the label off alone does not stop a tree that has started." })
   ```

The daemon admits each root when Dispatch's event reaches it; the next `legion state --json`
shows it in `admission.active`. When the candidates run out with slots still free, leave those
slots free and say so in your summary.

## Daily report (Go daemon)

Once a day, post one Dispatch message that says what Legion finished, what it closed without a
change and why, and what is running.

**Where.** On the issue the deployment instructions name for Legion's reports. With none named,
on the project's `Legion daily report` issue:
`dispatch_search({ query: "\"Legion daily report\"", project: "<PROJECT>" })` finds it. When it
does not exist, create it once and park it in `icebox`, so nobody takes it as work; it never
carries the `legion` label:

```text
dispatch_issue({ project: "<PROJECT>", title: "Legion daily report", spec: "## Summary\n\nLegion's controller posts one message here each day: what Legion finished, what it closed without a change and why, and what is running. This issue is not work, so it carries no `legion` label and stays in icebox." })
legion status <report KEY> icebox
```

**When.** On your first turn of each UTC day, whatever it is: your start, or a wake of any kind.
While you are registered, the daemon's `tick` gives you a turn at least every
`controller_wake_interval_seconds`. After the turn's own work, read the report issue with
`dispatch_read`, and post when its `Events:` show no `message.created` from today.

**What.** One `dispatch_message({ issue: "<report KEY>", body })` of at most 2,000 characters,
written as `skill://dispatch`'s "Writing for the human" says: every issue by its key and title,
every pull request by its URL.

- **Finished.** `dispatch_issues({ project: "<PROJECT>", status: "done", updated_since: "<the
  previous report's time, or 24 hours ago>", limit: 250 })`, read every page, and keep the issues
  `legion state --json` records under `issues` whose `issue.closed` event is after the previous
  report. For each, `dispatch_read` it: the pull request under `External links:` is the one that
  merged.
- **Closed without a change.** Those with no pull request, each with the reason its closing
  message gave (the `message.created` just before `issue.closed` among `Events:`).
- **Running.** Each root in `admission.active` with its `issues.<KEY>.phase`, and the roots in
  `admission.waiting`. A root whose architect told you its claim was refused is named as waiting
  on that holder: its architect started nothing and asked them to release it or take the issue
  back. Nothing in `legion state` records that, so read the tree's issue (its `Claimed by:` line
  and the ask or message the architect opened) before you name it.
- **The slots and the walk.** The free slots, as **How many** counts them, then this turn's walk
  when it made one: what it took, and how many candidates each row of the table skipped, so a
  reader can see why a free slot stays empty.

A day with nothing finished says so in one sentence. When the lists do not fit, keep the counts
and the highest-priority issues.

## Deployment instructions

Deployment instructions, when present, are the operator's standing rules for this repository —
required checks, deploy/smoke commands, code-owner expectations, and standing roles you may
consult. They override this skill's defaults where they conflict, and may narrow which issues the
walk takes, but never widen it past `todo` issues or change the order it takes them in: highest
priority first, then board rank ([Keeping the slots full](#keeping-the-slots-full-go-daemon)).

## Turn discipline

- **Direct user message always first.** If this turn includes a direct user message, answer
  it before handling every other wake.
- **One wake = one turn.** Handle exactly the wake's implication, then end the turn. Never
  poll, idle-loop, or wait for another event. Two additions, after any direct user message: every
  turn under the Go daemon first rechecks the [trees waiting on a root
  claim](#trees-waiting-on-a-root-claim-go-daemon), and your first turn of each UTC day, whatever
  woke you, also posts the day's report ([Daily report](#daily-report-go-daemon)).
- **Wakes are advisory.** Before any side effect, verify the current daemon state and the
  relevant Dispatch issue. A stale or duplicate wake may cost a read, never a wrong action.
- **Controller state is disposable.** Do not reconstruct or preserve local controller
  bookkeeping between turns.
- **Write for a human.** Every `dispatch_comment`, `dispatch_message`, and `dispatch_ask` you
  post follows `skill://dispatch`'s "Writing for the human" rules: plain sentences, every
  identifier expanded on first use, no coined shorthand. A triage note that reads like a log
  line is not a triage note.

## Wake routing table

| Wake | Content | Controller action |
|---|---|---|
| New issue created in the Dispatch project (`issue.created`, status `triage`; under the TypeScript daemon resync heals misses, under the Go daemon the boot step above does). From the Go daemon: `triage on <KEY>` (payload `{kind: "triage"}`) on the controller topic, for an unrecorded root carrying the `legion` label only ("Issues handed to Legion" above) | issue key + triage context (incl. pre-existing children) | Triage: `legion status <KEY> todo` to admit, or set `backlog`/`icebox` to park |
| Backlog eligibility (TypeScript daemon) | slot freed / priority change | Reconsider parked items and move the eligible root to `todo` |
| `slot-free on <KEY>` from the Go daemon (payload `{kind: "slot-free"}`) | the root whose slot the daemon released with no waiting root to take it | Verify a free slot in `legion state --json`, then fill it ([Keeping the slots full](#keeping-the-slots-full-go-daemon)) |
| `todo on <KEY>` from the Go daemon (payload `{kind: "todo"}`) | an issue not handed to Legion that changed while in `todo` and a slot stood free, sent half a minute later | Verify a free slot, then walk the whole `todo` list ([Keeping the slots full](#keeping-the-slots-full-go-daemon)) |
| `tick on <PROJECT>` from the Go daemon (payload `{kind: "tick"}`) | the project key; the daemon's periodic wake, whatever the slots | Recheck the trees waiting on a claim, then walk if a slot is free; post the day's report if this is the day's first turn |
| Architect escalation (controller-actionable only: re-file a child as a root issue, capacity, cross-tree conflicts) | request + context | Judge and act; the owning architect writes an issue-design decision as a decision block and opens `dispatch_ask` only for a human to-do |
| Resync report | artifact-driven anomaly list (zero-owner trees, untriaged-open, launch-failed, admission-drift) | Verify against fresh state, then heal |
| Resync report: `admission-drift` entry | issue key + whether the daemon added it to, or removed it from, its admission list (the detail says which) | No action: the daemon already repaired it in the same run. An issue that reappears in consecutive reports is a live leak — file a LEGION issue on Dispatch with both reports pasted as evidence (never a GitHub issue) |
| `child-status` | child key + status transition | Not controller-actionable by default; if the daemon could not route it to the parent's architect role, verify the transition and forward it with `envoy_publish` |
| Mention | Slack/GitHub PR @mention text | Answer, or route to the owning issue's architect role |
| READY packet seen on a Dispatch issue (via issue subscription) | READY line + gate facts | No action: a human merges; the merger has already notified the queue role if the project has one |
| `worker-recovered` (role `architect`) from the daemon | issue, fromRef | A root architect's tree volume was lost; it restarted as a new session. Verify the tree is active in `legion state` and that the architect posts its next step on the issue within one resync interval; otherwise treat it as an anomaly. |
| `held on <KEY>` from the Go daemon (payload `{kind: "held", phase, role?, reason?}`) | the held issue, the phase it left, and the role whose claim failed, or `reason: "escalated"` | Verify the hold in `legion state` (the issue's phase is `held`). Without `reason`, a phase worker's launches or prompts ran out and the tree's architect decides retry or escalate: no action. With `reason: "escalated"` (on the record, `issues.<KEY>.holdReason` is `escalated`), the architect sent it to you: handle it as an architect escalation below. Parking the tree is `legion status <root> backlog`; setting the root back to `todo` later re-admits it as a new generation, which starts again from its architect |
| `worker-died on <KEY>` from the Go daemon with `role: "architect"` | the tree root whose architect's claim failed, and the phase the root was in | The tree's architect ran out of launches or prompts and the daemon relaunches nothing; every other notice of the tree goes to that architect, so nobody inside the tree can act. Verify in `legion state` (`issues.<KEY>.architect.state` is `failed`); if the root's phase is `done`, the tree is already parked: no action. Otherwise re-admit the tree (`legion status <root> backlog`, then `todo`: a new generation, whose architect starts again with fresh budgets) or leave it parked and say why on the issue |
| Closed-tree activity (comment, review, CI on a closed tree) | issue, root, event summary | Read the artifact; if work should resume, `legion status <root> todo`; otherwise no action — the event is not held or redelivered |
| Direct user message | — | Always first |

## New issue triage

1. Read `legion state --json`, then inspect the reported Dispatch issue with `dispatch_read`.
   Verify the issue is in this project, is eligible for a root process, and whether it
   has pre-existing children. Dispatch and daemon state, not the wake text, decide triage.
   Note the `Assignee:` line: that human answers the tree's asks, and their Inbox opens on
   the issues they hold. Never reassign during triage — who holds an issue is the humans'
   decision, made from the issue header.
2. If it should run now, admit the root issue:

   ```text
   legion status <issue> todo
   ```

3. If it should deliberately wait, move it to a parked status instead of leaving it in
   `triage`:

   ```text
   legion status <issue> backlog
   ```

   (or `icebox` for longer-term deferral). Dispatch status is the durable record; there is no
   other marker to maintain, beyond the Go daemon's `legion` label, which parking leaves in
   place. Under the Go daemon a root never waits for capacity in `backlog`: in `todo` the
   daemon's admission queue holds it (`admission.waiting`), so park only a root that should not
   run now. Do not triage a system-created child as a root issue.
4. When you post a triage note (a `dispatch_comment` on the issue saying what you decided and
   why), name who will be asked with the assignee sentence: `Assigned to <login>, who will get
   this tree's questions and its design approval`, or, when the `Assignee:` line says
   `unassigned`, `Unassigned — nobody's Inbox shows this tree's questions or its design approval
   until someone takes it from the issue header (Assignee, beside Priority)`. The design approval
   is promised only when the `Design gate policy:` line of your system prompt, which
   `legion controller start` writes from the daemon's own configuration, says
   `gates.design: root-issues`. Under `gates.design: off` nobody approves a design, so drop "and
   its design approval" (and "or its design approval") from the sentence. An unassigned root
   still runs; the architect's asks wait in every Inbox's Unassigned band.

## Backlog eligibility

Under the Go daemon nothing reconsiders `backlog` or `icebox` on its own: [Keeping the slots
full](#keeping-the-slots-full-go-daemon) takes only `todo` issues, since an issue that waits on a
deploy or a decision belongs in `backlog` (`skill://dispatch`, "Choosing what to work on"). A
handed-over root waits for a slot in `todo`, where the daemon's
admission queue holds it (`admission.waiting`), so a park means "should not run now", and a
parked root keeps its `legion` label. A parked issue runs again when a person sets it to `todo`,
or when a wake tells you to re-admit it (`worker-died`, closed-tree activity).

Under the TypeScript daemon, when a slot frees or priority changes, use `legion state --json` and
the current Dispatch issue to reconsider parked roots. Admit the selected root with
`legion status <KEY> todo`. Moving an item to or from `backlog`/`icebox` is a deliberate
controller decision, not a no-op.

## Architect escalation

Only decide controller-actionable escalations: re-filing independent work, capacity, and
cross-tree conflicts. The owning architect writes an issue-design decision as a decision block and
uses `dispatch_ask` only for a human to-do, not the controller.

For an independence judgment, verify the child and its parent against current daemon state
and the Dispatch issue. If the work belongs in an independent root:

1. File a **fresh root issue** with `dispatch_issue({ project, title, spec })` (no `parent`;
   under the Go daemon add `labels: ["legion"]`, without which it is never admitted).
   `project` is the issue key's prefix before `-<n>` (e.g. `LEGSMOKE-3` → `LEGSMOKE`): the
   project key exactly as `legion.yaml` writes it, which `legion state --json` shows as
   `daemon.project`. It is not the lowercase project token in role names such as
   `legion-<project>-controller`.
2. Park the child (`legion status <child> icebox`) and leave
   a pointer to the new root issue. The controller's capability is `todo`/`backlog`/`icebox`
   only — only the owning architect or the daemon closes an issue as `done`.
3. Admit or deliberately backlog the new root through the normal triage procedure.

Never promote a child in place. Resolve capacity and cross-tree conflicts from verified
state, routing design decisions back to the owning architect when they are not controller
judgments.

## Resync report

Treat a resync report as an anomaly list, not an instruction. For every zero-owner tree,
untriaged-open, or launch-failed issue it names, verify `legion state --json` and the
current Dispatch issue first. Then heal the verified condition: admit an eligible root, move
an issue back to its intended status, or use the applicable daemon control path. Do not act
on stale entries until their source artifact explains the anomaly. An `admission-drift` entry
needs no healing — the daemon added the tree back to (or removed it from) its admission list in
the same run; verify only that the same issue does not recur in the next report, and file a
LEGION issue with both reports if it does.

## Mentions

Read the mention and its artifact. Answer it when it asks the controller for triage or
human-facing information. A human asking how to let a root proceed past its design gate
approves the root issue's spec document in Dispatch — the `Approve` control in the document's
header, or the approval question the architect's request opened in the Inbox. The controller
never opens a gate and there is no operator command for it; a project that does not want the
gate at all runs `gates.design: off` in its `legion.yaml`. Otherwise resolve the authoritative
owning architect role and route the verified context with `envoy_publish`. Do not route raw
event traffic or invent a role token from a partial issue reference.

