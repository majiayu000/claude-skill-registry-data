---
name: download-gated-pdfs
description: |
  Download the actual PDF binary from bot-gated sites (taxpolicycenter.org, urban.org,
  SSRN-hosted mirrors, think-tank/publisher sites) via the Wayback Machine id_ URL form.
  Use when: (1) curl/WebFetch of a .pdf URL returns HTML instead of a PDF even with a
  browser User-Agent, (2) pypdf fails with "invalid pdf header: b'<!DOC'" or
  "EOF marker not found" on a freshly downloaded file, (3) Firecrawl can parse the PDF
  to markdown but you need the original file on disk (e.g., filing a reference copy).
author: Claude Code
version: 1.0.0
date: 2026-07-15
---

# Download bot-gated PDFs via Wayback id_

## Problem
Many think-tank and publisher sites (taxpolicycenter.org, urban.org, SSRN delivery)
serve an HTML bot-challenge page instead of the PDF to non-browser clients. A browser
User-Agent header does not help. The downloaded "PDF" is actually HTML.

## Context / Trigger Conditions
- `curl -o file.pdf <url>` succeeds but the file starts with `<!DOC`
- pypdf raises `invalid pdf header: b'<!DOC'` or `PdfStreamError: Stream has ended unexpectedly`
- Firecrawl `scrape` returns clean markdown for the same URL (its proxies get through),
  but Firecrawl does not return the binary — only parsed content

## Solution
1. Request the file through the Wayback Machine's raw-content (`id_`) endpoint, which
   serves the original archived binary without rewriting:
   ```sh
   curl -sL -A "Mozilla/5.0 ... Chrome/126.0 Safari/537.36" \
     "https://web.archive.org/web/<YYYY>id_/<original-pdf-url>" -o out.pdf
   ```
   `<YYYY>` is any year likely to have a snapshot (e.g. publication year); Wayback
   redirects to the nearest capture. The `id_` suffix after the timestamp is what
   requests the untouched original.
2. Verify the download with pypdf — a bot page fails immediately:
   ```python
   from pypdf import PdfReader
   r = PdfReader("out.pdf"); print(len(r.pages), "pages")
   ```
3. If Wayback has no capture, fall back to: another mirror found via search
   (Exa/Firecrawl), or Firecrawl scrape for the parsed text when the binary is not
   strictly needed.

## Verification
`PdfReader` opens the file and reports a plausible page count; first-page text matches
the expected title.

## Example
Verified 2026-07-15: `taxpolicycenter.org/sites/default/files/publication/165884/ssrn-id4797771.pdf`
and `urban.org/sites/default/files/publication/80621/2000790-...pdf` both bot-gated to
direct curl (with UA), both downloaded intact via
`https://web.archive.org/web/2024id_/<url>` and `.../web/2023id_/<url>` (18 and 12 pages).

## Notes
- Government data hosts (e.g. `ticdata.treasury.gov`) are usually NOT gated — try direct
  curl first; Wayback is the fallback, not the default.
- Wayback captures can be stale for frequently-revised documents; check the snapshot date
  if currency matters.
- See also: the `pdf` skill (parsing/extraction after download) and
  `firecrawl:firecrawl-scrape` (parsed markdown when the binary is unnecessary).
