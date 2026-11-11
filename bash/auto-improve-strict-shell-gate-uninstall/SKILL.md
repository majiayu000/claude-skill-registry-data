---
name: auto-improve-strict-shell-gate-uninstall
description: "Remove the strict-shell-gate add-on of the agentic-auto-improve plugin from this project: the settings.json row of the bash-gate hook (PreToolUse on Bash), then the file .claude/hooks/bash-gate.py. Previews the row and the file, asks for one confirmation, then writes: the row first with a backup, then the file. Keeps the file when you edited it, and keeps the shared helpers. The add-on has no kill switch, so this skill is the way out. The name carries the plugin name because you may have several plugins installed. Use when: user says /auto-improve-strict-shell-gate-uninstall, 'remove the strict shell gate', 'turn off bash-gate', or 'uninstall the shell write gate'. Never deletes a helper."
user_invocable: true
---

# /auto-improve-strict-shell-gate-uninstall — remove the strict-shell-gate add-on

This skill takes the `strict-shell-gate` add-on out of a project: the `PreToolUse` row (matcher `Bash`) in `.claude/settings.json` that runs `bash-gate.py`, and the file `.claude/hooks/bash-gate.py`.

This skill proposes first. It writes only after one yes, and it reads and touches only `agentic-auto-improve`.

## The rule that shapes everything here

**The skill carries the conversation. The script carries every rule.**

Which rows match, which files are deleted, which are kept and in which order everything is written all live in `auto_improve_finish_install.py addon-remove`, which has its own test suite. Read its answer. Do not work any of it out yourself. The skill never deletes the hook file and never edits `settings.json` by hand to remove this add-on: a hook row that points at a missing script exits 2 and blocks every shell command. The script writes `settings.json` first, with a backup, and deletes the file last. Only when a hook cannot run (the table in the README, section "Ways out when a hook cannot run") does the user remove its row by hand.

This add-on has no kill switch. `CLAUDE_BASH_GATE` is not read, and `CLAUDE_CONCEPT_GATE=off` no longer turns this gate off: it still turns off the concept gate and the Changed-file check, and nothing else. This skill is the way out.

What the script will not do:

- It deletes `bash-gate.py` only when it is identical to the plugin's copy (line endings and a leading byte order mark are ignored). A file you edited is kept and reported as `kept-differs`; its row is still removed.
- It keeps a hook file that a `settings.local.json` or user settings row still names (`kept-referenced`).
- It never deletes a helper. `_project_paths.py`, `_shell_write_targets.py` and `.claude/scripts/_contract_index.py` stay: the default main-checkout guard and the concept gate use them.
- It does not touch the concept gate or the Changed-file check, which stay on whatever you decide here.

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

Every command below is `$PY "$FI" addon-remove --name strict-shell-gate --project . ...`.

## Step 1: Preview (writes nothing)

```bash
$PY "$FI" addon-remove --name strict-shell-gate --project . --json
```

The answer carries:

- `rows`: every `settings.json` row it would remove, with its `event`, `matcher`, `file` and the `command` as written. A row matches by the hook file name, under any event and in any form.
- `files`: `bash-gate.py` with its action: `delete`, `kept-differs`, `kept-referenced` or `absent`.
- `kept`: what it leaves, each with the reason: the three helpers, and every file it kept.
- `kill-switches`: an empty list. The add-on has none.
- `profile` (`null` for this add-on), `uninstall-skill`, `target`, `plugin-root` and `plan-sha256`.

**Keep `plan-sha256`.** The apply needs it as `--expect-sha256`. It covers the `settings.json` bytes and the project's bytes of every file to delete, so anything that moves between the preview and the write is refused as `changed-since-preview`.

If `rows` is empty and the file is `absent`, the add-on is not installed. Say so and stop.

## Step 2: Show the plan and ask once

Show the user, in plain words:

- the row it would remove from `.claude/settings.json`, and that a backup is taken first.
- the file it would delete, or keep, with the reason.
- what it leaves: the helpers.
- that after the removal a shell command that writes into a source file is no longer checked against an approved contract.

State your recommendation first, in one or two sentences. Then ask **once**: remove this add-on?

Declining writes nothing.

## Step 3: Apply

On a yes, apply with the `plan-sha256` from the preview:

```bash
$PY "$FI" addon-remove --name strict-shell-gate --project . --apply --expect-sha256 <plan-sha256 from the preview>
```

The answer lists `removed-rows`, `deleted`, `kept` and the `backup` path. Tell the user to **start a new session**: Claude Code reads the hook rows once, when a session starts, so this session still runs the gate until then.

If the answer says `nothing-to-do`, the add-on was not installed. Nothing was written. Running the skill again after a removal changes nothing.

### Refusals

Exit `2` is a refusal you can correct. Exit `3` is an environment problem. On either, read `code` and `message`, tell the user the reason in one plain sentence, and stop. A refusal always means nothing was changed. The ones you may see:

- `changed-since-preview`: something moved after the preview. Go back to the preview, show the new plan, and ask again. Never reuse the old hash.
- `malformed-settings` or `unexpected-settings-shape`: `settings.json` is not plain enough to edit safely. Nothing was written. Name the file and the reason, and tell the user to remove the row by hand, then run this skill again.
- `write-failed`: for example `.claude/settings.json` is a symbolic link. Nothing was written, or the message says what was done before the failure. Tell the user to edit the file the link points to by hand.
- `plugin-source-checkout`: this folder is the plugin's own checkout. Run it in a project that uses the plugin.
- `addon-unknown`: the name matches no add-on folder in the plugin.

## Closing

End with a short summary: which row was removed, whether the file was deleted or kept and why, and the backup path. Then repeat the new-session note. Say that the helpers were left on purpose, and that the install skill, `/auto-improve-strict-shell-gate-install`, puts the add-on back.

## Anti-patterns

- **Deleting `bash-gate.py` yourself before its row is gone.** A row that points at a missing script blocks every shell command. The script removes the row first.
- **Hand-editing `settings.json` instead of using the script.** Only a hook that cannot run (the README table) is removed by hand, by the user.
- **Writing without the preview's `plan-sha256`**, or with an old one. The hash is what proves the user saw the change as it is now.
- **Telling the user to set `CLAUDE_BASH_GATE` or `CLAUDE_CONCEPT_GATE=off` to get past the gate.** Neither does. The way out is this skill.
- **Deleting a kept file because the script kept it.** A `kept-differs` file may hold the team's edits.
- **Skipping the new-session note.** The user will otherwise test in this session and conclude the gate is still on.

## When NOT to use

- To install the add-on. That is `/auto-improve-strict-shell-gate-install`.
- Inside the plugin's own checkout. The script refuses it as `plugin-source-checkout`.
- On Cursor or Codex. Hooks are Claude-only in this release.
