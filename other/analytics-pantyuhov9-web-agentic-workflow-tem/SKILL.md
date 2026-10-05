---
name: analytics
description: Website analytics audit — tracking verification, SEO check, performance metrics, conversion path analysis
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Agent
  - TodoWrite
  - WebSearch
  - WebFetch
model: opus
argument-hint: <"tracking" | "seo" | "performance" | "full"> [path to site root]
---

# Site Analytics — tracking, SEO, and performance audit

You are running the `analytics` skill. Your job: audit a website's analytics implementation, SEO health, or performance, then help the user pick ONE thing to fix.

## Architecture

**Layer 1 (deterministic Python):** `python3 tools/site_analytics.py --root <path> --mode <mode>` — scans HTML files for tracking IDs, SEO tags, and performance signals. Generates `.tmp/site_analytics_map.json`.

**Layer 2 (Opus subagent):** For `seo` and `full` modes, spawn an Explore subagent to check live indexation and competitive signals via WebSearch.

## Step-by-step

### Step 0 — Parse arguments

Parse `$ARGUMENTS` for the mode and optional path:
- First word should be one of: `tracking`, `seo`, `performance`, `full`
- Remaining text is the site root path
- Default mode: `full`. Default path: current working directory (else ask for the site root)

### Step 1 — Run Layer 1

```bash
python3 tools/site_analytics.py --root "<site_root>" --mode <mode>
```

### Step 2 — Layer 2 (SEO and full modes only)

For `seo` or `full` modes, spawn an Explore subagent:

```
subagent_type: "Explore"
model: "opus"
description: "Layer 2 SEO analysis"
```

The subagent should:
1. Read `.tmp/site_analytics_map.json`
2. Use WebSearch to check: `site:<domain>` indexation, search for the site's target keywords
3. Assess whether structured data meets Google Rich Results requirements
4. Return findings in the standard format:

```
[CONCEPTUAL] <category>
    <path>
    → <description>
    Fix: <fix>
```

### Step 3 — Combine and present

Same format as `site-audit`: numbered findings list, user picks ONE.

### Step 4 — Wait, then fix ONE

Same discipline: one fix per invocation.

## Mode details

- **tracking** — GA4/Pixel/Clarity ID consistency, duplicate init, CAPI presence, consent banner
- **seo** — sitemap, robots.txt, canonical, JSON-LD, title/description quality and uniqueness
- **performance** — page weight, external requests, render-blocking scripts, image optimization, preconnect
- **full** — all three combined

## See also

- [tools/site_analytics.py](../../../tools/site_analytics.py)
- [workflows/site_analytics.md](../../../workflows/site_analytics.md)
