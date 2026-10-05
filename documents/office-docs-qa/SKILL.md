---
name: office-docs-qa
description: "Office file QA: Word, PDF, Excel, PPTX checks, file reading, diagrams, Markdown knowledge base. Word dosyası, PDF birleştir, Excel düzenle, akış şeması çiz."
---

# Office Docs QA

Planning and quality checks for office files and diagrams. Use the host's native document, PDF, spreadsheet and presentation tools for the actual file operations; these modules add preservation and validation.

## Choose the module

| File or task | Module |
|---|---|
| Word / DOCX | `docx-workflow` |
| PDF: extract, create, merge, split, rotate, OCR, forms, redaction | `pdf-workflow` |
| Excel / XLSX / CSV | `xlsx-workflow` |
| Large, unknown or binary file inspection | `file-reading-workflow` |
| Process, system or data-flow diagram (Mermaid, SVG, HTML) | `workflow-visualizer` |
| Markdown knowledge base, notes vault, index, broken links | `knowledge-base` |

Designing a new HTML/strategic slide deck → the separate `slides` skill; thesis or academic talks → `academic-study-coach`; data analysis → `data-analyst`.

## Shared rules

- Never overwrite the original file; write a new version.
- Preserve structure, styles, formulas and links.
- Verify the result by reopening or rendering it; never claim formulas were recalculated unless a real engine did it.

## Module map

Open only the module(s) the request needs and read the module file completely before acting. Several modules may combine in one task.

| Module | Use when | File |
|---|---|---|
| `docx-workflow` | Apply a preservation-first workflow to read, create, edit, and validate Word DOCX documents while protecting structure, styles, relationships, accessibility, and existin… | [MODULE.md](modules/docx-workflow/MODULE.md) |
| `pdf-workflow` | Apply a provenance-first PDF workflow for inspecting, extracting, creating, combining, splitting, rotating, redacting, OCR, or form filling. | [MODULE.md](modules/pdf-workflow/MODULE.md) |
| `xlsx-workflow` | Apply a preservation-first workflow to read, create, edit, clean, calculate, chart, and validate XLSX/XLSM workbooks. | [MODULE.md](modules/xlsx-workflow/MODULE.md) |
| `file-reading-workflow` | Apply a safe, bounded workflow for inspecting local or uploaded files without flooding context or treating binary data as text. | [MODULE.md](modules/file-reading-workflow/MODULE.md) |
| `workflow-visualizer` | Create an accessible, self-contained workflow diagram as HTML, Mermaid, or SVG from a process description. | [MODULE.md](modules/workflow-visualizer/MODULE.md) |
| `knowledge-base` | Create, organize, audit, or maintain a durable Markdown knowledge base with an index, atomic notes, stable identifiers, links, tags, and maintenance checks. | [MODULE.md](modules/knowledge-base/MODULE.md) |

Supporting files (open only when the module points to them):

- `workflow-visualizer`: [interactive-html-diagrams.md](modules/workflow-visualizer/references/interactive-html-diagrams.md)
