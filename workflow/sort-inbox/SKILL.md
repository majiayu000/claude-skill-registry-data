---
name: sort-inbox
description: Empties inbox/ into raw/ and ingests each item into the wiki. Use when the user says sort my inbox, file this, process the inbox, or drops new files in inbox/.
---

# Sort the inbox

1. List everything in `inbox/` (skip `README.md`). If it is empty, say so and stop.
2. For each item, pick a short name: `YYYY-MM-DD-what-it-is.ext` using today's date (example: `2026-10-27-cs-lecture-5-notes.md`).
3. If the item is a pasted link with no content, fetch it if you can and save the text as a `.md` file; otherwise keep the link and note that the page was not read.
4. Move the item to `raw/` under its new name. Do not change its contents.
5. Run the **ingest** workflow on each moved file, one at a time.
6. Append one line to `wiki/log.md`: `- YYYY-MM-DD | sort | moved N items from inbox`.
7. Finish with a short report: what you filed, which pages you created or updated, and anything you could not read.
