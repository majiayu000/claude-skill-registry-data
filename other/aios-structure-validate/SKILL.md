---
name: aios-structure-validate
description: "Read-only structural check of an existing AIS-OS project against the frozen starter-kit baseline (missing/drifted/malformed items, not a maturity score -- see /audit for that). User-invoked only through /aios-structure-validate."
disable-model-invocation: true
allowed-tools: Bash(powershell -NoProfile -ExecutionPolicy Bypass -File *)
---

## What this skill does

Scans the current working directory and compares it against the exact, frozen default AIS-OS starter-kit baseline bundled inside this skill's own folder. Reports what's missing, what structural content has drifted, which placeholder files aren't empty, and any recognized anti-pattern clutter -- each with a concrete manual fix. It never modifies the scanned project except one optional, explicitly-consented report file.

This skill only ever runs when the user explicitly types `/aios-structure-validate`. It does not auto-trigger from natural language and is not invoked programmatically by Claude on its own initiative -- `disable-model-invocation: true` enforces this, for consistency with its sibling `aios-structure-build` even though this skill has no write risk.

## Not the same as /audit

This repo may also have an `/audit` skill installed. They answer different questions:

- **`/audit`** -- "is this AIOS mature and well-connected?" A broad Four-Cs score out of 100 (Context/Connections/Capabilities/Cadence).
- **`aios-structure-validate`** -- "does this project's file tree literally match the frozen AIS-OS baseline?" A narrow, structural pass/fail per item. No score. Two unrelated tools -- don't conflate them or their triggers.

## Portability

Same contract as `aios-structure-build`: this exact folder works installed personally (`~/.claude/skills/aios-structure-validate/`) or project-locally (`<project>/.claude/skills/aios-structure-validate/`), with no changes. All paths resolve relative to this skill's own script location or to the current working directory -- never a fixed username, drive letter, or dependency on any specific repo or on sibling skills being installed.

## Execution

1. Run the bundled scanner from the current working directory, without the save flag first:
   ```
   powershell -NoProfile -ExecutionPolicy Bypass -File "<this skill's folder>\scripts\validate.ps1"
   ```
   Resolve `<this skill's folder>` from the base directory Claude Code reports for this skill at invocation -- never hardcode a path.

2. Relay the script's console output to the user as-is.

3. Check the process exit code:
   - **`0`** -- scan completed, project fully conforms. Relay the PASS message plainly.
   - **`1`** -- scan completed, issues found. Relay the categorized report plainly (Missing / Structural Drift / Non-Empty Placeholders / Unrecognized Items, each with its fix line). Do not add your own summary that contradicts or duplicates it.
   - **`2`** -- not an AIS-OS project. Relay the redirect message plainly. Do not proceed further.
   - **`10`** -- this skill's own bundled package is corrupt (preflight failure). Report this as a problem with the skill installation itself, not with the scanned project.
   - **`20`** -- an unexpected error occurred during the scan. Relay the FAIL message plainly. Do not describe the run as successful.

4. Only if the exit code was `0` or `1` (a real scan actually completed), ask the user via `AskUserQuestion`: "Save this validation report to `validations/validate-{date}.md`?" -- options **Yes, save it (Recommended)** / **No, don't save**.
   - If yes, re-run the same command with `-SaveReport` appended, then relay the `REPORT_SAVED: <path>` line the script prints. The script itself guarantees this never overwrites an existing report -- it appends a numbered suffix (`-2`, `-3`, ...) if a same-day report already exists.
   - If no (or exit code was `2` or `10`), do nothing further.

## What the script guarantees (for context, not to be re-implemented here)

- Preflight: every one of this skill's 14 bundled templates is present, readable, and its normalized SHA-256 matches `manifest.json` before any scan runs.
- Non-AIS-OS detection: if none of 7 distinctive AIS-OS files exist in the target, the scan stops immediately with a redirect message -- no noisy "everything is missing" report.
- Three-tier content policy: content-mutable files (`CLAUDE.md`, `aios-intake.md`, `connections.md`, `decisions/log.md`) are checked for presence only, never content -- their being filled in by `/onboard` is expected and never flagged. Structural files are hash-compared exactly. Placeholder files (`archives/.gitkeep`, `context/.gitkeep`) must exist and be exactly zero bytes.
- Sanctioned growth (anything from `EXPANSIONS.md`, extra or sibling skills) is never flagged. Only the specific named anti-patterns (`notes/`, `misc/`, `tmp/`, `inbox/`, a duplicate top-level `decisions.md`) are ever reported as unrecognized.
- The only possible write in the entire skill is the optional saved report, and only when `-SaveReport` is explicitly passed after user consent -- collision-safe by construction (date-based name, numbered suffix on conflict, never overwrites).

## Notes -- what this skill must NOT do

- Never invoke this outside an explicit `/aios-structure-validate` command.
- Never write anything to the scanned project except the optional report file, and only after explicit user consent each time.
- Never flag content-mutable file content changes -- that's expected, healthy project state, not an issue.
- Never flag EXPANSIONS.md-sanctioned growth folders or extra/sibling skill folders as unrecognized.
- Never deep-recurse into `node_modules/`, `.git/`, or the internal contents of growth folders.
- Never hardcode this repo's path, or any other machine-specific path, anywhere in this skill.
- Never register itself by editing the scanned project's `CLAUDE.md` or `decisions/log.md` -- this skill only reads and, optionally, writes one report file under `validations/`.

## Clickable-question convention

This skill has exactly one user-facing question -- the Step 4 save-report confirmation -- which already used `AskUserQuestion`; made its second option explicit (was previously implied only by "if no"). No other question points exist; everything else is deterministic script output relayed as-is.
