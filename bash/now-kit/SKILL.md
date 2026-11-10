---
name: now-kit
description: Sets up a new Claude Code project folder from scratch — the NOW.md/RULES.md/CLAUDE.md layout, hooks that load NOW on start, log unproven claims, save disk state before compaction and remind about close-out, plus an in-project /close-out skill. ALWAYS use it when the user says "new project", "set up / start / create a project", "create a project folder", "make this folder a project", or when new work is about to start in a new folder. Also use it to check whether a project's scripts lag behind the template ("is the kit up to date", "compare the hooks").
license: MIT
compatibility: Designed for Claude Code. Requires python3 (3.9+); git is optional.
---

# now-kit — new project skeleton

This skill is the project-independent version of a layout that worked well for a long time in two real projects.
Why it exists: the old kit was copied by hand; steps got skipped (one project never got its close-out scripts) and stale copies spread.
`scripts/setup.py` does the mechanical work; your job is to gather the right information, verify the result and explain it to the user in plain language.

## What gets installed

```
<project>/
├── CLAUDE.md          short instructions loaded every session (On start · While working · Never · Skills)
├── NOW.md             "What now?" — ≤40 lines, 8 fixed sections, printed by a hook on start
├── RULES.md           standing rules (§1 file roles … §7 never), not read on start, grep'd when needed
├── TODO.md            deferred work and ideas
├── evidence/INDEX.md  receipt index (R-<PREFIX>-NN); evidence/now_archive/ holds old NOW files; evidence/DECISIONS.md appears at the first close-out
├── data/              raw/personal data that never goes into the repo
├── .gitignore         secrets, data, .claude/state stay out; hooks/skills/rules stay in
└── .claude/
    ├── settings.json  SessionStart · PreCompact · Stop · SessionEnd registrations
    ├── hooks/         now_load.sh · now_check.py · due_dates.py · close.py · close_reminder.py ·
    │                  safety_net.py · claim_check.py · precompact_snapshot.sh · state_io.py (shared helper) ·
    │                  secret_filter.py (removes passwords/keys from text written to disk) ·
    │                  decisions.py (Dead ends → evidence/DECISIONS.md, never trimmed) ·
    │                  memory_audit.py (memory: duplicates / dead paths / missing index lines / old notes; read-only)
    ├── rules/         (empty) rules that load when a given folder is touched go here
    └── skills/close-out/SKILL.md   the /close-out procedure
```

If the user's machine has global hooks (`~/.claude/hooks`), leave them alone and don't copy them into the project; this kit installs project-level hooks only.

## Steps

1. **Gather the information** (ask for what's missing in one message, don't invent it):
   - folder path (e.g. `~/projects/<name>`)
   - project name (human readable, e.g. "Blog — weekly post tracking")
   - one-sentence purpose
   - receipt prefix: 2-4 capital letters (e.g. BL, WEB). Suggesting one is your job; offer options to the user.
   - git: yes by default (makes undo and the close-out commit possible). If the user doesn't want it, `--no-git`.
2. **Look at the folder** (`ls -la`). If it isn't empty, tell the user what's there; the script never overwrites existing files, but don't install without telling them.
3. **Install:**
   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/setup.py" "<folder>" --name "<name>" --purpose "<sentence>" --prefix <XX>
   ```
   Claude Code replaces `${CLAUDE_SKILL_DIR}` with this skill's folder when the skill loads (plugin install or manual copy alike).
   It is not a shell variable: if you see it unreplaced, use the base directory shown when the skill loaded.
   Windows: if `python3` is missing or opens the Microsoft Store ("Python was not found"), use `py -3` in its place here and in every later `python3` command. The installed hooks find Python on their own (`.claude/hooks/py.sh`).
   The exit code must be 0 and the last line `VERIFICATION OK …` (the verdict is always printed last). If the folder already had a `.claude/settings.json` or `.gitignore`, verification checks that they still register every hook and keep secrets/data out; if not, it lists what to merge — merge it with the user, never overwrite their file. If it says `FAILED`, fix the cause and rerun; don't say "installed".
   If there are "skipped" lines, tell the user which files kept their old version.
4. **Fill in the project-specific part** (the script can't do this, you do):
   - Add the project's own folders (code, config…) to the `RULES.md §1` table, and project-specific claim rules to §2 — only from what the user said, don't invent.
   - If there's a code folder, create `.claude/rules/<area>.md`; the `paths:` list at the top loads the rule when that folder is touched:
     ```
     ---
     paths:
       - "src/**"
     ---
     ```
   - If there will be tests, make `tests/run.py` the single entry point; /close-out looks for it.
   - Rewrite the `NOW.md` "Next ONE step" for the first task the user gave, then `python3 .claude/hooks/now_check.py NOW.md` → OK.
5. **Report to the user** (≤12 lines, plain language): what was installed, what you verified (with command output), that the first commit hasn't been made yet,
   and one action: "open a new chat in this folder; NOW.md should appear on start". You can't have verified that the hooks really run in a new chat
   before that chat is opened — say "not verified".

## Comparing an existing project

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/setup.py" "<project>" --compare
```
Read-only. Don't blindly replace a DIFFERENT file with the template: projects pick up their own fixes over time
(e.g. project-specific gate scripts added later). Show the difference and leave the decision to the user.
Don't touch projects the user has marked inactive until they reactivate them.

## Updating the template

If an improvement in one project is useful in general (e.g. a hook fix that would apply to every project), move it into `assets/template/` too
and test it with `setup.py` in a temporary folder (`mktemp -d`). Project-specific names, paths and tool names (a particular service, server…) never go into the template.
