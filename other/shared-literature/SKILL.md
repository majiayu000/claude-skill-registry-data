---
name: shared-literature
description: Reuse and maintain a shared literature library across research projects. Use before downloading or extracting papers, creating durable source packets, or updating literature indexes. Keeps source identity, versions, and project-specific notes separate.
---

# Shared literature library

Durable papers belong in the common library configured by `.research-library.json`,
not in an independent project cache. The configuration supplies `root` and
`default_domain`; relative roots are resolved from the configuration directory.
`RESEARCH_LIBRARY_ROOT` or the helper's `--root` can override the location.
If that library is unavailable, report the missing checkout/configuration;
do not silently start another local cache.

## Local results before web search

Every prior-work search starts with the common extracted literature, even when
web browsing will also be needed. Search succinct result statements and project
notes first with `python3 scripts/research_library.py search 'terms'`; add
`--sources` to search full extracted text. Read `merged-results.md` when present,
then the underlying extraction and its provenance. These local statements may
match the current question better than an abstract or web snippet. Browse for
gaps, primary-source verification, or updates; finding a paper online is not a
reason to download or convert it again when an adequate local version exists.

## Before downloading or extracting

1. Locate the library with `python3 scripts/research_library.py locate`.
2. Search all subjects with `python3 scripts/research_library.py search QUERY`.
   Try DOI, versionless arXiv ID, PMID, title, authors, and old citation keys.
   Search `catalog.json` and project notes directly when needed. A missing
   citation key alone does not establish that the paper is absent.
3. Inspect `metadata.json`, `library-record.json`, existing source files,
   `key-results.md`, and `variants/`. Reuse an adequate extraction. Record a
   needed new version or conversion explicitly instead of replacing the old one.
4. If absent, reserve the entry before acquisition:

   ```bash
   python3 scripts/research_library.py reserve --domain math --key author2024topic \
     --title 'Paper title' --doi '10.1234/example'
   ```

   Domains are `math`, `biomed`, and `physics`; choose one home for an
   interdisciplinary paper and use tags/aliases for its other subjects. The
   reservation searches across domains and serializes concurrent reservations.
   `reuse-or-review` means inspect the matching entry, not download another copy.
   `reserved` grants this task a location to populate. If another task reserved
   it, coordinate before taking over; a reservation is not a completed download.
5. Save sources and extraction outputs directly in the returned packet. Record
   URL, version, access date, extraction commands, checksums, and acquisition
   status. Set the status to `complete` or explain incomplete access when done.

## Packet and note ownership

Our own substantive writeups also need shared packets. Use `research-knowledge` to register an
internal work, fingerprint its source dependencies, and create extraction candidates. Check these
against the source before curating result cards. Refresh candidates after source changes, preserve
reviewed cards, and audit their freshness. A packet's extraction status is separate from the
mathematical status of its claims. Original writeup sources remain in their owning repository.

```text
<library>/<domain>/<citation-key>/
  metadata.json
  library-record.json       # aliases and import provenance, when present
  original.pdf              # when storage policy permits
  source.txt                # or source TeX / official HTML
  key-results.md            # precise reusable result extraction
  project-notes/<project>.md # relevance, notation translation, local caveats
  variants/<origin>/        # retained alternative sources/versions and notes
```

Keep universal statements separate from a project's interpretation. Never
silently overwrite differing extractions, publication versions, or reading
notes during deduplication. Identical titles or citation keys alone can be
ambiguous; inspect authors and persistent identifiers before merging. Preserve
conflicting metadata as an explicit discrepancy.

Source PDFs and archives are immutable evidence. Some imported binary files
are symlinks to an identical stored source: add a new version using a new file
instead of editing shared source bytes in place. Metadata and editable notes
remain separate files even when initially identical.

Project `literature/` or `references/` paths may be compatibility links. They
preserve existing citations and scripts, but new papers must be reserved in the
canonical subject directory. Use a link to the canonical packet when adding a
new paper to a project's view. A symlink does not stage the target files in Git.
Commit packet changes and shared indexes in the library's owning repository;
commit only links and project guidance in the consuming repository.

## Indexes and access

Run `python3 scripts/research_library.py index` and
`python3 scripts/render_literature_index.py` after changing packets. The default
renderer uses the configured library; `--literature-dir` selects an explicit
collection. Refresh global and subject indexes as supported by the workspace.
Link the shared index or packet from a dashboard using the project's configured
path or existing compatibility view.

Consolidation does not authorize broader publication. Preserve restricted
project views and keep private notes out of newly published surfaces. Shared
storage is not permission to redistribute copyrighted material; retain the
existing storage policy and provenance for each source.
