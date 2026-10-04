---
name: seo-lighthouse-audit
description: >
  Run a Lighthouse audit against any URL via the local Lighthouse CLI or the
  PageSpeed Insights API fallback, parse category scores and failed audits,
  and map every failed audit ID to its official Chrome docs page plus a
  one-line fix. Use when user says "lighthouse", "lighthouse audit",
  "run lighthouse", "lighthouse score", or "pagespeed".
allowed-tools:
  - Read
  - Bash
  - WebFetch
  - Write
---

# Lighthouse Audit & Fix Mapping
<!-- Updated: 2026-06-10 -->

Lighthouse is Google's open-source page quality tool. It runs a series of audits
against a URL and scores four categories: Performance, Accessibility, Best
Practices, and SEO. Reference: https://developer.chrome.com/docs/lighthouse/overview

**Scope notes (keep the report honest):**
- **PWA category was removed in Lighthouse v12 (2024).** Do NOT score or report a PWA category. If the user asks for it, explain it no longer exists.
- **Lighthouse is lab data** — a single synthetic run on emulated hardware/network. Always recommend validating against CrUX field data (75th percentile of real users) before treating a score as ground truth. Delegate field-data analysis to the `seo-core-web-vitals` skill.
- **Agentic Browsing** is a new experimental category (llms.txt, WebMCP tools, accessibility-for-agents). It is informational only — it reports a pass ratio, not a 0-100 score. See https://developer.chrome.com/docs/lighthouse/agentic-browsing/scoring

## Inputs

| Input | Required | Default |
|-------|----------|---------|
| URL to audit | Yes | — |
| Strategy (mobile/desktop) | No | mobile |
| Categories | No | performance, seo, best-practices, accessibility |

## Execution

1. **Detect a local Lighthouse CLI:**
   ```bash
   npx lighthouse --version 2>/dev/null || which lighthouse
   ```
   Requires Chrome installed locally. If either succeeds, prefer the CLI path (step 2); otherwise fall back to the PageSpeed Insights API (step 3).

2. **CLI path** — run headless and write JSON to a temp file:
   ```bash
   npx lighthouse <url> --output=json \
     --output-path=/tmp/lh-report.json \
     --chrome-flags="--headless" --quiet
   ```
   For desktop strategy add `--preset=desktop`.

3. **API fallback** — PageSpeed Insights v5 (no API key needed for light use; add `&key=` if one is configured):
   ```bash
   curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=<url>&category=performance&category=seo&category=best-practices&category=accessibility&strategy=mobile" -o /tmp/psi.json
   ```
   The Lighthouse result lives under `.lighthouseResult`. Docs: https://developers.google.com/speed/docs/insights/v5/get-started
   Bonus: the same response embeds CrUX field data under `loadingExperience` — surface it as a lab-vs-field sanity check.

4. **Parse the JSON:**
   - Category scores: `.categories[].score` (multiply by 100).
   - Failed audits: every entry in `.audits` with `score < 0.9` and a non-informative `scoreDisplayMode` (`binary` or `numeric`). Capture `id`, `title`, `displayValue`, and `details.overallSavingsMs` / `overallSavingsBytes` where present.
   - Key lab metrics: `largest-contentful-paint`, `total-blocking-time`, `cumulative-layout-shift`, `first-contentful-paint`, `speed-index`. Performance scoring weights: https://developer.chrome.com/docs/lighthouse/performance/performance-scoring

5. **Map each failed audit to its docs page and a fix.** Docs URL pattern:
   ```
   https://developer.chrome.com/docs/lighthouse/<category>/<audit-id>
   ```
   where `<category>` is `performance`, `seo`, `best-practices`, or `accessibility`. Use the reference table below for the highest-impact audits; for others, construct the URL from the pattern and write a one-line fix from the audit's own `description` field.

6. **Prioritize**: sort performance audits by estimated savings (ms/bytes), then list SEO and best-practices failures (these are usually binary pass/fail and cheap to fix).

## High-Impact Audit Reference

### Performance

| Audit ID | One-line fix | Docs |
|----------|--------------|------|
| `render-blocking-resources` | Inline critical CSS, defer non-critical CSS/JS | [docs](https://developer.chrome.com/docs/lighthouse/performance/render-blocking-resources) |
| `unused-javascript` | Code-split and lazy-load unused bundles | [docs](https://developer.chrome.com/docs/lighthouse/performance/unused-javascript) |
| `uses-responsive-images` | Serve appropriately sized images via `srcset`/`sizes` | [docs](https://developer.chrome.com/docs/lighthouse/performance/uses-responsive-images) |
| `total-byte-weight` | Reduce total payload below ~1.6 MB (compress, trim, lazy-load) | [docs](https://developer.chrome.com/docs/lighthouse/performance/total-byte-weight) |
| `bf-cache` | Remove `unload` handlers and `no-store` headers blocking back/forward cache | [docs](https://developer.chrome.com/docs/lighthouse/performance/bf-cache) |
| `largest-contentful-paint` | Preload the LCP resource, add `fetchpriority="high"` | [docs](https://developer.chrome.com/docs/lighthouse/performance/lighthouse-largest-contentful-paint) |
| `total-blocking-time` | Break up long main-thread tasks, defer third-party JS | [docs](https://developer.chrome.com/docs/lighthouse/performance/lighthouse-total-blocking-time) |
| `dom-size` | Keep DOM under ~1,500 nodes; virtualize long lists | [docs](https://developer.chrome.com/docs/lighthouse/performance/dom-size) |
| `third-party-summary` | Lazy-load or facade heavy third-party embeds | [docs](https://developer.chrome.com/docs/lighthouse/performance/third-party-summary) |
| `font-display` | Use `font-display: swap` to avoid invisible text | [docs](https://developer.chrome.com/docs/lighthouse/performance/font-display) |

Other frequent flags: `unused-css-rules`, `unminified-javascript`, `unminified-css`, `uses-text-compression`, `uses-long-cache-ttl`, `uses-optimized-images`, `offscreen-images`, `server-response-time`, `redirects`, `uses-rel-preconnect`, `mainthread-work-breakdown`, `bootup-time`, `non-composited-animations` — same URL pattern.

### SEO

| Audit ID | One-line fix | Docs |
|----------|--------------|------|
| `is-crawlable` | Remove blocking `noindex` / robots.txt rules on indexable pages | [docs](https://developer.chrome.com/docs/lighthouse/seo/is-crawlable) |
| `meta-description` | Add a unique, descriptive meta description | [docs](https://developer.chrome.com/docs/lighthouse/seo/meta-description) |
| `canonical` | Add a single valid, absolute canonical URL | [docs](https://developer.chrome.com/docs/lighthouse/seo/canonical) |
| `hreflang` | Fix hreflang codes and ensure reciprocal links | [docs](https://developer.chrome.com/docs/lighthouse/seo/hreflang) |
| `http-status-code` | Return 200 for indexable pages, not 4xx/5xx | [docs](https://developer.chrome.com/docs/lighthouse/seo/http-status-code) |
| `link-text` | Replace "click here" with descriptive anchor text | [docs](https://developer.chrome.com/docs/lighthouse/seo/link-text) |

Also check: `font-size` (legible ≥12px text), `tap-targets` (48x48px touch targets), `invalid-robots-txt`, `structured-data` (manual).

### Best Practices

| Audit ID | One-line fix | Docs |
|----------|--------------|------|
| `viewport` | Add `<meta name="viewport" content="width=device-width, initial-scale=1">` | [docs](https://developer.chrome.com/docs/lighthouse/best-practices/viewport) |
| `csp-xss` | Add a strict Content-Security-Policy against XSS | [docs](https://developer.chrome.com/docs/lighthouse/best-practices/csp-xss) |
| `has-hsts` | Send a `Strict-Transport-Security` header | [docs](https://developer.chrome.com/docs/lighthouse/best-practices/has-hsts) |

Also frequent: `is-on-https`, `errors-in-console`, `no-vulnerable-libraries`, `image-aspect-ratio`, `uses-http2`, `deprecations`, `charset`, `doctype`, `external-anchors-use-rel-noopener`, `clickjacking-mitigation` — same URL pattern.

### Agentic Browsing (informational — do not score)

Experimental audits for AI-agent readiness: `llms-txt` (machine-readable site summary at `/llms.txt` — N/A if 404, flagged only on server error; see [docs](https://developer.chrome.com/docs/lighthouse/agentic-browsing/llms-txt)), WebMCP tool registration and schema validity, accessibility-for-agents, layout stability for agents. Report pass ratio only and cross-reference the `seo-llms-txt` and `seo-robots-ai` skills.

## Output

```
# Lighthouse Audit: <url> (mobile|desktop, lab data)

## Category Scores
| Category | Score |
|----------|-------|
| Performance | XX/100 |
| Accessibility | XX/100 |
| Best Practices | XX/100 |
| SEO | XX/100 |

## Key Lab Metrics
| Metric | Value | Rating |
|--------|-------|--------|
| LCP | X.Xs | ✅/⚠️/❌ |
| TBT | XXXms | ✅/⚠️/❌ |
| CLS | 0.XX | ✅/⚠️/❌ |
| FCP / Speed Index | ... | ... |

## Failed Audits → Fixes (sorted by estimated savings)
| # | Audit | Category | Est. Savings | Fix | Docs |
|---|-------|----------|--------------|-----|------|
| 1 | render-blocking-resources | Performance | 1,200 ms | Inline critical CSS, defer the rest | link |
| ... | | | | | |

## Field vs Lab (if PSI response included loadingExperience)
Note agreement/divergence between lab metrics and CrUX field data.

## Caveats
- Lab data from a single emulated run — validate with CrUX field data
  (see seo-core-web-vitals skill) before declaring CWV pass/fail.
- PWA category removed in Lighthouse v12; Agentic Browsing is experimental
  and informational only.
```
