---
type: Skill
name: design-crm
description: Manage the NV oOS Pro Toolkit CRM — leads, deals, companies, contacts, customers, activities, and support tickets. Covers the complete sales pipeline from lead capture through qualification, deal management, and post-conversion customer tracking with BANT/MEDDIC scoring, activity logging, and workflow automation. Use when working with CRM records, managing pipeline stages, qualifying leads, creating company profiles, logging calls/emails/meetings, or troubleshooting CRM data issues.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# NV oOS Pro Toolkit CRM

The Pro Toolkit CRM is a complete sales and customer relationship management
system built on WordPress Custom Post Types. It manages the full lifecycle:
**lead capture → qualification → deal management → conversion → customer retention**.
All entities are stored as CPT records accessible via the `toolkit_cpt` MCP tool.

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for CRM operations. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai cron` | Check CRM automation cron events (lead scoring, workflow triggers) |
| `wp mcp-ai queue` | Inspect CRM background jobs, retry failed imports |
| `wp mcp-ai bulk` | Bulk import/export CRM records |
| `wp mcp-ai health` | Verify CRM system health before running automations |
| `wp mcp-ai log` | View CRM workflow execution logs |

## When to use this skill

Trigger when ANY of the following is true:

- Viewing, searching, or filtering leads, deals, companies, customers, or activities.
- Creating or updating CRM records (leads, deals, companies, contacts, customers, activities, tickets).
- Qualifying leads using BANT or MEDDIC frameworks.
- Moving a deal through pipeline stages (inquiry → scoping → qualification → proposal → negotiation → engagement_signed).
- Converting a lead to a deal, or a deal to a customer.
- Logging sales activities: calls, emails, meetings, tasks, notes with dispositions.
- Building company profiles with industry, size, website, and status metadata.
- Managing support tickets with SLA tracking.
- Bulk importing leads or companies from CSV/email sources.
- Triaging the CRM pipeline — identifying hot leads, stalled deals, overdue follow-ups.
- Setting up CRM workflow rules for lead scoring, auto-assignment, or stage progression.
- Searching CRM records by email, company, status, or BANT score.

## Mental model — CRM entities and lifecycle

The CRM is organized around six core entity types connected by a lifecycle:

```
LEAD ──(qualified)──→ DEAL ──(won)──→ CUSTOMER
  │                     │                 │
  ├── activities        ├── activities    ├── activities
  ├── company           ├── company       ├── company
  └── contacts          └── contacts      └── contacts

TICKET ─── support requests, independent of lifecycle but linked to contacts/companies
```

**Relationships:**
- A **Lead** can be linked to a **Company** and **Contacts** (via `_company_id`, `_contact_id` meta).
- A **Deal** is linked to its source **Lead** via `lead_id` meta.
- A **Customer** is the post-conversion record after a deal is won.
- **Activities** link to any entity via `related_type` + `related_id` (e.g., `related_type: "lead"`, `related_id: 12398`).
- **Tickets** are independent support records that may reference a customer or company.

## CRM Entity Types

All CRM entities are managed through the **`toolkit_cpt`** MCP tool. Use the appropriate
`post_type` slug for each entity:

| CPT Slug | Label | Purpose | Key Meta Fields |
|---|---|---|---|
| `mcp_ai_lead` | Leads | Inbound lead capture, scored and staged | `first_name`, `last_name`, `email`, `phone`, `source`, `lead_status`, `lifecycle_stage`, `lead_score`, `bant_assessment` |
| `mcp_ai_deal` | Deals | Pipeline opportunities with stage tracking | `lead_id`, `deal_name`, `amount`, `currency`, `pipeline_stage`, `expected_close_date`, `deal_owner`, `win_probability` |
| `mcp_ai_company` | Companies | Organization profiles | `_company_industry`, `_company_size`, `_company_website`, `_company_phone`, `_company_address`, `_company_status`, `_company_assigned_to` |
| `mcp_crm_contacts` | Contacts | Individual contact records | Custom meta (varies by implementation) |
| `mcp_ai_customer` | Customers | Post-conversion customer records | Custom meta (varies by implementation) |
| `mcp_ai_crm_activity` | Activities | Calls, emails, meetings, tasks, notes | `activity_type`, `related_type`, `related_id`, `due_date` |
| `mcp_ai_ticket` | Support Tickets | ITIL-aligned SLA-tracked tickets | Custom meta (varies by implementation) |
| `mcp_ai_sequence` | Sequences | Automated outreach sequences | Custom meta |
| `mcp_crm_campaigns` | Campaigns | Marketing campaign records | Custom meta |
| `mcp_ai_crm_wf_rule` | Workflow Rules | Automation rules for CRM | Custom meta |

### Lead Meta Fields (detailed)

| Field | Type | Description | Example |
|---|---|---|---|
| `first_name` | string | Lead's first name | `"Scher"` |
| `last_name` | string | Lead's last name | `"Jill"` |
| `email` | string | Contact email address | `"jill.scher@cbiz.com"` |
| `phone` | string | Contact phone number | `""` |
| `source` | string | Lead source channel | `"email"`, `"webform"`, `"referral"`, `"upwork"` |
| `lead_status` | string | Current lead status | `"new"`, `"contacted"`, `"qualified"`, `"disqualified"` |
| `lifecycle_stage` | string | Lifecycle stage | `"lead"`, `"mql"`, `"sql"`, `"opportunity"` |
| `lead_score` | string | Numeric lead score (0-100) | `"62"` |
| `bant_assessment` | object | BANT qualification scores | See BANT/MEDDIC section below |
| `_source_message_id` | string | Source email message ID | `"19fd8cceb7c8e589"` |

### Deal Meta Fields (detailed)

| Field | Type | Description | Example |
|---|---|---|---|
| `lead_id` | string | Source lead post ID | `"12324"` |
| `deal_name` | string | Descriptive deal name | `"NUGL Media - Growth Capital"` |
| `amount` | string | Deal amount (string for precision) | `"0"`, `"50000"` |
| `currency` | string | ISO currency code | `"USD"` |
| `pipeline_stage` | string | Current pipeline stage | `"qualification"` |
| `stage_history` | array | Machine-readable transitions (from/to/at/source) | see JobNavigator section |
| `stage_changed_at` | string | ISO 8601 of the last real stage change | `"2026-09-16T09:00:00+00:00"` |
| `last_email_received` | string | Last inbound reply timestamp | `"2026-09-16T09:00:00+00:00"` |
| `last_email_sentiment` | string | Sentiment of the last reply | `"positive"` |
| `expected_close_date` | string | Expected close date | `""`, `"2026-09-15"` |
| `deal_owner` | string | WordPress user ID of owner | `"1"` |
| `win_probability` | string | Win probability (0-1) | `"0.1"`, `"0.75"` |

**Pipeline stages (standard flow):**
```
inquiry → scoping → qualification → proposal → negotiation → engagement_signed
                                                                  └──→ won/lost
```

### Activity Meta Fields (detailed)

| Field | Type | Description | Example |
|---|---|---|---|
| `activity_type` | string | Type of activity | `"task"`, `"call"`, `"email"`, `"meeting"`, `"note"` |
| `related_type` | string | Entity type this activity belongs to | `"lead"`, `"deal"`, `"company"`, `"customer"` |
| `related_id` | string | Post ID of the related entity | `"12398"` |
| `due_date` | string | Due date for tasks | `"2026-08-08"` |

### Company Meta Fields (detailed)

| Field | Type | Description | Example / Enum |
|---|---|---|---|
| `_company_industry` | string | Industry vertical | `"Technology"`, `"Healthcare"`, `"Finance"` |
| `_company_size` | string | Size tier | `"1-10"`, `"11-50"`, `"51-200"`, `"201-1000"`, `"1000+"` |
| `_company_website` | string | Company website URL | `"https://example.com"` |
| `_company_phone` | string | Primary phone | `"+1-555-0100"` |
| `_company_address` | string | Headquarters address | `"123 Main St, Suite 100"` |
| `_company_status` | string | CRM pipeline status | `"prospect"`, `"lead"`, `"qualified"`, `"customer"`, `"churned"` |
| `_company_assigned_to` | int | WordPress user ID of owner | `1` |

## BANT / MEDDIC Scoring

Leads are automatically scored using **BANT** (Budget, Authority, Need, Timeline) with
four sub-scores, each 0-100. The `bant_assessment` object has this structure:

```json
{
  "budget": {
    "score": 50,
    "evidence": "invest; $; "
  },
  "authority": {
    "score": 50,
    "evidence": "cto; director; "
  },
  "need": {
    "score": 100,
    "evidence": "need; problem; challenge; solution; "
  },
  "timeline": {
    "score": 75,
    "evidence": "urgent; by; immediately; "
  }
}
```

**Total BANT score** = sum of all four sub-scores (max 400).

For **enterprise deals**, supplement BANT with MEDDIC:
- **M**etrics: Quantifiable value the solution delivers.
- **E**conomic Buyer: Who controls the budget?
- **D**ecision Criteria: What are the formal evaluation criteria?
- **D**ecision Process: What's the purchasing process?
- **I**dentified Pain: What problem are they solving?
- **C**hampion: Who is your internal advocate?

Use `bant_assessment` for automated lead scoring. For enterprise deals, manually track
MEDDIC elements in the deal `content` field or as additional meta.

## Available Tools

All CRM operations use the **`toolkit_cpt`** MCP tool. This is the single interface
for all CRM CRUD operations.

### Discovery

```
# List all available CRM post types
toolkit_cpt(action: "list_types")

# Get field schema for any CRM type
toolkit_cpt(action: "get_schema", post_type: "mcp_ai_lead")
```

### Upwork job search (`search_upwork_jobs`)

Freelancer sourcing uses the Upwork CRM tools (`search_upwork_jobs`,
`score_upwork_job`, `draft_upwork_proposal`). Key behaviour:

- **Args:** `query`, `location` (folded into the GraphQL `searchExpression`,
  e.g. `wordpress developer (Remote)`), `job_type` (`hourly`/`fixed`/`all` —
  `all` or omitted = no filter), `experience_level`
  (`entry`/`intermediate`/`expert`/`all`), `skills`, `budget_min/max`,
  `exclude_keywords` (API: boolean `NOT (a OR b)`; fallback: `-"a"`
  operators), `sort` (`recency` default — sends GraphQL
  `sortAttributes: [{field: RECENCY}]`; `best_match`), `limit`, `cursor`.
  Omitted filters resolve from **CRM Settings → Upwork → Search Defaults**
  (`default_search_keywords`, `default_location`, …). `"all"` sentinels are
  normalised away, so preset steps carrying `job_type: "all"` never leak the
  literal into the GraphQL filter.
- **Every response echoes its criteria** — `criteria` (the effective
  query/location/skills/filters/sort/limit after defaults) and
  `criteria_provided` (false = unfiltered noise search) — so workflow digests
  can tell weak filters from a missing Upwork connection.
- **API mode** (Remote Sites connection with OAuth creds): returns structured
  jobs including a derived `url`
  (`https://www.upwork.com/jobs/<slug>_~<id>/` — the canonical marketplace
  job-page form).
- **MCP mode** (Remote Sites connection with `upwork_mode: mcp`, v1.1.89):
  routes the search through the official Upwork MCP gateway
  (`https://mcp.upwork.com/mcp`) via `WP_MCP_AI_Upwork_MCP_Bridge` —
  `upwork__find_jobs` (action `search`/`get`) returns envelopes normalized to
  the same shape as API mode, and `upwork__list_accounts` resolves the
  `upwork_org_uid` stored on the connection. Test Connection runs a real MCP
  handshake and validates without GraphQL credentials; tokens persist to the
  **encrypted** central `mcp_oauth` store (auto-refresh via the attached OAuth
  client).
- **Fallback mode** (no connection, or MCP mode without a token blob): two-pass web search — site-restricted
  Upwork pass, then a broader pass merged with URL dedupe. Upwork category
  landing pages (`/freelance-jobs/{slug}/` — no `~jobId`) are filtered out
  and reported in `filtered_out`, as are non-marketplace Upwork subdomains
  (`community.upwork.com`, `support.upwork.com`) and category/help-centre
  page titles; snippets are parsed for `job_type`, `budget`/`budget_max`
  (ranges), `tier` (Entry level/Intermediate/Expert), and `published`;
  `skills` build a quoted OR group; direct postings rank first.
- **Fallback URLs are canonicalised.** SERP URLs (the
  `/freelance-jobs/apply/<slug>_~<jobId>/` SEO form, often with tracking query
  strings like `referrer_url_path` that Upwork's SPA mishandles) are rewritten
  to the canonical `https://www.upwork.com/jobs/<slug>_~<jobId>/` marketplace
  form with the query string dropped — the form that reliably resolves to the
  listing (verified against the vanooo/upwork-mcp live-SPA scraper, which
  keeps only `/jobs/` links). Login-walled SPA surfaces (`/nx/…`, `/o/jobs/…`,
  `/r/…`) are dropped as non-listings, except `/nx/search/jobs/details/~<jobId>`
  which is rebuilt to the bare-ID form. Non-Upwork aggregator links pass
  through unchanged.
- **The fallback needs a real search provider.** With the default
  DuckDuckGo provider the fallback returns 0 results (Instant Answer API
  has no SERPs). Set a Brave/Tavily key in plugin Settings → Web Search.
- A bare query (no keywords, no defaults) returns the guidance notice
  ("unfiltered marketplace noise") — configure default keywords or pass
  `query`/`skills` for targeted results.

### Reading records

```json
// List leads (most recent first):
{ "action": "list_items", "post_type": "mcp_ai_lead", "orderby": "date", "order": "DESC", "per_page": 20 }

// Search leads by email:
{ "action": "list_items", "post_type": "mcp_ai_lead", "search": "jill.scher@cbiz.com" }

// Filter by meta field:
{ "action": "list_items", "post_type": "mcp_ai_lead", "filters": [{ "key": "lead_status", "value": "new" }] }

// Get a single record:
{ "action": "get_item", "post_type": "mcp_ai_lead", "item_id": 12398 }
```

### Creating records

```json
// Create a lead with BANT scoring:
{ "action": "create_item", "post_type": "mcp_ai_lead", "fields": {
  "title": "Jane Smith", "first_name": "Jane", "last_name": "Smith",
  "email": "jane@acmecorp.com", "phone": "+1-555-0100", "source": "referral",
  "lead_status": "new", "lifecycle_stage": "lead", "lead_score": "50",
  "bant_assessment": {
    "budget": { "score": 0, "evidence": "" },
    "authority": { "score": 25, "evidence": "manager;" },
    "need": { "score": 50, "evidence": "looking for;" },
    "timeline": { "score": 25, "evidence": "soon;" }
  }
} }

// Create a company:
{ "action": "create_item", "post_type": "mcp_ai_company", "fields": {
  "title": "Acme Corporation", "_company_industry": "Manufacturing",
  "_company_size": "201-1000", "_company_website": "https://acmecorp.com",
  "_company_phone": "+1-555-0200", "_company_status": "prospect"
} }

// Log an activity:
{ "action": "create_item", "post_type": "mcp_ai_crm_activity", "fields": {
  "title": "Discovery call with Jane Smith (Lead #12400)",
  "activity_type": "call", "related_type": "lead", "related_id": "12400",
  "due_date": "2026-08-14"
} }
```

### Updating records

```json
// Qualify a lead:
{ "action": "update_item", "post_type": "mcp_ai_lead", "item_id": 12398,
  "fields": { "lead_status": "qualified", "lifecycle_stage": "sql" } }

// Move a deal through pipeline stages:
{ "action": "update_item", "post_type": "mcp_ai_deal", "item_id": 12327,
  "fields": { "pipeline_stage": "proposal", "win_probability": "0.5",
  "expected_close_date": "2026-09-15", "amount": "25000" } }
```

### Bulk operations

```json
// Bulk create leads from a CSV import:
{ "action": "bulk_create", "post_type": "mcp_ai_lead", "items": [
  { "title": "Alice Brown", "first_name": "Alice", "last_name": "Brown",
    "email": "alice@example.com", "source": "csv_import", "lead_status": "new" },
  { "title": "Bob Wilson", "first_name": "Bob", "last_name": "Wilson",
    "email": "bob@example.com", "source": "csv_import", "lead_status": "new" }
] }
```

### Deleting records

```json
// Delete a lead (prefer disqualifying instead — see Critical Rules):
{ "action": "delete_item", "post_type": "mcp_ai_lead", "item_id": 12398 }
```

**⚠️ Warning:** Deleting a record is permanent. Consider using `update_item` to
change `lead_status` to `"disqualified"` instead of deleting, to preserve audit history.

## Common Workflows

### Lead qualification workflow

```
1. List new leads:   list_items(mcp_ai_lead, filters: [{key: "lead_status", value: "new"}])
2. Review BANT:      Check bant_assessment scores. Prioritize high Need + Timeline.
3. Create activity:  create_item(mcp_ai_crm_activity, activity_type: "call")
4. Update lead:      update_item(mcp_ai_lead, lead_status: "contacted")
5. If qualified:     update_item(mcp_ai_lead, lead_status: "qualified", lifecycle_stage: "sql")
                     create_item(mcp_ai_deal, lead_id: <lead_id>, pipeline_stage: "qualification")
```

### Deal pipeline management

```
1. Find stalled deals:  list_items(mcp_ai_deal, filters per pipeline_stage)
2. Check activities:    list_items(mcp_ai_crm_activity, filters: [{key: "related_id", value: "<deal_id>"}])
3. Advance stage:       update_item(mcp_ai_deal, pipeline_stage: <next_stage>, win_probability: <new_prob>)
4. Log activity:        create_item(mcp_ai_crm_activity, activity_type: "note", content: "<disposition>")
```

### Pipeline stage progression with win probabilities

| Stage | Win Probability | Typical Actions |
|---|---|---|
| `inquiry` | 5% | Initial contact, needs discovery |
| `scoping` | 10% | Define requirements, budget range |
| `qualification` | 25% | BANT/MEDDIC confirmed, champion identified |
| `proposal` | 50% | Proposal sent, economic buyer engaged |
| `negotiation` | 75% | Terms negotiation, legal review |
| `engagement_signed` | 90% | Contract signed, onboarding begins |
| `won` | 100% | Revenue recognized |
| `lost` | 0% | Closed-lost with reason |

### Building a company profile

```
1. Research company:  Use deep_research or web_search_validated for company info.
2. Create company:    create_item(mcp_ai_company, with industry, size, website, status).
3. Link lead:         update_item(mcp_ai_lead, adding _company_id reference to the company post ID).
4. Add contacts:      create_item(mcp_crm_contacts) for key personas at the company.
```

### Activity logging (call disposition)

```
After every call/meeting:
1. create_item(mcp_ai_crm_activity, activity_type: "call"|"meeting"|"email")
2. Set title:         "<Action> with <Contact Name> (<Entity> #<ID>)"
3. Set related_type:  "lead" | "deal" | "company" | "customer"
4. Set related_id:    The entity post ID
5. Set content:       Summary of the conversation, next steps, disposition
6. Set due_date:      For follow-up tasks (activity_type: "task")
```

### Pipeline triage

```
Weekly pipeline review:
1. list_items(mcp_ai_lead, filters: [{key: "lead_status", value: "new"}])
   → Identify high-score leads (lead_score >= 60) for immediate follow-up.
   
2. list_items(mcp_ai_deal, filters: [{key: "pipeline_stage", value: "qualification"}])
   → Find deals stuck in qualification for 2+ weeks — they need a champion.
   
3. list_items(mcp_ai_crm_activity, filters: [{key: "activity_type", value: "task"}])
   → Check for overdue follow-up tasks (due_date < today).
   
4. list_items(mcp_ai_lead, filters: [{key: "lead_status", value: "disqualified"}])
   → Review disqualified leads — some may be worth re-engaging.
```

### Searching across CRM

```json
// Find all leads from a specific company domain:
{ "action": "list_items", "post_type": "mcp_ai_lead", "search": "@cbiz.com" }

// Find all activities for a lead:
{ "action": "list_items", "post_type": "mcp_ai_crm_activity",
  "filters": [{ "key": "related_type", "value": "lead" },
              { "key": "related_id", "value": "12398" }] }
```

## JobNavigator-Adoption Features (v3.2.0)

Adopted from [vesaias/JobNavigator](https://github.com/vesaias/JobNavigator);
full plan in `docs/developer/crm-toolkit-jobnavigator-adoption-plan.md`.

### Stage transition history (deals)

Every `move_deal_stage` (and `create_deal`) appends a machine-readable
entry to the deal's `stage_history` meta:

```json
{ "from": "prospecting", "to": "qualification", "at": "2026-09-16T…", "source": "tool" }
```

- `source` is one of `tool`, `agent`, `workflow`, `manual`, `email_reply`, `bulk`.
- `stage_changed_at` meta stamps the last real change — drives time-in-stage
  and stalled-deal detection. **No-op stage moves never bump `updated_at`.**
- `move_deal_stage` accepts `undo: true` to revert the last move without
  recording a new transition (audits `deal_stage_reverted`).
- Helper: `WP_MCP_AI_CRM_Stage_History` (`record`, `get_history`,
  `undo_last`, `time_in_stage`, `next_open_stage`).

### Lead dedup, companies, signals

- `create_lead` refuses duplicates by normalized email with a 409
  `wp_mcp_ai_duplicate_lead` error carrying `existing_lead_id`;
  pass `allow_duplicate: true` to force-create.
- `create_lead` auto-links `company_name` to a canonical company record
  (case/space-insensitive; auto-creates when missing) via
  `WP_MCP_AI_CRM_Identity`. Settings: `identity.auto_create_company`
  (default true), `identity.auto_create_company_from_domain` (default false),
  `identity.dedupe_leads` (default true).
- Lead/deal email signals: `last_email_received`, `last_email_snippet`
  (capped 500), `last_email_sentiment` (positive|neutral|negative|mixed|unknown).
- Auto-disqualification: settings `auto_disqualify` block
  (`enabled`, `max_score`, `min_age_days`, `only_statuses`) — evaluated
  on lead create/update, fires `wp_mcp_ai_crm_lead_auto_disqualified`.

### New tools

| Slug | Purpose |
|---|---|
| `bulk_move_deal_stages` | Move up to 100 deals to one stage; reports `updated`/`skipped`/`not_found`; supports `undo` |
| `record_crm_reply` | Store reply signals on lead + open deals; optionally advance a deal (`advance_deal: true`) with source `email_reply` |
| `get_crm_handover` | Paste-ready plain-text bundle (facts, BANT, stage history, signals, activities + closing ask) for any AI/human handoff |
| `get_pipeline_digest` | Compact digest text + data: stage totals, pipeline value, stalled deals, hot leads, overdue tasks |
| `create_tracked_link` | Create a `?nvoos_track=<token>` link for a deal; opens recorded on the deal |

- `delete_deal` on a `closed_won` deal releases the lead lifecycle back to
  `opportunity` when no other won deal remains (hook `wp_mcp_ai_crm_deal_deleted`).

### Gmail reply poller (v3.2.0)

Settings `gmail_reply_poll` block (`enabled` default false,
`advance_on_positive` default false, `max_per_poll` 10,
`min_interval_minutes` 15). When enabled, the cron
(`wp_mcp_ai_crm_gmail_reply_poll`) polls Gmail for unread replies via the
Gmail client + Remote Sites connections, matches senders to leads by
normalized email, classifies sentiment via `WP_MCP_AI_CRM_Classifier`, and
applies signals through `WP_MCP_AI_Tool_Record_CRM_Reply::apply()`. Unknown
senders are skipped; the `wp_mcp_ai_crm_classify_intent` filter can swap in
an LLM classifier. Last-poll stamp: `wp_mcp_ai_crm_reply_last_poll` option.

### Pipeline digest scheduling (recipe asset, no code)

`addons/pro/config/pipeline-digest-recipe.json` — an importable recipe:
workflow nodes `get_pipeline_digest` → `send_telegram_message`
(`{{digest.result.text}}` template) plus a `create_pro_schedule` daily
config. Apply via the Pro Workflow Builder + Pro Schedule Manager MCP tools;
swap the delivery node for WhatsApp or local persistence as needed.

## Critical Rules

- **Always use `get_schema` first** before creating or updating a record to verify available field keys and types.
- **Lead scoring is automated** — the `lead_score` and `bant_assessment` are populated by the CRM engine. Manual overrides should be rare and documented.
- **Never delete leads** — use `lead_status: "disqualified"` to preserve audit trail and prevent re-import of the same contact.
- **Activities are the audit trail** — log every meaningful interaction (call, email, meeting, note) with `related_type` and `related_id`.
- **Deal pipeline stages are sequential** — don't skip stages. Each stage transition should have an activity log.
- **`deal_owner` is a WordPress user ID** — ensure the user exists and has appropriate CRM capabilities.
- **`win_probability` is a float stored as string** — use `"0.1"` not `0.1` in JSON.
- **BANT `evidence` is semicolon-delimited** — the engine parses email content for keyword evidence. When manually setting, use `"keyword1; keyword2; "` format.
- **Bulk operations (`bulk_create`) are for imports** — each item must be a complete fields object. Existing records with matching IDs will be overwritten.
- **Support tickets (`mcp_ai_ticket`) are SLA-tracked** — create them for customer issues, not sales inquiries.

## Common Mistakes

```
WRONG — deleting a lead instead of disqualifying
{ "action": "delete_item", "post_type": "mcp_ai_lead", "item_id": 12398 }

RIGHT — disqualify to preserve history
{ "action": "update_item", "post_type": "mcp_ai_lead", "item_id": 12398,
  "fields": { "lead_status": "disqualified" } }

WRONG — creating a deal without linking to a lead
{ "action": "create_item", "post_type": "mcp_ai_deal",
  "fields": { "deal_name": "Some Deal", "pipeline_stage": "qualification" } }
// Missing lead_id — the deal has no source traceability.

RIGHT — always link deals to their source lead
{ "action": "create_item", "post_type": "mcp_ai_deal",
  "fields": { "lead_id": "12398", "deal_name": "CBIZ - Audit Automation",
  "pipeline_stage": "scoping", "amount": "0", "currency": "USD", "deal_owner": "1",
  "win_probability": "0.1" } }

WRONG — logging an activity without related_type or related_id
{ "action": "create_item", "post_type": "mcp_ai_crm_activity",
  "fields": { "title": "Call with prospect", "activity_type": "call" } }
// This activity is orphaned — it can't be found when viewing the lead/deal.

RIGHT — always link activities to their parent entity
{ "action": "create_item", "post_type": "mcp_ai_crm_activity",
  "fields": { "title": "Discovery call with Jill Scher (Lead #12398)",
  "activity_type": "call", "related_type": "lead", "related_id": "12398" } }

WRONG — skipping pipeline stages
// Moving from "inquiry" directly to "proposal" with no scoping or qualification.
// The pipeline history should reflect the actual sales process.

RIGHT — advance stage-by-stage with activity log
1. update_item: pipeline_stage: "scoping"
2. create_item(activity): "Scope of work discussed"
3. update_item: pipeline_stage: "qualification"
4. create_item(activity): "BANT confirmed, champion identified"
5. update_item: pipeline_stage: "proposal"

WRONG — setting win_probability to 0 or 1 prematurely
// Win probability should reflect real pipeline stage, not optimism/pessimism.

WRONG — searching with filters that use meta keys not in the schema
// Some meta fields may be added dynamically. Always call get_schema first
// to confirm which fields are registered and filterable.
```

## Cross-References

- Run `design-deep-research` to research target companies before creating company profiles.
- Run `design-web-research` for quick company lookups and competitive intelligence.
- Run `design-pro-workflow-builder` to automate CRM workflows (lead scoring, auto-assignment, stage progression).
- Run `design-pro-schedule-manager` to schedule recurring CRM tasks (pipeline reviews, follow-up reminders).
- Run `design-document-generation` to create proposals, SOWs, and invoices from deal data.
- Run `wp-security-audit` on any CRM automation callbacks — CRM data is sensitive and must be access-controlled.

## What This Skill Does NOT Cover

- Email integration details (Gmail/Outlook sync) — use `search_gmail` for inbox queries.
- Remote WordPress CRM access — use `nv_oos_console_agent_remote_wp_connection` for multi-site CRM.
- Paper Store integration — use `paper_store_*` tools for research-backed company profiles.
- ERP integration (EZuite) — use `ezuite_erp` / `ezuite_erp_get_products` for ERP-connected CRM data.
- CRM workflow rule configuration — use `toolkit_cpt` with `post_type: "mcp_ai_crm_wf_rule"` and the `design-pro-workflow-builder` skill.
- Sequence automation — use `toolkit_cpt` with `post_type: "mcp_ai_sequence"`.

## References

- NV oOS Pro Toolkit CRM admin page: `/wp-admin/admin.php?page=nvoos-pro-toolkit-crm`
- `toolkit_cpt` MCP tool — the primary interface for all CRM operations.
- BANT framework: [blog.hubspot.com/sales/bant](https://blog.hubspot.com/sales/bant)
- MEDDIC framework: [meddic.co](https://meddic.co)
