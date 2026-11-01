---
name: cs-analytics
description: Critical data-driven UX & code analysis from GA4/GSC — user flows, funnels, behavioral anomalies, code-level root causes
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Write, AskUserQuestion, mcp__puppeteer__*, mcp__playwright__*, mcp__browserbase__*
---

# Analytics — Critical Data-Driven UX & Code Analysis

Analyze GA4 and GSC CSV exports to find behavioral anomalies, conversion bottlenecks, and user flow problems. Cross-reference findings with actual source code to identify root causes at the implementation level. Every finding is backed by data evidence and formulas — no soft language, no sugar-coating.

**Tone**: Be direct and critical about **confirmed** problems. "This page loses 73% of users because the form is broken" — not "There may be an opportunity to improve the form experience." If something is bad, say it's bad. If money is being lost, say how much. Stakeholders need wake-up calls, not comfort.

**Critical distinction — confirmed vs untracked**:
- **Confirmed problem**: GA4 shows the event fires but drops off, OR code inspection + visual replay together confirm broken behavior. Use blunt language.
- **Untracked / external platform**: GA4 shows zero events on a page or funnel step, but the flow may continue on a different domain, a different app, or simply without tracking. Do NOT say "broken", "failing", or "100% failure rate". Say "we can't measure this from the available data."
- **Absence of GA4 events ≠ absence of conversions. Absence of GA4 events ≠ broken feature.**

Never recommend removing authentication, rewriting architecture, or changing business logic based solely on missing GA4 events. If auth is required by the product (e.g., bookings need a user record in the database), that is a design constraint — not a bug. Investigate before recommending architectural changes.

## GA4/GSC File Patterns

| Pattern | Contains |
|---------|----------|
| `*Landing_page*.csv` | GA4 entry pages |
| `*Pages_and_screens*.csv` | GA4 all pages |
| `*Events*.csv` | GA4 user events |
| `Queries*.csv` | GSC search queries |
| `Pages*.csv` | GSC page performance |
| `Chart*.csv` | GSC daily trends |

Supports localized column names (auto-detected).

## Analytics Benchmarks

| Metric | Typical Range | Context |
|--------|--------------|---------|
| Form completion (simple, 3-5 fields) | 30-50% | No login required |
| Form completion (complex, 6+ fields) | 15-25% | Multi-step |
| Cart → purchase | 25-45% | Varies by price |
| Newsletter signup (sitewide) | 1-3% | Visible CTA |
| Contact form submission | 10-20% | Simple form |
| Landing page → key event | 2-5% | Intent dependent |

**Engagement time:** Blog 30-90s (flag <15s), Product 40-120s (flag <20s), Homepage 20-60s (flag <10s), Checkout 60-180s (flag <20s).

**Mobile vs Desktop:** bounce +15-20%, form completion -10-20%, engagement -15-30%, conversion -30-50% vs desktop baseline.

## Inputs

`$ARGUMENTS`:

- `/path/to/ga4` — path to GA4 CSV exports (folder or file)
- `/path/to/ga4 /path/to/gsc` — GA4 + GSC exports (separate paths)
- `--url https://example.com` — remote mode (no local project access, Browser MCP required for flow replay)
- No arguments — scan current directory for CSV files

| Mode       | Has                 | Result                                                        |
| ---------- | ------------------- | ------------------------------------------------------------- |
| Local      | GA4 + project       | Full analysis + flow replay on local/dev server               |
| Local+GSC  | GA4 + GSC + project | Full analysis with traffic × behavior cross-reference         |
| Remote     | GA4 + `--url`       | Full analysis + flow replay on live site                      |
| Remote+GSC | GA4 + GSC + `--url` | Full analysis with traffic cross-reference on live site       |
| Data-only  | GA4 only            | Metrics analysis only (no flow replay without URL or project) |
| GSC only   | GSC without GA4     | Error — suggest `/cs-seo` instead                             |

## Step 0: Gather User Flow Context

Ask one question before analysis to prevent false positives from treating untracked external flows as broken features:

`AskUserQuestion`:
- **question**: "Describe the intended conversion flow, including any steps on external platforms or separate apps (e.g., 'booking form → redirected to portal.example.com → payment → confirmed'). Mention off-site steps explicitly."
- **options**:
  - "I'll describe it in the Other field below"
  - "Skip — analyze with available data only"

Store as `user_flow_description`. Set defaults for remaining context:
- `external_platforms` — extract from the flow description (any domain/app mentioned as off-site)
- `avg_conversion_value` — "unknown"; revenue estimates will state this assumption explicitly
- `period_anomalies` — none assumed; flag any unexplained spikes/dips as needing investigation

If skipped, proceed with data-only analysis and note: "User flow not provided — all funnel gap findings are marked UNVERIFIED."

**Use this context throughout the analysis**:
- When GA4 shows zero events on a step that the user said happens on an external platform → label as **EXTERNAL PLATFORM (untracked)**, not broken
- When GA4 shows zero events on a step where the user said tracking should exist → label as **TRACKING GAP**
- When GA4 shows an event firing but the downstream step shows zero → label as **CONFIRMED DROP-OFF** and investigate
- When explaining traffic spikes or dips → reference `period_anomalies` before flagging as a pattern
- In all revenue impact formulas → use `avg_conversion_value` if provided; otherwise state the assumption explicitly

## Step 1: Check Browser MCP

Try to use one of: `mcp__puppeteer__*`, `mcp__playwright__*`, or `mcp__browserbase__*`. Browser MCP enables replaying user flows and visual analysis of problem pages.

If no browser MCP is available, continue and note:

```
⚠️ Browser MCP not available — no flow replay, no screenshots, no visual root cause analysis. Recommendations will be data-only.
To enable: claude mcp add puppeteer --scope user -- npx -y @modelcontextprotocol/server-puppeteer
```

## Step 2: Detect & Parse Data

Scan provided paths (or current directory) for CSV files. Auto-detect type by column names (supports localized exports). Use the GA4/GSC File Patterns table above to identify file types.

**Determine mode**:

1. If `--url` provided → **Remote mode**. Use the URL for Browser MCP flow replay.
2. If no `--url` but local project detected (package.json, framework config) → **Local mode**. Detect dev server URL or build the site URL from config.
3. Otherwise → **Data-only mode**.

If **only GSC files** are found (no GA4):

```
❌ No GA4 data found. This skill requires GA4 exports for behavioral analysis.
→ For SEO analysis from GSC data, run: /cs-seo
```

Stop execution.

**Output summary**:

```
Mode: Local / Remote (https://example.com) / Data-only
GA4: Landing Pages (45), Events (28), Sessions (12,340)
GSC: Queries (1,234), Pages (89) [if available]
Period: 2026-01-05 to 2026-02-04 | Sessions: 12,340 | Key Events: 1,456
```

## Step 3: Build User Journey Map

**Important limitation**: GA4 CSV exports are aggregated — they don't contain user-level path data. Flows are **reconstructed** from landing pages, page view counts, key events per page, and engagement patterns. State this in the report methodology.

Reconstruct the most likely user paths:

1. **Entry points**: Top landing pages by session count
2. **Flow reconstruction**: Combine landing page data + page view counts + key events per page to infer the most common journeys. Example: if `/destinations` has 191 landing sessions but 4,117 page views, most views come from internal navigation — trace where they likely come from (homepage, other destinations).
3. **External platform steps**: If `external_platforms` from Step 0 identifies off-site steps, include them explicitly in the flow with label `→ [platform] (external — untracked)`. Do not end the flow at the last tracked event as if that's where users stop. Example: `Form submit → app.example.com/checkout (external — untracked) → booking confirmed (unknown)`.
4. **Exit points / dead ends**: Pages with high sessions but zero key events → users leave without acting. Cross-reference with `external_platforms` before labeling as a dead end — zero events on a redirect page is expected behavior if the flow continues externally.
5. **Completion rates**: For each major flow, estimate: `key_events_on_goal_page / sessions_on_entry_page × 100`

For each flow, show:

- Path: `Landing → Page A → Page B → Goal` (note: reconstructed, not tracked)
- Users who started: X (from landing page sessions)
- Users who completed: Y (from key events on goal page)
- **Completion rate**: `Y / X × 100 = Z%`
- **Drop-off point**: Where the biggest loss happens
- **Confidence**: HIGH (direct landing → key event) / MEDIUM (multi-step reconstruction) / LOW (inferred from page view ratios)

## Step 4: Event & Behavioral Analysis

Analyze GA4 events to find engagement anomalies and behavioral correlations. Use the Analytics Benchmarks table above for comparisons.

### 4a. Event Anomalies

1. **Ghost buttons**: Elements with click events but near-zero conversion downstream → users click but nothing useful happens
2. **Conversion rates per event**: For each key event (form_submit, add_to_cart, sign_up), calculate `event_count / sessions × 100`. Compare against benchmarks.
3. **Engagement anomalies**: Pages with high session count but low engagement time — use page type thresholds from benchmarks (blog < 15s, product < 20s, homepage < 10s)
4. **Event sequence gaps**: Expected event chains (e.g., form_start → form_submit) where the second event is disproportionately low. Flag as CRITICAL if gap > 80%.
5. **Device segmentation**: If GSC Devices data is available, break down key metrics by mobile/desktop/tablet. Flag significant gaps — e.g., if mobile conversion rate is 50%+ lower than desktop, this indicates mobile UX issues.

### 4b. Behavioral Correlations

Find what behaviors correlate with conversion — what the DATA says works, not conventions.

1. **Engagement × conversion correlation**: Group pages by engagement time ranges (0-10s, 10-30s, 30-60s, 60s+). Calculate key event rate per group. Quantify the gap.
2. **Page-type conversion comparison**: Compare conversion rates across page types (blog, destination, region, contact, homepage). Identify which types drive conversions and which are dead weight.
3. **High-engagement zero-conversion pages**: Pages with >60s engagement but zero key events → high-intent users with no conversion path. Biggest missed opportunities.
4. **Event co-occurrence**: Check which events appear together — a brochure download correlating with form_start is a conversion signal. Use event/user counts to estimate overlap.

### 4c. Segment Comparison

Compare behavior across user segments derivable from CSV data:

1. **Blog visitors vs. destination visitors**: Compare engagement time, key event rate, pages per session (if available). Quantify the gap.
2. **Landing page groups**: Group landing pages by type (blog, destination, homepage, region). For each group: total sessions, total key events, conversion rate, avg engagement. This reveals which traffic segments actually matter.
3. **Mobile vs desktop** (if GSC Devices available): Compare CTR, clicks, and positions. Cross-reference with GA4 engagement if page-level device data exists.

For each finding:

- **Data**: exact numbers and percentages
- **Formula**: how the metric was calculated
- **Benchmark comparison**: compare to typical rates from the Analytics Benchmarks table above

## Step 5: Traffic × Behavior Cross-Reference

If GSC data is available, correlate search traffic with on-site behavior:

1. **High-traffic, low-engagement pages**: High GSC clicks but GA4 engagement time < 10s or bounce rate > 80% → content doesn't match search intent
2. **High-converting, low-traffic pages**: GA4 pages with high conversion rates but few GSC impressions → SEO priority targets (improving rankings has direct revenue impact)
3. **Intent mismatch detection**: Compare top GSC queries driving traffic to a page with the page's actual GA4 behavior metrics. Flag pages where the search query intent doesn't match what users do on the page.

For each finding, show:

- Page URL
- GSC metrics: clicks, impressions, CTR, avg position
- GA4 metrics: sessions, engagement time, key events, conversion rate
- **Gap formula**: e.g., `CTR: 4.2% but engagement: 8s avg → intent mismatch score = clicks × (1 - engagement_rate)`

**Temporal trends** (if GSC Chart data or GA4 date data available):

- Is overall traffic trending up, down, or flat?
- Any seasonal patterns? (important for tourism, e-commerce, events)
- Day-of-week or weekly patterns in conversions?
- Flag significant trend changes: "Traffic dropped 30% in week of Jan 20" or "Clicks for 'svalbard skiing' peaked Dec-Jan (seasonal demand)"

If no GSC data, skip this step with a note: "GSC data not available — skipping traffic cross-reference. Run `/cs-seo` for search traffic analysis."

## Step 6: Conversion Funnel Analysis

Identify and analyze conversion funnels from GA4 event sequences:

1. **Auto-detect funnels**: Look for event chains that suggest a funnel (e.g., `page_view → form_start → form_submit`, `product_view → add_to_cart → begin_checkout → purchase`)
2. **Prioritize by revenue proximity**: Analyze checkout/cart/payment/booking funnels FIRST — these are closest to revenue. Then analyze lead-gen funnels (contact forms, newsletter). Then engagement funnels.
3. **Drop-off rates**: For each funnel step, calculate `users_at_step_N / users_at_step_1 × 100`
4. **Revenue impact**: Use `avg_conversion_value` from Step 0 if provided. Formula: `drop-off_users × avg_conversion_value = lost_revenue`. If value is unknown, state: "Revenue impact unknown — avg booking value not provided. Provide it in Step 0 for accurate estimates."
5. **Comparison**: If multiple funnels exist, compare their efficiency

For each funnel:

```
Funnel: [Name]
Step 1: [Event] — 1,000 users (100%)
Step 2: [Event] — 450 users (45%) ← 55% drop-off
Step 3: [Event] — 120 users (12%) ← 73% drop-off from Step 2
Overall conversion: 12%
Revenue impact: 880 lost users × $50 avg value = $44,000/month potential
```

Flag funnels with > 80% drop-off at any single step as CRITICAL.

## Step 7: Code-Level Root Cause Analysis

**Cross-reference analytics findings with actual source code** to identify WHY confirmed problems (Type C) exist. Only investigate findings from Steps 3–6 that are backed by data — not tracking gaps or external platform flows.

For each CRITICAL/HIGH confirmed finding, search the codebase:

- **Form drop-off** (`Glob` `**/*form*` `**/*booking*` `**/*checkout*`): field count, required fields, submit handler, redirect logic, error/loading states
- **Tracking gaps** (`Grep` `gtag|dataLayer|analytics|track`): event firing timing, revenue parameters, conditions that block tracking (dev-mode checks, consent gates)
- **High bounce / low engagement**: SSR vs client-side fetching, blocking API calls, meta tag vs content mismatch
- **Ghost buttons / dead CTAs**: click handler logic, broken routing, conditional rendering (auth-gated, A/B tests)

For each finding output:
- **File:line** — exact location
- **Code snippet** — max 10 lines
- **Data connection** — which analytics finding this explains
- **Severity** — CRITICAL / HIGH / MEDIUM
- **Fix suggestion** — what it should do instead (brief)

## Step 8: Browser MCP — Replay User Flows & Visual Analysis

**Skip if no Browser MCP available.** In Data-only mode without `--url`, skip with note.

**Three rules**:
1. **Confirm hypotheses only** — every page visit must answer a specific data question from Steps 3–6. Do NOT browse for generic UX issues — that's `/cs-ux-review`. Before navigating, state: "Data: X% drop-off at step Y. Question: what does the user see here?"
2. **Viewports** — if mobile > 50% of traffic (GSC), replay critical flows at both desktop (1280×800) and mobile (390×844). Otherwise desktop + spot-check on mobile.
3. **Connect everything to data** — every visual observation must cite the specific metric it explains: "Form has 12 fields — explains 73% drop-off." Drop any observation that can't be tied to a data point.

**Replay up to 3 top funnels** (Step 6) and **up to 5 problem pages** (Steps 3–5): navigate → screenshot initial state → interact as data suggests → screenshot drop-off point → test ghost buttons → note load time vs engagement budget. Reference Step 7 code findings during replay.

## Step 9: Tracking Gaps Audit

Before recommendations, classify every gap by type — they require different language and different actions:

| Type | What it means | Language in report | Action |
|------|--------------|-------------------|--------|
| **A — External platform** | Flow continues on a different domain/app (checkout on portal, payment on Stripe). Zero GA4 events is expected. | "This step happens on [platform] — we can't measure it from GA4." | Recommend cross-domain or server-side tracking |
| **B — Missing tracking** | Feature exists on main site, events were never set up or are broken. | "Tracking is missing — we can't confirm if this works or fails." | Add tracking first, re-analyze before recommending changes |
| **C — Confirmed drop-off** | Upstream event fires, downstream doesn't — measurable gap within tracked flow. | Use direct language. Investigate root cause in Step 7. | Treat as confirmed problem |

Cross-reference with `external_platforms` from Step 0 before classifying any page with zero events.

Check for:
1. **Revenue tracking** — booking/checkout events with $0 values → CRITICAL, blocks all ROI analysis
2. **Untracked conversion pages** — apply Type A/B classification per above
3. **Partial funnel** — form_start with no form_submit → Type C if both on main site; Type A if submit goes external
4. **Orphan events** — fire but can't be attributed to pages → note attribution gap
5. **No source/channel data** — note channel-level analysis is impossible

For each gap: **Type** | **What's missing** | **Impact on analysis** | **Priority** (CRITICAL/HIGH/MEDIUM)

## Step 10: Generate Recommendations

For each finding, generate a data-backed recommendation:

- **What to fix**: specific, actionable change
- **Evidence**: the data that supports this recommendation
- **Estimated impact formula**: quantified prediction
  - Example: `Current: 450 form_starts, 120 form_submits (26.7%). If simplified form improves to 40%: 450 × 0.40 = 180 submits (+60/month)`
- **Effort level**: LOW / MEDIUM / HIGH
- **Revenue proximity**: DIRECT (checkout, payment, booking form) / INDIRECT (lead gen, email capture, SEO) / BRAND (engagement, content, UX)
- **Priority**: based on `estimated_impact × revenue_proximity_weight / effort` — DIRECT items get priority over INDIRECT at equal effort

**Key principle**: Never recommend anything without data evidence. If the data doesn't support a conclusion, say so. But when data DOES support a conclusion — be blunt. "This is costing you $X/month" is better than "There may be room for improvement."

**Critical language rules**:

- **Confirmed problems** (Type C data): use "broken", "failing", "losing money" — quantify in users or revenue: "73% drop-off = 330 lost bookings/month = ~$66K"
- **External platform / missing tracking** (Type A/B): use "we can't measure this", "tracking gap", "unknown" — never "broken" or "failing"
- If a page has 0% conversion but is an external platform flow → "we have no visibility into this step" — not "dead page"
- If a page has 0% conversion with significant traffic AND is confirmed on the main site with tracking in place → THEN call it a "dead page"

**Architectural recommendations require confirmed data**:
- Never recommend removing authentication, rewriting checkout flows, or changing business logic based on missing GA4 events alone
- If auth is required by the product (e.g., booking needs a user record in the DB), that is intentional design — not a bug. Recommend tracking the auth flow instead
- Before recommending any architectural change, confirm: (a) the feature is on the main site, (b) tracking exists, (c) data shows actual failure

## Step 11: Generate Reports & Save Results

Generate **two separate reports** and save them locally. Reports must be critical and direct — no hedging, no "potential opportunities." If something is broken, say it's broken. If money is being lost, state the amount.

### Output Directory

Create a timestamped results directory:

```
.claude/analytics-result/YYYY-MM-DD_HH-MM/
├── technical-report.md    — Full technical report for developers
└── client-report.md       — Executive report for stakeholders/clients
```

Use `Bash` to create the directory: `mkdir -p .claude/analytics-result/$(date +%Y-%m-%d_%H-%M)`

### Report 1: Technical Report (`technical-report.md`)

For the development team. Include code references, formulas, raw data. Sections:

- **Header**: Site, period, generated date
- **Executive Summary**: 3–5 sentences. Blunt. "The site loses $X/month because Y. Z% of traffic converts to nothing."
- **Critical Verdict**: 🔴 CRITICAL / 🟡 WARNING / 🟢 HEALTHY
- **Data Summary**: GA4 file counts, session totals, GSC if available, device split, overall conversion rate
- **User Journey Map**: Top flows with completion rates. Note flows are reconstructed, not tracked.
- **Engagement & Event Analysis**: Ghost buttons, event conversion rates vs benchmarks, engagement anomalies, device gaps
- **Traffic × Behavior** (GSC only): High-traffic/low-engagement, high-converting/low-traffic (SEO targets), intent mismatch, temporal trends
- **Conversion Funnels**: Steps + drop-off rates + revenue impact. Checkout/booking funnels first.
- **Code-Level Root Causes**: File:line, snippet (max 10 lines), data connection, severity, fix suggestion
- **Tracking Gaps**: Classified by Type A/B/C. Code locations for missing tracking.
- **Flow Replay** (Browser MCP only): Screenshots + data correlations per flow
- **Action Items**:

  **Type key**: ✅ Confirmed | ⚠️ Needs verification | 📊 Add tracking first

  | # | Type | Severity | Action | Evidence | Code Location | Impact Formula | Effort | Revenue Proximity |
  |---|------|----------|--------|----------|---------------|----------------|--------|-------------------|

- **Methodology**: Data sources, period, limitations, confidence levels

### Report 2: Client Report (`client-report.md`)

For stakeholders — no code, no file paths, no jargon. Business impact only. Sections:

- **Header**: Site name, period, prepared date
- **Overall Health**: 🔴/🟡/🟢 + one paragraph verdict with user/money numbers
- **Key Numbers**: Table — metric, value, benchmark, verdict emoji
- **What We Couldn't Measure**: ⚠️ **This section comes before findings.** Lead with: "Before reading this report — here's what our data cannot see." For each gap: what we can't see → why (external platform / no tracking / missing export) → which sections of this report it affects. Be explicit: "The booking form sends users to a separate app — we don't know how many complete payment. The findings below are about the booking *form*, not the booking *completion*." If there are no significant gaps, keep this section brief.
- **What's Costing You Money**: Numbered list of **confirmed** problems only (not tracking gaps). Each item: problem in plain language → how we know (specific GA4 numbers) → impact in users/money → fix difficulty. If `avg_conversion_value` was provided in Step 0, use it; otherwise state the assumed value.
- **What's Working**: Brief positives. Every critical report needs this.
- **Traffic Overview** (GSC only): Top search terms, page traffic, mobile/desktop split, trends. Reference `period_anomalies` when explaining traffic spikes or dips.
- **Recommended Actions**:

  **Basis key**: ✅ Confirmed by data | 📊 Add tracking first (may not be a real problem)

  | # | Basis | Action | Expected Impact | Difficulty | Timeline |
  |---|-------|--------|-----------------|------------|----------|

- **Next Steps**: 1–3 concrete actions. Always include tracking setup as a step if measurement gaps exist.

### Saving

Use `Write` tool to save both files to the timestamped directory. After saving, output:

```
📊 Reports saved:
  Technical: .claude/analytics-result/YYYY-MM-DD_HH-MM/technical-report.md
  Client:    .claude/analytics-result/YYYY-MM-DD_HH-MM/client-report.md
```

---

## Important

- **Source code is read-only** — this skill never modifies the target project (only writes to `.claude/analytics-result/`)
