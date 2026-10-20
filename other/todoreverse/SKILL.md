---
name: todoReverse
description: "The reverse of the normal flow: turn a piece of work that was done straight through the terminal WITHOUT a todo item — a hotfix, a quick 'fix this' with its corrections — into an item in the user's todo file (TODO.<git user.name>.md, resolved as in the todo rules) after the fact. Distills that dialog into its ideal prompt (same rules as /todoIdealPrompt), appends it with the next id as a done `- [x] #N` item (or open with --open), and adds the `[<name>#N]` markers at the change sites of that dialog so the code can be traced back to it. Use when the user wants an untracked dialog recorded in the todo — phrases like '/todoReverse', 'make a todo item from what we just did', 'record this hotfix in the todo', 'reverse prompt', 'add what we just fixed to my todo', 'create the prompt for this fix'. This skill IS allowed to edit the user's todo file and to add markers in the code changed by that dialog; that is its purpose."
argument-hint: "[words identifying the dialog] [--open]"
allowed-tools: Read, Edit, Glob, Grep, Bash(git config:*), Bash(git status:*), Bash(git diff:*), Bash(git log:*)
---

# /todoReverse

Normal flow: the first prompt is a numbered item in the todo file, the terminal carries the
corrections, and `/todoIdealPrompt` writes the distilled prompt back into the item. A hotfix
skips the first step — the user types "fix the crash on the camera screen" straight into the
terminal, iterates, and ships it. Nothing in the todo file, no marker in the code, no prompt to
learn from. This skill closes that gap from the other end: it takes the untracked dialog and
creates the item it should have started from.

## Argument forms

```
/todoReverse                    # the most recent untracked dialog in this session
/todoReverse camera crash       # the untracked dialog those words identify, when there are several
/todoReverse --open             # append as an open item `- [ ] #N …` (default is done, `[x]`)
```

`--open` is for a hotfix still being verified: the item is then "the item most recently
worked", so a following confirm word (`works` / `fixed`) ticks it and re-idealizes it the
usual way.

## What Claude does

1. **Resolve the dialog.** An *untracked dialog* is a stretch of this session where code or
   docs were changed without a `#N` / `#new…` / pasted-item prompt starting it. Take the most
   recent one; with a hint argument, the one those words identify. If none exists, say so and
   stop. If several are plausible and no hint was given, list them — at most 3, one line each —
   and ask. If an item for that dialog was already created (by an earlier `/todoReverse`, or
   because the user typed a `#N` for it midway), say which and stop: never a duplicate.

2. **Resolve and read the user's todo file** — `TODO.<name>.md` at the repo root, `<name>` from
   `git config user.name` (the rule in `.claude/prompt-todo/RULES.md`). Never another user's
   file. Run the Autoincrement rule first, as on any touch. Next id = highest `#N` across the
   file and `TODO.<name>.archive.md` (if present), plus one. Edit tool only, never the shell.

3. **Distill the ideal prompt** from the dialog with the `/todoIdealPrompt` rules: the user's
   first message, every correction, the accepted result; a few typeable lines, ~60 words max;
   the intent, the constraints that only surfaced through iteration, the decisions Claude
   would otherwise guess wrong — nothing the codebase or the project's rules already carry.
   Imperative, in the user's own vocabulary.

4. **Derive the prefix** from the dialog, in this order after the id: a ticket key if one was
   named (`PROJ-123`), then a tag from the tag table in the todo rules if the work was clearly
   scoped to one (`IOS:`, `Android:`, `Web:`, `IOS+:` …). Never invent either.

5. **Append the item** at the end of the todo file:

   ```
   - [x] #N KEY TAG: <first line of the ideal prompt>
     - <each further line as an indented sub-bullet>
   ```

   While the **Line width** rule in `.claude/prompt-todo/RULES.md` is on, every line stays
   within its limit, prefix and score included — split at a clause boundary, never mid-word.
   `[x]` by default — the work is done and the user is recording it; `[ ]` with `--open`. If
   the dialog sat under an existing `## KEY — …` ticket block in the file, append the item
   under that block instead of at the end. While the **Prompt scores** rule in
   `.claude/prompt-todo/RULES.md` is on, the item line ends with ` (N/5)`: the dialog's first
   terminal message is the original prompt, scored as `/todoIdealPrompt` would.

6. **Add the markers** — only while the **Code markers** rule in `.claude/prompt-todo/RULES.md`
   is on; when it says markers are off (`/todoMarkCode off`), skip this step and say so in the
   reply. For every principal change site of that dialog — files this session
   changed for it, still in the working tree or in this session's commits — append
   `[<name>#N]` to the comment the change already carries, or to the comment that change
   warrants; never a bare marker-only comment where none is justified (the **Code markers**
   rule). A site already marked for another item gets the id added: `[jd#16 jd#N]`. Skip a
   site rather than guess; list what was skipped. This is the whole point of the reverse flow —
   without it `grep "\[jd#N\]"` finds nothing.

7. **Reply** with: the new item as written, the files that received markers (one line each),
   the 3–6 feedback bullets `/todoIdealPrompt` would give — what the terminal prompt lacked
   that the ideal prompt states — and, when `--open` was used, that a confirm word now refers
   to this item.

## Notes

- Ids are never renumbered or reused; the appended item takes the next id like any other.
- The dialog itself is not edited or summarised anywhere else; the todo file is the record.
- If the dialog's changes were already committed, the markers land as an uncommitted edit —
  say so; this skill never commits.
- A dialog that was only investigation (no change accepted) is recorded as `[x]` with the
  distilled question as its prompt only if the user asks; by default say there is nothing to
  trace and stop.
