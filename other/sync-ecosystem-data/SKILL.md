---
name: sync-ecosystem-data
description: 'Pull meeting transcripts, email threads, and calendar activity into /raw/ecosystem and index in /wiki. Use when syncing ecosystem data or as part of /data-ingestion.'
---

# Sync Ecosystem Data

Pipeline skill: pull personal-ecosystem signals into the knowledge base so the
system learns operational patterns. Runs standalone or as step 2 of
`/data-ingestion`.

## Sources

Use whichever connectors are available this session (check with `ToolSearch`);
skip silently any that aren't connected:

| Signal | Tool |
|--------|------|
| Meeting notes/transcripts | Notion `notion-query-meeting-notes`, Google Drive search |
| Email threads (non-newsletter) | Gmail `search_threads` — recent important threads |
| Schedule patterns | Google Calendar `list_events` — past 7 days |
| Document activity | Google Drive `list_recent_files` |

## Process

1. **Find the last sync point.** Read `raw/ecosystem/.last-sync`; default to
   7 days ago if missing.
2. **Pull and digest.** For each available source, fetch items since the sync
   point and extract only decisions, commitments, deadlines, recurring
   contacts, and operational patterns — not full bodies. Never store
   credentials, financial details, or obviously sensitive personal content;
   summarize around them.
3. **Write digests.** One file per source with content:
   `raw/ecosystem/YYYY-MM-DD_<source>.md` (e.g. `2026-07-12_meetings.md`).
   Skip sources with nothing new.
4. **Index.** Add one row per written file to the **Ecosystem Data** table in
   `wiki/index.md`.
5. **Update the sync point** in `raw/ecosystem/.last-sync`.
6. **Report.** Sources synced, sources skipped (and why), notable patterns.
   If run from `/data-ingestion`, keep this to 3 lines.
