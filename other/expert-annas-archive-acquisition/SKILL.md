---
name: expert-annas-archive-acquisition
version: 0.7.1
description: Search for candidate books, download owner-named titles immediately, present candidates for selection questions, save approved files through the configured sink, and ingest them into the domain's page library.
tools:
  - annas_archive_search
  - annas_archive_import
mutating: true
---

# Anna Archive Acquisition

Two request shapes, two behaviors — both leave a complete content-free audit
record:

- **The owner names a specific book.** The naming message is the approval:
  download immediately, reference that message as the approval id, ingest into
  the domain's page library, and report exactly what landed. Do not ask again.
- **The owner asks a selection question** ("the best book on X"). Search first
  and return specific candidate titles with ranking rationale, then let the
  owner choose. Never guess which candidate the owner meant.

The runtime—not the agent—resolves credentials and the configured books root.
Never request or reveal an API key. Refuse overwrites and preserve stable
locators and hashes in the content-free audit record. Record the owner's
standing copyright posture with each acquisition.

If the domain has no library to ingest into, a named book still downloads;
report that the ingest is pending rather than inventing a destination.

Source metadata is advertising, not evidence: a record can carry a monograph's
title, author, year and byte size and deliver a pamphlet. The runtime measures
the downloaded artifact and refuses to ingest a PDF whose measured page count is
implausibly small, leaving the file on disk. Report that refusal with the
measured page count instead of retrying; only pass `allow_short_artifact: true`
when the owner has confirmed a genuinely short work is wanted. When search
flags a candidate as unusually small against other editions of the same title,
say so before recommending it.

A search result whose `search.backend` is `libgen_fallback` came from Library
Genesis because Anna's Archive search was unavailable (the result's `warnings`
say why). Treat its candidates exactly like any other: select by md5 and import
as usual, since import still resolves the md5 through Anna's Archive fast
download. Mention the fallback to the owner in one clause; do not retry the
search hoping Anna's Archive comes back.

## Ingest into the page library

An import with `ingest: true` stores the original in the domain's library and
queues a page-library ingest job. The result's `rag_ingest` reads
`status: "page_ingest_queued"`, `target: "page_library"` and a `job_id`; the
book is not in the library yet. Check `library_ingest` with `action: "status"`
and that `job_id` until the job is `done` or `done_with_failures`, then report
what it lists: units and figures ingested, failed pages, empty pages,
unresolved readings and undescribed figures. Never describe a queued or
running job as success. A `failed` job names its error; report it verbatim.

Every PDF page is read locally — the text layer, then DeepSeek-OCR, then the
vision lane — so a scan ingests like any other PDF, and no page can be refused
for its content. Page-library ingest takes PDF, EPUB, Markdown and plain text.
Any other format (MOBI, AZW3, DJVU) is refused with
`page_ingest_format_unsupported`; the download stays on disk and the refusal
names the path. When the owner intends to ingest, search with
`ingest_intent: true` so ingestible formats rank first.

A PDF cites by page (`Author, Title, p.N`) and its pages can be viewed with
`view_page`; an EPUB, Markdown or text source cites by section. Prefer the
edition the owner asked for; when both are offered, say which citation form
each gives.

Re-ingesting the same original replaces its book; there is nothing to clean up
by hand. Report a scale refusal with the measured page count (`scale.pages`)
and do not substitute another copy without telling the owner.

A domain with no page library reports `rag_ingest` status `blocked` with
`page_library_not_configured`: nothing was ingested and the download is kept.
Report it verbatim.
