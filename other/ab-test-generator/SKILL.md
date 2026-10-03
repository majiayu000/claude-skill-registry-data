---
name: ab-test-generator
description: "Reads page analytics and click data from Humblytics, generates A/B test hypotheses with element selectors, and launches no-code split tests via the Humblytics MCP. Use when creating A/B tests, split tests, multivariate tests, or when you need to test headlines, CTAs, layouts, or pricing. Triggers: A/B test, split test, experiment, test hypothesis, launch test, variant."
metadata:
  version: 1.0.0
  author: Humblytics
---

# A/B Test Generator

## Purpose

Generate data-driven A/B test configurations from Humblytics analytics and heatmap data. This skill creates complete test definitions including hypotheses, variant specifications with CSS/element selectors, success metrics, sample size requirements, and can launch tests directly through the Humblytics MCP.

Live data comes from the Humblytics MCP (server `humblytics`) — read tools like `get_page_details`, `get_clicks_details`, and `get_split_test_recommendations`, and write tools like `create_split_test`, `update_split_test`, and `stop_split_test`.

## When to Use

- Creating A/B tests from conversion data or heatmap insights
- Generating test hypotheses for a specific page or funnel step
- Launching no-code split tests via the Humblytics MCP
- Calculating required sample size and test duration
- Designing multivariate test matrices
- Reviewing and iterating on existing test results

## Setup

This skill calls the Humblytics MCP (server `humblytics`) for all live data and test launches — connect it once and the MCP handles auth, base URL, and property resolution. See the repo README for connection steps. The skill then calls `mcp__humblytics__*` tools directly; there is no per-run key to export.

Keep the security ethos: **never paste API keys directly into chat** and never commit a `.env` — the key now lives in the MCP connection headers, set once. For a single-property key the MCP auto-resolves the property; for a multi-property key call `list_properties` and pass the `propertyId` you want.

## Before You Start

1. **Confirm property and page** — Which page URL to test (the MCP resolves the property; use `list_properties` only for multi-property keys)
2. **Pull current data** — Retrieve page analytics, click data, and current conversion rate via the MCP
3. **Check existing tests** — Look for any running tests to avoid conflicts (`list_split_tests`)
4. **Understand the goal** — What is the primary conversion action on this page?
5. **Verify traffic volume** — Ensure enough traffic for statistical significance within a reasonable timeframe
6. **Check for context** — Look for product briefs, AGENTS.md, or existing CRO documents that inform test direction

## Core Workflow

### Step 1: Gather Page Intelligence

Pull data from Humblytics:

- **Page analytics**: Traffic volume, bounce rate, time on page, scroll depth
- **Heatmap data**: Click maps, scroll maps, attention maps
- **Event data**: CTA clicks, form interactions, video plays
- **Device split**: Mobile vs desktop behavior differences
- **Source split**: How different traffic sources behave on this page

MCP tools (analytics reads take `start`, `end` (ISO-8601), and `timezone`):
- `get_page_details` (page param) — Single-page deep dive (UTM, device, country, scroll depth, bounce)
- `get_clicks_details` (page param) — Click data with UTM attribution (there is no heatmap endpoint; click data is the closest analogue)
- `get_forms_details` (page param) — Form submissions and conversion rates for that page (no generic events tool exists)
- `list_split_tests` — List existing experiments. Optionally filter by status (`active`/`complete`)

### Step 2: Identify Test Opportunities

Analyze the data for signals:

**High-value signals from heatmaps:**
- Users clicking non-clickable elements (rage clicks) — make them clickable or remove confusion
- Low scroll depth — critical content is below the fold, move it up
- CTA getting few clicks despite visibility — copy, color, or placement issue
- Form field abandonment — simplify or reorder fields
- Dead zones — large page areas with no interaction

**High-value signals from analytics:**
- High bounce rate from specific sources — message mismatch
- Mobile conversion significantly lower than desktop — responsive layout issue
- High time-on-page but low conversion — users are interested but not persuaded
- Low time-on-page and low conversion — page fails to engage

### Step 3: Formulate Hypotheses

For each opportunity, create a structured hypothesis:

```
Test Name: [descriptive-slug]
Page: [URL]
Hypothesis: IF we [specific change], THEN [primary metric] will [direction]
            BECAUSE [evidence from data]

Control: [current state description]
Variant: [proposed change description]

Primary Metric: [conversion event or goal]
Secondary Metrics: [engagement metrics to monitor]

Element Selector: [CSS selector for the element to modify]
Change Type: [text | style | visibility | layout | redirect]
```

### Step 4: Calculate Sample Size and Duration

For each test, calculate statistical requirements:

**Inputs needed:**
- Baseline conversion rate (from current analytics)
- Minimum detectable effect (MDE) — typically 10-20% relative lift
- Statistical significance level — default 95%
- Statistical power — default 80%

**Sample size formula (per variant):**
```
n = (Z_alpha/2 + Z_beta)^2 * (p1(1-p1) + p2(1-p2)) / (p2 - p1)^2
```

**Duration estimate:**
```
Days = (n * number_of_variants) / daily_traffic_to_page
```

Present this clearly:
- Required sample per variant
- Total sample needed
- Estimated days to reach significance at current traffic
- Recommendation: proceed, increase traffic first, or test a larger change

### Step 5: Define Test Configuration

Create the test spec and pass it as the `create_split_test` tool input. The required shape is:

```json
{
  "name": "descriptive-test-name",
  "page": "/pricing",
  "type": "a_b",
  "variants": [
    { "label": "control", "is_control": true, "changes": [] },
    {
      "label": "variant-a",
      "changes": [
        {
          "selector": "#hero-cta",
          "attribute": "textContent",
          "value": "See Your Analytics"
        }
      ]
    }
  ],
  "goal": "form_submission",
  "auto_stop_days": 30
}
```

Required fields: `name`, `page`, `type` (use `"a_b"` for selector-based tests; valid enum: `a_b`, `component_a_b`, `multivariate`, `component_multivariate`), `variants` (each with `label` + `changes`). Mark the control variant with `is_control: true` rather than relying on a magic label value like `"control"`.
Optional: `goal` (primary conversion event), `auto_stop_days` (auto-end the test after N days, 1–30).

`goal` enum: `click_through`, `form_submission`, `bounce_rate`, `session_time`, `destination_page`, `external_destination`, `revenue`. A plain "conversion" goal maps to `form_submission`. The `revenue` goal requires a connected revenue source (e.g. a Stripe/revenue connector) — don't select it unless revenue tracking is live for the property.

> **TBD — confirm the `changes[]` schema against a live `create_split_test` call.** This skill documents `attribute: "textContent"`, but some tooling uses `op: "text"`. The exact shape (`attribute` vs `op`, and the allowed values) has not been verified against a live create here — treat it as unconfirmed and validate before relying on it.

### Step 6: Launch or Document

**To launch via the MCP:**
- `create_split_test` — Create and start the test (input shape above)
- `get_split_test` (id) — Experiment details with per-variant metrics inline (no separate results call — variant metrics come back in the same response). Only act on a variant once its confidence is >= 70.
- `update_split_test` (id) — Update an active experiment. Input: `{ "name": "...", "auto_stop_days": N }` (1–30)
- `stop_split_test` (id) — Stop a running experiment. Input: `{ "reason": "..." }`
- `get_split_test_recommendations` (page param) — AI-generated split-test suggestions for a page

**To document for manual launch:**
- Output the full test specification
- Include screenshot annotations if click-data informed the test
- Provide the hypothesis document for the team

## Test Type Selection Guide

| Scenario | Test Type | Notes |
|----------|-----------|-------|
| One element change | A/B test | Fastest to significance |
| Two element changes | A/B/C test | Test both independently |
| Multiple interacting elements | Multivariate | Needs 4x+ traffic |
| Completely different page | Split URL test | Redirect-based |
| Copy variations only | A/B test | Quick wins |
| Layout restructure | Split URL test | Build separate variant page |

## Common Test Categories

### Headlines and Copy
- Value prop rewording
- Specificity (add numbers, timeframes, outcomes)
- Emotional vs rational framing
- Length (short punchy vs detailed)

### CTAs
- Button text (action verbs, benefit language, urgency)
- Button color and size
- Button placement (above fold, after social proof, sticky)
- Single CTA vs multiple CTAs

### Social Proof
- Testimonials vs logos vs metrics
- Placement (near CTA vs header vs throughout)
- Specificity (named customers vs anonymous)

### Layout and Structure
- Long page vs short page
- Information hierarchy reordering
- Form length and field order
- Navigation presence vs removal

### Pricing
- Price anchoring (show higher price first)
- Plan naming
- Feature comparison layout
- Free trial vs freemium vs demo

## Avoiding Common Mistakes

1. **Testing too small a change** — If your MDE requires 50,000 visitors per variant, the change is too subtle. Test bolder.
2. **Running too many tests on one page** — Interaction effects corrupt results. One test per page at a time.
3. **Stopping early on positive results** — Peeking inflates false positives. Commit to the sample size.
4. **Ignoring secondary metrics** — A variant that increases signups but increases churn is not a win.
5. **Not segmenting results** — A test can be flat overall but show strong wins on mobile. Always segment.

## Output Format

For each generated test, present:

1. **Hypothesis** — One sentence: IF/THEN/BECAUSE
2. **Evidence** — What data supports this test
3. **Variants** — Control and variant descriptions
4. **Selectors** — CSS selectors and exact changes
5. **Metrics** — Primary and secondary goals
6. **Duration** — Estimated days to significance
7. **Expected Impact** — Projected conversion lift range

## Related Skills

- **cro-optimizer** — Identify which pages and funnel steps need testing
- **page-cro** — Deep page-level audit to inform test hypotheses
- **copywriting** — Generate high-quality copy variants for tests
- **funnel-reporter** — Track how test results affect downstream funnel metrics

## Shared Frameworks (REQUIRED reading)

Test design without grounding in base rates produces overconfident projections. Read these before generating test configs.

- **`_shared/frameworks/base-rate-priors.md`** — load-bearing for this skill. Anchor expected impact against:
  - **Only ~14% of CTA tests reach significance** (VWO/Wingify 2023 across thousands of tests)
  - **~31% of headline rewrites beat control** (73-test study)
  - Avg lift when a test wins: +49% — but most tests don't win
  - If you propose 10 tests, expect 2–3 to win meaningfully. Frame the roadmap that way.
- **`_shared/frameworks/ice-confidence-rubric.md`** — anchor Confidence on evidence quality from `_shared/benchmarks/patterns.json`, not on test-designer enthusiasm. 9–10 requires ≥2 independent sources with n≥1000 in the target vertical.
- **`_shared/frameworks/anti-patterns.md`** — critical pitfalls when designing tests:
  - **"Always multi-step" forms**: Baymard 2024 — step count exerts substantially less impact than total field count. A 15-field three-step form is worse than an 11-field three-step. Reduce fields BEFORE proposing step splits.
  - **Bundled changes masquerading as a single test**: a "headline" test that also moves the sub-headline, image, and CTA isn't a headline test. Strict isolation matters when projecting future lift.
  - **Underpowered tests stopped at the first peak**: regression-to-mean is severe in low-sample tests. Hold to the pre-computed sample size.
- **`_shared/benchmarks/patterns.json`** — when generating a test config, find the matching `pattern_id` and use the evidence-backed `lift_range_pct` as the basis for the Expected Impact field. Don't quote the +260% Docsend outlier — quote the median.
