---
name: resolve-conflicts-by-intent
description: 'Use when Git reports conflicts during a merge, a rebase, or a cherry-pick. Also use it when the user says "fix the merge conflicts", "rebase onto main", or "the merge broke the build". Traces each side of a conflict to the change that it came from. Keeps both intents when they fit together, and asks when they do not. Then runs the checks on the combined result. Not for choosing what a new behavior should be (use `choose-by-consequence`).'
metadata:
  shadowclone-category: version-control
  shadowclone-section: workflow
  shadowclone-applies-when: while a merge, rebase, or cherry-pick has conflicts
---
# Resolve Conflicts by Intent

## Use when

A merge, a rebase, or a cherry-pick stops with conflicted files. Each side of a conflict carries an intent. A correct resolution keeps each intent that still applies.

## Gates

1. For each conflicted file, can you name the commit and the intent behind each side?
2. Does the resolution keep both intents when they fit together?
3. When the intents do not fit together, did you ask the user instead of picking one?
4. Did you check related names and code outside the conflict markers?
5. Do the checks pass on the combined result, and did you separate failures that were already on a parent?
6. Are all conflict markers gone, with no file left unmerged?

## Process

1. Read the operation in progress, the conflicted paths, and the commits on each side.
2. For each side, read the commit message, the tests, and the design notes that explain it.
3. Resolve each conflict in the current design. Keep the compatible parts of both sides.
4. Search the rest of the code for names and assumptions that either side changed.
5. Run the focused checks and the required merge check.
6. Read the combined diff against both intents, then finish the operation that the user asked for.

## Example

**Situation:** A rebase conflicts in a lock file. One side adds a package, and the other side updates a different package.
**Easy route:** Take one whole side of the lock file, because a tool writes it.
**Hidden cost:** One change is lost. The build passes on a machine that still has the old cache, and it fails for everyone else.
**Best route:** Take the lock file from the base branch. Apply the package change from the other side again, and run the install so that the tool writes the lock file.
**Evidence:** The new lock file has both packages. A clean install and the full check passed.

## Guardrails

- Take a whole side of a file only when nobody wants that side any more.
- Keep schema changes, migrations, generated files, and tests consistent with each other.
- Treat rename and delete conflicts as behavior changes.
- Do not add a third design that neither side asked for.
- Keep unrelated edits of the user, and follow the approval rules of the repository for Git operations.

## Completion

- Each conflicted file, with the intent that you kept from each side.
- The check that covers the combined behavior, with its result line.
- The operation that you finished, and the final commit hash.
