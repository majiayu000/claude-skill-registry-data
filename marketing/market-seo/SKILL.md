---
name: market-seo
description: SEO content audit covering on-page SEO, E-E-A-T, keyword analysis, technical SEO, and content strategy.
---

# SEO Content Audit

## Skill Purpose

Perform a comprehensive SEO audit of a webpage or website, covering on-page SEO,
content quality, keyword alignment, technical SEO, and content strategy. Use the
automated page analysis script for baseline evidence, then add expert judgment
and prioritized recommendations.

## When to Use

- User provides a URL and asks for SEO analysis, audit, or recommendations.
- User wants to improve organic search rankings and traffic.
- User asks about on-page SEO, meta tags, content quality, or technical SEO.
- User wants content gap analysis or content strategy recommendations.
- Triggered by `/market seo <url>` or `/market seo`.

## Core Workflow

1. Run automated analysis:

   ```bash
   python3 scripts/analyze_page.py <url>
   ```

2. Use the JSON output as evidence for title, metadata, headings, links,
   images, forms, CTAs, schema, social links, tracking scripts, viewport,
   canonical, and robots directives.
3. Manually evaluate on-page SEO: title, meta description, headings, images,
   internal links, and URL structure.
4. Assess E-E-A-T: experience, expertise, authoritativeness, and
   trustworthiness.
5. Identify primary keyword, secondary keywords, and search intent fit.
6. Check technical SEO basics: robots, sitemap, canonical, speed, and mobile.
7. Identify content gaps, featured snippet opportunities, schema needs,
   internal linking improvements, and Core Web Vitals impact.
8. Recommend blog/content strategy based on topic gaps, search intent,
   competition, and business value.
9. Produce `SEO-AUDIT.md` with evidence, scores, before/after recommendations,
   and priorities by impact and effort.

## Operating Rules

- Do not claim search volume, ranking, traffic, or conversion impact unless you
  have evidence or clearly mark it as an estimate.
- Do not fabricate crawl data, analytics, Search Console data, or competitor
  findings.
- Use automated output as the starting point; explain what it means and what to
  change.
- Tie recommendations to business outcomes, not only checklist completion.
- Prioritize by effort-to-impact ratio.
- Keep private analytics, customer data, credentials, and unpublished strategy
  out of tracked files and final public docs.
- If `/market audit` or `/market landing` findings exist, cross-reference them
  when relevant.

## Reference Map

Read `references/seo-operating-reference.md` when you need the full audit
rubrics and templates for:

- title, meta, heading, image, internal link, and URL criteria
- E-E-A-T assessment prompts
- keyword and search intent tables
- robots, sitemap, canonical, speed, and mobile checks
- content gap and featured snippet methods
- schema markup audit table
- internal linking architecture
- Core Web Vitals impact notes
- content prioritization matrix
- complete `SEO-AUDIT.md` output template

## Output Standard

The final audit should include:

- SEO health score and evidence basis
- current state and recommended change for each major issue
- content quality and keyword analysis
- technical SEO findings
- content gap, snippet, schema, internal link, and performance opportunities
- prioritized recommendations: critical, high, medium, and low

Keep the audit educational: explain why each issue matters and how the user can
verify the fix.
