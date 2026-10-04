---
name: phone-finder
description: >
  Find phone numbers for decision makers via Lemlist using Chrome DevTools MCP.
  Takes LinkedIn profile URLs and returns phone numbers where available.
tags: [phone, enrichment, lemlist, chrome-devtools]
---

# Phone Finder

Finds phone numbers for decision maker contacts using Lemlist via Chrome DevTools MCP. Takes LinkedIn profile URLs (from decision-maker-finder output) and returns phone numbers where available.

## Prerequisites

- `agency.config.json` at repo root with `tools.phone_lookup` configured
- Lemlist logged in on Chrome Beta
- Chrome DevTools MCP available (`mcp__chrome-devtools__*`)
- LinkedIn profile URLs for contacts (from decision-maker-finder)

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `tools.phone_lookup.tool` -- must be "lemlist"
   - `tools.phone_lookup.access` -- must be "chrome_devtools"
   - `tools.browser_automation` -- Chrome DevTools MCP config
3. Accept parameters:
   - `contacts` -- (required) array of contact objects, each with: name, company, linkedin_url, email (if available)
   - `batch_size` -- (optional) how many to process at once (default: 25)

## Phase 1: Navigate to Lemlist

Using Chrome DevTools MCP:

1. `mcp__chrome-devtools__navigate_page` to Lemlist dashboard
2. Verify logged-in state (check for user avatar or dashboard elements)
3. If not logged in: STOP and report "Lemlist login required in Chrome Beta"
4. Navigate to the contact enrichment / people search section

## Phase 2: Upload Contacts

For each contact (or batch):

1. Use the Lemlist people finder / enrichment feature
2. Input the LinkedIn profile URL
3. If LinkedIn URL is not available, input name + company as search terms
4. Wait for Lemlist to process and return results

### Chrome DevTools MCP workflow:

```
1. mcp__chrome-devtools__navigate_page → Lemlist enrichment page
2. mcp__chrome-devtools__fill → paste LinkedIn URL or name+company
3. mcp__chrome-devtools__click → search/enrich button
4. mcp__chrome-devtools__wait_for → results to load
5. mcp__chrome-devtools__take_snapshot → read results from page
```

## Phase 3: Extract Phone Numbers

For each processed contact, extract:

```json
{
  "name": "Jane Doe",
  "company": "BrandX",
  "linkedin_url": "https://linkedin.com/in/janedoe",
  "phone": "+1-555-123-4567",
  "phone_type": "mobile",
  "phone_source": "lemlist",
  "found": true
}
```

If no phone number found:
```json
{
  "name": "Jane Doe",
  "company": "BrandX",
  "linkedin_url": "https://linkedin.com/in/janedoe",
  "phone": null,
  "phone_type": null,
  "phone_source": "lemlist",
  "found": false
}
```

## Phase 4: Update CRM

Use `crm-writer` to update the Pipeline tab:
- Add phone numbers to the corresponding contact rows
- For contacts without phone numbers, leave the phone field empty (do not overwrite existing data)

## Phase 5: Output

Return structured JSON:

```json
{
  "total_contacts": 25,
  "phones_found": 18,
  "phones_not_found": 7,
  "success_rate": "72%",
  "contacts": [
    {
      "name": "Jane Doe",
      "company": "BrandX",
      "phone": "+1-555-123-4567",
      "found": true
    }
  ],
  "processed_at": "2026-03-16T09:30:00Z"
}
```

Summary:
```
Phone Finder Complete:
- Contacts processed: 25
- Phone numbers found: 18 (72%)
- CRM updated: 18 contacts
```

## Example Usage

Trigger phrases:
- "Find phone numbers for today's leads"
- "Get phone numbers via Lemlist"
- "Enrich contacts with phone numbers"
- "Look up phones for these decision makers"
