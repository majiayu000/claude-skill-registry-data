---
name: move-and-repoint
description: >-
  When a file or folder is moved, renamed, or retired, find every reference to it, repoint the living
  documents to the new location, and leave historical records citing the old name untouched. Use before and
  after any move or rename that other files point at, and when cleaning up broken links after a
  reorganization. Trigger phrases include "rename X to Y", "move this folder", "fix the references", "repoint
  the links", "clean up after the move", "we have broken links", "this doc moved". Does NOT rewrite the
  content of historical records, and does not decide on its own to retire a document.
license: Apache-2.0
metadata:
  author: Marc Taccolini
  version: 1.1.0
---

# Move and Repoint

A rename is never one change. Every file that points at the old name breaks, and most of those pointers
are not markdown links a link checker can see: they are backticked paths in prose, script arguments,
config values, and skill files. This skill makes a move a single coordinated operation.

## The one rule

**Records are history. Living documents are navigation.**

- **Living documents** (README, specs, `CLAUDE.md`, skill and agent files, configs, scripts, the current
  tracker) get repointed to the new location.
- **Records** (session notes, changelog entries, decision logs, dated reports, anything written to say
  what was true on a given day) are left exactly as they are. They cite the old name because the old name
  was correct when they were written. Rewriting them falsifies the history.

When a living document is wrong, correct its text in place; git keeps the old version. Do not stack
"superseded" banners on top of living documents. A banner belongs only on a record that has been
overtaken, and even then one line is enough.

## Procedure

1. **The change set.** List each move as `old/path -> new/path`.
2. **Find every referrer, BEFORE moving.** Search by the bare file or folder name, not by the full path:
   `grep -rn "old-name" .` A full-path search misses relative links (`../docs/old-name.md`) and
   backticked mentions, so it reports clean when it is not. Include scripts, hooks, CI config, and
   `.claude/` (skills, agents, settings): a moved folder that a script reads breaks silently at run time.
3. **Classify each hit** as living, record, or generated. Generated files (indexes, built docs) are fixed by
   re-running the generator, never by hand.
4. **Move and repoint as one operation.** Apply each move together with every living-document fix it
   needs, in dependency order. Never split one rename across parallel sessions or agents: they race on the
   same referrers.
5. **Search again.** Re-run the step 2 search after the move. Zero living hits is the done test, and a
   link checker passing is not.
6. **Report.** Repointed (paths), records left untouched (count), and anything that needs a person (a
   reference inside content whose meaning, not just location, changes).

## Reading an old pointer

The inverse case: you find a path in a record and the file is not there. That is expected, not evidence
the file is lost. Before concluding anything, resolve the name across the whole repository and try the
routine transformations: moved into a subfolder, a draft that was promoted (`DRAFT-x.md` to `x.md`), a
dated file that became a living one (`x-2026-07-07.md` to `x.md`). In practice nearly all such pointers
resolve this way, and a literal path check raises mostly false alarms.

If a pointer truly resolves nowhere, the record holding it may be the last copy of that detail. Say so;
do not trim it.

## Ask first when

- The edit touches what a document says, not only where it points.
- The document is published outside the repository, or other people depend on its address.
- The file being retired is still referenced by something you cannot update.
