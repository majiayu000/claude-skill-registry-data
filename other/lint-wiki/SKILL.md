---
name: lint-wiki
description: Health-check the podcast wiki (wiki/) and fix what's found. Use when the user asks to lint, audit, clean up, or check the wiki, or after a large ingest.
---

# Lint the wiki

Two passes: mechanical checks by script, then judgment checks by reading. Fix issues in place following the conventions in CLAUDE.md, then report.

## 1. Mechanical pass

Run `uv run tools/lint_wiki.py`. Each line is `<check> <page>: <detail>`:

| Check | Fix |
|---|---|
| `broken-link` | Point the link at the right page, or create the missing page if it's warranted |
| `not-in-index` | Add a one-line entry to `wiki/index.md` under the right hub section ("Unsorted" if no hub page) |
| `orphan` | Link the concept from related concepts' `## Related` and its hub |
| `missing-section` | Add the missing template section (it may stay empty) |
| `sources-mismatch` | Set `sources:` to the number of distinct episodes the page links |
| `no-hub` | Set `hubs:` to 1–2 domains |
| `missing-raw` / `url-mismatch` | Copy `raw:` path and `spotify_url` verbatim from the raw file; never retype |
| `needs-hub` | Create `wiki/hubs/<domain>.md` (hub template) and move its concepts out of "Unsorted" in the index |

Re-run until it prints `clean`.

## 2. Judgment pass

Read `wiki/index.md`, then the concept pages (prioritise those with the most sources and those updated most recently). Look for:

- **Near-duplicate concepts:** two pages covering the same topic. Merge into the better slug, then redirect every link to it and delete the other.
- **Silent contradictions:** claims in Key ideas that conflict, within one page or across pages, but aren't under Disagreements & open questions. Move them there with both sources. Never delete either claim.
- **Stale summaries:** a Summary that no longer reflects its Key ideas (e.g. written at 1 source, now 5). Rewrite it.
- **Missing cross-links:** concepts that clearly relate but don't link each other in `## Related`.
- **Unlinked claims:** Key ideas with no episode link.
- **Takeaway drift:** concept Takeaways missing from `wiki/takeaways/to-try.md`, or vice versa.
- **Concept gaps:** a topic recurring across 3+ pages with no page of its own. Suggest it; don't create it unless the user agrees.

Don't edit `raw/`. Don't re-synthesise from raw transcripts: lint works on the wiki as written.

## 3. Finish

- Append to `wiki/log.md`: `## YYYY-MM-DD — lint` then `fixed: …` (counts by check) and `suggested: …`.
- Commit: `git add wiki && git commit -m "lint: <summary>"`.
- Reply with what was fixed, by check, and any suggestions awaiting the user's decision.
