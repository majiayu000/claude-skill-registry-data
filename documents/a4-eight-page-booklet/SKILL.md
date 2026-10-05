---
name: a4-eight-page-booklet
description: Use A4 Eight Page Booklet 2.2 to create, write, repair, impose, and validate a printable A4 one-sheet eight-page mini book or zine from text, notes, images, BIRD Graph JSON, iMandalArt/九宮, FIRE, outlines, templates, or PDFs. Use whenever the user says A4八頁小書, 八頁小書, 八頁小冊, 八格小書, A4一張八頁, 八頁在一頁, 8頁在一頁, 八張一頁, 一張紙變八頁, 摺頁書, 折頁小書, 迷你書, 小誌, zine, mini zine, booklet, 做成小書, 印成小書, 單張印出八頁, 幫我拼版, 八頁PDF, 合併八頁, 6-7-8-1／5-4-3-2排列, or asks for eight upright page PDFs, an eight-page reading PDF, an editable DOCX, or a correctly rotated A4 landscape print sheet.
---

# A4 八頁 Eight Page Booklet 2.2

Compile source material into a reproducible paper thinking object. Version 2.2 is the Skill integration release; it keeps `BookletManifest 2.0` for backward compatibility, then renders every output from that manifest.

The 2.2 Skill remains in alpha while deterministic scripts are being implemented. Preserve the verified 1.x direct-PDF workflow as `legacy-direct`; do not claim script-backed validation when a named script is absent.

## Three Kings 2.2 Integration

A4 Eight Page Booklet is the **paper publishing king** in the three-skill chain:

`iMandalArt 2.2 overview -> BIRD 2.2 seven Routes -> A4 Booklet 2.2 reading PDF + print sheet + DOCX`

- Put the iMandalArt center and overview on page 1 without changing its spatial identities.
- Put seven BIRD Routes on pages 2-8 and preserve source IDs, citations, addresses, and merge reasons.
- Deliver synchronized reading, printing, editing, preview, companion, and validation artifacts.

## Output Contract

For a complete build, produce:

```text
booklet-output/
├── booklet-manifest.json
├── companion.md
├── pages/page-01.pdf ... page-08.pdf
├── reading-8-pages.pdf
├── print-a4-landscape.pdf
├── editable-pages.docx
├── previews/contact-sheet.png
├── previews/print-imposition.png
└── validation-report.json
```

Keep all eight single-page PDFs upright. Generate the reading PDF in page order 1–8. Generate the A4 print sheet only after the single pages pass structural checks.

When the user requests a Japanese textbook listening booklet, all three learner-facing formats are mandatory:

1. `print-a4-landscape.pdf`: one A4 landscape sheet imposed for folding into eight pages.
2. `reading-8-pages.pdf`: eight upright pages in reading order for Voice Dream Reader.
3. `editable-pages.docx`: an editable eight-page Word file that opens cleanly in Apple Pages without blank pages.

## Core Workflow

1. Inspect every supplied source before drafting.
2. Select one dominant content mode; combine modes only when the user or material requires it.
3. Normalize content into `BookletManifest 2.0`. Read [references/manifest-schema.md](references/manifest-schema.md) before creating or validating the manifest.
4. Preserve source IDs, BIRD addresses, verified deep links, citations, route references, and explicit ordering.
5. Draft eight page objects before rendering. Give each page one strong idea plus three to five short lines or one readable visual block.
6. Store long context, complete cards, citations, selection reasoning, and cross-route notes in `companion.md`.
7. Render eight upright single pages first. Use existing deterministic scripts when present; during alpha, use the PDF skill and preserve the manifest as the source of truth.
8. Merge pages 1–8 into the reading PDF.
9. Render a contact sheet, identify the visible booklet page number on every source page, then impose the A4 print sheet using the fixed physical map below.
10. Render previews and perform V1–V4 validation. Record results in `validation-report.json`; do not report a check as passed without current-run evidence.

## Japanese Textbook Listening Mode

Use this mode for `みんなの日本語` and comparable lesson-based Japanese materials.

- Write every learner-facing page entirely in Japanese. Keep Chinese analysis, translations, and production notes in `companion.md`, not in the booklet.
- Use only genuine sentences found in the supplied lesson's sentence patterns, example sentences, dialogue, and Exercises A–J. Do not invent replacement examples when source sentences are available.
- Preserve question-answer pairs and dialogue turns as complete listening chunks. Mark their source section in the manifest.
- Page 1 must contain two iMandalArt nine-grids: a directory grid and a grammar/keyword index grid. Preserve the の字型 coordinates defined below.
- Pages 2–8 contain seven semantic learning Routes. Each page should have one short Japanese heading, one audible route cue, three to five authentic examples or dialogue turns, and one concise Japanese takeaway.
- Design for presbyopia: body text should normally be 16 pt or larger on upright A7 pages; headings 20–24 pt; avoid dense furigana and low-contrast gray. If the source cannot fit, reduce sentence count before reducing body text below 15 pt.
- Design for Voice Dream Reader: use true text, logical page order, simple punctuation, short headings, and one sentence or dialogue turn per paragraph. Do not use text rendered only as an image. Avoid decorative symbols that a speech engine will read aloud unnecessarily.
- Insert a short pause marker only when useful for shadowing. Prefer Japanese labels such as `聞きましょう`, `止めましょう`, and `声に出しましょう`; do not fill pages with repeated ellipses.
- The reading PDF and DOCX must follow the same page sequence and wording. The imposed print sheet may change placement and rotation only.

## Source Types

Accept these source types:

- `text`: article, note, chapter, manuscript, reflection, or daily plan.
- `bird_graph`: Book, Route, Keyword, Context, Chunk, Node, and Edge data.
- `imandalart`: center plus eight cells, including standard and の字型 layouts.
- `fire`: Full-D, Index, Route, and Evolution notes.
- `outline`: Bike, Bonsai, Markdown, or another explicit hierarchy.
- `pdf_pages`: existing pages, templates, scans, or prior booklets.
- `mixed`: multiple source types with explicit source mapping.

Use only the analysis skills that the source needs. Do not force FIRE, BIRD, iMandalArt, or Daily Plan semantics onto unrelated material.

## Content Modes

### Classic Eight Pages

Use this default sequence when no stronger structure exists:

1. Cover or center question.
2. Overview or route map.
3. Entry or transition.
4. Core claim or scene.
5. Method, equipment, or risk.
6. Relation, collaboration, or revision.
7. Reflection, tension, or judgment.
8. Next action, gratitude, or return commitment.

Respect user-supplied page headings. Fill a missing page 1 as cover or overview only when needed.

### Seven Routes

Use for BIRD, book deconstruction, knowledge systems, and 64＋8＋1:

- Page 1: one directory nine-grid plus one keyword nine-grid.
- Pages 2–8: seven Route pages.
- Give each Route page one center claim, three to five concise points, and one ordered path.
- If eight source Routes must become seven reading Routes, merge only semantically compatible routes and record the mapping and reason in the manifest.

### Mandala Eight Angles

Use for iMandalArt-centered material:

- Page 1: center and overview grid.
- Pages 2–8: seven readable angle pages.
- If two of eight angles are combined, record both source identities and the merge reason.
- Never silently change the supplied spatial order.

### Daily Paper Loop

Use for daily or weekly planning. Organize capture, frog, calendar, time grid, eight life areas, journal, plan, and review into a writable paper loop.

### PDF Repair

Use when content must remain unchanged. Repair only page order, rotation, merging, safe margins, legibility, or imposition unless the user explicitly requests rewriting.

## BookletManifest Rules

Use `schema_version: "2.0"`. Require exactly eight uniquely numbered page objects. Store content in typed blocks rather than page-specific ad hoc fields.

Initial allowed block types:

- `title`
- `paragraph`
- `bullets`
- `quote`
- `route`
- `mandala`
- `image`
- `qr`
- `write_area`
- `source_note`

Use `source_refs`, `route_refs`, and citation IDs instead of copying long evidence into paper pages. Keep render choices under `render`; keep QA observations under `validation`.

## BIRD Integration

When the source is BIRD:

- Use Book Address for structural location, not for semantic routing.
- Use Index `W + T + K + A` to choose and label retrieval terms.
- Use Route for ordered cross-page reasoning.
- Preserve verified Deep Links byte-for-byte; leave proposed links blank or pending.
- When 64 Keywords are compressed to eight visible entrances, retain all 64 IDs and record which keywords each entrance represents.
- Keep Context and Chunk content in companion material unless it remains readable on paper.

Use `thebrain-bird-address` for BIRD assignment or audit. Do not invent weights, evidence, or deep links.

## iMandalArt 2.2 Integration

Use `imandalart` for source analysis and complete 11-line text cards. Preserve these の字型 coordinates:

Directory grid:

```text
Ⓕ　Ⓒ　Ⓖ
Ⓑ　◎　Ⓓ
Ⓔ　Ⓐ　Ⓗ
```

Keyword child grid:

```text
⑥　③　⑦
②　◎　④
⑤　①　⑧
```

Treat the center identity as `Ⓘ` when useful but always display `◎`. Preserve `Ⓐ` or `①` as the first semantic item even though it appears at bottom center. Never convert the layout to ordinary reading order. Keep full 11-line cards in the companion Markdown; a simplified paper grid may shorten text but must preserve coordinates. Store citations and cross-route notes outside cramped cells.

## Content Normalization

- Rewrite source into reader-facing paper language.
- Remove meaningless raw labels such as `副題：`, `用途：`, `日期：`, `資訊：`, `格式：`, or `主軸：` unless they carry meaning.
- Preserve personal wording when it carries identity or emotional force.
- Keep each page focused and leave space for handwriting.
- Mark weak claims as `待證`, `推論`, or `需補例`.
- Scan manuscripts and PDFs for user-blocked names, tags, schools, or phrases.

## PDF Generation

Generate upright single pages using A7 portrait proportions: one finished page is one eighth of A4, approximately `74.25 × 105 mm`. Use a fold-safe inset of roughly 10–14 pt. Keep page numbers, footer labels, QR blocks, and frames inside the safe area.

Impose on one A4 landscape page:

- Top row left to right: visible booklet pages `6, 7, 8, 1`, upright.
- Bottom row left to right: visible booklet pages `5, 4, 3, 2`, each rotated 180 degrees.

Treat these numbers as semantic booklet page numbers, not source-PDF indices. A source PDF may already be stored in imposition sequence such as `6,7,8,1,5,4,3,2`, and some source pages may already be visibly upside down. Render all source pages, map their visible page labels, and record the correction needed to make every source page upright before placing anything. Do not trust filenames, file order, `/Rotate`, or other PDF metadata alone.

Use exact A4 landscape dimensions, approximately `841.89 × 595.276 pt`. Divide the sheet into four equal columns and two equal rows. Fit each upright A7 page inside one cell without cropping or stretching.

When fold guides are requested, draw light dashed lines at one-quarter, one-half, and three-quarters of the sheet width, plus the horizontal midpoint. Draw the central cut as a solid line along the midpoint from one-quarter to three-quarters of the sheet width. Otherwise omit guides. Preserve blank space around fold paths and keep the print imposition separate from the upright reading PDF.

For image-based or scanned pages, prefer a single grayscale A4 raster of about `3368 × 2381 px` at 288 dpi. Use grayscale mode `L`/`DeviceGray`, high-quality resampling, and a white background. For vector pages, normalize page rotation to content before applying placement transforms.

Print instructions must say: A4 landscape, one-sided, actual size 100%, no automatic rotation, and no fit-to-page scaling.

### Visible-Page Mapping Procedure

1. Render the eight source pages to PNG and make a contact sheet.
2. Read the printed page labels or identify the cover and content sequence visually.
3. Build a semantic map from booklet page number to source-PDF index and an orientation correction for every source page.
4. Normalize every source page to upright.
5. Place semantic pages `6,7,8,1` across the upper row without further rotation.
6. Place semantic pages `5,4,3,2` across the lower row and rotate each normalized panel 180 degrees.
7. Render the resulting A4 PDF again. Confirm the visible arrangement, not merely the transform matrix.

If a transformed preview disagrees with the intended layout, stop and correct the semantic mapping. For fragile scanned PDFs, reconstruct the sheet from rendered upright page images; this avoids inherited crop boxes and hidden transforms.

## Template And Fold Feedback

Render supplied PDF templates to PNG before inferring visual rotations or coordinates. Do not trust PDF metadata alone.

Treat a photograph or scan of the physically folded booklet as stronger evidence than a screen preview. Preserve paper size and page order while moving content inward or reducing density. Save corrected builds with a clear `foldsafe` suffix without overwriting the prior build.

## Validation Gate

Perform four levels:

### V1 Structure

- Confirm exactly eight unique page numbers.
- Confirm every reference target exists.
- Confirm required manifest fields and source mappings.
- Confirm seven-route or Mandala merges have recorded reasons.

### V2 Typography

- Confirm a Chinese-capable font is embedded or available.
- Confirm pages are upright, nonblank, legible, and unclipped.
- Confirm text stays inside fold-safe bounds.
- Confirm blocked or unwanted labels are absent.
- For large-print Japanese builds, confirm body text is at least 15 pt and that every Japanese glyph renders correctly.

### V3 Imposition

- Confirm the print PDF is exactly one A4 landscape page.
- Confirm the rendered top row is visibly `6,7,8,1`, upright.
- Confirm the rendered bottom row is visibly `5,4,3,2`, upside down.
- Confirm visible page numbers and upright corrections were mapped independently of source-PDF index order and rotation metadata.
- When guides are present, confirm the central solid cut spans only the middle two cells and all other fold lines are light and dashed.
- Confirm the reading PDF has eight equal-size pages.

### V4 Visual

- Render all eight reading pages and the print sheet to PNG.
- Inspect for clipping, overlaps, missing glyphs, wrong rotations, empty pages, and inconsistent margins.
- Prefer a contact sheet for whole-book review and inspect dense pages individually.
- Open the DOCX with a Pages-compatible renderer or Apple Pages. Confirm exactly eight nonblank pages and no empty page caused by a trailing manual page break.
- Build DOCX page transitions with paragraph `page_break_before`, not standalone manual page-break paragraphs. Leave enough bottom safety space for Pages reflow.

### V5 Listening And Source Fidelity

- Extract text from `reading-8-pages.pdf` and confirm Japanese text is selectable and follows pages 1–8.
- Confirm headings and body text read in a sensible order without headers or footers interrupting every sentence.
- Confirm every learner-facing example maps to a supplied textbook sentence-pattern, example, dialogue, or Exercise A–J source item.
- Confirm the booklet contains no fabricated example presented as textbook text.
- Confirm the PDF and DOCX learner text are synchronized.

Write pass, fail, not-run, evidence path, and notes for every check in `validation-report.json`. If an alpha build lacks automated overflow detection, mark that check as visual/manual rather than automated.

## 1.x Compatibility

Keep the established direct workflow available as `legacy-direct`:

1. Draft companion Markdown.
2. Generate `page-01.pdf` through `page-08.pdf` upright.
3. Merge the reading PDF.
4. Render a contact sheet and map visible booklet page numbers.
5. Impose the A4 print sheet using the fixed `6,7,8,1 / 5,4,3,2` map.
6. Render and inspect previews.

When using `legacy-direct`, create a manifest from the finished page plan so future rerenders have a stable source. Do not remove or rewrite existing user templates during the 2.0 alpha phase.

## Resource Routing

- Use `scripts/impose_a4_eight_page.py` after establishing the semantic page and orientation maps. For a true upright reading-order PDF, omit both mapping options. For a PDF stored as visible pages `6,7,8,1,5,4,3,2`, pass `--source-order 6,7,8,1,5,4,3,2`. If its last four source pages visibly start upside down, also pass `--source-rotations 0,0,0,0,180,180,180,180`. Add `--guides` only when the user wants printed fold and cut lines.
- Read [references/manifest-schema.md](references/manifest-schema.md) for the canonical manifest fields and validation rules.
- Read [references/mandala-grid-v1.md](references/mandala-grid-v1.md) when preserving the existing Mandala-Grid human-readable source format.
- Read [references/japanese-lesson-bird-graph.md](references/japanese-lesson-bird-graph.md) when textbook example sentences must become BIRD Chunks, grammar and vocabulary Indexes, semantic Routes, a Seven Routes booklet, or a synchronized Voice Dream reading document.
- Use the PDF skill for PDF creation, merging, rendering, and visual verification.
- Use Skill Tree Manager when changing version, status, dependencies, cross-app links, or promotion from alpha to active.

## 2.2 Promotion Gate

Keep 2.0 in alpha until all conditions pass:

1. One manifest can deterministically rebuild all outputs.
2. BIRD Seven Routes, Daily Paper Loop, and PDF Repair cases each pass V1–V4.
3. の字型 directory and keyword coordinates have an automated check.
4. At least one physical print, cut, fold, and photo-feedback cycle passes.
5. Skill validation passes and `agents/openai.yaml` matches this contract.
