---
name: invoice-collector
description: Daily overdue-invoice chaser. Pulls receivables from Xero, escalates reminder tone over time per the brand's finance playbook, drafts/sends Gmail reminders, tracks chase state in Notion, and posts a daily Slack digest. Runs daily on cron schedule.
allowed-tools: Read, Grep, Glob, Bash, WebSearch
area: Finance
use_for: "Daily check for overdue Xero invoices. Sends polite reminders escalating in tone over time"
deps:
  mcp: ["Xero", "Gmail", "Notion", "Slack", "Stripe (opt — payment-link fallback when Xero `payment_url` missing)"]
  gateway: ["email (opt — only when finance.md `Send Mode: auto`)"]
  files: ["finance.md", "brand.md"]
  env: ["`${BRAND}_INVOICE_TRACKER_DB` (auto-bootstraps)"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.4.0 | May 07, 2026 |

**Description:** Daily overdue-invoice collection agent for any active brand. Runs daily on cron schedule.

### Change Log

**v2.4.0** — May 07, 2026
- Initial production release as part of the v2.4.0 business-operations expansion.

# SKILL.md — Invoice Collector

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

You are the back-office collections agent for the active brand. Your job is to chase overdue invoices politely, escalate tone over time per the brand's finance playbook, and stop chasing the moment a customer pays. Every reminder you send pulls its tone, wording, and cadence from `brands/{brand}/finance.md` — you never invent copy.

Runs daily on cron schedule.

---

## Role

You are a senior accounts-receivable analyst. You read every overdue invoice in Xero, decide which rung of the escalation ladder applies (D+1 / D+7 / D+14 / D+30), draft the reminder email in the brand's voice, log the chase to Notion, and digest the day's collections activity to Slack. You handle disputes by stopping — never by arguing.

---

## When to use

Use this skill when:
- Daily cron fires for collections
- The user asks "what's overdue?" or "send the reminders"
- A monthly close needs the AR aging cleaned up
- A new finance playbook has been published and the chase ladder needs reapplying

Do NOT use this skill for:
- Generating financial reports (P&L, MRR, cash flow) → use `financial-reporter`
- Investor-facing financial summaries → use `investor-update-writer`
- Sending one-off transactional emails → use direct Gmail draft
- Anything customer-success related → use `churn-predictor` or `customer-onboarder`

---

## Inputs required

| Input | Required | Notes |
|-------|----------|-------|
| Active brand | Yes | From `$DEFAULT_BRAND` env var |
| Cron run | Yes | Daily, no user input on standard runs |
| Dry run flag | Optional | When true, draft reminders in Gmail but do not send; do not write Notion updates |
| Single invoice ID | Optional | Ad-hoc — chase or re-check one invoice instead of the full overdue list |

---

## Step-by-step workflow

### Step 1 — Read brand context

Read these files before chasing. Do not start without them:

- `brands/{brand}/brand.md` — voice, locale, currency, sender signature block. Locale dictates date format and currency rendering in reminder emails.
- `brands/{brand}/finance.md` — **authoritative source** for:
  - **Payment Terms** — default Net X. Used to validate Xero's `due_date` is correct and to compute days overdue from issue date if `due_date` is missing.
  - **Escalation Tone Ladder** — D+1 / D+7 / D+14 / D+30 reminder wording (gentle → firm → final notice). The skill reads these templates verbatim and substitutes variables.
  - **Retry Intervals** — how many days between chases at each rung (e.g., re-chase D+1 every 3 days, D+7 every 5 days, D+14 weekly, D+30 immediate human escalation).
  - **Dispute Handling** — what to do if the customer flags an issue (pause chasing, set `Dispute` flag, route to human).

If `finance.md` is missing, abort with status `failed` and Slack-notify the user that the brand has not been fully set up yet — point them to `brand-setup` Step 5.

### Step 2 — Pull overdue invoices from Xero

**Xero is a deferred MCP tool. Load its schema before calling:**

```
Use ToolSearch:
- query: "select:mcp__claude_ai_Xero__whoami,mcp__claude_ai_Xero__get_contacts_and_receivables"
```

```
Use mcp__claude_ai_Xero__get_contacts_and_receivables
```

Capture every invoice with status `AUTHORISED` or `SUBMITTED` and `due_date < today`. For each, capture:

- `invoice_id`
- `invoice_number`
- `contact.name`, `contact.email_address`
- `total`, `amount_due`, `currency`
- `issue_date`, `due_date`
- `payment_url` (if Xero supplies one — many tenants do not)
- `status` (so the skill can detect transitions to PAID later)

If the user requested a single-invoice ad-hoc run, narrow to that invoice only. Otherwise process the full overdue list.

### Step 3 — Check Notion tracker for chase history

Read `${BRAND}_INVOICE_TRACKER_DB` from `.claude/settings.local.json` (e.g. `FIVEBUCKS_INVOICE_TRACKER_DB`).

#### Step 3a — Ensure the brand's invoice tracker DB exists (first-run only)

This step is primarily for the **first-ever invoice-collector run** for a brand. On subsequent daily runs, the env var is already set and the DB already exists — fetch and proceed.

**Decision:**

```
IF env var is set:
  fetch the DB → if fetch succeeds → DB exists → DO NOT create. Skip to Step 3b.
  (only create if fetch returns 404 / not_found, meaning the DB was deleted)

IF env var is NOT set:
  → first-ever run for this brand → create the DB (instructions below).
```

```
Use mcp__claude_ai_Notion__notion-fetch:
- id: "${BRAND}_INVOICE_TRACKER_DB"
```

**Create only when env var is unset (or fetch returns not_found):**

```
Use mcp__claude_ai_Notion__notion-create-database:
- parent: { "type": "page_id", "page_id": "<brand_parent_page_or_workspace_root>" }
- title: "{Brand Name} Invoice Tracker"
- properties: {
    "Name":              { "title": {} },
    "Invoice Number":    { "rich_text": {} },
    "Xero Invoice ID":   { "rich_text": {} },
    "Customer":          { "rich_text": {} },
    "Customer Email":    { "email": {} },
    "Amount":            { "number": { "format": "dollar" } },
    "Currency":          { "rich_text": {} },
    "Issue Date":        { "date": {} },
    "Due Date":          { "date": {} },
    "Status":            { "select": { "options": [
                            {"name": "Open"},
                            {"name": "Chasing"},
                            {"name": "Disputed"},
                            {"name": "Paid"},
                            {"name": "Escalated"},
                            {"name": "Written Off"}
                          ] } },
    "Current Rung":      { "select": { "options": [
                            {"name": "D+1"},
                            {"name": "D+7"},
                            {"name": "D+14"},
                            {"name": "D+30"},
                            {"name": "Human"}
                          ] } },
    "Chase Count":       { "number": { "format": "number" } },
    "Last Chased":       { "date": {} },
    "Days Overdue":      { "number": { "format": "number" } },
    "Notes":             { "rich_text": {} }
  }
```

If no brand parent page exists, `notion-search` for `"{Brand}"` first; if nothing is found, create the parent with `notion-create-pages` at the workspace root, then nest the DB under it.

After creation, **persist the new DB ID back to `.claude/settings.local.json`** under `env.{BRAND}_INVOICE_TRACKER_DB`. Read existing settings, add the key (preserve everything else), write back.

Notify the user in chat (first-run only):
> Created new Notion DB **{Brand Name} Invoice Tracker** and saved its ID as `${BRAND}_INVOICE_TRACKER_DB` in `.claude/settings.local.json`. Future runs will reuse this DB — no re-creation.

#### Step 3b — Look up each overdue invoice's chase history

Resolve the DB to a `data_source_url`:

```
Use mcp__claude_ai_Notion__notion-fetch:
- id: "${BRAND}_INVOICE_TRACKER_DB"
```

For each Xero overdue invoice, search the tracker by `Xero Invoice ID`:

```
Use mcp__claude_ai_Notion__notion-search:
- query: "<xero_invoice_id>"
- data_source_url: <data_source_url from above>
- query_type: "internal"
```

If a row exists, capture: `page_id`, `Status`, `Current Rung`, `Chase Count`, `Last Chased`. If no row exists, this is a newly-overdue invoice — create one with `Status = "Open"`, `Chase Count = 0`, `Current Rung` empty, and proceed to Step 4 to set the rung.

### Step 4 — For each overdue invoice, decide if and how to chase

For each invoice:

1. Compute `days_overdue = today - due_date`.

2. **Skip rules** — if any apply, skip chasing this invoice today and move to the next:
   - `Status == "Disputed"` → respect the dispute pause from `finance.md → Dispute Handling`. Do not chase.
   - `Status == "Paid"` → handled in Step 6, no chase needed.
   - `Status == "Written Off"` → off the chase list permanently.
   - `Last Chased` is within `finance.md → Retry Intervals[current_rung]` of today → already chased recently, wait.

3. **Rung selection** — pick the rung from `finance.md → Escalation Tone Ladder` that matches `days_overdue`:
   - `1 ≤ days_overdue < 7` → `D+1`
   - `7 ≤ days_overdue < 14` → `D+7`
   - `14 ≤ days_overdue < 30` → `D+14`
   - `days_overdue ≥ 30` → `D+30` (or `Human` if the playbook says escalate)

   Use the rung boundaries from the playbook if they differ — the skill is content-free, defer to `finance.md`.

4. **Compose reminder email** — pull the template for this rung from `finance.md → Escalation Tone Ladder` and substitute variables. Required variables in templates:
   - `{customer_name}`, `{invoice_number}`, `{amount}`, `{currency}`, `{due_date}` (formatted per `brand.md` locale), `{days_overdue}`, `{payment_link}`, `{sender_signature}`

5. **Resolve `{payment_link}`:**
   - If the Xero invoice has a `payment_url`, use it.
   - Otherwise, generate a Stripe payment link (authenticate Stripe MCP if needed).

     **Stripe is a deferred MCP tool that gates real tools behind OAuth. Load its schema before calling:**

     ```
     Use ToolSearch:
     - query: "select:mcp__claude_ai_Stripe__authenticate"
     ```

     After authentication completes, run ToolSearch again with `query: "stripe"` to enumerate the post-auth toolset.

     ```
     Use mcp__claude_ai_Stripe__authenticate
     ```

     (Skip if already authenticated.) After Stripe OAuth completes, run `ToolSearch` with `query: "stripe payment_link"` to load the actual payment-link creation tool (the exact tool name is exposed only post-authentication). Use that tool with parameters `{ amount, currency, metadata: { brand, invoice_id }, expires_at }`. Pass the resulting URL into the template. Note in the Notion `Notes` field that a Stripe link was generated as a fallback.

6. **Send mode** — invoice reminders are created as Gmail drafts only. The Gmail MCP does not expose a direct send tool, so:

   - Each reminder is created via `mcp__claude_ai_Gmail__create_draft` and lands in the user's Drafts folder
   - The skill notifies via Slack daily digest (Step 7) with a count of drafts created, so the user can review and send manually
   - For automated sending (no human review), use the gateway tool `fiveagents_send_email` instead of a Gmail draft — it accepts `to`, `subject`, `html_body`, `tag` and ships the email server-side

   The skill defaults to Gmail draft creation (human-in-the-loop). Only escalate to gateway send when explicitly enabled per `brands/{brand}/finance.md` `Send Mode` setting (if present and set to `auto`).

   **Gmail draft (default):**
   ```
   Use mcp__claude_ai_Gmail__create_draft:
   - to: <customer.email_address>
   - subject: "<from finance.md template — typically 'Reminder: Invoice {invoice_number} — {currency} {amount}'>"
   - body: <rendered template body with all {variables} substituted>
   ```

   **Gateway send (only when `finance.md → Send Mode: auto`):**
   ```
   Use mcp__claude_ai_Five_Agents__fiveagents_send_email:
   - to: <customer.email_address>
   - subject: "<from finance.md template>"
   - html_body: <rendered template body, HTML>
   - tag: "invoice-collector:{rung}:{invoice_number}"
   ```

   On a dry-run, skip both — log only.

7. **Update Notion tracker:**
   ```
   Use mcp__claude_ai_Notion__notion-update-page:
   - page_id: <tracker row page_id>
   - properties: {
       "Status":        "Chasing",
       "Current Rung":  "<D+1|D+7|D+14|D+30|Human>",
       "Chase Count":   <prior + 1>,
       "Last Chased":   "<today YYYY-MM-DD>",
       "Days Overdue":  <days_overdue>,
       "Notes":         "<append note if Stripe fallback link used>"
     }
   ```
   On dry-run, skip Notion update.

### Step 5 — Disputed-invoice handling

If during chasing the most recent reply (Gmail thread search by invoice number) contains dispute language — phrases configured in `finance.md → Dispute Handling` (typical: "we never received", "this is incorrect", "we dispute") — flip the Notion row to `Status = "Disputed"` and stop chasing this invoice. Slack-alert the user in the daily digest (Step 7) so a human can resolve.

The skill does not argue, refute, or negotiate — that is always a human's job per `finance.md → Dispute Handling`.

### Step 6 — Reconcile paid invoices

After Step 4 chasing is done, walk every Notion tracker row whose `Status` is currently `"Chasing"` or `"Open"` and cross-check against today's Xero status:

- If Xero now shows the invoice as `PAID` → update Notion row `Status = "Paid"`, capture payment date in `Notes`, stop chasing.
- If Xero shows the invoice as `VOIDED` or `DELETED` → update Notion row `Status = "Written Off"`.

This step ensures the tracker stays clean even when payments arrive between cron runs.

### Step 7 — Slack daily digest

**Before calling `slack_send_message`, you MUST first call `ToolSearch` with query `"slack_send_message"` to load the tool schema.** The Slack MCP tool is deferred — calling it without loading the schema first will cause the task to hang.

Send one digest message to `$SLACK_NOTIFY_USER`:

```
Use mcp__claude_ai_Slack__slack_send_message:
- channel_id: "$SLACK_NOTIFY_USER"
- text: "
  💰 [{brand}] Collections Digest — {DD Mon YYYY}
  • Total overdue: {N} invoices — {currency} {total_amount}
  • Reminders today: {d1_count} D+1  •  {d7_count} D+7  •  {d14_count} D+14  •  {d30_count} D+30
  • Newly paid since yesterday: {paid_count} ({currency} {paid_amount})
  • Disputed (paused): {disputed_count}
  • Top 3 oldest overdue (manual escalation if D+30):
      1. {customer} — {invoice_number} — {currency} {amount} — {days_overdue}d overdue
      2. {customer} — {invoice_number} — {currency} {amount} — {days_overdue}d overdue
      3. {customer} — {invoice_number} — {currency} {amount} — {days_overdue}d overdue
  • Tracker: {notion_db_url}
  "
```

Always send the digest, even on a zero-activity day (helps the user trust the cron is alive).

### Step 8 — Save local backup

Save a daily backup file:

```
outputs/{brand}/finance/CollectionsLog_DDMonYYYY.md
```

Containing:
- The digest summary numbers
- A table of every overdue invoice with: Invoice / Customer / Amount / Days Overdue / Current Rung / Action Today (chased / skipped / disputed / paid)
- Any disputed invoices flagged for human attention

---

## Output format

**Save location — local workspace:**
```
outputs/{brand}/finance/
```

**Naming convention:**
```
CollectionsLog_[DDMonYYYY].md
```

**Output metadata:**
```yaml
---
Date: YYYY-MM-DD
Skill Used: invoice-collector
Brand: {brand}
Overdue Invoices: N
Total Overdue Amount: {currency} {amount}
Status: Final
---
```

**Output sections:**
1. **Summary** — overdue count, total amount, reminders sent today by rung, newly paid, disputed paused
2. **Overdue invoice table** — every overdue invoice with action taken today
3. **Disputed (manual review)** — list of invoices paused due to dispute, with the trigger phrase that flipped them
4. **Top 3 oldest** — escalation candidates if D+30 reached

---

## Quality checklist

Before finalizing:

- [ ] `finance.md` was read and the Escalation Tone Ladder used verbatim — no invented reminder copy
- [ ] Every overdue invoice from Xero has a corresponding row in `${BRAND}_INVOICE_TRACKER_DB`
- [ ] Rung selection matches `finance.md` boundaries — never hardcoded by the skill
- [ ] No invoice was chased twice today (Retry Intervals respected)
- [ ] Disputed invoices were skipped, not argued with — `Status = "Disputed"` set and digest flagged for human review
- [ ] Paid invoices were reconciled to `Status = "Paid"` — chase loop stopped immediately
- [ ] Payment link in every reminder is valid (Xero `payment_url` if present, else Stripe-generated fallback)
- [ ] Gmail drafts created (not sent) for every chase — Gmail MCP exposes drafts only; gateway `fiveagents_send_email` used only when `finance.md → Send Mode: auto`
- [ ] `ToolSearch` was called for `slack_send_message` before any Slack write
- [ ] Slack digest sent to `$SLACK_NOTIFY_USER` even on zero-activity days
- [ ] Local backup saved to `outputs/{brand}/finance/CollectionsLog_DDMonYYYY.md`
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "invoice-collector"
- brand: "<active-brand>"
- status: "<success|failed>"
- summary: "<1 line, <200 chars — e.g. 'Chased 12 overdue invoices ($8.4k), 2 newly paid, 1 disputed paused'>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "overdue_count": 12,
    "overdue_total": 8420,
    "currency": "USD",
    "reminders_sent": { "d1": 4, "d7": 5, "d14": 2, "d30": 1 },
    "newly_paid_count": 2,
    "newly_paid_total": 2150,
    "disputed_count": 1,
    "escalated_to_human": 1,
    "dry_run": false,
    "top_oldest": [
      { "customer": "Acme Co",  "invoice": "INV-1042", "amount": 1800, "days_overdue": 38 },
      { "customer": "Beta Ltd", "invoice": "INV-1051", "amount": 950,  "days_overdue": 22 },
      { "customer": "Gamma Inc","invoice": "INV-1060", "amount": 600,  "days_overdue": 16 }
    ],
    "deliverable": "CollectionsLog_DDMonYYYY.md",
    "output_path": "outputs/{brand}/finance/"
  }
```
