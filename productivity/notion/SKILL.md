---
name: notion
description: Use when automating Notion workflows including database CRUD, page creation,
  content publishing, and workspace management via API.
domain: productivity
author: oyi77
license: Apache-2.0
subdomain: productivity
tags:
- api
- notion
- productivity
- time-management
- tools
- workflow
version: 1.0.0
category: productivity
---

# Notion

## When to Use

**Trigger phrases:**
- "notion"
- "Help me with notion"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

invoke <skill-name> with appropriate parameters

# Advanced usage with options
invoke <skill-name> --option value --verbose
```


### Query via MCP
```
User: "Apa saja task yang overdue?"
Vilona: Uses notion_search to find tasks, notion_fetch for details
```

### Create Page
```
User: "Buat meeting notes untuk meeting yesterday"
Vilona: Uses notion_create_pages
```


## When NOT to Use

- When the tool already handles the workflow natively
- For personal preferences that do not affect output quality
- When the overhead of the system exceeds the time saved


## Overview

Notion serves as a unified workspace that combines notes, databases, wikis, calendars, and project management into a single platform. The Notion API (v1) provides programmatic access to every object in your workspace — pages, databases, blocks, users, and comments — enabling full CRUD automation. This skill covers the complete lifecycle of Notion automation: from integration setup and authentication through database querying, page creation, content publishing, and workspace-wide management.

The Notion API uses an internal_id-based addressing system where every page, database, and block is identified by a 32-character hex UUID. A database in Notion is both a container of pages AND a schema definition — each page in a database is a row whose properties (columns) conform to the database schema. This dual nature makes Notion databases powerful as lightweight application backends for content management, CRM, project tracking, and publishing workflows.

Key API capabilities include querying databases with rich filter and sort expressions, creating and updating pages with structured property values (text, select, multi-select, date, people, files, status, formula, relation, rollup), appending and modifying block children for rich document content, and searching the entire workspace. The API uses Bearer token authentication tied to a Notion integration (formerly called "bots") that must be explicitly granted access to each workspace and database.

Rate limiting is managed per-integration: 3 requests per second (RPS) burst, 90 requests per minute sustained. The API returns standard HTTP codes with detailed error JSON bodies. Pagination uses cursor-based keys with page_size parameters (default 100, max 100). Beyond basic CRUD, automation patterns include template-based page generation, bidirectional sync with external systems, bulk import/export workflows, and event-driven publishing via webhook polling or scheduled diffs.

## Daily Workflow

1. **Plan** — Review priorities and set daily objectives
2. **Execute** — Focus blocks with minimal interruptions
3. **Review** — End-of-day reflection and tomorrow's prep

## Frameworks

- **GTD (Getting Things Done)** — Capture, clarify, organize, reflect, engage
- **Pomodoro** — 25min focus + 5min break cycles
- **Eisenhower Matrix** — Urgent/Important prioritization
- **Time Blocking** — Dedicated blocks for deep work

## Tools

- Task management (Todoist, Notion, Linear)
- Calendar blocking for focus time
- Note-taking for capture and reference
- Automation for repetitive tasks

## Tips

- Batch similar tasks together
- Protect deep work time ruthlessly
- Review and adjust systems weekly
- Eliminate before optimizing


## Workflow

1. **Plan the data model** — Define database schemas (property types, relation links, formula fields). Map external data sources to Notion property types. Decide between single-page content and database-driven collections.

2. **Set up integration** — Create a Notion integration at https://www.notion.so/my-integrations. Copy the Internal Integration Secret (Bearer token). Share the target database or page with the integration from the Notion UI.

3. **Authenticate and connect** — Initialize the Notion client SDK or direct HTTP client with the Bearer token. Retrieve database metadata to confirm access. Parse the database schema to get property ID mappings.

4. **Query and transform data** — Build filtered queries using Notion's filter conditions (property filters, compound AND/OR). Process paginated results with cursor iteration. Transform API response data into the target format.

5. **Create or update pages** — Construct page create requests with correct property value formats. Handle nested block content for rich pages. Use page update (PATCH) for partial modifications. Implement idempotent upsert patterns using unique property lookups.

6. **Validate and inspect** — Read back created pages to confirm property values match. Verify block children render correctly. Test edge cases: empty values, long text truncation, relation targets, rollup recalculation.

7. **Automate and monitor** — Wrap the workflow in a scheduled task or webhook listener. Implement error handling for rate limit (429) and permission (403) responses. Add logging for each major step. Set up alerts for failures exceeding retry thresholds.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I am too busy to organize" | Disorganization costs more time than organizing. Invest upfront. |
| "Multitasking is productive" | Context switching costs 25 minutes per switch. Focus on one thing. |
| "I will remember this" | You will not. Write it down. Externalize your memory. |
| "I can just manually update 10 records" | Manual updates are error-prone and don't scale. A 5-line script that runs in 2 seconds is safer and faster. |
| "The Notion API is too limited for real work" | The API covers all core objects: databases, pages, blocks, users, comments. Limitations (no webhooks, no file upload) can be bridged with polling and external storage. |
| "My integration token worked yesterday so it's fine" | Tokens can be invalidated by workspace admin actions, re-authorization, or permission changes. Always verify access with a test query before production runs. |


## Code Examples

### Query a Database with Filters
```python
from notion_client import Client

notion = Client(auth="ntn_xxxxx_secret")
database_id = "abc123def456"

# Filter for tasks with Status = "Done" and Priority = "High"
response = notion.databases.query(
    database_id=database_id,
    filter={
        "and": [
            {"property": "Status", "status": {"equals": "Done"}},
            {"property": "Priority", "select": {"equals": "High"}},
        ]
    },
    sorts=[{"property": "Due Date", "direction": "ascending"}],
    page_size=50,
)

for page in response["results"]:
    title = page["properties"]["Name"]["title"][0]["plain_text"]
    print(f"Task: {title}")
    next_cursor = response.get("next_cursor")
    if not next_cursor:
        break
```

### Create a Page with Properties and Blocks
```python
from notion_client import Client

notion = Client(auth="ntn_xxxxx_secret")

page = notion.pages.create(
    parent={"database_id": "abc123def456"},
    properties={
        "Name": {"title": [{"text": {"content": "Meeting Notes — Q4 Review"}}]},
        "Date": {"date": {"start": "2025-10-15", "end": None}},
        "Status": {"select": {"name": "In Progress"}},
        "Attendees": {"people": [{"id": "user-uuid-here"}]},
    },
    children=[
        {"heading_2": {"rich_text": [{"text": {"content": "Agenda"}}]}},
        {"bulleted_list_item": {"rich_text": [{"text": {"content": "Review Q4 metrics"}}]}},
        {"bulleted_list_item": {"rich_text": [{"text": {"content": "Set Q5 priorities"}}]}},
        {"divider": {}},
        {"paragraph": {"rich_text": [{"text": {"content": "Full notes will be shared separately."}}]}},
    ],
)
print(f"Created page: {page['url']}")
```

### Upsert Page by Unique Property
```python
def upsert_page(notion, database_id, unique_title, properties, children=None):
    """Create a page if it doesn't exist, otherwise update it."""
    existing = notion.databases.query(
        database_id=database_id,
        filter={"property": "Name", "title": {"equals": unique_title}},
    )
    if existing["results"]:
        page_id = existing["results"][0]["id"]
        notion.pages.update(page_id=page_id, properties=properties)
        print(f"Updated page: {page_id}")
        return page_id
    page = notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "Name": {"title": [{"text": {"content": unique_title}}]},
            **properties,
        },
        children=children or [],
    )
    print(f"Created page: {page['id']}")
    return page["id"]
```

### Append Blocks to an Existing Page
```python
def append_toggle_section(notion, page_id, heading, body_lines):
    notion.blocks.children.append(
        block_id=page_id,
        children=[
            {"heading_3": {"rich_text": [{"text": {"content": heading}}]}},
            *[
                {"paragraph": {"rich_text": [{"text": {"content": line}}]}}
                for line in body_lines
            ],
        ],
    )

append_toggle_section(
    notion, "page-uuid-here",
    "Key Decisions",
    ["Decision 1: Use Notion as CMS", "Decision 2: Deploy via GitHub Actions"],
)
```

## Setup / Configuration

### Prerequisites
- A Notion workspace with admin or integration-grant access
- A Notion integration created at https://www.notion.so/my-integrations
- The Integration Token (Bearer token) from the integrations dashboard
- The target database or page shared with the integration (click Share → Invite → select your integration)
- Python 3.9+ with `pip install notion-client`

### Environment Setup
```bash
export NOTION_TOKEN="ntn_xxxxx_secret"
export NOTION_DATABASE_ID="abc123def456"
```

### SDK Initialization
```python
import os
from notion_client import Client

notion = Client(auth=os.environ["NOTION_TOKEN"])

# Verify access by fetching database metadata
db = notion.databases.retrieve(os.environ["NOTION_DATABASE_ID"])
print(f"Connected to database: {db['title'][0]['plain_text']}")
```

### Getting Property IDs
Notion uses property **names** in filter/query code but returns property data keyed by **ID** (a hashed string). Log the schema once to map names to IDs:
```python
db = notion.databases.retrieve(database_id)
for prop_name, prop_meta in db["properties"].items():
    print(f"{prop_name} -> id={prop_meta['id']}  type={prop_meta['type']}")
```

## Common Issues / Troubleshooting

| Error | Root Cause | Solution |
|---|---|---|
| `401 Unauthorized` | Invalid or revoked token | Generate a new token at the integrations dashboard. Check that the integration was re-shared with the workspace. |
| `403 Forbidden` | Integration not granted access to page/database | Open the page in Notion, click Share, and invite your integration by name. |
| `404 Not Found` | Invalid page or database ID | Verify the 32-char UUID is correct. Database IDs are the first segment in the URL after the workspace name. |
| `409 Conflict` | Duplicate page creation or concurrent edit | Implement idempotent upsert using a unique property lookup before create. Retry on conflict. |
| `429 Too Many Requests` | Rate limit exceeded (90 req/min per integration) | Implement exponential backoff. Batch operations into fewer bulk requests. Add delays between request bursts. |
| `Validation Error` | Malformed property value or filter | Check the property type and value format against the API reference. Use the schema inspection code in Setup. |
| Missing `next_cursor` | Expected more pages but got none | Ensure `page_size` is set (max 100). Verify that `start_cursor` is passed correctly on the next call. |
| Block append returns 200 but nothing shows | Wrong block type or parent block is empty toggle | Verify block type strings are lowercase with underscores. Use the Notion API docs for block type reference. |

## Monetization

| Approach | Timeframe | Description |
|---|---|---|
| Notion-powered CMS Service | 1-2 weeks | Build and sell a content management system where clients manage website/blog content in Notion databases, and a sync service publishes it to their site. Charge monthly retainer. |
| Workflow Automation Consulting | 1-4 weeks | Offer Notion API automation to small businesses: CRM pipelines, invoice tracking, meeting notes automation. Fixed-price per automation ($200-$2000). |
| Notion Template Marketplace | 2-4 weeks | Create premium Notion templates with integrated API automations (project dashboards, content calendars, CRM). Sell on Gumroad or Notion marketplace. |
| Internal Tool Builder | 2-8 weeks | Build custom internal tools for companies using Notion as the data layer — inventory tracking, order management, HR onboarding. Monthly SaaS subscription. |
| Integration-as-a-Service | 4-12 weeks | Develop a generic sync adapter (Notion ↔ Google Sheets, Notion ↔ Airtable, Notion ↔ Slack) and sell it as a managed service with per-workspace pricing. |
| Data Migration Service | 1-3 weeks | Migrate clients from Airtable, Excel, or Monday.com into structured Notion databases. Charge per table/database migrated ($100-$500 each). |

## Process

### Preparation
- Identify the automation target: database-backed collection, single-page content, or workspace-wide sync.
- Map the data model: list all property names, types, and expected value formats.
- Create the Notion integration and share it with target pages/databases.
- Install dependencies: `pip install notion-client` (or use raw HTTP with `httpx`).
- Verify connectivity with a test database retrieve or page fetch.

### Execution
- Query existing data to confirm the filter and sort logic before creating or modifying.
- Use the upsert pattern (query by unique property → create or update) for idempotent operations.
- Append block children in batches of max 100 blocks per API call.
- Handle pagination with cursor iteration in a loop.
- Log each page created, updated, or skipped for audit trail.

### Stewardship
- Monitor API usage to stay under rate limits (90 req/min). Schedule large imports during low-traffic windows.
- Rotate integration tokens periodically and update secrets in all consumers.
- Archive or unshare databases when automations are decommissioned to avoid stale permission warnings.
- Keep a schema registry (JSON file or Notion page) documenting all automated database schemas and their integration purposes.


## Verification

- [ ] Integration token is valid and the target database/page is shared with the integration
- [ ] Database query with filters returns expected results (test with known data)
- [ ] Page creation completes with all properties populated correctly
- [ ] Block children render as expected (headings, paragraphs, lists, dividers)
- [ ] Upsert pattern works: first call creates, second call updates the same page
- [ ] Pagination handled correctly across all result pages
- [ ] Rate limit handling implemented with exponential backoff
- [ ] Error cases produce meaningful log messages
- [ ] Integration token stored securely (environment variable, vault, not hardcoded)