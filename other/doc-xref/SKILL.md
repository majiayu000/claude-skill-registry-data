---
name: doc-xref
description: >-
  User-invoked as /doc-xref <target>. Finds every inbound reference to a doc
  path, heading/anchor, or code symbol - across docs/ AND src/ docstrings and
  comments - so a rename, move, split, or reworded section propagates everywhere.
  Use before renaming/moving/splitting docs or public symbols.
allowed-tools: Grep, Glob, Read, Edit, Bash
invocation: /doc-xref <target>
---

# Doc Cross-Reference

Find and update everything that points **at** `$ARGUMENTS` (a doc path, a heading
text/anchor, or a public symbol). Complements `/link-check`, which validates a
file's *outbound* links; this finds *inbound* references so a change propagates
instead of leaving stale pointers.

## Steps

1. Enumerate inbound references across both trees:
   - **Docs**: links `](<path-or-anchor>)`, bare path mentions, and prose mentions
     of the heading/title in `docs/**`, repo-root `*.md`, and `.claude/**`.
   - **Code**: docstring / comment pointers in `src/**` and `tests/**` (e.g.
     ``See docs/specs/PRODUCTION_DESIGN_SPEC.md §6.4``), plus the symbol name itself
     when the target is a symbol.
   ```bash
   git grep -nF "<target>"   # exact path / anchor / symbol; repeat for old name + anchor
   ```
2. **Rename/move**: update every hit to the new path/anchor; `git mv` when renaming
   a whole file so history follows.
3. **Reworded section**: update mentions whose surrounding text now misstates the
   section (registry descriptions, "see X" summaries, titles).
4. Update the `docs/README.md` registry line if a file was added/renamed/removed.
5. Verify with `/link-check` (or `python scripts/check_doc_links.py`).

## Output

List each reference updated (`file:line`, old → new) and confirm `/link-check`
passes. Flag any reference you could not safely auto-update for human review.
