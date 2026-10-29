---
name: aios-structure-build
description: "Scaffold and verify the frozen AIS-OS starter-kit baseline in an empty target directory. User-invoked only through /aios-structure-build."
disable-model-invocation: true
allowed-tools: Bash(powershell -NoProfile -ExecutionPolicy Bypass -File *)
---

## What this skill does

Scaffolds the exact, frozen default AIS-OS starter-kit folder structure into the current working directory, then cryptographically verifies the result before reporting success. It is a portable, self-contained builder: all template content and the verification manifest ship inside this skill's own folder, never read from any other project.

This skill only ever runs when the user explicitly types `/aios-structure-build`. It does not auto-trigger from natural language, and it is not invoked programmatically by Claude on its own initiative — `disable-model-invocation: true` enforces this.

## Portability

This exact folder can be installed in either location with no changes:

- **Personal:** `~/.claude/skills/aios-structure-build/`
- **Project-local:** `<project>/.claude/skills/aios-structure-build/`

All paths the skill uses are resolved relative to its own script location or to the current working directory at invocation — never a fixed username, drive letter, or a path back to any specific original repository. The skill has no dependency on Claude's memory, no network dependency, and does not require `aios-structure-validate` or `aios-structure-organize` to be installed — those two are referenced only as suggestions in abort messages when a target isn't empty.

## Execution

1. Run the bundled builder script from the current working directory:
   ```
   powershell -NoProfile -ExecutionPolicy Bypass -File "<this skill's folder>\scripts\build.ps1"
   ```
   Resolve `<this skill's folder>` from the base directory Claude Code reports for this skill at invocation — never hardcode a path.

2. Relay the script's console output to the user as-is.

3. Check the process exit code:
   - **`0`** — success. The script's own output already lists what was created, what was preserved, and confirms verification passed. Do not add anything that contradicts or duplicates that report.
   - **any non-zero code** — failure. Relay the script's failure output plainly. Do not describe the run as successful, partially successful, or "mostly done." A non-zero exit is a hard failure regardless of how much output preceded it.

## What the script guarantees (for context, not to be re-implemented here)

- Preflight: every bundled template is present, readable, and its CRLF/CR-normalized SHA-256 matches `manifest.json` before anything is touched.
- Target check: the current directory must be empty, except it tolerates pre-existing `.claude/skills/aios-structure-build/`, `.claude/skills/aios-structure-validate/`, and `.claude/skills/aios-structure-organize/` (nothing else). Any other existing item aborts with zero changes.
- Write: creates the baseline tree from the bundled templates, copying file bytes verbatim (hash normalization is for comparison only and never alters what's written).
- Rollback: if any write or verification step fails, only paths created during that attempt are removed. Nothing that existed beforehand is touched, including preserved skill folders.
- Post-build verification: recomputes every file's normalized hash and confirms no unexpected paths exist before the script reports success.

## Notes — what this skill must NOT do

- Never invoke this outside an explicit `/aios-structure-build` command.
- Never write anything to the target beyond what `build.ps1` produces. No extra reports, logs, backups, or manifests written into the scaffolded project — those live only inside this skill's own package.
- **Never register this skill by editing the target's `CLAUDE.md` or `decisions/log.md` after scaffolding.** Both are part of the frozen, hash-verified baseline content and must remain byte-identical to the bundled templates. Do not append an "Active Skills" entry, a decision log entry, or any other note to files inside the newly scaffolded project. (This intentionally departs from the general skill-authoring convention of registering new skills in the target project — that convention does not apply here, because the target project isn't this skill's own home and its files are verification-frozen.)
- Never touch git in the target directory.
- Never attempt to build `aios-structure-validate` or `aios-structure-organize` behavior — this skill only builds a fresh, empty-directory baseline.

## Clickable-question convention

Not applicable. This skill is entirely non-interactive: the user explicitly invokes `/aios-structure-build`, the bundled script runs to completion deterministically, and Claude only relays its console output and exit code. There is no point where the skill asks the user anything, so there is no question to convert.
