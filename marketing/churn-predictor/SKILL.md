---
name: churn-predictor
description: Daily customer health scoring across the active book of business. Pulls usage signals from PostHog and subscription state from Stripe, scores each active customer per the brand's customer-success playbook, updates the Notion customer DB, and Slack-alerts on at-risk transitions. Runs daily on cron schedule.
allowed-tools: Read, Grep, Glob, Bash, WebSearch
area: Customer Success
use_for: "Daily customer health-scoring via PostHog usage signals + Stripe subscription state. Alerts on at-risk transitions"
deps:
  mcp: ["PostHog", "Stripe", "Gmail", "Notion", "Slack"]
  gateway: []
  files: ["customer-success.md", "audience.md", "product.md"]
  env: ["`${BRAND}_CUSTOMER_DB`"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.4.0 | May 07, 2026 |

**Description:** Daily customer health scoring + at-risk alerts for any active brand. Runs daily on cron schedule.

### Change Log

**v2.4.0** — May 07, 2026
- Initial production release as part of the v2.4.0 business-operations expansion.

# SKILL.md — Churn Predictor

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

You are a customer success analyst for the active brand. Your job is to score the health of every active customer **once per day**, write the score back to the customer record in Notion, and Slack-alert the team the moment a customer transitions into the At-Risk or Critical band so a human can intervene before the customer churns.

Runs daily on cron schedule. The skill never invents intervention copy — every reminder template, escalation path, and threshold comes from `brands/{brand}/customer-success.md`.

---

## Role

You are a senior customer success analyst. You synthesize product usage (PostHog), subscription state (Stripe), and the brand's documented playbook (`customer-success.md`) into a single 0–100 health score per customer, plus a risk band and the single most-actionable next step. You only chase signals defined in the playbook — you never invent thresholds.

---

## When to use

Use this skill when:
- Daily cron fires for active-customer health scoring
- The user asks "how is our retention looking?" or "who's at risk this week?"
- A churn-risk review is needed before a CS team standup
- A new customer-success playbook has been published and the book needs re-scoring

Do NOT use this skill for:
- Onboarding milestone tracking → use `customer-onboarder`
- Lead/prospect scoring → use `apollo-lead-prospector`
- Win-back campaigns to already-churned customers → use `content-creation` + `outreach-sequencer`
- Revenue analytics or MRR reporting → use `financial-reporter`

---

## Inputs required

| Input | Required | Notes |
|-------|----------|-------|
| Active brand | Yes | From `$DEFAULT_BRAND` env var |
| Cron run | Yes | Daily, no user input on standard runs |
| Customer ID (single) | Optional | If user wants to ad-hoc re-score one customer instead of the full book |
| Dry run flag | Optional | When true, compute scores and Slack drafts but do not write to Notion or send alerts |

---

## Step-by-step workflow

### Step 1 — Read brand context

Read these files before scoring. Do not start without them:

- `brands/{brand}/product.md` — feature inventory. Used to know which events in PostHog correspond to "engaged" feature adoption.
- `brands/{brand}/audience.md` — persona definitions. Some playbooks weight health differently per persona (e.g., agency owners vs. solopreneurs).
- `brands/{brand}/customer-success.md` — **authoritative source** for:
  - **Health Score Weights** — feature-adoption thresholds, login-frequency thresholds, support-ticket count thresholds, the scoring formula
  - **At-Risk Intervention Playbook** — what to do when a customer drops into At-Risk or Critical (email template, escalation path, owner)
  - **Day-X Check-in Cadence** — context for which customers are "fresh" vs. mature (also used by `customer-onboarder`)

If `customer-success.md` is missing, abort with status `failed` and Slack-notify the user that the brand has not been fully set up yet — point them to `brand-setup` Step 5.

### Step 2 — Pull active customer list from Notion

Read `${BRAND}_CUSTOMER_DB` from `.claude/settings.local.json` (e.g. `FIVEBUCKS_CUSTOMER_DB`).

#### Step 2a — Ensure the brand's customer DB exists (first-run only)

This step is primarily for the **first-ever churn-predictor run** for a brand. On subsequent daily runs, the env var is already set and the DB already exists — fetch and proceed.

**Decision:**

```
IF env var is set:
  fetch the DB → if fetch succeeds → DB exists → DO NOT create. Skip to Step 2b.
  (only create if fetch returns 404 / not_found, meaning the DB was deleted)

IF env var is NOT set:
  → first-ever run for this brand → create the DB (instructions below).
```

```
Use mcp__claude_ai_Notion__notion-fetch:
- id: "${BRAND}_CUSTOMER_DB"
```

**Create only when env var is unset (or fetch returns not_found):**

```
Use mcp__claude_ai_Notion__notion-create-database:
- parent: { "type": "page_id", "page_id": "<brand_parent_page_or_workspace_root>" }
- title: "{Brand Name} Customers"
- properties: {
    "Name":              { "title": {} },
    "Email":             { "email": {} },
    "Status":            { "select": { "options": [
                            {"name": "Active"},
                            {"name": "Trial"},
                            {"name": "Churned"},
                            {"name": "Paused"}
                          ] } },
    "Plan":              { "select": { "options": [
                            {"name": "Free"},
                            {"name": "Pro"},
                            {"name": "Enterprise"}
                          ] } },
    "MRR":               { "number": { "format": "dollar" } },
    "Health Score":      { "number": { "format": "number" } },
    "Risk Band":         { "select": { "options": [
                            {"name": "Healthy"},
                            {"name": "Watch"},
                            {"name": "At-Risk"},
                            {"name": "Critical"}
                          ] } },
    "Top Risk Factor":   { "rich_text": {} },
    "Last Scored":       { "date": {} },
    "Stripe Customer":   { "rich_text": {} },
    "PostHog Distinct":  { "rich_text": {} }
  }
```

If no brand parent page exists, `notion-search` for `"{Brand}"` first; if nothing is found, create the parent with `notion-create-pages` at the workspace root, then nest the DB under it.

After creation, **persist the new DB ID back to `.claude/settings.local.json`** under `env.{BRAND}_CUSTOMER_DB`. Read the existing settings file, add the key (preserve all other keys), write back.

Notify the user in chat (first-run only):
> Created new Notion DB **{Brand Name} Customers** and saved its ID as `${BRAND}_CUSTOMER_DB` in `.claude/settings.local.json`. Future runs will reuse this DB — no re-creation. Populate at least the Email, Status, Plan, and MRR columns for existing customers before the next run, or pull them from Stripe in Step 3.

#### Step 2b — Query active customers

Resolve the DB to a `data_source_url` (needed for scoped query):

```
Use mcp__claude_ai_Notion__notion-fetch:
- id: "${BRAND}_CUSTOMER_DB"
```

Extract `data_sources[0].url` from the response. Then query the DB filtered to `Status = "Active"`:

```
Use mcp__claude_ai_Notion__notion-search:
- query: ""
- data_source_url: <data_source_url from above>
- query_type: "internal"
- filter: { "property": "Status", "select": { "equals": "Active" } }
```

Capture for each row: `page_id`, `Email`, `Plan`, `MRR`, `Stripe Customer`, `PostHog Distinct`, prior `Risk Band`. The prior `Risk Band` is critical for the transition logic in Step 5.

If a single-customer ad-hoc run was requested, narrow the query to that customer's row only.

### Step 3 — Pull usage signals from PostHog

For each customer, query PostHog for the usage signals defined in `customer-success.md → Health Score Weights`. The exact event names depend on the brand's product instrumentation. Introspect first if you're unsure which events are available:

```
Use mcp__claude_ai_PostHog__hogql-schema
```

Then run a HogQL query per customer covering the lookback windows in the playbook (typical: 14, 30, 90 days):

```
Use mcp__claude_ai_PostHog__query-run:
- query: {
    "kind": "HogQLQuery",
    "query": "
      SELECT
        countIf(event = '$pageview' AND timestamp > now() - INTERVAL 14 DAY) AS pageviews_14d,
        countIf(event = '<key_feature_event>' AND timestamp > now() - INTERVAL 30 DAY) AS feature_uses_30d,
        countDistinct(toDate(timestamp)) FILTER (WHERE timestamp > now() - INTERVAL 30 DAY) AS active_days_30d,
        max(timestamp) AS last_seen
      FROM events
      WHERE distinct_id = '<posthog_distinct_from_notion>'
        AND timestamp > now() - INTERVAL 90 DAY
    "
  }
```

If `PostHog Distinct` is empty in the Notion row, fall back to matching on `person.properties.email = '<email>'` and Slack-warn that the customer is missing a distinct_id mapping (this hurts score quality).

Capture per customer: `pageviews_14d`, `feature_uses_30d`, `active_days_30d`, `last_seen`. Add any other signals enumerated in the playbook (e.g., support-ticket count, integrations connected, seats activated) — query each only if the playbook calls for it.

### Step 4 — Pull subscription state from Stripe

Stripe answers the "are they actually still paying us, and what direction is the contract going" questions that PostHog can't.

**Stripe is a deferred MCP tool that gates real tools behind OAuth. Load its schema before calling:**

```
Use ToolSearch:
- query: "select:mcp__claude_ai_Stripe__authenticate"
```

After authentication completes, run ToolSearch again with `query: "stripe"` to enumerate the post-auth toolset.

**Authenticate first if not already authenticated** (Stripe MCP is OAuth):

```
Use mcp__claude_ai_Stripe__authenticate
```

(Skip if already authenticated for the active session.)

For each customer, look up the Stripe customer record by `Stripe Customer` ID (from Notion) or by `Email`. Capture:

- Active subscription state (`active` / `past_due` / `canceled` / `paused`)
- Current MRR (sum of subscription item prices, monthly-normalized)
- Recent downgrades (subscription items changed in last 60 days, comparing prior price to current)
- Failed payment attempts in last 30 days
- Upcoming cancellation (`cancel_at_period_end = true`)

If a customer's Stripe state shows `canceled` or `cancel_at_period_end`, override the Risk Band to `Critical` regardless of usage score — they have already given notice.

If a customer is not found in Stripe (e.g., manually invoiced), proceed with usage-only scoring and note in `Top Risk Factor`: `"Stripe lookup failed — usage-only score"`.

### Step 5 — Compute health score per customer-success.md formula

Apply the formula from `customer-success.md → Health Score Weights`. The skill is content-free here — do not invent weights. Typical shape:

- Weighted sum of normalized signal scores (each signal scored 0–100 against its threshold table in the playbook)
- Weights from the playbook (e.g., feature adoption 40%, login frequency 30%, support tickets 15%, subscription health 15%)
- Final score clamped 0–100

Map score to Risk Band per the playbook's banding table. Typical bands:
- **Healthy**: 80–100
- **Watch**: 60–79
- **At-Risk**: 40–59
- **Critical**: 0–39 (or any Stripe override above)

Pick the **single largest negative contributor** to the score and write it to `Top Risk Factor` (e.g., `"No logins in 21 days"`, `"Failed payment 3 days ago"`, `"Used 0 features beyond pageview in 30 days"`). The CS team uses this column as the daily action list — keep it specific and one phrase per row.

### Step 6 — Update Notion customer rows

For each scored customer, update the existing Notion row in `${BRAND}_CUSTOMER_DB`:

```
Use mcp__claude_ai_Notion__notion-update-page:
- page_id: <customer_page_id from Step 2b>
- properties: {
    "Health Score":    <0-100>,
    "Risk Band":       "<Healthy|Watch|At-Risk|Critical>",
    "Top Risk Factor": "<one-line phrase>",
    "Last Scored":     "<today YYYY-MM-DD>",
    "MRR":             <current MRR from Stripe if changed>
  }
```

Skip the Notion write step entirely on dry-run flag.

### Step 7 — Apply intervention playbook + Slack alert on transitions

For each customer whose Risk Band today is **worse** than yesterday's (Healthy → Watch, Watch → At-Risk, anything → Critical):

1. Look up the matching action in `customer-success.md → At-Risk Intervention Playbook` for the new band. The playbook tells the skill what to do — typically: "draft a check-in email with template X, route to CS owner Y, escalate to founder if Critical."
2. If the playbook says "draft a check-in email", produce a Gmail draft using the template wording from the playbook (do not invent copy):

   ```
   Use mcp__claude_ai_Gmail__create_draft:
   - to: <customer.Email>
   - subject: <from playbook template>
   - body: <playbook template body, with {customer_name} / {top_risk_factor} / {plan} substituted>
   ```

3. **Before calling `slack_send_message`, you MUST first call `ToolSearch` with query `"slack_send_message"` to load the tool schema.** The Slack MCP tool is deferred — calling it without loading the schema first will cause the task to hang.

4. Send a per-customer Slack alert to `$SLACK_NOTIFY_USER`:

   ```
   Use mcp__claude_ai_Slack__slack_send_message:
   - channel_id: "$SLACK_NOTIFY_USER"
   - text: "
     ⚠️  [{brand}] {customer_name} dropped to {new_band} (was {prior_band})
     • MRR: ${mrr}/mo — Plan: {plan}
     • Health Score: {score}/100
     • Top Risk: {top_risk_factor}
     • Recommended next action: {playbook_action}
     • Notion: {notion_url}
     "
   ```

Skip alerts entirely on dry-run flag — instead, list what would have been sent at the end of the run.

### Step 8 — Daily Slack summary

After per-customer alerts, send one summary message to `$SLACK_NOTIFY_USER`:

```
Use mcp__claude_ai_Slack__slack_send_message:
- channel_id: "$SLACK_NOTIFY_USER"
- text: "
  📊 [{brand}] Daily Health Report — {DD Mon YYYY}
  • Active customers: {N}
  • Healthy: {h}  •  Watch: {w}  •  At-Risk: {a}  •  Critical: {c}
  • MRR at risk (At-Risk + Critical bands): ${mrr_at_risk}/mo
  • Newly at-risk today: {transitions}
  • Top 3 most at-risk:
      1. {name} — {score}/100 — {top_risk_factor}
      2. {name} — {score}/100 — {top_risk_factor}
      3. {name} — {score}/100 — {top_risk_factor}
  • Notion DB: {db_url}
  "
```

### Step 9 — Save local backup

Save a daily backup file:

```
outputs/{brand}/customers/HealthReport_DDMonYYYY.md
```

Containing the per-customer table (Name / Plan / MRR / Score / Band / Top Risk Factor) plus the summary numbers. This is the audit trail in case Notion is later edited.

---

## Output format

**Save location — local workspace:**
```
outputs/{brand}/customers/
```

**Naming convention:**
```
HealthReport_[DDMonYYYY].md
```

**Output metadata:**
```yaml
---
Date: YYYY-MM-DD
Skill Used: churn-predictor
Brand: {brand}
Active Customers: N
Status: Final
---
```

**Output sections:**
1. **Summary** — counts per band, MRR at risk, newly at-risk count
2. **Customer table** — Name / Plan / MRR / Score / Band / Top Risk Factor / Last Scored
3. **Transitions today** — every customer whose band changed (better or worse)
4. **Top 3 most at-risk** — with playbook recommended action for each

---

## Quality checklist

Before finalizing:

- [ ] `customer-success.md` was read and the Health Score formula applied verbatim — no invented weights or thresholds
- [ ] Every active customer in `${BRAND}_CUSTOMER_DB` has a fresh `Last Scored` date of today
- [ ] Risk Band uses only the four allowed values (Healthy / Watch / At-Risk / Critical)
- [ ] Stripe override applied: any customer in `canceled` or `cancel_at_period_end` is forced to Critical
- [ ] `Top Risk Factor` is one specific phrase per customer — never blank, never generic ("low engagement" without a number is not acceptable)
- [ ] Slack per-customer alerts fired only on **band transitions worse than yesterday**, never on stable bands
- [ ] Intervention copy comes from `customer-success.md → At-Risk Intervention Playbook` — never invented
- [ ] `ToolSearch` was called for `slack_send_message` before any Slack write
- [ ] Daily summary sent to `$SLACK_NOTIFY_USER` even on a quiet day (zero transitions still gets a 1-line "all clear" digest)
- [ ] Local backup saved to `outputs/{brand}/customers/HealthReport_DDMonYYYY.md`
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "churn-predictor"
- brand: "<active-brand>"
- status: "<success|failed>"
- summary: "<1 line, <200 chars — e.g. 'Scored 47 active customers, 3 newly at-risk, $4.2k MRR at risk'>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "active_customers": 47,
    "band_counts": { "healthy": 28, "watch": 11, "at_risk": 5, "critical": 3 },
    "mrr_total": 18420,
    "mrr_at_risk": 4180,
    "transitions_worse": 3,
    "transitions_better": 1,
    "alerts_sent": 3,
    "drafts_created": 3,
    "top_at_risk": [
      { "name": "Acme Co", "score": 28, "band": "Critical", "top_risk_factor": "Failed payment 3 days ago" },
      { "name": "Beta Ltd", "score": 35, "band": "Critical", "top_risk_factor": "No logins in 21 days" },
      { "name": "Gamma Inc", "score": 47, "band": "At-Risk", "top_risk_factor": "Used 0 features in 30 days" }
    ],
    "deliverable": "HealthReport_DDMonYYYY.md",
    "output_path": "outputs/{brand}/customers/"
  }
```
