---
name: crm-writer
description: Read and write data to the agency CRM (Google Sheets via webhook or API)
tags: [crm, google-sheets, data, pipeline]
---

# CRM Writer

Reads and writes lead, outreach, and pipeline data to the agency's CRM. Default backend is Google Sheets via webhook. The skill checks `tools.crm` in `agency.config.json` to determine the execution path and credentials.

## Prerequisites

- `agency.config.json` at repo root with `crm` and `tools.crm` sections
- For webhook method: a deployed Google Apps Script webhook URL in `crm.webhook_url`
- For API method: `GOOGLE_SERVICE_ACCOUNT_KEY` env var set (referenced in `tools.crm.api_key_env`)

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `crm.type` -- CRM backend type (e.g., `google_sheets`)
   - `crm.sheet_id` -- the Google Sheet ID
   - `crm.webhook_url` -- the Google Apps Script webhook endpoint
   - `crm.tabs` -- map of logical tab names to actual sheet tab names
   - `tools.crm.access` -- execution method: `webhook` | `api` | `browser`
   - `tools.crm.api_key_env` -- env var name for API credentials (if applicable)
3. Accept parameters:
   - `operation` -- one of: `READ`, `APPEND`, `UPDATE`, `CREATE_TAB`
   - `tab` -- logical tab name (looked up in `crm.tabs`) or literal tab name
   - `data` -- the data to write (for APPEND/UPDATE operations)
   - `query` -- search/filter criteria (for READ operations)

## Phase 1: Resolve Tab Name

Map the logical tab name to the actual sheet tab name using `crm.tabs`:

- If `tab` matches a key in `crm.tabs`, use the mapped value.
- If `tab` does not match any key, use it as-is (literal tab name).

Example: `tab: "hawk_leads"` resolves to `"Hawk Leads"` per the config.

## Phase 2: Execute Operation

### APPEND -- Add New Rows

Add one or more rows to a tab. Each row is an object with column headers as keys.

**Via Webhook (preferred):**

```bash
curl -s -X POST "{{crm.webhook_url}}" \
  -H "Content-Type: application/json" \
  -d '{
    "sheet": "{{resolved_tab_name}}",
    "headers": ["Col1", "Col2", "Col3"],
    "row": ["value1", "value2", "value3"]
  }'
```

Rules:
- `headers` must match the existing column headers in the tab exactly (case-sensitive).
- If the tab does not exist, the webhook will create it with the provided headers.
- For multiple rows, send one request per row (the webhook processes single rows).
- Add a `timestamp` column with ISO datetime for every write.
- Rate limit: max 1 request per second to avoid Google quota issues.

**Via API (if webhook is unavailable):**

Use the Google Sheets API v4 with the service account credentials from the env var specified in `tools.crm.api_key_env`.

```
POST https://sheets.googleapis.com/v4/spreadsheets/{{crm.sheet_id}}/values/{{resolved_tab_name}}!A:Z:append?valueInputOption=USER_ENTERED
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "values": [["value1", "value2", "value3"]]
}
```

### READ -- Query Existing Data

Read rows from a tab, optionally filtered.

**Via Webhook:**

```bash
curl -s -X POST "{{crm.webhook_url}}" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "read",
    "sheet": "{{resolved_tab_name}}",
    "filters": {
      "column": "Stage",
      "value": "HOT"
    }
  }'
```

**Via API:**

```
GET https://sheets.googleapis.com/v4/spreadsheets/{{crm.sheet_id}}/values/{{resolved_tab_name}}!A:Z
Authorization: Bearer {{access_token}}
```

Then filter the returned data in-memory based on the query criteria.

Query options:
- `stage` -- filter by pipeline stage (e.g., HOT, WARM, CONTACTED)
- `date_range` -- filter by date column (e.g., last 7 days)
- `search` -- substring match across all columns
- `limit` -- max rows to return

### UPDATE -- Modify Existing Rows

Update specific fields on existing rows. Identify the row by a unique key (usually URL, email, or company name).

**Via Webhook:**

```bash
curl -s -X POST "{{crm.webhook_url}}" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "update",
    "sheet": "{{resolved_tab_name}}",
    "match_column": "Email",
    "match_value": "founder@example.com",
    "updates": {
      "Stage": "CONTACTED",
      "Last Touch": "2024-01-15",
      "Notes": "Sent cold email"
    }
  }'
```

**Via API:**

1. Read the sheet to find the row number matching the key.
2. Use `PUT` to update the specific cells.

### CREATE_TAB -- Create a New Tab

Create a new tab with specified headers.

**Via Webhook:**

```bash
curl -s -X POST "{{crm.webhook_url}}" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "create_tab",
    "sheet": "{{new_tab_name}}",
    "headers": ["Date", "Company", "Contact", "Email", "Stage", "Source", "Notes"]
  }'
```

**Via API:**

Use the Sheets API `batchUpdate` to add a new sheet, then write the header row.

## Phase 3: Validation

Before executing any write operation:

1. **Data completeness**: Verify all required columns have values. Warn if critical fields (company, contact, email) are empty.
2. **Dedup check** (for APPEND): If the tab already contains a row with the same URL or email, warn and ask for confirmation before adding a duplicate.
3. **Tab existence**: For APPEND/UPDATE, verify the tab exists first with a READ. If it does not exist, offer to CREATE_TAB first.

## Phase 4: Error Handling

- **Webhook returns error**: Log the error, retry once after 3 seconds. If still failing, report the error and the raw data so the user can manually add it.
- **API auth failure**: Check if the env var exists. Report which env var is missing.
- **Rate limit**: If Google returns 429, wait 5 seconds and retry. Max 3 retries.
- **Tab not found**: Suggest creating the tab with CREATE_TAB.

## Phase 5: Confirmation

After each operation, report:

```
CRM Write Complete:
- Tab: {{tab_name}}
- Operation: APPEND
- Rows written: {{count}}
- Timestamp: {{iso_datetime}}
```

For READ operations, return the data in a clean table format.

## Example Usage

Trigger phrases:
- "Log this lead to the CRM"
- "Add these leads to Hawk Leads"
- "Update the stage for [company]"
- "Read all HOT leads from the pipeline"
- "Create a new CRM tab for [purpose]"
- "Write to the outreach log"

```
User: Log these 5 scored leads to Hawk Leads
Assistant: [reads config, resolves tab name, sends 5 webhook POSTs with rate limiting, confirms 5 rows written]
```

```
User: Show me all leads contacted this week
Assistant: [reads Outreach CRM tab, filters by date range, returns table]
```
