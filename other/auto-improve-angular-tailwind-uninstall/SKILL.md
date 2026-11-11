---
name: auto-improve-angular-tailwind-uninstall
description: "Remove the angular-tailwind add-on of the agentic-auto-improve plugin from this project: the four rule documents under .claude/references/angular-tailwind/ and their entries in the project profile's review.documents slot, and any copy of the retired prompt advisor hook (a settings.json row and a file, under the name angular-tailwind-advisor.py or the older architecture-advisor.py). Previews every row, file and profile change, asks for one confirmation, then writes: rows first, then the profile, then the files. Keeps any file you edited. The name carries the plugin name because you may have several plugins installed. Use when: user says /auto-improve-angular-tailwind-uninstall, 'remove the angular tailwind add-on', 'uninstall the Angular and Tailwind rule documents', 'remove the architecture advisor', or when the install refuses with disabled-hook-present. Never deletes a helper or the stylesheet snippet."
user_invocable: true
---

# /auto-improve-angular-tailwind-uninstall — remove the angular-tailwind add-on

This skill takes the `angular-tailwind` add-on out of a project. It does two jobs, and one run does both:

- It removes what the current add-on installs: the four rule documents in `.claude/references/angular-tailwind/` and their four entries in the project profile's `review.documents` slot.
- It cleans up the retired prompt hook. Older releases of the plugin installed a hook that ran on every prompt, as `.claude/hooks/architecture-advisor.py` (releases before 0.9.9 registered it from the plugin's own `hooks.json`, and a project may carry a hand-copied row for it) and then as `.claude/hooks/angular-tailwind-advisor.py`. Both names, in every row form those releases wrote, are found and removed. The current install refuses with `disabled-hook-present` until this has run.

This skill proposes first. It writes only after one yes, and it reads and touches only `agentic-auto-improve`.

## The rule that shapes everything here

**The skill carries the conversation. The script carries every rule.**

Which rows match, which files are deleted, which are kept and in which order everything is written all live in `auto_improve_finish_install.py addon-remove`, which has its own test suite. Read its answer. Do not work any of it out yourself, and never delete a hook file or edit `settings.json` by hand to remove this add-on: a hook row that points at a missing script exits 2 and blocks every prompt. The script writes `settings.json` first (with a backup), then the profile, and deletes a file last.

What the script will not do:

- It deletes a file only when it is identical to the plugin's copy (line endings and a leading byte order mark are ignored) or it matches a copy an earlier release shipped. A file you edited is kept and reported as `kept-differs`; its row is still removed.
- It keeps a hook file that a `settings.local.json` or user settings row still names (`kept-referenced`).
- It never deletes a helper (`.claude/hooks/_project_paths.py`) and never removes the stylesheet snippet if one was added to a stylesheet. The snippet is in your own file; delete the marked block by hand if you want it gone.
- In the profile it removes exactly the add-on's four document paths from `review.documents`. Every other entry keeps its own text. When nothing is left the slot reads `none`.

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

Every command below is `$PY "$FI" addon-remove --name angular-tailwind --project . ...`.

## Step 1: Preview (writes nothing)

```bash
$PY "$FI" addon-remove --name angular-tailwind --project . --json
```

The answer carries:

- `rows`: every `settings.json` row it would remove, with its `event`, `matcher`, `file` and the `command` as written. A row matches by the hook file name, under any event and in any form (`py -3 "..."` strings, the `${CLAUDE_PLUGIN_ROOT}` form, and the exec form with `args`).
- `files`: each file with its `kind` (`hook`, `disabled-hook`, `document`) and its action: `delete`, `kept-differs`, `kept-referenced` or `absent`.
- `profile`: the `review.documents` slot (`removes` the paths it would take out, `before` and `after` the slot text, and a `unified-diff`). It is `null` only when the add-on has no documents.
- `kept`: what it leaves, each with the reason: helpers, the stylesheet snippet, and every file it kept.
- `kill-switches`: always empty for this add-on.
- `uninstall-skill`, `target`, `plugin-root` and `plan-sha256`.

**Keep `plan-sha256`.** The apply needs it as `--expect-sha256`. It covers the `settings.json` bytes, the profile bytes and the project's bytes of every file to delete, so anything that moves between the preview and the write is refused as `changed-since-preview`.

If `rows`, `files` and the profile change are all empty or `absent`, the add-on is not installed. Say so and stop.

## Step 2: Show the plan and ask once

Show the user, in plain words:

- the rows it would remove from `.claude/settings.json`, and that a backup is taken first.
- the files it would delete, and the files it would keep with the reason (an edited file is the team's; say how to compare it with the plugin's copy if they want to).
- the profile change: the slot before, the slot after.
- what it leaves: the helper and the stylesheet snippet.
- any hook file a local row still names, and that the user must remove that row first.

State your recommendation first, in one or two sentences. Then ask **once**: remove this add-on?

Declining writes nothing.

## Step 3: Apply

On a yes, apply with the `plan-sha256` from the preview:

```bash
$PY "$FI" addon-remove --name angular-tailwind --project . --apply --expect-sha256 <plan-sha256 from the preview>
```

The answer lists `removed-rows`, `unregistered` (the paths taken out of the slot), `deleted`, `kept` and the `backup` path. If it removed any row, tell the user to start a new session: Claude Code reads the hook rows once, when a session starts.

If the answer says `nothing-to-do`, nothing was installed. Nothing was written. Running the skill again after a removal changes nothing.

### Refusals

Exit `2` is a refusal you can correct. Exit `3` is an environment problem. On either, read `code` and `message`, tell the user the reason in one plain sentence, and stop. A refusal always means nothing was changed. The ones you may see:

- `profile-slot-missing`: the project has no `.claude/project-profile.md`, or the profile has no `review.documents` row, and the add-on's documents are still in the project. Their entries cannot be unregistered, so nothing was written. Tell the user to run `/auto-improve-finish-install` first, then run this skill again.
- `changed-since-preview`: something moved after the preview. Go back to the preview, show the new plan, and ask again. Never reuse the old hash.
- `malformed-settings` or `unexpected-settings-shape`: `settings.json` is not plain enough to edit safely. Nothing was written. Name the file and the reason, and tell the user to remove the row by hand, then run this skill again.
- `write-failed`: for example `.claude/settings.json` is a symbolic link. Nothing was written, or the message says what was done before the failure. Tell the user to edit the file the link points to by hand.
- `plugin-source-checkout`: this folder is the plugin's own checkout. Run it in a project that uses the plugin.
- `addon-unknown`: the name matches no add-on folder in the plugin.

## Closing

End with a short summary: which rows were removed, which files were deleted, which were kept and why, and which paths left `review.documents`. Say that the helper and the stylesheet snippet were left on purpose. Then say the install skill, `/auto-improve-angular-tailwind-install`, can put the documents back.

## Anti-patterns

- **Deleting the old advisor file or its row yourself.** A row left pointing at a missing script blocks every prompt. The script removes the row first.
- **Hand-editing `settings.json` or the profile instead of using the script.**
- **Writing without the preview's `plan-sha256`**, or with an old one. The hash is what proves the user saw the change as it is now.
- **Deleting a kept file because the script kept it.** A `kept-differs` file may hold the team's edits. Leave the decision to the user.
- **Removing the helper or the stylesheet snippet.** The script keeps them on purpose.

## When NOT to use

- To install the add-on. That is `/auto-improve-angular-tailwind-install`.
- Inside the plugin's own checkout. The script refuses it as `plugin-source-checkout`.
- On Cursor or Codex. Hooks are Claude-only in this release.
