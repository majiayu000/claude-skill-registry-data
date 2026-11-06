---
name: link-check
description: User-invoked as /link-check [path ...]. Validates that documentation relative links and heading anchors resolve across docs/ (plus repo-root Markdown files and .claude/), using scripts/check_doc_links.py. Use after editing, splitting, merging, or renaming docs to catch dangling references.
allowed-tools: Bash, Read, Grep, Glob, Edit
invocation: /link-check [path ...]
---

# Link Check

Verify documentation cross-references resolve - every relative `[text](path)`,
`[text](path#anchor)`, and in-page `#anchor` points at an existing file and a real
heading. Backed by `scripts/check_doc_links.py` (the same checker the
`doc_link_check` hook runs), so results match the automated gate.

## Steps

1. **Prerequisite — linkify bare mentions** (whole corpus or scoped to `$ARGUMENTS`):
   ```bash
   python scripts/linkify_doc_mentions.py $ARGUMENTS
   ```
   This converts prose mentions of `*.md` filenames into Markdown links before
   the link checker runs.  Any unresolvable mention is written to
   `.claude/state/linkify-report.md` for human review.

2. Run the checker over `$ARGUMENTS` (or the whole doc set when no path is given):
   ```bash
   python scripts/check_doc_links.py $ARGUMENTS
   ```
3. For each `missing file` / `missing anchor` finding, open the offending file at
   the reported line and fix it: correct the path, update the anchor to the
   current GitHub-style heading slug (the exact slug algorithm, with worked
   examples, is in [references/anchor-slug-rules.md](references/anchor-slug-rules.md)
   — mind the double-hyphen case), or repoint to the moved target.
4. If a heading was renamed/moved, also run `/doc-xref` to fix *inbound* links from
   other docs and from code docstrings - not just this file's outbound links.
5. Re-run step 2 until it exits `0`.

## Output

Report the findings fixed and confirm a clean `exit 0`. Note any link left
intentionally dangling (e.g. a planned-but-unwritten doc) so reviewers know it is
deliberate.

Complement: `/doc-xref <target>` patches *inbound* references from other docs and
code docstrings - link-check covers outbound, doc-xref covers inbound. Run both after a rename.
