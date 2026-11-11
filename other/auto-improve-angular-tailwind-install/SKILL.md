---
name: auto-improve-angular-tailwind-install
description: "Install the angular-tailwind add-on of the agentic-auto-improve plugin in this project: four rule documents (Angular code, Angular Material, Tailwind styling, UI patterns) copied into .claude/references/angular-tailwind/ and listed in the project profile's review.documents slot, plus, on request, the scroll-edge classes appended to the project's global stylesheet. Installs no hook and writes no settings.json row. Previews the files and the profile change, asks for one confirmation, then writes. The name carries the plugin name because you may have several plugins installed. Use when: user says /auto-improve-angular-tailwind-install, 'install the angular tailwind add-on', 'add the Angular and Tailwind rule documents', or 'turn on the UI rules'. Never overwrites a file that differs and never removes a row."
user_invocable: true
---

# /auto-improve-angular-tailwind-install — install the angular-tailwind add-on

The `angular-tailwind` add-on gives a project the Angular and Tailwind rule documents. It copies four markdown files into `.claude/references/angular-tailwind/` and lists them in the project profile's `review.documents` slot, so the agents that read that slot find them. It is for projects built with Angular and Tailwind. Nothing registers it by default.

It starts no program on any prompt. The old prompt hook of this add-on is **disabled**: its script still ships, but this install never copies it and never writes its row. The edit-time guard `architecture-guard.py` stays the enforcement.

This skill proposes first. It writes only after one yes, and it reads and touches only
`agentic-auto-improve`.

## The rule that shapes everything here

**The skill carries the conversation. The script carries every rule.**

Which files are copied, which rows are written, what is already there, and what is refused all
live in `auto_improve_finish_install.py addon`, which has its own test suite. Read its answer.
Do not work any of it out yourself, and never edit `settings.json` by hand to install this
add-on: a typing mistake there can switch every check off, or block every action.

The script never removes a row or a file. It never overwrites a file that differs from the
plugin's copy. It copies a helper file only when the project lacks it. In the project profile it
writes exactly one thing: it appends its own document paths to the `review.documents` slot. It
changes no other slot and no other entry in that slot. In a stylesheet it writes exactly one thing, and
only when you name the file: the scroll-edge snippet, appended at the end.

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

Every command below is `$PY "$FI" addon --name angular-tailwind --project . ...`.

## What this add-on does

Four rule documents, each one a short list of rules with a stable Rule ID (`A-nnn` Angular code, `M-nnn` Material, `T-nnn` Tailwind and styling, `P-nnn` patterns):

- `ANGULAR_CODE_RULES.md`
- `ANGULAR_MATERIAL_RULES.md`
- `TAILWINDCSS_RULES.md`
- `UI-UX-PATTERNS.md`

The install copies them verbatim into `.claude/references/angular-tailwind/`. The project never edits them. Project facts in them are placeholders that point at profile slots or at the project's own documents. The install then lists the four paths in the profile's `review.documents` slot, so a reviewer or an implementer reads them with the rest of that list. The guard's block and warn lines name the Rule ID, and name the document when it is installed here.

The install writes **no hook file and no `settings.json` row**, and the add-on declares **no kill switch**. Nothing starts on a prompt. The old prompt hook (`angular-tailwind-advisor.py`, once `architecture-advisor.py`) is a disabled hook of this add-on: see `DISABLED.md` in the add-on folder for what it did, what it cost and how to turn it back on.

It needs one helper, `.claude/hooks/_project_paths.py`, which the install copies only if the project lacks it.

It also carries a small stylesheet snippet: three classes, `.scroll-edge`, `.scroll-edge-content` and `.scroll-edge-header`,
that the scroll container pattern (`UI-UX-PATTERNS.md`) and the guard's scroll-edge rule rely on. The header background is the
setting `--scroll-edge-header-bg` (default: the Material surface colour). The wrapper has no `overflow-hidden`; add it on the
element yourself if you want it. The snippet goes at the end of the project's global stylesheet, after Tailwind and the theme
bridge, between the comments `/* agentic-auto-improve:scroll-edge begin */` and `... end */`.

## Step 1: Preview (writes nothing)

```bash
$PY "$FI" addon --name angular-tailwind --project . --json
```

Without `--stylesheet` the preview only lists candidates and writes nothing: the answer's `stylesheet.candidates` holds each
`frontend.roots` entry's `src/styles.scss` or `src/styles.css` that exists. If there is one candidate, recommend it. If there are
several, or none, ask the user which file is the global stylesheet (the one that imports Tailwind). Then run the preview again
with the choice (repeat the option for more than one file); an answer of "none" skips the snippet:

```bash
$PY "$FI" addon --name angular-tailwind --project . --stylesheet <relative path> --json
```

`stylesheet.targets` then says, for each file, `append` (none of the three classes is defined, so the snippet would be added) or
`present` (all three are defined already, by this install or by the project; the file is not touched), and
`stylesheet.unified-diff` shows the appended text.

The answer carries `files` (each file with its kind, `document` or `helper`, and its action: `copy`, `present` or `keep-existing`),
`profile` (the `review.documents` slot: `adds` the paths it would append, `already-listed` the paths it skips, `before` and `after`
the slot text, and a `unified-diff`), `to-add` (settings rows; empty for this add-on), `notes`, `kill-switches` (empty),
`disabled-hooks`, `retire`, `target`, `plugin-root` and `plan-sha256`.
**Keep `plan-sha256`.** The apply needs it as `--expect-sha256`. It covers the settings bytes, the profile bytes before and
after, the bytes of each named stylesheet before and after, and every file the install would copy, so anything that moves between
the preview and the write is refused as `changed-since-preview`.

How the slot is written: a slot that still holds its placeholder, or `none`, becomes the list of the four paths. A slot the team
wrote keeps its text, and the missing paths are appended after it. A path that is already listed (with or without backticks,
with either slash) is skipped. When all four are listed, the profile is not written at all.

## Step 2: Show the plan and ask once

Show the user, in plain words:

- the documents it would copy into `.claude/references/angular-tailwind/`, and any helper into `.claude/hooks/`, with the
  action for each. A file marked `present` is already identical and is not touched. A helper marked `keep-existing` is kept as it is.
- the `profile` change: the slot before, the slot after, and the `unified-diff`.
- the `stylesheet` change, when a file was named: which file gets the snippet, or that it already defines the classes.
  The removal never takes the snippet out again, so say that it stays in the stylesheet after an uninstall.
- that no hook is installed and no row is written to `settings.json`.
- any `notes`.

State your recommendation first, in one or two sentences. Then ask **once**: install this
add-on?

No new session is needed for the documents to be found: they are files, read when an agent reads `review.documents`.

Declining writes nothing.

## Step 3: Apply

On a yes, apply with the `plan-sha256` from the preview:

```bash
$PY "$FI" addon --name angular-tailwind --project . [--stylesheet <relative path>] --apply --expect-sha256 <plan-sha256 from the preview>
```

Pass the same `--stylesheet` options as in the preview that gave the hash; the hash covers them.

The script copies the documents first, then updates the profile, then appends the snippet, so the profile never lists a file that is not there.
`settings.json` is not touched, so there is no backup to print. The answer lists `copied`, `registered` (the paths appended to the slot)
and `stylesheets` (the files the snippet was appended to).

If the answer says `nothing-to-do`, the add-on was already installed. Nothing was written.

### Refusals

Exit `2` is a refusal you can correct. Exit `3` is an environment problem, such as an add-on
folder with no `addon.json`. On either, read `code` and `message`, tell the user the reason in
one plain sentence, and stop. A refusal always means nothing was changed. The ones you may see:

- `profile-slot-missing`: the project has no `.claude/project-profile.md`, or the profile has no
  `review.documents` row. Nothing was written, not even the documents. Tell the user to run
  `/auto-improve-finish-install` first (it writes the profile), then run this skill again.
- `disabled-hook-present`: the project carries a row for the retired advisor in `.claude/settings.local.json` (this install does not write that layer), or an edited copy of the advisor together with a row that names it in `.claude/settings.json` (removing the row would switch off the user's edits). The advisor is `.claude/hooks/angular-tailwind-advisor.py`, or `.claude/hooks/architecture-advisor.py` under its former name. Name what the message names. Nothing was written. Tell the user to run `/auto-improve-angular-tailwind-uninstall` first, which removes the row and then the file (it keeps an edited file), then run this skill again. Do not delete the row or the file yourself: a row left pointing at a missing script blocks every prompt.
- **A retired advisor in `.claude/settings.json` is not a refusal any more.** The install retires it in two steps (issue #262), exactly like the codegraph add-on's two old hooks:
  - **Step A.** The preview's `retire` entry has `step` `A`. The run removes the advisor's `UserPromptSubmit` row (under either file name) and deletes no file. Say so, and say: **start a new session, then run this install again to delete the leftover file.** A session that is already open still holds the row, and a plain row (written before the Project hook launcher) that names a missing script exits 2 and blocks every prompt.
  - **Step B.** A later run, when no row names the advisor, deletes the file if it is an unedited released copy. An edited copy is kept and listed. When `retire.confirm-new-session` is true, ask once, before you apply: "Have you started a new session since the last install run?" On a no, add `--keep-retired-files` to the preview and the apply, and tell the user to re-run after restarting.
- `addon-file-differs`: one of the four documents already exists in the project and is not the
  plugin's copy. Name the file. The script will not overwrite it. The user compares it with the
  plugin's copy and renames or removes it by hand, then runs this skill again.
- `stylesheet-partial-snippet`: the named stylesheet defines some of the three classes and not the others, or holds the snippet's
  markers without all three classes. Nothing was written, not even the documents. Name the file and the classes the message says are
  missing. The user adds the missing class by hand (copy it from `.claude/addons/angular-tailwind/snippets/scroll-edge.scss` in the
  plugin) or removes the half-installed block, then runs this skill again. Do not edit the stylesheet yourself.
- `stylesheet-missing`: the named path is not a file inside the project. Nothing was written. Ask for the right path (the preview lists
  the candidates).
- `changed-since-preview`: something moved after the preview. Go back to the preview, show the
  new plan, and ask again. Never reuse the old hash.
- `write-failed`: for example `.claude/settings.json` is a symbolic link. Nothing was written.
  Tell the user to edit the file the link points to by hand.
- `plugin-source-checkout`: this folder is the plugin's own checkout. Install an add-on in a
  project that uses the plugin instead.
- `addon-unknown`: the name matches no add-on folder in the plugin.

## How to remove it

This install never removes anything. The removal is its own skill, `/auto-improve-angular-tailwind-uninstall`. It leaves the
stylesheet snippet where it is, because the snippet lives in the project's own stylesheet; delete the block between the two marker
comments by hand if you want it gone.
It also cleans a project that installed the old advisor hook under either of its file names, which is
the route `disabled-hook-present` names for the cases the install cannot retire itself.

## Closing

End with a short summary: what was copied, which paths were registered in `review.documents`, and what was
**not** written and why (no hook, no row, no `settings.json`), and whether the stylesheet snippet was appended or skipped. Say that
running this skill again changes nothing: identical files are left alone, a path that is already listed is not listed twice, and a
stylesheet that defines the classes is not touched. If the snippet was appended, remind the user that Tailwind 4's `@apply` in it is
checked by the project's own build, not by this install: run the build once.

## Anti-patterns

- **Telling the user the documents enforce anything.** They state the rules. The architecture guard enforces
  what it checks, and for those rules its verdict is final.
- **Offering a kill switch or an environment variable for this add-on.** It declares none, and it starts nothing.
- **Writing a hook row or a `settings.json` entry for this add-on.** Its hook is disabled; the script writes no row.
- **Writing the profile by hand to list the documents.** Use the script: it compares paths and skips the ones already listed.
- **Writing without the preview's `plan-sha256`**, or with an old one. The hash is what proves the user saw the
  change as it is now.
- **Hand-editing `settings.json` or deleting the old advisor row or file yourself.** Run the uninstall skill:
  it removes the row first, because a row that points at a missing script blocks every prompt.
- **Overwriting a document that differs.** The script refuses; do not copy over it yourself.
- **Choosing the stylesheet for the user, or appending the snippet by hand.** Offer the candidates and let the user pick; the script
  decides whether the classes are already defined and writes the block between its markers.

## When NOT to use

- To turn on the check that blocks a bad write. That is `architecture-guard.py`, already a default hook.
- To change the rules the documents state. They belong to the add-on's `documents/` folder in the plugin.
- To get the prompt reminder back. See `DISABLED.md` in the add-on folder.
- Inside the plugin's own checkout. The script refuses it as `plugin-source-checkout`.
- On Cursor or Codex. Hooks are Claude-only in this release.
