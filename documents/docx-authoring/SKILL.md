---
model_tier: medium
name: docx-authoring
description: "When generating or editing a Word .docx — create, fill a template, or edit body XML via a consumer library; round-trip validated. Triggers on 'generate a docx', 'fill this Word template'."
status: active
tier: senior
domain: process
compatibility: "Requires a consumer-installed OOXML library (python-docx for create/fill; a zip+xml toolchain for the unpack→edit→pack path). No LibreOffice/soffice dependency — that surface is gated (see pptx, road-to-ecosystem-harvest-document-skills Phase 2). Ships zero runtime in this package."
harness_compat: consumer-installed-deps
workspaces:
  - agent-config-maintainer
packs:
  - meta
---

# docx-authoring

Wing-1 engineering skill for **writing** Word documents — the generation half of
the read→write cycle whose read side is [`markitdown`](../markitdown/SKILL.md).
Ships zero runtime in this package: the agent drives a library the consumer
already has (python-docx, or a zip+XML toolchain), exactly as `markitdown` wraps
a consumer-installed converter. Re-implements the **pattern**, never any
proprietary source.

## When to use

- "Generate a .docx report / letter / contract from this content."
- "Fill this Word template with these values."
- "Edit the body of this .docx" (a heading, a table cell, a style).

Do NOT use for: reading a docx → Markdown (that is `markitdown`); slide decks
(`html-deck`, or the gated pptx surface); PDFs (`pdf-tools`).

## Procedure

### 1. Pick the path by task

| Task | Path |
|---|---|
| Create from scratch / structured content | Library create (python-docx `Document()`) — build paragraphs, tables, styles programmatically |
| Fill a supplied template | Open the template, replace placeholder runs in place, save a copy — never mutate the original |
| Surgical edit of existing body | **unpack → edit XML → pack-with-validate**: a `.docx` is a ZIP of XML; unzip, edit `word/document.xml`, re-zip preserving the archive structure |

### 2. Honor the hard-won gotchas (encode as rules, not hope)

- **Page size defaults to US Letter** in most libraries — set A4 explicitly when the locale needs it; never assume.
- **Table columns need dual widths** — set BOTH the table grid width and each cell width, or renderers ignore one and collapse the layout.
- **No Unicode bullet glyphs** as literal characters (`•`, `‣`) — use the list-style paragraph, or the document loses its list semantics and screen readers skip it.
- **Runs, not paragraphs, carry formatting** — a placeholder that spans two runs will not match a naive whole-paragraph replace; split/merge runs first.

### 3. Validate — round-trip, do not trust the write

1. Re-open the generated file with the SAME library; assert it parses (a corrupt ZIP or malformed XML throws here).
2. Read back one written value (a heading text, a table cell) and assert it equals what was written.
3. For the unpack→pack path: confirm the archive still contains `[Content_Types].xml` and `word/document.xml` (dropping either produces a file Word refuses to open).

## Output format

1. The generated/edited `.docx` path.
2. The validation result: parses ✅, read-back value matched ✅, required parts present ✅.
3. Any gotcha that applied (e.g. "set A4 explicitly; template used Letter").

## Gotcha

The most common silent failure is a file that **saves without error but Word
refuses to open**: an unpack→pack cycle that re-zipped with a directory entry,
wrong compression, or a dropped `[Content_Types].xml`. The round-trip re-open in
step 3 is the only check that catches it — a green "file written" line does not.

- **Silent corruption:** an unpack→pack cycle re-zipped with a directory entry or a dropped `[Content_Types].xml` → saves fine, Word shows "file is corrupt". Only the round-trip re-open catches it.

## Do NOT

- Do NOT bundle or ship a Python toolkit in this package — drive the consumer's library (zero-runtime posture, like `markitdown`).
- Do NOT mutate a supplied template in place — always write a copy.
- Do NOT claim success on "file written"; claim it only after the round-trip re-open.
- Do NOT reach for LibreOffice/soffice — that dependency is gated (pptx surface).

## Related Skills

**WHEN to use this**

- The target artifact is a Word `.docx` — a report, letter, contract, or a filled template.
- A `.docx` body needs a surgical edit (heading, table cell, style) via the unpack→edit→pack path.

**WHEN NOT to use this**

- Reading a docx into the conversation → [`markitdown`](../markitdown/SKILL.md).
- PDFs → [`pdf-tools`](../pdf-tools/SKILL.md); spreadsheets → [`spreadsheet-authoring`](../spreadsheet-authoring/SKILL.md); slide decks → [`html-deck`](../html-deck/SKILL.md).
- The task needs LibreOffice-backed rendering (pptx) — that surface is gated, do not reach for it here.

## When the agent should load this

- "Generate a Word report from this content."
- "Fill this .docx template with these values."
- "Edit the heading / a table cell in this .docx."
- "Produce a contract as a .docx."

## Output

1. **Generated document** — the `.docx` path. Cite as `docx-output`.
2. **Validation receipt** — parses on re-open ✅, read-back value matched ✅, required OOXML parts present ✅. Cite as `docx-validation`.
3. **Gotcha log** — present only when a gotcha applied (page-size override, run-split for a template placeholder). Cite as `docx-gotchas`.
