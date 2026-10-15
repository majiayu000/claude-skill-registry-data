---
name: responsive-audit
description: Audit a web interface at phone, tablet and desktop widths with Playwright, measure what's broken (horizontal overflow, small touch targets, tiny text, console errors), make a contact sheet to review by eye, fix, and re-run until clean. Use when the user asks to check or fix mobile, responsive or "looks wrong on my phone" issues.
---

# /responsive-audit

Measure first, then look, then fix. Numbers catch overflow you can't see; your eyes catch layouts that are technically fine and still wrong.

## 1. Set up

- The app must be running locally (for example `npm run dev`). Find its URL and the pages to check: every route, or the pages the user named.
- Playwright must be available: `npm i -D playwright && npx playwright install chromium` if it isn't.
- Work in a scratch directory, not in the project.

## 2. Run the measurement

Save this as `audit.mjs` in the scratch directory and run it:

```
node audit.mjs <base-url> <out-dir> <path> [path…]
```

For example `node audit.mjs http://localhost:3000 ./audit / /pricing /about`.

```js
// Responsive audit: measures each page at three widths, saves a screenshot per page and width,
// writes report.json, and builds sheet.html (a contact sheet) to review by eye.
import { chromium } from "playwright";
import fs from "node:fs";
import path from "node:path";

const [base, out, ...paths] = process.argv.slice(2);
if (!base || !out || !paths.length) {
  console.error("usage: node audit.mjs <base-url> <out-dir> <path> [path…]");
  process.exit(1);
}
const WIDTHS = [
  { name: "phone", width: 375, height: 812, mobile: true },
  { name: "tablet", width: 768, height: 1024, mobile: true },
  { name: "desktop", width: 1280, height: 800, mobile: false },
];
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch();
const report = [];

for (const p of paths) {
  for (const w of WIDTHS) {
    const ctx = await browser.newContext({ viewport: { width: w.width, height: w.height }, isMobile: w.mobile, hasTouch: w.mobile });
    const page = await ctx.newPage();
    const errors = [];
    page.on("console", (m) => m.type() === "error" && errors.push(m.text().slice(0, 200)));
    page.on("pageerror", (e) => errors.push(String(e).slice(0, 200)));
    await page.goto(new URL(p, base).href, { waitUntil: "load", timeout: 60000 });
    await page.waitForTimeout(1200);
    const m = await page.evaluate(() => {
      const W = innerWidth;
      const visible = (el) => {
        const s = getComputedStyle(el);
        return s.visibility !== "hidden" && s.display !== "none" && Number(s.opacity) > 0.05;
      };
      // Covered by something else (an overlay, a sticky bar)? Then it isn't what the user sees.
      const onTop = (el) => {
        const r = el.getBoundingClientRect();
        const x = r.left + r.width / 2;
        const y = r.top + r.height / 2;
        if (x < 0 || y < 0 || x > innerWidth || y > innerHeight) return true;
        const hit = document.elementFromPoint(x, y);
        return !hit || hit === el || el.contains(hit) || hit.contains(el);
      };
      // An element past the right edge only matters if no ancestor clips it.
      const clipped = (el) => {
        for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) {
          const s = getComputedStyle(a);
          if (s.overflowX !== "visible" || s.clipPath !== "none") {
            const r = a.getBoundingClientRect();
            if (r.right <= W + 2 && r.left >= -2) return true;
          }
        }
        return false;
      };
      const label = (el) => `${el.tagName.toLowerCase()}${el.id ? "#" + el.id : ""}${typeof el.className === "string" && el.className ? "." + el.className.split(" ")[0] : ""}`;
      const overflow = [];
      for (const el of document.body.querySelectorAll("*")) {
        const r = el.getBoundingClientRect();
        if (!r.width || !r.height) continue;
        if ((r.right > W + 2 || r.left < -2) && visible(el) && !clipped(el)) {
          overflow.push(`${label(el)} spans ${Math.round(r.left)}→${Math.round(r.right)}px`);
          if (overflow.length >= 5) break;
        }
      }
      const small = [];
      for (const el of document.querySelectorAll("a[href],button,input:not([type=hidden]),select,textarea,[role=button],[role=tab],[role=checkbox],[role=radio],[role=switch],[role=slider],[role=option]")) {
        const r = el.getBoundingClientRect();
        // Screen-reader-only elements (1px boxes) aren't targets anyone taps.
        if (r.width <= 2 || r.height <= 2 || !visible(el) || !onTop(el)) continue;
        if (r.width < 24 || r.height < 24) small.push(`${(el.getAttribute("aria-label") || el.textContent || label(el)).trim().slice(0, 30)} (${Math.round(r.width)}×${Math.round(r.height)})`);
      }
      const tiny = [];
      for (const el of document.body.querySelectorAll("*")) {
        if (![...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) continue;
        const box = el.getBoundingClientRect();
        if (box.width <= 2 || !visible(el) || !onTop(el)) continue;
        const size = parseFloat(getComputedStyle(el).fontSize);
        if (size < 10.5) tiny.push(`"${el.textContent.trim().slice(0, 24)}" at ${size}px`);
      }
      return { scrollWidth: document.documentElement.scrollWidth, width: W, overflow, small, tiny };
    });
    const file = `${p.replace(/[^a-z0-9]+/gi, "_") || "home"}-${w.name}.png`;
    await page.screenshot({ path: path.join(out, file) });
    report.push({ path: p, viewport: w.name, file, errors, ...m, horizontalScroll: m.scrollWidth > m.width + 1 });
    await ctx.close();
  }
}
await browser.close();

fs.writeFileSync(path.join(out, "report.json"), JSON.stringify(report, null, 2));
const cells = report.map((r) => `<figure><img src="${r.file}"><figcaption>${r.path} · ${r.viewport}${r.horizontalScroll || r.overflow.length ? " · OVERFLOW" : ""}</figcaption></figure>`).join("");
fs.writeFileSync(path.join(out, "sheet.html"), `<!doctype html><meta charset="utf-8"><style>body{margin:0;padding:16px;background:#111;color:#ddd;font:12px system-ui;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}figure{margin:0}img{width:100%;border:1px solid #333}</style>${cells}`);

for (const r of report) {
  const issues = [];
  if (r.horizontalScroll || r.overflow.length) issues.push(`overflow: ${r.overflow.join("; ") || `page is ${r.scrollWidth}px wide`}`);
  if (r.small.length) issues.push(`${r.small.length} small targets: ${r.small.slice(0, 4).join(", ")}`);
  if (r.tiny.length) issues.push(`${r.tiny.length} tiny text: ${r.tiny.slice(0, 3).join(", ")}`);
  if (r.errors.length) issues.push(`console: ${r.errors[0]}`);
  console.log(`${r.path} [${r.viewport}] ${issues.length ? issues.join(" | ") : "ok"}`);
}
console.log(`\nReport: ${path.join(out, "report.json")}  Contact sheet: ${path.join(out, "sheet.html")}`);
```

## 3. Look

Open `sheet.html` in a browser, or screenshot it with Playwright if you can't open files, and review every cell. The script can't see these, so look for them:

- A desktop layout squeezed into a phone: side-by-side columns, a sidebar taking most of the width.
- Text overlapping other text, or controls covering content (arrows over cards, sticky bars over headings).
- Content cut off at the bottom of a fixed-height box with no way to scroll to it.
- Huge empty areas, or everything crammed into the top third.
- Tablet: the awkward middle, where desktop grids are too narrow and phone stacks are too wide.

## 4. Judge what the numbers mean

- **Overflow** (the page scrolls sideways, or an element pokes out) is always a bug. Fix it at its cause: a fixed width, a `nowrap`, a long word or URL, a grid without `minmax(0, 1fr)`, a transform or scale that grows past its box. Don't hide it with `overflow-x: hidden` on the body.
- **Small targets** under 24×24px fail WCAG 2.5.8 unless there's spacing around them or an equivalent larger control. On touch, grow the hit area (padding, or an `::after` with negative inset) rather than the visual.
- **Tiny text** under 10.5px: fine for deliberate uppercase mono labels with wide tracking; not fine for anything a person has to read.
- **Console errors**: fix them all; hydration and key warnings often come from layout code.

## 5. Fix, then re-run

- Prefer the component's own container width (container queries, `%`, `min()`) over new viewport breakpoints, so the component works wherever it's placed.
- If a preview or demo renders components inline inside a narrower box, remember `@media` still sees the window. Test in a real viewport, or render the demo in an iframe.
- Re-run the script after the fixes. Finish only when overflow and console errors are at zero and every cell of the contact sheet looks deliberate.

## 6. Report

List what failed, what you changed per page, and anything you left alone on purpose (and why).
