---
name: lead-enrichment-pipeline
description: >
  Takes raw leads and enriches them to outreach-ready status. Chains
  company-researcher, cro-auditor, decision-maker-finder, apollo-lead-finder,
  email-validator, and personalization-enricher.
tags: [enrichment, pipeline, composite]
---

# Lead Enrichment Pipeline

Takes leads in NEW stage and enriches them through research, contact discovery, email validation, and personalization. Moves them to OUTREACH_READY.

## Prerequisites

- `agency.config.json` populated (tools, ICP, CRM)
- Leads in CRM with stage = NEW (from `signal-to-lead`)
- Tool stack configured for enrichment method (API vs browser)

## Capabilities Used

1. `company-researcher` -- business research
2. `cro-auditor` -- website audit
3. `decision-maker-finder` -- find contacts
4. `apollo-lead-finder` or manual enrichment -- get email/phone/LinkedIn
5. `email-validator` -- validate emails
6. `personalization-enricher` -- build personalization packet (for HOT leads)

## Phase 0: Intake

Read `agency.config.json`:
- `tools.lead_enrichment` -- determines enrichment method
- `tools.email_validation` -- determines validation method
- `crm.tabs` -- where to read/write leads

Query CRM for leads with stage = NEW, sorted by score (HOT first).

Ask user:
- "Found N new leads. Enrich all, or just HOT leads?" (default: HOT + WARM)
- "Run personalization enricher for HOT leads?" (default: yes)

## Phase 1: Company Research

For each lead, execute `company-researcher`:
- Visit website, research business
- Capture tech stack, social presence, pain points
- Update CRM with research data

## Phase 2: CRO Audit

For each lead with a website, execute `cro-auditor`:
- Audit key pages
- Find 3 actionable issues with outreach hooks
- Update CRM with findings

## Phase 3: Decision Maker Discovery

For each lead, execute `decision-maker-finder`:
- Find right contact based on company size + ICP titles
- Determine execution path from `tools.lead_enrichment`:

### API Path (tools.lead_enrichment.access === "api")
- Use Apollo People Search API to find contacts
- Enrich to get email, phone, LinkedIn
- 1 Apollo credit per enrichment

### Browser Path (tools.lead_enrichment.access === "browser")
- Use Chrome automation to search Apollo.io
- Navigate to People Search
- Enter company domain + title filters
- Copy contact details from results
- No API credits used (free plan)

### Manual Path (tools.lead_enrichment.access === "manual")
- Use WebSearch to find team page, LinkedIn profiles
- Extract names, titles, LinkedIn URLs
- No emails without enrichment tool

**APPROVAL GATE** (API path only):
"About to enrich N contacts using N Apollo credits. Proceed?"

## Phase 4: Email Validation

Execute `email-validator` for all discovered emails:
- Check tool config for method (API vs browser)
- Validate each email
- Handle invalids (find alternatives or mark LinkedIn-only)

**APPROVAL GATE**:
"About to validate N emails using N credits. Proceed?"

## Phase 5: Personalization (HOT leads only)

For leads scored HOT, execute `personalization-enricher`:
- Build full personalization packet
- Assemble company + CRO + person research into JSON
- Generate recommended approach and opening line

WARM leads skip this step (Tier 2 personalization at message generation).

## Phase 6: Update CRM

For each lead:
- Update stage: NEW -> RESEARCHED (after company research + CRO)
- Update stage: RESEARCHED -> ENRICHED (after contact discovery + email validation)
- Update stage: ENRICHED -> OUTREACH_READY (after personalization, or immediately for WARM)
- Write all collected data to CRM columns

## Phase 7: Summary

```
ENRICHMENT PIPELINE SUMMARY
---
Leads processed: N
Company research completed: N
CRO audits completed: N
Decision makers found: N contacts across M companies
Emails validated: N (X valid, Y catch-all, Z invalid)
Personalization packets built: N (HOT leads)

Credits used:
- Apollo: N credits
- ZeroBounce: N credits

Leads now OUTREACH_READY: N
Next step: Run /outreach-draft-pipeline to generate messages
```

## Example Usage

**Trigger phrases:**
- "Enrich today's leads"
- "Research and enrich HOT leads"
- "Run the enrichment pipeline"
- "Find contacts for these companies"
