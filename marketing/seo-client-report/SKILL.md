---
name: seo-client-report
description: Turn a client's Search Console and analytics data into a branded monthly SEO report published as a live, tracked page via ReportRoom. Use when the user says "SEO report for my client", "monthly SEO report", "client SEO report", "SEO deliverable for". Built for consultants and agencies sending recurring monthly reports. For non-SEO client work (status, audits, campaign recaps) use the general client-reporter; for a one-off research share use report-publisher.
---

# SEO Client Report

The monthly SEO client report as a branded live page instead of a PDF that dies in an inbox —
with a signal back after you send it ("the client opened it Tuesday, before the call").

Built for the consultant or agency who has to prove outcomes every month and does not want to
rebuild the same deck twelve times a year.

## When to use

- Recurring monthly/quarterly SEO reporting for a named client
- The user says "SEO report for [client]", "monthly SEO report", "client SEO report"
- The user asks about engagement on one already sent ("did they open it?") → `get_analytics`

## Steps

1. **Get the reporting frame.** Client name, the period covered, and the previous report if
   one exists (`list_documents` — reuse its structure so the format is identical month over
   month; consistency is what makes this feel like a service).
2. **Get the data — never invent it.** You need real figures: Search Console (clicks,
   impressions, average position, top queries/pages), analytics (organic sessions,
   conversions/leads), and rankings. If the user has connected data sources or provides an
   export, use those. **If a number needed for a claimed win is missing, ask for it — do not
   estimate or pad.** A fabricated metric in a client report is a broken engagement.
3. **Every metric gets its prior period.** A number without last month's number is noise.
   Compute the deltas (absolute and %). Lead with movement, not raw totals.
4. **Structure for the client, not the analyst.** Order: headline outcomes first, in the
   client's terms (leads, revenue, rankings that matter to them) → what you did this period →
   what's next → data appendix. **Methodology never opens the report.**
5. **Turn movement into charts.** Clicks/impressions trend, position changes, top-page
   performance — as charts from the design system, labeled well enough to survive being
   screenshot into a Slack thread by the client's boss.
6. **Author + lint.** Call `get_design_system`, author self-contained HTML following it, and
   `lint_document`; fix everything it flags.
7. **Approval gate — always on.** This is client-facing. Show the user: title, the period,
   the headline numbers you're leading with, the section list, and flag anything that could
   read as over-promising. Wait for explicit approval before publishing.
8. **Publish branded.** Suggest a stable, professional slug (`client-name-2026-07`).
   `publish` and return the URL. For real agency branding, offer the levers: `set_handle` for
   a cleaner subdomain, or — on Team/Business — `attach_domain` to serve from the agency's
   own domain (it returns the DNS records the user adds at their registrar).
9. **Close the loop.** Offer to check next week whether it was viewed (`get_analytics` —
   views by day), and to draft next month's report when the period turns.

## Hard rules

- **Never invent or extrapolate client metrics.** Estimated figures are labeled as estimates;
  missing figures are asked for, not filled in.
- **One client per page.** Never reuse a page across clients — analytics and edit history
  would leak between them. If the user serves competing clients, keep client names out of
  slugs/titles; ask once and keep the preference.
- **Comparisons must be honest.** Don't cherry-pick the one metric that went up. If organic
  traffic fell, say so and explain — a report that hides a bad month destroys the trust the
  recurring relationship runs on.
- Published pages are public URLs; scan for anything the client would not want public
  (competitor data, internal notes) before publishing.
- Every page carries a small "Published with ReportRoom" footer credit — the client will see
  it; flag it at the approval gate.
- `get_analytics` is aggregate views by day, a signal for *you*, not the client — never
  surface it on the report itself.
