---
name: literature-zotero-screen
description: Match Zotero metadata and attachments, cache text, identify duplicates, and screen titles and abstracts economically; not full-text review.
---

# Zotero Library Screening

Read [shared contract](../../references/shared-contract.md) and [large-corpus workflow](../../references/large-corpus.md).

Use the local Zotero API when available. Database access requires authorization beyond an attachment-folder-only request. Use zotero_metadata.py in read-only mode; do not bypass locks. Backup use must disclose its snapshot date and matching coverage.

Run ingest.py, zotero_metadata.py and benchmark_corpus.py with the same output directory. Reuse source-hash caches. Distinguish duplicates, supplements, malformed downloads, title-only records and abstract candidates. Examine representative and ambiguous records; preserve version corrections in audit-overrides.json.

Output screening-records.json and quality information. NMF topics are exploratory; phrases are not original author keywords. Do not guess institution mappings or findings. Route full-text reading, export and static maps to their respective modules.
