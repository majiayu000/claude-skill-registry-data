---
name: seo-a11y-audit
description: Composite skill — full SEO + Accessibility audit of a website or webapp in one workflow. Chains audit-website (squirrelscan SEO + tech + perf scan) + seo-audit (SEO framing) + playwright-best-practices (axe-core a11y) + ui-audit (design-system accessibility patterns) → reconciled severity-ranked report split by SEO vs A11y vs Both. Use for periodic site health checks, pre-launch audits, or when search rankings drop.
triggers:
  - seo-a11y-audit
  - seo audit
  - accessibility audit
  - a11y
  - site audit
  - pre-launch check
  - composite skill
---

# SEO + Accessibility Audit

Pairs SEO and accessibility in one composite because they share root causes: both
fail when content isn't discoverable, semantic, or properly structured. A site that
fails for screen readers usually also fails for search bots, and vice versa.

## Auto-invocation triggers

- User says "audit my site", "check SEO", "accessibility audit", "is this site good"
- Pre-launch / pre-redesign reviews
- Quarterly site health check
- After a search rankings drop or accessibility complaint
- Before submitting a site to government/enterprise procurement (a11y compliance often required)

## Workflow

### Phase 1 — Broad scan (always, in parallel)

Dispatch in parallel:

**`audit-website`** (squirrelscan, 230+ rules across 15 categories)
- SEO: meta tags, Open Graph, schema markup, sitemap, robots, canonical, internal links
- Accessibility: alt text, ARIA, color contrast, focus order, semantic HTML
- Technical: HTTPS, performance, broken links, redirects
- Returns: structured findings with severity + URL

**`seo-audit`** (focused SEO framing on top of audit-website)
- Indexability: robots.txt, sitemap.xml, noindex tags
- On-page: title/meta uniqueness, heading hierarchy, keyword targeting
- Content: thin content, duplicate content, content-to-code ratio
- Returns: SEO backlog with remediation order

### Phase 2 — Deep accessibility (always, requires running site)

**`playwright-best-practices` axe-core scan:**
- Run axe-core against each top-level route
- WCAG 2.1 AA + AAA flags
- Returns: per-route a11y violations with element selectors

If the site isn't accessible from the dev machine: skip Phase 2, mark as PARTIAL,
recommend running locally with the site up.

### Phase 3 — Design-system pattern review (always)

**`ui-audit` accessibility-focused mode:**
- Color palette: contrast ratios across actual UI states
- Typography: font sizes, line heights, readability scores
- Layout patterns: focus order, keyboard navigation, skip links
- Component patterns: form labels, error messaging, ARIA usage
- Returns: pattern-level recommendations distinct from per-page violations

### Phase 4 — Reconcile findings

Combine all four sources into one severity-ranked list, organized into 3 buckets:

**Bucket A — SEO only** (search-discoverability issues)
- Missing meta descriptions
- No canonical tags
- Missing schema markup
- Slow page load (Core Web Vitals)

**Bucket B — Accessibility only** (assistive-tech issues)
- Color contrast failures
- Missing alt text on decorative images
- Keyboard traps
- ARIA misuse

**Bucket C — Both** (highest priority — impacts both audiences)
- Missing/empty `<title>` tags (SEO + screen readers)
- No heading hierarchy (SEO + navigation)
- Images without alt text (SEO + screen readers)
- No semantic HTML (`<main>`, `<nav>`, `<article>`) (SEO + screen readers)
- Inaccessible forms (SEO can't index, users can't submit)
- JS-only content (search bots and screen readers both miss it)

Bucket C findings are **always CRITICAL** — they fail for both audiences with one
root cause. Fix these first; ROI is doubled.

### Phase 5 — Severity ranking + remediation plan

For each finding:
- **Severity**: CRITICAL (blocks audience) / HIGH (degrades experience) / MEDIUM (best practice) / LOW (polish)
- **Effort**: 5min / 30min / 2h / day+
- **Affected scope**: single page / template / sitewide

Sort by **(impact × audiences) ÷ effort** for the action plan.

### Phase 6 — Capture

Write report to `~/.claude/projects/<slug>/memory/seo_a11y_audit_<domain>_<date>.md`.
Trend visible across periodic runs.

If pre-launch and any CRITICAL/HIGH found: surface as a launch blocker.

## Reconciliation

```
SEO + ACCESSIBILITY AUDIT — <domain> — <date>

Tools run:  audit-website ✓, seo-audit ✓, axe-core ✓ (N routes), ui-audit ✓
Pages scanned: N

CRITICAL — Bucket C (both audiences):
  ✗ <finding>     (5min, sitewide)    Fix: <action>
  ✗ <finding>     (30min, single page) Fix: <action>

CRITICAL — Bucket A (SEO):
  ✗ <finding>

CRITICAL — Bucket B (A11y):
  ✗ <finding>

HIGH (X), MEDIUM (Y), LOW (Z): see report.

Top 5 actions (impact × audiences ÷ effort):
  1. <action> (fixes 1 CRITICAL Bucket C, 5min)
  2. <action> (fixes 3 HIGH Bucket B, 30min)
  3. ...

Memory: <report path>
Launch blocker: YES / NO
```

## Outputs / Evidence

- Reconciled severity-ranked report split by bucket
- Effort-sorted remediation plan
- Memory file for trend tracking
- Launch-blocker verdict if pre-launch context

## Failure / Stop Conditions

- Site not reachable → audit-website + seo-audit fail; partial report from
  ui-audit only with note
- Playwright cannot run (CI/headless env without browser): skip Phase 2,
  mark as PARTIAL, recommend manual axe DevTools scan
- audit-website CLI not installed: stop with install instruction; this skill
  needs squirrelscan to function

## Memory Hooks

- Read prior reports for trend (e.g., "color contrast HIGH flagged 4 quarters
  running — push design system fix")
- Read documented false-positive list (e.g., "decorative SVG with empty alt is
  intentional, suppress")
- Write report as primary output
