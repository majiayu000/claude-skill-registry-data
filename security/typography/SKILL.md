---
name: typography
description: Use when styling or reviewing text in any medium; choosing fonts, size, spacing, measure, headings, emphasis, punctuation, or numeric typography; auditing websites, documents, slides, email, resumes, tables, or PDFs; or resolving a user's visual preference against typographic, accessibility, language, and delivery constraints
---

# Typography

Good typography reinforces the meaning of the text and conserves the reader's attention. Start with body text, but never apply body-text rules to every role. Treat Practical Typography as a benchmark, not a compliance standard. Rule IDs point to [provenance.md](provenance.md), which distinguishes source guidance (`PT`), project choices (`DEVIATION`), and current external requirements (`CURRENT`).

## Load only what the task needs `[ROUTE-001]`

- Character substitutions, punctuation, whitespace, emphasis, or literal text: [composition.md](composition.md)
- Paragraphs, headings, lists, quotations, tables, styles, pagination, columns, or grids: [layout.md](layout.md)
- Font selection, pairing, glyphs, features, or licensing: [fonts.md](fonts.md)
- Websites, responsive measure, actual font use, fallbacks, or accessibility: [web.md](web.md)
- Print, slides, email, resumes, tables of numbers, or PDF delivery: [media.md](media.md)
- Non-English, non-Latin, bidirectional, or mixed-script text: [international.md](international.md)
- Authority, scope, freshness, and evaluation coverage for a rule: [provenance.md](provenance.md)

Do not load every reference by default. A PDF containing Arabic code examples, for example, needs `media.md`, `international.md`, and the literal-text section of `composition.md`; a simple English print paragraph does not need `web.md`.

## Precedence

Apply this order whenever recommendations conflict `[CORE-002]`:

1. content correctness and semantics;
2. accessibility, language conventions, and legal or license constraints;
3. user intent and delivery medium;
4. Practical Typography benchmarks;
5. project presets and optional taste.

Preserve the user's requested aesthetic as far as higher-priority constraints allow. If it departs from a benchmark, label the departure once and give the benchmark alternative without repeatedly arguing the point.

## Gated audit

### 1. Classify context `[AUDIT-001]`

Identify the medium and delivery format, reading environment, intended audience, language and script, user intent, and the roles present: running prose, display heading, navigation, caption, table, code, data, and so on. State a material assumption if it cannot be verified.

### 2. Protect literal and semantic regions `[AUDIT-002]`

Before changing characters, classify spans as prose, code, command, URL, email address, identifier, measurement, legal reference, or data. Transform eligible prose only. Preserve unknown or mixed spans and report uncertainty instead of silently normalizing them. See [composition.md](composition.md).

### 3. Inspect the strongest available evidence `[AUDIT-003]`

Distinguish four levels:

1. authored source or declared styles;
2. computed or application formatting, including the font actually selected;
3. rendered pages, lines, and glyphs;
4. final delivery artifact, such as an exported PDF or printed page.

Use the highest level available and name what was not verified. Never present a source-only inference as a rendered fact.

### 4. Apply constraints `[CORE-002]`

Check semantics, accessibility, language/script behavior, font capability, licensing, and delivery reliability before aesthetic benchmarks. For web work, use [web.md](web.md); for unfamiliar languages or scripts, use [international.md](international.md).

### 5. Apply benchmarks in impact order `[AUDIT-004]`

1. **Body text:** font, size, line spacing, and rendered measure. For English-language running prose, Practical Typography's starting ranges are 15–25 px on the web, 10–12 pt in print, 120–145% line spacing, and about 45–90 actual characters per line `[TYPE-001]`. CSS `ch` is only a setup heuristic because it measures the zero glyph, not average characters; verify representative rendered lines or use the two-to-three-lowercase-alphabets test.
2. **Alignment and paragraphs:** use either first-line indents or paragraph space, not both; do not center running prose; justify only when language-aware line breaking and spacing produce an acceptable result `[TYPE-002] [TYPE-003]`.
3. **Headings:** keep hierarchy restrained, use the smallest visible distinction that works, avoid underlining and untracked caps, make space above exceed space below, and keep headings with what follows `[TYPE-004]`.
4. **Emphasis:** prefer one signal, keep emphasis shorter than a sentence when practical, do not underline non-links, and use genuine small caps with appropriate tracking `[TYPE-005]`.
5. **Composition:** inspect eligible prose for quotes, apostrophes, dashes, ellipses, symbols, ordinals, delimiters, and whitespace without altering literal content `[COMP-001..007]`.
6. **Supporting elements:** apply role-specific guidance for quotations, lists, code, tables, captions, navigation, callouts, slides, and other media. Do not invent exact ratios where visual calibration is the actual test.

### 6. Prioritize and report `[AUDIT-005]`

Report each actionable finding as:

```text
[MAJOR|MINOR] element: observed problem -> correction (value or edit; evidence level)
```

`MAJOR` means the defect materially harms reading, meaning, accessibility, language behavior, or delivery. `MINOR` means refinement whose absence does not materially block reading. Severity is contextual, not a fixed lookup table.

End every audit with:

- corrected values, code, or an edit list;
- the evidence level reached and any verification still needed;
- the three fixes expected to make the greatest improvement.

## Optional presets `[PRESET-001]`

These are project-authored starting points, not Butterick rules. Calibrate them against the actual font, content, viewport, and medium.

| Preset | Starting point | Intended feel |
|---|---|---|
| Bookish | 17–18 px, 1.3–1.4 leading, rendered lines near the middle of the source range, serif, first-line indents | dense, print-influenced |
| Airy screen | 19–21 px, 1.5–1.6 leading, narrower rendered measure, paragraph space | deliberately looser than the PT leading range |
| Compact docs | 15–17 px, 1.35–1.45 leading, wider but verified measure, modest paragraph space | information-dense documentation |

Use the smallest visible adjustment, render alternatives when possible, and judge the result in its delivery context `[CORE-001]`.
