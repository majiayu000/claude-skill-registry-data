---
name: link-check
description: >-
  User-invoked as /link-check [path ...]. Validates that documentation relative
  links and heading anchors resolve across docs/ (plus repo-root *.md and
  .claude/), using scripts/check_doc_links.py. Use after editing, splitting,
  merging, or renaming docs to catch dangling references.
allowed-tools: Bash, Read, Grep, Glob, Edit
invocation: /link-check [path ...]
---

# Link Check

Verify documentation cross-references resolve - every relative `[text](path)`,
`[text](path#anchor)`, and in-page `#anchor` points at an existing file and a real
heading. Backed by `scripts/check_doc_links.py` (the same checker the
`doc_link_check` hook runs), so results match the automated gate.

## Steps

1. Run the checker over `$ARGUMENTS` (or the whole doc set when no path is given):
   ```bash
   python scripts/check_doc_links.py $ARGUMENTS
   ```
2. For each `missing file` / `missing anchor` finding, open the offending file at
   the reported line and fix it: correct the path, update the anchor to the
   current GitHub-style heading slug, or repoint to the moved target.
3. If a heading was renamed/moved, also run `/doc-xref` to fix *inbound* links from
   other docs and from code docstrings - not just this file's outbound links.
4. Re-run step 1 until it exits `0`.

## Output

Report the findings fixed and confirm a clean `exit 0`. Note any link left
intentionally dangling (e.g. a planned-but-unwritten doc) so reviewers know it is
deliberate.
