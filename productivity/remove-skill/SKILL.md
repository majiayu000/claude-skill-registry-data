---
name: remove-skill
description: Cleanly undo something self-build added (a my-* skill or helper agent, a tool switched on from the catalogue, an automation or a built blueprint), including its settings and its record; use for "remove the skill you built", "turn off Zotero", "undo the morning brief", or "/remove-skill <name>".
model: sonnet
effort: medium
argument-hint: "<my-name | blueprint slug | tool id>"
---

# Remove skill

Take out something Alterbrain built for you, and put every setting back the way it was.

## When to use

- "Remove the skill you built last week", "I don't need the case summary any more".
- "Turn off the Zotero tool", "Stop the morning brief".
- A build failed halfway and needs cleaning up.
- A blueprint's **How to undo** says to run `/remove-skill`.

## Before you start

1. No clarify needed. You only need to know **what** to remove.
2. Find it: `node system/scripts/built.mjs list --json`. Match the user's words to a `name`, `blueprint` or `mcp` id. If several match, ask one AskUserQuestion with the candidates.
3. Not in `state/built.json`?
   - A folder `.claude/skills/my-<slug>/` or file `.claude/agents/my-<slug>.md` exists: treat those as the paths to remove.
   - A built-in skill (no `my-` prefix, not in `state/built.json`): don't remove it. Say kindly: "That one is part of Alterbrain itself, so I can't remove it. You can simply not use it." Stop.
4. Read the proposal card (`proposal` in the entry) and, for a blueprint, its **How to undo** section. Blueprint undo steps take priority over the generic ones below.

## Steps

1. **Show the plan** in plain words, one line each:
   - files that will be deleted (only `my-*` skill and agent files, and other paths listed in the entry);
   - routine notes (paths under `vault/90_routines/`): pause (recommended) or delete, see step 2;
   - tools that will be switched off (`mcp` ids → `config/mcp.selected.json`);
   - channels that go back to **draft** (`channels` → `config/autonomy.json`);
   - things only the user can do (delete a scheduled task in the app, remove a key from `.env.local`, revoke a sign-in);
   - what stays: "Your notes and anything it already wrote stay in your vault."
   Ask: "Remove it?" Remove it (recommended) / Keep it.
2. **Delete files.** The `my-*` skill and agent files are deleted by the script in step 6 (`built.mjs remove <name> --delete-files`), which works on Windows and Mac and refuses to delete anything else. For each path in the entry:
   - `.claude/skills/my-*` and `.claude/agents/my-*.md`: nothing to do here.
   - A routine note (a path in the entry under `vault/90_routines/`): ask once per note with AskUserQuestion. "Pause it (recommended): the note stays with its run history and is no longer checked or flagged late. / Delete it: the list is clean, but the history is gone." Pause by setting `status: "paused"` in the note's frontmatter (one line, nothing else); delete only after a clear yes. Whichever they pick, the job keeps running on its host until they delete the schedule there: step 5 covers that. If the note is already gone, skip it. A routine note whose `runs` is a different skill is not this build's: leave it.
   - Any other path (for example a view in `vault/_views/`): ask about each one first; default keep.
   - Never delete anything without the `my-` prefix under `.claude/`, anything in `system/`, or anything in `vault/40_sources/raw/`.
3. **Switch off tools.** Remove the entry's `mcp` ids from `config/mcp.selected.json` `enabled`, unless another entry in `state/built.json` still lists the same id. Run `node system/scripts/mcp-gen.mjs`. Say: "Close and reopen this project so the tool disappears."
4. **Reset channels.** For each channel in the entry's `channels`: set `config/autonomy.json` `channels.<name>.level` to `draft` (recommended) or `approve` if the user prefers. Remove any extra keys the blueprint added for that channel (for example `caps`, `quiet_hours`, `auto_rules`), after showing before and after.
5. **User-only steps.** For each one, give the exact clicks and add a task: `node system/scripts/tasks.mjs add "<step>" --tag remove-skill --priority medium`.
   - Scheduled task: "In the Claude app, open **Scheduled tasks**, find '<name>', and delete it." Always give this step when the build had a routine note or a schedule, and say plainly that pausing or deleting the note does not stop the job: only deleting the schedule on the host does (a Claude cloud routine: its page in the Claude app; a server: its own scheduler, for example the crontab line).
   - Key: offer to open the keys file (Windows `notepad .env.local`, Mac `open -e .env.local`, run in the background after a yes), then: "Delete the line that starts with `<NAME>=`, save and close." Never ask them to paste it.
6. **Update the records.**
   - `node system/scripts/built.mjs remove <name> --delete-files`. This forgets the entry and deletes its `my-*` skill folder and agent file. It lists anything it kept.
   - The proposal card: `status: "removed"`.
   - `node system/scripts/proposals.mjs mark <key> rejected` (so it isn't suggested again).
   - Tick any open `#ab/build` or `#ab/propose` tasks for it.
7. **Check and save.** Run `node system/scripts/validate.mjs` (it must still pass), then `node system/scripts/git-auto.mjs commit`.
8. **Tell the user** in 3 lines: what was removed, what they still need to do (if anything), and "Changed your mind? Say 'build <name>' and I'll set it up again. A copy also stays in your backup history."

## Outputs

- Deleted: the entry's `my-*` skill or agent files, and a routine note only if the user chose delete. Paused: a routine note the user chose to keep (`status: "paused"`).
- Updated: `config/mcp.selected.json` + `.mcp.json`, `config/autonomy.json` (channels back to draft), `state/built.json`, `state/proposals.json`, the proposal card (`status: "removed"`).
- Tasks tagged `#ab/remove-skill` for steps only the user can do.

## Safety

- Always show the plan and get a yes before deleting.
- Only `my-*` files and paths recorded for this build. Never framework files, never raw sources, never the user's notes.
- Removing a sending add-on always puts its channel back to `draft` or `approve`, never leaves `auto`.
- Never handle keys or passwords; the user edits `.env.local` themselves.
