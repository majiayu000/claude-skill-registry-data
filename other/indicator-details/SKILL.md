---
name: indicator-details
description: Returns the notes Trade Stories holds on a named indicator, or lists the indicators that have notes.
argument-hint: "[indicator name]"
---

# Print an indicator's notes

Follow **Operating rules** in `${CLAUDE_SKILL_DIR}/../../story-skills.md`, and
nothing else in that file. No story is involved: look for none, and run nothing
under `dsl/`.

The notes are in `${CLAUDE_SKILL_DIR}/../../../extras/indicators/`. Read its
`README.md` first. Beyond that, read only what the step for this run names.

Print only the lines below, and nothing you know about an indicator from
anywhere else: no progress line, no opening line, and no comment before or
after them.

## No argument

List the subfolders. For each one holding an `indicator.md`, read that file's
`#` title and print one line, in alphabetical order, the folder name first:

```
<folder name>: <title>
```

So `quadzilla-tf`, titled `# Quadzilla TF`, prints `quadzilla-tf: Quadzilla TF`.

With no subfolder holding an `indicator.md`, print this line alone:

```
The indicator notes folder holds no notes yet.
```

## A name

Resolve the argument against the subfolders as the README says, taking the
argument as the name a story would give.

A match: read every file in the matched folder, then print one line naming the
indicator by its `indicator.md` title, then `indicator.md`, then each other file
in alphabetical order, after a line naming it:

```
Notes on <title>:
<indicator.md>
<file name>:
<that file>
```

Print every file whole and exactly as written, with nothing summarised or
reworded.

No match: print this line, then the list under **No argument**:

```
No notes are held for <argument as given>.
```
