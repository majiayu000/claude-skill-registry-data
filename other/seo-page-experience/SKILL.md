---
name: seo-page-experience
description: >
  Holistic page-experience self-assessment mirroring Google's own question
  list: Core Web Vitals, HTTPS, intrusive interstitials, mobile usability,
  content prominence, and ad distinguishability. Use when user says "page
  experience", "UX signals", "interstitials", "mobile friendly", or
  "HTTPS check".
allowed-tools:
  - Read
  - Bash
  - WebFetch
---

# Page Experience Self-Assessment
<!-- Updated: 2026-06-10 -->

Google retired the standalone "page experience ranking signal" framing.
Per https://developers.google.com/search/docs/appearance/page-experience there
is **no single page experience signal** — Google's core ranking systems look
at a variety of signals that align with overall page experience. Of these,
**Core Web Vitals are used by ranking systems**; other aspects (HTTPS,
interstitials, mobile usability) don't directly boost rankings but make the
site more satisfying to use, which aligns with what ranking systems reward.
Evaluation is generally **page-specific**, with some site-wide assessments.

This skill runs Google's own self-assessment question list against a URL.

## Google's Self-Assessment Questions

| # | Question | How this skill checks it |
|---|----------|--------------------------|
| 1 | Do your pages have good Core Web Vitals? | Delegate to `seo-core-web-vitals` skill (field data at p75) |
| 2 | Are your pages served in a secure fashion? | HTTPS, redirect, certificate, mixed content |
| 3 | Does your content display well on mobile devices? | Viewport meta, responsive markup, font size, tap targets |
| 4 | Does your content avoid excessive ads that distract from or interfere with the main content? | Ad density heuristics on HTML (manual confirmation advised) |
| 5 | Do your pages avoid using intrusive interstitials? | Interstitial heuristics on initial HTML |
| 6 | Can visitors easily distinguish the main content from other content? | Above-fold content prominence, labeled ads |

## Inputs

| Input | Required | Notes |
|-------|----------|-------|
| URL | Yes | Single page; page experience is evaluated per page |
| Mobile or desktop focus | No | Default mobile — interstitial rules target mobile entry from search |

## Execution

1. **Fetch the page and check HTTPS:**
   ```bash
   curl -sI -L -w 'final_url=%{url_effective} http=%{http_code}\n' http://<host><path>
   curl -s -o /dev/null -w '%{http_code}' https://<url>
   ```
   - `http://` must 301-redirect to `https://` (single hop ideal).
   - Certificate valid (`curl -v` shows no TLS errors).
   - Scan HTML for mixed content: `http://` URLs in `src=`, `href` of stylesheets, `srcset`.

2. **Check mobile usability on the fetched HTML:**
   - `<meta name="viewport" content="width=device-width...">` present.
   - No fixed-width layouts (`width=1024` style viewports, large fixed px containers).
   - Base font size ≥ 12px legible (16px recommended); tap targets ~48x48px.
   - For deeper checks, cross-reference the `seo-technical` skill (category 5).

3. **Run interstitial heuristics on the initial HTML** (the case Google
   penalizes is a pop-up covering the main content when a user enters from
   mobile search):
   - Fixed/absolute full-viewport overlays in initial HTML: elements with
     `position:fixed` or `position:absolute` combined with `top:0` +
     `width:100%`/`100vw` + `height:100%`/`100vh`, high `z-index`.
   - Modal markers present at load: `class`/`id` containing `modal`,
     `popup`, `overlay`, `interstitial`, `lightbox` outside obvious consent
     managers; `<dialog open>`.
   - Body scroll-lock at load: `overflow:hidden` on `html`/`body` in initial CSS.
   - Redirects to a separate consent/input page (Google calls this out
     explicitly as a mistake — it can remove all but that page from results).
   - Flag findings as **suspected** — heuristics on static HTML can't see
     JS-triggered timing; recommend a real mobile-device check.

4. **Classify any interstitial found** per
   https://developers.google.com/search/docs/appearance/avoid-intrusive-interstitials:

   | Type | Verdict |
   |------|---------|
   | Full-page promo/app-install interstitial covering main content on entry | ❌ Intrusive |
   | Dialog obscuring part of the content for promotion | ⚠️ Risky — prefer a banner |
   | Legally mandated (cookie consent, age gate) | ✅ Exempt — but overlay content, don't redirect; for adult age gates, consider serving verified Googlebot without the gate |
   | Login wall for genuinely gated content | ✅ Exempt |
   | Small, easily dismissible banner (e.g., Smart App Banner, newsletter strip) | ✅ Fine — Google's recommended pattern |

5. **Assess content prominence and ads:**
   - Is meaningful main content present in the initial HTML above the fold,
     or is the first viewport dominated by ads/promos/navigation?
   - Are ad containers distinguishable/labeled (e.g., "Advertisement",
     `aria-label`, distinct containers)?
   - Count ad-network script includes (adsbygoogle, GPT, taboola, outbrain,
     mgid) as an ad-pressure signal. These are heuristics — note that final
     judgment needs visual review.

6. **Delegate CWV measurement** to the `seo-core-web-vitals` skill and import
   its PASS/FAIL verdict for question 1. Do not duplicate the measurement here.

7. **Optional speed-up note:** if the site is a publisher with heavy
   search-entry traffic, mention Signed Exchanges (SXG) as a way to let
   Google prefetch content and improve effective LCP from search
   (https://developers.google.com/search/docs/appearance/signed-exchange).

## Quick Reference — Pass Criteria

| Check | Pass threshold |
|-------|----------------|
| HTTPS | http→https 301 in ≤1 hop, valid cert, zero mixed-content URLs |
| Viewport | `width=device-width` viewport meta in initial HTML |
| Font size | ≥60% of text ≥12px (16px base recommended) |
| Tap targets | ~48x48px with ~8px spacing |
| Interstitials | No non-exempt full-page overlay in initial HTML |
| Ad pressure | Main content begins above the fold; ads labeled |

Useful companion tools (from Google's resources list): Search Console's
HTTPS report and Core Web Vitals report, and Chrome Lighthouse
(https://developer.chrome.com/docs/lighthouse/overview) for mobile-usability
and page-experience improvement hints.

## Output

```
# Page Experience Self-Assessment: <url>

## Google's Six Questions
| # | Question | Verdict | Evidence |
|---|----------|---------|----------|
| 1 | Good Core Web Vitals? | ✅/⚠️/❌ | from seo-core-web-vitals (p75 field data) |
| 2 | Served securely (HTTPS)? | ✅/⚠️/❌ | https enforced, cert valid, no mixed content |
| 3 | Displays well on mobile? | ✅/⚠️/❌ | viewport meta, font size, tap targets |
| 4 | Avoids excessive ads? | ✅/⚠️/❌ | N ad scripts, above-fold ad pressure |
| 5 | Avoids intrusive interstitials? | ✅/⚠️/❌ | overlays found / exempt types |
| 6 | Main content distinguishable? | ✅/⚠️/❌ | above-fold content vs ads/nav |

Overall: X/6 yes — "Answering yes to these questions means you're probably
on track in providing a good page experience."

## Findings Detail
### HTTPS  (redirect chain, certificate, mixed content list)
### Mobile usability  (specific failures with code locations)
### Interstitials  (each suspected overlay: selector, type, verdict per the
    classification table, recommended replacement — banner pattern)
### Ads & content prominence  (observations + manual-review note)

## Recommendations (prioritized)
1. ...

## Context
- No single "page experience signal" exists; CWV is used by ranking systems,
  other aspects improve user satisfaction rather than rankings directly.
- Evaluation is page-specific (with some site-wide assessments) — re-run on
  templates that differ (home, article, product).
- Source: https://developers.google.com/search/docs/appearance/page-experience
```
