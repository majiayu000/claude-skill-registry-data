---
name: ctx-core
tier: D
primitive: null
category: orchestration
version: 0.3.1
description: |
  The shared context core, phase 1: a read-only shared board for every Claude
  Code session in a workspace scope. Hooks publish each session's start, the
  keyword of its ARC-STATUS line at every Stop, and its death on StopFailure to
  one append-only log per scope, as structured fields only. A SessionStart hook
  injects a short factual brief of the board rows for the session's branch and
  cwd, including other live sessions on the same branch. Sessions in different
  worktrees therefore see each other without anyone reading a transcript. `ctx
  board` shows the board, `ctx doctor` checks the config, store and hooks, and
  `ctx doctor --unscoped` lists repos that have sessions but no scope.
  Coordination only; not a security boundary. USE WHEN setting up or checking
  the shared board, asking "which sessions are on this branch", "what is every
  session doing", "is anyone else working here", reading or debugging the ctx
  store, registering the ctx hooks, or adding a repo to a scope. Also holds
  the System 1 injection gate (off by default): at each hook stage it looks
  the event's keys up in a cache System 2 builds offline (`ctx-s1 build`, BM25
  over specs, entities, PRs, memory rules and board sessions) and injects a
  cached factual claim only when it clears that stage's floor, else abstains;
  with its evals (`ctx-s1 eval`: offline replay; `ctx-s1 tune`: the bounded
  tune loop) and the owner's registration script. NOT FOR messaging a session
  or waking an idle one (phase 2, not built), enforcing what a session may do
  (no local hook is a boundary), or waiting on CI (use p9).
when_to_use: |
  Triggers on "ctx board", "ctx doctor", "shared board", "shared context core",
  "who else is on this branch", "which sessions are live", "register the ctx
  hooks", "add a scope", "unscoped repos", "board.json", "events.jsonl",
  "ctx s1", "ctx s2", "System 1 gate", "injection gate", "[ctx claims]",
  "s1-decisions.jsonl", "which stage injected this", "tune the gate's floors".
---

# ctx-core: the shared board (phase 1)

In the 09-26 → 09-29 run, coordination state lived in the coordinator's
context window. Compaction kept dropping it, and no worker session could see
another. Phase 1 of the shared context core
([design](https://github.com/broomva/workspace/pull/825),
`docs/specs/2026-09-29-shared-context-core.html`) puts the minimum of that
state on disk: which sessions exist in a scope, where they are (cwd, branch),
the keyword of their last ARC-STATUS line, and whether they died. Every
session gets the relevant slice of it at start.

It is read and publish only. There is no mailbox, no wake-up, and no
retention.

## What it stores: structured fields, no free text

| Field | From | Kept as |
|---|---|---|
| `session_id`, `paseo_agent_id` | hook input, `PASEO_AGENT_ID` | id-shaped strings (`[A-Za-z0-9][A-Za-z0-9._:-]{0,127}`), otherwise omitted |
| `cwd`, `repo`, `branch` | the filesystem and git | flattened to one line |
| `type`, `ts` | the hook | `session.start`, `session.stop` or `session.died`; UTC milliseconds |
| `arc_status`, `arc_line` | Stop's `last_assistant_message` | The last line matching exactly `^ARC-STATUS: [A-Z]+`. The keyword is `MERGED`, `CLOSED`, `DONE`, `BLOCKED`, or `OTHER`, plus at most the first 120 characters of that line |
| `error` (the row's `died_error`) | StopFailure | The error class (`rate_limit`, `billing_error`, …). Claude Code 2.1.280 sends it as `error`; the reference documents it as `error_type`. A value that is not class-shaped is stored as `unknown`. `error_details` and the message text are never read |

Nothing else is written: no model, source, role, prose, message text or error
text. The schema is enforced on read too, so a hand-written log line with free
text, an unknown key, or a guard-failing field is skipped by the fold.
Schema: [`references/event-schema.md`](references/event-schema.md).

**One cheap guard** (`guard_ok`) runs on every stored string. It drops a field
in either of two cases:
- The field contains `crm/`, `Bearer `, `ghp_`, `gho_`, `github_pat_`, `sk-`,
  `xox` or `AKIA`. These match case-insensitively, and only at the start of a
  token, so `fix/task-list` and `mycrm/` pass.
- The field contains a run of 32 or more ASCII letters and digits.

It is substring finds plus one byte-translate scan, with no regular
expression, and it is linear (tests at 10 KB and 1 MB). What it drops:
- a status line that fails is stored as its keyword alone;
- a branch or agent id that fails is omitted;
- a cwd or repo that fails means no event is written at all, which covers a cwd
  under `crm/`.

The guard sees the whole status line before the 120-character cut, so a token
is never cut in half and kept. It is narrow on purpose. It does catch a
40-character commit SHA (a run of 40), so a status line quoting one keeps only
its keyword. It does not catch a short token of an unlisted shape; what bounds
that exposure is that only a 120-character status line of a strict shape is
stored at all.

## How it works

| Piece | Does |
|---|---|
| `scripts/ctx-hook.sh` | The registered command. It execs `python3 -I -S ctx_hook.py` only if that file and the interpreter exist, and otherwise exits 0. A Python asked to run a missing file exits 2, and a Stop hook exiting 2 keeps its session turning |
| `scripts/ctx_hook.py` | The hook entry for `session-start`, `stop` and `stop-failure`. It owns the deadline, the output guard, the miss record, and exit 0 |
| `scripts/ctx.py` | The single writer and reader: scope resolution, the guard, the append, the fold, and the CLI |
| `~/.config/ctx/scopes.yaml` | Scope id → repos, written by the owner. The key is the realpath of the repo's git common dir, so every worktree of a repo lands in its main checkout's scope |
| `~/.local/state/ctx/<scope>/events.jsonl` | Append-only, one JSON object per line |
| `~/.local/state/ctx/<scope>/board.json` | A cache: the log folded up to `log_offset` |
| `~/.local/state/ctx/hook-misses.jsonl` | One line per hook that ran out of time or skipped work: event, stage, ms, with no path. Machine-wide. Written only when `scopes.yaml` exists, and rotated to `.1` at 1 MiB |

**Writes are append-only.** A hook takes the lock (`fcntl.flock(LOCK_EX |
LOCK_NB)`), appends one line, and releases it:
- Nothing else happens under the lock, so its hold does not grow with the board
  (a test bounds it under 5 ms with a 10,000-session board in place).
- Hooks wait at most 40 ms for the lock. StopFailure, the one terminal event,
  waits for what is left of its budget.
- A skipped append is recorded as a miss.
- Stop and StopFailure never touch `board.json`.

**Reads fold the tail.** `board.json` is a cache.
- Readers fold the log since its offset. A crc32 over the 64 bytes before that
  offset detects a replaced or truncated log.
- SessionStart folds at most 64 KiB past the cache and never the whole log.
  Once it has folded 16 KiB, or run out of cap, it writes the advanced cache
  back (an atomic replace, with no lock). So a cache that fell behind catches
  up across SessionStarts, which give no brief until it has.
- `ctx board` folds the whole tail and writes the cache back.
- `ctx board --rebuild` recomputes the cache from byte 0.
- Cache plus tail is byte-identical to a full rebuild (a test pins this).

**How it finds the repo.** A hook reads `.git`, the `gitdir:` file of a
worktree or submodule, and `commondir` itself, which is the rule `git
rev-parse --git-common-dir` follows. So a hook spawns no process. A test checks
that the resolver agrees with git on each of these layouts:
- a main checkout and its subdirectories;
- a linked worktree;
- a nested repo;
- a submodule;
- a `.git` directory, a bare repo, and a non-repo, each of which gives no repo.

git runs only when `GIT_DIR`, `GIT_WORK_TREE` or `GIT_COMMON_DIR` redirect it,
or to read a reftable repo's branch. It is then bounded and killed.

**Live**, one definition in the code (`LIVE_DEFINITION`), here and in
PLANS.md: *an event within the last 6 h and no `session.died` since the
session's last other event.* A session that died and later started again is
live. `session.died` is the only terminal event; Stop fires at the end of
every turn.

Invariants, each pinned by a test:

- **A repo with no scope is a silent no-op.** Every hook and every command
  exits 0 with no output. The same holds for a cwd outside git and for a repo
  listed in two scopes; the ambiguous repo has no scope, and the other repos
  are unaffected. A malformed `scopes.yaml` disables every scope. `ctx doctor`
  reports that from any directory and exits 1.
- **Scopes never cross.** The `sri` and `broomva` stores are separate
  directories. A test audits every `open()`, `io.open()` and `os.open()` an sri
  session makes, and finds none under broomva's store.
- **A hook never blocks a session:**
  - The lock covers the append and nothing else.
  - The hook has a hard self-deadline of 80 ms inside the interpreter, and 200
    ms of wall time measured from outside, on the owner's machine and on Linux.
    A run the deadline cuts records when it fired (when
    `~/.config/ctx/scopes.yaml` exists). A hosted macOS CI runner is slower:
    its clamped QoS fires the alarm up to about 160 ms late (at most 10 ms in a
    process a Claude Code session spawns on the owner's machine), and start-up
    has reached 589 ms. There a hung ctx module is held to 1 s, half of Claude
    Code's timeout.
  - A hook never parses a `board.json` over 2 MiB, because that parse is one C
    call the alarm cannot interrupt.
  - Every hook exits 0, including on SIGTERM and through the wrapper.
  - Tracebacks and stray prints go to `/dev/null`.
- **Injection fails open, and the failure is recorded.** A hook that runs out
  of time, skips its append, meets a board over the cap, or finds the cache too
  far behind injects nothing and leaves one line in `hook-misses.jsonl`. So
  `ctx doctor` can tell "too slow" from "not registered".
- **The brief is factual statements only.** The phase-0 spike found models
  treat imperative text in hook output as prompt injection. So the brief has no
  imperatives and no second person, and every field is flattened to one line. A
  newline in a directory name, or a U+2028 or NEL in a status line, cannot
  start a sentence of its own. The one piece of a session's own words, its
  status line, appears only as a labelled quote.

## What it does NOT do

**It is not a security boundary.** The owner decided on 2026-09-29 that the
core is coordination only. Hooks and `disallowedTools` guard against
accidents. The boundary is the GitHub rulesets and the server-side merge gate.
The phase-0 spike (`~/.config/broomva/fleet/ctx-spike-20260929/SPIKE-REPORT.md`)
is why:

- **P4:** `disallowedTools` removes a tool from the model's surface, even under
  bypassPermissions. But any session with Bash can still:
  - write files, so it can append anything to `events.jsonl` (the fold skips
    lines that break the schema, but a well-formed lie is folded) or hand-edit
    `board.json` (`ctx doctor` detects a hand edit, but nothing prevents one);
  - `curl` the Paseo MCP endpoint with the bearer token in its own argv. The
    token is shared by every session, and `callerAgentId` is spoofable.

  The board is what sessions *say*, not an attestation.
- **P6:** a hook that crashes or overruns its timeout fails open. That is the
  right polarity for injection, which is all phase 1 does, and it is why no
  deny rule may rest on these hooks.
- **P7:** a `create_agent` with a plain `claude/*` provider yields a session
  with no role. Phase 1 stores no role at all.
- **P1/P2:** asyncRewake wakes an idle session, but models ignore imperatives
  in its payload, and a lapsed watcher strands mail. Phase 1 arms no watcher.
  It also makes no headless-vs-interactive call. `CLAUDE_CODE_ENTRYPOINT` is
  `sdk-cli` for Paseo sessions too (#825 round 4), so nothing reads it.
- **P8:** Paseo's `lastActivityAt` is its `updatedAt`, so a label write resets
  it. Liveness here comes only from the core's own events (see *Live* above).
  Nothing marks a session ended (SessionEnd is not hooked), so a closed session
  stays live for up to 6 hours.
- **Not built in phase 1:**
  - **Retention.** The log and `board.json` only grow; `ctx doctor` says so.
  - The mailbox, deltas on each prompt, and asyncRewake (phase 2).
  - The role gate and the owner CLI. The design cut them; no phase will build
    them.

**When the board reaches its cap.** A row is 550–720 bytes (measured), so the
2 MiB a hook will parse holds about 2,900–3,800 sessions: roughly 4 weeks at
~117 sessions a day. Past that, hooks still append, but SessionStart gives no
brief. Each such run leaves a `board-cap` miss, and `ctx doctor` reports a
PROBLEM (it warns at half). The recovery path:
1. `ctx board --rebuild` rebuilds the cache from the log. That fixes a stale or
   hand-edited cache, but not a board that is simply large.
2. To shrink the board, move the log aside by hand, e.g. `mv events.jsonl
   events-2026-10-27.jsonl` in the scope's store, then run `ctx board
   --rebuild`. The board then holds only what is appended afterwards.
3. A scripted archive procedure, with retention, is phase 2.

## Commands

```bash
CTX="python3 -I ~/broomva/skills/skills/orchestration/ctx-core/scripts/ctx.py"
$CTX board              # cache + tail, printed newest first with the live count (writes the cache back)
$CTX board --json       # the board as JSON
$CTX board --rebuild    # recompute the cache from byte 0; says whether the old cache matched
$CTX doctor             # config, store, cache, hook activity, misses, board size, retention
$CTX doctor --unscoped  # from anywhere: repos with Claude Code sessions (last 14 days) but no scope
$CTX doctor --compare   # the phase-1 exit comparison: live board rows vs listed sessions, 6 h (ctx_compare.py)
$CTX -C <dir> board     # as if run in <dir>
```

In a repo with no scope, `board` prints nothing and exits 0, and so does
`doctor` unless the config itself is broken or ambiguous, which it reports
from any directory. `doctor` exits 1 in any of these cases:
- the config is broken;
- a repo is listed in two scopes;
- the cache differs from a rebuild of what it claims to have folded;
- `board.json` is over the 2 MiB a hook will parse;
- Claude Code sessions ran in the scope in the last 24 h (judged from their
  transcripts) and no hook recorded any of them. That is the BRO-2019
  silent-dead-hook case, which doctor attributes to misses when there are any,
  and otherwise to registration.

An idle scope is not a problem. A cache far behind the log is a warning: it
catches up by itself.

`doctor --compare --registered <UTC time> [--hours 6] [--json]` is the phase-1
exit criterion (core spec §9 as merged in workspace#842): board rows that are
live against in-scope sessions from `claude agents --json --all` with a
timestamped transcript entry in the same window (not the mtime), matched on the
full session id. The pass bar is ≥95% each way on the raw sets; every
difference gets one reason from an ordered list, which explains it and removes
nothing, and in-scope transcripts on neither side are listed uncounted. The
registration time is passed once and kept in `compare.jsonl`'s first line; a
later one that disagrees is refused. It rebuilds the board in memory and writes
only `compare.jsonl`. No evidence (an unreadable transcript directory, an empty
listing, an empty side) fails. fleet-reconcile's tick runs it once a day.
The last entry is read from the transcript's tail, widening from 128 KiB to
2 MiB and 16 MiB when the last line is larger (`last_in_tail`, which
fleet-reconcile reads activity through). A comparison that raises is written
as an error line too.

The first run is the owner's. A `compare.jsonl` written by the pre-spec
prototype (its first line has no `neither` field; its registration time was a
guess, not the hooks' registration that §9 wants), or one whose first line
can't be read, is refused until it is moved aside, once per scope. The loop
moves only such a file and never overwrites an earlier move:

```bash
for s in broomva sri; do f=~/.local/state/ctx/$s/compare.jsonl
  [ -f "$f" ] && ! head -1 "$f" | grep -q -e '"neither"' -e '"error"' && mv -n "$f" "${f%.jsonl}.prototype.jsonl"; done
cd ~/broomva && python3 <ctx-core>/scripts/ctx.py doctor --compare --registered <UTC time the hooks were registered>
cd ~/broomva/work/stimulus/sri && python3 <ctx-core>/scripts/ctx.py doctor --compare --registered <same, or sri's own>
```

## Registration (owner step; an agent does not apply it)

Registering hooks is human-gated. No agent edits `~/.claude/settings.json`,
`~/broomva/.claude/settings.json` or any `hooks.json`. The owner applies these
three steps.

**1. Scopes.** Write `~/.config/ctx/scopes.yaml`. The grammar is a strict
subset of YAML: two-space indents, one path per `- ` item, and `#` comments.
List a repo by its main checkout, its `.git`, or any of its worktrees:

```yaml
version: 1
scopes:
  broomva:
    - ~/broomva              # broomva/workspace
    - ~/broomva/skills       # broomva/skills
    - ~/broomva/bstack       # broomva/bstack
    - ~/broomva/broomva.tech
  sri:
    - ~/broomva/work/stimulus/sri
```

`ctx doctor --unscoped` then lists every repo that has sessions and is not in
the file.

**2. Hooks.** Merge these entries into the `hooks` object of
`~/.claude/settings.json` (user scope, so the hooks fire in every repo,
including Paseo worktrees and `claude -p`). If `SessionStart`, `Stop` or
`StopFailure` already has entries, **append** to its array; do not replace
it.

Each command runs the wrapper, which exits 0 if the skill is moved or the
checkout is on another branch. If the wrapper itself is missing, `/bin/sh`
exits 127, which Claude Code treats as a non-blocking error. `CTX_PYTHON` pins
the interpreter so that the hook shell's `PATH` cannot swap in a slower one:

```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [ { "type": "command", "timeout": 2,
        "command": "CTX_PYTHON=/opt/homebrew/bin/python3 /bin/sh /Users/broomva/broomva/skills/skills/orchestration/ctx-core/scripts/ctx-hook.sh session-start" } ] }
    ],
    "Stop": [
      { "hooks": [ { "type": "command", "timeout": 2,
        "command": "CTX_PYTHON=/opt/homebrew/bin/python3 /bin/sh /Users/broomva/broomva/skills/skills/orchestration/ctx-core/scripts/ctx-hook.sh stop" } ] }
    ],
    "StopFailure": [
      { "hooks": [ { "type": "command", "timeout": 2,
        "command": "CTX_PYTHON=/opt/homebrew/bin/python3 /bin/sh /Users/broomva/broomva/skills/skills/orchestration/ctx-core/scripts/ctx-hook.sh stop-failure" } ] }
    ]
  }
}
```

The path assumes the `~/broomva/skills` checkout is on `main`. If the skill is
installed with `npx skills add broomva/skills --skill ctx-core`, use the
installed copy's `scripts/ctx-hook.sh` instead. `timeout: 2` is Claude Code's
outer bound. The hook's own deadline is 80 ms.

**3. Verify.** Open a new session in a scoped repo and end one turn. Then run
`ctx doctor` in that repo. `SessionStart` and `Stop` should report a last
event, and `misses` should be absent or small.

**Phase-1 exit comparator** (#825 round 7). This is a manual check; nothing
computes it:
- One side is the board's live rows (the definition above). `ctx board` prints
  the live count, how many of those have a Paseo agent, and a LIVE column.
- The other side is the `list_agents(cwd: "/")` agents in scope whose
  transcript was modified in the same 6 h.
- Phase 1 passes when at least 95% of each set appears in the other, and every
  difference is listed with its reason.
- Expected reasons for a difference:
  - a single turn longer than 6 h (Stop has not fired, so the row aged out);
  - a session closed within the window (nothing marks a session ended);
  - a session not launched by Paseo (`claude -p`, a terminal session), which
    has no `paseo_agent_id`;
  - a hook that ran out of time or skipped work (`ctx doctor` lists the misses,
    by stage);
  - a session in an unscoped repo, or in a cwd the guard drops.

**Rollback:** delete the three entries from `settings.json`. The store under
`~/.local/state/ctx/` is inert without them.

## System 1: the per-stage injection gate (off by default)

Design of record: workspace#840 §6.2. Full reference, with the telemetry
schema and the eval method: [`references/s1-gate.md`](references/s1-gate.md).

- **System 2** (`ctx_s2.py`, `ctx-s1 build`) runs offline: a tick, a person,
  never a synchronous hook. It indexes the scope's specs, ADRs, KG entities
  (not person, persona or org ones), memory rules (not `user` ones), open and
  recent PRs (not fork PRs, nor any touching `crm/`), and live board sessions;
  skips anything under `crm/` and anything the guard rejects; ranks with BM25 behind a ranker interface; and writes one
  sharded cache per scope, swapped in by one atomic rename.
- **System 1** (`ctx_s1.py`) runs in the hook. Per event it builds keys (the
  path in `tool_input`, the branch, prompt words, a PR number, the words a
  shell command searches for), sums the cached scores, and injects the best
  claims only when they clear the stage's floor, within the stage's budget,
  once per session. Otherwise it abstains, and abstaining is the default. Each
  claim is one line copied from its source (an entity's core_claim, a spec's
  lede, a PR's title and state, a memory rule quoted) with its source id,
  under a `[ctx claims]` header. Every decision is logged to
  `s1-decisions.jsonl` with its top candidates and why.
- **Stages:** `session-start`, `compact` (SessionStart), `prompt`, `pre-edit`,
  `post-read`, `post-bash`, `subagent`, and `post-compact` (measurement only).
  PreCompact and PostCompact could not inject on CLI 2.1.280
  (`references/s1-stage-probe.md`).
- **Off unless named:** `CTX_S1=1` and the stage in `CTX_S1_STAGES`;
  `CTX_S1_SHADOW=1` logs and injects nothing; `~/.config/ctx/s1-off` stops
  every stage. The shipped floors (`references/s1-params.json`) abstain on
  everything: in E1 today no stage clears the spec's bar (strict
  precision >= 0.30 over >= 50 injections on the test split, stage alone; no
  stage makes a single strict hit there). The tune's proposal,
  `references/s1-params.candidate.json`, is a prompt floor below every
  candidate's score: it gates nothing, so in shadow it logs what the top three
  claims at every prompt would be, the live follow-through a real floor needs.
  It is not for injection.
- **What it never offers:** person, persona and org entities, `user` memory,
  anything under `crm/` (and a PR touching it), fork PRs, session and PR
  claims older than 6 h and 24 h (from the cache or re-offered), the event's
  own file or one the session already opened, a path in another scope's or an
  unscoped repo (a nested checkout included), and to a reviewer subagent
  (`Explore` included: P20's Stratum B runs as one) nothing at all. A
  subagent only ever gets claims its parent received.
- **Fails open:** every error or deadline miss exits 0 with no output; a stage
  that is off costs one `/bin/sh` and no Python.

```bash
S1="python3 -I ~/broomva/skills/skills/orchestration/ctx-core/scripts/ctx_s1_cli.py"   # the `ctx-s1` command (ctx.py's CLI is the core's)
$S1 build [--no-network]          # System 2: build this scope's cache
$S1 snapshot                      # E1's snapshot, private: ~/.local/state/ctx/<scope>/e1/
$S1 eval --params P --out DIR     # E1: replay, every arm, the aggregate report
$S1 tune --params P --ledger L --write-candidate C   # E3
$S1 follow                        # follow-through of live injections
python3 scripts/register_s1_hooks.py --stages pre-edit,post-bash --shadow   # the owner, by hand
```

## Tests

```bash
cd skills/orchestration/ctx-core
python3 -m pip install -r tests/requirements-dev.txt
python3 -m pytest tests/ -q
python3 tests/mutation_check.py   # 39 protections removed in turn; the test pinning each must fail
python3 tests/mutation_check_s1.py   # the System 1 / System 2 / E1 protections, the same way
```

| File | Pins |
|---|---|
| `test_guard.py` | Every needle at a token start, the boundaries, the guard before the cut, free text rejected end to end and on read, and linear time at 10 KB and 1 MB |
| `test_scope_isolation.py` | Unscoped is a silent no-op. A worktree shares its main checkout's scope. The filesystem resolver agrees with `git rev-parse`. sri never reads broomva. Per-repo ambiguity. Malformed configs. crm/ and token-shaped cwds. `doctor --unscoped` |
| `test_lock_contention.py` | A held lock: the hook returns under 200 ms, skips the append, and records the skip. Two concurrent writers: neither blocks, and no line tears. The lock is held under 5 ms with a 10,000-session board |
| `test_rebuild_determinism.py` | Cache plus tail equals a full rebuild. Any split of the log folds the same. Hooks never write the board under the lock. A torn line is healed. A hand edit is detected and replaced. A replaced log is detected. SessionStart never reads the whole log, and catches a stale cache up across runs |
| `test_fail_open.py` | A ctx module that fails to import, raises, prints, hangs, gets SIGTERM or exits non-zero: exit 0 and no output every time, under half of Claude Code's 2 s timeout. Only the hang is cut by the self-deadline, and its own record says when. The wall bound against the registered timeout. Hostile stdin. An unwritable store. The miss breadcrumb and its rotation |
| `test_hook_deadline.py` | The normal path, git never run (or bounded and killed on the `GIT_DIR` path), an 11 MB log, and a board over the cap: each under 200 ms of wall time |
| `test_compare.py` | `doctor --compare`: every reason on the fixed list, the pass bar on the raw sets, a last entry past a large last line, the prototype's line refused, a run that leaves the store's files byte-identical and appends one summary, the exit codes, the CLI in and out of a scope |
| `test_s1_gate.py` | Each stage's positive and negative case, the flags and the kill file, shadow, dedup, path-once, the stage, session and budget caps, compaction and subagent stages, person/crm/credential exclusion, what the decisions log holds, scope isolation |
| `test_s1_failopen.py` | A broken module, a raising decision, hostile stdin, a corrupt or missing cache, a held session lock, the self-deadline, SIGTERM, the wrapper's guards; the off path starts no interpreter; the wall bound per stage |
| `test_s2_cache.py` | The atomic swap, a reader pinned to its build, a build that dies midway, collection never following a symlink, byte-identical rebuilds, private files, the ranker seam |
| `test_s1_eval.py` | E1's counterfactual truth and its masks, the hashed snapshot, where it may be written and its integrity check, exact times, determinism, E3's bounds, ledger, strict objective and acceptance rules; with `CTX_S1_FROZEN` set, the private snapshot's reproduction of the committed report and the spec's bar on the shipped parameters |
| `test_s1_e1_synthetic.py` | E1 end to end on a synthetic world (`s1_synthetic.py`) where a working gate exists: separation on the test split, strict hits, the mutant arms below the gate. CI's E1 step |
| `test_s1_boundaries.py` | A nested repo's or an unscoped repo's path is not keyed; `gh -R` and PR URLs key their own repo; re-offered claims age out; housekeeping never removes a held or recently used lock; the output is emitted before the log line |
| `test_s1_register.py` | The registration script: off unless named, backup, idempotent, only its own entries, `--remove` |
| `test_hooks.py` | Structured fields only. The strict ARC-STATUS shape. The error class only. The brief's relevance, cap, one-line fields, linear cost and factual register. Live after a resumed death. The CLI and doctor. The wrapper: exit 0 with the script or the interpreter gone, against a positive control where Python exits 2 |
