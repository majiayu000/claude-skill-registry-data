---
name: docx-pro
description: Word document automation — generating, templating, and parsing .docx files — use when working with Word documents programmatically.
category: document-processing
---

## Overview

`.docx` is a zipped XML format (Office Open XML), which makes Word documents
surprisingly automatable: generate reports from templates, mail-merge at scale,
extract structured content, or convert to other formats. This skill covers
template-driven generation and reliable parsing across the major libraries.

## When to use

- Generating contracts, letters, or reports from templates with placeholders
- Mail-merge style bulk document production
- Extracting text, tables, headings, or images from .docx files
- Converting .docx to PDF, HTML, or Markdown
- Manipulating styles, headers/footers, and tracked changes

## Core concepts

**Template + data is the winning pattern.** Author the document in Word with
placeholder syntax (`{{name}}`, `{% for item in items %}`), then render with
data. This keeps design in the hands of whoever owns the document and logic in
code — far more maintainable than building documents paragraph-by-paragraph in
code.

**docx is XML in a zip.** Every library ultimately manipulates
`word/document.xml` inside the archive. Knowing this helps when libraries fall
short: you can unzip, inspect, and patch XML directly for edge cases (custom
XML parts, content controls, unusual formatting).

**Styles beat direct formatting.** Documents built on named styles (Heading 1,
Normal, custom styles) are parseable and convertible; documents with manual
bold/size/color everywhere are fragile. When generating, apply styles; when
parsing, key off styles (headings → document outline) rather than font sizes.

**Tracked changes and comments live in the XML.** Accept/reject revisions
programmatically before extraction if you want the "final" text; comments are
separate ranges that naive text extractors may interleave or drop.

**Fidelity vs structure trade-off.** Converting docx → PDF preserves visual
fidelity (use a real renderer like LibreOffice headless for best results);
docx → Markdown/HTML preserves structure but loses precise layout. Choose by
what the consumer needs.

## Practical workflow

1. **For generation:** create the template in Word with placeholders and real
   styles; keep logic (loops, conditionals) minimal and readable in the
   template.
2. **Render with data,** then open the output in Word/LibreOffice to verify —
   automated checks catch missing placeholders, but only eyes catch broken
   layout (orphaned headings, tables splitting badly).
3. **Handle the edge cases in data:** empty lists (hide the table, don't render
   an empty one), long text (test wrapping), special characters (escape
   template syntax), missing values (defaults, not blanks).
4. **For parsing:** extract by structure — styles for headings, table objects
   for tables, paragraph iteration for body text; preserve the mapping back to
   source locations for debugging.
5. **For conversion:** prefer headless LibreOffice for docx → PDF fidelity;
   prefer structure-aware extractors for docx → Markdown/HTML.
6. **Version your templates** alongside code — a template change is a code
   change; test generation in CI with fixture data.

## Common pitfalls

- **Placeholders broken across XML runs** — Word splits `{{name}}` into multiple
  runs if edited mid-word; templates authored carelessly fail to render. Type
  placeholders in one go, or use content controls.
- **Building documents purely in code** for complex layouts — unmaintainable;
  templates exist for a reason.
- **Ignoring section properties** (page size, margins, headers/footers differ
  per section) when manipulating documents — edits can silently apply to the
  wrong section.
- **Assuming .doc == .docx** — the old binary format needs different tooling;
  convert legacy .doc files first (LibreOffice headless batch conversion).
- **Losing images on round-trips** — images are separate parts referenced by
  relationship IDs; naive XML patching can orphan them. Use library APIs for
  image handling.
- **Not testing with tracked changes present** — real-world documents arrive
  with revisions; decide your accept/reject policy up front.
