---
name: todoArchive
description: "Move every done ([x]) item out of the user's todo file (TODO.<git user.name>.md, resolved as in the todo rules) into TODO.<git user.name>.archive.md, verbatim, and report what moved. Done items are never deleted — the archive keeps the ids so the next id stays unique, and git picks the move up in the user's normal commits (no git checks, no commits by this skill). Use when the user wants to clean the done prompts out of the todo file — phrases like '/todoArchive', 'archive the done items', 'remove done prompts', 'clean up the todo', 'move done items out'. This skill IS allowed to edit the user's todo file and its archive; that is its purpose."
argument-hint: ""
allowed-tools: Read, Edit, Write, Glob, Grep, Bash(git config:*), Bash(bash .claude/prompt-todo/bin/py.sh:*)
---

# /todoArchive

Clears finished prompts out of the user's todo file without losing them: they move to the
archive file. "Remove" never means delete — the **Ids** rule in the todo rules
(`.claude/prompt-todo/RULES.md`) derives the next id from the highest id across the todo file
*and* its archive, so an archived item still pins its number. The archive is the history; git
records the move whenever the user next commits, so this skill neither checks git state nor
commits anything.

## What Claude does

1. **Resolve and read the user's todo file** — `TODO.<name>.md` at the repo root, `<name>`
   from `git config user.name` (the rule in the todo rules). Never another user's file. Run
   the Autoincrement rule first, as on any touch. Edit tool only.

2. **Collect the candidates**: every top-level `- [x]` / `- [X]` item together with the
   indented sub-bullets that belong to it. Rows carrying one of the ignore tags of the rules
   (`QA:` / `Admin:` by default) are candidates too once the user has ticked them: moving a
   row verbatim is not working, rewriting or ticking it, so the ignore rule is not broken.
   An open ignore row stays where it is like any other open item. If there are none, say so
   and stop.

3. **Move**: append the collected items, in file order and verbatim, to
   `TODO.<name>.archive.md` — create it with the header `# <projectTitle> — TODO archive` if it
   does not exist, where `<projectTitle>` is the `projectTitle` in
   `.claude/prompt-todo/config.json` (the same title the todo file's header uses) — then delete
   those lines from the todo file. Open items and the header stay exactly where they are. A
   `## KEY — …` ticket heading (and its `> ` excerpt line) is copied to the archive the first
   time one of its items moves, and removed from the todo file once no item is left under it.

4. **Reply with a summary**: the ids archived and the archive file path.

## Notes

- Never renumbers, edits or re-idealizes the items it moves; run `/todoIdealAll` before this
  if any done item still has its original text, since an archived item is never rewritten.
- The archive file is a normal tracked file once committed. Remind the user to include it in
  their next commit the first time it is created.
