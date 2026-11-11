---
name: html-to-pdf
description: "Builds polished PDF documents (one-pagers, reports, guides, proposals, briefs) as HTML and CSS with exact page layout, renders them with headless Chromium through Playwright, then checks every page as an image before handing the file over. Fixed page sizes, controlled page breaks, no split tables, no orphan headings, a page count you can promise. Use when someone says \"make a PDF\", \"turn this into a PDF report\", \"make a one-pager\", \"PDF version of this doc\", \"export this as a printable guide\", \"it has to fit on two pages\" or \"the PDF layout is broken\"."
---

# HTML to PDF

Most converters give you a PDF but not control: a half-empty last page, a lone heading at the bottom, a table cut in half. This skill writes the document as HTML and CSS, prints it with headless Chromium, and looks at every page before calling it done.

## What it does

1. Turns content (notes, a draft, data, a brief) into a single self-contained HTML file laid out page by page.
2. Renders it to PDF with headless Chromium. No window ever opens.
3. Exports each page as a PNG, checks it by eye and by script, fixes problems and renders again.
4. Hands over the PDF with its page count, size and the QA it passed.

## What you need

- Python 3.9 or newer.
- Playwright and Chromium:
  ```
  pip install playwright pypdf pypdfium2
  python -m playwright install chromium
  ```
  `pypdfium2` is only for PNG export. If it is missing, the script falls back to `pdftoppm` from poppler.
- The content, the audience, the paper size (A4 or Letter) and a target page count. If any are missing and cannot be inferred, ask once; otherwise default to A4 and the shortest length that fits.
- Puppeteer works too (same engine, same CSS).

## Steps

1. **Plan the pages.** Before writing HTML, write a one-line outline per page: what goes on page 1, page 2, and so on. A one-pager is one page. A report is usually a cover plus 2 to 6 pages. Decide the page count now, not after rendering.
2. **Copy the template.** Start from `templates/document.html`. It has a cover page, a content page, a key-number grid, two columns, a table, a callout and a footer, all in neutral styling with `[placeholders]`. Swap the colour and font tokens in `:root` if the reader has a brand.
3. **Fill one `.page` block per planned page.** Real content, not lorem ipsum. Lead with the point.
4. **Render:**
   ```
   python scripts/render_pdf.py report.html out/report.pdf --png-dir qa/ --expect-pages 3
   ```
   It prints the page count, file size and PNG paths, and warns about overflowing content, fonts that did not load, broken images, and a mismatch between `.page` boxes and PDF pages. Add `--strict` to make any warning a failure.
5. **Look at every PNG** against the QA list below. The script catches overflow; only your eyes catch ugly.
6. **Fix and render again.** Repeat steps 4 and 5 until every page passes. Old PNGs are cleared on each run so you never review a stale render.

## Layout rules

**Two ways to lay out pages. Pick one per document.**

- **Fixed pages (default, used by the template).** Each `<div class="page">` is exactly one sheet: `width` and `height` set to the paper size, `overflow: hidden`, `break-after: page`. You decide what goes on each page, so the page count is guaranteed. Best for one-pagers, covers, proposals and anything with a promised length.
- **Flowing text.** For long prose (guides, manuals) let content flow and use `@page { size: A4; margin: 20mm; }` with break rules. Page count is then an output, not an input, so check it every render.

**Always:**

- Set the paper size once, in `@page { size: A4; margin: 0; }` (or `Letter`), and render with `prefer_css_page_size=True`. Letter is 8.5in by 11in, A4 is 210mm by 297mm. Never mix them.
- Use print units (`mm`, `in`, `pt`) for page boxes, margins and type. Body text 10 to 11pt, captions 8pt, nothing under 7.5pt.
- Keep things whole: `break-inside: avoid` on cards, metric grids, callouts, figures and table rows. `break-after: avoid` on headings so a heading never ends a page.
- `orphans: 3; widows: 3;` on paragraphs so a single line is never stranded.
- Tables: `thead { display: table-header-group; }` repeats the header if a long table must continue. Otherwise move the whole table to the next page or split it at a logical row.
- Turn on `print-color-adjust: exact` and render with print backgrounds, or tinted panels vanish.
- Self-contained file: inline CSS, inline SVG charts, images as local files or data URIs. Every remote font or image is a chance to render with a fallback.
- Fonts: system font stacks are safest. If you load a web font, keep the fallback stack and check the script's font warnings.
- Pin footers with `margin-top: auto` in a flex column, not absolute positioning, so overflow is detectable.
- No empty pages, and the last page should not be mostly blank. Consolidate or cut copy.

## QA

Run the script, then check each page image for:

- **Overflow:** text clipped at the bottom or right edge, or content hidden under the footer.
- **Orphans:** a heading at the foot of a page with its text on the next, or one stray line of a paragraph.
- **Cut tables and cards:** rows, metric grids or callouts split across pages.
- **Fonts:** the intended typeface, not a Times fallback. The script lists any font that failed to load.
- **Images and charts:** every image loaded, every SVG drawn, labels readable.
- **Contrast:** bold text, links and labels inside dark or tinted panels are still visible. A global text colour often hides nested `strong` on dark cards.
- **Page count:** matches the plan. Use `--expect-pages N` so the script fails if it drifts.
- **Folios and footers:** page numbers correct ("2 / 3"), no stale totals left from an earlier draft.
- **File size:** a few MB at most for email (the script warns over 10 MB). Resize large photos before embedding.
- **Text check (optional):** extract the text (`pdftotext -layout`) and search for leftover `[placeholders]`, typos in names and figures that must match the source.

After any fix, even a one-line CSS change, re-render the PDF and regenerate every PNG before saying it passed. Screenshots from before a fix prove nothing.

## Output

- The PDF, named in kebab-case for what it is: `q3-board-report.pdf`, `onboarding-guide.pdf`.
- The HTML source next to it, so the next edit is a re-render.
- A short note: page count, paper size, file size, and anything you could not verify.
- QA images stay out of the deliverable folder.

## Honest limits

- Chromium print is not a typesetting engine. Hyphenation, footnotes and running headers that change by chapter are weak. For a book, use a dedicated tool.
- Fixed pages hide overflow by design (`overflow: hidden`). That is why the script measures it; never skip the warnings.
- `break-inside: avoid` is a request. A block taller than a page will still split.
- Remote fonts and images can fail silently on slow networks. Self-contain the file when it matters.
- Visual QA needs a model or person that can see images.
- It produces a print PDF, not an accessible tagged PDF or a fillable form.
