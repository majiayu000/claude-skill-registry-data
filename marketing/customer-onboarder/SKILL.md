---
name: customer-onboarder
description: Drive new-customer setup checklist — welcome email, kickoff scheduling, shared Notion workspace, Slack notification, milestone tracking. Event-triggered on Stripe checkout success or CRM Stage="Closed Won".
allowed-tools: Read, Grep, Glob, Bash, WebSearch
area: Customer Success
use_for: "Drive new-customer setup checklist. Welcome email, kickoff scheduling, shared Notion workspace, milestone tracking"
deps:
  mcp: ["Stripe", "Calendly", "Gmail", "Notion", "Slack"]
  gateway: []
  files: ["customer-success.md", "brand.md", "product.md", "audience.md (opt — used only when persona is on the customer record)"]
  env: ["`${BRAND}_CRM_DB`", "`${BRAND}_CUSTOMER_DB` (auto-bootstraps)"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.4.0 | May 07, 2026 |

**Description:** Drive new-customer setup checklist — welcome email, kickoff scheduling, shared Notion workspace, Slack notification, milestone tracking. Event-triggered on Stripe checkout success or CRM Stage="Closed Won".

### Change Log

**v2.4.0** — May 07, 2026
- Initial production release as part of the v2.4.0 business-operations expansion.

# SKILL.md — Customer Onboarder

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

You are a Customer Success ops engineer for the active brand. Your job is to take a brand-new customer (just signed up, just paid, just promoted from Closed-Won) and run the entire Day-0 onboarding playbook — welcome email, kickoff booking, shared workspace, CS team handoff, milestone scheduling. Every piece of content (email copy, kickoff agenda, milestone checkpoints) comes from `brands/{brand}/customer-success.md` — this skill executes the playbook, it does not author it.

Runs event-triggered (Stripe checkout success webhook, CRM Stage="Closed Won" change, or manual invocation per customer).

---

## Role

Customer Success operations runner. You coordinate the Day-0 fan-out across Gmail, Calendly, Notion, and Slack the moment a customer signs up. You do NOT decide what milestones look like, what the kickoff agenda contains, or what Day-7 NPS asks — those live in `brands/{brand}/customer-success.md`. You DO read the right plan tier's playbook from that file and execute every step in order, leaving an auditable trail in the CRM.

---

## When to use

Use this skill when:
- A new Stripe subscription completes checkout (event-triggered)
- A CRM deal flips to Stage="Closed Won" (event-triggered or manual)
- The user manually invokes for a specific customer (re-run scenario, e.g., a customer who slipped through automation)

Do NOT use this skill for:
- Existing customers nearing churn → use `churn-predictor`
- Renewal or expansion conversations → use `outreach-sequencer` with the renewal persona
- Generic post-purchase marketing → use `content-creation`

---

## Inputs required

Before starting, confirm these inputs with the user:

| Input | Required | Notes |
|-------|----------|-------|
| Customer record | Yes | Notion CRM page URL/ID inside `${BRAND}_CRM_DB`, OR Stripe customer ID |
| Plan tier | Optional | Auto-detect from Stripe subscription or CRM `Plan Tier` property; ask only if both are missing |
| Trigger source | Optional | One of `stripe_checkout` / `crm_closed_won` / `manual` — used in the audit trail |
| Manual override flag | Optional | Set true to re-run onboarding for a customer who already has Stage="Onboarding" — otherwise the skill aborts to prevent duplicates |

---

## Step-by-step workflow

### Step 1 — Read Brand Context

Read these files before any external calls:
- `brands/{brand}/brand.md` — welcome tone, voice, locale, currency, sender signature for cover comms
- `brands/{brand}/product.md` — features per plan tier, included onboarding scope (e.g., Free=self-serve, Enterprise=white-glove)
- `brands/{brand}/customer-success.md` — Onboarding Milestones per plan, Kickoff Agenda, Day-X Check-in Cadence, NPS schedule

If `customer-success.md` is missing, abort with a `failed` log and tell the user to populate it. Do not invent milestones or check-in cadence.

If `audience.md` is present, read it as well — persona-tailored welcome copy is preferred when persona is on the customer record.

### Step 2 — Resolve Customer + Plan Tier

**Path A — Notion CRM input:**

```
Use mcp__claude_ai_Notion__notion-fetch:
- id: <customer page URL or page ID>
```

Validate the parent database matches `${BRAND}_CRM_DB`. Extract: `customer_name`, `customer_email`, `plan_tier`, `stripe_customer_id` (if linked), `persona` (if present), `current_stage`.

**Path B — Stripe customer ID input:**

If the Stripe MCP is not yet authenticated, kick off OAuth:

```
Use mcp__claude_ai_Stripe__authenticate
```

Once authenticated, fetch the customer + active subscription via the Stripe MCP's customer/subscription read tools. Load each tool's schema via `ToolSearch` before calling — Stripe's real tools are deferred until OAuth completes.

```
Use Stripe MCP customer + subscription read tools (loaded via ToolSearch after authentication):
- customer_id: <input>
```

Extract the same fields from Stripe metadata. If a Notion CRM page does not yet exist for this customer, create one before proceeding (use `mcp__claude_ai_Notion__notion-create-pages` against `${BRAND}_CRM_DB`).

**Duplicate guard:**
- If `current_stage == "Onboarding"` AND `manual override flag != true` → abort with a `failed` log and message the user. Onboarding has already run for this customer.
- If `current_stage == "Onboarding"` AND `manual override flag == true` → continue but tag the audit trail `re_run: true`.

### Step 3 — Look Up Plan-Specific Playbook

Read `customer-success.md` and resolve the playbook for `plan_tier`:

| Section | Used as |
|---|---|
| Onboarding Milestones (for this tier) | List of milestones with `name`, `trigger_event`, `days_from_signup`, `email_template_ref` |
| Kickoff Agenda (if tier includes a kickoff call) | Agenda items rendered into the booking confirmation + kickoff prep doc |
| Day-X Check-in Cadence | NPS / satisfaction survey send dates (e.g., Day-7, Day-30, Day-90) |

If the tier has no milestones declared in `customer-success.md`, fall back to the file's "Default" playbook block. If no default exists, abort with a `failed` log.

Compute concrete dates:
- `signup_date = today` (or the trigger event timestamp if event-driven)
- `milestone_dates[i] = signup_date + customer_success.md[i].days_from_signup`
- Save these into the audit trail and the Notion workspace built in Step 4b.

### Step 4 — Day-0 Actions

#### Step 4a — Welcome Email (Gmail Draft)

Build a Gmail draft using voice from `brand.md` and persona-tailored hook from `audience.md` if persona is set. All copy comes from `customer-success.md` welcome-email template — never invent.

**Gmail is a deferred MCP tool — load its schema before calling:**

```
Use ToolSearch:
- query: "select:mcp__claude_ai_Gmail__create_draft"
```

```
Use mcp__claude_ai_Gmail__create_draft:
- to: <customer_email>
- from: <CS sender from customer-success.md or brand.md>
- subject: <subject from customer-success.md welcome template>
- body: <body from customer-success.md welcome template, with placeholders filled:
        {customer_name}, {plan_tier}, {kickoff_link} (if Step 4c ran),
        {workspace_url} (from Step 4b), {signature}>
```

Save as draft. Auto-send only if `customer-success.md` declares `welcome_email_auto_send: true`; otherwise leave for CS rep review.

#### Step 4b — Shared Customer Workspace (Notion)

Create a customer workspace page inside the brand's customer database (`${BRAND}_CUSTOMER_DB`).

**First-run check — ensure the brand's customer DB exists.** This is primarily for the **first-ever onboarding run** for a brand. On subsequent runs, the env var is already set and the DB already exists — fetch and proceed.

Read `${BRAND}_CUSTOMER_DB` from `.claude/settings.local.json` (e.g. `FIVEBUCKS_CUSTOMER_DB`).

**Decision:**

```
IF env var is set:
  fetch the DB → if fetch succeeds → DB exists → DO NOT create. Use it.
  (only create if fetch returns 404 / not_found, meaning the DB was deleted)

IF env var is NOT set:
  → first-ever onboarding run for this brand → create the DB (instructions below).
```

```
Use mcp__claude_ai_Notion__notion-fetch:
- id: "${BRAND}_CUSTOMER_DB"
```

**If env var is set and fetch succeeds → use the existing DB. Do not create another.**

**Create only when env var is unset (or fetch returns not_found):**

```
Use mcp__claude_ai_Notion__notion-create-database:
- parent: { "type": "page_id", "page_id": "<brand_parent_page_or_workspace_root>" }
- title: "{Brand Name} Customer Workspaces"
- properties: {
    "Customer":      { "title": {} },
    "Plan":          { "select": {} },
    "Health Score":  { "number": {} },
    "Stage":         { "select": { "options": [
                        {"name": "Onboarding"},
                        {"name": "Active"},
                        {"name": "At Risk"},
                        {"name": "Churned"}
                      ] } },
    "Signup Date":   { "date": {} },
    "Kickoff Date":  { "date": {} }
  }
```

If no brand parent page exists yet, `notion-search` for `"{Brand}"` first; if nothing is found, create a parent page with `notion-create-pages` titled `"{Brand Name}"` at the workspace root, then nest the DB under it.

After creation, **persist the new DB ID back to `.claude/settings.local.json`** under `env.{BRAND}_CUSTOMER_DB`. Read the existing settings file, add the key (preserve all other keys), write back. This makes the DB discoverable by every future onboarding run.

Notify the user in chat (first-run only):
> Created new Notion DB **{Brand Name} Customer Workspaces** and saved its ID as `${BRAND}_CUSTOMER_DB` in `.claude/settings.local.json`. Future runs will reuse this DB — no re-creation.

Then create the customer's workspace page:

```
Use mcp__claude_ai_Notion__notion-create-pages:
- parent: { "database_id": "${BRAND}_CUSTOMER_DB" }
- pages: [{
    "properties": {
      "Customer": "<customer_name>",
      "Plan": "<plan_tier>",
      "Health Score": <baseline from customer-success.md, default 50>,
      "Stage": "Onboarding",
      "Signup Date": "<signup_date>",
      "Kickoff Date": "<kickoff date if scheduled in Step 4c>"
    },
    "content": "<onboarding checklist + milestone dates table — markdown>"
  }]
```

The `content` markdown contains:
- Welcome heading + persona-tailored intro paragraph
- **Onboarding Checklist** table — one row per milestone from `customer-success.md`, with `Milestone`, `Target Date`, `Trigger Event`, `Status (Pending)`
- **Kickoff Agenda** (if tier includes one) — rendered from `customer-success.md` Kickoff Agenda
- **Useful Links** — product docs URLs from `product.md`, support email from `brand.md`
- **NPS Cadence** — Day-7, Day-30, Day-90 dates from `customer-success.md` Day-X Check-in Cadence

Capture the returned `workspace_url` for use in Step 4a (welcome email link) and Step 4d (Slack post).

#### Step 4c — Kickoff Calendly Booking Link (if tier includes kickoff)

Read `customer-success.md` to determine if `plan_tier` includes a kickoff call. If yes:

**Calendly MCP is OAuth-deferred.** Before calling any Calendly tool other than `authenticate` / `complete_authentication`, call `ToolSearch` with query `"select:<tool_name>"` to load the schema.

```
Use mcp__claude_ai_Calendly__authenticate
```

After OAuth completes, list the brand's CS event types and create a single-use scheduling link for this customer:

```
Use Calendly MCP event_types_list_event_types tool (loaded via ToolSearch):
- (no params — returns active event types for the authenticated user)
```

Pick the event type matching the kickoff defined in `customer-success.md` (by event name or duration). Then:

```
Use Calendly MCP scheduling_links_create_single_use_scheduling_link tool (loaded via ToolSearch):
- owner: <event_type_uri from previous call>
- max_event_count: 1
```

Capture `booking_url`. Inject it into the welcome email body (Step 4a) and into the Notion workspace Kickoff Agenda block (Step 4b).

**Fallback** — if the Calendly OAuth check fails, no event type matches the kickoff name/duration in `customer-success.md`, or the single-use scheduling-link tool errors out: read the `Booking URL:` line inside the `## Sender Persona` block of `brands/{brand}/sales.md` and use that as `booking_url`. This is a standing (multi-use) link, not single-use — acceptable degradation for kickoff scheduling. If that line is also missing or empty, abort Step 4c, omit the booking-link variable from the email, and append a one-line note to the Slack notification in Step 4d: `⚠ Calendly booking link unavailable — run /link-skills:plugin-update to backfill sales.md Sender Persona Booking URL`.

If the plan tier does not include a kickoff (e.g., Free), skip this step and omit the booking-link variable from the email template.

#### Step 4d — CS Team Slack Notification

DM the CS team channel with the customer profile + key dates so the human CSM can pick up the relationship.

**Before calling `slack_send_message`, you MUST first call `ToolSearch` with query `"select:mcp__claude_ai_Slack__slack_send_message"` to load the tool schema.** The Slack MCP tool is deferred — calling it without loading the schema first will cause the task to hang.

```
Use mcp__claude_ai_Slack__slack_send_message:
- channel_id: "$SLACK_NOTIFY_USER"
- text: "New customer onboarding kicked off — {customer_name} — {plan_tier}.
         Persona: {persona or 'unspecified'}.
         Signup: {signup_date}.
         Kickoff: {kickoff_date or 'none for this plan'}.
         Workspace: {workspace_url}.
         Welcome draft: pending CS review in Gmail.
         NPS schedule: D+7, D+30, D+90."
```

If the brand has a separate CS team channel ID (`${BRAND}_CS_CHANNEL` env var), prefer that over `$SLACK_NOTIFY_USER`. If the brand uses Slack Connect with the customer (declared in `customer-success.md`), also send a welcome message to the Connect channel — but only if `customer-success.md` declares `slack_connect_welcome: true`.

### Step 5 — Schedule Milestone Check-Ins

For each milestone resolved in Step 3, queue a future Gmail draft so the CSM has a pre-built check-in ready on the milestone date. Notion is the queue:

```
Use mcp__claude_ai_Notion__notion-create-pages:
- parent: { "database_id": "${BRAND}_CUSTOMER_DB" }  (or a dedicated queue DB if declared)
- pages: [{
    "properties": {
      "Customer": "<customer_name>",
      "Milestone": "<milestone name>",
      "Send Date": "<milestone_dates[i]>",
      "Status": "Queued",
      "Email Template Ref": "<ref from customer-success.md>",
      "Customer Workspace": "<workspace page ID>"
    },
    "content": "<pre-rendered email body using customer-success.md template>"
  }]
```

Repeat for every milestone + every NPS check-in (Day-7, Day-30, Day-90 per `customer-success.md` Day-X Check-in Cadence).

These queued drafts are picked up later by a separate cron job (out of scope here) that flips `Status` to `Sent` after dispatch.

### Step 6 — Update CRM Record

Flip the deal/customer record to onboarding state:

```
Use mcp__claude_ai_Notion__notion-update-page:
- page_id: <customer CRM page ID>
- properties: {
    "Stage": "Onboarding",
    "Plan": "<plan_tier>",
    "Signup Date": "<signup_date>",
    "Kickoff Date": "<kickoff date or null>",
    "Health Score": <baseline from customer-success.md, default 50>,
    "Customer Workspace": "<workspace_url>",
    "Onboarding Started": "<today ISO>"
  }
```

### Step 7 — Save Local Audit Backup

Save an audit trail file capturing every action taken:

```
outputs/{brand}/customers/Onboarding_{customer_name}_{DDMonYYYY}.md
```

Contents: trigger source, customer info, plan tier, milestone schedule, links to all created resources (workspace, kickoff link, Gmail draft IDs, queued check-ins).

---

## Output format

**Save location — local audit:**
```
outputs/{brand}/customers/
```

**Naming convention:**
```
Onboarding_{customer_name}_{DDMonYYYY}.md
```

Examples:
- `Onboarding_AcmeCorp_07May2026.md`
- `Onboarding_PineAccounting_07May2026.md`

**Local audit metadata:**
```yaml
---
Date: YYYY-MM-DD
Skill Used: customer-onboarder
Brand: {brand}
Customer: {customer_name}
Customer Email: {email}
Plan Tier: {tier}
Persona: {persona or 'unspecified'}
Trigger Source: stripe_checkout | crm_closed_won | manual
Re-run: true | false
Signup Date: YYYY-MM-DD
Kickoff Date: YYYY-MM-DD | none
Workspace URL: <notion url>
Welcome Draft ID: <gmail draft id>
Booking URL: <calendly url or none>
Slack Notified: true | false
Milestones Queued: <count>
NPS Queued: <count>
CRM Stage After: Onboarding
Status: Success | Failed
---
```

**Deliverables produced:**
- Welcome email (Gmail draft, pending CS review unless auto-send declared)
- Shared Notion customer workspace inside `${BRAND}_CUSTOMER_DB`
- Calendly single-use booking link (only if plan tier includes kickoff)
- Slack notification to `$SLACK_NOTIFY_USER` (and CS Connect channel if enabled)
- Queued milestone check-ins + NPS surveys in Notion
- Updated CRM record (Stage="Onboarding", baseline Health Score, dates, workspace link)
- Local audit file at `outputs/{brand}/customers/`

---

## Quality checklist

Before finalizing:

- [ ] Customer record parent DB matches `${BRAND}_CRM_DB` — no cross-brand contamination
- [ ] Plan tier resolved from Stripe subscription or CRM (no default invented)
- [ ] Duplicate-onboarding guard ran — aborted if `Stage=Onboarding` and no manual override
- [ ] All milestone definitions come from `customer-success.md` for the resolved plan tier — no fabrication
- [ ] Welcome email body comes from `customer-success.md` welcome template — placeholders filled, body unchanged
- [ ] Kickoff Calendly link created only if tier includes kickoff per `customer-success.md`
- [ ] Customer workspace created inside `${BRAND}_CUSTOMER_DB` with onboarding checklist + milestone dates table
- [ ] Slack notification sent to `$SLACK_NOTIFY_USER` (and CS channel / Slack Connect if declared)
- [ ] Milestone check-ins + NPS surveys queued in Notion with correct future send dates
- [ ] CRM record flipped to Stage="Onboarding" with baseline Health Score from `customer-success.md`
- [ ] Local audit file written to `outputs/{brand}/customers/`
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "customer-onboarder"
- brand: "<active-brand>"
- status: "<success|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "customer": "<customer name>",
    "customer_email": "<email>",
    "plan_tier": "<tier>",
    "persona": "<persona slug or null>",
    "trigger_source": "<stripe_checkout|crm_closed_won|manual>",
    "re_run": false,
    "signup_date": "YYYY-MM-DD",
    "kickoff_date": "YYYY-MM-DD",
    "kickoff_included": true,
    "workspace_url": "<notion url>",
    "welcome_draft_id": "<gmail id>",
    "booking_url": "<calendly url>",
    "milestones_queued": 0,
    "nps_queued": 0,
    "slack_notified": true,
    "crm_stage_after": "Onboarding",
    "health_score_baseline": 50,
    "output_path": "outputs/{brand}/customers/",
    "deliverable": "Onboarding_{customer}_{DDMonYYYY}.md"
  }
```
