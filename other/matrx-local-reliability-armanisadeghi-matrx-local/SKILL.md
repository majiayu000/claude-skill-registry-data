---
name: matrx-local-reliability
type: Skill
title: "matrx-local-reliability — the installed-app repair loop"
description: "The repair loop for the installed Matrx Local desktop app: run scripts/reliability.py, then fix every issue its README lists until it is verified on the installed build. Use when woken by the Matrx Local reliability schedule, when asked what is broken in Matrx Local, to fix errors or warnings in its logs, or to verify a Matrx Local fix landed. NOT for release or install (the release watch owns those)."
tags: [matrx-local, reliability, errors, repair, scheduled]
timestamp: 2026-09-30T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/matrx-local-reliability/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# matrx-local-reliability

The script does every mechanical step. You do the one thing a script cannot: find the cause and fix the class.

**One file to read:** `matrx-local/_reliability/README.md`. The script rewrites it from the installed app's own evidence: `~/Library/Logs/MatrxLocal/*.log`, `~/.matrx/diagnostics/*.json`, the local database's failure tables, `GET /health` on port 22140, the installed bundle version and the release tags. Every failure signature becomes one stable issue `MXL-R-nnn` that is counted across builds. A log line is never an issue; an issue is a cause.

```
python3 scripts/reliability.py scan            # rewrite README + ledger from live evidence (read-only, ~4 s); exit 1 while an agent has work
python3 scripts/reliability.py status          # the same two lines and exit code without rescanning
python3 scripts/reliability.py claim ID --owner "<your session or name>"
python3 scripts/reliability.py fix ID --commit <sha>          # after the repairing commit exists locally
python3 scripts/reliability.py ignore ID --reason "..."       # expected state / external / duplicate of ID
python3 scripts/reliability.py arman ID --question "..."      # a genuine human-only decision, one sentence
python3 scripts/reliability.py note ID "..."
python3 scripts/reliability.py reopen ID
```

Every command commits `_reliability/` by itself (pathspec-only, `reliability: ...`), so the shared checkout never carries it dirty and the sync ships it; every agent on every machine sees the same ledger. `~/.matrx/reliability/latest.json` is the last scan.

**This skill wins over the repo's older release lines.** `CLAUDE.md § Release: you run it` predates the sync; on a reliability wake you commit locally by pathspec and never run `release.sh`, never push, never install. The `ship-all` sweep pushes and releases; the app's auto-updater installs.

## The loop, every time you wake

1. **Scan.** `python3 scripts/reliability.py scan` from the repo root. Read `_reliability/README.md` top to bottom.
2. **PROBLEMS first.** Each line names its own fix path:
   - *installed app is N releases behind* → the app's auto-updater (`desktop/src/hooks/use-auto-update.ts`, `lib.rs` updater) or the release watch's install step failed. Read `lifecycle.log` `[update]` lines, `~/.codex/automations/matrx-local-release-watch/memory.md` and `~/.matrx/ship-all/latest.json`; fix the class in source. Never install by hand and never restart his app.
   - *engine not reachable* → discovery or startup is broken on the installed build. Diagnose from `lifecycle.log`, `engine-stderr.log`, the newest `~/.matrx/diagnostics/*.json`. Fix the class in source.
   - *failed services* / *outbox without identity* → a code defect; treat like an open error.
3. **Regressed, then Open errors by count, then warnings above threshold.** For each: `claim` it, then follow the `diagnose` skill (proven cause, siblings, guard shown failing then passing per `forcing-function-tests`), fix the class in source, run the checks `.matrx/LANDING_CHECKLIST.md` names for the files you touched, commit locally by pathspec, then `fix ID --commit <sha>`. **Runtime proof:** a change to a server-facing, startup, sync or lifecycle path gets one real run on a dev engine before `fix` is recorded, unless the guard itself exercises the real boundary (a live probe against the real server counts; a fake client does not). If `./scripts/dev.sh` refuses to start because a `~/.matrx-dev` cache link escapes the dev home, run it with `--fresh`; that refusal is the isolation guard working, not a blocker. Adjacent issues with the same timestamp and component are usually one cause; fix once and record the same commit on each.
4. **Leave Claimed alone** when the owner is not you, unless it has no note for 24 hours: then reopen and take it.
5. **Ignore only with a real reason**: an expected state (a gated model the user has not authorized, a permission the user declined), an external outage, or a duplicate of another issue. "Noisy" is not a reason; a noisy warning gets its rate fixed at the producer.
6. **Needs Arman** is for decisions only a human can make. One plain sentence a stranger could answer in seconds. Never for "should I fix this".
7. **Rescan, then `status`.** You are done when it exits 0, or when every remaining item is Fixed-awaiting-install, Installed-verifying, or Needs Arman with its question written.

## What you may and may not touch

- **His installed app is his.** `/Applications/AI Matrx.app` and port 22140: never sign in, sign out, click, restart, update, or edit `~/.matrx`, its database, discovery files, permissions or settings. Read it only through GETs with `Authorization: Bearer local-probe` and by reading its files.
- **Reproduce on a source engine you start** (`./scripts/dev.sh`, home `~/.matrx-dev`, ports 22240–22259) signed in as the shared admin test account (`AI_ADMIN_USERNAME` / `AI_ADMIN_PASSWORD` in the `aidream` or `matrx-frontend` `.env`). Startup, lifecycle and packaging changes get `./scripts/smoke.sh` as `docs/TESTING_LADDER.md` says.
- **Release and install are not yours.** Commit locally by pathspec; the sync pushes and the release watch ships and installs. A fix is "installed" when the ledger says the installed build contains it, and "verified" after 24 hours of silence on that build. Do not report deployment status to Arman.
- **Never suppress to win.** Lowering a log level, sampling, disabling a feature or a retry earns nothing; the ledger counts the failed operation, not the line.

## Completion rule

Inspection is not completion. A diagnosis, a list, or a status report is not completion. If a blocker can be removed by you or by a subagent you dispatch, it is not a blocker; remove it and continue. Only a decision that genuinely needs a human stops an item, and then it stops only that item, written under Needs Arman. Your job is not done until `status` exits 0 or every remaining line is awaiting install, verifying, or a written human question. Do not end with "next steps".

## Report

Only when something changed. Plain English, in this order: what was broken and what you fixed (issue, cause in one sentence, commit); what is fixed and waiting for the release watch; what became verified; what needs Arman, as the question itself. Numbers only where they change what he does. No paths, hashes, or task IDs in the message to him.

## Knobs (environment, defaults in the script)

`MATRX_RELIABILITY_WARNING_THRESHOLD=20` per window · `MATRX_RELIABILITY_VERIFY_HOURS=24` · `MATRX_RELIABILITY_INSTALL_LAG=2` releases · `MATRX_RELIABILITY_FIX_LAG_HOURS=3`. The wake prompt is `wake-prompt.md` beside this file.
