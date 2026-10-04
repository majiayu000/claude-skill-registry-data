---
name: hug
description: Turn HuG Flow on or off for Claude Code, or report whether it is on. `on` records the current setup, resolves instructions that conflict with HuG Flow, then applies the minimal setup through one import line; `off` reverts only what `on` added. Use when the user types /hug on, /hug off or /hug status, or asks in plain words to switch HuG Flow on or off.
argument-hint: on [--repo <owner>/<repo>] | off | status
---

# /hug

Everything is done by `~/.claude/hug/scripts/hug.sh`, a clone of
<https://github.com/julienbrg/hug>. If it's missing, follow
[SETUP.md](https://github.com/julienbrg/hug/blob/main/SETUP.md) first.

Run the script as it is. Don't edit `~/.claude/CLAUDE.md`,
`~/.claude/settings.json` or `~/.claude/skills/` by hand: `off` can
only revert what the script recorded.

## on

1. **Scan.** Run `sh ~/.claude/hug/scripts/hug.sh scan`. It prints
   candidate lines as `<file>:<line>:<text>`, from the global
   `CLAUDE.md` and the current repository's. They are only candidates:
   keep the ones that really contradict HuG Flow:
   - the agent stages its own work, or runs `git add -A`, `git add .`
     or `git commit -a`;
   - the agent commits without waiting for the maintainer to stage;
   - pushing or force-pushing to `main`;
   - `Co-Authored-By` trailers or "Generated with" footers.

   Also read `~/.claude/settings.json`: `includeCoAuthoredBy` or
   `gitAttribution` set to `true` is a conflict too. The script never
   overwrites an existing key, so the maintainer changes it or keeps it.

2. **Ask.** Show the real conflicts in one list. For each, the
   maintainer picks: keep theirs, comment it out (restored by `off`),
   or leave both. Say that an unresolved conflict makes the agent's
   behavior unpredictable, since both files load together.
3. **Plan.** State what `on` will change and that `/hug off` reverts
   it:
   - one import line appended to `~/.claude/CLAUDE.md`, pointing to
     `examples/minimal/CLAUDE.md` in the clone (skipped if the file
     already has HuG rules);
   - `includeCoAuthoredBy: false`, `gitAttribution: false` and deny
     rules for bulk staging, `git commit -a`, pushes to `main` and
     admin merges, added to `~/.claude/settings.json` where missing;
   - the `/intake` skill in `~/.claude/skills/intake/`, if absent;
   - with `--repo`: squash-only merges, merged branches deleted, and
     the `hug-flow` ruleset requiring the checks that passed on the
     last merged pull request, through `hug init`, which refuses if
     none did. This needs admin rights, is visible to
     collaborators, and rulesets on private repositories may need a
     paid GitHub plan.

   Wait for a yes.

4. **Apply.** Run
   `sh ~/.claude/hug/scripts/hug.sh on [--comment <file>:<line>]... [--repo <owner>/<repo>]`,
   with one `--comment` per line to comment out. Report its output,
   including the backup path.
5. Tell the maintainer the rules load in the **next** session: they
   start a new one, or run `/clear`.

## off

Run `sh ~/.claude/hug/scripts/hug.sh off` and report its output. It
removes the import line, uncomments what `on` commented out, removes the
settings and the intake skill `on` added and, if `on` had `--repo`,
deletes the ruleset and restores the merge settings. Changes the
maintainer made in the meantime stay. The full backup stays on disk.

## status

Run `sh ~/.claude/hug/scripts/hug.sh status` and report its output.
