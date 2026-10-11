---
name: portfolio-cv-pdf-from-site-content
description: "Use when a portfolio has no CV or resume, a recruiter needs a downloadable one-page PDF, a generated CV PDF spills onto page two although a screenshot or viewport measurement said it fits, the CV needs reprinting after a title or content change, or a Download CV link needs wiring."
---

# CV PDF from site content

Goal: a recruiter-ready one-page PDF built from facts the repo already commits,
regenerable after any content change, with no invented credentials.

Worked example: the Astro portfolio at `D:/AlexMollard`, whose audit found "no CV anywhere
in `public/`" as a Tier-1 hireability gap. It now ships `scripts/cv.html` ->
`public/alex-mollard-cv.pdf`. Nothing here is Astro-specific.

## 1. Source the facts, do not recall them

Never write a CV from conversation memory. Pull each claim from committed data:

```bash
# roles/dates/titles straight out of the content collection frontmatter
for f in src/content/projects/*.md; do
  sed -n 's/^title: //p;s/^date: //p;s/^role: //p;s/^category: //p' "$f" | paste -sd'|'
done | sort
```

Then **grep the repo for every skill/platform line you are about to claim**:

```bash
grep -rio "nintendo switch\|unity\|steamworks\|playfab\|playgo" src/content/ | sort -u
```

Anything with zero hits comes out: on the real run "Nintendo Switch" was plausible,
unsourceable, and deleted. A hit also dates the claim. Unity hits only older work
(`frozen-depths.md`, dated 2021, and the 2019-2020 bullet in `early-work.md`), so it
may be listed as past experience, never as a current tool.

Education, referees, and exact employment dates are **not** in the content collection.
Ask the owner or omit; never infer a qualification from a framework name in a frontmatter
field (`engine: AIE Bootstrap` is not a diploma). For `D:/AlexMollard` the owner's answers
are in `alexmollard-portfolio-house-rules`.

## 2. Keep an editable source in-repo

Write `scripts/cv.html` - plain HTML + CSS, no build step, no dependency. It is the source
of truth; the PDF is a build artifact the owner can reprint after any promotion or
shipped title.

Print-critical CSS (the values `D:/AlexMollard` fits one page with, 2026-09-24):

```css
@page { size: A4; margin: 10mm 13mm; }
body { font-family: "Segoe UI", Arial, sans-serif; font-size: 8.5pt; line-height: 1.28; }
.titles { column-count: 2; }   /* shipped-title lists halve their height */
```

## 3. Print it

Any Puppeteer-style handle works:

```js
const cv = await browser.open({ name: "cv", url: "file:///ABS/PATH/scripts/cv.html" });
await cv.run(async ({ page }) => {
  await page.pdf({ path: "public/alex-mollard-cv.pdf", format: "A4",
                   printBackground: true, preferCSSPageSize: true });
});
```

## 4. The trap: prove one page at PRINT width

A screenshot at a 1000px viewport showed content ending well short of the fold - and the
PDF was still **two pages**. Print lays out at page width minus the *side* margins, so
text reflows taller than any wide-viewport measurement suggests. Measuring wide
under-reports height and gives a false one-page verdict.

```
content width  = 794px (A4 @96dpi) - (left + right margin in mm x 3.7795)
content height = 1123px - (top + bottom margin in mm x 3.7795)
```

For `margin: 10mm 13mm` that is **696 x 1047**. Subtract both side margins: 745 (794
minus a single 13mm margin) is still too wide and passes falsely.

Measure at print width with print media emulated:

```js
await cv.run(async ({ page }) => {
  await page.setViewport({ width: 696, height: 1047 });
  await page.emulateMediaType('print');
  await page.goto("file:///ABS/PATH/scripts/cv.html");
  const h = await page.evaluate(() => document.body.scrollHeight); // must be <= 1047
});
```

Then confirm against the PDF itself rather than trusting the measurement:

```bash
node -e "const b=require('fs').readFileSync('public/alex-mollard-cv.pdf').toString('latin1');
console.log(b.match(/\/Type\s*\/Pages[\s\S]{0,200}?\/Count\s+(\d+)/)[1]);"
```

`/Count 1` is the only acceptance criterion. Counting `/Type /Page` occurrences is less
reliable - use the `/Pages` `/Count`.

Overflowing? Shrink in this order: body `font-size` -> `line-height` -> `li`/`.job`
margins -> section heading size. Editing the multi-line CSS rules with line-anchored edits
clobbers neighbours easily; re-read the rule block after each edit.

## 5. Wire the CTA

- Resolve the href through the site's base-path helper, not a bare string, or it breaks
  under a base path: `const cvHref = withBase('/alex-mollard-cv.pdf', import.meta.env.BASE_URL)`.
- Put it in the hero action row **and** the footer links grid, with `download`.
- Verify over the built preview, not the dev server:
  `fetch('/alex-mollard-cv.pdf')` -> `200 application/pdf`.

## 6. Hand back honestly

State plainly that the PDF is a draft generated from their own content and that they
must read it before sending it anywhere. It carries their name; a hallucinated line costs
them an interview, not you.
