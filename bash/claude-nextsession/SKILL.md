---
name: claude-nextsession
description: >
  Schedule a set of instructions to run automatically once the current
  Claude Code usage session resets, using the local rate-limit cache (no
  API key needed). Trigger: "postpone this to next session", "run this once
  my usage resets", "queue this for later / after the reset", /claude-nextsession.
license: MIT
user-invocable: true
allowed-tools:
  - bash
  - read_file
---

# claude-nextsession Skill

## Purpose
Postpone a series of instructions to the moment your Claude Code usage
session resets. The skill:
1. **Reads the local rate-limit cache** to get the exact reset time for the
   current 5-hour usage window.
2. Schedules a script to run at that exact time with the provided
   instructions, invoking `claude -p` non-interactively.

## How It Works

Claude Code's statusline hook (`~/.claude/statusline-command.sh`) already
receives a `rate_limits` JSON object from Claude Code on every turn — the
same data behind the `session 42% (60m)` indicator in the status bar. This
skill piggybacks on that: the statusline script now also writes the raw
`rate_limits` object to `~/.claude/cache/rate-limits.json` each time it
renders.

`postpone.py` reads `rate_limits.five_hour.resets_at` from that cache — no
API call, no API key needed. This only works for Claude Code's own
subscription-based session limits; it has nothing to do with pay-per-token
API rate limits (those are a different quota system and aren't relevant
here).

**Prerequisite**: the cache must be fresh. It's written on every turn of an
active Claude Code session, so just having run a prompt recently in this (or
any) session is enough. If the cache is missing or older than 6 hours, the
script refuses to guess and asks you to run a prompt first.

## Permissions (important)

The scheduled task runs headless via `systemd-run` — nobody is there to
answer a permission prompt. Without an explicit permission flag, `claude -p`
on existing files **fails silently**: it politely declines the Read/Edit and
exits 0, so the log looks like a success even though nothing happened. Only
creating brand-new files works unprompted by default.

`--permissions` picks how the unattended run is allowed to act:

| Value | Effect |
|-------|--------|
| `scoped` (default) | `--allowedTools "Read Edit Write Bash Glob Grep"` — covers the vast majority of coding tasks without opening up web/MCP/other tools |
| `bypass` | `--dangerously-skip-permissions` — no restrictions at all |

```bash
# scoped (default) — fine for most tasks
python3 postpone.py -i "Fix the failing tests in src/"

# bypass — for tasks that need something outside Read/Edit/Write/Bash/Glob/Grep
python3 postpone.py -i "..." --permissions bypass
```

There is no human oversight when this fires, so pick `bypass` deliberately,
not as a default.

## Usage

### Inside a Claude Code session (the normal way)

Just ask, in plain language — the trigger phrases in this file's frontmatter
match things like "postpone this to next session", "run this once my usage
resets", "queue this for later". Or invoke it explicitly:
```
/claude-nextsession Analyze the logs in /var/log/app/ and generate a report
```

**Instruction for Claude when this skill is triggered:** run
`python3 postpone.py -i "<the user's instructions, verbatim>" -w
"<the current project's working directory>"` via Bash, from this skill's own
directory. Add `--permissions bypass` only if the task clearly needs
something outside Read/Edit/Write/Bash/Glob/Grep (see **Permissions**
above). Report the command's output back to the user as-is — don't
paraphrase the scheduled time or unit name.

The user never types Python themselves in this flow — Claude runs it as a
tool call on their behalf.

**Instruction for Claude when the user asks to resume / catch up** ("what did
the scheduled task do?", "resume where we left off", `/claude-nextsession
resume`): run `python3 postpone.py --resume` from this skill's directory. It
reports on the project of the *current* working directory, which is almost
always what the user means. Only add `--global` if they explicitly ask about
another project or the scoped lookup came back empty. Then read the
**Next steps** section and continue that work — the report ends with a
`claude --resume <session-id>` line if the user wants the original
transcript instead.

### Direct CLI (no Claude Code session involved — cron, scripting, testing)
```bash
# Basic usage — reads the reset time from the local cache
python3 postpone.py --instructions "Your instructions here"

# Run in a specific project directory
python3 postpone.py -i "Check system" -w /path/to/project

# Dry run (test without scheduling)
python3 postpone.py -i "Check system" --dry-run

# Override the detected reset time (for testing)
python3 postpone.py -i "Test" -t "2026-07-26T15:30:00Z"

# Catch up on this project's most recent report
python3 postpone.py --resume

# ...or the most recent report from any project
python3 postpone.py --resume --global
```

## Setup

No dependencies beyond Python 3's standard library, and no configuration —
there is no API key to set. Scheduling uses `systemd-run --user`, which is
already available on any machine with a systemd user session (check with
`systemctl --user status`).

## Requirements
- Python 3.10+ (standard library only)
- `systemd-run` + a working systemd user session (`systemctl --user`)
- `claude` CLI available in `$PATH` at execution time
- Read/write access to `/tmp/` for the generated script and its log
- Read access to `~/.claude/cache/rate-limits.json`

## Files
- `postpone.py` — main script
- `report.py` — builds and reads execution reports (see below)
- `templates/delayed_task.sh` — template for the scheduled task; invokes
  `claude -p "$INSTRUCTIONS" --output-format json` in the captured working
  directory and logs output to `/tmp/claudepostpone_<timestamp>.log`
- `~/.claude/statusline-command.sh` — extended (outside this directory) to
  write the rate-limit cache this skill depends on

## Reports

Every run — success, failure, or crash — writes a report to
`~/.claude/cache/claude-nextsession/reports/<id>/` (outside this repo, since
it's public and reports can contain private task content). Each report has:

- `summary.md` — leads with a **Next steps** section, then status (`SUCCESS`
  / `PARTIAL (N denied)` / `FAILED` / `CRASHED` / `UNKNOWN`), timestamps,
  cost, turns, the instructions, Claude's final result text, any permission
  denials, a `git diff --stat` of what changed in the workdir (if it's a git
  repo), and a **Resume** line.
- `report.json` — the full `claude -p --output-format json` output.
- `diff.patch` — the full `git diff HEAD` (if the workdir is a git repo).

```bash
# print this project's most recent report — the intended way to catch up
# after starting a new session
python3 postpone.py --resume

# same, but ignore project scoping
python3 postpone.py --resume --global
```

**Reports are scoped to the project you run this from.** Several postponed
tasks in different repos all fire at the same reset, so an unscoped "most
recent report" is usually the wrong one. Lookup canonicalizes the working
directory to its git toplevel and matches on that; `--last-report` is kept
as an alias for `--resume`.

### Next steps and Resume

Two things make a report enough to actually restart from:

- **Next steps** — every scheduled instruction gets a short epilogue appended
  (`HANDOFF_EPILOGUE` in `postpone.py`) asking the run to close with a
  `## NEXT STEPS` section: what it completed, what it didn't and why, what
  should happen next. That section is lifted to the top of `summary.md`. If
  the run omits it, the report is built without it.
- **Resume** — `claude -p --output-format json` returns the `session_id` of
  the headless run. The report ends with
  `cd <workdir> && claude --resume <session_id>`, which reopens that exact
  session with its full transcript — no session picker involved.

Status meanings: `SUCCESS` = ran clean, nothing denied. `PARTIAL (N
denied)` = Claude worked around N denied tool calls (e.g. `--permissions
scoped` blocking something) — check what still got done. `FAILED` = Claude
itself reported an error (`is_error: true`). `CRASHED` = the wrapper script
never got a result from `claude` at all (not found, bad workdir, non-zero
exit before JSON was produced).

## Inspecting a scheduled task
```bash
# job is a systemd-run transient unit; check it directly
systemctl --user status claudepostpone-<timestamp>-<pid>
journalctl --user -u claudepostpone-<timestamp>-<pid>

# or just tail the log the script itself writes
tail -f /tmp/claudepostpone_*.log

# or the structured report, once it's done
python3 postpone.py --resume
```

## Example
```bash
python3 postpone.py --instructions "Check system health and report issues"

# Output:
# Task scheduled successfully
#   Scheduled for: 2026-07-26T12:00:00+00:00
#   systemd unit:  claudepostpone-20260726120000-12345
#   Script:        /tmp/claudepostpone/claudepostpone_20260726_090512.sh
#   Check later:   journalctl --user -u claudepostpone-20260726120000-12345
```
