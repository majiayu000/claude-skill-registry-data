---
name: team-teardown
description: Use when about to spawn teammates and idle ones exist — the spawn gate will say so — or when a previous session left teammates running, or when asked to clean up agents or panes.
---

# team-teardown

Teardown happens at the next spawn, not when a lane finishes. A teammate
whose lane is done stays alive and idle so the next batch can reuse it; just
before spawning, the lead reconciles — reuses the idle teammates that fit and
reaps the rest. The three-stage teardown further down (request → verify →
reap) is for teammates a previous session left running, or an explicit
request to clean up. Graceful shutdown alone is not enough there — some
teammates approve a shutdown request and then go back to idle instead of
exiting. Verification is mandatory.

Never kill a pane yourself, and never before its process. **Claude Code sets
`remain-on-exit failed` on every teammate pane, so a pane does NOT close on
its own when its process exits** (corrected 2026-09-21 — an earlier revision
of this doc claimed it did). Killing the pane first leaves the `claude`
process alive with no pane at all — invisible to `tmux ls` and strictly
worse than the leak you were fixing; killing the pane at all yourself,
even after the process, races the reaper's own pane cleanup and its
teardown-log record. `reap-teammates.sh --yes` (Stage 3, below) removes the
process first and then its dead pane itself, in that order, logging the
removal to `~/.claude/logs/team-teardown.log` before it kills the pane —
just run it and let it do both.

## Reconcile before spawning

Run this before any batch of teammate spawns while this session has idle
teammates. `spawn-gate.sh` (a `PreToolUse` hook on `Agent`) enforces it:
while this session has idle teammates and no reconcile marker younger than
120 seconds (`TEAM_RECONCILE_WINDOW`), it refuses a named teammate spawn,
lists the idle teammates, and marks those reusable for that spawn (same
`cwd` and agent type).

1. **See who is idle** (dry run):

   ```bash
   ~/.claude/skills/team-teardown/scripts/reap-teammates.sh --idle
   ```

   It prints one `IDLE <name> type=<agentType> cwd=<cwd>` line per idle
   teammate (alive, `isActive: false`), then the usual table with each
   non-kept idle teammate as `would-reap`. Working teammates never appear.
2. **Reuse** — SendMessage each idle teammate whose type and directory fit a
   lane you were about to spawn, and drop that spawn.
3. **Reap the rest** and record the reconcile:

   ```bash
   ~/.claude/skills/team-teardown/scripts/reap-teammates.sh --idle --keep <reused,...> --yes
   ```

   Omit `--keep` when nothing was reused (an empty `--keep` is exit 64).
   `--yes` writes the reconcile marker
   (`~/.claude/state/team-reconcile/<session id>`, overridable
   `TEAM_RECONCILE_DIR`) even when nothing was idle, which re-opens the gate
   for 120 seconds; markers older than 24 h are pruned on the same write.
   A `--keep` name that is not an idle teammate of this session is reported
   on stderr and ignored. A `working` teammate is never reaped, `--keep` or
   not.
4. Spawn only the lanes still uncovered, in one message.

`--idle` scopes itself to the running session through
`$CLAUDE_CODE_SESSION_ID`, with no fallback: run from outside a Claude Code
session (a plain terminal, cron) it exits 69 and selects nothing. It cannot
be combined with `--session`, `--dead-leads-only` or `--from-hook`, and
`--keep` without `--idle` is rejected — all exit 64.

A reused teammate can still read as idle for a moment, until it picks up the
SendMessage. If the window has lapsed by then, the gate refuses again and
names it as reusable; a fresh reconcile re-opens the window.

## Full teardown: a previous session's teammates, or an explicit clean-up

The three stages below retire a whole team. Use them when a previous session
(e.g. one you resumed) left teammates running, or when asked to clean up
agents or panes — not as the end of every lane.

## Stage 1 — Request

Send every teammate a shutdown request naming why its lane is closed:

```
SendMessage(to: "<name>", message: {"type":"shutdown_request","reason":"<lane> complete"})
```

Send them all in one message. Wait for the approvals, roughly 15 seconds.
A `shutdown_response` reply with `approve: true` means that one agreed to
exit — but the reply alone does not prove it actually did (see Stage 2).

## Stage 2 — Verify

Do not trust the replies. Do not `ps | grep` for the agent-id token either —
use the reaper's own dry run instead:

```bash
~/.claude/skills/team-teardown/scripts/reap-teammates.sh --session <sid8>
```

`<sid8>` is the first 8 characters of this session's id. Use the reaper's dry
run, not a hand-written `ps | grep`: it matches on exactly the
`--agent-id <name>@session-<sid8>` token the reaper kills on, so the verify
step and the reap step can never disagree about what counts as a live
teammate. A hand-written grep can drift from that regex without anyone
noticing.

Scoped to `--session <sid8>` (no `--dead-leads-only`), a dry run reports only
`would-reap`; it never emits `already-gone` (that only happens when actually
killing, in Stage 3) or `spared-live-lead` (that only happens under
`--dead-leads-only` — see the Outcomes table below). On the
terminated-but-unreaped case specifically: on macOS such a process loses its
argument vector and renders as `<defunct>`, so it drops out of `--agent-id`
matching entirely rather than being misreported by the dry run. If a dry run
ever shows `would-reap` for something you believe is already dead, treat
that as a signal to re-run Stage 1 and re-check — not as a reason to jump
straight to `--yes --force`. Anything the dry run reports as `would-reap`
ignored the shutdown request.

## Stage 3 — Reap

```bash
~/.claude/skills/team-teardown/scripts/reap-teammates.sh --session <sid8>        # dry run
~/.claude/skills/team-teardown/scripts/reap-teammates.sh --session <sid8> --yes  # act
```

Dry run first, always. Report each teammate by name and outcome.

### CLI

| Flag | Effect |
|---|---|
| `--idle` | Scope to this session's idle teammates via `$CLAUDE_CODE_SESSION_ID` (absent or malformed → exit 69); prints the `IDLE <name> type=<agentType> cwd=<cwd>` reuse menu ahead of the table. With `--yes`, also writes the reconcile marker the spawn gate reads. Mutually exclusive with `--session`, `--dead-leads-only` and `--from-hook` (exit 64 if combined) |
| `--keep <a,b>` | With `--idle` only (exit 64 otherwise): spare these idle teammates from reaping. Unknown names are reported on stderr and ignored |
| `--session <sid8>` | Scope to one session's teammates (first 8 hex chars of the session id). Deliberately does not consult lead liveness — it dismisses this session's teammates regardless of whether the lead is alive, because at teardown time the lead is you. Mutually exclusive with both `--from-hook` and `--dead-leads-only` (exit 64 if combined) — each of those would otherwise silently win over an explicit `--session` |
| `--from-hook` | Read the session id from a hook payload on stdin instead of `--session`. Mutually exclusive with `--session` (exit 64 if combined) |
| `--dead-leads-only` | Sweep teammates whose lead process is dead, across all sessions. The only mode that consults lead liveness — that's the whole point of the sweep. Mutually exclusive with `--session` (exit 64 if combined) |
| `--yes` | Actually kill; without it, dry run only |
| `--force` | Skips the grace period when acting — `TERM`, then immediate `SIGKILL`. Does **not** imply `--yes`; you still need `--yes` to act. (No dry run ever waits, `--force` or not — the grace period is only consumed while actually killing.) |
| `--json` | Machine-readable output |
| `-h` | Help |

### Outcomes

Each teammate is reported as one of:

- `would-reap` — dry run, any mode; this teammate would be killed by `--yes`
- `spared-live-lead` — dry run or acting, **`--dead-leads-only` only**: a lead
  process was **positively found alive** for this teammate, so it's never
  touched, even idle for hours (see below). `--session <sid8>` can never
  produce this outcome — it does not gate on lead liveness at all
- `spared-unknowable` — dry run or acting, **`--dead-leads-only` only**: lead
  liveness could not be determined, so the teammate is spared same as a
  confirmed-alive lead, but this is a different claim and reported under a
  different label. Covers: `jq` missing from `PATH`; the sessions ledger
  directory missing, unreadable, or non-traversable; a malformed (unparseable)
  ledger entry; a ledger entry missing `pid` or `sessionId`; and a teammate
  carrying no `--parent-session-id` at all. Each case also logs one line to
  stderr naming the offending file or condition
- `reaped` — killed; only when acting with `--yes`
- `already-gone` — only when acting with `--yes`; covers **both** "no such
  process" and "terminated but not yet reaped by its parent." Neither is a
  failure; do not report either as one
- `failed` — only when acting with `--yes`; survived `SIGKILL`
- `recycled` — the pid no longer matches the teammate it was identified as,
  so no signal was sent. Two causes, and the second is the common one:
  the OS reassigned the pid to an unrelated process, **or** the teammate is
  mid-exit and the kernel no longer reports its argument vector (macOS prints
  it as `(claude)`). The second case is expected whenever a teammate complied
  with the Stage 1 shutdown request and is already on its way out, so
  `recycled` frequently means "it did what we asked" rather than anything
  anomalous. Either way withholding the signal is correct — a process whose
  identity cannot be confirmed must not be killed, and one already exiting
  does not need to be. Its children get `TERM` but not `KILL`, which is moot
  for a process the kernel is already tearing down.

### Exit codes

| Code | Meaning | What to do |
|---|---|---|
| 0 | All clear, or nothing to do | Report done |
| 64 | Bad arguments — including a `--session` value that isn't 8 hex characters, or a non-numeric/negative `REAP_GRACE` | Fix the invocation |
| 69 | No session id resolvable — for `--idle`, `$CLAUDE_CODE_SESSION_ID` is absent or malformed | Pass `--session <sid8>` explicitly; for `--idle`, run it from inside the Claude Code session |
| 70 | A teammate survived `SIGKILL` | Report it by PID; do not claim a clean teardown |

## Cleaning up after a crashed session

A teammate whose lead process is dead is garbage — nobody can read or message
it. Sweep those without naming a session:

```bash
~/.claude/skills/team-teardown/scripts/reap-teammates.sh --dead-leads-only        # dry run
~/.claude/skills/team-teardown/scripts/reap-teammates.sh --dead-leads-only --yes
```

Teammates whose lead is still alive are reported `spared-live-lead` and are
never touched, even when idle for hours. That is deliberate: idle-and-abandoned
cannot be reliably distinguished from idle-and-between-assignments.

## Pane cleanup

`reap-teammates.sh --yes` removes a dead teammate's tmux pane itself, as a
second step strictly after that teammate's process is confirmed gone —
never before, never concurrently. **Claude Code sets `remain-on-exit
failed` on every teammate pane, so a pane never closes on its own just
because its process exited** (measured 2026-09-21; an earlier revision of
this skill said otherwise). Do not `tmux kill-pane` a teammate pane
yourself — the reaper already does it, in the right order, and logs the
pane's identity to `~/.claude/logs/team-teardown.log` before removing it.
Injectable as `REAP_TMUX` (default `tmux`); degrades to a silent non-event
when tmux is absent, no server is running, or the teammate never had a real
tmux pane (in-process backend).

## Dead-teammate reporting

Separately from pane cleanup, the `UserPromptSubmit` roster hook
(`roster-line.sh`) tells a lead when a teammate it is responsible for has
died — not just which ones are currently live. The team config
(`~/.claude/teams/session-<team-id>/config.json`) is append-only in
practice, so a lead polling only the live roster gets silence forever for a
teammate that never started or crashed mid-work. The hook cross-checks each
member's `isActive` field against actual process liveness and adds a second
line, only when something is actionable:

- `isActive: null`, process gone — **never started** (spawn failure); re-spawn it.
- `isActive: true`, process gone — **died mid-work**; stop waiting on it, do not assume it will come back.
- `isActive: false`, process gone — finished normally. Never mentioned; this is the common case and would otherwise be pure noise.

The live line splits teammates whose process is still alive, and is what a
lead reads to decide reuse before spawning:

- `Working: a, b.` — alive with `isActive: true` or `null`, plus any live
  teammate the team config does not account for (no team dir resolved, or
  not yet written to `config.json`). Busy; never offered for reuse.
- `Idle, reusable: name (agentType, cwd).` — alive with `isActive: false`.
  Reuse one via `SendMessage` when a planned spawn has the same `cwd` and
  `agentType`; reap the rest with `reap-teammates.sh --idle --keep <reused> --yes`.

## Limitations

- Only native Claude Code teammates, identified by `--agent-id <name>@session-<sid8>`.
- For OMC modes — `ralph`, `ultrawork`, `omc-teams`, `autopilot`, `swarm` — use
  `/cancel` instead, not this skill. `/cancel` is LLM-executed and scoped to
  OMC modes; it clears native team artifacts only under `--force`/`--all`,
  and it never runs from `SessionStart` or `SessionEnd` — so it cannot close
  the crash-orphan path that `--dead-leads-only` exists for.
- Never *modify or delete* anything under `~/.claude/teams` or
  `~/.claude/tasks`. Claude Code's retention sweep owns those at
  `cleanupPeriodDays`, default 30. `roster-line.sh` reads (never writes)
  team configs under `~/.claude/teams` for the dead-teammate check above;
  that is not an exception to this rule, since it's read-only.

## Supported platforms

Tested on macOS (BSD `ps`, bash 3.2.57) and Linux (Debian 13.6, procps-ng
4.0.4, bash 5.2.37, verified in a container via `tests/run-linux.sh`) — all
seven test suites pass identically on both: `test-reap.sh` 134,
`test-roster.sh` 52, `test-session-end.sh` 22, `test-spawn-gate.sh` 27,
`test-team-state.sh` 15, `test-dispatch-nudge.sh` 12, `test-session-start.sh`
66 = 328 checks (2026-09-30, after the resumed-session team-lookup fix; the four original suites stood at
115 / 42 / 18 / 52 = 227 on 2026-09-21, up from 163 at 2026-09-18's close-out — pane-cleanup and
dead-teammate-reporting test cases, plus three review fix rounds covering
an empty-pane_pid match bug, a lead-classification edge case, an
unwritable-log-target ordering fix, a mutation-tested case-exclusion
fixture that the first round's tests claimed to pin but didn't, and —
found only by instrumenting the stubs, not by reading the prose — two of
those same tests asserting the exact inverse of what actually executes).
`REAP_PS`
defaults to
`ps -eww -o pid=,command=` unconditionally, because GNU procps can truncate
the command column — cutting off `--parent-session-id` and silently turning
`--dead-leads-only` into a no-op. Measured condition: piped output is **not**
truncated when `COLUMNS` is unset, so the trigger is `COLUMNS` present in the
environment (or stdout being a terminal), not the old spelling by itself.
`-ww` removes that dependency. Note the suites all stub `REAP_PS`, so the
container run does not exercise this default — a static grep guards it.
Not tested: BusyBox `ps` (Alpine), WSL, or any distro besides Debian — see
the design doc's "Supported platforms" section for exactly what was run and
what wasn't.

## Related skills

- `/team-dispatch` — the other half; its Protocol step 0 is the reconcile above
- `/cancel` — OMC modes and tmux CLI worker teams
