---
name: link-check
description: User-invoked as /link-check [path ...]. Validates that documentation relative links and heading anchors resolve across docs/ (plus repo-root Markdown files and .github/copilot/), using scripts/check_doc_links.py. Use after editing, splitting, merging, or renaming docs to catch dangling references.
allowed-tools: Bash, Read, Grep, Glob, Edit
invocation: /link-check [path ...]
# Ported from Claude (.claude/skills/link-check/SKILL.md) on 2026-07-03
# Note: Copilot now also runs doc_link_check.py automatically via native PostToolUse
#       and Stop hooks. Use /link-check for an explicit full sweep or after big doc refactors.
---

# Link Check

Verify documentation cross-references resolve - every relative `[text](path)`,
`[text](path#anchor)`, and in-page `#anchor` points at an existing file and a real
heading. Backed by `scripts/check_doc_links.py`.

> **Copilot note**: In Claude Code this ran automatically after every Markdown edit
> (PostToolUse) and at session end (Stop hook). Copilot CLI now does the same via
> native `.github/hooks/` hooks; still run `/link-check` manually after large
> edits, splits, merges, or renames when you want an explicit full sweep.

## Steps

1. **Prerequisite — linkify bare mentions**:
   ```bash
   python scripts/linkify_doc_mentions.py $ARGUMENTS
   ```

2. Run the checker over `$ARGUMENTS` (or the whole doc set when no path is given):
   ```bash
   python scripts/check_doc_links.py $ARGUMENTS
   ```

3. For each `missing file` / `missing anchor` finding, open the offending file at
   the reported line and fix it: correct the path, update the anchor to the
   current GitHub-style heading slug (see `.github/copilot/skills/link-check/references/anchor-slug-rules.md`).

4. If a heading was renamed/moved, also run `/doc-xref` to fix *inbound* links
   from other docs and from code docstrings.

5. Re-run step 2 until it exits `0`.

## Output

Report the findings fixed and confirm a clean `exit 0`. Note any link left
intentionally dangling (e.g. a planned-but-unwritten doc).

Complement: `/doc-xref <target>` patches *inbound* references - link-check covers
outbound, doc-xref covers inbound. Run both after a rename.
