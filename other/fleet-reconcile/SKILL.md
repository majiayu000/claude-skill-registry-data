---
name: fleet-reconcile
tier: D
primitive: null
category: orchestration
version: 0.4.1
description: |
  The hourly fleet coordinator. Phase 1 observes and classifies, report only;
  phase 2 adds the coordinator and its verbs under dry run.
  Each tick reads every Claude Code session (claude agents --json --all and the
  background job files), Paseo's agent records and schedules from disk, the
  ctx-core board, transcript times, and GitHub (open PRs and the effective
  branch rules of every repo in the scope). It classifies each session with the
  spec's class table, runs the count check, inventories scheduled work
  (Paseo schedules, com.broomva.* LaunchAgents, bookkeeping, Dream), and writes
  a markdown and JSON report plus one batch of owner asks, raised in the
  Paseo app as Maestro work at Needs you.
  In act mode (phase 2) a headless coordinator acts only through fleet act
  (mail, spawn, label, resume), which re-checks eligibility in code and, under
  dry run, logs what it would do; a send gate hooks its SendMessage. Runs
  hourly from launchd once the owner installs it. Coordination only; not a
  security boundary. USE WHEN installing or checking the fleet tick, reading a
  tick report, answering the fleet's asks (fleet asks, fleet ack), asking
  "which sessions are live / stalled / waiting on me", "which repos can get a
  driver", "what runs on a schedule and is it keeping time", or producing the
  phase-1 labelling sheet, rendering a driver profile, checking a worktree
  before a janitor removes it. NOT FOR live actions (phase 3, after the spec's
  §5.2 preconditions), merging PRs, or waiting on CI (use p9).
when_to_use: |
  Triggers on "fleet tick", "fleet reconcile", "fleet-reconcile", "fleet asks",
  "fleet ack", "class table", "which sessions are stalled", "count check",
  "labelling sheet", "install the tick", "is the fleet running", "scheduled
  work inventory", "fleet act", "send gate", "driver profile", "janitor-check",
  "fleet recover".
---

# fleet-reconcile: the hourly coordinator (phase 1 observe and classify; phase 2 dry run)

The 09-26 → 09-29 run's coordinator reported 6 live sessions when there were
30, lost state to compaction, and kept its ledgers by hand. This skill is the
first phase of its replacement, as the design of record specifies:
`docs/specs/2026-09-29-fleet-reconcile-design.html` in broomva/workspace (§5.3
observe, §5.4 classes, §9 row 1), with the formats of its 2026-09-30
build-readiness amendment (§5.7, broomva/workspace#842, merged as 007f05a98).
Ticket BRO-2674.

Phase 1 (`mode: report`, the installed default) is report-only and runs
deterministic code; no model reads or decides anything in a tick. It observes,
classifies and reports, and asks the owner in one batch per tick. The `would
do` column of a report says what phase 3 would do; nothing is done. Phase 2
(`mode: act`, `dry_run: 1`) adds one headless coordinator per tick, which acts
only through `fleet act`; under dry run every verb but ask logs what it would
do (see "Phase 2" below).

**Not a boundary.** Nothing here constrains any session. The tick's reads are
the owner's own reads (claude agents, gh on the owner's login, files under
$HOME). What bounds a merge is the repo's ruleset on GitHub (spec
§5.1), as far as it binds the owner's admin login (step 5 below); the
report's ruleset check says which repos have one.

## Install (the owner runs this)

```bash
cd ~/broomva/skills && git pull            # the checkout the job will run from
bash skills/orchestration/fleet-reconcile/scripts/install.sh --scope broomva --dry-run   # see it first
bash skills/orchestration/fleet-reconcile/scripts/install.sh --scope broomva
launchctl kickstart gui/$(id -u)/com.broomva.fleet-reconcile.broomva   # one tick now
# sri, report-only like everything in phase 1:
bash skills/orchestration/fleet-reconcile/scripts/install.sh --scope sri
# remove:
bash skills/orchestration/fleet-reconcile/scripts/install.sh --scope broomva --uninstall
```

The job runs a **pinned copy**, not the checkout: `install.sh` copies
fleet-reconcile's and ctx-core's scripts and templates to
`~/.local/share/fleet-reconcile/releases/<commit>/` and points the plist there,
so a branch switch or an edit in `~/broomva/skills` doesn't change what launchd
runs; installing again does. A checkout with uncommitted changes in either
skill is refused unless `--force`. It seeds `~/.config/ctx/fleet.json` from
`templates/fleet.json.example` only when absent (mode 0600, report mode,
`dry_run: 1`) and runs `config-check` (in `--dry-run` too), renders
`templates/launchd.plist.template` into
`~/Library/LaunchAgents/com.broomva.fleet-reconcile.<scope>.plist`
(StartInterval 3600, ProcessType Standard, logs in `~/Library/Logs/`), then
`launchctl bootout`, waits for the job to go, and `bootstrap`s (retried three
times), so a rerun reloads. `--uninstall` unloads and moves the plist to the
Trash; the config, the releases and the state dir stay.

## A tick

`scripts/tick.sh`, per scope (FLEET_SCOPE):

1. The recursion guard (`FLEET_CHILD`), then the kill switch: the tick fires
   only when `fleet config-get <scope> dispatch_enabled` prints exactly `1`.
   Any other value is the owner's off (exit 0). A config that can't be read
   is off too, and is a failure (below). Then `config-check`.
2. `dry_run` falls toward dry: live only when the config says exactly `0` and
   `live_accepted` holds the owner's note (step 5); any `DRY_RUN` value but `0`
   in the environment forces dry. `dry_run: 0` without that note fails
   `config-check` in any mode, so no tick runs. Phase 1 acts on nothing
   either way; the ledger records the mode.
3. A mkdir lock per scope. A stale lock (both pids gone, 2 minutes old) is
   reclaimed under a second mkdir mutex that re-reads its holder, so two
   ticks can't both reclaim it.
4. The tick number from `fleet next-tick`: one past both the counter file and
   the ledger's last `tick_fire`, so a lost counter can't reuse a number.
5. GitHub is read and written on the owner's gh login (the keyring). Owner
   decision 2026-10-01: no fleet token or GitHub App, and spec §5.2's
   non-admin credential precondition is waived. The accepted residual is
   that the fleet acts with the owner's admin rights. A repo's ruleset binds
   that login only as far as the ruleset lets an admin through: an admin can
   merge past a ruleset that lists admins as bypass actors, and can edit a
   ruleset over REST. What holds a driver to the rules is its brief (never
   touch rulesets or workflows; merge only once every required check passes),
   and phase 3's checks. tick.sh drops a `GH_TOKEN` or `GITHUB_TOKEN` it
   inherits before it runs anything, and so does `Sources` for every gh call
   and child, so every step reads GitHub as that login. `gh_token_file` is accepted and not read.
   With no token to gate live mode, `config-check` refuses `dry_run: 0`
   unless `live_accepted` holds the owner's note that the Phase 3 list below
   is done and names both gate tickets, BRO-2755 and BRO-2756; tick.sh then
   alerts and runs no tick, and every verb stays dry without it. The note
   records a deliberate second edit; requiring the ticket ids keeps a bare
   "no" or "TODO" from passing (it still doesn't check the work itself).
6. `fleet recover` (closes intents a dead tick left open), `fleet observe`,
   `fleet report`, in act mode `fleet coordinator` (only after the three
   before it succeeded), and `fleet
   core-compare` (the core's comparison, once a day from `compare_hour`),
   each in its own process group under a TERM-then-KILL watchdog bounded by
   `tick_timeout_min` (15), so a timeout also ends its `claude` and `gh`
   children.
7. `tick_fire` and `runner_exit` records in the ledger (through
   `fleet ledger-append`), the lock released, then `fleet act ask --show` (a
   Maestro item at Needs you in the Paseo app), and one line on stdout for launchd's log.

**A failed tick is loud.** An unreadable config, a failed `config-check`, or
observe or report failing, or a lock held for over 2 h, raises a Maestro item directly
from bash (so it works when Python is what broke), at most once per 6 h per
kind, and exits 1, so launchd's last exit shows it.

By hand: `FLEET_SCOPE=broomva bash scripts/tick.sh`.

## What a tick reads, and what it does with a failure

| Surface | Read from | On failure |
|---|---|---|
| Sessions | `claude agents --json --all` | reported; nothing is classified. At `listing_cap` (200) rows or more the listing counts as complete only when every job file on disk appears in it (the listing has no limit parameter but lists every background job ever run); otherwise it **fails closed** the same way |
| Background detail | `~/.claude/jobs/<id>/state.json` | the directory unread: every background session that would be 9, 9a or 10 reads unknown. One file that doesn't parse: only its session does |
| Activity | the latest assistant entry or tool result in each session's transcript and its newest subagent transcripts (spec §5.3); not the mtime, which Claude Code moves with untimestamped records long after a turn (36 of 77 captured transcripts by over 10 min) | reported |
| Paseo | `~/.paseo/agents/*/*.json`, `~/.paseo/schedules/*.json` (read-only) | reported; the count check says it could not run |
| The board | ctx-core's `events.jsonl`, rebuilt in memory (no cache write) | reported and asked per scope; that scope's sessions that would be 9, 9a or 10 read unknown, since 2, 4, 7 and 8 couldn't be checked |
| GitHub | per repo: slug from `origin`, `repos/<r>` default branch, `rules/branches/<b>`, `gh pr list` | **that repo** is reported as not observed. A slug that doesn't resolve, a gh error or a PR list at `pr_list_cap` never reads as zero PRs |

The parsers are pinned to Claude Code 2.1.280 and tested against copies
captured on it (`tests/fixtures/cc-2.1.280/`). Another running version, a new
listing field or an unfamiliar enum value is reported as drift and asked
about. Never extracted (each file is loaded whole and these fields are
dropped before anything is kept): a Paseo record's `persistence.metadata`
(where the MCP bearer lives), a job file's `providerEnv`, `output` and inline
`--settings`, a schedule's prompt and run output, the bookkeeping log's
`source_files`.
Other sessions' words (names, job details, PR titles) are flattened, clipped
and passed through ctx-core's guard; a credential-shaped string or a `crm/`
path is withheld.

## The classes (spec §5.4, first match wins)

| # | class | evidence |
|---|---|---|
| 1 | out of scope | the core's scope rule places the cwd elsewhere, the cwd is in no repo, or it can't be placed (cwd gone, no board row) |
| 2 | dead: limit | a board `session.died` with `rate_limit`, or a background job blocked on Claude Code's limit text; the reset is read from the job or the transcript tail, else assumed 5 h after the death |
| 3 | waiting at a prompt | listing `status: waiting` with a `waitingFor`, unless it is a background question to its user |
| 4 | error | listing `state: failed`, or a board death with another error (transient: 5xx or network only) |
| 5 | running | busy, activity within 2 h |
| 6 | hung | busy, a transcript found, no activity for over 2 h |
| 7 | blocked on the owner | a current `ARC-STATUS: BLOCKED`, or a background job blocked on a question (its needs, a suggested reply, or a detail that asks) |
| 8 | closed | a current `MERGED`, `CLOSED` or `DONE`, a known branch, and no open PR on it; an unknown branch is unknown |
| 9 / 9a | stalled / idle, recent | ours (a ledger spawn, or adopted by session id or through its Paseo agent), idle, no activity for ≥ 1 h / activity within 1 h; 9's action is a mail with a live process, else a resume |
| 10 | unmanaged | in scope, not ours |
| — | unknown | nothing matched (a missing transcript), or a terminal status on a repo whose PRs weren't read |

Choices the spec leaves open, pending the spec and listed in
`scripts/fleetlib/classify.py`: class 2 also reads the job file and the
transcript tail for the reset (a dated reset like "Oct 3, 10am" included; an
unreadable one is assumed 5 h after the death); a board death or ARC-STATUS
counts only while nothing happened after it (the core measured sessions that
died at the limit and kept working); "idle" includes a background session with
no process and no status whose state is done or stopped; the spawn pause counts
a limit death in any scope, since every scope here runs on one account.

The overlap pass runs on fixtures only until the core's phase 2 publishes
claims. The count check reports every Paseo record that isn't archived and has
no live process, and every in-scope session with neither a Paseo record nor a
fleet name.

## The owner channel (spec §5.7, the ask channel)

An ask is per occurrence of a condition. Candidates: a session waiting at a
prompt or blocked on the owner, a repo without a pull_request rule or with
unpinned checks, a repo not observed, a surface not read, drift, records
with no process. A key is asked once, stays open until the owner answers it or
a tick finds it no longer true (a resolution record), and an answer holds for
as long as the condition does; a condition that ends and comes back is a new
ask. A tick resolves a key only when it read the surfaces that raise it: the
listing for a prompt (and not while the session reads as unknown), the scope's
board too for a blocked session (and the job files for a background one), the
version, job files and listing for drift, the Paseo records for records with
no process, the repo for its rules (a repo that leaves the scope resolves,
unless some repo's slug couldn't be read). A key left open because its surface
wasn't read is still listed and counted, as not re-checked. Keys carry no counts or error text, so they don't change tick to
tick. A prompt's key is the session and what it waits for: the first tick that
sees it not waiting resolves it, so the next wait is a new ask (two waits
between ticks read as one). The core comparison asks when it can't run, keyed
on the owner's action still owed (`compare:move` for the prototype's
`compare.jsonl` or a first line that can't be read, `compare:register` for no
registration time), and when it couldn't run three attempts in a row; a failed
attempt is retried at the next tick. A tick writes a batch
(`<state_dir>/asks/<tick>.md` and an ask intent in the ledger) only when it has
a new key.

**The asks reach the owner in the Paseo app** (owner decision 2026-10-01:
"If it goes to the computer and I'm not there it won't work"; this replaces
the dialog that workspace#842 chose). Inside the tick's lock and budget, `fleet
act ask --show` turns each batch with an open ask into one Maestro work item
(`scripts/fleetlib/paseo_ask.py`) once an ask in it has been open for
`ask_raise_after_min` (50 by default: past the next hourly tick, so an ask
that a later tick found no longer true isn't raised; 0 raises at once).
- `maestro new`, then `maestro dispatch`, runs one turn of a Paseo agent in
  the fleet's own scratch repo (`ask_repo`, by default
  `~/.local/state/fleet-reconcile/maestro-asks`, not a scope repo). Two calls,
  so the fleet holds the item's id whatever the dispatch says.
- The asks go in the item's brief as fenced data. The run changes nothing and
  ends with the fleet's own one-line summary under `## Ask`, so the item waits
  at **Needs you** and the agent's Paseo record is marked as needing
  attention.

Measured end to end on 2026-10-01, at the daemon state the app renders: the
item reached `review` and the agent read `requiresAttention: true`. A phone
push was not measured.

Raising is idempotent. The title ends with a marker carrying the scope and
the batch id (`[fleet-reconcile <scope> batch <id>]`), so an open item a `new`
with no clear answer made is found with `ls` and adopted; a done or canceled
one, or one older than the batch, is not. An item made whose run couldn't
start is recorded all the same, queued, and dispatched at a later tick; the
failed start fails the ask step. Where an item stands is one rule,
`ledger.maestro_phase`, which every ask path reads: queued (`proposed`,
`reviewing`, `triggered`: waiting for a dispatch), owner (`running`,
`review`, `blocked`: in the Paseo app), final (`done`, `canceled`), or gone
(Maestro no longer has it). A batch counts as seen only once its item reached
the owner, whoever started it, and no longer once it is gone; each tick
records the item's state when it changes. A queued item is dispatched at a
later tick while an ask in its batch is still open. A dispatch that leaves it
queued is logged, not a failed tick: at the run cap (`At capacity:`), or
while Maestro's loop is starting it (`This work is already being
dispatched.`). Any other refusal is checked against the item: one the loop or
the owner moved out of the queue first (a lost race) is recorded where it
went, and one still queued fails the ask step. An item Maestro no longer has
(`No work item with id`) is recorded gone, which frees its batch to be raised
again while an ask in it is open.

Maestro's refusals carry no code (the socket answers `{ok: false, error}`;
the CLI prints `maestro: <message>` and exits 1 for each; BRO-2753 asks for
one). Those three are told apart by the words their message starts with,
never by a match anywhere in it, and only on exit 1. A reworded one reads as
a refusal, which fails the ask step: loud, not silent.

Each tick reads the owner's decisions back from every item that isn't final
and either has an ask still open or was raised (its latest raise) in the last
14 days, following Maestro's wire (server/events.ts
`toWireEvents`). There every settled decision reads as made, so only one that
**took effect** counts: its words followed by `Took effect`, or a decision
applied at once. One undone (`Undone`) or dropped (`… did not take effect`) is
not the owner's answer. The item's `verdict` field is display text and isn't
read. Each new decision is an `ack` by `owner:maestro`:
- Approve acknowledges;
- Send back with a note answers (every note is kept, up to 1000 characters
  each, flattened to one line, even after a later approve; a note sent after
  the asks stopped being true is still recorded);
- Cancel dismisses.

Only Send back's note is read. A reply typed in the run's chat is not a
decision, and the run answers one by saying so.

Limits, by design:
- A session can't cancel an item, so one whose batch resolved first, or was
  answered from a terminal, stays until the owner closes it.
- A Stuck run (its turn failed) shows in Maestro's Stuck group, is logged, and
  isn't raised again.
- Each item costs one turn of the provider Maestro is configured with, and a
  send-back costs a second.

tick.sh's own alerts (a bad config, a failed step, a held lock) are Maestro
items too, at most once per 6 h per kind, stamped only once the item is past
Maestro's queue. `fleet alert` adopts an open item of the same kind rather
than raising a second, so that item stands for the later alerts of its kind
(`tick.log` has each one's words). When Python or the config is what broke, a
bash fallback raises one (`maestro new --dispatch`, in its own process group
under a TERM-then-KILL watchdog: TERM at 120 s, KILL 30 s later). It can't
adopt or classify, so any answer from Maestro counts (made; refused, a run
that couldn't start included; no clear answer), which keeps it to one per 6 h
whatever Maestro's words. An exit 1 is Maestro's answer only with the CLI's
`maestro: ` line; anything that never reached Maestro (not listening, a CLI
that didn't run, one the watchdog stopped) is tried again at the next tick.
`fleet alert` itself is bounded by its maestro calls' own timeouts (90 s
each). When Maestro itself is down, they reach only `tick.log`:
the channel's blind spot. There is no dialog, banner, ntfy or p9 notify. The
owner can also answer from a terminal:

```bash
F=~/.local/share/fleet-reconcile/releases/<commit>/orchestration/fleet-reconcile/scripts/fleet
$F asks --scope broomva            # the open asks, one line each, oldest first
$F ack 12 --scope broomva          # answer tick 12's batch
$F ack 12 --ask a3 --scope broomva # one ask of tick 12
$F ack --all --scope broomva       # every batch with an open ask
```

`fleet ack` refuses when `FLEET_CHILD` or `CLAUDECODE` is set (a floor: the
owner answers from a terminal). Every report leads with the number of
unanswered and unseen batches and of open asks. `ask` runs in every mode and
under dry run (§5.7): it reaches only the owner.

## Files

```
~/.config/ctx/fleet.json                         the config (spec §5.7), owner-edited, 0600
~/.local/state/fleet-reconcile/<scope>/
  ledger.jsonl, ledger.lock                      the write-ahead ledger (flock, fsync)
  ticks/<NNNNN>/snapshot.json, report.json, report.md   (snapshots pruned after 7 days)
  asks/<NNNNN>.md                                one ask batch per tick
  labelling/<name>.md, .csv                      the owner's labelling sheet
  ticks/<NNNNN>/coordinator.jsonl, .err          the coordinator's stream (act mode)
  coordinator-settings.json                      its send-gate hooks, 0600
  profiles/<fleet key>.json                      a live driver's 0600 profile (no token; a ghcfg/<key>/
                                                 dir only from a spawn before 0.4.0)
  backups/<path hash>/<UTC>/                     the janitor's backups, deleted after 14 days
  tick.log, tick-counter, .tick.lock, .alert-<kind>
~/.local/share/fleet-reconcile/releases/<commit>/  the pinned copy the job runs
~/Library/Logs/com.broomva.fleet-reconcile.<scope>.log
```

Config keys beyond §5.7's, pending the spec: `listing_cap`, `pr_list_cap`,
`actions_app_id` (15368, GitHub Actions), `launchd_prefix`,
`launchd_logs` (a label's real log, when its stdout is silent),
`bookkeeping_run_log`, `dream_run_log`, `tick_timeout_min`, `compare_hour`,
`coordinator_model` (phase 2; null is Claude Code's default), `coordinator_budget_usd` (2),
`maestro_cli`, `maestro_bun`, `ask_repo`, `ask_raise_after_min` (50; the owner channel),
`live_accepted` (0.4.0: the owner's note that live mode's preconditions are done; `dry_run: 0` needs it, and 0.4.1 requires it to name BRO-2755 and BRO-2756). §5.7's `paseo_tools` defaults to
the pinned 0.9.2 classification (19 read, 42 write) and `driver` to probe 6's GitHub
allowlist with no registries.
§5.7's `b_step_timeout_min` and an adoption's `paseo_agent_id` are accepted.

## Scheduled work (report-only; the seam for the Dream and heartbeat section)

`scripts/fleetlib/scheduled.py` lists, per scope: Paseo schedules (placed by
cwd), LaunchAgents with the scope's `launchd_prefix` (cadence, loaded, runs,
last exit, last run read from a log's mtime, staleness), the last bookkeeping
run, and the last Dream (P13) run when `dream_run_log` names one (there is no
Dream run log on this machine yet). Every item has the same keys, so the later
spec section adds a source without changing the report. It starts, stops and
edits nothing, and raises no asks (its readings are in the report's table).

## The phase-1 exit (spec §9)

The tests pass; then three real ticks, and the owner labels a stratified
sample (at least 3 sessions per class that occurs):

```bash
$F label-sheet --scope broomva --ticks 1,2,3   # writes labelling/<name>.md and .csv
```

≥90% agreement overall and no class below 2 of 3. Spec §9 also asks that each
of those ticks' dialogs be clicked Seen. With the owner channel on Paseo
(0.3.0), that reads as each batch those ticks raised answered in Maestro; the
spec's wording is to be amended.

## Commands

```
fleet config-get <scope> <key> | config-check [<scope>]
fleet observe --tick N [--fixtures DIR]
fleet report --tick N [--dry-run 0|1]
fleet act ask --show --tick N
fleet act mail --session SID --template stalled|hung|overlap [--var k=v ...]
fleet act spawn --repo OWNER/NAME --pr N | label --repo R --pr N --label L [--remove] | resume --session SID
fleet recover | send-gate pre|post (stdin: the hook JSON) | coordinator --tick N
fleet config-check <scope> --init <stream-json file>
fleet driver-profile --key K [--write]       (it holds no token: the owner's gh login)
fleet janitor-check PATH --owner ID | janitor-run PATH --owner ID [--remove]
fleet asks [--all] | ack <tick> [--ask ID ...] | ack --all
fleet next-tick | ledger-append fire|exit --tick N
fleet core-compare [--force]
fleet label-sheet --ticks A,B,C [--per-class 3] [--seed 0]
```

All take `--scope` or `FLEET_SCOPE`. `scripts/fleet` execs `python3 -I`, so
the caller's cwd and user site stay off `sys.path`; it imports ctx-core from
`../ctx-core/scripts` in the same checkout.

## Tests

```bash
cd skills/orchestration/fleet-reconcile
python3 -m pytest tests/ -q
python3 tests/mutation_check.py      # every rule deleted, every overlapping pair swapped, every listed protection removed
python3 tests/capture_fixtures.py    # recapture on a new Claude Code version (anonymized; public repo)
```

| File | Pins |
|---|---|
| `test_parsers.py` | Every parser against the 2.1.280 capture; missing fields fail the surface; drift is reported; the bearer, env and prompts are never extracted; the slug rule; the ruleset check (skills flagged until its pull_request rule lands, unpinned checks flagged) |
| `test_classify.py` | A positive case per class; the spec's five ordering tests; 41 rule pairs that can both match, the earlier winning; a grid proving the other 14 pairs can't; the arc and death currency rules; the spawn pause; the count check; the overlap pass |
| `test_observe.py` | The pipeline over the capture in a scratch HOME; a 200-row listing fails closed unless the job files show it complete; one unparsed job file degrades only its session; an unresolvable slug, a gh error and a PR list at the cap fail only their repo; the bearer never reaches a snapshot or report; activity found past a last line larger than the first tail window (ctx-core's reader); an inherited GH_TOKEN or GITHUB_TOKEN dropped, so gh reads the owner's login |
| `test_report.py` | Every section; withheld crm/ paths and tokens; per-occurrence asks (once, then still open; an answer holds while true; a recurrence is new; a different question is new), answers per batch, stable count keys, failed-surface asks, a resolution only from the surfaces that raise the key (for a session that still classifies, too), open asks not re-checked still listed, a wait's key holding while its subagents write, a failing comparison asked after three runs with its error guarded, the ack wording, the ruleset wording, scheduled work as inventory only, a duplicate fleet name asked while it lasts (and not resolved without a listing); the labelling sheet (distinct sessions only) |
| `test_ledger.py` | Validation, distinct owner ids within one millisecond, corrupt-line counting, 4 processes × 50 appends lose nothing, the ask and spawn folds |
| `test_paseo_ask.py` | A batch raised as Maestro work in the fleet's own repo, then dispatched; only decisions that took effect read back, on Maestro's own wire sequences (undone, dropped, a torn cancel, the undo window, the display verdict, an agent's words); the note through the guard; Maestro's exit codes as errors; refusals told apart by the words they start with, on exit 1 only; `find` adopting only an open item of this scope's batch made after it; an alert adopting its kind's open item; the sync recording each new decision once, a note after the asks resolved, nothing past 14 days from the latest raise once its asks closed (an open one still read) or a final answer; a refusal at the cap, the loop starting it, or a lost race as no failure; a gone item freeing its batch and no longer seen; a refused dispatch whose item can't be read again raising its own error; a Stuck item and a persistent read error each logged (and the error failing the step) at most once per 6 h, not every tick |
| `test_tick.py` | tick.sh end to end with stub claude/gh/maestro: kill switch, a bad config alerting once and exiting 1, a failed step alerting, dry falls toward dry, live and stale locks and the reclaim mutex, the recursion guard, the watchdog killing the step's children, no token reaching any step (one configured or inherited included), recover and a live coordinator on the owner's login, tick numbers past a lost counter, the lock released before a tick-number alert, a lock held over 2 h alerting, a batch raised once at Needs you and the owner's verdict read back as the answer, a cancel dismissing, a batch raised only once its asks lasted, a batch queued at the cap neither failing the tick nor seen until dispatched, an open alert of its kind adopted, an alert queued at the cap not delivered, the bash fallback raising at most one per 6 h whatever Maestro answers, tried again when nothing reached Maestro (not listening, a CLI that didn't run), and stopped with its children when it hangs (or its leader dies), reaching Maestro with its state dir broken, live mode refused until `live_accepted` names BRO-2755 and BRO-2756 and every verb dry (at the CLI too: is-dry, act label/spawn, the coordinator child's DRY_RUN) without it, an unusable state dir alerting its own kind not a misread config-check, the bash fallback classifying a refusal in memory when mktemp fails, a raised batch whose run can't start recorded queued and dispatched later, an ask Maestro doesn't take not recorded and raised at the next tick, alerts as Maestro work, a failed compare not using up the day and the prototype's compare line refused and asked about, ack refused inside a session, refused verbs, the labelling sheet |
| `test_act.py` | Every verb refused in report mode and on a corrupt ledger or an open ask on its target; spawn's floor (held, draft, Dependabot, a fork, a head or base branch that isn't a plain ref (incl. a 121-char head over the brief width), a withheld repo slug, a hostile default branch, owner-merge, unread files, unruled repo, closed PR, taken name, a branch checked out, the caps, unknown claims, the spawn pause) against text that says otherwise; a 120-char plain head shown in full; `render_template` raising on a non-string; dry spawn, label and resume closed with the argv or call; mail only to fleet or adopted sessions, the 6 h rule (failed doesn't count, live and dry apart), not_live, ambiguous_name, a Paseo relaunch followed, template values guarded, no template names a merge or removal; a PR file list GitHub capped refused; the rendered driver brief's PR number, branches, base fetch and LFS-check order |
| `test_sendgate.py` | Each pre check refusing with its own name; dry run closing the intent and still blocking (incl. when the config refuses live); a live send passing and post closing it with the msg_id; harness_refused and unledgered_send; the CLI failing closed |
| `test_recover.py` | Mail found in either delivery shape only after the intent (an enqueue only), else lost or unknown; a malformed entry counting as nothing; spawn's one, none or duplicate rows; resume by process start; label by the PR's labels |
| `test_coordinator.py` | Every Paseo tool the captured 0.9.2 list holds is classified (fails when Paseo adds one); the argv's disallowed list and `--`; the settings' hooks; the posture check; a coordinator whose tool list fails it, or whose stream ends before its init event (its own exit code kept, a still-running one stopped), terminated; the child environment; the driver profile's shape and 0600 file, with no token even when a token file is configured, the keychain and gh config left readable, and the credential files the gh route doesn't need denied |
| `test_janitor.py` | Each check passing, failing, or not running (a process listing showing only the janitor, an ignored directory it can't walk); the backup; pruning; a profile it can't delete failing the run; report-only without --remove; no removal of a scope repo's worktree; the scratch run's order |
| `test_install.py` | The pinned copy (runnable without the checkout), plist rendering, config seeded once at 0600, bootout-wait-bootstrap on every run, a retried bootstrap, uninstall to the Trash, dry run, a broken config, uncommitted changes refused without --force |

## Phase 2: acting under dry run (spec §5.3, §5.5, §5.7, §9 row 2)

Switch a scope with `"mode": "act"` and `"dry_run": 1` in `~/.config/ctx/fleet.json`
(sri stays at report in every phase, §5.6). Each tick then runs one coordinator
after the report: `claude -p --name fleet-coordinator-<scope> --settings
<state>/coordinator-settings.json --output-format stream-json --verbose
--permission-mode bypassPermissions --strict-mcp-config --max-budget-usd
<coordinator_budget_usd, 2> --tools Bash Read SendMessage --disallowedTools Agent Edit Write NotebookEdit
mcp__paseo__<each pinned write tool> -- "<runner prompt>"`, with the Claude and
Paseo variables unset and `FLEET_CHILD=1`, `FLEET_TICK`, `DRY_RUN` set; no MCP
server loads (pending the spec, which names only the Paseo writes). Its init
event's tool list is checked as it starts: any tool outside the allowlist
(measured: with `--tools` the init event lists exactly those three), a Paseo
tool in neither pinned list, no list at all, an event before the init event,
or no init event within 60 s or before its stream ends (a clean exit with its
tool list never checked) stops it (exit 4; the tick fails loudly). It stays in the step's process
group, so tick.sh's TERM-then-KILL reaches it. The tool
list is a posture: the coordinator runs unsandboxed and its Bash reaches git,
gh and the Paseo CLI.

**fleet act** (`scripts/fleetlib/act.py`) is its named route. Each verb refuses
in report mode, on a corrupt ledger (mail, spawn) and on an unanswered ask about
its target, then re-observes and re-checks in code:

- `spawn --repo R --pr N` (drivers only; janitor runs are report-only): §5.5's
  rules from a fresh observation (ruleset, open, not draft or Dependabot, not a
  fork (spec §5.2 W3: a fork's author picks the head name and PR text a brief
  would carry), no `hold` label, head and base branches that are plain ref
  names the text guard renders unchanged and no longer than 120 characters (the
  width a brief shows), and a repo slug the guard renders unchanged (the head
  judged on its raw name; the brief carries the slug and base into a command).
  The text guard withholds not only `+`, `@` and non-ASCII but credential-shaped
  tokens (an `SK-123` key, a `ghp_`/`sk-`/`xox`/`AKIA` substring), a `crm/` path
  segment, and a run of 32 or more letters and digits; a PR whose head, base or
  slug it would change gets no driver. There must be no
  `research/entities/**` file among all its files (a list
  shorter than the PR's `changed_files`, GitHub's 3000-file cap, refuses
  it), no live
  session on its branch, no unknown claim, the name unused live or stopped in
  the raw listing, ≤ 8 live fleet sessions, ≤ 12 active in 30 min, no
  usage-limit pause), refusing when the listing, job files, transcripts or any
  board weren't read, or while a spawn of the same key is unconfirmed. The
  argv is §5.3's: `claude --bg -w <key> --name <key> --strict-mcp-config
  --dangerously-skip-permissions --settings <0600 profile> "<brief>"`. A live
  spawn whose session the listing doesn't show yet is done with its job id,
  which keys it until then.
- `mail --session SID --template ...`: only a fleet spawn in the ledger or an
  adopted session; resolved to the live row by session id, else through its
  Paseo agent's current session; refused when no row has a process
  (`not_live`) or another live row carries its name (`ambiguous_name`); one per
  recipient (the Paseo agent id, else the session id) per `mail_interval_h`,
  live and dry counted apart, a failed mail not counted. It prints the exact
  `to` and `message` for SendMessage. The templates never name a merge or a
  removal, and take no free text: `other` must be a session name and `paths`
  up to five plain paths; `hours` comes from the config.
- `resume --session SID`: only a fleet or adopted background session with no
  process, never twice while one is unconfirmed; `claude --bg --resume <id>`
  with no other flag (a flag starts a copy; so does a session that still holds
  its process, which the drill measured).
- `label --repo R --pr N --label L [--remove]`: an open PR of a scope repo;
  never the `hold` label (the owner's).

Each writes its intent (fsynced) before acting; under dry run spawn, label and
resume are closed at once with `done` and `would: true` plus the argv or API
call. **The send gate** (`sendgate.py`) is mail's other half: the coordinator's
PreToolUse hook on SendMessage refuses unless an unclosed mail intent from this
tick matches `to` exactly (no `[ref]`) and `message`, the recipient is still
fleet or adopted, the 6 h rule holds, and a fresh listing shows exactly one
live row with that name and the intent's session id; under dry run a send that
passes is closed `done (would)` and still blocked. The gate fails closed: an
error of its own (a config it can't read included) exits 2, and it bounds its
ledger lock (3 s) and listing (5 s) inside the hook's 10 s, since a hook the
harness kills lets the tool run. PostToolUse and
PostToolUseFailure close a live send, and a send with no intent is recorded as
`unledgered_send`. **fleet recover** closes every intent a dead tick left open
from what happened (§5.7's rules); a mail counts as delivered only from a user
entry or a queue-operation `enqueue`, and a malformed transcript entry counts
as nothing.

**The driver profile** (`profile.py`, `fleet driver-profile`): probe 6's shape,
written 0600 per spawn under `profiles/`, with no token (since 0.4.0). The
denyRead on gh's config and the login keychain is gone, so a driver reads the
owner's login inside the sandbox with `gh auth token`, which needs no network;
the ~/.paseo, ~/.claude and settings-file denies stay. gh's own network calls
fail TLS inside the sandbox (OSStatus -26276; a CA file doesn't help), and
`sandbox.excludedCommands` didn't take gh out of it while
`allowUnsandboxedCommands` is false, so drivers push with git (hooks
bypassed: the global pre-push hook's git-lfs fails the same way, so a driver
can't push LFS objects) and call the REST API with curl. Measured in the
credential drill (`~/.config/broomva/fleet/credential-drill-20261001/`):
push, a REST PR, update-branch and a squash merge on a private scratch repo,
with ~/.paseo reads and $HOME writes still refused. Since BRO-2755 it also
denies the credential files the gh route doesn't need (`~/.aws`, `~/.ssh`,
`~/.config/gcloud`, `~/.kube`, `~/.config/op`, `~/.gnupg`, `~/.netrc`,
`~/.docker/config.json`); `~/.config/gh` and git config stay readable (the gh
route needs them). **Open residual (measured, BRO-2755,
`keychain-table-20261002-bro2755.md`):** securityd is reachable from inside the
driver sandbox, so a driver can read ANY login-keychain item via
`/usr/bin/security` without a prompt — not just gh's (the `Claude Code` and
`Orca Claude Code Managed Credentials`, `Houston-Linear-credentials`, cursor
tokens, an `api.anthropic.com` internet-password, and the rest). A file-based
`denyRead` on the keychain is whole-keychain and would break gh's own read, so
the keychain can't be partially denied: the exposure is a W1 decision for the
owner (accept arm D, or arm A — a per-spawn env token with the keychain file
re-denied, which a file deny *does* reach). Spawns stay dry until the owner
answers W1 and the rest of Phase 3 lands.

**The janitor** (`janitor.py`): `fleet janitor-check PATH --owner ID` exits 0
only when every check passes, 1 on a failure and 2 when a check couldn't run;
`fleet janitor-run` refuses unless PATH is the owner's own worktree, prunes backups
older than 14 days, checks, stops the owner, re-checks, backs up, re-reads the
listing and runs `claude rm`, and removes nothing but scratch worktrees (of no
scope repo) until the owner accepts the janitor drill. An ignored directory
it can't walk makes the backup check `not run` (it could hold a secret), and
a removed driver's profile or gh dir it can't delete fails the run (exit 1,
`left` in its result). A scope repo's owner
needs a terminal status on the board; the listing's `done` counts only for a
scratch worktree.

Not built in phase 2: `fleet adopt` and `fleet audit` (the owner's side), the
recovery drill, spawning through bstack's peer.py (it takes no settings path;
the argv is built here), research spawns.

**Drills** (scratch sessions and repos, 2026-10-01; evidence in
`~/.config/broomva/fleet/phase2-drills-20261001/`):

- PASS: the kill switch; the tool-list posture; SendMessage refusals (5 of 5);
  the injected-text eligibility floor; the janitor.
- Driver profile:
  - the sandbox half passed on a fake token, fresh and after a resume;
  - the credential half and the update-branch probe passed on the owner's
    login in the 2026-10-01 credential drill (above), after the owner waived
    the fleet token.
- NOT RUN: the recovery drill.

**The ask channel is on Paseo** (owner decision 2026-10-01; see "The owner
channel" above): Maestro work at Needs you, never a macOS dialog.

## Phase 3

Needs the two remaining preconditions of spec §5.2 (the owner waived the
first, the fleet token): the Merge Gate judged by the base's copy, and the
Hold and owner-merge checks. It also needs the unrun recovery drill, the
owner's review of the dry run's proposals, BRO-2755 (what a driver can read
from the login keychain) and BRO-2756 (phase-3 hardening, including that fork
PRs get no driver — spec §5.2 W3). Then `dry_run: 0` with `live_accepted` set
to the owner's note that these are done, naming both BRO-2755 and BRO-2756:
`config-check` refuses `dry_run: 0` without a note that names them (a bare
"no" or "TODO" does not pass), so tick.sh alerts and runs no tick, and every
verb stays dry.
