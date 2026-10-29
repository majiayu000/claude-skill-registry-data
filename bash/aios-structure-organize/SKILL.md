---
name: aios-structure-organize
description: "Additively repair an existing AIS-OS project by creating whatever's missing against the frozen starter-kit baseline -- never overwrites, deletes, or moves anything that already exists. User-invoked only through /aios-structure-organize."
disable-model-invocation: true
allowed-tools: Bash(powershell -NoProfile -ExecutionPolicy Bypass -File *)
---

## What this skill does

Scans the current working directory, compares it against the exact frozen AIS-OS starter-kit baseline bundled inside this skill's own folder, shows a dry-run plan of exactly what's missing, waits for explicit confirmation, then creates only those missing items. This is the highest-risk skill in the `aios-structure-*` family because it's the only one that writes to an existing, already-in-use project -- so it only ever runs when the user explicitly types `/aios-structure-organize`. It does not auto-trigger from natural language and is not invoked programmatically by Claude on its own initiative -- `disable-model-invocation: true` enforces this.

## The additive-only boundary -- the single most important guarantee of this skill

Organize may only ever **create things that don't exist yet.** It will:

- Create missing baseline directories.
- Restore missing structural files by copying this skill's bundled frozen template.
- Create missing content-mutable files (`CLAUDE.md`, `aios-intake.md`, `connections.md`, `decisions/log.md`) using the blank/unfilled template -- but only if the file is absent entirely.
- Create missing placeholder files as zero bytes.

It will **never**, under any circumstance including error paths:
- Overwrite an existing file's content, even if that content has drifted from the frozen baseline.
- Delete anything.
- Move or rename anything that already exists.
- Touch a recognized anti-pattern item (`notes/`, `misc/`, `tmp/`, `inbox/`, a duplicate `decisions.md`).

Structural drift and anti-pattern items are strictly out of scope. If found, they're mentioned in the report -- never acted on. That's `aios-structure-validate`'s job to report in detail; a human decides what to do about them.

## Not the same as /audit or aios-structure-validate

- **`/audit`** -- broad Four-Cs maturity score, unrelated to this skill.
- **`aios-structure-validate`** -- read-only, reports everything including drift and anti-patterns, never writes (except an optional consented report file).
- **`aios-structure-organize`** (this skill) -- writes, but only ever adds what's missing. Narrower and safer than validate's full issue set by design.

## Portability

Same contract as its siblings: this exact folder works installed personally (`~/.claude/skills/aios-structure-organize/`) or project-locally (`<project>/.claude/skills/aios-structure-organize/`), with no changes. All paths resolve relative to this skill's own script location or to the current working directory -- never a fixed username, drive letter, or dependency on any specific repo or on sibling skills being installed.

## Execution

1. Run the bundled scanner from the current working directory, without `-Apply` first:
   ```
   powershell -NoProfile -ExecutionPolicy Bypass -File "<this skill's folder>\scripts\organize.ps1"
   ```
   Resolve `<this skill's folder>` from the base directory Claude Code reports for this skill at invocation -- never hardcode a path.

2. Relay the script's console output to the user as-is.

3. Check the process exit code:
   - **`0`** -- either the project already fully conforms (nothing to create), or (only possible after step 5 below) the apply run succeeded. Relay plainly.
   - **`1`** -- a dry-run plan was generated; there are missing items. Proceed to step 4.
   - **`2`** -- not an AIS-OS project. Relay the redirect message plainly. Do not proceed further.
   - **`10`** -- this skill's own bundled package is corrupt (preflight failure). Report this as a problem with the skill installation itself, not with the target project.
   - **`30`** or **`31`** -- (only possible after step 5) the apply run failed. Relay the FAIL and rollback lines plainly. Never describe this as a success.

4. If the exit code was `1`, ask the user via `AskUserQuestion` to confirm: "Create the missing items listed above?" -- options **Yes, create the missing items (Recommended)** / **No, don't create anything**. If the answer is anything other than yes, stop here -- do not proceed to step 5.

5. Only on explicit yes, re-run the same command with `-Apply` appended. Relay its output the same way. This is the only point in the entire skill where anything is written.

## What the script guarantees (for context, not to be re-implemented here)

- Preflight: every one of this skill's 14 bundled templates is present, readable, and its normalized SHA-256 matches `manifest.json` before any scan runs.
- Non-AIS-OS detection: same 7-file heuristic as `aios-structure-validate`.
- The scan only ever determines what's *missing* -- it never hash-compares existing files, since organize never acts on drift regardless of what it would find.
- A directory or file that already exists is never touched, full stop, even if it's technically a reparse point or otherwise unusual -- existence alone is enough to leave it alone. The one exception: if an *expected-missing* directory turns out to occupy a reparse point, organize refuses to create through/over it and reports it as blocked rather than silently writing into it.
- Apply-run failures track every path created during that specific run and roll back only those paths, deepest-first for directories, never touching anything that pre-dated this run.

## Notes -- what this skill must NOT do

- Never invoke this outside an explicit `/aios-structure-organize` command.
- Never skip the dry-run -> confirmation -> `-Apply` sequence, in that order, for any reason.
- Never overwrite, delete, move, or rename anything that already exists in the target project.
- Never fix structural drift or remove anti-pattern items -- mention only.
- Never touch git.
- Never write anything beyond the missing baseline items themselves -- no logs, backups, or extra files in the target project.
- Never register itself by editing the target project's `CLAUDE.md` or `decisions/log.md` -- if those files are among the missing items, the frozen unfilled templates are created as-is; if they already exist, they are never touched.
- Never hardcode this repo's path, or any other machine-specific path, anywhere in this skill.

## Clickable-question convention

This skill has exactly one user-facing question -- the Step 4 apply confirmation -- which already used `AskUserQuestion`; made its second option explicit (was previously implied only by "anything other than yes"). No other question points exist; everything else is deterministic script output relayed as-is.
