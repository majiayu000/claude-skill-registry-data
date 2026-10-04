---
name: web-vitals-budgets
description: Browser-measured Core Web Vitals (LCP/CLS/INP) budgets and measurement workflow for hero video, animated headers, and immersive media surfaces. Use when shipping or auditing any above-the-fold media change to skyyrose.co, and during launch audits — the browser half that wp-performance (backend-only) explicitly excludes. Do NOT use for backend TTFB root-causing, DB/query/cron/object-cache work (that is wp-performance), or for changes that cannot alter above-fold rendering.
---

# Web Vitals Budgets — Media-Heavy Surfaces

`wp-performance` explicitly opts out of browser measurement. This skill is the browser half: real
LCP/CLS numbers via Chrome DevTools MCP or Playwright, with budgets for the media patterns this
site actually ships.

## When to use

- An above-the-fold media change (hero video, animated header, image strip, lockup image) is about
  to ship or just shipped to skyyrose.co — measure before AND after.
- A launch audit needs LCP/CLS/INP numbers with element attribution.
- A CSS/JS change altered above-fold layout — CLS must be re-measured, not just visually QC'd.

**When NOT to use:**

- Backend slowness (TTFB, REST, admin, cron) → `wp-performance`. This skill only *attributes* TTFB
  inside the LCP breakdown; it does not fix it.
- Changes with no above-fold rendering impact (PHP-only logic, admin screens, email templates).
- Judging design quality — this skill produces milliseconds and shift scores, not taste.

## Inputs

**Absent input = STOP.** Numbers, not vibes — no browser tooling means no verdict.

1. **A reachable target URL** (production `https://skyyrose.co/...` or a preview). Probe it first
   (see Verification check 1); a non-200 or sub-50KB response means measure nothing yet.
2. **Chrome DevTools MCP or Playwright MCP available.** If neither is available this session, the
   LCP/CLS/INP checks are **SKIPs, not PASSes** — say so explicitly and name who closes them
   (the caller re-runs with browser tooling). Do not substitute a curl for a CLS number.
3. **The budgets table below** — a measurement without a budget to compare against is trivia.
4. **Logged-OUT context** — the WP admin-bar shifts everything 32px and corrupts CLS.

## Budgets (skyyrose.co, mobile 4G reference)

| Metric | Budget | Hard fail |
|---|---|---|
| LCP | ≤ 2.5s (excl. known TTFB debt ~2.3-3.4s — track separately, don't hide it) | > 4.0s |
| CLS | ≤ 0.05 | > 0.1 |
| INP | ≤ 200ms | > 500ms |
| Above-fold media weight | ≤ 1.5MB total | > 2.5MB |
| Header animated asset | ≤ 400KB | > 1MB |

## Procedure

1. **Baseline TTFB + reachability** with cache-busted curl (Verification check 1). Record whether
   the edge cache HIT or MISS — the `server-timing`/`x-ac` headers say which; a MISS number and a
   HIT number are different experiments and must not be compared.
2. **Chrome DevTools MCP**: `performance_start_trace` → navigate cold (cache disabled) →
   `performance_stop_trace` → `performance_analyze_insight` for the LCP breakdown (TTFB / load
   delay / load time / render delay). Mobile viewport 390×844 AND desktop 1440×900.
3. **Playwright fallback**: `browser_evaluate` → `new PerformanceObserver` for
   `largest-contentful-paint` + `layout-shift` entries; report element attribution for LCP (WHICH
   element — if the header video steals LCP candidacy from the hero, that's a regression even at
   the same ms).
4. **Three runs, report median.** One run = noise.
5. Before/after on the SAME network conditions — deploy comparisons across different cache states
   are invalid.
6. Report in the format: `LCP 2.31s (el: img.hero-lockup, ttfb 1.9s) | CLS 0.02 | INP 140ms |
   mobile, 3-run median, cold` — element attribution + conditions or the number doesn't count.

## Verification

A trace that errored or timed out is an artifact, not a green result — re-run it (bug-230). Each
check states its pass condition; each can fail.

```bash
curl -s -o /dev/null -w 'code=%{http_code} ttfb=%{time_starttransfer}s total=%{time_total}s size=%{size_download}B\n' \
  "https://skyyrose.co/?cb=$(date +%s)"
```
**PASS:** `code=200`, size ≥ 50000B. Record `ttfb` — it is the floor under LCP (LCP can never beat
TTFB + render). Observed 2026-07-28: `code=200 ttfb=1.888431s total=2.092811s size=136605B` on an
edge-cache MISS. `[live]`

```js
// Playwright browser_evaluate — run on the target page, logged out, mobile viewport
new Promise((resolve) => {
  let lcp = null, cls = 0;
  new PerformanceObserver((l) => { const e = l.getEntries().at(-1);
    lcp = { t: e.startTime, el: e.element?.tagName + '.' + (e.element?.className || '') };
  }).observe({ type: 'largest-contentful-paint', buffered: true });
  new PerformanceObserver((l) => { for (const e of l.getEntries())
    if (!e.hadRecentInput) cls += e.value;
  }).observe({ type: 'layout-shift', buffered: true });
  setTimeout(() => resolve({ lcp, cls: +cls.toFixed(4) }), 6000);
});
```
**PASS:** median of 3 runs → LCP ≤ 2.5s AND the attributed element is the intended hero (not the
nav video), AND CLS ≤ 0.05. Hard fail at LCP > 4.0s or CLS > 0.1 per the budgets table. `[live]`

```bash
curl -s -o /dev/null -w '%{size_download}\n' "https://skyyrose.co/<header-asset-path>?cb=$(date +%s)"
```
**PASS:** header animated asset ≤ 409600 bytes (400KB budget); above-fold media sum ≤ 1572864
bytes. `[live]`

Prove the CLS check can fail (rule 3): once per harness setup, strip `width`/`height` off the hero
`<img>` in a local copy and re-measure — CLS must go red — then restore. A CLS gate never observed
failing is a guess with a citation.

## Worked example

Real probe of production, 2026-07-28, from this repo:

```bash
curl -s -o /dev/null -w 'code=%{http_code} ttfb=%{time_starttransfer}s total=%{time_total}s size=%{size_download}B\n' \
  "https://skyyrose.co/?cb=$(date +%s)"
curl -sI "https://skyyrose.co/?cb=$(date +%s)" | grep -iE "^(HTTP|x-ac|server-timing)"
```

Observed output `[live]`:

```
code=200 ttfb=1.888431s total=2.092811s size=136605B
HTTP/2 200
x-ac: 1.sjc _atomic_bur MISS
server-timing: a8c-cdn, dc;desc=sjc, cache;desc=MISS;dur=2493.0
```

Reading it: the cache-busted request MISSed the WP.com edge (`cache;desc=MISS;dur=2493.0`), so
1.888s TTFB is the *origin* cost — consistent with the known ~2.3-3.4s TTFB debt band. Any LCP
measured on this cold path carries that debt; report it separately (`ttfb 1.9s` inside the LCP
line) instead of hiding it, and also measure the warm-cache path real visitors mostly hit. The
browser half (LCP element attribution, CLS) still requires the Playwright/DevTools run — this curl
alone is `[live]` evidence for TTFB and reachability ONLY, never for LCP/CLS (bug-287: evidence
scope must cover claim scope).

## Failure modes

- **CLS traps specific to this theme:**
  - `.min` rebuild changing rendered sizes: any CSS edit that alters above-fold layout re-measures
    CLS, not just visual QA (production serves `.min` — measure after `npm run build`).
  - WP admin-bar (logged-in) shifts everything 32px — measure logged-OUT.
  - Batcache/edge cache serves stale HTML referencing new CSS versions (or vice versa) during
    deploy windows — measure after cache settles or with cache-busted URL, and note which.
- **WebFetch on live HTML is banned** — it strips `<script>`, so anything script-injected (LCP
  candidates included) silently vanishes. Use `curl` with `?cb=$(date +%s)`.
- **Blank Playwright screenshots**: call `img.decode()` on hero images before screenshotting, or
  the capture races the decode and you QC an empty frame.
- **Header video stealing LCP candidacy** from the hero at "same ms" — always check the attributed
  element, not just the number. Small + `fetchpriority="low"` on nav media; `fetchpriority="high"`
  on the ONE intended LCP element.
- **Poster is the LCP candidate** for hero video — optimize it like a hero image (≤200KB),
  `preload="metadata"`, `autoplay muted loop playsinline`, explicit `width/height`.
- **Auto-scrolling strips**: `content-visibility: auto` off-screen, `transform`-only animation
  (compositor thread), `loading="lazy"` beyond first viewport, ≤100KB/image.
- **A dead trace read as green** (bug-230): DevTools trace that errors/timeouts has no findings
  *because it has no data* — re-run, never report it as passing.
- **Scope jump** (bug-287): a repo-side asset diff is not a live vitals claim — "regressed LCP"
  requires the `[live]` probe.
