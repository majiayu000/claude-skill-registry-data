---
name: docx-workflow
description: "Apply a preservation-first workflow to read, create, edit, and validate Word DOCX documents while protecting structure, styles, relationships, accessibility, and existing user content. Use when the user asks for this workflow or needs an additional DOCX validation checklist alongside installed document tooling. Turkish triggers: Word belgesi oluştur veya düzenle, DOCX incele, biçim ve sayfa düzenini doğrula."
license: MIT
---

# DOCX Workflow

## Choose the path

- **Read/review:** extract paragraphs, headings, tables, headers/footers, notes/comments, links, and media inventory without changing the source.
- **Create:** use an installed DOCX library or the active document tool and define styles before content.
- **Edit:** preserve the existing package, styles, numbering, sections, relationships, tracked changes, comments, fields, and embedded objects unless the task explicitly changes them.
- **Convert/render:** use an installed office renderer in a separate output location and visually inspect the result.

Do not install libraries or office software implicitly. If the needed tooling is absent, state the exact proposed dependency and wait for authorization unless installation is already in scope.

## Editing rules

1. Back up the original or write to a new path.
2. Inventory sections, page setup, styles, numbering, tables, fields, links, images, headers/footers, and accessibility metadata.
3. Make the narrowest semantic edit. Avoid raw ZIP/XML edits unless the library cannot preserve the feature and the OOXML relationship changes are fully understood.
4. Preserve macros and signatures as opaque artifacts; never execute them. Warn that editing a signed document may invalidate its signature.
5. Keep headings hierarchical, tables readable, links meaningful, images described, and language metadata correct.
6. Use real list/heading/table structures rather than visual approximations with spaces or symbols.
7. Do not invent citations, legal clauses, values, or document metadata.

## Creation quality

Define page size/margins, body and heading styles, paragraph spacing, list numbering, table rules, captions, headers/footers, and section breaks consistently. Keep the design restrained unless the user supplies a brand system. Provide a table of contents only when headings and the target viewer support updating fields.

## Validation

- reopen the produced DOCX with an independent parser;
- verify paragraph/table counts and required text;
- inspect relationships for missing media or links;
- render to PDF/images when layout matters and inspect every page for overflow, blank pages, clipping, bad page breaks, and font substitution;
- compare preserved features when editing an existing file;
- scan the output package for unexpected files or active content.

Report output path, source preserved, tools used, pages/sections checked, known viewer differences, and any feature that could not be preserved.
