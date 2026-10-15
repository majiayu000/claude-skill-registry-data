---
name: performance-pass
description: Measure and fix how fast a site loads and responds on a mid-range phone - LCP, CLS, total blocking time, bytes by type, oversized images, font weight - with a Playwright script that throttles CPU and network, then fix the causes in order of impact and re-measure. Covers animated canvases and WebGL backgrounds, which must pause offscreen and fall back on weak devices. Use before launch, when a page feels slow on a phone, or after adding heavy visuals.
---

# /performance-pass

A page is fast when the thing you came for appears quickly, stays where it is, and responds when you touch it. Measure those three things on a phone-class device, fix the biggest cause, and measure again.

| Metric | What it answers | Good | Needs work |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | When did the main content appear? | ≤ 2.5 s | ≤ 4 s |
| **CLS** (Cumulative Layout Shift) | Did things jump while I was reading? | ≤ 0.1 | ≤ 0.25 |
| **TBT** (Total Blocking Time) | Was the page frozen while loading? (Stands in for INP in a lab.) | ≤ 200 ms | ≤ 600 ms |

## 1. Measure a production build

Development servers ship unminified code and inflate every number, so build and serve the site first:

```
npm run build && npm run start
```

Save this as `perf.mjs` in a scratch directory (it needs `playwright`) and run it:

```
node perf.mjs http://localhost:3000 / /pricing /blog/some-post
```

Each page is loaded as a 390px-wide phone at 2x density, with the CPU slowed 4x and a fast-4G network. The script scrolls through the page once, then reports:

- LCP and its element, CLS and TBT
- transfer size by type, and the five heaviest requests
- the font faces loaded
- images served much larger than they're shown, or without dimensions

```js
// Performance pass: loads each page as a mid-range phone on a fast 4G connection (4x CPU slowdown,
// throttled network) and reports LCP, CLS, total blocking time, bytes by type, the heaviest
// requests, and images that are much larger than they're displayed. Measure a production build.
import { chromium } from "playwright";

const [base, ...paths] = process.argv.slice(2);
if (!base || !paths.length) {
  console.error("usage: node perf.mjs <base-url> <path> [path…]");
  process.exit(1);
}
const kb = (b) => `${Math.round(b / 1024)} KB`;
const browser = await chromium.launch();

for (const p of paths) {
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  const page = await ctx.newPage();
  const cdp = await ctx.newCDPSession(page);
  await cdp.send("Network.enable");
  await cdp.send("Network.emulateNetworkConditions", { offline: false, latency: 150, downloadThroughput: (9 * 1024 * 1024) / 8, uploadThroughput: (1.5 * 1024 * 1024) / 8 });
  await cdp.send("Emulation.setCPUThrottlingRate", { rate: 4 });

  const sizes = new Map();
  cdp.on("Network.responseReceived", (e) => sizes.set(e.requestId, { url: e.response.url, type: e.type, bytes: 0 }));
  cdp.on("Network.loadingFinished", (e) => {
    const r = sizes.get(e.requestId);
    if (r) r.bytes = e.encodedDataLength;
  });

  await page.addInitScript(() => {
    window.__perf = { lcp: 0, lcpEl: "", cls: 0, tbt: 0, longTasks: 0 };
    new PerformanceObserver((l) => {
      for (const e of l.getEntries()) {
        window.__perf.lcp = e.startTime;
        const el = e.element;
        window.__perf.lcpEl = el ? el.tagName.toLowerCase() + (el.className && typeof el.className === "string" ? "." + el.className.trim().split(/\s+/)[0] : "") : e.url || "";
      }
    }).observe({ type: "largest-contentful-paint", buffered: true });
    new PerformanceObserver((l) => {
      for (const e of l.getEntries()) if (!e.hadRecentInput) window.__perf.cls += e.value;
    }).observe({ type: "layout-shift", buffered: true });
    new PerformanceObserver((l) => {
      for (const e of l.getEntries()) {
        window.__perf.longTasks++;
        window.__perf.tbt += Math.max(0, e.duration - 50);
      }
    }).observe({ type: "longtask", buffered: true });
  });

  const t0 = Date.now();
  await page.goto(base + p, { waitUntil: "load", timeout: 120000 });
  const loadMs = Date.now() - t0;
  await page.waitForTimeout(3000);
  // Scroll through once so lazy content and late layout shifts are counted.
  await page.evaluate(async () => {
    for (let y = 0; y < document.body.scrollHeight; y += innerHeight * 0.8) {
      scrollTo(0, y);
      await new Promise((r) => setTimeout(r, 250));
    }
    scrollTo(0, 0);
  });
  await page.waitForTimeout(1000);

  const perf = await page.evaluate(() => window.__perf);
  const images = await page.evaluate(() =>
    [...document.images]
      .filter((i) => i.complete && i.naturalWidth && i.getBoundingClientRect().width)
      .map((i) => ({ src: i.currentSrc.split("/").pop().slice(0, 50), natural: i.naturalWidth, shown: Math.round(i.getBoundingClientRect().width * devicePixelRatio), lazy: i.loading === "lazy", sized: i.hasAttribute("width") && i.hasAttribute("height") }))
      .filter((i) => i.natural > i.shown * 1.5 || !i.sized),
  );
  const fonts = await page.evaluate(() => [...document.fonts].filter((f) => f.status === "loaded" && !/fallback/i.test(f.family)).map((f) => `${f.family} ${f.weight}`));

  const all = [...sizes.values()];
  const byType = {};
  for (const r of all) byType[r.type] = (byType[r.type] ?? 0) + r.bytes;
  const total = all.reduce((s, r) => s + r.bytes, 0);

  const flag = (ok, warn) => (ok ? "ok" : warn ? "needs work" : "poor");
  console.log(`\n# ${p}  (load event ${loadMs} ms, throttled)`);
  console.log(`LCP  ${Math.round(perf.lcp)} ms  ${flag(perf.lcp <= 2500, perf.lcp <= 4000)}  · element: ${perf.lcpEl}`);
  console.log(`CLS  ${perf.cls.toFixed(3)}  ${flag(perf.cls <= 0.1, perf.cls <= 0.25)}`);
  console.log(`TBT  ${Math.round(perf.tbt)} ms over ${perf.longTasks} long tasks  ${flag(perf.tbt <= 200, perf.tbt <= 600)}`);
  console.log(`Transfer  ${kb(total)} in ${all.length} requests · ${Object.entries(byType).sort((a, b) => b[1] - a[1]).map(([t, b]) => `${t} ${kb(b)}`).join(" · ")}`);
  console.log(`Heaviest:`);
  for (const r of all.sort((a, b) => b.bytes - a.bytes).slice(0, 5)) console.log(`  ${kb(r.bytes).padStart(8)}  ${r.type.padEnd(10)} ${r.url.replace(base, "").slice(0, 90)}`);
  console.log(`Fonts loaded: ${fonts.length}${fonts.length > 6 ? " (more than six faces: subset or drop weights)" : ""} · ${[...new Set(fonts)].join(", ")}`);
  for (const i of images) console.log(`  image ${i.src}: ${i.natural}px wide, shown at ${i.shown}px${i.natural > i.shown * 1.5 ? " (serve a smaller size)" : ""}${i.sized ? "" : " (no width/height: may shift layout)"}`);
  await ctx.close();
}
await browser.close();
```

Run it three times. Lab numbers vary, so use the median.

## 2. Find the cause

Work on the worst metric first.

**Slow LCP**

- **Is the LCP element an image?**
  - Serve it at its displayed size, in AVIF or WebP.
  - Don't lazy-load it; give it `fetchpriority="high"`, or `priority` in `next/image`.
  - Preload it if it's a CSS background.
- **Is it text?** Then it's waiting on fonts or JavaScript.
  - Use `font-display: swap` with a metric-matched fallback (`next/font` does this).
  - Preload only the one or two faces above the fold.
  - Make sure the text is in the server HTML, not rendered after hydration.
- **Is the document itself slow?** Check server time, and whether the page could be static.

**Layout shift**

- Give images, videos, iframes and embeds `width` and `height`, or an `aspect-ratio`.
- Reserve space for anything that loads late: banners, ads, consent bars, async components. Use a placeholder the size of the real content (see the Progressive Reveal pattern: placeholders that are typographically true).
- Fonts swapping in with different metrics cause shifts too. Match the fallback's size-adjust and ascent.

**Blocking time**

- Find what runs. In Chrome DevTools, open Performance with 4x CPU throttling and record a load; the long tasks show which script.
- **Ship less JavaScript.** Look for heavy libraries used for one function, components that don't need to be client components, and code for below-the-fold features.
- **Split and defer.** Dynamically import heavy widgets (editors, charts, maps, 3D) when they're needed or scrolled near. Load third-party scripts after the page is interactive.
- **Hydrate less.** Server-render static sections, and keep interactive islands small.

**Heavy visuals** (canvas, WebGL, video backgrounds, big animations). These are common on distinctive sites, so check each one:

- Does it **pause offscreen** (IntersectionObserver) and when the tab is hidden?
- Does it render at a **reduced resolution** (for example 0.5–0.6 of the device pixel ratio for soft fields) and cap its frame rate on phones?
- Is there a **still fallback** for reduced motion, low-power devices (`navigator.hardwareConcurrency <= 4`, `navigator.connection.saveData`) and no WebGL: a CSS gradient or a poster image in the same palette?
- Is it created **after** the main content paints, never blocking it?
- Is it cleaned up on unmount, including the WebGL context?

**Weight**

- **Fonts:** at most four to six faces on a page; subset to the scripts you use; variable fonts only when you use the range.
- **Images:** anything over about 200 KB on a phone deserves a second look.
- **CSS:** unused CSS from a framework or old pages.

## 3. Fix and re-measure

Fix one cause at a time and re-run the script after each fix, so you know what each change was worth. Stop when all three metrics are in the good range on every page that matters, or when the next fix would cost the design something the user cares about. If so, say so and let them choose.

## Report

For each page, give:

- the before and after numbers
- what caused each problem
- the fix, with file and line
- what's still slow, why it stays, and what it would take

Keep claims to what you measured. "LCP 3.9 s → 1.8 s on /pricing, by serving the hero at 780px as AVIF with high priority" is a result; "improved performance" is not.
