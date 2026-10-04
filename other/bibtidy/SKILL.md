---
name: bibtidy
description: Use when the user wants to validate, check, or fix a BibTeX (.bib) reference file, wrong authors, stale arXiv preprints, incorrect metadata, duplicate entries, formatting issues
metadata:
  short-description: Validate and fix BibTeX reference files
allowed-tools: Bash(python3 *), Bash(cp *), Bash(rm *), Read, Agent, WebSearch
---

Use this skill for any request to validate, check, clean up, or fix a BibTeX `.bib` file.

If the request includes a `.bib` path, operate on it. If the path is missing or does not exist, ask for it.

Assumptions:
- Process entries one by one.
- Only brace-style BibTeX like `@article{...}` is supported; reject parenthesized `@article(...)`.
- Preserve `@string`, `@preamble`, and `@comment` blocks verbatim.

## Resolve Tools

All bundled scripts live in `tools/` next to this file. Resolve `TOOLS_DIR` once:

```bash
for d in \
  "${CODEX_HOME:-$HOME/.codex}/skills/bibtidy/tools" \
  "$HOME/.claude/skills/bibtidy/tools" \
  "${CLAUDE_PLUGIN_ROOT:-/dev/null}/skills/bibtidy/tools"; do
  [ -f "$d/crossref.py" ] && TOOLS_DIR="$d" && break
done
```

Useful commands:
- `python3 $TOOLS_DIR/compare.py <file.bib> [--key KEY]`
- `python3 $TOOLS_DIR/crossref.py doi <DOI>`
- `python3 $TOOLS_DIR/crossref.py search "<title>"`
- `python3 $TOOLS_DIR/crossref.py bibliographic "<query>"`
- `python3 $TOOLS_DIR/duplicates.py <file.bib>`
- `python3 $TOOLS_DIR/edit.py <file.bib> <patches.json>`

## Patch Rules

Use `edit.py` for all actual `.bib` changes. Do not edit the file directly with agent editing tools and do not rewrite the whole file.

- `fix` patch: include `key`, `action`, `urls`, `explanation`, and `fields`; `entry_type` is optional.
- In `fields`, set a field to `null` to remove it; omit a field to leave it unchanged.
- `not_found`: comment out the original entry; do not add URL lines.
- `duplicate`: add `% bibtidy: DUPLICATE of <other_key> — consider removing` above the original entry; no URL lines.
- `review`: add one or more `% bibtidy: <URL>` lines plus `% bibtidy: REVIEW, <reason>` above the unchanged entry.
- Clean entries get no comments.

For `fix` patches, `edit.py` should produce:
- fully commented original entry
- one `% bibtidy: <URL>` line per source
- one `% bibtidy: <explanation>` line
- corrected entry

Use source values verbatim. If the bib entry uses `and others` and a verified source provides the full author list, replace it with the full list.

## Workflow

Each entry has a web-search budget of 1 total, used in at most one of Wave A or Wave B.

1. Read the file and note the path.
2. Clear the platform log: `> <file>.bib.cc.log` in Claude Code or `> <file>.bib.codex.log` in Codex.
3. Back up the file: `cp <file>.bib <file>.bib.orig`
4. Run `python3 $TOOLS_DIR/duplicates.py <file.bib>` before metadata fixes.
5. Run `python3 $TOOLS_DIR/compare.py <file.bib>` for CrossRef candidates.
6. Wave A web search: every entry with `error` set or no `candidates` must be web-verified. Those entries have spent their budget.
7. After each wave, classify every entry as one of:
   - `Clean`: confirmed, no changes
   - `Fix`: confident correction
   - `Escalate`: still ambiguous and budget unused
   - `Not found`: no paper found after required search
   - `Review`: budget spent and still uncertain
8. Wave B web search: only entries marked `Escalate` and not yet searched. After Wave B, final outcomes are only `Clean`, `Fix`, `Not found`, or `Review`.
9. Write a real `patches.json` file and apply fixes with `python3 $TOOLS_DIR/edit.py <file.bib> patches.json`.
10. Run `python3 $TOOLS_DIR/duplicates.py <file.bib>` again. Resolve every `unresolved same-key collisions` warning and rerun until the warning is gone.
11. Manually review likely related entries after fixes. Strong clues: repeated citation keys, repeated DOIs, same normalized title with overlapping authors, obvious preprint→published pairs. If two entries should be linked but not auto-removed, apply a `duplicate` patch.
12. Validate format, delete the backup, and print a summary table with rows: total entries, verified, fixed, not found, needs review, exact duplicates removed, near-duplicates flagged.

For files with more than 30 entries, work in batches of about 15 and report progress. Entry count must match before and after.

## Compare Carefully

`compare.py` returns raw CrossRef candidates plus `discrepancies`. Treat them as hints, not truth.

- A missing candidate field is not evidence that the bib field should be removed.
- If a verified candidate supplies a missing standard venue field such as volume, issue, or pages, add it.
- Never add a `doi` field when the bib entry currently lacks one.
- Treat `author` vs `authors` and `journal` vs `booktitle` as schema mismatches until verified.
- If a preprint has a verified published version, update title, venue, year, volume, number, and pages together.
- When the published title differs, replace the title verbatim; do not partially edit it.
- Use `--` for BibTeX page ranges.
- Missing `pages` is not automatically an error for venues that do not publish page numbers.

## Web Verification

Use subagents when available; otherwise do the same work sequentially. Cap at 6 subagents per wave and distribute entries evenly.

Each web-search subagent should return only JSON with:
- `key`
- `source_urls`
- `fields`
- `notes`

Rules for subagents:
- `fields` is either a fix-patch dict or `null`.
- Use `null` inside `fields` to remove a stale field.
- Verify against authoritative pages when possible: DOI page, publisher page, venue page, arXiv, OpenReview, etc.
- Check title, full author list, year, journal/booktitle, volume, number/issue, pages, and DOI.
- Put a value in `fields` when the verified source disagrees with the bib entry or when the bib entry is missing a standard field that the venue publishes.
- Do not add a missing `doi` field just because you found one; mention it in `notes` if useful.
- If a standard field is genuinely unavailable, say so in `notes`.

## Preserve

- Entry order
- All unchanged fields
- Empty lines between entries
- User `%` comments that are not `% bibtidy:`
- `@string`, `@preamble`, and `@comment` blocks
- LaTeX macros and brace-protected capitalization in titles

If rate-limited, note it and continue with the next entry.
