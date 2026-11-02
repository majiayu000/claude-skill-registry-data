---
name: ingest
description: Turns one source file in raw/ into linked wiki pages and updates the index and log. Use after sorting the inbox, or when the user says ingest this, learn this, or add this to my brain.
---

# Ingest one source

1. Read the source file in `raw/` all the way through.
2. Read `wiki/index.md` to see which pages already exist.
3. Write one `type: source` page summarizing the file in five bullets or fewer, named after the file (`wiki/src-2026-10-27-cs-lecture-5-notes.md`).
4. Pull out the people, projects, ideas and events that matter. For each one:
   - If a page exists, add the new facts under `## Notes` with the source cited, and bump `updated:`.
   - If not, create it using the page format in `CLAUDE.md`.
   - Aim for 3 to 8 pages touched. Fewer, richer pages beat many thin ones.
5. Link every page you touched to the source page and to each other where it makes sense, using `[[page-name]]`.
6. Add a line to `wiki/index.md` for every new page: `- [[page-name]]: one-line hook`.
7. Append to `wiki/log.md`: `- YYYY-MM-DD | ingest | raw/file -> N pages touched`.
8. If the new source contradicts an existing page, keep both claims, cite both sources, and flag it with `> [!warning] Conflict`.
