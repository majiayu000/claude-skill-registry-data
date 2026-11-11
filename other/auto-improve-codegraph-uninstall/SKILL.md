---
name: auto-improve-codegraph-uninstall
description: "Remove the codegraph add-on of the agentic-auto-improve plugin from this project: the settings.json rows of the code-search-first guard (and of the retired tracker and reset hooks, when an older install left them), then the hook files. Previews every row and file, asks for one confirmation, then writes: rows first with a backup, then the files. Keeps any hook file you edited, and keeps the shared helpers. The add-on has no kill switch, so this skill is the way out. The name carries the plugin name because you may have several plugins installed. Use when: user says /auto-improve-codegraph-uninstall, 'remove the codegraph add-on', 'turn off the code-search-first guard', or 'uninstall the CodeGraph gate'. Never deletes a helper."
user_invocable: true
---

# /auto-improve-codegraph-uninstall — remove the codegraph add-on

This skill takes the `codegraph` add-on out of a project. Since 0.17.0 the add-on is one hook file, `codegraph-first-guard.py`, with two rows in `.claude/settings.json` (`PreToolUse` on `Read|Grep|Glob`, and `UserPromptSubmit` with the argument `notice`). A project installed by an older release may still carry the two retired hooks too: `codegraph-turn-reset.py` and `codegraph-turn-tracker.py`, with their rows (`UserPromptSubmit`; `PostToolUse` on the CodeGraph tools; `PostToolUse` on `Bash` with `if: "Bash(codegraph *)"`). The removal takes out every row that names any of the three files, in whatever form, and the three files in `.claude/hooks/`. It is also the way out for a retired hook that the install refused to retire (`disabled-hook-present`: a row in `.claude/settings.local.json`, or an edited copy).

This skill proposes first. It writes only after one yes, and it reads and touches only `agentic-auto-improve`.

## The rule that shapes everything here

**The skill carries the conversation. The script carries every rule.**

Which rows match, which files are deleted, which are kept and in which order everything is written all live in `auto_improve_finish_install.py addon-remove`, which has its own test suite. Read its answer. Do not work any of it out yourself. The skill never deletes a hook file and never edits `settings.json` by hand to remove this add-on: a hook row that points at a missing script exits 2 and blocks every prompt (and here, every source read). The script writes `settings.json` first, with a backup, and deletes a file last. Only when a hook cannot run (the table in the README, section "Ways out when a hook cannot run") does the user remove its row by hand.

This add-on has no kill switch and no bypass variable. This skill is the way out.

What the script will not do:

- It deletes a hook file only when it is identical to the plugin's copy or to a released copy listed in the manifest's `released_sha256` (line endings and a leading byte order mark are ignored). So an unedited copy from an older release is deleted too. A file you edited is kept and reported as `kept-differs`; its row is still removed.
- It keeps a hook file that a `settings.local.json` or user settings row still names (`kept-referenced`).
- It never deletes a helper. `_project_paths.py` and `_error_log.py` stay: other hooks use them.
- It keeps the `mcp__codegraph__*` permission entry in `permissions.allow` and lists it under `kept`.
- It does not delete the session folder `auto-improve-codegraph-<session id>` under the Per-user session parent (`%LOCALAPPDATA%\auto-improve-codegraph\` on Windows, `~/.cache/auto-improve-codegraph/` or `$XDG_CACHE_HOME/auto-improve-codegraph/` on POSIX): that is a leftover, and the guard's prompt row prunes it. Folders `auto-improve-codegraph-*` left in the system temp folder by 0.15.2 are no longer read; delete them by hand if wanted (an older `.claude/.codegraph-used-this-turn` is a leftover of a turn the user may delete).

- It keeps the measurement log, `<project>/.claude/logs/codegraph-shadow.jsonl`, and everything else under `.claude/logs/`. The log is measurement data the report (`py -3 .claude/scripts/codegraph_shadow_report.py`) reads; the user deletes it by hand if they want it gone. Hook backups an upgrade took (`.claude/hooks/*.bak-*`) are kept too.

**Upgrade route.** An uninstall is not needed to upgrade: re-running `/auto-improve-codegraph-install` backs up and replaces an unedited older hook copy (a hash listed in the manifest's `released_sha256`). The route through this skill is for a hook file you edited, which the install refuses as `addon-file-differs`: run this skill (it keeps the edited file; rename or remove it by hand), run `/auto-improve-codegraph-install`, then start a new session.

## Step 0: Find the script

Find the script through the plugin install **only**. A copy under the project's own `.claude/scripts/` is never used here: a vendored installer can be older than the hooks it manages. Without a separate plugin install the removal already refuses, so nothing is lost. Test the places **in this order** and keep the first hit. Do not use
`ls` on all the paths: `ls` sorts its operands, so the order you meant is lost.

```bash
FIP=
S=.claude/scripts/auto_improve_finish_install.py
if [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/$S" ]; then FIP=$CLAUDE_PLUGIN_ROOT/$S
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
  FIP=$({ printf '%s\n' "$MINE"; printf '%s\n' "$REC" | grep '"scope" *: *"user"'; } | sed -n 's/.*"installPath" *: *"\([^"]*\)".*/\1/p' | { cat; printf '%s\n' "$NEWEST"; } | while IFS= read -r D; do
    [ -n "$D" ] && [ -f "${D%/}/$S" ] && { printf '%s\n' "${D%/}/$S"; break; }
  done)
fi
py -3 "$FIP" --help   # macOS and Linux: python3 "$FIP" --help
```

**If `FIP` is empty, stop and say so.** Say that the script was not found in
`$CLAUDE_PLUGIN_ROOT` or in the plugin cache. Then stop. Without the script there is nothing
to run, and a skill that guesses is worse than one that stops.

Pick the launcher once and reuse it. On Windows use `py -3`. On macOS and Linux use
`python3`. The rest of this file writes it as `PY`.

```bash
PY="py -3"        # Windows
PY="python3"      # macOS and Linux
```

Every command below is `$PY "$FIP" addon-remove --name codegraph --project . ...`.

## Step 1: Preview (writes nothing)

```bash
$PY "$FIP" addon-remove --name codegraph --project . --json
```

The answer carries:

- `rows`: every `settings.json` row it would remove, with its `event`, `matcher`, `file` and the `command` as written. A row matches by the hook file name, under any event and in any form.
- `files`: each hook file (the guard and any retired tracker or reset hook the project still has) with its action: `delete`, `kept-differs`, `kept-referenced` or `absent`.
- `kept`: what it leaves, each with the reason: the two helpers, and every file it kept.
- `kill-switches`: an empty list. The add-on has none.
- `profile` (`null` for this add-on), `uninstall-skill`, `target`, `plugin-root` and `plan-sha256`.

**Keep `plan-sha256`.** The apply needs it as `--expect-sha256`. It covers the `settings.json` bytes and the project's bytes of every file to delete, so anything that moves between the preview and the write is refused as `changed-since-preview`.

If `rows` is empty and every file is `absent`, the add-on is not installed. Say so and stop.

## Step 2: Show the plan and ask once

Show the user, in plain words:

- the rows it would remove from `.claude/settings.json`, and that a backup is taken first.
- the files it would delete, and the files it would keep with the reason.
- what it leaves: the helpers, and the `mcp__codegraph__*` permission entry (it is harmless without the hooks).
- that after the removal a source `Read`, `Grep` or `Glob` is no longer held back until a CodeGraph tool has run.

State your recommendation first, in one or two sentences. Then ask **once**: remove this add-on?

Declining writes nothing.

## Step 3: Apply

On a yes, apply with the `plan-sha256` from the preview:

```bash
$PY "$FIP" addon-remove --name codegraph --project . --apply --expect-sha256 <plan-sha256 from the preview>
```

The answer lists `removed-rows`, `deleted`, `kept` and the `backup` path. Tell the user to **start a new session**: Claude Code reads the hook rows once, when a session starts, so this session still runs the guard until then.

If the answer says `nothing-to-do`, the add-on was not installed. Nothing was written. Running the skill again after a removal changes nothing.

### Refusals

Exit `2` is a refusal you can correct. Exit `3` is an environment problem. On either, read `code` and `message`, tell the user the reason in one plain sentence, and stop. A refusal always means nothing was changed. The ones you may see:

- `changed-since-preview`: something moved after the preview. Go back to the preview, show the new plan, and ask again. Never reuse the old hash.
- `malformed-settings` or `unexpected-settings-shape`: `settings.json` is not plain enough to edit safely. Nothing was written. Name the file and the reason, and tell the user to remove the three rows by hand, then run this skill again.
- `write-failed`: for example `.claude/settings.json` is a symbolic link, or `.claude` or `.claude/hooks` is a link (a junction on Windows) to another folder. Nothing was written, or the message says what was done before the failure. Tell the user to edit the file the link points to by hand.
- `plugin-source-checkout`: this folder is the plugin's own checkout. Run it in a project that uses the plugin.
- `addon-unknown`: the name matches no add-on folder in the plugin.

## Closing

End with a short summary: which rows were removed, which files were deleted, which were kept and why, and the backup path. Then repeat the new-session note. Say that the helpers were left on purpose, and that the install skill, `/auto-improve-codegraph-install`, puts the add-on back.

## Anti-patterns

- **Deleting a hook file yourself before its row is gone.** A row that points at a missing script blocks every prompt. The script removes the rows first.
- **Hand-editing `settings.json` instead of using the script.** Only a hook that cannot run (the README table) is removed by hand, by the user.
- **Writing without the preview's `plan-sha256`**, or with an old one. The hash is what proves the user saw the change as it is now.
- **Telling the user to set a bypass variable.** The guard has none. The way out is this skill.
- **Deleting a kept file because the script kept it.** A `kept-differs` file may hold the team's edits.
- **Skipping the new-session note.** The user will otherwise test in this session and conclude the guard is still on.

## When NOT to use

- To install the add-on. That is `/auto-improve-codegraph-install`.
- To pause the guard for one turn. There is no pause; call a CodeGraph tool, or repeat the blocked call once (the retry escape: it is allowed and logged). Not after a `session-state-unusable` block, which offers no retry. After a `retry-ticket-unwritten` block the retry was not recorded, so the repeat is blocked once more (as `source-target` or `ambiguous-target`) and the identical call after it is allowed.
- Inside the plugin's own checkout. The script refuses it as `plugin-source-checkout`.
- On Cursor or Codex. Hooks are Claude-only in this release.
