---
name: auto-improve-strict-shell-gate-install
description: "Install the strict-shell-gate add-on of the agentic-auto-improve plugin in this project: a hook that reads each shell command before it runs and blocks a write into a source file that no approved contract covers. Says plainly what it gets wrong. Previews the files and the settings.json change, asks for one confirmation, then writes. The name carries the plugin name because you may have several plugins installed. Use when: user says /auto-improve-strict-shell-gate-install, 'install the strict shell gate', 'block shell writes before they happen', or 'turn on bash-gate'. Never overwrites a file that differs and never removes a row."
user_invocable: true
---

# /auto-improve-strict-shell-gate-install — install the strict-shell-gate add-on

The `strict-shell-gate` add-on is the strict way to enforce the concept rule on shell commands. It reads the command text before it runs. Nothing registers it by default, because the default is cheaper and catches more.

This skill proposes first. It writes only after one yes, and it reads and touches only
`agentic-auto-improve`.

## The rule that shapes everything here

**The skill carries the conversation. The script carries every rule.**

Which files are copied, which rows are written, what is already there, and what is refused all
live in `auto_improve_finish_install.py addon`, which has its own test suite. Read its answer.
Do not work any of it out yourself, and never edit `settings.json` by hand to install this
add-on: a typing mistake there can switch every check off, or block every action.

The script never removes a row or a file. It never overwrites a file that differs from the
plugin's copy. It copies a helper file only when the project lacks it.

## Step 0: Find the script

The script sits at a different path under a vendored copy and under a plugin install. Test
the places **in this order** and keep the first hit. Do not use `ls` on all three paths:
`ls` sorts its operands, so the order you meant is lost.

```bash
FI=
S=.claude/scripts/auto_improve_finish_install.py
if [ -f "$S" ]; then FI=$S
elif [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/$S" ]; then FI=$CLAUDE_PLUGIN_ROOT/$S
else
  # What Claude Code recorded for this plugin (this project's entry, then the user entry), then the newest cache folder by version number.
  CFG=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
  ME=$(printf %s "$CLAUDE_PROJECT_DIR" | tr 'A-Z\134' 'a-z/' | tr -s /)
  REC=$(tr -d '\r\n' 2>/dev/null < "$CFG/plugins/installed_plugins.json" | grep -o '"agentic-auto-improve@[^"]*" *: *\[[^]]*]' | grep -o '{[^{}]*}' | tr '\134' / | tr -s /)
  MINE=$(printf '%s\n' "$REC" | grep '"scope" *: *"project"' | while IFS= read -r O; do
    P=$(printf %s "$O" | sed -n 's/.*"projectPath" *: *"\([^"]*\)".*/\1/p' | tr 'A-Z' 'a-z' | tr -s /)
    [ -n "$ME" ] && [ "${P%/}" = "${ME%/}" ] && printf '%s\n' "$O"
  done)
  NEWEST=$(ls -d "$CFG"/plugins/cache/*/agentic-auto-improve/*/ 2>/dev/null | sed -n 's|^\(.*/\([0-9][0-9.]*\)/\)$|\2 \1|p' | sort -rV | cut -d' ' -f2-)
  FI=$({ printf '%s\n' "$MINE"; printf '%s\n' "$REC" | grep '"scope" *: *"user"'; } | sed -n 's/.*"installPath" *: *"\([^"]*\)".*/\1/p' | { cat; printf '%s\n' "$NEWEST"; } | while IFS= read -r D; do
    [ -n "$D" ] && [ -f "${D%/}/$S" ] && { printf '%s\n' "${D%/}/$S"; break; }
  done)
fi
py -3 "$FI" --help   # macOS and Linux: python3 "$FI" --help
```

**If `FI` is empty, stop and say so.** Say that the script was not found in the project, in
`$CLAUDE_PLUGIN_ROOT` or in the plugin cache. Then stop. Without the script there is nothing
to run, and a skill that guesses is worse than one that stops.

Pick the launcher once and reuse it. On Windows use `py -3`. On macOS and Linux use
`python3`. The rest of this file writes it as `PY`.

```bash
PY="py -3"        # Windows
PY="python3"      # macOS and Linux
```

Every command below is `$PY "$FI" addon --name strict-shell-gate --project . ...`.

## What this add-on does

The hook `bash-gate.py` runs before every `Bash` command. It looks for the files the command writes (a redirect, `tee`, `sed -i`, `cp`, `mv`, `dd of=`, and a Python `open(..., 'w')`). If a target is a source file that no approved concept contract covers, it blocks the command before the write happens.

It needs three helpers: `.claude/hooks/_project_paths.py`, `.claude/hooks/_shell_write_targets.py` (the shell parser) and `.claude/scripts/_contract_index.py`. The install copies each only if the project lacks it. If the parser file is later deleted, the gate exits with an error that names the file, so a gate that stopped reading is loud, not silent.

## What it gets wrong (say this plainly before asking)

Tell the user these facts in plain words. Do not soften them.

- **It blocks before the write, but it reads the command text with a parser, and the parser misreads some commands.** The
  measured case: `sed -i` followed by `git diff --stat` made it read `--stat` as the file being written, and it blocked a
  correct command.
- **It cannot see what a program writes.** A command such as `python script.py` or `node build.js` can write any file, and
  the gate sees only the command line, never the files the program opens.
- **It costs a program start on every shell command.**
- **The Changed-file check stays on.** The plugin already runs a check at the end of each turn that asks git which files
  changed and judges each one against the approved contracts. That check sees what a program wrote. This add-on does not
  replace it and does not turn it off. The gate adds an early block on top of it.

So this add-on is for a team that wants the early block and accepts the false alarms. Recommend it only on that basis.

## Step 1: Preview (writes nothing)

```bash
$PY "$FI" addon --name strict-shell-gate --project . --json
```

The answer carries `files` (each file with its action: `copy`, `present` or `keep-existing`),
`to-add` (the settings rows it would write), `already-present`, `unified-diff` (the exact change
to `.claude/settings.json`), `notes`, `kill-switches`, `target`, `plugin-root` and `plan-sha256`.
**Keep `plan-sha256`.** The apply needs it as `--expect-sha256`. It covers the settings bytes, the
text the write would produce and every file the install would copy, so anything that moves
between the preview and the write is refused as `changed-since-preview`.

**Read the section "What it gets wrong" to the user before you ask for the yes.**

## Step 2: Show the plan and ask once

Show the user, in plain words:

- the files it would copy into `.claude/hooks/` (and any helper into `.claude/hooks/` or
  `.claude/scripts/`), with the action for each. A file marked `present` is already identical
  and is not touched. A helper marked `keep-existing` is kept as it is.
- the exact `unified-diff` for `.claude/settings.json`, and how many rows it adds.
- that the add-on has no kill switch (`kill-switches` is an empty list): the way out is `/auto-improve-strict-shell-gate-uninstall`.
- any `notes`.

State your recommendation first, in one or two sentences. Then ask **once**: install this
add-on?

Say plainly: **the new rows take effect only in a NEW session.** Claude Code reads the hook rows
once, when a session starts, so this session keeps running without them.

Declining writes nothing.

## Step 3: Apply

On a yes, apply with the `plan-sha256` from the preview:

```bash
$PY "$FI" addon --name strict-shell-gate --project . --apply --expect-sha256 <plan-sha256 from the preview>
```

The script copies the hook files first and writes the rows last, so a row never points at a file
that is not there. It takes a timestamped backup of `.claude/settings.json` before it replaces
it. Print the `backup` path and the `rollback` line (one copy command that puts the old file
back). Tell the user to add `.claude/settings.json.bak-*` to `.gitignore`.

If the answer says `nothing-to-do`, the add-on was already installed. Nothing was written.

This gate has no kill switch. `CLAUDE_BASH_GATE` is not read, and `CLAUDE_CONCEPT_GATE=off` no longer turns this gate off (it still turns off the concept gate and the Changed-file check). To get past the gate, remove it with `/auto-improve-strict-shell-gate-uninstall`.

### Refusals

Exit `2` is a refusal you can correct. Exit `3` is an environment problem, such as an add-on
folder with no `addon.json`. On either, read `code` and `message`, tell the user the reason in
one plain sentence, and stop. A refusal always means nothing was changed. The ones you may see:

- `addon-file-differs`: a hook file of this add-on already exists in the project and is not the
  plugin's copy. Name the file. The script will not overwrite it. The user compares it with the
  plugin's copy and renames or removes it by hand, then runs this skill again.
- `changed-since-preview`: something moved after the preview. Go back to the preview, show the
  new plan, and ask again. Never reuse the old hash.
- `write-failed`: for example `.claude/settings.json` is a symbolic link. Nothing was written.
  Tell the user to edit the file the link points to by hand.
- `plugin-source-checkout`: this folder is the plugin's own checkout. Install an add-on in a
  project that uses the plugin instead.
- `addon-unknown`: the name matches no add-on folder in the plugin.

## How to remove it

This install never removes anything. The removal is its own skill, `/auto-improve-strict-shell-gate-uninstall`. It previews, asks once, then removes the `PreToolUse` row (matcher `Bash`) from `settings.json` (with a backup) and only then deletes `.claude/hooks/bash-gate.py`. It keeps the file if you edited it, leaves `_project_paths.py`, `_shell_write_targets.py` and `.claude/scripts/_contract_index.py` because the default main-checkout guard and the concept gate use them.

Do not delete the hook file or the row by hand while the hook can run: a row that points at a missing script blocks every shell command. Only when the hook cannot run (the README table, section "Ways out when a hook cannot run") does the user remove its row by hand.

## Closing

End with a short summary: what was copied, which rows were added, the backup path, and what was
**not** written and why. Then repeat the new-session warning. Say that running this skill again
changes nothing: identical files are left alone and a row that is already there is not written
twice.

## Anti-patterns

- **Selling it as complete.** It misses what programs write, and it misreads some commands.
- **Describing it as a replacement for the Changed-file check.** The check stays on.

- **Writing `settings.json` without the preview's `plan-sha256`**, or with an old one. The hash
  is what proves the user saw the change as it is now.
- **Hand-editing `settings.json` instead of using the script.**
- **Overwriting a hook file that differs.** The script refuses; do not copy over it yourself.
- **Skipping the new-session warning.** The user will otherwise test in this session and
  conclude the add-on does nothing.

## When NOT to use

- To catch files a program wrote. The Changed-file check does that, and it is already on.
- To switch the gate off. There is no switch; `/auto-improve-strict-shell-gate-uninstall` removes it.
- Inside the plugin's own checkout. The script refuses it as `plugin-source-checkout`.
- On Cursor or Codex. Hooks are Claude-only in this release.
