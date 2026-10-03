---
name: zotero-paper-reader
description: "Use Zotero to find, read, summarize, cite, or export academic papers. Use for paper lookup, library searches, attachments, BibTeX, and draft citation work."
user-invocable: true
---

# Zotero Paper Reader

Search, retrieve, and analyze papers from a Zotero library via pyzotero. Defaults to the Zotero Desktop local API; falls back to the Zotero Web API when local Zotero is unavailable.

## Access Model

**Run the bundled tool** with `uv run --script <skill-dir>/scripts/zotero_tool.py`, where `<skill-dir>` is the directory containing this `SKILL.md` — substitute the real path. It detects the access mode automatically.

Load [`references/access-modes.md`](references/access-modes.md) for fallback rules, credential setup, or access-mode troubleshooting.

## Paper-Reading Workflow

Load [`references/paper-reading.md`](references/paper-reading.md) for exact invocations, JSON field names, disambiguation logic, parent-item hydration on full-text hits, and troubleshooting.

1. Search: `zotero_tool.py search "query"` — plain metadata search; `--fulltext` for indexed content (local or web).
2. Identify top-level item: inspect `data.itemType` on each hit; attachment hits from `--fulltext` need parent hydration via `data.parentItem`.
3. Choose: present concise metadata when multiple top-level papers match; ask the user only if the intended paper cannot be inferred.
4. Get PDF attachment key: `zotero_tool.py children ITEM_KEY` → find child with `data.contentType == "application/pdf"`.
5. Get PDF path: `zotero_tool.py pdf ATTACHMENT_KEY` → emits `{"source": ..., "path": ...}`.
6. Convert to markdown: invoke the `mistral-pdf-to-markdown` skill with the PDF path; save to `Notes/PaperInMarkdown/Author_Year_ShortTitle.md`.
7. Read and analyze: in sections — abstract and introduction first, then targeted sections.

## Library Query Commands

| Goal | Command |
|---|---|
| List libraries (user + groups) | `libraries` |
| Metadata search (title/creator/year) | `search "query"` |
| Full-text search (indexed content; local or web) | `search "query" --fulltext` |
| Single item | `item ITEM_KEY` |
| Child items / attachments | `children ITEM_KEY` |
| Attachment full-text retrieval (one attachment) | `fulltext ATTACHMENT_KEY` |
| PDF path or download | `pdf ATTACHMENT_KEY` |
| All collections | `collections` |
| All tags | `tags` |
| DOI-to-key index | `doiindex` |
| BibTeX export + master-`.bib` sync | `bibtex --item-key KEY` (or `--query "text"` / `--doi DOI`) |
| Insert a citation into a draft + sync `.bib` | `cite --item-key KEY --tex FILE --bib PATH` (or `--markdown FILE`) |
| Render formatted references | `bibliography --item-key KEY` (default APA) |
| Health / access check | `health` |

All commands emit JSON. Add `--help` to any subcommand for parameter details.

**Targeting a library.** Commands default to the user's own library ("My Library"). For a group library, run `libraries` first to get the group ids, then pass `--library <group-id>` (or `--library group:<id>`) — e.g. `search "your query" --library <group-id>`. Works on `search`, `item`, `children`, `collections`, `tags`, `fulltext`, `doiindex`, `pdf`, `bibtex`, `cite`, and `bibliography`.

## Citations & BibTeX

`bibtex`, `cite`, and `bibliography` generate citations from selected library items. Citekeys come from the researcher's **Better BibTeX (BBT)** by default, falling back to Zotero's built-in translator — with a key-mismatch warning — when BBT is unreachable. All three share the `--item-key` / `--query` / `--doi` selection flags, `--library` targeting, and the dedup-append `.bib` sync.

Load [`references/bibtex-citations.md`](references/bibtex-citations.md) for command examples, the full flag list (`--bib` / `--tex` / `--markdown` / `--marker` / `--style`), the BBT-vs-built-in key model and fallback semantics, JSON fields, and troubleshooting.

## Configuration

Credentials come from environment variables, else `Notes/.env`; they are never printed to the agent transcript. Web API mode needs `ZOTERO_LIBRARY_ID`, `ZOTERO_LIBRARY_TYPE` (default `user`), `ZOTERO_API_KEY`. Local mode needs none. Details in [`references/access-modes.md`](references/access-modes.md).

## Resources

- [`scripts/zotero_tool.py`](scripts/zotero_tool.py) — unified pyzotero command surface (pinned to pyzotero 1.13.0 via PEP 723 inline metadata)
- References — [`paper-reading.md`](references/paper-reading.md), [`access-modes.md`](references/access-modes.md), [`bibtex-citations.md`](references/bibtex-citations.md); load conditions in the sections above
