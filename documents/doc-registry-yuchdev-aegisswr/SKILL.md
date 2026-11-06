---
name: doc-registry
description: >
  User-invoked as /doc-registry. Builds a registry of every *.md file under
  docs/ and .github/copilot/, then reports any cross-references that point at missing
  files, with rename candidates ranked by confidence. Use for a one-shot corpus
  health check before or after structural documentation changes (adding
  milestones, reorganising folders, bulk renames). For automated iteration and
  auto-fix, use /loop update-docs instead.
allowed-tools: Bash, Read, Edit
invocation: /doc-registry
# Ported from Claude (.claude/skills/doc-registry/SKILL.md) on 2026-07-03
---

# Doc Registry

Build a corpus map of every `*.md` file under `docs/` and `.github/copilot/`, then
report cross-references that point at files that do not exist. Backed by
`scripts/doc_registry.py`.

## When to use

- Before restructuring `docs/` (get a baseline of which links will break).
- After adding a new milestone or task directory.
- As a quick pre-commit check when bulk-renaming docs.
- To get the list of "orphan" links that `/link-check` might not catch.

## Steps

1. **Prerequisite — linkify bare mentions**:
   ```bash
   python scripts/linkify_doc_mentions.py
   ```

2. Run the registry scanner:
   ```bash
   python scripts/doc_registry.py
   ```

3. For each `[HIGH] Likely rename` entry: update the link in the source file
   to point at the candidate path. Use the shortest correct relative path.
   Do NOT rename files.

4. For each `[MEDIUM] Possible rename` entry: inspect the candidates, pick the
   right one if obvious, then update the link. If ambiguous, flag for human review.

5. For each `[REVIEW] No candidates found` entry: decide whether to:
   - Create the missing file (then update `docs/README.md`).
   - Remove the broken link.
   - Update the link to point at an existing related file.

6. Re-run step 1 until it reports all references resolve.

7. Run `/link-check` to validate anchors and non-`.md` links.

## Complement

| Tool | Checks |
|------|--------|
| `/doc-registry` | Missing *.md files referenced by links |
| `/link-check` | Broken anchors and non-.md file links |
| `/doc-xref <target>` | Inbound references from other docs and code |
| `/loop update-docs` (emulated in Copilot) | Iterative auto-fix + human review for the full corpus |

Run `/link-check` after `/doc-registry` for full coverage.
