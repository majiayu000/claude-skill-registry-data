---
name: update
version: 1.0.0
description: "Bring this marketing folder up to date with the latest skills and templates from the Compound Marketing starter kit, keeping your own changes. Trigger with /update or when the user mentions 'update compound marketing,' 'get the latest skills,' 'pull updates,' 'upgrade,' or 'is there a new version.'"
---

# Update

Pull the latest starter kit and apply its changes to this folder. Every file gets a three-way comparison: the kit version this folder was built from, the kit now, and the file here. Files you never touched take the new version. Files you changed (including Learnings that `/reflect` added) get the kit's changes merged in around your edits. When you and the kit changed the same lines, you decide.

Brain content (`truth.md`, `personas.md`, and the rest) is never modified. New brain files are added.

The script lives next to this file. Call it `$UPDATE`: `.claude/skills/update/update.sh`, or `.agents/skills/update/update.sh` when `.compound-marketing.yml` says `primary_runtime: codex`. Run it from the folder root.

---

## Workflow

### Step 1: Save current work

Run `git status --porcelain`. If anything is uncommitted, show it and offer to commit it first ("Save work before update"). The update needs a clean folder so it can be undone in one step. If `.update-conflicts/` is there, a previous update wasn't finished. Go to Step 4 and resolve it before anything else.

### Step 2: Preview

Run `$UPDATE plan`. It pulls the latest starter kit, then lists what would change without touching anything.

If it can't find the starter kit, ask where the user downloaded `compound-marketing`, then rerun with the path: `$UPDATE plan /path/to/compound-marketing`. Pass the same path to `apply`. After this update, the path is saved and won't be needed again.

Explain the plan in plain language, grouped:

| Line | Meaning |
|------|---------|
| `NEW` | New skill or file from the kit |
| `UPDATED` | You never changed it; it takes the new version |
| `MERGED` | You both changed it in different places; both sets of changes kept |
| `CONFLICT` | You both changed the same lines; you'll choose |
| `REMOVED` | The kit dropped it and you never changed it |
| `KEPT` | The kit dropped it, but you changed it, so it stays |
| `SKIPPED` | You deleted it; it stays deleted |

For new skills, read each new `SKILL.md` description and say in a line what it does. If the output starts with `BASE guessed`, mention that this folder predates version tracking, so the tool estimated its starting point from the folder's creation date. If no change lines appear, say the folder is up to date and stop.

Ask: "Apply these updates?"

### Step 3: Apply

Run `$UPDATE apply`. It makes the changes, rebuilds the Codex/Claude mirror (`AGENTS.md`/`CLAUDE.md` and the second skills folder), and records the new starter kit version.

### Step 4: Resolve conflicts

For each `CONFLICT`, the script left the real file alone and wrote a marked-up version to `.update-conflicts/<same path>`. Between `<<<<<<< yours` and `=======` is this folder's version; between `=======` and `>>>>>>> starter-kit` is the kit's.

For each one:

1. Explain both versions in plain words: what the user's edit does, what the kit's change does.
2. Recommend a resolution. Usually that keeps the user's intent and takes the kit's new content.
3. On approval, write the resolved text to the real file and delete its conflict copy.

When `.update-conflicts/` is empty, delete it. If any skill files were edited here, run `/sync-skills` so the second runtime's copy matches.

### Step 5: Review and commit

Show `git status --short` and a one-line summary per changed area. Commit with the message `Update Compound Marketing to <first 7 characters of starter_kit_version>`. Tell the user they can undo the whole update with `git reset --hard HEAD~1`.

---

## Rules

- **Never commit while `.update-conflicts/` exists.** The recorded version has already moved forward, so the next update won't flag those files again.
- **Never edit the starter kit folder.** If the pull fails because it has local changes, tell the user and stop.
- **Never hand-edit brain content during an update.** New brain files only.
- **Don't add the `setup` skill.** It belongs to the starter kit only; the script skips it.

## Learnings

<!-- Updated by /reflect in your instance. Promote stable patterns to the main skill body. Ships empty. -->
