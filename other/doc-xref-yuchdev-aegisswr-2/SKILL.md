---
name: doc-xref
description: User-invoked as /doc-xref <target>. Finds every inbound reference to a doc path, heading/anchor, or code symbol - across docs/ AND src/ docstrings and comments - so a rename, move, split, or reworded section propagates everywhere. Use before renaming/moving/splitting docs or public symbols.
allowed-tools: Grep, Glob, Read, Edit, Bash
invocation: /doc-xref <target>
# Ported from Claude (.claude/skills/doc-xref/SKILL.md) on 2026-07-03
---

# Doc Cross-Reference

Find and update everything that points **at** `$ARGUMENTS` (a doc path, a heading
text/anchor, or a public symbol). Complements `/link-check`, which validates a
file's *outbound* links; this finds *inbound* references so a change propagates
instead of leaving stale pointers.

## Steps

1. **Prerequisite — linkify bare mentions** so prose references become
   discoverable links before the inbound search runs:
   ```bash
   python scripts/linkify_doc_mentions.py
   ```

2. Enumerate inbound references across both trees:
   - **Docs**: links `](<path-or-anchor>)`, bare path mentions, and prose mentions
     of the heading/title in `docs/**`, repo-root `*.md`, and `.github/copilot/**`.
   - **Code**: docstring / comment pointers in `src/**` and `tests/**`.
   ```bash
   git grep -nF "<target>"   # exact path / anchor / symbol; repeat for old name + anchor
   ```

3. **Rename/move**: update every hit to the new path/anchor; `git mv` when renaming
   a whole file so history follows.

4. **Reworded section**: update mentions whose surrounding text now misstates the section.

5. Update the `docs/README.md` registry line if a file was added/renamed/removed.

6. Verify with `/link-check` (or `python scripts/check_doc_links.py`).

## Output

List each reference updated (`file:line`, old → new) and confirm `/link-check`
passes. Flag any reference you could not safely auto-update for human review.

Complement: `/link-check` validates *outbound* links from any file you edited -
doc-xref covers inbound, link-check covers outbound. Run both after a rename.

## Completion checklist

- [ ] Every hit from `git grep` is updated - file:line list provided in output
- [ ] Any reference not safely auto-updated is explicitly flagged for human review
- [ ] `docs/README.md` registry line updated if the file was renamed or moved
- [ ] `/link-check` exits 0 after all edits
