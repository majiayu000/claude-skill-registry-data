---
name: lead-crm-manager
description: Fill the fb.ai CRM with sendable leads — search (0.25/query), import, and enrich (0.075/lead) so emails are unmasked, then build the lists and segments a campaign targets. Unenriched leads are silently dropped by a send, so this skill's real job is getting emails unmasked. Run on demand.
allowed-tools: Read, Grep, Glob, Bash
area: Sales
use_for: "Find, import, and enrich leads in the fb.ai CRM, and build the lists/segments a campaign targets"
deps:
  mcp: []
  gateway: ["fivebucks (**scope: leadgen_crm**)", "FiveAgents (logging)"]
  files: ["sales.md", "audience.md", "brand.md"]
  env: ["`FIVEBUCKS_API_KEY`", "`FIVEAGENTS_API_KEY`"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.20.1 | July 13, 2026 |

**Description:** Find, import, and enrich leads in the fb.ai CRM, and build the lists/segments a campaign targets.

### Change Log

**v2.20.1** — July 13, 2026
- **Added the missing "import to CRM" step (v2.20.0 implied `fivebucks_search_leads_status` results land in the CRM automatically — they don't).** New Step 3a calls `fivebucks_import_search_results` to persist chosen search results before they're sendable/enrichable. Corrected the masked-email signal (empty/`null` `email` field, not a literal `***`) and the `whoami` quota field (`quota.quotas.<bucket>.{current, max}` per bucket — search bills `seo_research`, enrich bills `content_generation` — no `quota.remaining` field exists).

**v2.20.0** — July 12, 2026
- Initial release. Drives fb.ai's `leadgen_crm` scope (gateway v1.8.0).

# SKILL.md — Lead CRM Manager

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools — including the **fb.ai API key — scopes, errors, quota** contract, which governs every `fivebucks_*` call in this skill. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

## Role

You build the brand's lead list on fb.ai. The output that matters is not "leads in the CRM" — it's **leads that can actually be emailed.**

That distinction is the whole job. Leads arrive from fb.ai's search with **masked emails** (`***`). A masked lead looks completely normal in a list, and a campaign will **silently drop it** — no error, no warning, it just quietly emails fewer people than the user thinks. If every lead is masked, the send fails outright. So the finished state you are working toward is: every lead the user intends to email has a real, unmasked address.

You are **spend-aware**. Search costs 0.25 a query and enrichment costs 0.075 a lead, so a careless 500-lead enrich is 37.5 quota. You price it before you run it, every time.

---

## When to use

Use this skill when the task involves:
- Finding new B2B leads for the brand on fb.ai
- Importing a lead list the user already has
- Enriching leads so their emails are real and sendable
- Building the list or segment a campaign will target
- Tagging, cleaning, or deduping the fb.ai CRM

Do NOT use this skill for:
- Setting up the sending domain / sender signature → use `leadgen-onboarder`
- Writing the email sequence and sending it → use `campaign-runner`
- Prospecting into **Notion** via Apollo → use `apollo-lead-prospector`. That's a different stack — Apollo's API into a Notion CRM, feeding Gmail outreach. This skill uses fb.ai's own lead search and CRM, feeding fb.ai campaigns. They don't share data. Pick the stack that matches how the brand sends (see `outreach-sequencer` vs `campaign-runner`)

---

## Inputs required

Before starting, confirm or default these inputs:

| Input | Required | Notes |
|-------|----------|-------|
| Active brand | Yes | From `$DEFAULT_BRAND`; ask if unset |
| ICP filters | Yes for search | Job titles, seniority, industry, location, company size. From `sales.md` / `audience.md`; confirm with the user |
| How many to enrich | Yes before enriching | **This is the price.** Confirm the number explicitly |
| Target list/segment | Optional | Only if the leads are being prepared for a specific campaign |

---

## Step-by-step workflow

### Step 1: Read brand context and check the key

Read `brands/{brand}/sales.md` (ICP filters, sender persona) and `audience.md` (personas, pain points).

```
Use gateway MCP tool `fivebucks_whoami`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
```

- Confirm `scopes` contains **`leadgen_crm`** (an empty `scopes` array = legacy full-access key, which is fine).
- If it's missing → stop. Send the user to https://www.fivebucks.ai/dashboard/api-keys. Do not retry.
- **Note your quota.** whoami returns `quota.quotas.<bucket>.{current, max}` (there is **no** `quota.remaining` field) — search bills `seo_research`, enrich bills `content_generation`; remaining for each is `max − current`. Steps 3 and 4 are priced against them.

### Step 2: See what's already in the CRM

Never buy a search for leads the brand already has:

```
Use gateway MCP tool `fivebucks_list_leads`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- search: "<optional keyword>"
- job_title: "<optional filter>"
- company_name: "<optional filter>"
- status: "<optional: new, contacted, replied, qualified, lost, bounced, unsubscribed>"
- source: "<optional: apollo_search, manual_import, api_integration>"
- limit: <max 1000>
- offset: <for paging>
```

**Look at the `email` field on every lead.** If it's empty/`null` (or contains `***`), that lead is **masked/unenriched** — it is in the CRM but cannot be emailed. Count them. Tell the user how many of their existing leads are sendable versus masked, because that number is usually a surprise.

If the brand already has enough of the right leads, skip Step 3 entirely and go straight to enrichment.

### Step 3: Find new leads (0.25 per search)

⚠️ **You must supply at least one real filter.** An empty search is rejected with `validation/no-filters`.

Propose the filters from `sales.md` / `audience.md` and show them to the user before spending:

```
Use gateway MCP tool `fivebucks_search_leads`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- person_titles: ["<e.g. Head of Marketing>", "<VP Marketing>"]
- person_seniorities: ["<e.g. director, vp, c_suite>"]
- q_organization_keyword_tags: ["<industry keywords>"]
- organization_locations: ["<e.g. Singapore>"]
- organization_industries: ["<e.g. software>"]
- organization_num_employees_ranges: ["<e.g. 11,50>"]
- page: <int>
- per_page: <int>
```

Async → poll:

```
Use gateway MCP tool `fivebucks_search_leads_status`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- jobId: "<jobId from fivebucks_search_leads>"
```

Each search is **0.25 quota**, so a wide net cast three different ways costs 0.75. Refine the filters *before* searching, not by searching repeatedly.

The completed status returns a `results` array — the found leads, **with MASKED emails** (the `email` field comes back `null`/blank and the *name* is partly redacted; `email_status` / `has_email_flag` signal sendability, not a `***` in the email itself). ⚠️ **These results are NOT in the CRM yet** — they live only in the search response and will not appear in `fivebucks_list_leads` until you import them (next step).

### Step 3a: Import the results you want into the CRM

This is the dashboard's "Import to Database" step. Show the user the results and let them pick which to keep — you don't have to import all of them. Then persist the chosen ones:

```
Use gateway MCP tool `fivebucks_import_search_results`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- searchResults: [ <the objects from the search_leads_status `results` array, unchanged> ]
- tags: ["<optional label, e.g. q1-outbound>"]
```

Free, and fb.ai deduplicates against existing leads. Now they're in the CRM — but **still masked**. Step 4 (enrich) is what makes them sendable, and it is not optional if these leads are going to be emailed.

### Step 3b: Or import a list the user already has

Free, and up to 1000 at a time. fb.ai deduplicates.

```
Use gateway MCP tool `fivebucks_import_leads`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- leads: [
    { "full_name": "<required>", "email": "...", "company_name": "...", "company_domain": "...", "job_title": "...", "linkedin_url": "...", "tags": ["..."] },
    ...
  ]
```

Only `full_name` is required per row. **Imported leads usually still need enrichment** — if the user's CSV had no email column, those rows are just as unsendable as a masked search result.

*(For one or two leads by hand, `fivebucks_create_lead(full_name, ...)` is simpler. Both are free.)*

### Step 4: Enrich — the step that makes leads sendable (0.075 per lead)

**Do the arithmetic out loud and get an explicit yes:**

> "You have 240 masked leads. Enriching all of them is 240 × 0.075 = **18.0 quota**. You have {remaining}. Do you want all 240, or should we narrow it first?"

Narrowing before enriching is almost always the right advice — enriching leads the brand will never email is money burned.

```
Use gateway MCP tool `fivebucks_enrich_leads`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- leadIds: ["<id>", "<id>", ...]
```

⚠️ **Max 100 leads per call.** For more, batch them — 240 leads is three calls.

⚠️ **Use this bulk tool even for a single lead.** fb.ai's single-lead enrich endpoint returns a job id that no status route can resolve, so it can't be polled. The bulk route with one id is the only workable path. There is no single-lead enrich tool exposed, and that's deliberate.

Async → poll every batch:

```
Use gateway MCP tool `fivebucks_enrich_status`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- jobId: "<jobId from fivebucks_enrich_leads>"
```

*(Re-sending the same `leadIds` within ~30 minutes returns the existing job rather than charging again. If you get the same job back, poll it — don't retry.)*

**Then verify.** Re-run `fivebucks_list_leads` and confirm the emails are no longer `***`. Enrichment doesn't always find an address — report how many actually came back sendable, not how many you paid for. That gap is real and the user needs to know it.

### Step 5: Tidy the CRM (all free)

- `fivebucks_bulk_tag_leads(leadIds, tags)` — tag up to 100 at a time, e.g. by campaign or source
- `fivebucks_update_lead(lead_id, ...)` — fix a title, change `status`, add notes
- `fivebucks_bulk_delete_leads(leadIds)` — ⚠️ **destructive and irreversible.** State the exact count and get an explicit yes: *"This will permanently delete 47 leads. Confirm?"*

### Step 6: Build the target — list or segment?

This choice is load-bearing and users get it wrong, so make it for them explicitly:

| | `fivebucks_create_lead_list` | `fivebucks_create_segment` |
|---|---|---|
| Membership | **STATIC** — snapshotted at creation | **DYNAMIC** — re-evaluates every time |
| New matching leads added later | ❌ Not included | ✅ Automatically included |
| Use it when | You want to email *exactly these people*, frozen | You want a living audience ("all VPs in fintech") |
| Campaign targets it as | `target_type: 'lists'` + `target_list_ids` | `target_type: 'segment'` + `target_segment_id` |

Both take the same filter shape:

```
Use gateway MCP tool `fivebucks_create_segment`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- name: "<e.g. Fintech VPs — Singapore>"
- description: "<optional>"
- filter_criteria: {
    "conditions": [
      { "field": "job_title", "operator": "contains", "value": "VP" },
      { "field": "company_industry", "operator": "equals", "value": "fintech" }
    ],
    "operator": "AND"
  }
```

**Valid `field` values:** `job_title`, `company_name`, `status`, `tags`, `seniority_level`, `location`, `company_industry`, `company_employee_count`, `email_opened`, `email_replied`, `created_at`.
**Valid `operator` values:** `equals`, `not_equals`, `contains`, `not_contains`, `greater_than`, `less_than`, `in`, `not_in`, `is_null`, `is_not_null`, `before`, `after`, `between`. The outer `operator` is `AND` or `OR`.

Existing targets: `fivebucks_list_lead_lists` / `fivebucks_list_segments` (both free — check before creating a duplicate).

### Step 7: Size the target and hand off

```
Use gateway MCP tool `fivebucks_segment_count`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- segment_id: "<segment id>"
```

This is how the send gets priced. Report it as money, not as a number:

> "The segment has 312 leads. A campaign to them costs 312 × 0.01 = **3.12 quota**. Of those, 298 are enriched and sendable — the other 14 would be silently dropped. Want me to enrich them first (14 × 0.075 = 1.05), or send to the 298?"

Then hand off to `campaign-runner`.

---

## Output format

**Save location — local workspace:**
```
outputs/{brand}/sales/leads/
```

**Naming convention:**
```
LeadCRM_[DDMonYYYY].md
```

**Output metadata:**
```markdown
---
Date: YYYY-MM-DD
Skill Used: lead-crm-manager
Brand: {brand}
Leads Found: {N}
Leads Enriched: {E}
Sendable Leads: {S}
Quota Spent: {Q}
Status: Final
---
```

**Output sections:**
1. **What's in the CRM now** — total leads, and critically: **how many are sendable vs still masked**
2. **New leads found** — the filters used, and what came back (a table: name · title · company · sendable?)
3. **Enrichment** — how many were enriched, how many actually returned a real address, and the gap between those two numbers
4. **Target built** — the list or segment, why that type, its filter criteria, and its size
5. **Quota spent** — itemized: searches × 0.25 + leads × 0.075. And what's left
6. **Next step** — the hand-off to `campaign-runner` with the send cost (N × 0.01)

---

## Quality checklist

- [ ] `fivebucks_whoami` checked **before** any spend; `leadgen_crm` scope confirmed
- [ ] `fivebucks_list_leads` checked first — existing leads reused rather than re-searched
- [ ] Masked (`***`) emails counted and reported — the sendable-vs-total gap surfaced explicitly
- [ ] Search filters proposed and confirmed **before** spending 0.25; at least one real filter supplied
- [ ] Enrichment priced out loud (N × 0.075) and explicitly confirmed
- [ ] User steered to narrow the set **before** enriching, not after
- [ ] Enrichment batched at ≤100 per call; bulk tool used even for a single lead
- [ ] Every async job polled to completion — no fire-and-forget
- [ ] Post-enrichment verified — reported how many came back **actually sendable**, not how many were paid for
- [ ] Destructive bulk delete confirmed with an exact count
- [ ] List-vs-segment choice made explicitly (static vs dynamic), not by default
- [ ] `fivebucks_segment_count` run before hand-off so the send is priced
- [ ] Quota spend reported and reconciled against the `fivebucks_whoami` snapshot
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "lead-crm-manager"
- brand: "<active-brand>"
- status: "<success|partial|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "searches_run": 0,
    "leads_found": 0,
    "leads_imported": 0,
    "leads_enriched": 0,
    "leads_sendable_after_enrich": 0,
    "leads_still_masked": 0,
    "enrichment_hit_rate": 0.0,
    "target_type": "none|list|segment",
    "target_size": 0,
    "search_quota": 0.0,
    "enrichment_quota": 0.0,
    "quota_spent": 0.0,
    "quota_remaining": 0.0,
    "output_path": "outputs/{brand}/sales/leads/"
  }
```
