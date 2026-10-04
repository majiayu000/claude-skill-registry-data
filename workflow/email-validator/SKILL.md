---
name: email-validator
description: >
  Find and validate email addresses using Snov.io via Chrome DevTools MCP.
  Takes LinkedIn profile URLs and returns verified emails. Replaces ZeroBounce.
tags: [email, validation, deliverability, snovio, chrome-devtools]
---

# Email Validator

Finds and validates email addresses using Snov.io via Chrome DevTools MCP. Takes LinkedIn profile URLs from decision-maker-finder and returns verified emails. Minimum 3 verified emails per company required; flags RED if fewer.

## Prerequisites

- `agency.config.json` populated with `tools.email_validation`
- Snov.io logged in on Chrome Beta
- Chrome DevTools MCP available (`mcp__chrome-devtools__*`)
- LinkedIn profile URLs for contacts (from decision-maker-finder)

## Phase 0: Intake

Read `agency.config.json`:
- `tools.email_validation.tool` -- must be "snovio"
- `tools.email_validation.access` -- must be "chrome_devtools"
- `tools.browser_automation` -- Chrome DevTools MCP config

Accept parameters:
1. List of contacts with LinkedIn profile URLs (from decision-maker-finder output)
2. Company name for each contact (for grouping and threshold checking)

## Phase 1: Navigate to Snov.io

Using Chrome DevTools MCP:

1. `mcp__chrome-devtools__navigate_page` to Snov.io dashboard
2. Verify logged-in state (check for user avatar or dashboard elements)
3. If not logged in: STOP and report "Snov.io login required in Chrome Beta"
4. Navigate to the email finder / LinkedIn lookup section

## Phase 2: Find and Validate Emails via LinkedIn Profile URLs

**CRITICAL: ALWAYS use Snov.io LinkedIn Search (app.snov.io/linkedin/search) with the person's LinkedIn profile URL. NEVER guess email patterns from domain names. Snov.io returns the actual verified email tied to the LinkedIn profile.**

For each contact:

### Chrome DevTools MCP Workflow (Single Lookup):

```
1. mcp__chrome-devtools__navigate_page → https://app.snov.io/linkedin/search
2. mcp__chrome-devtools__fill → paste full LinkedIn profile URL (e.g. https://www.linkedin.com/in/chris-ferguson-80b98b79)
3. mcp__chrome-devtools__click → "Find email" / search button
4. mcp__chrome-devtools__wait_for → results to load (email found or not found)
5. mcp__chrome-devtools__take_snapshot → read verified email from results
```

Snov.io finds the real email from the LinkedIn profile and returns:
- Email address (the actual email, not a guess)
- Verification status (valid, invalid, catch-all, unknown)
- Green dot = verified, Gray dot = not found

### For Multiple Contacts (Bulk):

Use Snov.io Bulk LinkedIn Search:
1. Navigate to bulk search or use the LinkedIn Search page repeatedly
2. Paste each LinkedIn URL one by one
3. Collect all verified emails before sending any outreach

### NEVER DO THIS:
- Do NOT guess emails from domain patterns (e.g. firstname@domain.com)
- Do NOT use Email Search with name + domain as primary method
- Do NOT send emails without Snov.io verification first
- Do NOT use Domain Search to infer email patterns and construct addresses

## Phase 3: Process Results

For each contact, record:

```json
{
  "name": "Jane Doe",
  "company": "BrandX",
  "linkedin_url": "https://linkedin.com/in/janedoe",
  "email": "jane@brandx.com",
  "email_status": "valid",
  "email_type": "professional",
  "source": "snovio"
}
```

Classification handling:
| Status | Action | Include in Outreach? |
|--------|--------|---------------------|
| Valid | Use as-is | Yes |
| Catch-All | Flag but use | Yes (with caution) |
| Invalid | Do not email | No |
| Unknown | Flag for review | Maybe |
| Not Found | LinkedIn-only outreach | No email outreach |

## Phase 4: Company Threshold Check

For each company, verify minimum email coverage:

- Count verified (valid + catch-all) emails per company
- **Minimum threshold: 3 verified emails per company**
- If >= 3 verified: company is GREEN
- If < 3 verified: company is RED

For RED companies:
1. FLAG as RED on CRM sheet (visual indicator)
2. Note in CRM: "Low email coverage - [N] verified emails. Prioritize LinkedIn outreach."
3. Still proceed with available emails, but prioritize LinkedIn/Instagram channels

## Phase 5: Update CRM

Write validation results back to CRM via `crm-writer`:
- Update email and email_status columns for each contact
- Flag RED companies with a visual indicator
- Update lead stage from RESEARCHED to email-validated

No approval gate. Results are written directly.

## Phase 6: Summary

```
Email Validation Complete (Snov.io):
- Contacts processed: N
- Emails found: N
- Valid: N (X%)
- Catch-All: N (X%)
- Invalid: N (X%)
- Not Found: N (X%)

Company Coverage:
- GREEN (3+ verified emails): N companies
- RED (< 3 verified emails): N companies [LIST]
```

## Example Usage

Trigger phrases:
- "Validate emails for today's leads"
- "Find emails via Snov.io"
- "Run email validation on the pipeline"
- "Check email coverage for these companies"
