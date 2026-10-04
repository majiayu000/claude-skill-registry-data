---
name: sync-curated-content
description: 'Read the +newsletter Gmail alias, extract claims and techniques into /raw/curated, update wiki entries. Use when syncing newsletters or as part of /data-ingestion.'
---

# Sync Curated Content

Pipeline skill: ingest external learning material (newsletters, articles
forwarded to a dedicated alias) into the knowledge base. Runs standalone or as
step 3 of `/data-ingestion`.

## Setup convention

Specialized industry newsletters are subscribed via the alias
`henrygoldsmith07+newsletter@gmail.com`, so they are filterable with the Gmail
query `to:henrygoldsmith07+newsletter@gmail.com`.

## Process

1. **Find the last sync point.** Read `raw/curated/.last-sync`; default to
   14 days ago if missing.
2. **Fetch.** Use Gmail `search_threads` with the alias query plus
   `after:<last-sync date>`. If the Gmail connector isn't available, say so
   and stop — don't guess at content.
3. **Extract claims, not prose.** For each newsletter/article, pull:
   - Concrete claims and techniques (with the source's reasoning)
   - Tools, releases, or practices worth evaluating
   - Anything that contradicts an existing wiki entry — flag these explicitly
4. **Write the digest.** One file per run:
   `raw/curated/YYYY-MM-DD_newsletter-digest.md`, one section per source with
   sender and subject as provenance.
5. **Update the wiki.** Add a row to the **Curated Content** table in
   `wiki/index.md`. Where a claim updates an existing `wiki/<topic>.md` page,
   edit that page: add the new claim with a dated citation, and mark
   contradicted statements as superseded rather than deleting them.
6. **Update the sync point** in `raw/curated/.last-sync`.
7. **Report.** Sources read, claims extracted, wiki pages updated,
   contradictions flagged. If run from `/data-ingestion`, keep this to 3 lines.
