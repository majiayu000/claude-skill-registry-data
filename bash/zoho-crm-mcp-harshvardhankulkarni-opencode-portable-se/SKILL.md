---
name: zoho-crm-mcp
version: 1.4.0
description: Connect your agent to Zoho CRM via MCP. Search contacts, list accounts, query records with COQL, and manage CRM data using mcporter. Includes ready-to-use Python scripts with pagination and custom-field support for common CRM operations.
---

# Zoho CRM MCP

Connect your agent to Zoho CRM through the Model Context Protocol (MCP). This skill provides everything you need to search, read, and manage CRM data using `mcporter`.

## Source Repository

GitHub source: [sprintberlin/openclaw-zoho-crm-mcp-skill](https://github.com/sprintberlin/openclaw-zoho-crm-mcp-skill)

## Requirements

| Requirement | Details |
|---|---|
| Zoho CRM MCP Server | A configured endpoint from [mcp.zoho.eu](https://mcp.zoho.eu) |
| mcporter | MCP client CLI (bundled with OpenClaw; elsewhere install via `npm i -g mcporter`) |
| Environment variable | `ZOHO_MCP_URL` must be set (see below) |

### Environment Variable Setup

This skill requires the `ZOHO_MCP_URL` environment variable. Without it, the Python scripts will not work.

Add this to your shell profile (e.g. `~/.bashrc` or `~/.zshrc`):
```bash
export ZOHO_MCP_URL="https://your-org-zoho-crm-xxxxx.zohomcp.eu/mcp/YOUR_TOKEN/message"
```

Or set it per session:
```bash
ZOHO_MCP_URL="https://your-org-zoho-crm-xxxxx.zohomcp.eu/mcp/YOUR_TOKEN/message" python3 scripts/list_contacts.py
```

To verify it's set:
```bash
echo $ZOHO_MCP_URL
```

## How to Get Your MCP URL

1. Go to [mcp.zoho.eu](https://mcp.zoho.eu) and sign in with your Zoho account.
2. Click **"Add Connection"** (or "New Connection").
3. Select **Zoho CRM** from the list of available apps.
4. Choose the **data center** matching your Zoho account (EU, US, IN, AU, JP, CN).
5. Grant the requested OAuth scopes (at minimum: read access to the modules you want to query).
6. After authorization, copy the generated **MCP endpoint URL**. It looks like:
   ```
   https://your-org-zoho-crm-xxxxx.zohomcp.eu/mcp/abc123def456/message
   ```
7. Set it as `ZOHO_MCP_URL` as shown above.

### Multiple Organizations

If you manage multiple Zoho CRM orgs, each gets its own MCP endpoint. You can:
- Set one default via `ZOHO_MCP_URL`
- Pass others explicitly in scripts or mcporter calls
- Use a wrapper script or `.env` file per project

## Quick Start

### List available tools on your MCP server
```bash
mcporter list $ZOHO_MCP_URL
```

### Search for a contact by name
```bash
cat << 'EOF' > /tmp/zoho_search.json
{
  "path_variables": {"module": "Contacts"},
  "query_params": {"criteria": "(Last_Name:equals:Smith)"}
}
EOF
mcporter call "$ZOHO_MCP_URL.ZohoCRM_searchRecords" --args "$(< /tmp/zoho_search.json)"
```

### Get a single record by ID
```bash
cat << 'EOF' > /tmp/zoho_record.json
{
  "path_variables": {"module": "Accounts", "recordID": "1234567890"}
}
EOF
mcporter call "$ZOHO_MCP_URL.ZohoCRM_getRecord" --args "$(< /tmp/zoho_record.json)"
```

### Run a COQL query (SQL-like)
```bash
cat << 'EOF' > /tmp/zoho_coql.json
{
  "body": {"select_query": "SELECT Id, Account_Name, Website FROM Accounts WHERE Website != '' ORDER BY Account_Name LIMIT 50"}
}
EOF
mcporter call "$ZOHO_MCP_URL.ZohoCRM_executeCOQLQuery" --args "$(< /tmp/zoho_coql.json)"
```

## Python Scripts

Ready-to-use scripts for common CRM operations. All scripts require `ZOHO_MCP_URL` to be set.

The bundled Python scripts call `mcporter` directly through `subprocess.run([...])` and do not invoke a shell. This avoids shell expansion of the credential-bearing `ZOHO_MCP_URL`.

`list_contacts.py` and `list_accounts.py` paginate automatically (they follow `more_records` until the full result set is retrieved) and normalize the different Zoho CRM MCP response shapes, so large modules are never silently truncated.

### Custom fields and filters

Every Zoho org has different custom fields. Instead of hard-coding them, the list scripts accept:

- `--fields F1,F2,...` — request any Zoho field **API names** (comma-separated), including org-specific custom fields (e.g. `Google_Drive_URL`, `Trello_URL`). Unknown fields appear under their API name in the table header.
- `--where "<COQL clause>"` (`list_accounts.py` only) — override the default WHERE filter, e.g. `--where "Google_Drive_URL != ''"`.

```bash
# Contacts with custom columns
python3 scripts/list_contacts.py --fields First_Name,Last_Name,Email,Designation

# Accounts filtered on a custom field, showing custom columns
python3 scripts/list_accounts.py \
  --where "Google_Drive_URL != ''" \
  --fields Account_Name,Website,Google_Drive_URL,Trello_URL,Trello_ID
```

Use `getFields` (see below) to discover the exact API names of your custom fields.

### list_contacts.py - Search and list contacts
```bash
# All contacts as table
python3 scripts/list_contacts.py

# Search by last name
python3 scripts/list_contacts.py --search "Smith"

# Raw JSON output
python3 scripts/list_contacts.py --json

# Full record data
python3 scripts/list_contacts.py --search "Smith" --json --full
```

### list_accounts.py - List companies/accounts
```bash
# All accounts with website
python3 scripts/list_accounts.py

# Search by company name
python3 scripts/list_accounts.py --search "Acme"

# All accounts (including those without website)
python3 scripts/list_accounts.py --all

# JSON output
python3 scripts/list_accounts.py --json
```

### search_records.py - Generic module search
```bash
# Search any module by name
python3 scripts/search_records.py Contacts "Smith"
python3 scripts/search_records.py Accounts "Acme Corp"
python3 scripts/search_records.py Deals "Project X"

# COQL query on any module
python3 scripts/search_records.py Contacts --coql "Email != ''" --json
```

## mcporter Usage Patterns

### Use temp files for shell-based JSON arguments
When calling `mcporter` directly from a shell, escaping can break inline JSON. Write arguments to a temp file:
```bash
cat << 'EOF' > /tmp/args.json
{
  "path_variables": {"module": "Contacts"},
  "query_params": {"criteria": "(Email:equals:test@example.com)"}
}
EOF
mcporter call "$ZOHO_MCP_URL.ZohoCRM_searchRecords" --args "$(< /tmp/args.json)"
```

### Pagination
For large result sets, use `page` and `per_page`:
```json
{
  "path_variables": {"module": "Contacts"},
  "query_params": {"page": 2, "per_page": 200}
}
```

### Field metadata
Get all field names for a module (useful before writing scripts or Deluge code):
```bash
cat << 'EOF' > /tmp/args.json
{
  "query_params": {"module": "Contacts", "include": "allowed_permissions_to_update"}
}
EOF
mcporter call "$ZOHO_MCP_URL.ZohoCRM_getFields" --args "$(< /tmp/args.json)"
```

## Recommended CRM Actions

For a fully capable CRM agent, enable these actions on your Zoho MCP server at [mcp.zoho.eu](https://mcp.zoho.eu):

### Read-only (safe starting point)
- `getModules` - List all CRM modules
- `getFields` - Get field definitions for any module
- `getRecord` / `getRecords` - Read individual or lists of records
- `searchRecords` - Search by criteria (email, name, etc.)
- `executeCOQLQuery` - SQL-like queries across modules
- `getRecordCount` - Count records per module
- `getRelatedRecords` - Read linked records (e.g., contacts of an account)
- `getPickListValues` - Get dropdown options for fields

### Read-write (for agents that create/update data)
- `createRecords` - Create new records in any module
- `updateRecord` - Update a single record by ID
- `upsertRecords` - Insert or update (upsert)
- `createNotes` - Add notes to records
- `createEventsRecords` - Create calendar events
- `createTags` / `postRemoveTags` - Manage tags

### Avoid enabling by default
- `deleteRecord` / `deleteRecords` - Only enable when specifically needed

## COQL Reference

COQL (Zoho's SQL-like query language) differs from standard SQL in several ways:

- No JOINs - query one module at a time
- Use single quotes for strings: `WHERE Last_Name = 'Smith'`
- DateTime format: `2026-01-01T00:00:00+01:00`
- LIMIT format: `LIMIT 20 OFFSET 0`
- Boolean: `true` / `false` (lowercase)

### Common COQL examples
```sql
-- All contacts with email
SELECT Id, Full_Name, Email FROM Contacts WHERE Email != '' LIMIT 100

-- Deals from last 3 months
SELECT Id, Deal_Name, Amount, Stage FROM Deals WHERE Created_Time >= '2026-04-01T00:00:00+01:00'

-- Accounts by city
SELECT Id, Account_Name, Billing_City FROM Accounts WHERE Billing_City = 'Berlin'
```

## Troubleshooting

### "ZOHO_MCP_URL not set"
Set the environment variable with your MCP endpoint URL. See "Environment Variable Setup" above.

### "Mandatory query param module is not present"
Use the temp-file approach with `--args "$(< /tmp/args.json)"` instead of inline JSON.

### "Invalid oauth scope to access this URL"
The MCP connection token may have expired. Go to [mcp.zoho.eu](https://mcp.zoho.eu), revoke and reconnect the affected app to get a fresh token.

### Field API name vs UI label
Zoho CRM shows display labels in the UI, but the API uses `api_name` values (e.g., `Account_Name` not "Account Name"). Always check field names with `getFields` before writing scripts or Deluge code.
