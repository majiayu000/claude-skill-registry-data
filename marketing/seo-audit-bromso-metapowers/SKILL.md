---
description: Audit technical SEO, on-page SEO, and content gaps
---

# SEO Audit

Conduct a comprehensive SEO audit for "$ARGUMENTS". Analyze technical SEO, on-page optimization, and content gaps to identify improvement opportunities.

## Prerequisites

Read `.metapowers/marketing/$ARGUMENTS/00-strategy.md`. If this file does not exist, tell the user:

> Phase 0 (Strategy) has not been completed for "$ARGUMENTS". Run `/marketing:customer-research $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check and log to `.metapowers/marketing/$ARGUMENTS/skip-log.md`.

## Process

1. **Read context:**
   - Read `.metapowers/marketing/$ARGUMENTS/00-strategy.md` for audience and competitor data
   - Read `plugins/marketing/shared/seo-checklist.md` for the audit framework
   - Read `plugins/marketing/shared/race-framework-guide.md` for Reach phase guidance

2. **Technical SEO analysis:**
   - If a URL is provided, use WebFetch to analyze the site
   - Check against the technical SEO checklist: site speed, mobile-friendliness, HTTPS, sitemaps, robots.txt
   - Identify crawlability and indexability issues
   - Check Core Web Vitals status

3. **On-page SEO analysis:**
   - Evaluate title tags, meta descriptions, heading structure
   - Check keyword usage and content optimization
   - Analyze internal linking structure
   - Review image optimization (alt text, file size, format)

4. **Content gap analysis:**
   - Use WebSearch to identify high-value keywords competitors rank for
   - Find "low-hanging fruit" — keywords with search volume and low competition
   - Map content gaps to content pillars (if content-strategy has been run)

5. **Prioritize recommendations:**
   - Score each issue by impact (traffic potential) and effort (implementation difficulty)
   - Create a prioritized action list: quick wins first, then strategic investments
   - Estimate traffic impact of top recommendations

6. **Write the artifact** — append to `.metapowers/marketing/$ARGUMENTS/01-reach.md` under a `## SEO Audit` section:
   - **Technical SEO** — issues found, severity, fix recommendations
   - **On-Page SEO** — optimization gaps per page
   - **Content Gaps** — keyword opportunities with search volume estimates
   - **Prioritized Action Plan** — ranked by impact/effort
   - **Estimated Impact** — traffic potential of top fixes

## Output

SEO audit appended to `.metapowers/marketing/$ARGUMENTS/01-reach.md`. Present a summary highlighting:
- Critical technical issues (if any)
- Top 5 keyword opportunities
- Recommended first actions
