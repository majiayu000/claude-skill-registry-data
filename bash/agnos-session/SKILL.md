---
name: agnos-session
description: "AGNOS process session-state skill. A script writes agnos-process/_sessionstate/session.yaml (trigram, tests, platform), prints it, and appends the session's friction-metrics row to METRICS_LOG.md, so that the agent never writes these files itself. USE FOR: START SESSION step 3 ('init'), reloading the session variables before a Tier M or L task ('show'), END SESSION step 2 ('close')."
argument-hint: "init --tri <TRI> --tests <true|false> | show | close <questions> <recoveries> <re-tiered> <verification>"
---

<!-- RQ-INI-011 to RQ-INI-015, RQ-INI-018 / ADR-INI-002 (DEC-INI-008 to DEC-INI-011) -->
# AGNOS Session

A script does all the writing: never write or edit `agnos-process/_sessionstate/session.yaml` or the rows of
`agnos-process/_sessionstate/METRICS_LOG.md` yourself. `<skill-folder>` is the folder holding this file; run every
command from the project's root. <!-- RQ-PLG-005 -->

## Script Selection

The script cannot be chosen from `session.platform`, which it writes. <!-- DEC-INI-008 -->

1. Run `powershell -NoProfile -File <skill-folder>/scripts/session.ps1 <sub-command> <arguments>`.
2. Only if the `powershell` command is not found, run `bash <skill-folder>/scripts/session.sh <sub-command> <arguments>`.

Use `powershell`, never `pwsh`. Both versions take the same arguments and give the same bytes.

## Sub-Commands

| Sub-command | When | What it does |
|---|---|---|
| `init --tri <TRI> --tests <true\|false>` | START SESSION step 3, once the user gave the trigram and answered the tests question | Detects the platform, rewrites `session.yaml` whole with `tri`, `tests` and `platform`, prints the table |
| `show` | Before a Tier M or L task, when the session variables are not in context | Prints `tri=<v> tests=<v> platform=<v>` on one line |
| `close <questions> <recoveries> <re-tiered> <verification>` | END SESSION step 2, with the 4 counters of the summary's metrics table | Appends `\| <date> \| <TRI> \| <q> \| <r> \| <t> \| <v> \|` to `METRICS_LOG.md`, creating it with its header if absent, prints the row |

- Both arguments of `init` are required; the trigram is three uppercase letters, stored as given, whatever the branch.
- To change a value the user overrides, call `init` again with all the values: the file is never completed.
- `close` reads the trigram from `session.yaml`; each counter is a non-negative integer.

## Exit Code

- `0`: done. Show the user what the script printed.
- `1`: error, nothing written. Report the message on the error stream; for a missing or invalid argument, ask the user
  for the value, then call again. If the platform is refused or `agnos-process/` is missing, apply the Error Recovery Protocol.

## Layout

| Path | Role |
|---|---|
| `scripts/session.ps1`, `scripts/session.sh` | The two versions, giving the same bytes |
| `scripts/agnos-layout.ps1`, `scripts/agnos-layout.sh` | The process folder's paths, generated from `agnos-init`'s `layout.json`, never edited by hand |
| `tests/test_session.py` | Runs both versions on the same cases |
