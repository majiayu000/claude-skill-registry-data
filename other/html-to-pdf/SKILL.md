---
name: html-to-pdf
version: 1.0.0
description: "Export HTML pages to print-quality vector PDFs using Playwright's page.pdf() API. Trigger with /html-to-pdf or when the user wants to export an HTML page to PDF, create a print-ready PDF from HTML, or generate a PDF of a handout, card, flyer, or any HTML design."
---

# HTML to PDF — Print-Quality Export

Export HTML pages to high-quality, print-ready vector PDFs using Playwright's `page.pdf()` API.

## When to Use

Trigger with `/html-to-pdf` or when the user asks to:
- Export an HTML page to PDF
- Create a print-ready PDF from HTML
- Generate a PDF of a handout, card, flyer, or any HTML design

## Critical Rules

1. **NEVER screenshot-to-PDF.** Never render HTML as a screenshot (PNG) and convert to PDF. This rasterizes text into pixels — unacceptable for print. Always use Playwright's `page.pdf()` which produces vector PDFs with selectable, scalable text.

2. **Always emulate screen media.** Chromium's PDF renderer defaults to `print` media which washes out colors (dark backgrounds turn grey, accents look dull). Force `screen` media to preserve exact browser colors:
   ```js
   await page.emulateMedia({ media: 'screen', colorScheme: 'dark' });
   ```

3. **Always set `printBackground: true`.** Without this, backgrounds are stripped entirely.

4. **RGB output only.** Generate RGB PDFs. the user handles CMYK conversion in Adobe Acrobat with proper ICC profiles. Pillow's RGB→CMYK conversion produces off colors — never attempt it programmatically.

## How It Works

The skill uses Playwright (Node.js) via a temporary script to:
1. Launch headless Chromium
2. Set viewport to match the HTML page dimensions
3. Emulate screen media + dark color scheme for accurate color rendering
4. Navigate to the local HTML file
5. Export as PDF with exact page dimensions, zero margins, backgrounds enabled

## Page Size — Pixels vs. Physical Units

**Critical:** Playwright's `page.pdf()` interprets pixel dimensions at 96 DPI. If your HTML body is 1056×1632px and you pass `width: '1056px'`, the PDF page will be 11"×17" (1056÷96 = 11).

To get the correct physical size, you need **two things**:

1. **Physical units** (`in`, `mm`, `cm`) in `page.pdf()` for the page dimensions
2. **`scale` factor** to shrink the viewport content to fit the smaller page

The viewport renders at the full HTML pixel size (e.g. 1056×1632). Without scale, the content overflows the smaller physical page. The scale factor = physical size ÷ (pixel size / 96).

**Example:** HTML body is 1056×1632px, target is 5.5"×8.5" at 192 DPI:
- PDF page at 96 DPI = 528×816 CSS px, but viewport is 1056×1632
- Scale = 528/1056 = **0.5** (equivalently: target DPI 96 ÷ design DPI 192 = 0.5)
- Result: `width: '5.5in', height: '8.5in', scale: 0.5`

**Quick formula:** `scale = 96 / designDPI`. For 192 DPI → 0.5. For 144 DPI → 0.667. For 96 DPI → 1.0 (no scaling needed).

## Export Script

Create this script at `/tmp/pdf-export.mjs` and run it with `cd /tmp && node pdf-export.mjs`:

```js
import { chromium } from 'playwright-core';

// ── Configure these per export ──
const exports = [
  // { name: 'descriptive-name', file: 'filename-without-extension' },
];
const baseDir = './marketing/events'; // adjust per job
const pageWidth = 1056;   // match the HTML body width (px)
const pageHeight = 1632;  // match the HTML body height (px)
const pdfWidth = '5.5in';   // physical page width — use in/mm/cm, NOT px
const pdfHeight = '8.5in';  // physical page height — use in/mm/cm, NOT px
// ─────────────────────────────────

const browser = await chromium.launch();

for (const p of exports) {
  const context = await browser.newContext({
    viewport: { width: pageWidth, height: pageHeight },
    colorScheme: 'dark',
    forcedColors: 'none',
  });
  const page = await context.newPage();

  // Force screen media — critical for accurate colors
  await page.emulateMedia({ media: 'screen', colorScheme: 'dark' });

  await page.goto(`file://${baseDir}/${p.file}.html`, { waitUntil: 'networkidle' });

  await page.pdf({
    path: `${baseDir}/${p.file}.pdf`,
    width: pdfWidth,
    height: pdfHeight,
    scale: 0.5,              // 96 / designDPI — adjust if DPI changes
    printBackground: true,
    preferCSSPageSize: false,
    margin: { top: '0', right: '0', bottom: '0', left: '0' },
  });

  console.log(`${p.name}: PDF saved → ${p.file}.pdf`);
  await context.close();
}

await browser.close();
```

## Step-by-Step Workflow

1. **Read the HTML file** to get the page dimensions from the CSS (`body { width: Xpx; height: Ypx; }`).

2. **Create the export script** at `/tmp/pdf-export.mjs` with the correct:
   - `exports` array (one entry per HTML file)
   - `baseDir` pointing to the folder containing the HTML files
   - `pageWidth` and `pageHeight` matching the HTML body dimensions

3. **Ensure playwright-core is installed:**
   ```bash
   cd /tmp && npm list playwright-core 2>/dev/null || npm install playwright-core
   ```

4. **Run the export:**
   ```bash
   cd /tmp && node pdf-export.mjs
   ```

5. **Open the PDF for review:**
   ```bash
   open /path/to/output.pdf
   ```

6. **Verify quality:** Colors should match the browser exactly. Text should be selectable and crisp at any zoom level. Dark backgrounds should be true black, not washed-out grey.

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Washed-out / grey backgrounds | Print media default | Add `page.emulateMedia({ media: 'screen' })` |
| No backgrounds at all | Missing flag | Add `printBackground: true` |
| PDF is wrong physical size (e.g. 11×17 instead of 5.5×8.5) | Using `px` units in `page.pdf()`, or missing `scale` | Use physical units (`in`, `mm`) for `width`/`height` AND set `scale: 96/designDPI` (e.g. 0.5 for 192 DPI). Physical units alone cause clipping; `scale` alone leaves wrong page metadata. |
| Content clipped on right | Viewport too narrow | Match `viewport.width` to HTML `body` width exactly |
| Fonts not rendering | Google Fonts not loaded | Use `waitUntil: 'networkidle'` |
| Colors dull after printing | RGB→CMYK shift | Convert to CMYK in Adobe Acrobat with ICC profiles (not programmatic) |

## Figma Handoff (Optional Post-Export Step)

After exporting to PDF, you can push the HTML design into Figma for team editing and visual refinement:

1. **Serve the HTML locally** — The HTML file needs to be accessible via URL for Figma capture.
2. **Capture into Figma** — Use `mcp__figma-remote-mcp__generate_figma_design` to import the rendered page as a Figma design.
3. **Choose output mode:**
   - `newFile` — creates a fresh Figma file (good for new documents)
   - `existingFile` — adds to an existing Figma file (good for adding pages to an ongoing project)

**What this gives you:** The design imports as a visual snapshot that the team can annotate, adjust typography, reposition elements, or polish in Figma's editor.

**What it doesn't give you:** Fully editable Figma components with proper text layers. The capture is a high-fidelity visual import, not a native Figma rebuild. For most whitepaper/datasheet workflows, this is the right trade-off: the HTML/CSS file remains the source of truth for content and layout, while Figma handles collaborative visual refinement.

**When to use:** Whitepapers, datasheets, one-pagers, or any multi-page branded document where the team wants to review or refine the design collaboratively in Figma before final delivery.

## Output Location

Output saves alongside the source file.

---

## Dependencies

- **playwright-core** (npm) — installed locally in `/tmp/node_modules/`
- No global install needed; `cd /tmp && npm install playwright-core` is sufficient
- Uses system Chromium bundled with Playwright
