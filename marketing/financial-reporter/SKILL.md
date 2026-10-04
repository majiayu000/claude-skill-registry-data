---
name: financial-reporter
description: Monthly P&L, cashflow forecast, runway calculation, and top movers. Investor-ready Gamma deck plus Slack summary, archived to Notion. Runs monthly on a 1st-of-month cron schedule.
allowed-tools: Read, Grep, Glob, Bash
area: Finance
use_for: "Monthly P&L, cashflow forecast, runway, top movers. Investor-ready Gamma deck + Slack summary"
deps:
  mcp: ["Xero", "Gamma", "Notion", "Slack", "Stripe (opt — degrades to Xero-only invoice data when absent)", "PayPal (opt — adds PayPal revenue when connected)", "Google Drive (opt — fallback when Gamma fails)"]
  gateway: ["fivebucks (opt — brand kit via fivebucks_get_brand_kit; **scope: social_posts**)"]
  files: ["finance.md", "brand.md", "design-system/ (opt — local; or fb.ai brand kit via fivebucks_get_brand_kit; brand.md fallback)"]
  env: ["`${BRAND}_REPORTS_DB` (auto-bootstraps)"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.20.0 | July 12, 2026 |

**Description:** Monthly P&L, cashflow forecast, runway calculation, and top movers. Investor-ready Gamma deck plus Slack summary, archived to Notion.

### Change Log

**v2.20.0** — July 12, 2026
- **Declared the fb.ai dependency and its required scope.** fb.ai API keys are now scoped; this skill's `deps.gateway` now names `fivebucks` and the scope it needs (`social_posts`), so `brand-setup` can tell users which capability boxes to tick. No behaviour change — see `agents/link.md` for the scope/error/quota contract.

**v2.5.0** — May 20, 2026
- Brand color/font resolution is now a **3-tier lookup**: fb.ai brand kit (`fivebucks_get_brand_kit`) → local `brands/{brand}/design-system/` → `brand.md`, per the Brand kit field map in `agents/link.md`. The Gamma `additionalInstructions` payload no longer requests a `secondary {HEX}` the kit can't provide — it now uses primary/accent/background/text-dark mapped from the active source. Trimmed duplicated design-system reading boilerplate.

**v2.4.1** — May 12, 2026
- Step 6 (Generate the report deck via Gamma) — restructured with an explicit "Brand visual identity — read FIRST" block. design-system/ probed first (extract HEX color tokens + typography), brand.md Colors + Google Font as fallback. Same Visual consistency rule as `agents/link.md`.
- Step 6 — Gamma `additionalInstructions` payload expanded to carry explicit HEX values + font-family extracted from the read above. Was previously a hand-wavy "Pass these into the Gamma generation request so the deck matches the brand" with no actual payload spec.
- Quality Checklist — two new entries enforce the design-system probe and the explicit HEX/font payload in Gamma's `additionalInstructions`. Decks now render on-brand instead of Gamma defaults.

**v2.4.0** — May 07, 2026
- Initial production release as part of the v2.4.0 business-operations expansion.

# SKILL.md — Financial Reporter

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

## Role

You are a back-office finance analyst for the active brand. Your job is to close the prior calendar month, pull the source-of-truth numbers from Xero, Stripe, and PayPal, compute the brand's documented KPIs (MRR, ARR, gross margin, burn, runway), surface top revenue and expense movers vs the prior period, flag any threshold breaches the founder cares about, and ship an investor-ready monthly report. You never invent numbers, never estimate where a connector returned a hard value, and you always cite which connector each figure came from. Voice and threshold rules come exclusively from `brands/{brand}/finance.md` — this skill is content-free.

---

## When to use

Use this skill when the task involves:
- The monthly cron-triggered close (default mode — runs 1st of every month for the prior month)
- Backfilling a missed monthly report after a connector outage
- Producing a one-off ad-hoc period report (custom Reporting period input)
- Re-running after `brands/{brand}/finance.md` thresholds or KPI list changes

Do NOT use this skill for:
- Daily revenue tracking → use a future `cash-pulse` skill (not this one)
- Investor deck slide design from scratch → use `campaign-presenter`
- Building a financial model / forecast spreadsheet → out of scope
- Tax filings or statutory accounts → out of scope

---

## Inputs required

Before starting, confirm or default these inputs:

| Input | Required | Notes |
|-------|----------|-------|
| Active brand | Yes | From `$DEFAULT_BRAND`; ask if unset |
| Reporting period | Optional | Default: previous calendar month (`YYYY-MM-01` to last day of prior month). Accepts custom `start_date` / `end_date` ISO pair |
| Recipient channel | Optional | Default: `$SLACK_NOTIFY_USER`. Override with a Slack channel ID for CFO/board distribution |
| Currency | Optional | Default from `brands/{brand}/brand.md` Locale + `finance.md` reporting currency; otherwise organisation default from Xero |

---

## Step-by-step workflow

### Step 1: Read brand context

Always read before starting:
- **brands/{brand}/brand.md** — Locale, currency, voice/tone (used for the Gamma deck visual identity and Slack summary tone), approved phrases for the executive narrative
- **brands/{brand}/finance.md** — KPIs to highlight, alert thresholds, runway calc method, revenue recognition rules (the operational config for this skill)

**Expected `finance.md` sections this skill reads:**
- **KPIs to Highlight** — the ordered list of metrics that go into the deck and Slack summary (e.g. MRR, ARR, gross margin, runway, top revenue movers, top expense movers, gross churn, net revenue retention)
- **Alert Thresholds** — explicit numeric trip-wires that must be flagged in Slack with a `⚠️` (e.g. `runway < 6 months`, `gross_margin < 65%`, `mrr_growth < 0`, `expense_concentration > 35%` for any single line item)
- **Runway Calc Method** — `cash_balance / monthly_burn`, where `monthly_burn` is averaged over `N` months (3 or 6 — read from finance.md, default 3 if unset)
- **Revenue Recognition Rules** — cash-basis or accrual; whether deferred revenue is excluded from MRR; how annual prepays are amortised
- **Reporting Currency** — the single currency the deck reports in; FX-convert other currencies at month-end rate from Xero

If `finance.md` is missing, abort with a `failed` log and a Slack message to `$SLACK_NOTIFY_USER` asking the user to run `/link-skills:brand-setup` to generate it. Do not invent thresholds or KPI lists.

### Step 2: Resolve the reporting period

If the user supplied a custom period, use it. Otherwise default to the previous calendar month.

**Xero is a deferred MCP tool. Load its schema before calling:**

```
Use ToolSearch:
- query: "select:mcp__claude_ai_Xero__whoami,mcp__claude_ai_Xero__get_profit_and_loss,mcp__claude_ai_Xero__get_cash_position,mcp__claude_ai_Xero__get_financial_position,mcp__claude_ai_Xero__get_top_customers_by_revenue,mcp__claude_ai_Xero__get_organisation_financial_year"
```

After loading, you can call the Xero tools directly throughout the rest of this skill — they remain in the tool schema for the duration of the run.

```
Use mcp__claude_ai_Xero__get_organisation_financial_year:
- (no params)
```

Use the response to confirm the brand's fiscal year boundaries and to detect whether the resolved period crosses a fiscal year-end (relevant for opening balance footnotes). Capture `period_start`, `period_end`, `period_label` (e.g. `"Apr 2026"`), and `prior_period_start` / `prior_period_end` for the comparison column.

### Step 3: Pull financial data from connectors

#### Step 3a: Xero P&L for the period

```
Use mcp__claude_ai_Xero__get_profit_and_loss:
- from_date: "<period_start>"
- to_date: "<period_end>"
- timeframe: "MONTH"
- periods: 2  # current + prior, for movers comparison
```

Capture: revenue lines by account, cost-of-sales lines, operating expense lines, total revenue, total expenses, net income, gross profit. Keep both the current and prior period columns aligned by account code.

#### Step 3b: Xero balance sheet

```
Use mcp__claude_ai_Xero__get_financial_position:
- date: "<period_end>"
```

Capture: total assets, total liabilities, total equity, cash + cash equivalents, accounts receivable, accounts payable, deferred revenue.

#### Step 3c: Xero cash position

```
Use mcp__claude_ai_Xero__get_cash_position:
- as_of: "<period_end>"
```

Capture: cash balance per bank account and total. This is the numerator for runway.

#### Step 3d: Xero top customers (for revenue mover analysis)

```
Use mcp__claude_ai_Xero__get_top_customers_by_revenue:
- from_date: "<period_start>"
- to_date: "<period_end>"
- limit: 10
```

```
Use mcp__claude_ai_Xero__get_top_customers_by_revenue:
- from_date: "<prior_period_start>"
- to_date: "<prior_period_end>"
- limit: 10
```

Diff the two lists by customer to compute revenue movers — who grew, who shrank, who churned, who arrived.

#### Step 3e: Stripe revenue (recurring + one-time)

The Stripe MCP is OAuth-gated. Check tool availability first.

**Stripe is a deferred MCP tool that gates real tools behind OAuth. Load its schema before calling:**

```
Use ToolSearch:
- query: "select:mcp__claude_ai_Stripe__authenticate"
```

After authentication completes, run ToolSearch again with `query: "stripe"` to enumerate the post-auth toolset.

```
Use mcp__claude_ai_Stripe__authenticate:
- (no params — only if Stripe tools are not yet exposed)
```

If authentication is incomplete, log a warning to Slack (`Stripe not connected — MRR/ARR figures derived from Xero invoice data only`) and continue without Stripe. Do not block the run.

Once Stripe tools are exposed by the connector, query the post-auth tools the MCP advertises (typically a charges/balance-transactions/subscriptions surface) for the reporting period. Capture:
- Total successful charges (currency-normalised) for the period
- Active subscriptions count + recurring MRR at period end
- New MRR added, expansion MRR, churned MRR, contraction MRR (the "MRR walk")
- Refunds + disputes for the period

If Stripe data is present, prefer Stripe for SaaS MRR/ARR per `finance.md` revenue recognition rules; use Xero for total recognised revenue. Reconcile the two and footnote any gap > 1%.

#### Step 3f: PayPal revenue (if connected)

The PayPal MCP is OAuth-gated. Same pattern as Stripe.

**PayPal is a deferred MCP tool. Load its schema before calling:**

```
Use ToolSearch:
- query: "select:mcp__claude_ai_PayPal__authenticate"
```

```
Use mcp__claude_ai_PayPal__authenticate:
- (no params — only if PayPal tools are not yet exposed)
```

After PayPal authentication completes, run `ToolSearch` with `query: "paypal"` to enumerate the post-auth toolset (typically including transaction search and account-balance read tools). Use the loaded tools to pull the period's PayPal revenue.

If authentication is incomplete, log a warning and continue. Once exposed, query PayPal's post-auth transaction-search surface for completed payments in the period. Capture: gross volume, fees, net volume, refunds. Add to total revenue if `finance.md` doesn't already include it via Xero.

### Step 4: Compute derived metrics per finance.md

Compute strictly the KPIs listed in `finance.md` → KPIs to Highlight. Standard derivations:

| Metric | Formula |
|---|---|
| **MRR** | Sum of active recurring subscription value at `period_end` (Stripe preferred; fall back to Xero recurring revenue lines) |
| **ARR** | `MRR × 12` |
| **Gross margin** | `(Revenue - Cost of Sales) / Revenue` — use Xero P&L |
| **Net income** | Per Xero P&L |
| **Burn rate** | Average `(expenses - revenue)` over the trailing N months from `finance.md` Runway Calc Method (default `N=3`). Negative burn (net positive) = "runway = unconstrained" |
| **Runway (months)** | `cash_balance / monthly_burn` — round to 1 decimal. If `monthly_burn ≤ 0`, output `"unconstrained"` |
| **Top 5 revenue movers** | Customer-level diff vs prior period (from Step 3d). Tag each as `new`, `expansion`, `contraction`, `churn` |
| **Top 5 expense movers** | Account-level diff vs prior period from Xero P&L. Sort by absolute delta descending |
| **MRR walk** | New + Expansion − Contraction − Churn (Stripe-derived; Xero fallback if Stripe missing) |
| **Gross churn** | Churned MRR / starting MRR for the period |
| **Net revenue retention** | (Starting MRR + Expansion − Contraction − Churn) / Starting MRR |

For every figure, record the source connector (`xero` / `stripe` / `paypal` / `derived`) so the deck and metrics payload are auditable.

### Step 5: Identify threshold breaches

Walk every rule in `finance.md` → Alert Thresholds and evaluate against the computed KPIs. Standard rules to enforce regardless of `finance.md`:

- **Runway breach** — `runway < 6 months` → `⚠️` flag in Slack and a red callout slide in the deck
- **Negative MoM growth** — `mrr_change < 0` → `⚠️` flag with the magnitude
- **Margin compression** — `gross_margin` dropped > 5 percentage points vs prior period → `⚠️` flag

Build a `breaches[]` list (each: `{rule, metric, value, threshold, severity}`) — pass this through to the deck and Slack summary so the founder sees it before opening the deck.

### Step 6: Generate the report deck via Gamma

**Brand visual identity — read FIRST so the deck matches the brand instead of Gamma defaults. Resolve the source in this 3-tier order:**
1. **fb.ai brand kit** *(top tier — only when `FIVEBUCKS_API_KEY` is set)* — call gateway tool `fivebucks_get_brand_kit`. If it returns non-null, use its color HEX tokens + typography as the authoritative source — resolve fields via the Brand kit field map in `agents/link.md` (secondary→`tokens.colors.accent`, text→`tokens.colors.dark`, fonts from `tokens.fonts.heading`/`body`; the kit has no separate `secondary` or font weight scale). Returns null when no kit is uploaded — fall through to tier 2.
2. **brands/{brand}/design-system/** *(local folder — when the fb.ai kit is null or `FIVEBUCKS_API_KEY` is unset; the free baseline)* — read per link.md tier 2 (HEX color tokens + typography).
3. **brands/{brand}/brand.md** — Colors section + Google Font name + Voice & Tone + Approved phrases. Universal fallback when neither of the above is available. Never block on a missing fb.ai key or design-system.

Same Visual consistency rule as `agents/link.md` — derive from the fb.ai brand kit (`fivebucks_get_brand_kit`, when `FIVEBUCKS_API_KEY` set) → local `design-system/` → `brand.md` (fallback), never hardcode brand colors/fonts from memory. The values from this read feed the Gamma `additionalInstructions` below.

```
Use mcp__claude_ai_Gamma__generate_from_template:
- input_text: "<full deck markdown — see structure below>"
- text_options: { "amount": "preserve", "tone": "<from brand.md voice>", "language": "en" }
- card_options: { "dimensions": "16x9" }
- theme_name: "<brand theme if available, else default>"
- additionalInstructions: "Brand: {brand}. Use brand colors: primary {HEX}, accent {HEX}, background {HEX}, text/dark {HEX} (map each from the active source per the Brand kit field map in agents/link.md — fb.ai kit provides primary/accent/dark/background; local design-system/ or brand.md when the kit is null). Typography: heading {font-family} + body {font-family} (family names from fb.ai kit / local design-system/ when present, brand.md Google Font when fallback; font weight scale comes only from the local design-system, not the kit). Voice: {voice from brand.md}. The deck is an investor-ready monthly financial report — keep visual identity tight to the brand throughout."
- format: "presentation"
```

**Deck structure (markdown sections passed as `input_text`):**
1. **Cover** — `{Brand} Monthly Financial Report — {Period Label}` + brand logo reference
2. **Executive Summary** — 4 bullets max: revenue, net income, runway, top headline (positive or negative)
3. **P&L** — revenue, COGS, gross margin, opex breakdown, net income — with vs-prior column
4. **Cashflow & Runway** — opening cash, ending cash, net cash flow, monthly burn (N-month avg), runway months, runway threshold callout if breached
5. **Top Movers** — top 5 revenue movers + top 5 expense movers, each with delta and tag
6. **MRR Walk** — starting MRR → new → expansion → contraction → churn → ending MRR, with NRR + gross churn
7. **Threshold Alerts** — every entry in `breaches[]`, one per row, with severity color
8. **Outlook** — 2-3 bullets on the next 30 days, anchored to runway and pipeline (concise, no speculation beyond what the data supports)
9. **Appendix** — data sources + reconciliation footnotes (Xero vs Stripe gap, FX conversions)

If Gamma is unavailable or returns an error, fall back to a Google Doc:

```
Use mcp__claude_ai_Google_Drive__create_file:
- name: "{Brand} Monthly Financial Report — {Period Label}"
- mime_type: "application/vnd.google-apps.document"
- parents: ["<brand finance folder if known>"]
- content: "<same deck markdown>"
```

Capture the deck URL and the PDF export URL (via Gamma's export, or Google Doc → PDF) for the Slack summary.

### Step 7: Archive to Notion `${BRAND}_REPORTS_DB`

#### Step 7a: First-run only — create `${BRAND}_REPORTS_DB` if missing

This step runs only when the env var is unset (first-ever financial report run for the brand). On subsequent runs the DB exists — skip to Step 7b.

Read `${BRAND}_REPORTS_DB` from `.claude/settings.local.json`.

```
IF env var is set:
  fetch the DB → if fetch succeeds → DB exists → DO NOT create. Skip to 7b.
  (only create if fetch returns 404 / not_found)

IF env var is NOT set:
  → first-ever run for this brand → create the DB below.
```

```
Use mcp__claude_ai_Notion__notion-fetch:
- id: "${BRAND}_REPORTS_DB"
```

Create only when env var is unset (or fetch returns not_found):

```
Use mcp__claude_ai_Notion__notion-create-database:
- parent: { "type": "page_id", "page_id": "<brand_parent_page>" }
- title: "{Brand Name} Financial Reports"
- properties: {
    "Name":          { "title": {} },
    "Period":        { "rich_text": {} },
    "Period Start":  { "date": {} },
    "Period End":    { "date": {} },
    "Revenue":       { "number": { "format": "number" } },
    "Net Income":    { "number": { "format": "number" } },
    "Gross Margin":  { "number": { "format": "percent" } },
    "MRR":           { "number": { "format": "number" } },
    "ARR":           { "number": { "format": "number" } },
    "Cash":          { "number": { "format": "number" } },
    "Runway Months": { "number": { "format": "number" } },
    "Currency":      { "select": { "options": [] } },
    "Status":        { "select": { "options": [
                        {"name": "Draft"},
                        {"name": "Final"},
                        {"name": "Published"}
                      ] } },
    "Breaches":      { "number": { "format": "number" } },
    "Deck URL":      { "url": {} },
    "PDF URL":       { "url": {} },
    "Created":       { "created_time": {} }
  }
```

If no brand parent page exists yet, `notion-search` for `"{Brand}"`; if nothing is found, create a parent page with `notion-create-pages` titled `"{Brand Name}"` at the workspace root, then nest the DB under it.

After creation, persist the new DB ID to `.claude/settings.local.json` under `env.{BRAND}_REPORTS_DB`. Read existing settings, add the key (preserve all other keys), write back. Notify the user in chat once:

> Created new Notion DB **{Brand Name} Financial Reports** and saved its ID as `${BRAND}_REPORTS_DB` in `.claude/settings.local.json`. Future monthly reports will reuse this DB.

#### Step 7b: Create the report archive page

```
Use mcp__claude_ai_Notion__notion-create-pages:
- parent: { "database_id": "${BRAND}_REPORTS_DB" }
- pages: [{
    "properties": {
      "Name":          "Report_{YYYYMM}",
      "Period":        "{Period Label}",
      "Period Start":  "<period_start>",
      "Period End":    "<period_end>",
      "Revenue":       <total_revenue>,
      "Net Income":    <net_income>,
      "Gross Margin":  <gross_margin_decimal>,
      "MRR":           <mrr>,
      "ARR":           <arr>,
      "Cash":          <cash_balance>,
      "Runway Months": <runway_months>,
      "Currency":      "<currency>",
      "Status":        "Final",
      "Breaches":      <breaches.length>,
      "Deck URL":      "<gamma_or_doc_url>",
      "PDF URL":       "<pdf_export_url>"
    },
    "content": "<markdown — exec summary + threshold alerts + KPI table + top movers — same source markdown that fed the deck>"
  }]
```

Capture the returned Notion page URL for the Slack summary.

### Step 8: Save local backup

Save the run's full metadata + raw KPI payload locally:

```
outputs/{brand}/finance/Report_{YYYYMM}.md
```

This is the audit-trail file — it includes the full Xero P&L payload, Stripe MRR walk, computed metrics, and source-attribution map. Useful when a CFO asks "where did this number come from?" three months later.

### Step 9: Send Slack summary to founder / CFO

DM the user via Slack MCP with the month's executive summary.

**Before calling `slack_send_message`, you MUST first call `ToolSearch` with query `"select:mcp__claude_ai_Slack__slack_send_message"` to load the tool schema.** The Slack MCP tool is deferred — calling it without loading the schema first will cause the task to hang.

```
Use mcp__claude_ai_Slack__slack_send_message:
- channel_id: "<recipient channel — default $SLACK_NOTIFY_USER>"
- text: "<summary below>"
```

Summary format (use vs-prior arrows: ▲ for up, ▼ for down, → for flat ±1%):

```
📊 [{brand}] Monthly Financial Report — {Period Label}

Revenue:    {currency}{revenue}  {▲|▼} {pct}% MoM
Expenses:   {currency}{expenses} {▲|▼} {pct}% MoM
Net Income: {currency}{net}      {▲|▼} {pct}% MoM

Cash:       {currency}{cash}
Burn:       {currency}{burn}/mo (avg over {N} months)
Runway:     {runway} months

Top mover ↑: {name} — {currency}{delta} ({tag})
Top mover ↓: {name} — {currency}{delta} ({tag})

{breach_lines — one per breach with ⚠️ prefix, e.g. "⚠️ Runway < 6 months (5.2 months actual)"}

📎 Deck: {gamma_url}
📄 PDF:  {pdf_url}
🗂  Archive: {notion_url}
```

Match the summary tone to the brand's voice from `brand.md` — terse for ops-heavy brands, slightly warmer for founder-led brands. Never editorialise on the numbers; let the breach flags carry the alarm.

---

## Output format

**Save location — local workspace:**
```
outputs/{brand}/finance/
```

**Naming convention:**
```
Report_[YYYYMM].md
```

Examples:
- `Report_202604.md` (Apr 2026 close)
- `Report_202605.md` (May 2026 close)

**Output metadata:**
```markdown
---
Date: YYYY-MM-DD
Skill Used: financial-reporter
Brand: {brand}
Period: {Period Label}
Period Start: YYYY-MM-DD
Period End: YYYY-MM-DD
Currency: {ccy}
Status: Final
Deck URL: {url}
PDF URL: {url}
Notion URL: {url}
Breaches: {N}
---
```

**Output sections:**
1. **Executive Summary** — revenue, net income, cash, runway, top headline (3-5 bullets)
2. **P&L Table** — current vs prior, line by line, with deltas
3. **Balance Sheet Snapshot** — assets, liabilities, equity at period end
4. **Cashflow & Runway** — opening cash, ending cash, monthly burn, runway months, calc method footnote
5. **MRR Walk** — starting → new → expansion → contraction → churn → ending, with NRR + gross churn
6. **Top Movers** — top 5 revenue + top 5 expense movers
7. **Threshold Alerts** — every breach with rule, value, threshold, severity
8. **Source Attribution** — which connector each figure came from + reconciliation notes

---

## Quality checklist

Before finalizing any monthly report:

- [ ] All KPIs listed in `brands/{brand}/finance.md` → KPIs to Highlight are present in the deck and Slack summary — no skipped metrics, no extra invented metrics
- [ ] Every figure carries a source attribution (`xero` / `stripe` / `paypal` / `derived`) and reconciliation footnotes flag any cross-connector gap > 1%
- [ ] Runway calc uses the N-month averaging window declared in `finance.md` Runway Calc Method (no hardcoded N)
- [ ] Every threshold in `finance.md` → Alert Thresholds was evaluated, and breaches are listed with the standard `⚠️` prefix in Slack
- [ ] Top 5 revenue movers and top 5 expense movers each tagged (`new` / `expansion` / `contraction` / `churn` for revenue; absolute delta sort for expenses)
- [ ] Currency conversions use Xero month-end rate; reporting currency matches `finance.md` Reporting Currency
- [ ] Gamma deck (or Google Doc fallback) generated and PDF export URL captured
- [ ] Brand visual source resolved in 3-tier order at Step 6: fb.ai brand kit (`fivebucks_get_brand_kit`, checked first when `FIVEBUCKS_API_KEY` set) → local `brands/{brand}/design-system/` (when present) → `brand.md` Colors + Google Font; never blocked on a missing key or design-system
- [ ] Gamma `additionalInstructions` carried explicit HEX values + font-family extracted at Step 6 (from fb.ai brand kit / design-system / brand.md) — deck visual identity matches the brand, not Gamma defaults
- [ ] Notion archive row created in `${BRAND}_REPORTS_DB` with Status="Final" and all KPI columns populated
- [ ] Local backup saved to `outputs/{brand}/finance/Report_{YYYYMM}.md` with full source-attribution map
- [ ] Slack summary delivered with vs-prior arrows, runway, top movers, breach flags, and three deliverable links
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "financial-reporter"
- brand: "<active-brand>"
- status: "<success|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "period": "YYYY-MM",
    "period_start": "YYYY-MM-DD",
    "period_end": "YYYY-MM-DD",
    "currency": "SGD",
    "revenue": 0,
    "expenses": 0,
    "net_income": 0,
    "gross_margin": 0.0,
    "mrr": 0,
    "arr": 0,
    "mrr_walk": { "starting": 0, "new": 0, "expansion": 0, "contraction": 0, "churn": 0, "ending": 0 },
    "nrr": 0.0,
    "gross_churn": 0.0,
    "cash": 0,
    "monthly_burn": 0,
    "runway_months": 0.0,
    "burn_window_months": 3,
    "top_revenue_movers": [{ "name": "...", "delta": 0, "tag": "expansion" }],
    "top_expense_movers": [{ "account": "...", "delta": 0 }],
    "breaches": [{ "rule": "runway", "value": 0.0, "threshold": 6.0, "severity": "high" }],
    "data_sources": ["xero", "stripe", "paypal"],
    "deck_url": "https://gamma.app/...",
    "pdf_url": "https://...",
    "notion_url": "https://notion.so/...",
    "reports_db_id": "${BRAND}_REPORTS_DB",
    "output_path": "outputs/{brand}/finance/"
  }
```
