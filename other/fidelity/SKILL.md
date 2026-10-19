---
name: fidelity
description: Use when the user runs /fidelity. Computes the plan-fidelity rate — what fraction of /mandos verdicts came back Faithful, and the Missing-vs-Scope-crept Blocker split that explains the rest — from the recorded /mandos history, renders a Henneth dashboard, and prints its URL. Read-only over the recorded history; never writes to a tracker or repo. The rate only fills in as /mandos runs — it is not backfilled from past sessions.
purpose: Computes the plan-fidelity rate from recorded plan-faithfulness verdicts.
user_invocable: true
stage: watch
composes: henneth:dispatch, mandos:companion
---

# Fidelity — The Plan-Fidelity Rate

Where `/este` asks whether the config's rules and skills were *followed*, `/fidelity` asks whether the *plans they governed* turned into matching code. Every `/mandos` verdict — Covered / Missing / Scope-crept — is recorded as it renders; this skill reduces that record into one standing rate, split by which way the drift ran.

## Run

    python3 ~/.claude/hooks/fidelity-scan.py

This reads `~/.skadi/mandos/history.jsonl` (read-only — written by `mandos-record.sh` as a side effect of `/mandos`), writes the board channel `~/.skadi/board/fidelity.json`, and renders `~/.skadi/henneth/plan-fidelity.html`. It prints the headline Faithful rate.

Then ensure the Henneth window is up (boot it with `/henneth` if not) and surface the dashboard URL inline — the page follows the folder, so the dashboard appears on its own once rendered.

## Notes

- **Read-only.** The scan reads the recorded history; it never writes to a tracker or repo.
- **Sourced from `/mandos`, not transcripts.** Unlike `/este`'s marker scan, this rate has no signal until `/mandos` has actually been run a few times — an unused history reads `total: 0` and the dashboard says so plainly, rather than guessing.
- **Blocker split localizes the leak.** `missingBlockers` (execution came up short of the plan) and `scopeBlockers` (execution went beyond the plan) are counted separately — only Blocker-severity items gate a `/mandos` tier, so they are what actually explains why the rate isn't higher.
- **Standing cadence.** The skill arms nothing. For a recurring read, wrap it: `/loop 6h /fidelity`, or a cron.
- **Tests ride beside the hook** — `fidelity-scan.test.sh` runs offline via injected fixture history (`MANDOS_HISTORY_DIR`).
