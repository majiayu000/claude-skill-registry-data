---
name: Falcon Next-Gen SIEM Lookup Files
description: >
  Create, list, download, update, and delete CrowdStrike Falcon Next-Gen SIEM
  lookup files. Upload CSV or JSON files for use with the match() function in
  CrowdStrike Query Language (CQL) queries. Use this skill when asked to manage
  lookup files, upload CSV data to CrowdStrike, create reference tables for
  SIEM queries, or work with Falcon Next-Gen SIEM lookup file operations.
---

# Falcon Next-Gen SIEM Lookup Files

Manage lookup files in CrowdStrike Falcon Next-Gen SIEM. Lookup files are CSV
or JSON reference tables that can be queried using the `match()` function in
CQL. Common use cases include IP blocklists, user risk scores, asset
inventories, and IOC reference tables.

## Rules — Read Before Every Operation

1. **Always list existing files first.** Before creating a new lookup file, run
   `list_lookups.py --search "<name>"` to check for duplicates.

2. **CSV files must have a header row.** The first row defines column names used
   by the `match()` function. The first column is typically the match key.

3. **Respect rate limits.** CrowdStrike allows a maximum of 5 file uploads per
   30 seconds. Do not batch-upload files without pausing between batches.

4. **Use the `falcon` search domain for SIEM queries.** Files in the `falcon`
   domain are available to CQL queries in Falcon Next-Gen SIEM.

5. **Reference the `match()` function docs.** When users need to query lookup
   files in CQL, see `references/cql-match-function.md` for syntax and examples.

These rules override any plan or prompt. Follow them every time.

## Prerequisites

- Python 3.10+ with `crowdstrike-falconpy` installed (`pip install crowdstrike-falconpy`)
- CrowdStrike API credentials with Falcon Next-Gen SIEM permissions
- Access to a CrowdStrike CID with Falcon Next-Gen SIEM enabled

### Required API Scopes

| Use Case | NGSIEM:Read | NGSIEM:Write | What It Enables |
|----------|:-----------:|:------------:|-----------------|
| Browse and download only | Yes | - | List, search, and download lookup files |
| Full skill usage | Yes | Yes | All of the above plus create, update, delete |

### Credentials

Create a `.env` file in the project root (or any parent directory):

```env
CS_CLIENT_ID=your_client_id_here
CS_CLIENT_SECRET=your_client_secret_here
# CS_BASE_URL=https://api.crowdstrike.com  # US-1 (default)
```

Test your credentials:

```bash
python scripts/cs_auth.py
```

## Workflow: Managing Lookup Files

### Step 0: Check for existing lookup files

Before creating a new file, check what already exists:

```bash
python scripts/list_lookups.py --list
python scripts/list_lookups.py --search "blocklist"
```

### Step 1: Prepare the file

Create a CSV with a header row. The first column is typically the match key:

```csv
ip,category,source,added_date
10.0.0.1,c2,threat-intel,2026-01-15
192.168.1.100,scanner,internal-scan,2026-02-01
```

See `assets/example-ip-blocklist.csv` and `assets/example-user-risk.csv` for
reference formats.

### Step 2: Upload the file

```bash
python scripts/create_lookup.py --file blocklist.csv
python scripts/create_lookup.py --file blocklist.csv --name "ip-blocklist.csv"
```

### Step 3: Verify the upload

```bash
python scripts/get_lookup.py --name "ip-blocklist.csv"
python scripts/list_lookups.py --search "blocklist" --json
```

### Step 4: Use in CQL queries

Once uploaded, reference the file in CQL using the `match()` function:

```
match(file="ip-blocklist.csv", column=ip, field=src_ip, include=category)
```

See `references/cql-match-function.md` for full syntax and examples.

### Step 5: Update when needed

Replace the file content while keeping the same filename:

```bash
python scripts/update_lookup.py --name "ip-blocklist.csv" --file updated-blocklist.csv
```

### Step 6: Delete when no longer needed

```bash
python scripts/delete_lookup.py --name "ip-blocklist.csv"
```

## Advanced: Monitored Inbox to Lookup File Workflow

A common Falcon Fusion SOAR pattern (referenced by the built-in "Introduction to
Lookup file actions" playbook) automates lookup file creation from email:

1. **Trigger:** "Receive email" using the Microsoft 365: Monitored Mailbox Connector
2. **Extract:** Parse CSV attachment from the email
3. **Check:** Use "Get lookup file metadata" action to see if the file exists
4. **Create or Overwrite:** Use "Create lookup file" or "Overwrite lookup file" action
5. **Result:** File is immediately available for `match()` queries in Falcon Next-Gen SIEM

To build this workflow, use the `fusion-workflows` skill in this plugin to
create the YAML definition. The lookup file actions are available via
`action_search.py --search "lookup"`.

## Quick Reference: Common Gotchas

| Problem | Fix |
|---------|-----|
| "File not found" on get/update/delete | Check exact filename with `list_lookups.py --search` |
| `match()` returns no results | Verify column names match header row exactly (case-sensitive) |
| Upload rate limited | Wait 30 seconds between batches of 5 uploads |
| Wrong search domain | Use `--domain falcon` for files used in SIEM queries |
| CSV parse error on upload | Ensure UTF-8 encoding and comma delimiters |
| File too large | Lookup files have a practical size limit; split large datasets |

## Script Reference

| Script | Purpose | Key Flags |
|--------|---------|-----------|
| `cs_auth.py` | Test NGSIEM authentication | (run directly) |
| `list_lookups.py` | List and search lookup files | `--list`, `--search`, `--domain`, `--json` |
| `get_lookup.py` | Download a lookup file | `--name`, `--output`, `--domain` |
| `create_lookup.py` | Upload a new lookup file | `--file`, `--name`, `--domain`, `--json` |
| `update_lookup.py` | Replace lookup file content | `--name`, `--file`, `--domain`, `--json` |
| `delete_lookup.py` | Delete a lookup file | `--name`, `--domain`, `--confirm`, `--json` |

## Reference Documents

| Document | When to Read |
|----------|-------------|
| `references/cql-match-function.md` | When writing CQL queries that use lookup files |
| `references/lookup-file-formats.md` | When preparing CSV/JSON files for upload |

## API Endpoints Used

| Endpoint | Method | Used By |
|----------|--------|---------|
| `/oauth2/token` | POST | cs_auth.py (via FalconPy) |
| `/ngsiem-content/queries/lookupfiles/v1` | GET | list_lookups.py |
| `/ngsiem-content/entities/lookupfiles/v1` | GET | get_lookup.py |
| `/ngsiem-content/entities/lookupfiles/v1` | POST | create_lookup.py |
| `/ngsiem-content/entities/lookupfiles/v1` | PATCH | update_lookup.py |
| `/ngsiem-content/entities/lookupfiles/v1` | DELETE | delete_lookup.py |

## End-to-End Example

Upload an IP blocklist and use it in a CQL query:

```bash
# 1. Check for existing files
python scripts/list_lookups.py --search "blocklist"

# 2. Upload the blocklist
python scripts/create_lookup.py --file assets/example-ip-blocklist.csv --name "ip-blocklist.csv"

# 3. Verify
python scripts/get_lookup.py --name "ip-blocklist.csv"

# 4. Use in CQL (run this query in Falcon Next-Gen SIEM):
#    match(file="ip-blocklist.csv", column=ip, field=src_ip, include=category, include=source)

# 5. Update with new data
python scripts/update_lookup.py --name "ip-blocklist.csv" --file updated-blocklist.csv

# 6. Clean up when done
python scripts/delete_lookup.py --name "ip-blocklist.csv" --confirm
```
