---
name: web-content-extraction
description: Use when an app needs to fetch and render THIRD-PARTY page content the app doesn't control — a reader mode, article extraction, OG/link-preview cards — from a static-hosted web app (CORS wall) or a native app (no CORS, different traps). Carries the multi-proxy CORS fallback chain with per-proxy timeouts and user-visible progress, the OG-metadata silent-skip rule, the iOS analog (URLSession fetch + off-screen WKWebView extraction with external resources STRIPPED first), and content-language detection done on the article's own text rather than metadata tags. Triggers on CORS proxy, allorigins, corsproxy, reader mode, readability, article extraction, link preview, OG metadata, open graph card, WKWebView extraction, "fetch blocked by CORS".
---

# Web Content Extraction

Patterns from shipping a reader mode + link previews in a production
client app on both web (static host, full CORS wall) and iOS (no
CORS, its own traps). The generic rule "never fetch no-CORS hosts"
(`web-platform-patterns`) is right for data you control; this skill
is for the case where fetching arbitrary third-party pages IS the
feature.

## Web: the multi-proxy fallback chain

No single free CORS proxy is reliable enough to bet a feature on.
Ship a **chain**, tried in order, each attempt bounded:

1. Order proxies by measured reliability (in production:
   codetabs.com → corsproxy.io → allorigins.win — the first was most
   reliable; the last times out on large pages). Re-verify the
   ordering per app; free proxies drift.
2. **Every attempt gets its own `AbortController` timeout**
   (~18 s worked). Unbounded, a dead proxy hangs the view.
3. **Show live per-proxy progress** ("Trying proxy 2 of 3…"). Worst
   case is chain-length × timeout before final failure — the user
   must see the app working, not a frozen screen.
4. Final failure is a user-visible error with a "open the original"
   escape hatch, never a blank pane.

Free proxies have no SLA. Treat the chain as a degradable
enhancement: the feature that needs it must have a proxy-free
fallback tab (open the URL directly).

**OG / link-preview metadata** rides the same proxy path with one
different failure rule: **silently skip on failure**. A compose flow
must never block or error because a preview couldn't be fetched —
post without the card.

## Native (iOS): no CORS, different traps

- Fetch the HTML directly with `URLSession` (send a real device
  User-Agent — many sites vary markup by UA). No proxy needed; the
  whole chain above is web-only.
- Extract by loading the HTML into an **off-screen `WKWebView`** and
  querying the DOM with the usual selector cascade (`article`,
  `main`, `.entry-content`, …) — a real DOM beats regex extraction.
- **Strip every external resource from the HTML before loading it
  into the extractor** — `<img> <script> <link> <iframe> <video>
  <audio> <source> <picture> <style>`. The extractor needs DOM
  structure only; leaving resources in makes the hidden web view
  fetch the entire page's assets — network churn, image-decode
  errors, sub-frame SSL failures, and web-content process churn, all
  invisible until profiled.

## Filter on the content's own language, not its metadata

If a reader surface should be language-filtered, detect the language
of **the article's own text** (title + description/card text) — not
the wrapping item's language tag. Post-level `lang` tags are wrong
two ways: link-share/bot posts usually omit them (and "missing"
defaults to a guess), and the post's language is independent of the
linked article's. On Apple platforms use the on-device
`NLLanguageRecognizer`; on web, honor an explicit tag strictly, then
a non-Latin-script ratio check, then function-word density for
Latin-script text. **Err toward allowing when ambiguous** —
over-filtering the primary language is worse than letting an
occasional other-language item through.

## Reading-state

Mark extracted/read items into the same seen-store the feed uses
(`values-based-feed-ranking` §3) so reader views and feed dedup agree
— a reader that re-surfaces what the feed already showed feels
broken.
