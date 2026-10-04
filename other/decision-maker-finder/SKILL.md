---
name: decision-maker-finder
description: Find 5 decision makers at a company via Apollo.io UI using Chrome DevTools MCP. No enrichment, no credits used.
tags: [decision-maker, contact-finding, lead-enrichment, apollo, chrome-devtools]
---

# Decision Maker Finder

Finds 5 decision makers at a target company using Apollo.io UI via Chrome DevTools MCP. Search only, no enrichment, no credits consumed.

## Prerequisites

- `agency.config.json` at repo root with `icp.segments[].titles`, `icp.segments[].seniority`, and `tools.lead_enrichment`
- Chrome DevTools MCP available (`mcp__chrome-devtools__*`)
- Apollo.io logged in on Chrome Beta
- Target company name and/or website

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `icp.segments[]` -- each segment's `titles` and `seniority` arrays
   - `tools.lead_enrichment.tool` -- must be "apollo"
   - `tools.lead_enrichment.access` -- must be "chrome_devtools"
   - `tools.lead_enrichment.contacts_per_company` -- number of contacts to find (default: 5)
   - `tools.browser_automation` -- Chrome DevTools MCP config
3. Accept parameters:
   - `company_name` -- (required) the target company
   - `website` -- (optional) company website domain
   - `company_size` -- (optional) if known, skip the size detection step
   - `segment` -- (optional) which ICP segment to use for title targeting
   - `max_contacts` -- (optional) how many contacts to return (default: 5)

## Phase 1: Company Size Detection

If `company_size` is not provided, determine it:

**WebSearch:**
- Search: `"{{company_name}}" "employees" OR "team size" OR "people" site:linkedin.com/company`
- Search: `"{{company_name}}" employees site:crunchbase.com`
- Search: `"{{company_name}}" "about us" "team"`

Classify into size tiers:
- **Early-stage**: < 50 employees
- **Mid-market**: 50 - 500 employees
- **Large**: 500+ employees

## Phase 2: Role Targeting

Based on company size, determine which titles to target:

### Early-stage (< 50 employees)
Primary targets:
1. **Founder / Co-Founder** -- they make all decisions
2. **CEO** -- same person as founder in most cases
3. **Head of Marketing / Growth** -- if they exist, they own the ecommerce stack

Rationale: Small companies have flat hierarchies. The founder decides on agency partnerships.

### Mid-market (50 - 500 employees)
Primary targets:
1. **Head of Ecommerce / Director of Ecommerce** -- owns the Shopify store
2. **VP Marketing / Head of Marketing** -- owns the growth budget
3. **Head of Digital / Director of Digital** -- owns the online experience
4. **CMO** -- if the company has one, they approve agency spend

Rationale: Mid-market companies have functional leads. Target the person who owns the ecommerce P&L or the marketing budget.

### Large (500+ employees)
Primary targets:
1. **VP of Ecommerce / VP of Digital** -- senior enough to approve budgets
2. **Director of Ecommerce** -- operational decision maker
3. **Head of D2C / Head of Online** -- if they have a dedicated D2C function
4. **SVP Marketing** -- if no dedicated ecommerce leadership

Rationale: Large companies have multiple layers. Target VP+ who can approve agency contracts without escalating.

Cross-reference these defaults with the `icp.segments[].titles` and `icp.segments[].seniority` arrays from config to ensure alignment with the agency's actual target persona.

## Phase 3: Contact Search via Apollo.io (Chrome DevTools MCP)

Use Chrome DevTools MCP to search Apollo.io UI. This is the ONLY path. No API, no WebSearch fallback.

### Chrome DevTools MCP Workflow:

1. `mcp__chrome-devtools__navigate_page` to `https://app.apollo.io/`
2. Verify logged-in state
3. Navigate to People Search
4. `mcp__chrome-devtools__fill` company filter with `{{company_name}}`
5. `mcp__chrome-devtools__fill` title filter with target titles from Phase 2
6. Apply seniority filters matching ICP config
7. `mcp__chrome-devtools__click` search/apply filters
8. `mcp__chrome-devtools__wait_for` results to load
9. `mcp__chrome-devtools__take_snapshot` to read results

### Extract from each result:
- Name
- Title
- Company
- LinkedIn profile URL (Apollo shows this)

### IMPORTANT:
- Pick 5 decision makers per company
- DO NOT click "Enrich" or "Access Email" on Apollo (no credits used)
- DO NOT use Apollo enrichment features
- We only use Apollo for SEARCH, not enrichment
- Email discovery happens via Snov.io (separate skill)

If fewer than 5 results: accept what Apollo returns. Note the shortfall.

## Phase 4: Contact Data Assembly

For each found contact, record:

- **Name**: Full name from Apollo search results
- **Title**: Current title at the target company
- **Company**: Company name
- **LinkedIn URL**: Direct profile link from Apollo
- **Email**: NOT from Apollo. Will be found via `email-validator` (Snov.io) skill.
- **Phone**: NOT from Apollo. Will be found via `phone-finder` (Lemlist) skill.

DO NOT attempt to enrich or find emails at this stage. That's handled by downstream skills.

## Phase 5: Prioritize Contacts

Rank the found contacts:

1. **Title match score**: How closely does their title match the target titles? Exact match = 10, partial match = 5, related = 3.
2. **Seniority alignment**: Does their seniority match the company size rules? Aligned = 10, adjacent = 5.
3. **Recency**: Recently joined (< 6 months) = bonus, as they may be actively building their vendor stack.

Sort by total priority score, descending.

## Phase 6: Output

Return structured JSON:

```json
{
  "company": "BrandX",
  "website": "https://brandx.com",
  "company_size": "Mid-market (120 employees)",
  "size_tier": "mid-market",
  "targeting_rationale": "Mid-market company, targeting Head/Director of Ecommerce or VP Marketing.",
  "contacts": [
    {
      "name": "Jane Doe",
      "title": "Head of Ecommerce",
      "linkedin_url": "https://linkedin.com/in/janedoe",
      "confidence": "HIGH",
      "method_used": "apollo_chrome_devtools",
      "priority_score": 27,
      "notes": "Joined 4 months ago. Likely building her vendor stack."
    }
  ],
  "recommended_contact": "Jane Doe -- Head of Ecommerce, highest priority score",
  "searched_at": "2026-03-16T09:30:00Z"
}
```

## Phase 7: Log to CRM

Use `crm-writer` to log the decision maker data to the Pipeline tab. Write: company, contact name, title, LinkedIn URL, confidence, found_at timestamp.

No approval gate. Contacts are logged directly.

## Example Usage

Trigger phrases:
- "Find the decision maker at [company]"
- "Who should I reach out to at [company]?"
- "Find the right contact at [company]"
- "Get me the founder of [company]"
- "Find the Head of Ecommerce at [company]"

```
User: Find the decision maker at BrandX
Assistant: [reads config, determines company size = mid-market, targets Head of Ecommerce / VP Marketing, searches via Apollo Chrome DevTools MCP, returns 5 prioritized contacts]
```

```
User: Who should I email at this 10-person startup?
Assistant: [size = early-stage, targets Founder/CEO, searches via Apollo Chrome DevTools MCP, returns contacts]
```
