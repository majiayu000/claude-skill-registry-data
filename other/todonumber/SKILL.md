---
name: todoNumber
description: "Assign ids on demand to the placeholder items in the user's todo file (TODO.<git user.name>.md, resolved as in the todo rules): every top-level `- [ ] #new …`, `- [ ] #newX …` or id-less `- [ ]` line gets the next id (highest #N present in the file and its archive, plus one), sloppy `- []` is normalised, and the token→id mapping is reported. Starts no work — it is the explicit form of the Autoincrement rule that otherwise runs on any touch. Use when the user just wants numbers — phrases like '/todoNumber', 'number the new items', 'assign ids', 'give the new prompts ids', 'what number did my new item get'. This skill IS allowed to edit the user's todo file; that is its purpose."
argument-hint: ""
allowed-tools: Read, Edit, Glob, Grep, Bash(git config:*)
---

# /todoNumber

The on-demand form of the **Autoincrement** rule in `.claude/prompt-todo/RULES.md`: give every
placeholder item in the user's todo file its id, report the mapping, and stop. Nothing is
worked, ticked or rewritten.

## What Claude does

1. **Resolve and read the user's todo file** — `TODO.<name>.md` at the repo root, `<name>`
   from `git config user.name`. Never another user's file. If `TODO.<name>.archive.md`
   exists, read it too: it takes part in finding the highest id.

2. **Find the next id**: the highest `#N` across the todo file and its archive, plus one.
   There is no counter line.

3. **Assign, top to bottom**, to every top-level `- [ ]` / `- []` line that has no `#N`:
   - `#new` or `#new<suffix>` → replaced by `#N`;
   - no `#` token at all → `#N ` inserted right after `- [ ] `;
   - `- []` → normalised to `- [ ] `;
   - a placeholder line indented under another item is a new item that landed in the wrong
     place (the IDE continued the parent's indentation): lift it to top level, keeping any
     detail lines that follow it as its own sub-bullets.
   One id per item, in file order; ids typed by hand are kept as written. Edit tool only.

4. **Remember the mapping** for the rest of the session — `#newCam` still resolves after it
   became `#27` — and **reply with it**: one line per item, `#newCam → #27  <first words>`, or
   "nothing to number" if no placeholder was found. Do not start work on any of them; if the
   user wants that, they type the id.

## Notes

- Same normalisation as the rule that runs on every touch, so running this first or letting
  the next prompt trigger it gives identical results.
- Never renumbers, reuses or reorders existing ids; never touches ignore rows (`QA:` /
  `Admin:` by default) beyond the id they may be missing.
