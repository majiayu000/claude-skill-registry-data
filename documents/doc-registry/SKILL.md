---
name: doc-registry
description: >
  User-invoked as /doc-registry. Builds a registry of every *.md file under
  docs/ and .claude/, then reports any cross-references that point at missing
  files, with rename candidates ranked by confidence. Use for a one-shot corpus
  health check before or after structural documentation changes (adding
  milestones, reorganising folders, bulk renames). For automated iteration and
  auto-fix, use /loop update-docs instead.
allowed-tools: Bash, Read, Edit
invocation: /doc-registry
---

# Doc Registry

Build a corpus map of every `*.md` file under `docs/` and `.claude/`, then
report cross-references that point at files that do not exist. Backed by
`scripts/doc_registry.py`.

## When to use

- Before restructuring `docs/` (get a baseline of which links will break).
- After adding a new milestone or task directory (confirm all internal links
  are correct).
- As a quick pre-commit check when bulk-renaming docs.
- To get the list of "orphan" links that `/link-check` might not catch
  (missing files rather than missing anchors).

## Steps

1. **Prerequisite — linkify bare mentions** so prose references are already
   links before the registry scan runs (converts auto-fixable mentions, writes
   a report of the ambiguous ones):
   ```bash
   python scripts/linkify_doc_mentions.py
   ```

2. Run the registry scanner:
   ```bash
   python scripts/doc_registry.py
   ```

2. For each `[HIGH] Likely rename` entry: update the link in the source file
   to point at the candidate path. Use the shortest correct relative path from
   the source file's directory, or an absolute `/`-prefixed path when relative
   would be confusing.

   Do NOT rename files. The correct file already exists at the candidate path;
   the link was simply written with a wrong path.

3. For each `[MEDIUM] Possible rename` entry: inspect the candidates, pick the
   right one if obvious, then update the link. If ambiguous, flag for human
   review.

4. For each `[REVIEW] No candidates found` entry: decide whether to:
   - Create the missing file (then update `docs/README.md` if it belongs there).
   - Remove the broken link.
   - Update the link to point at an existing related file.

5. Re-run step 1 until it reports `"All .md cross-references resolve correctly."`.

6. Run `/link-check` to validate anchors and non-`.md` links — doc-registry
   only checks file existence, not anchor correctness.

## Output

See [examples/sample-report.md](examples/sample-report.md) for an annotated
report and how to act on each `[HIGH]`/`[MEDIUM]`/`[REVIEW]` tier.

A human-readable report with three sections:

- **Missing .md References**: each broken link with confidence tag, source
  location, and ranked rename candidates.
- **Summary**: registry size, total `.md` links scanned, missing count,
  high-confidence / needs-review split.

## Complement

| Tool | Checks |
|------|--------|
| `/doc-registry` | Missing *.md files referenced by links |
| `/link-check` | Broken anchors and non-.md file links |
| `/doc-xref <target>` | Inbound references from other docs and code |
| `/loop update-docs` | Iterative auto-fix + human review for the full corpus |

Run `/link-check` after `/doc-registry` for full coverage — they check
orthogonal things.
