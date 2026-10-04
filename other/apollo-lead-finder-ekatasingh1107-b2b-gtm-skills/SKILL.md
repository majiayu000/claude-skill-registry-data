---
name: apollo-lead-finder
description: >
  Two-phase Apollo.io prospecting: free People Search to discover ICP-matching
  leads, then selective enrichment to reveal emails/phones (credits per contact).
  Deduplicates against CRM (Google Sheets). Supports Apollo API and MCP tools.
tags: [lead-generation, apollo, enrichment, prospecting]
---

# Apollo Lead Finder

Two-phase Apollo.io prospecting: **free** People Search for lead discovery, then selective **paid** enrichment to reveal emails and phone numbers. Deduplicates against the CRM (Google Sheets via crm-writer). Supports both Apollo API (direct) and Apollo MCP tools when available.

**Key advantage:** Apollo People Search is free (no credits consumed). Credits are only spent when enriching contacts to reveal email/phone. This lets you search tens of thousands of leads at zero cost, review results, then selectively enrich only the best matches.

## Prerequisites

- `agency.config.json` at repo root with `icp`, `crm`, and `tools.lead_enrichment` sections
- CRM initialized via `/crm-setup` (pipeline tab must exist)
- One of:
  - Apollo API key in env var (if `tools.lead_enrichment.access === "api"`)
  - Chrome browser automation via Claude-in-Chrome MCP (if `tools.lead_enrichment.access === "browser"`)
  - Apollo MCP tools available (`mcp__claude_ai_Apollo_io__*`)

## Phase 0: Read Config

1. Read `agency.config.json` from the project root.
2. Extract:
   - `icp.segments` -- array of ICP segment definitions, each containing:
     - `name` -- segment label (e.g., "India D2C", "US/UK/AU D2C")
     - `markets` -- geographic locations array
     - `company_size` -- employee count ranges in "min,max" format
     - `industries` -- industry/keyword tags
     - `titles` -- target job titles
     - `seniority` -- seniority levels (owner, founder, c_suite, vp, director, etc.)
     - `description` -- human-readable segment description
   - `crm.webhook_url` -- for CRM read/write operations
   - `crm.tabs.pipeline` -- the tab name where leads are stored
   - `tools.lead_enrichment.tool` -- should be "apollo"
   - `tools.lead_enrichment.access` -- "api" | "browser"
   - `tools.lead_enrichment.api_key_env` -- env var name for API key (if access is "api")
   - `tools.lead_enrichment.daily_limit` -- max enrichments per day
   - `tools.lead_enrichment.plan` -- "free" | "basic" | "professional"
3. Determine the execution path:
   - **API path**: `tools.lead_enrichment.access === "api"` and `tools.lead_enrichment.api_key_env` is set. Use Apollo REST API directly.
   - **MCP path**: Apollo MCP tools are available (`mcp__claude_ai_Apollo_io__apollo_mixed_people_api_search`, etc.). Use MCP tools.
   - **Browser path**: `tools.lead_enrichment.access === "browser"`. Use Chrome browser automation via Claude-in-Chrome MCP to interact with Apollo's web UI.
4. If no execution path is available, halt and tell the user to configure Apollo access in `agency.config.json` via `/agency-setup`.

## Phase 1: Search (FREE -- No Credits Consumed)

### Step 1: Select ICP Segment

Present the available ICP segments from `icp.segments` to the user:

```
Available ICP Segments:
  1. India D2C -- Post-PMF early stage D2C brands...
  2. US/UK/AU D2C -- Early stage D2C brands with basic store UI/UX...
```

Ask which segment to search, or accept the segment name from the user's trigger message.

If the user provides custom criteria instead of selecting a pre-defined segment, build an ad-hoc filter set from their input.

### Step 2: Map ICP Segment to Apollo Filters

Convert the selected ICP segment into Apollo's search filter format:

```json
{
  "person_titles": ["{{from segment.titles}}"],
  "person_seniority": ["{{from segment.seniority}}"],
  "person_locations": ["{{from segment.markets}}"],
  "organization_num_employees_ranges": ["{{from segment.company_size}}"],
  "q_organization_keyword_tags": ["{{from segment.industries}}"]
}
```

Mapping rules:
- `segment.titles` maps to `person_titles` directly
- `segment.seniority` maps to `person_seniority` directly
- `segment.markets` maps to `person_locations` directly
- `segment.company_size` maps to `organization_num_employees_ranges` directly (already in "min,max" format)
- `segment.industries` maps to `q_organization_keyword_tags` directly

Present the mapped filters to the user for confirmation before searching.

### Step 3: Execute Search

**Via Apollo API** (access === "api"):

```bash
curl -s -X POST "https://api.apollo.io/api/v1/mixed_people/api_search" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${APOLLO_API_KEY}" \
  -d '{
    "person_titles": ["Head of Ecommerce", "VP Marketing"],
    "person_seniority": ["vp", "director", "owner", "founder", "c_suite"],
    "person_locations": ["United States", "United Kingdom"],
    "organization_num_employees_ranges": ["21,50", "51,100", "101,200"],
    "q_organization_keyword_tags": ["D2C", "DTC", "Shopify", "Ecommerce"],
    "page": 1,
    "per_page": 100
  }'
```

Paginate through results: increment `page` from 1 until either `total_entries` is exhausted or the mode cap is reached. Each page returns up to 100 results.

**Via Apollo MCP** (MCP tools available):

Use `mcp__claude_ai_Apollo_io__apollo_mixed_people_api_search` with the same filter parameters. The MCP tool handles authentication and pagination internally.

**Via Browser** (access === "browser"):

Use Claude-in-Chrome MCP to:
1. Navigate to `https://app.apollo.io/`
2. Go to People Search
3. Apply filters: titles, seniority, locations, company size, keywords
4. Extract search results from the page
5. Paginate through results by clicking "Next" and extracting each page

Browser mode is slower but works on Apollo's free plan without API access.

### Step 4: Collect Results

The free search returns limited preview data per person:
- Apollo person ID
- First name
- Obfuscated last name (via API) or full name (via browser/MCP)
- Title
- Company name
- Boolean flags: has_email, has_phone
- Company employee count (approximate)

**No LinkedIn URLs, emails, or phone numbers are revealed at this stage.**

### Mode Caps

| Parameter | Test | Standard | Full |
|-----------|------|----------|------|
| Max pages | 1 | 50 | 500 |
| Max results | 100 | 5,000 | 50,000 |
| Credits consumed | 0 | 0 | 0 |

Default mode is "standard" unless the user specifies otherwise.

### Step 5: Save Search Results

Store the raw search results in memory for Phase 2 review. Include:
- Total matches found in Apollo
- Number of results retrieved
- The filter criteria used
- Timestamp of the search

## Phase 2: Review Search Results

Present a summary to the user:

```
Apollo Search Results
---------------------
Segment: US/UK/AU D2C
Filters: VP Marketing, Director of Digital, Head of Growth
         at D2C/Shopify companies (21-200 employees)
         in US, UK, Australia

Total matching profiles: {{total_entries}}
Results retrieved: {{retrieved_count}}
Mode: standard (max 5,000)

Title distribution:
  Head of Ecommerce .... 342
  VP Marketing ......... 287
  Director of Digital .. 198
  Head of Growth ....... 156

Company size distribution:
  21-50 employees ...... 412
  51-100 employees ..... 389
  101-200 employees .... 182

Sample leads (first 10):
  1. J*** S*** -- Head of Ecommerce at ExampleBrand (52 employees)
  2. M*** P*** -- VP Marketing at AnotherCo (89 employees)
  ...
```

Ask the user:
- "Do you want to proceed with enrichment? This will cost credits."
- "Do you want to adjust filters and search again?"
- "Do you want to export the search preview as-is?"

Do not proceed to Phase 3 without explicit user approval.

## Phase 3: Enrich (COSTS CREDITS -- Approval Required)

### APPROVAL GATE

**CRITICAL: Never enrich without explicit user approval.** Enrichment costs 1 Apollo credit per contact. Present the cost clearly:

```
Enrichment will cost approximately {{count}} credits.
Your daily limit is {{tools.lead_enrichment.daily_limit}} enrichments.

Proceed with enrichment? (yes/no, or specify a limit like "enrich top 50")
```

Wait for explicit confirmation. If the user says no, export the search preview and stop.

### Step 1: Dedup Against CRM

Before enrichment, check the CRM for existing leads to avoid duplicating contacts.

Read the pipeline tab from the CRM:

```bash
curl -s -X POST "{{crm.webhook_url}}" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "read",
    "sheet": "{{crm.tabs.pipeline}}"
  }'
```

Or use the crm-writer skill with operation `READ` on the `pipeline` tab.

Build a dedup set from existing CRM records using:
- Company name (normalized, lowercase, trimmed)
- Contact name + Company combination
- Email (if already known from prior enrichments)
- LinkedIn URL (if already known)

Filter the search results to remove any leads that already exist in the CRM. Report the dedup results:

```
Dedup Results:
  Search results: {{total_search_results}}
  Already in CRM: {{existing_count}}
  Net-new leads: {{net_new_count}}
  Proceeding to enrich: {{enrich_count}} (capped by daily limit)
```

### Step 2: Execute Enrichment

**Via Apollo API** (access === "api"):

Use the bulk match endpoint for efficiency:

```bash
curl -s -X POST "https://api.apollo.io/api/v1/people/bulk_match" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${APOLLO_API_KEY}" \
  -d '{
    "details": [
      {"id": "apollo_person_id_1"},
      {"id": "apollo_person_id_2"},
      ...
    ]
  }'
```

Send in batches of 10 (Apollo's batch limit). Each match costs 1 credit. Handle rate limits (429) with exponential backoff using the Retry-After header.

Enriched data returned per person:
- Full name
- Email (personal and/or work)
- Phone number(s)
- LinkedIn URL
- Full title
- Company name, domain, employee count, industry
- Location (city, state, country)

**Via Apollo MCP** (MCP tools available):

Use these MCP tools:
- `mcp__claude_ai_Apollo_io__apollo_people_match` -- single person enrichment (1 credit)
- `mcp__claude_ai_Apollo_io__apollo_people_bulk_match` -- batch enrichment (1 credit each)
- `mcp__claude_ai_Apollo_io__apollo_organizations_enrich` -- company data enrichment

For richer company context, also call `mcp__claude_ai_Apollo_io__apollo_organizations_enrich` with the company domain to get:
- Company description
- Technologies used
- Funding details
- Social media links

**Via Browser** (access === "browser"):

Use Claude-in-Chrome MCP to:
1. Navigate to each person's Apollo profile
2. Click "Access Email" or "Reveal Contact Info"
3. Extract the revealed email and phone
4. Navigate back and repeat for the next person

Browser enrichment is slow (one at a time) and limited by daily reveal caps on the free plan. Respect `tools.lead_enrichment.daily_limit`.

### Step 3: Present Enriched Results

Show the enriched leads before writing to the CRM:

```
Enriched Leads ({{count}} contacts)
-------------------------------------
1. Jane Smith -- Head of Ecommerce at ExampleBrand
   Email: jane@examplebrand.com
   Phone: +1-555-0123
   LinkedIn: linkedin.com/in/janesmith
   Company: 52 employees, D2C, Shopify

2. Mark Parker -- VP Marketing at AnotherCo
   Email: mark@anotherco.com
   Phone: --
   LinkedIn: linkedin.com/in/markparker
   Company: 89 employees, Ecommerce

Email coverage: {{email_pct}}%
Phone coverage: {{phone_pct}}%
Credits used: {{credits_used}}
```

**Second approval gate:** "Write these {{count}} leads to the CRM pipeline? (yes/no)"

Do not write to CRM without this confirmation.

## Phase 4: Write to CRM

After user approval, write enriched leads to the CRM pipeline tab using crm-writer.

For each enriched lead, APPEND a row to the pipeline tab:

```bash
curl -s -X POST "{{crm.webhook_url}}" \
  -H "Content-Type: application/json" \
  -d '{
    "sheet": "{{crm.tabs.pipeline}}",
    "headers": ["Date", "Company", "Website", "Contact", "Title", "Email", "LinkedIn", "Phone", "Platform", "Signal_Type", "Score", "Tier", "Stage", "Cadence_Day", "Last_Action", "Last_Action_Date", "Next_Action", "Next_Action_Date", "Response_Received", "Response_Summary", "Notes", "Created_At"],
    "row": [
      "{{today_iso}}",
      "{{company_name}}",
      "{{company_domain}}",
      "{{full_name}}",
      "{{title}}",
      "{{email}}",
      "{{linkedin_url}}",
      "{{phone}}",
      "Apollo",
      "ICP Search",
      "",
      "",
      "NEW",
      "0",
      "Enriched via Apollo",
      "{{today_iso}}",
      "Email Outreach",
      "{{tomorrow_iso}}",
      "No",
      "",
      "Segment: {{segment_name}}. {{company_employee_count}} employees.",
      "{{now_iso}}"
    ]
  }'
```

Column mapping:
- `Date` -- today's date (YYYY-MM-DD)
- `Company` -- company name from Apollo
- `Website` -- company domain
- `Contact` -- full name
- `Title` -- job title
- `Email` -- revealed work email (or personal if no work email)
- `LinkedIn` -- LinkedIn profile URL
- `Phone` -- phone number (or empty)
- `Platform` -- "Apollo"
- `Signal_Type` -- "ICP Search"
- `Score` -- leave empty (will be scored by lead-scorer if needed)
- `Tier` -- leave empty
- `Stage` -- "NEW"
- `Cadence_Day` -- "0" (not yet in cadence)
- `Last_Action` -- "Enriched via Apollo"
- `Last_Action_Date` -- today's date
- `Next_Action` -- "Email Outreach"
- `Next_Action_Date` -- tomorrow's date
- `Response_Received` -- "No"
- `Response_Summary` -- empty
- `Notes` -- segment name, employee count, any notable details
- `Created_At` -- current ISO datetime

Rate limit: 1 request per second to the webhook.

Optionally, also save contacts to Apollo's CRM for list management:
- Use `mcp__claude_ai_Apollo_io__apollo_contacts_create` (if MCP available)
- Or `POST https://api.apollo.io/api/v1/contacts` (if API access)

## Phase 5: Summary

Present the final summary:

```
Apollo Lead Finder -- Complete
-------------------------------
Segment: {{segment_name}}
Search results: {{total_search_results}}
Already in CRM: {{dedup_filtered}}
Enriched: {{enriched_count}}
Written to CRM: {{written_count}}
Credits used: {{credits_used}} / {{daily_limit}} daily limit

Coverage:
  Email: {{email_pct}}%
  Phone: {{phone_pct}}%
  LinkedIn: {{linkedin_pct}}%

CRM tab: {{crm.tabs.pipeline}}
Sheet: https://docs.google.com/spreadsheets/d/{{crm.sheet_id}}/edit

Next steps:
  1. Run /lead-scorer to score and tier the new leads
  2. Run /outreach-draft-pipeline to generate personalized emails
  3. Run /cadence-manager to start multi-channel cadence
  4. Search another segment or refine filters
```

## Apollo API Reference

- **People Search:** `POST https://api.apollo.io/api/v1/mixed_people/api_search` -- FREE, returns Apollo IDs + preview data (first name, title, org name, boolean flags). No LinkedIn URLs or emails.
- **People Match (enrich):** `POST https://api.apollo.io/api/v1/people/match` -- 1 credit, reveals email/phone/LinkedIn
- **Bulk People Match:** `POST https://api.apollo.io/api/v1/people/bulk_match` -- up to 10 per request, 1 credit each
- **Create List:** `POST https://api.apollo.io/api/v1/labels` -- create a named list
- **Create Contact:** `POST https://api.apollo.io/api/v1/contacts` -- add person to Apollo CRM + optional list
- **Organization Enrich:** `POST https://api.apollo.io/api/v1/organizations/enrich` -- company data by domain
- **Auth:** `x-api-key: {APOLLO_API_KEY}` header on all requests
- **Rate limit:** Varies by plan. Handle 429 with Retry-After header.
- **Search Pagination:** `page` param (1-indexed), `per_page` max 100

## Apollo MCP Tools Reference

When Apollo MCP tools are available, prefer them over raw API calls:

- `mcp__claude_ai_Apollo_io__apollo_mixed_people_api_search` -- People Search (free). Pass person_titles, person_seniority, person_locations, organization_num_employees_ranges, q_organization_keyword_tags.
- `mcp__claude_ai_Apollo_io__apollo_people_match` -- Single person enrichment (1 credit). Pass person ID or name+company+title combo.
- `mcp__claude_ai_Apollo_io__apollo_people_bulk_match` -- Batch enrichment (1 credit each). Pass array of person details.
- `mcp__claude_ai_Apollo_io__apollo_organizations_enrich` -- Company enrichment by domain. Returns tech stack, funding, employee count.
- `mcp__claude_ai_Apollo_io__apollo_organizations_bulk_enrich` -- Batch company enrichment.
- `mcp__claude_ai_Apollo_io__apollo_contacts_create` -- Save enriched contact to Apollo CRM.
- `mcp__claude_ai_Apollo_io__apollo_contacts_search` -- Search existing Apollo contacts (dedup).
- `mcp__claude_ai_Apollo_io__apollo_contacts_update` -- Update existing Apollo contact.
- `mcp__claude_ai_Apollo_io__apollo_emailer_campaigns_search` -- Find existing email campaigns.
- `mcp__claude_ai_Apollo_io__apollo_emailer_campaigns_add_contact_ids` -- Add contacts to an email campaign.

## Available Apollo Search Filters

Full list of filters for the People Search endpoint:

- `person_titles` -- job title keywords (array of strings)
- `person_seniority` -- seniority levels: owner, founder, c_suite, partner, vp, director, manager, senior, entry
- `person_locations` -- geographic locations (array of strings)
- `organization_num_employees_ranges` -- employee count ranges, format "min,max" (e.g., "51,200")
- `q_organization_keyword_tags` -- company keyword tags (e.g., "SaaS", "D2C")
- `person_not_titles` -- titles to exclude (array of strings)
- `q_organization_name` -- organization name search
- `organization_locations` -- company HQ locations
- `q_keywords` -- general keyword search across all fields
- `contact_email_status` -- filter by email status: "verified", "guessed", "unavailable"
- `organization_ids` -- filter by specific Apollo organization IDs
- `revenue_range` -- company revenue filter

## Example Usage

Trigger phrases:
- "Search Apollo for D2C founders in India"
- "Find leads on Apollo matching my ICP"
- "Run Apollo search for the US/UK/AU segment"
- "Enrich the top 50 Apollo leads"
- "Prospect on Apollo for Head of Ecommerce at Shopify brands"

```
User: Search Apollo for my India D2C segment
Assistant: [reads config, maps India D2C segment to Apollo filters, runs free search,
           presents results with title/company distribution, asks for enrichment approval]
```

```
User: Enrich the top 25
Assistant: [dedup against CRM pipeline, enriches 25 leads via bulk_match,
           presents enriched contacts with emails, asks for CRM write approval,
           writes to pipeline tab, reports summary]
```

```
User: Find VP Marketing at D2C brands in the US with 50-200 employees
Assistant: [builds ad-hoc filter set from user criteria, runs free search,
           presents results, follows same approval flow for enrichment and CRM write]
```
