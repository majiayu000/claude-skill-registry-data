---
name: heatmap-analyst
description: "Click-engagement analyst that pulls element-level click data, a page-level scroll proxy, and bounce/exit signals from Humblytics to surface UX friction and ignored CTAs. Generates prioritized, data-backed optimization recommendations. NOTE: Humblytics does NOT provide pixel-level click heatmaps, scroll-depth distributions, or rage-click detection — those need a dedicated heatmap tool. Use when auditing element-level click patterns, finding ignored CTAs, gauging scroll engagement, or diagnosing on-page friction. Triggers: click analysis, element clicks, ignored CTA, click engagement, scroll engagement, UX friction, interaction audit."
metadata:
  version: 1.0.0
  author: Humblytics
---

# Heatmap Analyst

## Purpose

Analyze Humblytics click-engagement data (element/target-level clicks, a single page-level scroll proxy, and bounce/exit signals) to diagnose UX friction and generate prioritized design recommendations. Live data comes from the Humblytics MCP (the click and page tools — `get_clicks_details`, `get_clicks_breakdown`, `get_page_details`, `get_pages_breakdown`, `get_entry_exit_pages`). This skill turns the interaction data Humblytics actually exposes into specific, ranked improvements for layout, CTAs, and content hierarchy.

> **Scope note — what Humblytics does and does not give you.** Humblytics provides **element/target-level click counts** (with UTM breakdown), a **single average scroll percentage** per page, and **bounce/exit** signals. It does **NOT** provide pixel-level click heatmaps (x/y coordinates), a 25/50/75/100 scroll-depth distribution, rage-click detection, dead-zone maps, or per-device click segmentation. Anything in that second list requires a dedicated heatmap tool (e.g. Hotjar, Microsoft Clarity) — do not promise it from Humblytics. See **"NOT available via Humblytics"** below.

## When to Use

- A page has a high bounce rate and you need to understand *why*
- CTAs are present but click-through rate is below benchmark
- You want to verify that the important content is actually being seen
- Users are reporting confusion or friction on a specific page
- You're auditing a page before a redesign or A/B test
- Investigating whether traffic from a specific source behaves differently on-page

## Setup

This skill reads live data through the **Humblytics MCP** (server `humblytics`) — see the repo README to connect it. Once connected, the skill calls `mcp__humblytics__*` tools; the MCP handles auth, base URL, and property resolution, so there are no keys to paste or `.env` files to source here. **Never paste API keys into chat** — the key lives once in the MCP connection headers, not in transcripts.

The MCP auto-resolves the property for a single-property key (the common case). For a multi-property key, call `list_properties` and pass the chosen `propertyId` to each tool.

## Before You Start

1. **Confirm the property** — With a multi-property key, run `list_properties` and confirm which property to analyze (single-property keys auto-resolve)
2. **Identify the target page(s)** — Which URL(s) are in scope
3. **Time range** — Default to last 30 days; shorter windows are noisier
4. **Sample size check** — Pages below ~500 sessions in the window produce unreliable heatmaps
5. **Context** — Pull product/persona context if available so recommendations match the audience

## Core Workflow

### Step 1: Pull the Interaction Data

For each target page, fetch what the API actually returns:

- **Element-level clicks** — clicks grouped by element `target` (and `secondary`), with `clicks`, `unique_sessions`, `most_recent`, a per-element `trend`, and a `utm_breakdown` (clicks + share by UTM source/medium/campaign). This is element-level, **not** an x/y coordinate map.
- **Scroll proxy** — a single `avg_scroll_percent` for the page (one number, e.g. 23.7), plus `bounce_rate`, `page_views`, `unique_visitors`, `avg_session_length`. This is **not** a 25/50/75/100 depth distribution.
- **Cross-page click comparison** — per-page `total_clicks`, `unique_sessions`, and `top_targets[]{target, clicks, share}`.
- **Entry/exit friction** — entry and exit pages as a friction proxy.

> Click **CTR is not a field** in the API — derive an engagement rate yourself as `clicks / unique_sessions` (or per-page `top_target.share`) when you need a CTR-like proxy.

Relevant Humblytics MCP tools (all take `start`, `end` as ISO-8601 and a `timezone` IANA name — there is no `?period=` shorthand; scroll depth lives in the page tools):
- `get_clicks_details` (`page: "/path"`) — element/target-level clicks + UTM breakdown for one page
- `get_clicks_breakdown` — cross-page top targets
- `get_page_details` (`page: "/path"`) — `avg_scroll_percent` (scroll proxy) + `bounce_rate` for one page
- `get_pages_breakdown` — page-level views/bounce across pages
- `get_entry_exit_pages` — entry/exit friction proxy

> **NOT available via Humblytics (needs a dedicated heatmap tool):** pixel-level click coordinate heatmaps, scroll-depth distribution (25/50/75/100%), rage-click detection, dead-zone maps, and per-device click segmentation. If the user needs any of these, tell them Humblytics does not return them and point to a purpose-built heatmap tool (Hotjar, Microsoft Clarity, etc.).

### Step 2: The Three Diagnostic Questions

Run each page through these three questions, using only data the API returns:

**Q1 — Are visitors clicking what you *want* them to click?**
- Primary CTA click share: is the CTA `target` a meaningful fraction of `total_clicks` (use its `share` from `get_clicks_breakdown` or `clicks` from `get_clicks_details`)?
- Secondary CTA click share: proportional to its importance?
- Which `target` dominates clicks, and is it a high-value action or a low-value/navigation element?

**Q2 — Are visitors engaging deeply enough to *see* the important content?**
- `avg_scroll_percent`: a low average (e.g. ~24%) suggests most visitors never reach below-fold content. This is a single average, **not** a depth distribution — do not claim "X% reached 50%".
- Is the primary CTA likely above or below where that average scroll lands?
- Cross-reference with `bounce_rate` from `get_page_details`.

**Q3 — Where is the friction?**
- High `bounce_rate` / exit share (from `get_page_details` and `get_entry_exit_pages`) on a page that should convert = friction proxy.
- Low scroll engagement on a long page where the CTA sits deep.
- A CTA `target` that gets almost no clicks despite high page views = ignored CTA.

> Frustration signals like rage clicks and clicks on non-interactive elements are **not** available from Humblytics — use the friction proxies above, and recommend a dedicated heatmap/session-replay tool if true rage-click detection is needed.

### Step 3: Identify the Top 3 Issues

Rank all issues by **expected conversion impact**:

1. **Blocker** — Primary CTA gets a negligible share of clicks, or low `avg_scroll_percent` suggests core content is rarely reached
2. **Friction** — High `bounce_rate` / exit share on a page meant to convert; confusing affordances
3. **Waste** — High click share on low-value elements (e.g., a `Link`/nav target dominating clicks instead of the CTA)

Always state the evidence: *"avg_scroll_percent on the homepage is 24% and bounce_rate is 0.89, while the signup CTA `hero-try-free` took only 1.2% of clicks."*

### Step 4: Generate Recommendations

For each issue, provide:

- **Specific change** — "Move CTA from below the pricing table to above the hero fold"
- **Expected lift** — Estimate based on traffic volume and issue severity
- **Implementation difficulty** — Copy change / layout change / redesign
- **How to verify** — Which metric to watch; which follow-up A/B test validates the fix

### Step 5: Output Format

Write a clean report with:

```
PAGE: [/path]
DATE RANGE: [window]
PAGE VIEWS / UNIQUE VISITORS: [page_views] / [unique_visitors]

HEADLINE FINDING:
[1 sentence capturing the biggest insight]

CLICK PATTERN SUMMARY (from get_clicks_details + get_clicks_breakdown):
- Primary CTA target + click share: [target] ([share]% of clicks)
- Highest-click element: [target] ([share]% of clicks)
- Total clicks / unique sessions: [total_clicks] / [unique_sessions]
- Notable UTM skew (if any): [utm_source/medium] drives [share]% of a target's clicks

SCROLL ENGAGEMENT (from get_page_details — single average, not a distribution):
- avg_scroll_percent: [N]%
- Implication: [most visitors likely do / do not reach below-fold content]

FRICTION PROXIES:
- bounce_rate: [N]
- Top exit pages (get_entry_exit_pages): [pages]

TOP 3 RECOMMENDATIONS (prioritized):
1. [Change] — Expected impact: [X] — Difficulty: [level]
2. [Change] — Expected impact: [X] — Difficulty: [level]
3. [Change] — Expected impact: [X] — Difficulty: [level]

SUGGESTED A/B TESTS:
- [Test hypothesis with clear control vs variant]
```

## Interpretation Cheatsheet

Based only on Humblytics-available signals (element-level click shares, single `avg_scroll_percent`, `bounce_rate`/exit):

| Pattern | Likely Cause | Action |
|---------|--------------|--------|
| A generic `Link`/nav `target` dominates clicks, CTA `target` near zero | CTA invisible, weak, or out-competed by navigation | Strengthen CTA prominence; reduce competing links |
| Low `avg_scroll_percent` on a long page | Weak hook, above-fold doesn't earn attention | Rewrite headline or move proof/CTA above the fold |
| CTA clicks concentrated on one variant | Other CTAs are invisible or redundant | Remove redundant CTAs; test single CTA variant |
| High `bounce_rate` + low scroll on a convert-intent page | Above-fold fails to engage | Audit hero copy/offer; move value prop up |
| Click share spread thinly across many targets | No clear visual hierarchy | Add hierarchy: emphasize primary action |
| One UTM source's clicks skew heavily to a low-value target | Mismatched intent from that channel | Align landing experience to that source's intent |

> Patterns that require pixel coordinates, rage-click detection, or per-device click maps (e.g. "rage clicks on image", "desktop clicks ≠ mobile clicks") are **not** diagnosable from Humblytics — use a dedicated heatmap tool.

## Related Skills

- `cro-optimizer` — Combines heatmap findings with funnel data for holistic CRO
- `page-cro` — Full 10-point page audit; heatmap analysis is one dimension
- `ab-test-generator` — Takes heatmap recommendations and launches them as tests

## Shared Frameworks (REQUIRED reading)

Heatmap interpretation is highly context-dependent. The shared primitives in `skills/_shared/` keep recommendations grounded.

- **`_shared/frameworks/preflight-checklist.md`** — confirm minimum 500 sessions per page-period combo before drawing conclusions. Heatmap patterns on smaller samples are noise.
- **`_shared/frameworks/anti-patterns.md`** — heatmap-relevant counter-evidence:
  - **Mobile hamburger menu**: NN/g says it hurts discoverability on task-oriented SaaS (Spotify hamburger → bottom-tab = +30% menu interactions). **BUT** Amazon's hamburger beat dropdown for browse-heavy ecom. Site_type is load-bearing — don't recommend bottom-tab universally.
  - **Mobile exit-intent**: architecturally broken (no cursor → no mouseleave event). If heatmap shows users leaving on mobile, the answer is not an exit modal.
  - **Progress-bar velocity**: NIH RCT shows slow-to-fast progress bars nearly double form abandonment. If your heatmap shows form-step drop-off, audit progress bar acceleration before redesigning fields.
- **`_shared/benchmarks/patterns.json`** — when heatmap data confirms a problem (e.g., low scroll past 30%, CTA clicks dominated by a single variant), match to a `pattern_id` and quote the evidence-backed lift range for the fix. Most relevant categories: `cta`, `navigation`, `above_fold`.
