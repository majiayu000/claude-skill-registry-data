---
name: tidy
description: Health check for the wiki that finds broken links, orphan pages, duplicates, missing index lines and stale facts, then fixes what is safe. Use when the user says tidy, clean up, health check, or lint.
---

# Tidy the wiki

1. Broken links: find every `[[link]]` with no matching page. Create the page if the topic is real, or fix the link.
2. Orphans: find pages nothing links to. Link them from a related page.
3. Duplicates: find pages about the same thing. Merge into one, keep all sources, and leave the other as a one-line pointer.
4. Index: every page in `wiki/` has exactly one line in `wiki/index.md`.
5. Stale or conflicting facts: list them for the human rather than guessing.
6. Never touch `raw/`.
7. Append to `wiki/log.md`: `- YYYY-MM-DD | tidy | fixed N issues, flagged M`. Report what you fixed and what needs the human.
