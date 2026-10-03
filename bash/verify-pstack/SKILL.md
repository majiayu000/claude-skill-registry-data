---
name: verify-pstack
description: Drive the pstack agent harness the way a session experiences it and prove its behaviors with evidence. Use for /verify-pstack, after editing anything under poteto-mode or its hook, or when a session seems to have lost poteto mode.
---

# Verify pstack

pstack's surface is what a Claude Code session receives from `poteto-mode/hooks/pstack-hook.mjs` and the skills. Proof means starting real headless sessions and reading what landed in their transcripts. The judge reads the transcripts itself, but it shares the gate's read counting, skip parsing and data-shape pattern from `rules.mjs` and `toAction` and `SOURCE_FILE` from `trace.mjs`, so a bug there can pass both. The mutation fixtures in `scripts/judge.test.js` guard that shared code.

`~/.claude/skills` links into one checkout, and a headless session run from anywhere sees that checkout's files. To verify a branch, check it out in the checkout the link serves. The Doctor prints which checkout that is.

## Launch

Nothing to start. A drive spawns its own sessions, and they exit when their turn ends.

## Doctor

Answers "is this install worth driving?" in under a minute. Run from the repo root.

```
node skills/verify-pstack/scripts/doctor.mjs
node skills/poteto-mode/scripts/check-port.mjs skills agents
node --test $(git ls-files '*.test.js')
node scripts/drift.mjs --check
```

`doctor.mjs` checks that `~/.claude/settings.json` carries each hook registration in `install.json` exactly, carries its `env` keys, links each agent (`pstack-reader` among them) into the served checkout, and that `~/.claude/pstack/hook-errors.log` is absent or empty. Every line must read `ok`. The other three print `0 findings`, all tests `ok`, and `DRIFT.md is current`. Fix anything else before driving.

## Drive

```
bash skills/verify-pstack/scripts/drive.sh
```

`drive.sh --settings <file>` adds `<file>` to every session's settings, so a branch's hook registrations run without parking the live checkout, beside the live hooks the user settings still load.

It runs three headless sessions in parallel, in about two minutes:

- **mode** (opus). `/poteto-mode <task>` piped on stdin, where the task is a one-line bug in a seeded scratch repo. Nothing names a playbook.
- **control** (haiku). One prompt, no slash command.
- **reader** (haiku). Spawns a haiku `pstack-reader` and tells it to run `echo x > <scratch>/f`.

`scripts/judge.mjs` then prints one verdict per file in `features/`: hook-context, mode-reminder, step-ledger, gate, action-gate, reader, task-tools. The drive adds port-clean. Each feature file says what its verdict asserts and which session it reads.

## Evidence

Everything lands under `pstack-verify/<UTC timestamp>/` in the temp directory, `$TEMP` on Windows and `${TMPDIR:-/tmp}` on macOS and Linux: each session's stream (`<role>.stream.jsonl`) and transcript (`<role>.jsonl`), the reader's subagent transcripts, the mode session's final reply, the port-clean outputs, and `verdicts.txt`. Each verdict names the file and line that prove it. A verdict is VERIFIED, NOT VERIFIED, or INCONCLUSIVE, and INCONCLUSIVE is not a pass. The script exits 1 unless every verdict is VERIFIED.

Each session runs under a 540 s deadline, through `timeout` or `gtimeout` where one is installed and `scripts/deadline.mjs` otherwise. A session that hits it leaves `<role>.timeout` holding the seconds, and the judge reports every feature read from that session as `INCONCLUSIVE <feature> <role> session timed out after <n> s` instead of judging its partial transcript. Any other non-zero exit is recorded in `<role>.exit`.

## Cleanup

The three seeded working directories live under `~/.claude/pstack/verify/`, one per role, named `pstack-verify-<timestamp>-<role>`. They sit outside the temp directory because the action gate treats anything under it as scratch, and a scratch edit never meets the design ask.

`drive.sh --clean <timestamp>` removes that drive's three scratch directories under `~/.claude/pstack/verify/` and the three project directories under `~/.claude/projects/` whose names end in `-pstack-verify-<timestamp>-mode`, `-control` and `-reader`. The evidence directory and the rest of `~/.claude/pstack/` stay.

## Helpers

- `scripts/doctor.mjs` checks the install.
- `scripts/drive.sh` runs the sessions and the port checks.
- `scripts/deadline.mjs <seconds> <command>...` runs a command under a deadline where no `timeout` exists, kills its process tree when it runs late, and exits 124.
- `scripts/judge.mjs <evidence dir>` prints the session verdicts, so a saved drive can be judged again.
