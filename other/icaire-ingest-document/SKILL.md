---
name: icaire-ingest-document
description: Ingest ICAIRE decks, PDFs, reports, policy documents, and source files into durable ICAIRE memory. Use when the user asks to save or process a document into summaries, facts, entities, initiatives, action items, or source notes.
---

# ICAIRE Ingest: Document

Turn source documents into durable ICAIRE memory while preserving provenance,
useful facts, extracted entities, initiative links, action items, and source
notes.

## Contract

- Start from the exact document or source material the user provided, attached,
  linked, or named.
- Use appropriate document tooling for PDFs, decks, spreadsheets, images, or
  text files before summarizing.
- Use BigBrain or the ICAIRE MCP connector for existing ICAIRE context,
  duplicate checks, initiative mapping, and page conventions.
- Prefer the remote ICAIRE MCP connector for remote-brain writes when it is
  available; use paths relative to the remote `cortex/` root.
- Before choosing paths, call ICAIRE MCP `filing_rules` and follow the compiled
  `FILING.md` guidance it returns. If that tool is unavailable, list and read
  the relevant `FILING.md` files directly; do not expect a page named
  `filing_rules` to exist.
- Keep provenance clear: document title, file name or URL, date, author or
  publisher when known, and what was actually read.
- For local binary artifacts that need to be preserved in the remote ICAIRE
  brain, use the MCP raw-file upload path: read the file locally, base64 encode
  it, and pass it as `raw_content_base64` to ICAIRE MCP `create_raw_file` or
  `create_raw_file_with_page`. Verify with `list_raw_files` and, when possible,
  `read_raw_file` size or checksum. Do not use direct git repo pushes as an
  ingestion substitute, and do not expect the remote MCP server to read a local
  client filepath. If the client surface cannot cleanly pass a large base64
  argument, use BigBrain's `scripts/prepare-raw-upload.mjs --call --mcp-name
  icaire` helper so the upload still goes through MCP.
- Verify any created or updated memory page by reading it back before claiming
  ingestion is complete.

## Workflow

1. Identify the source.
   - Determine document type, title, date, author or owner, source location,
     user goal, and whether the user expects local or remote ICAIRE memory.
   - If the document is inaccessible, report the access problem and ask only
     for the missing file, link, or permission.
2. Extract content.
   - Read the whole document when feasible; for long documents, process enough
     structure to avoid relying on a title or executive summary alone.
   - Capture headings, key claims, tables, figures, appendices, dates, names,
     organizations, commitments, and evidence quality.
3. Check existing memory.
   - Call ICAIRE MCP `filing_rules` before choosing the destination collection
     or raw-file path.
   - Search BigBrain or ICAIRE MCP for existing source pages, related
     initiatives, people, organizations, meetings, concepts, or prior versions.
   - Avoid duplicating an existing source note; update it when the new document
     is a version or follow-on.
4. Build durable notes.
   - Choose the destination by role, not file type. Use `sources/` only for
     input evidence, imported material, research material, transcripts, source
     extracts, or raw evidence used by ICAIRE work. Use `reports/` for
     ICAIRE-produced written reports, status reports, policy briefs, research
     papers, and PDF-style report outputs. Use `deliverables/` for
     ICAIRE-produced non-report outputs such as decks, toolkits, workshop
     packs, declarations, media assets, and course materials.
   - Create or update a `sources/*.md` page only when the document is an input
     source rather than produced ICAIRE work.
   - Create or update a `reports/*.md` page when the produced artifact is a
     written report, status report, policy brief, research paper, or report
     PDF, and place the raw file under `reports/.raw/<page-slug>/`.
   - Create or update a `deliverables/*.md` page when someone needs to review,
     approve, send, publish, present, or maintain a produced non-report output,
     and place the raw file under `deliverables/.raw/<page-slug>/` when the
     file itself is the deliverable.
   - Update related initiative, project, concept, person, or organization pages
     only when the document changes durable context.
   - Add action items or open questions to the appropriate page or report them
     as follow-up when the target is unclear.
5. Preserve source boundaries.
   - Separate extracted facts from interpretation and ICAIRE implications.
   - Mark quotes, figures, legal or policy claims, and sensitive partner claims
     that require review before external use.
6. Verify the write.
   - Read created or updated pages directly.
   - For uploaded raw files, list the target `.raw` folder and compare decoded
     byte count or checksum when the raw file can be read back.
   - Note skipped pages, failed extraction, unread sections, missing metadata,
     or follow-up needed for attachments and approvals.

## Output

Return an ingestion report with:

- `Created Or Updated`: source, report, deliverable, and related pages changed.
- `Document Summary`: concise summary of the source.
- `Key Facts`: facts that matter for ICAIRE.
- `Extracted Entities`: people, organizations, initiatives, places, dates, and
  documents.
- `Relevant Initiatives`: links or mappings to ICAIRE workstreams.
- `Action Items`: owner, action, deadline, and source evidence where known.
- `Source Notes`: provenance, document limits, sensitive claims, and review
  needs.
- `Verification`: pages read back or checks performed.

## Guardrails

- Do not summarize a document from its filename or title alone.
- Do not invent authors, dates, publication status, partner positions, or
  action owners.
- Do not merge external source claims into ICAIRE memory as confirmed internal
  commitments unless the source supports that.
- Do not over-update people or initiative pages from weak evidence; report the
  candidate update for review when uncertain.
- Do not claim full ingestion when only part of a long document was read.
- Do not ignore document access, OCR, formatting, or extraction failures.
- Do not bypass the MCP `filing_rules` tool by guessing from stale local
  conventions or by reading a nonexistent `filing_rules` page.
- Do not file produced ICAIRE work under `sources/` merely because it is a
  document. File produced report-style outputs under `reports/`; file produced
  non-report outputs under `deliverables/`; reserve `sources/` for inputs and
  research evidence.
- Do not fall back to editing or pushing the backing ICAIRE git repo to upload
  source files unless the user explicitly asks for repository maintenance rather
  than MCP ingestion.
