---
name: conversion-funnel-auditing
description: "Audits a live website funnel end to end (traffic promise, landing page, CTAs, forms, scheduler, payment, confirmation page, nurture handoff, client-visible tracking, consent and mobile layout) without submitting anything, separates what was observed from what was inferred, and turns it into copy/reject/improve findings, a P0/P1/P2 fix list and a target funnel. Use for competitor funnel teardowns, CRO audits, 'why aren't we getting bookings', 'check our tracking', launch-readiness checks, event QR funnels and AI-search (LLM) visibility audits. Works best in Claude Code with a headless browser (Playwright); web fetch alone covers the text-only parts."
---

# Conversion Funnel Auditing

Audit the funnel that is live today, not the one the brand name, old reputation
or the brief implies. If the domain has been repurposed or redirects somewhere
else, that is the lead finding.

## Tools

- Best: Claude Code with a headless browser (Playwright or Puppeteer) for DOM,
  network requests, console errors, CSP and fixed-size screenshots. Keep it headless.
- Fallback: web fetch / `curl` for HTML, headers, robots, sitemaps and redirects.
  Then say plainly that runtime tags, CSP blocking and mobile layout were NOT verified.
- Never submit a form, confirm a booking or start a checkout with made-up details.
  A full operational test needs the owner's permission and a designated test identity.

## Steps

1. **Identity and scope.** Open the root URL; record final URL, title,
   description, brand, audience, main conversion goal. Read `robots.txt`,
   `sitemap.xml`, `sitemap_index.xml` (discovery aids, not proof of absence).
   Extract every link, form, iframe and nav destination.
2. **Map the path before judging it:**
   `traffic source -> landing page -> CTA -> offer page -> form/scheduler/payment -> confirmation -> nurture/sales handoff`.
   Include every branch: email-only applications, alternate offers, cross-domain hops.
3. **Inspect each conversion surface.** Headline, audience qualifier, CTA
   hierarchy, offer, price, proof, objections handled, friction, next step.
   Follow real CTA destinations (not button labels). Open embedded forms and list
   fields without submitting. Follow the public thank-you page. Say explicitly when
   a scheduler, payment step, lead magnet or nurture is absent.
4. **Tracking, four separate signals per tag** (GTM, GA4, Google Ads, Meta,
   PostHog, session replay, server-side collectors): present in code / requested by
   the browser / allowed or blocked by CSP / observed sending a collection request.
   Capture console CSP errors. A tag ID or preload proves nothing about firing.
5. **Consent (if a banner exists).** In a fresh browser state, log requests
   before any choice, after decline and after accept. Report network behaviour,
   not legal conclusions.
6. **UTM survival.** Load the landing page with a test query
   (`?utm_source=audit&utm_medium=test&utm_campaign=check`) and follow each CTA
   across domains and into embedded schedulers. A dropped source field is a P0.
7. **Responsive check.** Screenshots at 1440x900 and 390x844 (state the real
   viewport). Compare CTA order and depth, stacking, touch targets, form behaviour,
   content hidden by breakpoint, total scroll.
8. **Route hygiene.** Probe a random nonexistent path, `/privacy`, `/terms`,
   `/thank-you`. A "not found" page returning 200 with `index, follow` is a soft
   404. Count sitemap pages with zero links or no CTA.
9. **Translate.** Three buckets: **Copy** (structural patterns worth adapting),
   **Reject** (misleading proof, weak trust, needless friction), **Improve** (how to
   beat it). Copy principles, not surface aesthetics.
10. **Propose the target funnel** if asked: entry pages, homepage structure, offer
    ladder, qualification and routing, scheduler expectations, proposal/payment
    path, confirmation page, segmented nurture, analytics events from source to
    revenue, phased priorities. Tie each item to an observed strength or gap.

## Variants (read the reference when the scope includes it)

| Scope | Reference |
|---|---|
| Typeform/embedded forms, hidden attribution, React/Next.js client logic, CSP | `references/live-site-inspection.md` |
| Exhaustive technical SEO, schema, `llms.txt`, AI crawler access, answer-engine visibility | `references/technical-crawl-and-answer-engines.md` |
| Live talk or deck driving a QR, personalised pages or scheduler | `references/event-and-presentation-funnels.md` |
| Launch plan, 7/14-day sequence, source-to-cash KPI scoreboard, ABM campaigns | `references/campaign-launch-and-source-to-cash.md` |
| YouTube/content descriptions routing to owned pages, affiliates, communities | `references/content-to-site-monetization.md` |

## Decision rules

- **P0** (blocks conversion or measurement): broken CTA or QR destination, form or
  scheduler that cannot complete, UTMs dropped at a boundary, conversion tag
  blocked by the site's own CSP, price or offer contradiction between pages.
- **P1** (costs conversions): message mismatch ad to page to scheduler, CTA buried
  more than about three screens deep on mobile, long form with no qualifier value,
  missing confirmation next step, soft 404s on linked routes.
- **P2**: proof quality, copy polish, secondary tracking, schema hygiene.
- Timeouts, 403, 429 and SSL failures on external URLs are "inconclusive", not
  "broken", unless reproduced.
- No access to CRM, ad accounts or email tool: say so, and never claim
  attribution accuracy, campaign performance or nurture content.

## Output

Save a Markdown report and confirm it was written. Keep the chat reply short:
decisive finding, report path, top fixes.

```markdown
# Funnel audit: example.com (observed 2026-01-15, nothing submitted)

**Lead finding:** the "Book a call" CTA opens a 45-min scheduler while the page
promises 20 minutes, and the scheduler drops all UTM parameters.

| Stage | Observed | Evidence |
|---|---|---|
| Landing | Headline "...", single CTA above fold | example.com/ (desktop + mobile shots) |
| Form | 9 fields, phone required, no qualifier | Typeform /to/abc123, fields listed |
| Confirmation | Generic "thanks", no next step | example.com/thank-you (public, indexable) |

| P | Fix | Acceptance test |
|---|---|---|
| P0 | Pass UTMs into the scheduler embed | test query survives to booking form hidden fields |

Tracking: GA4 present+requested+collecting; Meta pixel present, blocked by CSP (console error).
Limits: no submissions, no CRM or ad-account access.
Copy / Reject / Improve: ...
Sources: (every URL inspected)
```

## Pitfalls

- Trusting server-rendered form `action` when React replaces submit behaviour.
- Stopping at the form instead of following the public completion page.
- Calling a crawl exhaustive because it hit a page cap.
- Treating a homepage catch-all as a valid robots, sitemap, feed or 404.
- Counting JSON-LD blocks without parsing each one.
- Social follower counts presented as buyer proof.
- One generic "book a call" recommendation instead of a routed offer ladder.
