---
name: docs-curation
description: "Use when pruning or restructuring a repository's docs."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [docs, documentation, cleanup, links, adr]
    related_skills: [kernel-clean-code, kernel-git-commit, project-operations]
---

# Pruning a repo's docs

"Clean up the docs, remove what isn't necessary" is a deletion task with a
correctness condition: **nothing that still governs behaviour may leave, and
every link must still resolve.** The failure mode is quiet — a deleted page that
another page links to, or a decision that lived only in the page you removed.

## When to Use

- Docs have accumulated proposals, plans and convention files that no longer
  describe the system.
- Renaming or deleting a doc, a task file, an ADR or a design folder.
- A docs tree is heavy with binaries, mockups or screenshots.
- Someone asks which docs are still true.

## Procedure

1. **Inventory with sizes and headings, not filenames.** Line count plus the
   first `#` heading per file tells you what a doc claims to be:

   ```bash
   for f in docs/*.md docs/**/*.md; do
     printf '%5s  %s  %s\n' "$(wc -l < "$f")" "$f" "$(grep -m1 '^#' "$f")"
   done
   ```

2. **Classify every doc into one of five states** before deciding anything:

   | State            | Test                                                                 | Action                                     |
   | ---------------- | -------------------------------------------------------------------- | ------------------------------------------ |
   | Current          | describes the code as it is                                          | keep                                       |
   | Shipped proposal | a design doc whose plan is now implemented                           | delete, after moving the durable decisions |
   | Dead system      | describes something removed (a renamed subsystem, a parked platform) | delete                                     |
   | Drifted          | names files, flags or paths that no longer exist                     | repair or delete                           |
   | Archive          | completed task files, ADRs                                           | keep                                       |

3. **Find the decision before deleting the page.** A proposal doc usually holds
   two different things: a plan (expendable) and the reasons a current behaviour
   is the way it is (not expendable). Move the reasons into the doc that governs
   behaviour — the dashboard doc for a UI decision, the ADR for an architecture
   decision — then delete the plan. Deleting a shipped proposal without
   relocating its rationale destroys the only explanation of a design nobody will
   otherwise question.

4. **Find every inbound link before removing a file.** Deletions break _other_
   pages, including ones you are not editing:

   ```bash
   grep -rn 'the-deleted-file\.md' --include='*.md' . | grep -v node_modules
   ```

   Typical hiding places: an index/README table, an ADR's "open items" section,
   and completed task files that cross-reference the plan they answered.

5. **Delete, then run the link sweep** (`scripts/check-doc-links.mjs`). It
   resolves every relative markdown link and exits non-zero on a dangling one,
   so it is the only proof the tree is still navigable.

6. **When a whole subsystem goes, delete its pages and rewrite the survivors.**
   A page whose _subject_ was removed (the dashboard guide, its conventions
   file, the observability page) is deleted, not edited. Pages that merely
   _mention_ it are rewritten if their structure still assumes it — a README
   whose layout block, setup commands and prerequisites all describe the deleted
   component is a rewrite, because patching three sentences leaves the rest
   lying. Measure it: count the hits for the removed identifiers
   (`apps/web`, the database name, the deleted package) per file; one or two
   mentions is a patch, a page half-built around it is a rewrite.

7. **An ADR whose decision was reversed is superseded, not deleted.** Add a
   `> **Superseded (date).**` block at the top naming what replaced it and why
   the code is gone, and keep the reasoning. Deleting it loses the argument; the
   conventions file that followed the dead system still goes.

8. **Update the index in the same commit.** A contents table that lists deleted
   pages is worse than no table: it advertises what is gone.

9. **Commit as one `docs(...)` change** with the reason per file, not a list of
   paths. If the prune is pushed, confirm the target remote is this project's
   repo before pushing — see `kernel-git-commit` for message rules and the
   pre-push gate.

## Stale is not the same as old

Age is not evidence. Two docs both saying `status: todo` after two months do not
have the same status:

- **Check the anchors, then decide.** A plan citing `path/to/file.ext`,
  `SymbolName` or a CSS class that no longer exists anywhere in the repo is an
  instruction for deleted code — delete it or rewrite it against the current
  file. A plan whose anchors still resolve is backlog: leave it, and say you left
  it, rather than silently deleting the user's intentions.
- **Keep the budgets, drop the plan.** A conventions doc derived from a dead plan
  (timing budgets, storage rules, prompt discipline) is still live guidance. Port
  the rules into the conventions doc, note that its source is gone, and delete
  the plan.
- **An empty scaffold is not an implemented plan.** `packages/x/src` existing
  with no files and no commits means the decision is still open; verify with
  `git log -- <path>` before calling a task done or stale.

## Deleting docs that carry binaries

Mockups and screenshots are the heaviest, least durable docs in a repo. Delete a
mockup folder once the feature ships — the running app is the reference, and a
screenshot of it goes stale with the next CSS change. Report the size removed;
that number is the justification.

## Pitfalls

- **A policy doc that no code reads is prose, not a contract.** Before treating a doc as the home of a
  rule, grep the source for its filename and for the identifiers it defines. If nothing loads it, the
  rule only holds while someone remembers it: move the durable part next to the mechanism (a registry
  field, a schema default, a validation message) and keep the doc as explanation — or delete it. A doc
  can be current, coherent and still be the reason the rule drifts, because nothing fails when it does.
- **A relocated decision must land where a future reader looks**, not in the
  commit message. Commit bodies are archaeology; the dashboard doc and the ADR
  are where someone actually reads.
- **Scripted link rewrites get depth wrong.** A `../adr/x.md` replacement applied
  from `docs/tasks/done/` needs `../../adr/x.md`; the fix looks right and 404s.
  Always re-run the sweep after the fix pass and read its output instead of
  trusting that the replacement was correct.
- **Keep the archive.** `done/` and `adr/` are the record of how the system got
  here; pruning removes instructions, not history. A parked ADR stays even when
  its implementation plan and conventions file are deleted — mark it parked and
  say the plan is gone.
- **Docs that advertise a withdrawn capability are worse than missing docs.**
  When a feature leaves the code in the same change, its page and every sentence
  promising it must leave too — including a skill's own `SKILL.md`
  (`description:` included). The next session trusts the doc, spends an hour
  implementing against it, and finds the entry point gone. Grep the docs, the
  AGENTS.md and the skill bodies for the capability's name before you call the
  removal done.
- **A retired system's conventions file follows it out.** Conventions for a
  platform that does not exist (a shell that was never built, a vault that became
  a different root) are dead guidance; delete them with the plan.
- **Do not "clean" prose you are not deleting.** Mentions of a removed system in
  a current doc are usually deliberate explanations of the rename; rewrite the
  ones that read as instructions ("attach X") and leave the ones that read as
  history ("X was replaced by Y").
- **Docs never fail the build, so drift is silent.** Nothing catches a stale page
  except the link sweep and a grep for the identifiers the page names.

## Files

- `scripts/check-doc-links.mjs` — resolve every relative markdown link under a
  root, suggest the correct path when only the depth is wrong, exit 1 on any
  dangling target.
