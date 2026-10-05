---
name: html-to-pdf
description: >-
  Convert HTML to PDF with pixel-perfect rendering, auto-fit overflow, and
  page-break rules. Use for HTML→PDF, print-ready forms/blanks layout checks,
  A4 fit-to-page, overflow detection, Puppeteer print CSS. (FST in-app blanks:
  prefer skill print-forms + printFit/print.css; this skill is upstream + CLI.)
version: "1.0.0"
author: aviz85
tags:
  - pdf
  - conversion
  - html
  - rtl
  - hebrew
allowed-tools: Bash, Read, Write, Glob
---

# HTML to PDF Converter

Pixel-perfect HTML to PDF conversion using Puppeteer (Chrome headless). Provides excellent support for Hebrew, Arabic, and other RTL languages with automatic direction detection.

## Why Puppeteer?

- **Pixel-perfect rendering**: Uses actual Chrome engine
- **Full CSS3/HTML5 support**: Flexbox, Grid, custom fonts, backgrounds
- **JavaScript execution**: Renders dynamic content
- **Automatic RTL detection**: Detects Hebrew/Arabic and sets direction
- **Web font support**: Loads custom fonts properly

## Auto-Fit (Built-in, No Flag Needed)

The script automatically handles content overflow:

- **Small overflow (up to ~18%)** → auto-shrinks font size to fit the page
- **Large content** → flows cleanly across multiple pages with smart page-break rules (no cutting headers, table rows, or images in half)
- **Fits perfectly** → does nothing

This runs automatically on every PDF generation. No flags needed.

## CRITICAL: Fit Content to Single Page

**Backgrounds on `html` or `body` cause extra pages!** Put backgrounds on a container element instead:

```css
@page { size: A4; margin: 0; }

html, body {
  width: 210mm;
  height: 297mm;
  margin: 0;
  padding: 0;
  overflow: hidden;
  /* NO background here! */
}

.container {
  width: 100%;
  height: 100%;
  padding: 20mm;
  box-sizing: border-box;
  background: linear-gradient(...); /* Background goes HERE */
}
```

**Common causes of extra pages:**
1. **Background on html/body** - always put on `.container` instead
2. Content overflow - use `overflow: hidden`
3. Margins/padding pushing content out

**Tips:**
- Use `--scale=0.75 --margin=0` if content still overflows
- For landscape: use `--landscape`

## Setup (One-time)

Before first use, install dependencies:

```bash
cd ~/.claude/skills/html-to-pdf && npm install
```

## Quick Usage

### Convert local HTML file:
```bash
node ~/.claude/skills/html-to-pdf/scripts/html-to-pdf.js input.html output.pdf
```

### Convert URL to PDF:
```bash
node ~/.claude/skills/html-to-pdf/scripts/html-to-pdf.js https://example.com page.pdf
```

### Hebrew document with forced RTL:
```bash
node ~/.claude/skills/html-to-pdf/scripts/html-to-pdf.js hebrew.html hebrew.pdf --rtl
```

### Pipe HTML content:
```bash
echo "<h1>שלום עולם</h1>" | node ~/.claude/skills/html-to-pdf/scripts/html-to-pdf.js - output.pdf --rtl
```

## Options Reference

| Option | Description | Default |
|--------|-------------|---------|
| `--format=<format>` | Page format: A4, Letter, Legal, A3, A5 | A4 |
| `--landscape` | Use landscape orientation | false |
| `--margin=<value>` | Set all margins (e.g., "20mm", "1in") | 20mm |
| `--margin-top=<value>` | Top margin | 20mm |
| `--margin-right=<value>` | Right margin | 20mm |
| `--margin-bottom=<value>` | Bottom margin | 20mm |
| `--margin-left=<value>` | Left margin | 20mm |
| `--scale=<number>` | Scale factor 0.1-2.0 | 1 |
| `--background` | Print background graphics | true |
| `--no-background` | Don't print backgrounds | - |
| `--header=<html>` | Header HTML template | - |
| `--footer=<html>` | Footer HTML template | - |
| `--wait=<ms>` | Wait time for fonts/JS | 1000 |
| `--rtl` | Force RTL direction | auto-detect |
| `--expect-pages=<N>` | Expected page count (warns if different) | 1 |
| `--no-page-check` | Disable page count warning | - |

## Automatic Overflow Detection

The script automatically checks page count after generating the PDF. By default, it expects 1 page and warns if the output has more:

```
⚠️  WARNING: PAGE OVERFLOW DETECTED!
   Expected: 1 page(s)
   Actual:   2 page(s)

   Fix: Reduce content, margins, or font sizes in HTML
   Use --no-page-check to disable this warning
```

**Usage:**
- Default: expects 1 page, warns on overflow
- `--expect-pages=3`: expects 3 pages (for multi-page documents)
- `--no-page-check`: disables the check entirely

**Note:** Requires `pdfinfo` to be installed (part of poppler-utils). If not available, the check is silently skipped.

## Examples

### Basic conversion:
```bash
node ~/.claude/skills/html-to-pdf/scripts/html-to-pdf.js report.html report.pdf
```

### Letter format with custom margins:
```bash
node ~/.claude/skills/html-to-pdf/scripts/html-to-pdf.js doc.html doc.pdf --format=Letter --margin=1in
```

### Hebrew invoice:
```bash
node ~/.claude/skills/html-to-pdf/scripts/html-to-pdf.js invoice-he.html invoice.pdf --rtl
```

### Landscape presentation:
```bash
node ~/.claude/skills/html-to-pdf/scripts/html-to-pdf.js slides.html slides.pdf --landscape --format=A4
```

### No margins (full bleed):
```bash
node ~/.claude/skills/html-to-pdf/scripts/html-to-pdf.js poster.html poster.pdf --margin=0
```

## Hebrew/RTL Best Practices

For best Hebrew rendering in your HTML:

1. **Set lang attribute**: `<html lang="he" dir="rtl">`
2. **Use UTF-8**: `<meta charset="UTF-8">`
3. **CSS direction**: Add `direction: rtl; text-align: right;` to body
4. **Fonts**: Use web fonts that support Hebrew (Noto Sans Hebrew, Heebo, Assistant)

### Example Hebrew HTML structure (single-page):
```html
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;700&display=swap" rel="stylesheet">
  <style>
    @page { size: A4; margin: 0; }
    html, body {
      width: 210mm;
      height: 297mm;
      margin: 0;
      padding: 0;
      overflow: hidden;
    }
    .container {
      width: 100%;
      height: 100%;
      padding: 20mm;
      box-sizing: border-box;
      font-family: 'Heebo', sans-serif;
      direction: rtl;
      text-align: right;
      background: #f5f5f5; /* Background on container, NOT body */
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>שלום עולם</h1>
    <p>זהו מסמך בעברית</p>
  </div>
</body>
</html>
```

## CRITICAL: Always Use scale=1.0 for Multi-Page PDFs

**NEVER use `--scale` < 1.0 for multi-page documents.** It causes:
- Content offset (not centered on page)
- RTL text overflow/clipping in grid layouts
- Unpredictable viewport width calculations

**Instead: reduce CSS font sizes and spacing to fit content at scale=1.0.**

```css
.page {
  width: 210mm;         /* Matches A4 exactly at scale=1.0 */
  height: 297mm;        /* Matches A4 exactly at scale=1.0 */
  padding: 8mm 10mm 12mm;
  page-break-after: always;
  position: relative;
  background: #f7f8fa;
  overflow: hidden;
  box-sizing: border-box;
}
```

**If content overflows at scale=1.0:** reduce font sizes (10-11px base), padding, margins — NOT the scale. This keeps 1:1 mapping between CSS and PDF, eliminating all layout artifacts.

**Color tip:** Pure white (#fff) backgrounds wash out colored accents. Use #f7f8fa or #f8fafb for subtle contrast that makes colors pop.

## Troubleshooting

### Fonts not rendering correctly
- Add `--wait=2000` for more font loading time
- Ensure fonts are loaded via `@font-face` or Google Fonts

### Hebrew appearing left-to-right
- Use `--rtl` flag to force RTL direction
- Add `dir="rtl"` to your HTML element

### Page breaks not working
Use CSS page-break properties:
```css
.page-break { page-break-after: always; }
.no-break { page-break-inside: avoid; }
```

### Backgrounds not showing
- Ensure `--background` is set (default is true)
- Use `--no-background` only if you want to exclude backgrounds

## Auto-Fit Content (MANDATORY VERIFICATION)

**CRITICAL - Claude MUST do this after EVERY PDF generation:**

1. **Read the PDF file** using the Read tool to visually inspect it
2. Check for **vertical overflow** (empty pages, content spilling to next page)
3. Check for **horizontal overflow** (text cut off at sides)
4. **If ANY issue found → FIX and regenerate** (max 5 attempts)
5. **Only deliver PDF to user after verification passes**

This is NOT optional. Never deliver a PDF without visual verification.

### Problems to Look For

| Problem | Symptom | Fix |
|---------|---------|-----|
| **Vertical overflow** | Empty space at page bottom, content on next page | Reduce `--scale` |
| **Horizontal cut-off** | Text cut at left/right edges | Reduce `--margin` AND fix HTML width |
| **Both issues** | Content cut AND extra pages | Fix HTML CSS first, then adjust scale |

### Fix Strategy (Max 5 Attempts)

**Attempt 1:** Default settings
```bash
node scripts/html-to-pdf.js input.html output.pdf
```

**Attempt 2:** If vertical overflow → reduce scale
```bash
node scripts/html-to-pdf.js input.html output.pdf --scale=0.9
```

**Attempt 3:** If horizontal cut-off → reduce margins
```bash
node scripts/html-to-pdf.js input.html output.pdf --scale=0.9 --margin=10mm
```

**Attempt 4:** If still issues → smaller scale + margins
```bash
node scripts/html-to-pdf.js input.html output.pdf --scale=0.8 --margin=5mm
```

**Attempt 5:** If still failing → FIX THE HTML CSS:
```css
/* Add to HTML to prevent horizontal overflow */
.container {
  width: 100%;
  max-width: 100%;
  overflow-wrap: break-word;
  word-wrap: break-word;
  box-sizing: border-box;
}
```

**STOP after 5 attempts** - regenerate HTML with proper constraints.

### HTML Width Fix (Required for Horizontal Fit)

If content is cut at sides, the HTML MUST have:

```css
html, body {
  width: 210mm;  /* A4 width */
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.container {
  width: 100%;
  max-width: 100%;
  padding: 15mm;
  box-sizing: border-box;
  overflow-wrap: break-word;
}
```

### Verification Checklist

After EVERY PDF generation, verify:
- [ ] All text visible (not cut at edges)
- [ ] No unnecessary empty pages
- [ ] Content fills pages properly
- [ ] No large gaps between sections

If ANY check fails → adjust and regenerate (max 5 times).

## Technical Notes

- Uses Puppeteer with Chrome headless for rendering
- Waits for `networkidle0` to ensure all resources load
- Automatically waits for `document.fonts.ready`
- Supports `@page` CSS rules for print styling
- Device scale factor set to 2 for crisp rendering
