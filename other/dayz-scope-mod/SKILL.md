---
name: dayz-scope-mod
description: "Restricts edits to one mod under workspace/<ModName>/ by adding Edit deny rules for every other mod's workspace, P:\\ and deploy folders; reads stay broad. Use when a session or subagent should work on a single mod, or to lift that scope again."
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-scope-mod

Scope the agent to a single DayZ mod. While scoped, the agent can read anywhere but cannot Edit or Write to any other mod's source, P:\ junction, or workshop deploy dir. Designed for sessions where you're iterating on one mod and don't want a wrong-instinct call to land in a sibling mod.

Follow `skills/_shared/dayz-conventions.md`.

## How to run

```cmd
:: Scope to a specific mod
python "<skill-dir>\scope.py" <ModName>

:: Show current scope (or "no active scope")
python "<skill-dir>\scope.py" --status

:: Lift the scope
python "<skill-dir>\scope.py" --clear
```

The project is found the same way `/dayz-init` finds it: `CLAUDE_PROJECT_DIR` when set, else the nearest folder at or above the current folder that holds `.claude\local-memory\dayz-current-project.txt`, else the clone that holds the skill scripts when that clone has the cache, else the current folder. So a run from `workspace\<ModName>\` still uses the project's `workspace\` and settings.

## What it does

1. Validates `<ModName>` exists at `workspace/<ModName>/`, matching the folder name case-insensitively and then using the folder's on-disk spelling in every rule, in the output and in the recorded scope (refuses unknown names, and names that permission rules would read as pattern syntax: `*`, `?` or `[` anywhere, or a leading `!` or `#`; `!` and `#` mid-name are fine because gitignore syntax treats them specially only at the start of a pattern).
2. Enumerates sibling mods under `workspace/`: every other non-dotted folder that has `config.cpp` or `$PBOPREFIX$` at its root (`/dayz-new-mod` writes both). Other folders, such as `workspace/_archive/`, get no deny rules, are named on an `[INFO]` line, and their names are not checked. The scope guard hook is stricter: it treats every other folder as a mod unless its name starts with `_`, so a folder like `workspace/_archive/` stays writable while `workspace/Scratch/` does not. Refuses if a sibling mod's name breaks the same rule as in step 1. The active mod itself only has to be a non-dotted folder under `workspace/`, so a mod still being set up can be scoped.
3. Reads `.claude/local-memory/dayz-active-scope.json` and `.claude/settings.local.json`, and removes any rules a previous run recorded (idempotent re-run). If either file is unreadable or has the wrong shape (the scope record must hold a `denied_rules` list; the settings must be an object whose `permissions.deny` is a list), it exits 1 with nothing changed. A corrupt scope record is never treated as "no scope", because the rules it recorded may still be in the settings; the message tells you to remove them by hand and delete the record.
4. For each sibling mod, appends deny rules to `permissions.deny`:
   - `Edit(/workspace/<other>/**)` (a leading `/` anchors at Claude Code's primary working directory, so start Claude Code from the project root)
   - `Edit(//p/<other>/**)` (`//` is absolute; Claude Code normalizes `P:\` to `/p/` before matching)
   - `Edit(//p/Mods/@<other>/**)`
   - `Edit(//<drive>/<DayZ game>/!Workshop/@<other>/**)`, the real folder behind the `P:\Mods` junction, e.g. `Edit(//c/Program Files (x86)/Steam/steamapps/common/DayZ/!Workshop/@OtherMod/**)`. The game is located with `find_dayz_game()` from `/dayz-preflight`; if it is not found this rule is skipped with an `[INFO]` line.

   Claude Code checks file writes against `Edit(...)` rules only, so one `Edit` rule blocks both the Edit and Write tools. `Write(path)` rules are accepted but never matched, which is why the skill does not write them.
5. Records the scope in `.claude/local-memory/dayz-active-scope.json` **before** touching the settings, listing both the previous run's rules and the new ones, so if the settings write fails every rule that may still be in the settings is recorded and `--clear` can remove it. The record is written to a temp file that replaces the old one in a single step (see "If a write fails" below).
6. Writes back `.claude/settings.local.json`, only if its content changed. The old file is first copied to `.claude/local-memory/settings.local.json.<timestamp>.bak`, a new name on every change, so no older backup is replaced (restore by copying one back). The new file replaces the old one in a single step, so a failed write never leaves it half-written. `--clear` backs up and writes the same way.
7. Narrows the record to the active mod and the rules this run actually appended (a matching rule you already had is skipped, left in place and not recorded, so `--clear` never removes it) so `--clear` can undo precisely what was set.

`--clear` removes the recorded rules from `permissions.deny`, then deletes the record. If `.claude/settings.local.json` does not exist it is not created. When fewer recorded rules are found than the record lists (the settings file is missing, or rules were edited by hand), it prints a `[WARN]` line with the count so you can check `permissions.deny` yourself.

**If a write fails.** Every write (the scope record and the settings) goes through a temp file in `.claude\local-memory\` (gitignored, so a leftover never shows up as an untracked file) that then replaces the target in one step. If the backup, the temp file or the replace fails, for example because an editor, antivirus or a sync tool holds a lock on `settings.local.json` or the disk is full, the temp file is deleted and the run exits 1 with a `[FAIL]` line that names the file and says what state each file is in:

- The first scope-record write fails: nothing was changed. Fix the cause, then run again.
- The backup or settings write fails: `settings.local.json` is unchanged and the scope record lists every rule that may be in it. Fix the cause, then run again, or run `--clear`.
- The final scope-record write fails: the settings were updated, but the record still also lists the previous scope's rules. `--clear` still removes them all; running again corrects the record.
- During `--clear`, the settings write fails: nothing was changed; run `--clear` again. If only deleting the record fails, the rules are already gone from the settings and the message tells you to delete the record by hand.

## What it does not do

- **Not a full sandbox.** Repo-wide files (`.claude/`, `scripts/`, `docs/`, root configs) stay writable so the agent can keep editing the template and tooling. Only sibling mods are protected.
- **Only partly covers Bash.** Edit deny rules also cover file commands Claude Code recognizes in Bash (such as `sed` or `tee`) and redirection targets, but a script or command that writes files indirectly still goes through. This skill protects the high-frequency accidents (Edit/Write) without pretending to be a security boundary. Use this as a guardrail, not a jail.
- **Deny rules do not auto-update on new mods.** They list only the siblings that existed when you scoped. The scope guard hook (`hooks/scope_guard.py`, loaded from `.claude/settings.json` in a clone and from the plugin's `hooks/hooks.json`) reads the recorded scope on every Edit, Write, MultiEdit, Bash and PowerShell call, so it also blocks mod folders created after scoping: every other top-level folder under `workspace/`, even one that has no `config.cpp` or `$PBOPREFIX$` yet (helper folders whose names start with `_`, such as `workspace/_notes/`, stay editable unless they hold one of those files), plus the `P:\<Other>\` junction and `P:\Mods\@<Other>\` deploy folder of each mod that has one. For Bash and PowerShell it checks the write targets on the command line: redirects, `rm`, `mv`, `cp` and `Copy-Item` destinations, `sed -i`, `tee`, `Set-Content`, `Out-File` and similar. A script file or `python -c` that writes files is not seen. Re-run `/dayz-scope-mod <ActiveMod>` anyway to add the new sibling to the deny list.
- **Does not gate on `/dayz-preflight`.** This is a meta-skill that operates on settings files, not on `P:\` content. Safe to run without preflight passing.

## When to run

- At the start of a session focused on a single mod.
- After importing or scaffolding a new mod that you then want to lock into.
- Before delegating work to a subagent that might fan out across the workspace.

Skip when:

- Working across multiple mods in the same session.
- Doing template/infrastructure work (skill edits, agent edits, docs).

## Output

```
DayZ scope: SuperMedKit

[OK]    Mod found: workspace\SuperMedKit
[INFO]  Not mods (no config.cpp or $PBOPREFIX$), left writable: _archive
[INFO]  Sibling mods detected: 2 (OtherModA, OtherModB)
[INFO]  Backed up settings to .claude\local-memory\settings.local.json.20261024-101500.bak
[OK]    Added 8 Edit deny rules to .claude\settings.local.json
[OK]    Active scope recorded at .claude\local-memory\dayz-active-scope.json

Reads remain broad. Edit and Write to other mods are blocked.
Run /dayz-scope-mod --clear (or scope.py --clear) to lift.
```

If only one mod exists:

```
DayZ scope: SuperMedKit

[OK]    Mod found: workspace\SuperMedKit
[INFO]  No sibling mods to deny. Scope is set, but no rules were needed.
```

If `<ModName>` does not exist:

```
[FAIL]  workspace\NoSuchMod does not exist.
        Known mods:
          - SuperMedKit
        Scaffold first: /dayz-new-mod NoSuchMod  or  /dayz-import-mod --source <path>
```

## Do not

- Don't edit the deny rules manually. Re-run the skill to get them right and to keep `dayz-active-scope.json` in sync.
- Don't rely on this for security against malicious agents. It blocks high-frequency accidents only.
- Don't run with `--clear` and forget to re-scope: every Edit and Write to any mod becomes possible again.
