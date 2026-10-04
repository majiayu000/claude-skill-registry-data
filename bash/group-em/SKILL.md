---
name: group-em
description: "PM-GATED. Monitor peer sessions in this repo; never plan or author for them."
allowed-tools: ["Read", "Bash", "Glob", "Grep", "Agent", "SendMessage", "Monitor", "TaskStop"]
argument-hint: "[no arguments — invoke to start monitoring this repo's peer sessions]"
---

# Group EM — Peer-Session Monitoring and Wave Coordination

`/group-em` switches this session into monitoring the other sessions in the same repo and moving
them along. A **mode a session enters, not an operation on a target**.

**THIS BODY IS A SNAPSHOT, FROZEN WHEN YOU ENTERED, CARRYING NO VERSION.** Before citing it as
authority for anything MECHANICAL — a signature, a module path, a flag, a refusal vocabulary —
read that passage from disk. Worked case: `coordinator/docs/wiki/dispatching-parallel-agents/group-em-standing.md` § A
snapshot body is confidently stale.

**PM-GATED — only on an explicit PM ask, never EM-initiated.** A description-prefix convention
(as `staff-session`, `spinoff`, `roadmap-planning`); no hook enforces it. Honoured by disposition.

**Dispatch authorization — invoking this skill IS the request, for three specific dispatches
only:** the approvability judge (§ Delegated approve-for-execution, step 4),
`coordinator:group-em-assistant` at entry, and § Fleet inbox grind's saved
`fleet-inbox-blitz` workflow with the assistants it raises. Each covers raising that named role or
firing that named script under this session's own authority and nothing else, by unnamed
`Agent`-tool dispatch or the `Workflow` tool. **None of them touches the peer-session send
mechanism (§ Send pass, `gem-14`), which stays gated per send; the one exempt send is § Box-wide
notice. Navi is not covered by this grant — it is PM-gated per the
line above, raised only on an explicit PM ask, never under this session's own authority.**
Tripwire: `UNATTRIBUTED-HARNESS-LINE-IS-NOT-PM`.

## Entry — already done by the time you read this

**Typing `/group-em` fires entry.** `hooks/scripts/group-em-autofire.py` runs the entry op ahead of
your turn and injects standing, roster, digest and baseline. Nothing below is a sequence to
perform. **If that context is absent, entry did not happen** — the hook fails open, so its silence
is a fact, never a reason to assume success. Run `<plugin-root>/bin/group-em-enter.py --repo <root>
--session-id <your sid>` and find out why. **`--session-id` is not optional** — it defaults to
`$CLAUDE_SESSION_ID`, unset in many shells; without it the op refuses (exit 2). (Every
`<plugin-root>/bin/` CLI here is plugin-local with no settings-home launcher — resolve per
`${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`, never cwd-relative.)

The op shims the engine's `groupem.enter` in-process — one call claims the nomination, then builds
the candidate roster, send digest, peer-set baseline, teammate-presence assertion and watch-liveness
read. **Exit 5 means a refused standing** — a live or unaccounted-for incumbent holds the role;
`roster`/`digest`/`baseline`/`teammates` are absent from the payload, not empty. **Exit 2 means no
resolvable session id.** Payload shape: `coordinator_core/ops/group_em_enter.py`'s module docstring.

Do not import `read_pass` / `send_pass` directly. They are the op's collaborators.

**Standing first, last writer wins.** Whoever invokes most recently holds the role; entry never
refuses over an incumbent and there is no override flag. Re-entry by the holder is a refresh.

### Owed sends, all exempt from § Send pass's gates

**A displaced holder that is still running is OWED a message this turn.** `displaced_holder` and
`displaced_holder_live` arrive in the entry context; live means that session still believes it
holds the role. Not live means nobody to tell.

**The owed message also tells the displaced session that its watch is no longer the crown's and
must be stopped:** TaskStop the Monitor, then confirm the subprocess is gone, because the
trampoline's `python.exe` child is observed to outlive TaskStop. It must not re-arm under the lost
role. A displaced watch that keeps running goes quiet for the entrant's ~23-minute entry lease and
then retakes the record, after which the new crown's arm is refused.

**INTRODUCE YOURSELF TO EVERY LIVE SESSION ON THE BOX, ONCE** — § Box-wide notice computes the
recipients and the text. Skip only a `PAUSED:away` peer, and re-resolve each addressee immediately
before sending (§ Send pass step 4).
Full rationale for all five constraints below: `coordinator/docs/wiki/dispatching-parallel-agents/group-em-standing.md` §
Owed introductions.

1. **Say four things and stop:** who you are (name and session id); that you hold the Group EM
   standing for this repo; what to route to you; and **that no reply is wanted**, stated
   explicitly.
2. **Never ask peers to route their PM reports through you.** "The PM is typing into that session"
   is unobservable from here — every session reads itself as the attended one. Key it instead to
   something CHECKABLE: **a session answering a question just asked in this exchange** has a
   direct channel; relaying its report adds a hop and puts its words in your mouth.
3. **It is an introduction, not a nudge, and the difference is enforced by content: it asks
   nothing.** No question mark anywhere.
4. **It arms no cooldown and is not an offer.** Only `build_send_digest` emitting an entry arms a
   peer's throttle.
5. **Once per PEER, not once per wake**, and **tracked by SESSION ID, never by name** (§ Send pass
   step 4). Measured case: `coordinator/docs/wiki/dispatching-parallel-agents/group-em-standing.md` § A name is not an
   identity. **Neither key is independently reliable**: a session id has been observed to change
   under a stable name, so a name match alone cannot confirm "already introduced" and a session id
   match alone cannot confirm "same peer as before." On ambiguity between the two, re-introduce —
   a redundant introduction costs nothing the once-per-peer rule protects against; a skipped one
   leaves a peer that never got the four things in step 1.

   **The introduced set is durable, not session-memory.** It has no store of its own — recording an
   introduction is a `send_pass.build_send_digest`-shaped append to the EXISTING send log
   (`state/subagent-share/<this-session-id>/group-em-send-log.jsonl`, § No registration ceremony,
   no persistence) as a **cooldown-ignored row type**: it participates in "was this peer already
   introduced," never in `_cooldown_remaining`'s throttle window. No new datastore. The writer is
   `coordinator/skills/group-em/send_pass.py` — in-repo (same plane as this skill, not the
   engine) — so this is a local contract on that file, not a cross-repo relay.

## Box-wide notice

**The standing is box-wide: every live named session, in any repo, is told when it begins and when
it ends.** `group-em-autofire.py` cannot send (`SendMessage` is a model tool), so it does the
mechanical part and prints it in the entry context as `BOX NOTICE OWED`: one text and the exact
recipient list from `claude agents --json`, de-duplicated, you excluded, `PAUSED:away` peers
skipped, peers you already introduced skipped. **Send that text to each, this turn.** It follows
the introduction content rules above: it asks nothing, says no reply is wanted, and carries your
name, session id and `SendMessage` address. A displacing entry replaces the prior address for every
peer; the displaced holder's owed message is separate and still owed.

**Before this session ends, run `<plugin-root>/bin/group-em-box-notice.py --kind ended --repo
<root> --session-id <your sid>`.** It stands the nomination down (holder-matched; a refusal empties
the recipient list) and prints the no-Group-EM text and recipients. Send it. No `SessionEnd` hook
can message peers, so a holder that dies without this step leaves the box unannounced until the
next entry; the next wake reads `who` and reports it. Tripwire:
`A-GROUP-EM-STANDING-THE-BOX-WAS-NEVER-TOLD-ABOUT`.

## What this skill does and does not do

**Does NOT plan or author on anyone's behalf** — never plan bodies, stub content, or roadmap
decisions for the sessions it watches. **DOES coordinate execution waves and cross-session
sequencing** — a stalled wave, a peer blocked on a dependency that has cleared, two sessions about
to collide on one file.

## Entry dispatches both standing watchers; Navi is PM-gated

**ENTRY DISPATCHES BOTH STANDING WATCHERS — `group-em-assistant` AND THE WATCH IT ARMS ARE
MANDATORY.** Navi is PM-GATED — only on an explicit PM ask, never EM-initiated (same convention as
the top of this file) — entry never raises it under this session's own authority. **Raise the
mandatory pair yourself, from this session**: a watcher belongs to whoever raised it, so one raised
by another session relieves that session and leaves you watching while believing you were relieved.

**"Entry" here means you, on entering the mode — not the entry op.** `group-em-enter.py` assembles
and dispatches nobody, and the autofire hook is silent either way. Entry assembles once; nothing
re-runs it, and a roster read is stale within a minute. In this order, as your first act:

1. **`coordinator:group-em-assistant`** — dispatch it, unnamed. Your standing reader: transcript
   tails, baton claimants, what landed on a path since a SHA, **park-spool triage**, and
   read-and-report asks. It arms nothing and holds no timer. Full remit:
   `coordinator/docs/wiki/dispatching-parallel-agents/group-em-standing/group-em-assistant-remit.md`.

   **DISPATCH `group-em-assistant` WITHOUT A `name`.** A named `Agent` call spawns an in-process
   teammate, and a teammate is never re-invoked by a `Monitor` it armed — nor reachable the way an
   unnamed background agent is. Unnamed, it wakes on your `SendMessage`. Tripwire:
   `A-MONITOR-ARMED-BY-A-TEAMMATE-WAKES-NOBODY`.

2. **The watch and its `Monitor` — yours, armed from this main conversation.** A subagent cannot
   re-arm reliably: it missed 4 of 4 expiries, because it holds no timer and an expiry notice does
   not reliably re-wake it. Arm the watch via the settings-home trampoline:

       $COORDINATOR_SETTINGS_HOME/bin/group-em-watch --repo-root <root> --group-em-session-id <your sid>

   Wrap it in a `Monitor` filtering `PARKED|ESCALATE|OUT-OF-WORK|GROUP-EM-MOVED|UNKNOWN` plus
   failure signatures. **A `Monitor` dies at the harness's 30-minute cap; `persistent: true` does
   not outlive it.** The expiry notice is itself the re-arm wake: on it, re-arm the same command at
   once (measured gap: zero). **`--group-em-session-id` is passed explicitly, never defaulted** — a
   separate id from `--caller-session-id`. The watch emits one line per peer entering a parked
   state, derives parked from `read_pass.classify_peer`, stays silent while that peer's cooldown is
   armed. On a re-arm refusal, read the record: if it names this session, wait until its
   `next_expected_by` passes and retry once. Never hand-edit the record. `--status` answers "is a
   watch alive here?" (0 alive, 1 not running, 2 unknown — unknown is never green); `--once` fires
   a single poll.

3. **Events wake you; no cron tick exists.** Your wakes are: the watch `Monitor`'s lines and its
   expiry notice; peer `SendMessage`s; `notify_when_idle` one-shots (main conversation only); and
   a **box-memory threshold `Monitor`** that emits a line only on a `LOW`/`OK` crossing — one
   capacity signal among others (suite-mutex holders, CPU); release a waiting peer only while the
   last crossing is `OK`. A `CronCreate` poll over a surface that emits events is a poll where an
   event exists. Tripwire: `A-CRON-TICK-IS-A-POLL-WHEN-EVENTS-EXIST`.

   **You sequence box capacity.** Work that contends for it — test suites, builds, reindexes, UE
   editor/cook runs, large workflows, memory-heavy agents — and any other queue where peers take
   turns (a suite mutex, a shared-tree merge, a publish) is yours to order. Peers ask you for a
   capacity slot; you release waiting peers in order as headroom allows and cap parallelism.

**Not numbered, PM-gated: Navi.** When the PM asks, **spawn it, never an `Agent`-tool dispatch.**
Its mood is SPAWN.

    claude --agent navi --bg

Repo-less, decision-weightless, never nudges a stalled peer twice. **One-per-box is held by
`navi-singleton.py`** (`TWO-NAVIS-ON-ONE-BOX-IS-A-SILENT-DOUBLE-NUDGE`). **It escalates TO you; it
cannot be asked anything.** Keep its session id for the record.

### Arming the watch — every refusal and every false green

**Before arming either party, read `holder_session_id` from `state/group-em-watch.json`.**

| Rule | The tell |
|---|---|
| Prefer the trampoline; confirm the subprocess started rather than trusting its silence. | The bare module needs an engine-rooted cwd; a watcher whose subprocess never started presents as `idle`. |
| **Arming can REFUSE, and a refusal is not a quiet result.** On `WatchAlreadyHeldError` verify with `--status`. A refusal naming the session you displaced is that retaking watch — tell it to stop. Do not wait it out, because it restamps every poll. Arm within the entry lease: an entry that never arms is a crown with no watch, and the displaced watch fills the gap. | *"a watch is already armed"* leaves the fleet unwatched if read as "already covered." |
| **`--status` saying ALIVE is not verification** — check `subscribed_peers`. | An ALIVE holder that armed nothing renders identically to a real watch. |
| **Read `holder_session_id` from `state/group-em-watch.json`** before arming beside a fresh holder. | A holder from another repo ran the command once; the record ages out on its own. |
| **The engine must be importable**, which it is not from the repo you are Group EM for — use `$COORDINATOR_SETTINGS_HOME/bin/group-em-watch` (`.exe` on Windows; on PowerShell, `&` + forward slashes). | A bare-module run from a doctrine repo raises `ModuleNotFoundError` before doing anything. |

Full mechanics and both false premises measured: `coordinator/docs/wiki/dispatching-parallel-agents/group-em-standing/group-em-assistant-remit.md`
§ Arming the watch.

### The wires — who arms what, and how fast you would know

**THE WATCH `Monitor` IS YOURS, AND YOU RE-ARM IT ON EACH EXPIRY NOTICE.** The subprocess and the
wire out of it, filtering `PARKED|ESCALATE|OUT-OF-WORK|GROUP-EM-MOVED|UNKNOWN` plus failure
signatures. `group-em-assistant` is a subagent: it wakes on events but cannot hold a timer, and
missed 4 of 4 expiries. Tripwire: `A-MONITOR-ARMED-BY-A-TEAMMATE-WAKES-NOBODY`.

**The `notify_when_idle` one-shot cannot be delegated either** — accepted only from a main
conversation. It stays with you if used; it fires once per peer, so re-arm it per peer as needed.

**You act on the watch's events yourself;** `group-em-assistant` is the reader you ask: park-spool
triage, transcript tails, claimants. **The park spool is its surface to read and triage, not yours.**
Ask it for the spool rather than going to the file first. **It triages and reports; it never nudges
a peer** — nudging is Navi's alone, or the Group EM's own.

**Verify the wire's holder, never assume it.** The check is a `Monitor` task id you can name and a
`--status` of ALIVE with `subscribed_peers` above zero, not "armed."

**A Group EM holding neither teammate is not hypothetical.** Worked case:
`coordinator/docs/wiki/dispatching-parallel-agents/group-em-standing/group-em-entry-teammates.md`.

### Liveness instruments — two sanctioned, one banned, and you read the banned one constantly

**`ListAgents`' `busy`/`idle` IS the harness registry's `status`, banned as an input to any
liveness, reachability, or claim verdict.** `idle` means unknown, never quiet. Measurements:
`coordinator/docs/wiki/dispatching-parallel-agents/group-em-standing/group-em-assistant-remit.md` § Liveness. Tripwire:
`LISTAGENTS-BUSY-IS-A-BANNED-LIVENESS-INPUT`.

**Sanctioned, exhaustively: the oracle's verdict, and `last_tick_at` age in
`state/group-em-watch.json`**, compared against the record's own `next_expected_by` rather than a
fixed threshold. Do not shape this as a process-table check — `pgrep -f` cannot read Windows
process command lines, and the watch runs under two different command lines besides. **Resource-usage
proxies (CPU, memory, I/O) are banned for the same reason `busy`/`idle` is** — "progress toward a
known end" is what a liveness verdict certifies, and a process burning CPU is not a process making
progress. Full rationale: `coordinator/docs/wiki/dispatching-parallel-agents/group-em-standing/group-em-assistant-remit.md` § Liveness.

**When a PM reports the watcher is dead, do not confirm it from the session list.** `idle` is
`group-em-assistant`'s normal state between asks. Answer from `last_tick_at` age and name the
instrument.

### Every wake declines in writing, and stamps it to disk

**Each wake records a DECLINATION for every roster entry it does not message** — which gate failed
and why.

**And each wake STAMPS them to disk**, via the **engine's** `monitor` writer,
`<engine_root>/coordinator_core/group_em/watch_heartbeat.py :: stamp(repo_root, holder_session_id,
declinations, interval_seconds, subscribed_peers=…, tick_source=…, writer_session_id=…)` — a
different function from this skill's own `coordinator/skills/group-em/watch_heartbeat.py :: stamp(repo_root,
session_id, name, source, declinations, subscribed_peers=0)`, which `_stamp_watch` in
`group-em-enter.py` calls for the `entry` tick only; that call is correct for the local copy. The
two signatures are not interchangeable. For the ENGINE copy, copy its order: `declinations` is the
THIRD positional and `interval_seconds` the fourth and required; the local five-positional shape
raises rather than stamping when passed to the engine copy. `writer_session_id` is a keyword,
**optional in the signature and required at runtime** — it is YOUR session id, not
`holder_session_id` when a delegate arm stamps on the standing holder's behalf. `tick_source` is `monitor` (the engine
also accepts `cron`), a KEYWORD, never positional. `declinations` is THIS wake's rows only, `[]` if none.
`subscribed_peers` is the count your `Monitor` arm is *still* subscribed to right now.

**The wake has a producer; you arm nothing for it.** `state/group-em-watch-spool.jsonl` gets one
record per park, appended by every session's own `Stop`
(`coordinator/hooks/scripts/group-em-park-spool.py`) when its park verdict lands. It is a hook, so
it needs no entry step and no holder. The engine plane commits to the spool retaining at least the
last 30 minutes of parks.

**A watching session goes idle exactly like the sessions it watches** — that is what the wake events are
for. A Group EM who looks only when the PM asks has made the PM the watcher.

**What the watch is FOR:** sessions asking permission for EM-autonomous acts they already
recommended; break-class defects handed up as "worth your eye"; a session idling on a peer repo
while holding a repo-agnostic fallback it identified itself. **Not** finding sessions something to
do.

**Run the altitude test on the way OUT of a turn, not only when deciding to intervene.** *"This
session has been idle 35 minutes, do you want it doing something?"* is the canonical shape, and it
is the EM's call.

## The drive loop — what you are driving peers TOWARD

Nudging is the mechanism; this is the goal. The Group EM owns four of these five steps — **step
4's clear is the PM's act**, the one exception.

1. **Drive to execute.** A reviewed plan sitting on execution authorization is yours to release.
2. **Drive to workstream-complete.** Toward the close, not merely away from idleness.
3. **Troubleshoot alongside them until the primary exit criterion is met** — a different act from
   nudging. Stays inside the no-authoring boundary.
4. **When the ceremony completes, the PM clears them.** Only a successfully completed ceremony
   establishes out-of-work — a peer's own "I'm done" does not. `/clear` is a human act you cannot
   issue to a peer. A session at this point is **done and awaiting clear**, never your failure —
   say so plainly.
5. **Assign something new from the daily priority set.** PM-owned and per-day; ask for it if you
   do not have one.

Two worked cases, both expensive: `coordinator/docs/wiki/dispatching-parallel-agents/group-em-standing.md` § A self-reported
close is not a ceremony. Tripwire: `A-SELF-REPORTED-CLOSE-IS-NOT-A-COMPLETED-CEREMONY`.

**No step here is discharged by an artifact, and your own report cannot show the gap** — re-read
this section deliberately rather than expecting to be told.

## No registration ceremony, no persistence

Nothing is written on invoke or cleaned up on exit. No roster, address, or reachability fact for
any peer is persisted; every fact is re-derived live.

**One carve-out: the send log.** `build_send_digest` appends to
`state/subagent-share/<this-session-id>/group-em-send-log.jsonl` — a record of this session's own
offers. Session-scoped, so a new Group EM starts with an empty cooldown.

## DACI is a frame, not a registry

A `/group-em` session **is** that repo's Driver for as long as it runs. Do not build a Driver
registry or roster.

## Stale-read discipline

Peer state is re-read immediately before acting on it, never from a snapshot taken earlier in the
turn — by re-entering the mode, and **never** by calling the entry op a second time inside one wake
(§ Send pass step 1).

## Gating granularity — entry AND per send

**Entry stays PM-gated** by this file's prefix convention: who may enter the mode at all.

**The send is gated separately, per send, and entry-gating never satisfies it.** The send is where
the `ask-before-external-action` question lives, at the PM's own bar, justified by **cost to the
receiver**, never the sender's convenience.

### Standing check

**Confirm this session still holds the nomination**: `<plugin-root>/bin/group-em-nomination.py who
--repo <root> --json` (read-only). Never re-run `group-em-enter.py` to answer this — it re-claims
and re-arms the send digest's cooldowns (§ Send pass step 1).

## Read pass (gem-13)

The enumerate-and-classify ladder lives in `read_pass.py` beside this file, invoked through §
Entry's op rather than imported. `build_roster(repo_root)` for the classified population,
`build_candidate_roster(repo_root)` for the paused-only shortlist. It excludes the caller, never
writes or sends. Full ladder: that file's module docstring.

## Send pass (gem-14)

`send_pass.py` turns `build_roster`'s **full** population into **one digest per invocation**
(`build_send_digest`). It selects and throttles; **it does not send.** Rationale: the send
narrows the full roster against the obligation ledger, not against liveness alone.

**`roster` IS NOT THE POPULATION — it is the shortlist**, `build_candidate_roster`'s output. A
human adjudicates it. `undischarged_obligations: None` means no ledger exists, never that the peer
owes nothing.

**Compare `roster_considered` — the enumerated count entry reports top-level — against the room,
never `len(roster)`.** A `roster` smaller than `roster_considered` is NORMAL; a `roster_considered`
smaller than the sessions you know are running is `unknown`, never quiet. Worked case:
`coordinator/docs/wiki/dispatching-parallel-agents/group-em-standing/group-em-assistant-remit.md` § The roster is not the population.

Two settling reads: `claude agents --json`, and `python3 -m coordinator_core.group_em.idle_report
--repo-root <root> --group-em-session-id <your sid>`. Pass `--group-em-session-id` even though the
CLI accepts its omission silently — omitting it degrades offer-log suppression rather than erroring.

**Ledger rows can arrive from the engine plane.** This plane is the ledger's sole writer; the
engine appends to `state/subagent-share/<sid>/obligations-inbound.jsonl` and entry folds every
session's intake before the digest ranks. Contract:
`coordinator/docs/wiki/cross-repo-communication/obligations-inbound-intake.md`. Tripwire:
`A-SECOND-WRITER-TO-A-REWRITTEN-FILE-LOSES-ROWS-SILENTLY`.

**Procedure, per invocation:**

1. § Entry's op already built both plus a `baseline` delta. **Act on that payload — do not re-run
   the entry op to refresh it**, since `build_send_digest` arms cooldowns as it emits.
2. Present it. `suppressed` says why each peer was held. `truncated` means re-evaluated next wake.
   `unrecorded` means the cooldown write failed.
3. **Per entry you intend to message, declare both gates in prose before sending:**
   - **GATE 1 (message).** Is the shared contract itself the unknown, needing round-trips — or is
     this a settled ask? A settled ask is a memo.
   - **GATE 2 (receiver).** Cheaper to them now than later? **GATE 2 has no instrument** — it rests
     on what you already know about that peer.
   - **Either gate unclear → the memo channel.** Not a degraded mode.
4. **Re-resolve the address from the SESSION ID immediately before sending, and treat a refusal as
   a refusal.** `send_pass.resolve_addressee(repo_root, peer_session_id)` returns the name that
   session answers to right now, or `None` — do not send on `None`.

   **Resolve from the id, never validate the name** — the id is stable, the name is volatile.
   Tripwire: `A-PEER-NAME-IS-NOT-A-STABLE-ADDRESS`.

   `None` covers four cases: absent from roster, no name on the row, the roster read failed, or an
   ambiguous name. **It does NOT filter by repo** — a name resolving outside this repo comes back
   clean; carry that gap yourself.

**Never loop over `entries` sending.** `SendMessage` is in `allowed-tools`; the gate is this
paragraph.

**A `PAUSED:away` peer is never offered**, reported as `never-send-reason`. Tripwire:
`A-PAUSED-ROSTER-IS-NOT-A-NUDGE-LIST`.

## The escalation screen — a claimed PM item is presumed yours until it survives

**When a session says it has something for the PM, it is wrong about 19 times in 20** — the PM's
own measured prior. Treat "this needs the PM" as a claim to test, never routing already done.

- **"Next: review."** The next step in a procedure the session owns. Push it — unless the plan is
  small enough that review is not a step at that size, in which case name the actual next step
  instead. Mirror anti-pattern: do not grant a permission the session already holds.
- **"Variable `x` or `xy`?"** Engineering, decided by whoever holds the file. Push it — do not
  answer it either.
- **"Do I execute?"** The one with a real question, answerable by you — below.

**Peers bring you a second opinion before, or instead of, asking the PM.** Answer engineering calls
yourself, or dispatch `coordinator:staff-eng` for a viability read. Route scope and direction to the
APM. Pass the PM only what survives this screen.

**This is a model disposition, not a peer failing.** Say so when you push, and push anyway.

### Push, do not nudge

**"Do you need anything?" is a failure, not a gentler success.** It hands the decision back to the
session that already froze on it. Same for "want me to...?", "let me know if...".

A push **names the act, names its owner, and closes**: *"That is yours. Do X."* No question mark,
no offer, no conditional. Give the reason in one clause so the correction generalises.

You are not pushing anyone past a gate their own skill names — a gate is a considered refusal with
a named reason; hesitation is the absence of one. Push the second, never the first.

### "Do I execute?" — yours to answer, with a viability read

The PM has delegated this call. **Do not read the plan into your own context to make it.** Dispatch
`coordinator:staff-eng` for a viability read.

**This does NOT route around the rubric.** Where a plan needs the formal `execution_authorized_by`
stamp, § Delegated approve-for-execution is the only path. This lighter call answers *"should I get
on with it"* for work that does not need that stamp.

## Delegated approve-for-execution procedure

The Group EM may take the PM's execute-plan turn on one condition: the plan is
reversibility-eligible and a rubric-scored judgment against its own prime exit criterion clears a
locked threshold (8 of 8, no dimension scoring 0).

1. **Standing check** (§ Standing check).
2. Run `<plugin-root>/bin/plan-reversibility-eligibility.py <plan-path> --json` (C9). `eligible:
   false` → escalate per the threshold page's shape, stop, do not dispatch. This CLI is the single
   source of truth.
3. Confirm the plan's falsifier baseline shows the prime exit criterion false **and that a blinded
   `coordinator:exit-criterion-falsifier` authored it**:
   - **Content.** Absent or already true → escalate, stop.
   - **Provenance.** A self-authored baseline satisfies "shows the criterion false" perfectly and
     voids the guarantee. Provenance lives in the plan BODY, a prior
     `state/review-trail/approvability/` record, or this session's own dispatch of the falsifier.
     **If none of the three establishes it, treat it exactly as a missing baseline and dispatch.**
   - **Instrument soundness.** A FALSE baseline proves the criterion false, never the instrument
     sound. Ask: **what would have to be true for this to print TRUE, and is any of it reachable in
     the world the fixture builds?** Unreachable → escalate with that reason named.
   Tripwires: `A-SELF-AUTHORED-FALSIFIER-SATISFIES-THE-CHECK-AND-VOIDS-IT`,
   `A-FALSE-BASELINE-PROVES-THE-CRITERION-FALSE-NOT-THE-INSTRUMENT-SOUND`,
   `UNATTRIBUTED-HARNESS-LINE-IS-NOT-PM`.
4. Dispatch the named Opus persona (the PM's chosen reviewer, at the PM's chosen effort) with the
   plan path and the rubric (`coordinator/schemas/plan-approvability-rubric.json`) and nothing else.
   Authorship blinding is a hard constraint.
5. Write the judgment record (`state/review-trail/approvability/<YYYY-MM-DD>-<plan-slug>.json`) and
   validate it with C9's `--validate-record` before treating it as final.
6. On `approve`: first refuse if `execution_authorized_by` is already present with any value — a
   plan the PM already authorized needs no delegated approval. Otherwise `review-exec-auth-stamp
   stamp <plan-path> --by "GROUP-EM:<session-id>" --append-note "<record-path>"`. On `escalate`,
   emit per the threshold page's shape — do not stamp.
7. **The stamp carries a standing offer: you produce criterion evidence the plan's author should
   not.** When a plan's terminal evidence is a live act rather than a test run, offer to perform it
   as the Group EM and let the author verify. Where the separation is not free, say so and let it
   go. Tripwire: `THE-AUTHOR-OF-A-CRITERION-IS-THE-WORST-PRODUCER-OF-ITS-EVIDENCE`.

## Fleet inbox grind

**On entry, when `coordinator.feature.cross_repo_memos` is on for the box, firing the saved
workflow is part of the request — not a decision.** The autofire hook prints the exact
invocation as `FLEET INBOX GRIND, FIRE NOW`:

    Workflow({scriptPath: "<plugin-root>/workflows/fleet-inbox-blitz.mjs", args: {repos: [...], gem: {...}}})

Fire it as your first act after arming the watch, unattended. `repos` is the fleet map
(`machine-local get repos.*`, de-duplicated, git repos carrying `state/cross-repo/inbox`) — every
repo, whether or not an EM is live in it. It assembles each inbox, triages and verifies in ~30-memo
Sonnet shards, then disposes and commits per repo, grinding each inbox to zero
(`workday-start.md` §1.45a owns the disposition rules). **Do not hand-author a variant.** If the
entry context carries no invocation, the feature is off or the hook failed open; check the flag,
and fire with `repos` read from the fleet map. Tripwire: `A-GROUP-EM-HAND-AUTHORING-THE-INBOX-WORKFLOW`.

## Cross-repo commit authority

**Committing in any fleet repo is presumed and inherent to this role** while this session holds
the standing (`group-em-nomination.py who --self`); it needs no per-session PM assent. Guardrails,
unchanged from the retired-grant rule: scoped pathspec commits only (never `git add -A`/`.`/`commit
-a`), no destructive git ops, never leave a sibling's tests red. Engine-subject work stays
the engine repo's: memo it, do not author it. The grant ends when the standing does. Record:
`docs/decisions/DR-group-em-role-carries-cross-repo-commit-authority.md`.

## Anti-scope

- **No auto-send.** `send_pass.py` selects and throttles; it holds no transport. Every send is an
  explicit per-send act with both gates declared. An unattended sender, a loop that messages each
  digest entry, or any `Stop`-registered trigger is out of scope.
- **Mandating that the watcher EXISTS is not mandating that it sends unattended.** Navi nudging on
  an observed registry transition is the "concrete observed signal" shape the ban preserves; a tick
  that messages everyone it can see is the shape it forbids. A session given a timing predicate
  re-derives `runtime-tripwire-stop-watcher.py` (681 fires / 26 days / ~99.4% wrong) one level down.
- **That ban is about AUTOMATION, never attentiveness.** A holder re-deriving the roster each turn
  and judging it is the opposite mechanism and is what the ban preserves.
- **The three dispatch grants at the top of this file are each scoped to their own named dispatch.**
  Raising the approvability judge and `group-em-assistant`, and firing `fleet-inbox-blitz`, under
  this session's own authority is the grant. What stays gated is that `/group-em` otherwise messages **peer sessions in their own
  windows** — an `ask-before-external-action` question no dispatch grant dissolves.
- `/autonomous` is a naming precedent only; its `/tmp` sentinel is not borrowed.
