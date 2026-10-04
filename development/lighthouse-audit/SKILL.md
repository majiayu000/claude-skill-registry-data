---
name: lighthouse-audit
description: Run Google Lighthouse against a live URL (mobile + desktop), diagnose the performance/accessibility/SEO/best-practices findings against this codebase's actual source, and write a prioritized fix plan. Use this whenever the user asks to "run a lighthouse audit", "check performance", "audit accessibility/SEO", wants Core Web Vitals (LCP, CLS, TBT, FCP) numbers for the site, mentions a slow page load, or asks "why is my site slow / scoring badly". Also use if the user hands you existing `lighthouse-*.json` report files and asks what's wrong — skip straight to the diagnosis step in that case.
---

# Lighthouse Audit

Runs Lighthouse against a URL, cross-references every finding against this repo's actual source (not generic advice), and produces a fix plan the user can act on immediately or hand off later.

**Ask for the URL first if the user didn't give one.** Default to the production URL if this is a deployed site with an obvious one (check `netlify.toml`, `package.json` homepage, or ask) — don't assume `localhost` unless the user says they want to audit a local dev build.

## Why both mobile and desktop

Lighthouse throttles mobile runs to simulate a mid-tier phone on a slow connection; desktop runs mostly untouched. The gap between the two numbers is itself a diagnostic signal — a huge mobile/desktop LCP gap (e.g. 3.5s vs 18.5s) usually means something that's cheap on a fast desktop CPU (large image decode, a heavy font, JS execution) becomes the bottleneck under mobile throttling. Always run both; don't stop after one just because it looks fine.

## Step 1 — Run the audits

```bash
lighthouse <PAGE_URL> \
  --output=json \
  --output-path=./lighthouse-mobile.json \
  --form-factor=mobile \
  --only-categories=performance,accessibility,best-practices,seo,agentic-browsing

lighthouse <PAGE_URL> \
  --output=json \
  --output-path=./lighthouse-desktop.json \
  --preset=desktop \
  --only-categories=performance,accessibility,best-practices,seo,agentic-browsing
```

Run these from the repo root so the JSON files land next to each other and are easy to diff across runs. If files from a previous audit already exist, that's fine — they'll just be overwritten; no need to ask before overwriting your own tool output in the working tree (this is different from overwriting the user's uncommitted work).

## Step 2 — Summarize, don't read raw

These reports are commonly 10,000-20,000 lines of JSON. Reading them directly with `Read` wastes most of the context window on data you won't use. Use the bundled script instead:

```bash
python3 .claude/skills/lighthouse-audit/scripts/summarize_report.py lighthouse-mobile.json
python3 .claude/skills/lighthouse-audit/scripts/summarize_report.py lighthouse-desktop.json
```

This prints category scores, the core metrics (FCP, LCP, TBT, CLS, Speed Index, TTI), ranked opportunities (with estimated savings), and every failing binary audit (accessibility/best-practices/SEO issues) — everything you need for a first pass, in well under 100 lines.

Once you've identified which metric is the actual problem (usually LCP or TBT on mobile), re-run with `--full` to pull the deeper diagnostic detail for that one report:

```bash
python3 .claude/skills/lighthouse-audit/scripts/summarize_report.py lighthouse-mobile.json --full
```

`--full` adds: the LCP element and its discovery/breakdown timing (which phase — TTFB, resource load delay, resource load duration, or render delay — is actually slow), CLS culprit elements, render-blocking requests, the network dependency (critical request chain) tree, unused JavaScript per-file, console errors, and accessibility label-mismatch details. Only pull this for the report(s) where it's actually needed — don't reflexively dump `--full` for both mobile and desktop if desktop already looks healthy.

If you need a field the script doesn't expose, read it directly with a scoped one-liner (`python3 -c "import json; d=json.load(open('lighthouse-mobile.json')); print(json.dumps(d['audits']['<audit-id>'], indent=2))"`) rather than opening the whole file — the `audits` object is keyed by audit id, and `report['audits'].keys()` lists everything available if you're not sure of the id.

Lighthouse versions differ in which audits they emit — newer versions replace some legacy audits (e.g. `render-blocking-resources`) with "Insight" versions (e.g. `render-blocking-insight`). The script checks both; if it comes back empty for something you expected, list `audits.keys()` and grep for the concept (`lcp`, `cls`, `render-blocking`, `network`) to find the current name before concluding the data isn't there.

## Step 3 — Diagnose against the actual codebase, not generic advice

This is the part that makes the plan useful instead of a Lighthouse advice regurgitation. For every finding worth fixing:

1. **Find the real cause in source.** A "reduce unused JavaScript" finding on a Gatsby site usually traces to a specific heavy import (a chart/animation library pulled in for one component, a dependency that ships an unminified build) — grep for the file the opportunity's `items` point at, or check `gatsby-browser.js` / `gatsby-ssr.js` / page-level imports. An LCP `elementRenderDelay` finding traces to what's blocking that element from painting — check if it's behind client-side data fetching, a heavy hero animation, or a large unoptimized image (check `gatsby-plugin-image` usage, image dimensions, format).
2. **Confirm the file and line.** Every issue in the fix plan must cite `path/to/file.tsx:123`, not "somewhere in the hero section." If you can't pin it down with grep/read, say so in the plan rather than guessing.
3. **Check whether it's a false positive or a genuine issue given this project's constraints.** E.g. a `best-practices` warning about a third-party script (analytics, fonts) might be an accepted tradeoff already made deliberately — note that rather than proposing to rip it out uncritically.

## Step 4 — Write the fix plan

Write `lighthouse-fix-report-plan.md` at the repo root (sibling to the `lighthouse-*.json` files). Use this structure — it's designed so a plan can be picked up and executed later with zero extra context, by a different session:

```markdown
# Lighthouse Audit — <URL> — <date>

## Scores

| Category       | Mobile | Desktop |
| -------------- | ------ | ------- |
| Performance    | 0.56   | 0.74    |
| Accessibility  | 1.00   | 1.00    |
| Best Practices | 0.96   | 0.96    |
| SEO            | 1.00   | 1.00    |

## Core metrics

| Metric      | Mobile | Desktop |
| ----------- | ------ | ------- |
| FCP         | 4.7s   | 1.0s    |
| LCP         | 18.5s  | 3.5s    |
| TBT         | 60ms   | 50ms    |
| CLS         | 0.001  | 0.015   |
| Speed Index | 14.5s  | 2.5s    |
| TTI         | 19.8s  | 3.7s    |

## Findings

### N. <Short imperative title>

- **Severity**: HIGH | MEDIUM | LOW (based on score impact and how far the metric is from Lighthouse's "good" threshold, not just presence of a finding)
- **Where**: `path/to/file.tsx:123`
- **Lighthouse evidence**: <the specific audit/metric and number that flags this>
- **Root cause**: <what's actually happening in this codebase, verified by reading the source — not generic Lighthouse copy>
- **Fix**: <the concrete change — file, what changes, resulting behavior>
- **Expected impact**: <rough — e.g. "removes a synchronous 2s render delay from the LCP image">

... one finding per issue worth fixing, ordered by severity ...

## Not fixing

<Findings that are false positives, accepted tradeoffs, or too low-impact to justify — say why, so nobody re-raises them next audit.>
```

Order findings by real-world impact: a metric far outside Lighthouse's "good" range (e.g. LCP > 4s is "poor"; the reference thresholds are FCP ≤1.8s good/>3s poor, LCP ≤2.5s good/>4s poor, TBT ≤200ms good/>600ms poor, CLS ≤0.1 good/>0.25 poor) outranks a cosmetic accessibility nit, even if both show up as "failing audits."

## Step 5 — Ask before fixing

Once the plan is written, ask the user whether to fix the issues now or leave the plan for later — don't start editing source files without that confirmation. If they say now, work through the plan's findings in severity order, verifying each fix with `bun run typecheck` and (for anything visual) the dev server, per this repo's [CLAUDE.md](../../../CLAUDE.md) conventions. If they say later, you're done — the plan file is the handoff artifact.
