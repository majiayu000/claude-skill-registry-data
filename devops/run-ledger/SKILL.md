---
name: run-ledger
description: Instrument an unattended job with START/END lines and read the run ledger it leaves. Use when the user wants to know whether a scheduled claude -p, cron, launchd, systemd or CI job really ran, asks to add a heartbeat, start/end logging or run history to a job, or asks which runs hung, failed or were skipped. Detects a START without END, gaps between starts, a schedule that stopped, and failed statuses.
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/ledger.sh *)
---

# Run ledger: START/END for every unattended run

> **Running the scripts.** One Bash call = one script call, by the absolute path shown
> (`${CLAUDE_SKILL_DIR}/scripts/<script>`), with no `bash` prefix, no variable assignment, and nothing
> chained after it (`;`, `&&`, `|`, `echo $?`): the exit code is reported anyway. Only that exact
> form is pre-approved by this skill's `allowed-tools`; in `dontAsk` mode or a headless
> `claude -p` run, anything else is refused. Use the Read tool, not `cat` or `tail`, for logs.

A scheduler's own status says little. A run that hangs writes no error; a fire that never
happens writes nothing at all. What they never write is the proof that they started **and**
finished. The ledger is that proof: one `START` line before the work, one `END` line after it,
in a plain tab-separated file.

```
START  20261012T030001Z-4242  2026-10-12T03:00:01Z
END    20261012T030001Z-4242  2026-10-12T03:04:10Z  ok
```

Default file: `$LEDGER`, else `./.heartbeat/beats.tsv`. The format is the one used by the
launcher of the Unattended Claude Code Field Kit, so both can share a file.

Script: `${CLAUDE_SKILL_DIR}/scripts/ledger.sh`. To instrument a job, copy it into the job's
repository (e.g. `tools/ledger.sh`); to read a ledger, run it from the skill folder.

## A. Instrument a job (pick one)

**1. Wrap the command (simplest, cron/launchd/systemd/CI).** Copy `ledger.sh` next to the job
(e.g. `tools/ledger.sh` in the repository) and put `wrap` in front of the command:

```bash
cd /path/to/repo && tools/ledger.sh wrap -- timeout -k 60 45m /full/path/to/claude -p "$(cat prompt.md)" --output-format stream-json --verbose >> logs/agent.log 2>&1
```

`wrap` writes START, runs the command (stdin from /dev/null, as a background job), writes
`END ok` or `END exit-N`, writes `END killed` if the wrapper itself gets TERM/INT/HUP, and exits
with the command's status. Keep `timeout` (on macOS: `gtimeout` from coreutils): the ledger
records a hang, it does not stop one.

**2. Explicit calls, when the job script has several steps or its own statuses:**

```bash
id=$(tools/ledger.sh start)
# ... work ...
tools/ledger.sh end "$id" ok          # or skip-nothing-new, exit-3, timeout, no-work ...
```

Statuses are one word (letters, digits, `.`, `_`, `:`, `-`). `ok` and anything starting with
`skip` count as healthy; everything else is reported as FAILED.

**3. Inside a cloud routine or Desktop scheduled task** (no wrapper of yours runs there): make
the first and last steps of the prompt write the lines, and commit the file so another clock can
read it:

```
First step: run `tools/ledger.sh start` and keep the id it prints. Commit and push .heartbeat/beats.tsv.
Last step, whatever happened: run `tools/ledger.sh end <id> <status>` and commit and push again.
```

When editing a user's job, show the diff and keep their existing redirections and timeouts.
Never put the ledger in a directory the job deletes or resets (`git clean`, a temp dir).

## B. Read the ledger

```bash
"${CLAUDE_SKILL_DIR}/scripts/ledger.sh" report -f .heartbeat/beats.tsv -n 20     # one line per run: start, end, duration, status
"${CLAUDE_SKILL_DIR}/scripts/ledger.sh" check  -f .heartbeat/beats.tsv -e 3600 -m 2700
```

`-e` = expected interval between starts (seconds), `-m` = longest healthy run (seconds).
`check` prints one finding per line and exits 0 (OK), 1 (findings) or 2 (no ledger):

| Finding | Meaning | Next step |
|---|---|---|
| `OPEN <id> ...` | START without END after `-m` | hung, killed or crashed: the run's log; `chain-diagnose` link 4 |
| `GAP a -> b (... slots missed)` | starts further apart than 1.5 x `-e` | scheduler did not fire: `chain-diagnose` link 1 |
| `LATE last START ...` | nothing started for 1.5 x `-e` up to now | the schedule stopped: `chain-diagnose` link 1 |
| `FAILED <id> <status>` | the run ended badly | classify its log: `chain-diagnose` |
| `BAD-LINE <n>` | line n is not a record | two writers interleaved, or a hand edit |

`--now 2026-10-12T02:30:00Z` (or epoch seconds) pins the clock, e.g. to replay "what would the
check have said at 3 a.m.".

## C. Turn the check into an alarm

The check is useful only if something other than the job runs it, on another clock:

```cron
35 * * * * cd /path/to/repo && tools/ledger.sh check -e 3600 -m 2700 >/dev/null || echo "agent: ledger check failed"
```

(cron mails the output line if mail is set up.) Or run it in a GitHub Actions schedule on a
repository where the job pushes the ledger: a failed step sends the owner an email. If the user
has the Field Kit, its `missed-run-check` workflow does exactly this; use this skill to read and
explain the ledger, and that workflow for the hourly alarm.

## Report

Give the user: the command(s) you added or the findings, the last 3 runs from `report`, and the
exact `check` line they can schedule. Do not claim a job is healthy from one `OK`: say over which
period the ledger covers it.
