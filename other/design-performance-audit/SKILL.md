---
type: Skill
name: design-performance-audit
description: Analyze GTmetrix (and PageSpeed) reports for WordPress sites and produce a prioritized optimization plan, a custom WPCode-ready PHP optimization snippet, and a self-contained HTML summary report. Covers PDF report extraction with pypdf, live-page cross-referencing, WordPress-specific fix mapping (Elementor, WooCommerce, Breeze, reCAPTCHA, Google-tag duplication, WebP conversion), and staging-test discipline. Use when asked to review GTmetrix reports, optimize page speed or Core Web Vitals, create a custom performance optimization snippet, or produce an optimization report for a WordPress site.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# WordPress Performance Audit (GTmetrix)

End-to-end workflow for turning a GTmetrix report (plus a captured copy of the
live page) into a prioritized fix list, a site-specific WPCode-ready PHP
optimization snippet, and a shareable HTML report. Works for any WordPress
site; the fix mapping in `references/common-fixes.md` is the core knowledge
base.

## When to use

Trigger when the user asks to:

- Review GTmetrix / PageSpeed / Lighthouse reports for a WordPress site
- Optimize page speed, Core Web Vitals (LCP / CLS / TBT), or page weight
- Create a custom optimization snippet for a WordPress site
- Produce an optimization report ("what's done / what's left") from an audit

## Inputs you need

| Input | Where | Notes |
|---|---|---|
| GTmetrix PDF(s) | Project folder (e.g. `projects/<site>/`) | Full + summary PDFs of the SAME run share a run ID/timestamp — they are one report, not two. A before/after comparison needs two different runs. |
| Page HTML capture | `projects/<site>/<page>.html` (view-source) | Grep it to confirm what the report flags (script tags, img attributes, inline styles). If missing, `fetch` the live URL — the HTML won't be identical to the cached run but is usually close enough. |
| Existing site code | `projects/<site>/functions.php`, snippet files | Shows what's already been optimized; avoids recommending things already done. |

## Step 1 — Extract the report(s)

Use Python + `pypdf` from the site's project folder:

```bash
python -c "import pypdf" 2>/dev/null || pip install pypdf
```

```python
import pypdf
r = pypdf.PdfReader('GTmetrix-report-<site>-<id>-full.pdf')
for i, p in enumerate(r.pages):
    print(f'--- PAGE {i+1} ---')
    print(p.extract_text())
```

Extract and note:

1. **Scores & metrics** — Performance/Structure %, LCP, TBT, CLS, TTFB, Fully
   Loaded, total size, request count.
2. **Top Issues** — the impact-ranked list on page 1.
3. **Waterfall / third-party tables** — total bytes per third-party
   (GTM, Yotpo, gstatic/reCAPTCHA, fonts), plus `(canceled)` entries.
4. **Every audit table** — payload URLs with transfer sizes, LCP element,
   CLS shift elements, cache-policy URLs, @import chains, render-blocking
   list, unused JS/CSS totals, image-size savings.

Key reading: the LCP breakdown (TTFB / Load Delay / Load Time / Render Delay)
tells you whether lazy-loading, server time, or render work is the LCP cost.

## Step 2 — Cross-reference the live page

Grep the saved HTML capture for the flagged items to locate the SOURCE (this
is what turns "the report says X" into "fix Y in Z"):

- `recaptcha` → which form/popup, which widget handle enqueues it
- `gtag|gtm|local_ga` → how many analytics paths are active, who loads what
- `jquery.com|code.jquery` → hardcoded CDN scripts vs WP core handles
- `@import|fonts.googleapis` → which plugin stylesheet imports fonts
- the LCP `<img>` → check `loading="lazy"` and the srcset/sizes
- `elementor-invisible|_animation` → entrance animations causing CLS
- `@font-face|font-display` → font loading strategy

## Step 3 — Review existing site code

Read the project's `functions.php` / snippet files to inventory what's already
deployed (caching, lazy-load, schema, custom handlers). Also look for
anti-patterns in the deployable source itself, e.g. `rand()`/`time()` cache
busting (kills browser/CDN caching — fix with `filemtime()`).

## Step 4 — Map audits to fixes

Use `references/common-fixes.md` — it maps each GTmetrix audit to concrete
WordPress/Elementor/WooCommerce/Breeze fixes with handle names, filter names,
and risk levels. Only include fixes that match this site's actual findings.

## Step 5 — Produce the prioritized action list

In the final message, present a table ordered by impact:

| Priority | Action | Est. benefit | Where |

- **High** = large bytes off the wire or LCP/CLS blockers (reCAPTCHA,
  duplicate analytics, PNG→WebP, eager LCP image).
- **Medium** = duplicate libs, CLS details, plugin CSS off-loading, cache fixes.
- **Low** = polish (minify, srcset gaps, preconnect, font woff2).

Separate **done/in place** from **still to do**. State estimated savings in KB
or ms, and always name WHERE the change is made (widget setting, Breeze
setting, WPCode, child theme file).

## Step 6 — Generate the custom optimization snippet

Create `<site>/performance-optimizations.php` from
`templates/optimization-snippet.php`:

- **Only include blocks that match the site's findings** — no copy-paste of
  irrelevant blocks.
- Safe blocks (preconnect, font-display swap, CLS CSS) stay enabled.
- Risky blocks (script dequeues, reCAPTCHA lazy-load, conditional asset
  removal) stay commented with an explicit "test on staging" warning.
- Keep the repo conventions: `defined( 'ABSPATH' ) || exit;` guard, one file
  per feature, escaped output, deploy notes (WPCode → Auto Insert → Run
  Everywhere).
- If the site's deployable `functions.php` has fixable bugs (e.g. cache
  busting), fix them there directly.

## Step 7 — Generate the HTML report

Create `<site>/<site>-optimization-report.html` from
`templates/report.html`. Fill the `{{PLACEHOLDERS}}`, keep it self-contained
(no external assets, print-friendly), then validate:

```bash
python -c "
from html.parser import HTMLParser
VOID={'meta','link','br','hr','img','input'}
class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack=[]; self.errors=[]
    def handle_starttag(self, tag, attrs):
        if tag not in VOID: self.stack.append(tag)
    def handle_startendtag(self, tag, attrs):
        if tag not in VOID: self.errors.append(f'self-closing non-void <{tag}>')
    def handle_endtag(self, tag):
        if not self.stack: self.errors.append(f'unmatched </{tag}>'); return
        if self.stack[-1]==tag: self.stack.pop()
        else: self.errors.append(f'mismatch </{self.stack[-1]}> vs </{tag}>')
p=P(); p.feed(open('<file>.html', encoding='utf-8').read())
print('errors:', p.errors or 'none'); print('unclosed:', p.stack or 'none')
"
```

(Note: self-closing void tags like `<meta … />` fire `handle_startendtag` —
override it or the parser reports false mismatches on them.)

## Step 8 — Verify after deployment (the "check again" pass)

After the user enables the snippet, re-inspect the LIVE page to confirm the
changes actually landed and measure the delta. `fetch` is NOT suitable here —
it returns Markdown and strips the `<link>`/`<img>` attributes you need. Use
the browser instead:

1. `browser_navigate` to the URL, then `browser_evaluate` to read the DOM:
   - Confirm preconnect hints: `[...document.querySelectorAll('link[rel=preconnect],link[rel=dns-prefetch]')].map(l => l.href)`
   - Confirm the LCP hero lost its lazy attribute: find the hero `img` and
     read `img.getAttribute('loading')` (should be `null`/absent; also check
     the `class` for a theme lazy-load marker like Flatsome's
     `lazy-load-active`).
   - Count `img[data-src]` / `img[loading=lazy]` vs `img[loading=eager]` to
     see the lazy-load surface.
2. Read **navigation + resource timings** for a head-to-head against the
   report: `performance.getEntriesByType('navigation')[0]` (TTFB,
   domContentLoaded, loadEvent) and `performance.getEntriesByType('resource')`
   to find the hero's `responseEnd` and `transferSize`.
3. **Warm-cache caveat (important):** a browser session that already loaded
   the page will report the hero's `transferSize: 0` (served from cache) and
   a deceptively low LCP. State this plainly — the structural fix (e.g.
   `loading` removed) is still verifiable, but for a real number you must
   re-run GTmetrix cold and archive the new PDF to diff before/after.
4. Check the console for NEW errors introduced by the snippet (e.g. a
   dequeue that broke a script): `browser_console_messages` with
   `level="error"`.

Also confirm whether the changes are truly live vs. cached (a page-cache/CDN
may serve a stale copy; hard-reload or purge cache before concluding "not
working").

## Rules & discipline

- **One report ≠ two reports.** Two PDFs with the same run ID/timestamp are
  the full + summary of one run. Say so if the user believes there are two.
- **Never deploy risky changes to production.** Anything that dequeues
  scripts, lazy-loads reCAPTCHA, or conditionally removes plugin assets must
  be tested on staging first (forms, popups, menus, icons, submit flows).
- **Never edit files inside containers** on this stack — edit host paths.
- **Archive the next GTmetrix PDF** into the project folder after deployment
  so the next review can diff before/after.
- **State what you could not verify** (e.g. which plugin enqueues a script
  without wp-admin access) and give the diagnostic steps instead of guessing.
