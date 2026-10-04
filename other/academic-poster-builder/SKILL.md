---
name: academic-poster-builder
description: Build, critique, and refine academic posters from a paper, LaTeX project, reference draft image, HTML/CSS source, PPT/PDF outputs, or local figure assets. Use when Codex is asked to create or improve a research poster, convert a poster design to HTML/PDF/PPTX, fix poster layout/typography/overflow/blank-space issues, or preserve paper figures and result semantics in a poster.
---

# Academic Poster Builder

## Operating Principle

Treat the poster as a compressed argument, not a decorated paper summary. Build a clear logic flow:

1. Why the problem matters.
2. What the method changes.
3. Why the method works.
4. How strongly the results support the claim.

For A0 portrait top-conference posters, prefer a restrained three-column structure with a wider center column for method and mechanism figures. Use flexible layout only when it serves the argument; avoid chaotic unindexed panels or content islands.

## Source Audit

Before redesigning, inspect the actual paper sources and assets.

- Read abstract, introduction, method, main results, conclusion, and appendix figure/table references.
- Search local assets first: `rg --files`, paper `res/`, figure PDFs, screenshots, tables, logos, QR images, and previous poster outputs.
- Prefer original paper figures/tables over redrawing. Crop/trim original figures when needed, but do not replace them with approximate sketches unless no asset exists.
- Verify result semantics from the paper. Do not infer that a baseline is trained with off-policy traces unless the paper says so.
- If a reference poster/draft image exists, use it to identify expected content, icons, and hierarchy, not as an exact layout to copy.

## Canonical A0 HTML Setup

Use standard A0 portrait physical size and keep export dimensions consistent.

- Physical size: `841mm x 1189mm` (often described as 84cm x 119cm).
- Stable CSS canvas: `3179px x 4494px` at 96dpi.
- 150dpi PNG target: about `4967px x 7022px`; exporting from the CSS canvas with `deviceScaleFactor: 150 / 96` is acceptable.
- PDF export: Playwright `page.pdf({ width: "841mm", height: "1189mm", printBackground: true, margin: 0 })`.
- If generating PPTX, set the slide to A0 portrait size; do not let pixel dimensions become physical page dimensions.

## Content Architecture

Use this default flow unless the paper demands otherwise:

- Header: conference mark, title, subtitle, authors, affiliations, institution logos, QR links.
- Metric strip: four high-signal result cards with icons, large values, and one-line comparisons.
- Thesis strip: one sentence stating the poster's central claim.
- Left column: motivation, mismatch/failure mode, method design contract or equations.
- Center column: method overview, key mismatch figure, mechanism evidence.
- Right column: main results, generalization/extensibility, sensitivity/robustness, one concise conclusion.

Keep exactly one summary section: either `Conclusion`, `Takeaways`, or `Key Takeaways`, not several.

## Layout Rules

- Prefer three columns, with center column wider when it contains large method/analysis figures.
- Preserve reading order from top to bottom and left to right. Avoid putting late-numbered sections in the first column unless intentionally restructuring all section numbers.
- Make large paper figures occupy wide columns. Do not squeeze an overview/method figure into a narrow column when it needs 1.5-2 columns of width.
- Align the lowest panels across columns. Bottom whitespace should read intentional, not accidental.
- Use section panels with clear headers, but do not nest decorative cards inside cards.
- If a section has no explanatory text, add a concise analysis sentence from the paper; if it only has text, consider whether a paper figure/table belongs there.
- If a narrow-column figure has awkward aspect-ratio whitespace, preserve the complete figure first. Do not split/crop it in a way that removes context unless the user explicitly wants a crop or the split remains semantically complete.
- Use nearby text sections to absorb meaningful content when a figure must remain complete. Add paper-backed context that strengthens the local argument, such as problem constraints, assumptions, design principles, or mechanism conclusions.
- When there is blank space, reason in this order:
  1. Is an essential paper result, figure, equation, mechanism, or limitation missing?
  2. Should an existing figure/table be larger so its text is readable?
  3. Would preserving figure completeness require adding concise context to adjacent sections?
  4. Should redundant content be deleted and the remaining content rebalanced?
  5. Only then add a short evidence-bearing note.

Never fill space with generic text just to occupy area.

## Typography

Make the poster readable without zoom.

- Use stable fixed sizes, not viewport-scaled font sizes.
- Body text should be visually consistent across sections.
- Section-specific explanatory notes must not drift smaller than the global body scale. In particular, robustness/sensitivity notes and mechanism notes should read like body text, not footnotes.
- Figure text should be at least comparable to body text where possible; if not, enlarge or crop the figure.
- Keep title and subtitle visually related. Avoid a huge bold title with a tiny subtitle/author block.
- Avoid heavy display weight. In CSS, prefer weights around `460-650`; avoid broad use of `800/900`.
- Keep letter spacing `0`; do not use negative letter spacing.
- Two-digit section numbers need pill/capsule labels or enough width so they never overflow.

## Figures, Tables, and Equations

- Use original paper assets for method overview, distribution/mismatch illustrations, dynamics plots, sensitivity plots, and equations.
- Comparable plots must use equal sizes. For example, entropy, off-policy log-probability, and on-policy log-probability should not appear at different scales unless there is a reason.
- Do not split a coherent paper figure unless the split improves legibility, preserves the complete context, and the user asked for it. If a split hides part of the original figure, revert to the complete figure and use text/content balancing elsewhere.
- Equation screenshots must be at least as readable as body text. If later equations are small, add a special larger class or allocate more vertical space.
- Tables should be simplified but semantically faithful. Avoid duplicating the same result table in multiple sections.
- A bar chart or mini table needs a label explaining what it measures; otherwise it is visual noise.

## Section-Level Content Heuristics

- Early problem sections can absorb short paper-backed context about constraints, stakes, assumptions, or why the problem setting makes the method necessary.
- Method sections can absorb compact design principles or invariants that explain why the method is structured the way it is.
- Failure-mode sections should preserve full illustrative figures when the figure is evidence. If the full figure creates empty space in a narrow column, adjust surrounding text or panel allocation before cropping.
- Mechanism sections should include concise interpretive conclusions that explain what the plots prove, not just what they show.
- Sensitivity/robustness sections need text at the global body scale explaining what the plots establish. Do not leave them as two small plots with a tiny footnote.

## Logos, Icons, and QR Codes

- Use official/source logos when available. Do not hand-draw university logos if a local or web asset exists.
- Metric cards should use icons, not text placeholders. Keep the four top metrics visually parallel.
- QR codes can include captions (`GitHub`, `arXiv`, `WeChat`) when captions aid scanning.
- QR codes should be large enough to scan from a poster; avoid tiny decorative QR blocks.
- Remove footer metadata unless the poster venue requires it. Put URLs near QR codes instead.

## Iteration and QA

After each meaningful layout change, render and inspect the poster.

Use Playwright or the Browser plugin to render the HTML at the A0 CSS canvas. Check:

- `document.body.scrollWidth === 3179`
- `document.body.scrollHeight === 4494`
- `posterBottom` equals the page height.
- Every panel has `scrollHeight <= clientHeight + tolerance`.
- The last panel in each column ends at approximately the same y-coordinate.
- No text touches borders; no captions or table rows are clipped.
- Large bottom gaps are intentional and balanced.

If using flex columns, remember that panels may shrink unless `flex-shrink: 0` is set. Fixed canvas height plus `overflow: hidden` can hide real problems; always measure panel scroll sizes.

See `references/poster-qa-checklist.md` for a compact implementation checklist and a Playwright measurement snippet.

## Delivery

Return links to updated artifacts:

- HTML source.
- PNG preview.
- PDF A0.
- Editable PPTX when requested.

Briefly report the verification results that matter: no overflows, page size, and column bottom alignment. Do not claim visual correctness without rendering or screenshot inspection.
