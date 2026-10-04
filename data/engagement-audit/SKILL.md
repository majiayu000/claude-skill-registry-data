---
name: engagement-audit
description: On-site engagement audit for visitors arriving from AI answers. Use when AI referral traffic bounces or fails to convert. Checks answer-first openings, mid-funnel context, interstitials, scannability, substance versus chrome, image-only content, form friction, next steps, and structural speed proxies.
license: MIT
---

# Engagement (on-site layer)

The second half of the problem, and a genuinely different one. Everything
upstream asks whether a machine can find, read and use the page. This asks
whether the *human* the machine sent stays.

## The arrival pattern that makes this different

A visitor from an AI answer does not arrive like a search visitor. They arrive:

- **Mid-funnel** — on a deep page, not the homepage, because the assistant
  cited the page that answered the question.
- **Partially informed** — they already have an answer. They are here to verify
  it, or to act on it.
- **Without the navigation context** a site assumes people accumulate on their
  way in.

So a deep page that reads as a fragment of a journey — assuming you know what
the product is, who the company is, and what the previous page said — fails
this visitor even when the site works fine for someone who entered at the
homepage. `EN002` is the check for exactly that.

## When to use

After `crawl-reachability`. Run standalone when a site gets AI-referred traffic
that does not convert or stay.

## What this layer can and cannot see

It reads shipped markup only, so it measures page-side proxies for engagement,
never engagement itself. Two consequences are load-bearing:

- **No JavaScript is executed and no session is simulated.** Anything that only
exists after hydration is out of scope, and a finding is never raised about it.
- **Where a proxy stands in for an unmeasurable quantity, the finding says so.**
`EN009` is labelled a structural proxy rather than presented as a Core Web
Vitals measurement.

## Inputs

- **Required** — a run workspace from the two upstream stages: `preflight.json`
  for the scope domain and `reachability.json` for the page inventory and saved
  HTML paths.
- **Optional** — `--config` (an `AuditConfig` JSON) and `--strictness`
  (`lenient` | `balanced` | `strict`) to override interstitials and chrome-ratio
  thresholds. Defaults come from `AuditConfig`.
- **Not consumed** — no network access, no analytics, no prior stage's
  findings, no visitor data. The layer is re-runnable offline and deterministic.

```
python3 scripts/check_engagement.py [--workspace PATH] [--json]
```

## Procedure

Deterministic, in this order. Every check is a pure function of the fetched
markup plus the config; nothing is sampled and nothing depends on the clock.

1. **Load the inventory and pages.** Resolve the scope domain from `preflight`,
   then read every fetched page; missing HTML becomes a coverage limitation.
2. **Answer-first orientation (`EN001`).** Test whether the opening states the
   answer or sells at the visitor.
3. **Intent continuity (`EN002`).** Test whether a deep page stands alone for a
   mid-funnel arrival who never saw the homepage.
4. **Interstitials (`EN003`).** Detect anything demanding an interaction before
   the first one the visitor came for.
5. **Scannability (`EN004`).** Check `h1` presence and heading-level
   continuity.
6. **Chrome ratio (`EN005`).** Compare substantive content against navigation,
   footer and consent chrome.
7. **Substance in images (`EN006`).** Flag content carried only by images with
   no text alternative.
8. **Form friction (`EN007`).** Measure how much is asked before anything is
   given on conversion paths.
9. **Dead ends (`EN008`).** Flag pages offering no next step beyond site-wide
   navigation.
10. **Perceived speed (`EN009`).** Count render-blocking resources in `<head>`,
    and label the result a structural proxy.
11. **Attach the sample caveat.** Every population claim carries its sample
    size for the advisory layer to verify.

## Checks and severities

Every check the procedure above can emit, with the claim level it is allowed to
assert.

| Check | Detects | Severity | Claim level |
|---|---|---|---|
| `EN001` | The opening sells rather than answering | medium | 3 |
| `EN002` | Deep pages that do not stand alone for a mid-funnel arrival | medium | 3 |
| `EN003` | Interstitials blocking the first interaction | medium | 3 |
| `EN004` | Missing `h1` or skipped heading levels | medium | 1 |
| `EN005` | Substance outweighed by surrounding chrome | medium | 3 |
| `EN006` | Substance carried only in images with no text alternative | medium | 3 |
| `EN007` | Conversion forms asking a lot before giving anything | medium | 1 |
| `EN008` | Pages offering no next step beyond site-wide navigation | medium | 2 |
| `EN009` | Render-blocking resources in `<head>` (structural proxy) | medium | 3 |

## Honesty about what cannot be measured

`EN009` is deliberately labelled a **structural proxy, not a measurement**.
Core Web Vitals cannot be computed from raw HTML: Largest Contentful Paint,
Interaction to Next Paint and Cumulative Layout Shift all require a real
rendering engine and, for field data, real users.

What *is* observable is render-blocking resource count in `<head>` and images
lacking intrinsic dimensions — structural conditions associated with poor LCP
and CLS. The check reports those as what they are, at claim level 3, capped at
`medium`. Reporting a fabricated performance score from raw HTML would be
precisely the kind of confident-and-wrong finding this marketplace is built to
avoid.

`EN008` needs at least three pages to distinguish site-wide chrome links from
page-specific next steps, and skips itself with a stated note below that
threshold rather than guessing.

## Summariser legibility

Handout appendix F describes a related failure: when the real substance of a
message is not available as readable text — carried in an image, or surrounded
by low-value filler — a summariser has little to work with and the important
part disappears. `EN005` and `EN006` cover both shapes of that on a web page.

## Output

`06-engagement-audit.json` with per-page opening analysis, interstitial
inventory, heading hierarchy, chrome ratio, form field counts, next-step link
analysis and the findings.

## Guardrails

Read-only; consumes saved HTML only. No form is ever submitted, no interaction
is simulated, no JavaScript is executed.

## Grounding

Handout appendix F (summariser legibility) and appendix E (answers are shaped
by who is asking, so a page must stand alone for an arrival it did not
script). The mid-funnel arrival pattern follows from the citation model in
arXiv:2604.25707: the cited page is the page that answered the question, which
is rarely the homepage.
