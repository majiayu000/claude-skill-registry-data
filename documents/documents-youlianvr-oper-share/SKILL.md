---
name: documents
description: >-
  Turning written material into readable documents: markdown to a single-file
  HTML document, PR reviews and long-form reports, reading Word files, and
  diagrams. Use when the deliverable is a document rather than a screen: a spec,
  a report, a review, or a diagram.
---

# documents — written material in and out

> Home branch in Memora: `root/skill/documents`.

## Choosing a part

| Part | What it covers |
|---|---|
| `parts/md-document/` | Long-form markdown (specs, RFCs, reports, plans, explainers) → a single-file, lightly interactive HTML document with sticky TOC and scrollspy |
| `parts/markdown-html-orchestrator/` | The general markdown → single-file HTML converter, for any markdown in a project |
| `parts/md-review/` | A PR writeup or code review with diff blocks and `[!BLOCKER]/[!MAJOR]/[!MINOR]/[!NIT]` callouts → a readable review document |
| `parts/read-docs/` | Reading `.doc`/`.docx` quickly via python-docx |
| `parts/diagram-generator/` | Diagrams from natural language, notes, code, schemas, tables or existing source |

**PDF, Word-creation and spreadsheet engines are not bundled.** The usable ones
are source-available under terms that forbid repackaging, so this kit ships
neither (see `PROVENANCE.md`). When the deliverable must be an `.xlsx`, a filled
PDF form or a Word file with tracked changes, install that engine from its own
source first and record the install there — do not hand-edit a zip of XML.

## Rules

- **HTML output is one file, opened locally.** No build step and no CDN
  dependency for something the user will send to someone; check it in a browser
  before calling it done.
- **Office files are edited by a tool, not by hand.** A re-zipped XML rewrite is
  how documents get corrupted; if no engine is installed, say so and install the
  right one instead of imitating it.
- **Prose quality is not optional**: long documents go through `antislop`
  before delivery.
- **Ask when it matters**: the output format when the request could mean HTML or
  a Word file, a document that will be signed or submitted formally, and any file
  destined for someone outside the workspace.
- **What the document decided** becomes a memory node under
  `root/skill/documents`; the file itself belongs with its project.

## Related

`decks` (slides), `antislop` (prose), `documentation-writer` (formal reports),
`design` (typography and layout of the rendered page).
