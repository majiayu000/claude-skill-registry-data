---
name: epub-pro
description: EPUB ebook creation and processing — structure, metadata, validation — use when generating or parsing ebooks.
category: document-processing
---

## Overview

EPUB is the open ebook standard: a zipped package of XHTML content, CSS, images,
and metadata (OPF). Creating valid, good-looking EPUBs means understanding that
package structure — and that "renders in my reader" is not the same as "valid
EPUB". This skill covers authoring, generation, and parsing.

## When to use

- Generating ebooks from Markdown, HTML, or structured content
- Fixing or validating EPUB files (EpubCheck)
- Designing reflowable layouts that work across readers (Kindle, Apple Books, Kobo)
- Extracting text and metadata from EPUBs for indexing
- Handling covers, TOCs (NCX/nav), and embedded fonts

## Core concepts

**EPUB is a zip with rules.** `mimetype` file first and uncompressed, then
`META-INF/container.xml`, then the OPF package document listing every resource
in the manifest with a spine defining reading order. Violate the packaging
rules and some readers refuse the file even if the content is fine.

**Reflowable is the default; fixed-layout is the exception.** Reflowable EPUBs
adapt to screen size and user font settings — right for novels, non-fiction,
docs. Fixed-layout (page-precise) suits children's books and comics but
sacrifices accessibility and adaptability. Choose deliberately.

**CSS support varies by reader.** Keep stylesheets simple: basic typography,
margins, and page-break controls work everywhere; floats, absolute positioning,
and web fonts are inconsistently supported. Embedded fonts work if subsetted
and declared properly — but increase file size and may be overridden by reader
settings anyway.

**Navigation documents matter.** EPUB 3 uses an XHTML nav document for the TOC;
EPUB 2 used NCX. Include both for maximum compatibility. A proper hierarchical
TOC (parts → chapters → sections) is the difference between a professional
ebook and an amateur one.

**Metadata is discoverability.** Title, creator, language, identifier, and
cover image in the OPF — plus schema.org refinements for series info. Validate
with EpubCheck; it's the industry gatekeeper for distribution channels.

## Practical workflow

1. **Author in a simple source format** (Markdown or semantic HTML) — one
   chapter per file keeps the pipeline clean.
2. **Convert with a real toolchain** (Pandoc-style converters or dedicated EPUB
   libraries) using a checked-in CSS file and metadata config; don't hand-roll
   the zip packaging.
3. **Set the cover, TOC depth, and metadata** explicitly — these are the first
   things readers and stores check.
4. **Validate with EpubCheck** and fix every error (warnings: triage, but fix
   most); validation failures block distribution on major stores.
5. **Test on multiple readers** — at minimum one Kindle, one Apple Books/Kobo,
   and one generic EPUB reader; check the cover, TOC navigation, images, and a
   long chapter's typography.
6. **For parsing/extraction:** unzip, read the OPF for spine order, extract
   XHTML in spine order, strip to text preserving chapter boundaries and
   image references.

## Common pitfalls

- **Skipping validation** — "opens in Calibre" ≠ valid; stores and some
  devices reject invalid EPUBs.
- **Absolute positioning and complex CSS** — renders unpredictably across
  readers; keep it simple and reflowable.
- **Huge unoptimized images** — bloat file size and crash low-memory readers;
  resize and compress images for ebook dimensions.
- **Missing or flat TOC** — a 300-page book with a 3-entry TOC is nearly
  unnavigable; generate the TOC from real heading structure.
- **DRM confusion** — standard EPUBs have no DRM; adding DRM requires specific
  vendor toolchains (and locks out readers); decide distribution strategy
  before production.
- **Hardcoded font sizes in px** — ignore user preferences and break
  accessibility; use relative units (em/%) and let readers control base size.
