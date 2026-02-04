---
name: notion-master
description: Shared resource library for Notion integration skills. DO NOT load directly - this provides common references (setup, API docs, error handling, database schema) and scripts used by notion-connect, query-notion-db, import-skill-to-nexus, and export-skill-to-notion.
---

# Notion Master

**This is NOT a user-facing skill.** It's a shared resource library referenced by Notion integration skills.

## Purpose

Provides shared resources to eliminate duplication across:
- `notion-connect` - Meta-skill for complete Notion workspace integration (NEW)
- `query-notion-db` - Browse and search Notion skills database
- `import-skill-to-nexus` - Download skills from Notion to local Nexus
- `export-skill-to-notion` - Push skills to Notion for team sharing

**Instead of loading this skill**, users directly invoke the specific skill they need above.

---

## Architecture: DRY Principle

**Problem solved:** The 3 Notion skills had 950 lines of duplicated content (setup wizard 3x, API docs 3x, error tables 3x).

**Solution:** Extract shared content into `notion-master/references/` and `notion-master/scripts/`, then reference from each skill.

**Result:** 60% context reduction (950 → 370 lines in SKILL.md files)

---

## Shared Resources

All 3 Notion skills reference these resources (progressive disclosure).

### references/

**[setup-guide.md](references/setup-guide.md)** - Complete setup wizard
- Getting Notion API key
- Finding database ID
- Configuring .env and user-config.yaml
- Getting user's Notion ID

**[api-reference.md](references/api-reference.md)** - Notion API patterns
- Database query API
- File upload API (3-step process)
- File download API (3-step process)
- Common curl examples

**[error-handling.md](references/error-handling.md)** - Troubleshooting
- Common errors and solutions
- API error codes
- Configuration issues
- Network and timeout handling

**[database-schema.md](references/database-schema.md)** - Beam Nexus Skills database
- Property types and descriptions
- Available Teams and Integrations
- Field mapping table
- Example entries

**[filter-syntax.md](references/filter-syntax.md)** - Query filter syntax
- Operators by property type
- Common filter patterns
- Sorting options

**[property-types.md](references/property-types.md)** - Property type reference
- All 20+ property types
- Read and write formats
- Validation rules

**[block-types.md](references/block-types.md)** - Block type reference
- All 50+ block types
- Block schemas and examples
- Rich text formatting

### scripts/

#### Configuration & Setup

**[check_notion_config.py](scripts/check_notion_config.py)** - Pre-flight validation
```bash
python check_notion_config.py [--json]
```
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--json` | No | False | Output structured JSON for AI consumption |

Exit codes: 0=configured, 1=partial, 2=not configured

**When to Use:** Run this FIRST before any Notion operation. Use to validate API key is configured, check if Skills DB ID is set, diagnose connection issues, or determine if setup wizard is needed.

---

**[setup_notion.py](scripts/setup_notion.py)** - Interactive setup wizard
```bash
python setup_notion.py
```
No arguments - runs interactively. Guides through API key setup, tests connection, saves to `.env`, gets user's Notion ID, auto-runs database discovery.

**When to Use:** Use when Notion integration needs initial setup, when check_notion_config.py returns exit code 2, or when user needs to reconfigure credentials or change integration settings.

---

**[discover_databases.py](scripts/discover_databases.py)** - Database discovery (POST /search)
```bash
python discover_databases.py [--refresh] [--json] [--detailed]
```
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--refresh` | No | False | Force refresh even if context file exists |
| `--json` | No | False | Output JSON only (no file save) |
| `--detailed` | No | False | Fetch full schema for each database (slower) |

Saves to: `01-memory/integrations/notion-databases.yaml`

**When to Use:** Use when user asks "what databases do I have", "list my notion databases", after connecting a new integration, or when database name resolution fails (--refresh to update cache).

---

#### Database Querying

**[search_skill_database.py](scripts/search_skill_database.py)** - Unified database querying (POST /databases/{id}/query)
```bash
# General mode
python search_skill_database.py --db "Database Name" [--filter EXPR] [--sort FIELD] [--sort-dir asc|desc] [--limit N] [--json]

# Skills DB preset mode
python search_skill_database.py --skills [--team TEAM] [--integration INT] [--name TEXT] [--owner ID] [--json]
```
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--db` | No* | - | Database name or ID (fuzzy match) |
| `--skills` | No* | False | Query Beam Nexus Skills database (preset mode) |
| `--team` | No | - | [Skills mode] Filter by team (General, Solutions, etc.) |
| `--integration` | No | - | [Skills mode] Filter by integration (Beam AI, Linear, etc.) |
| `--name` | No | - | [Skills mode] Filter by skill name (partial match) |
| `--owner` | No | - | [Skills mode] Filter by owner user ID |
| `--filter` | No | - | Filter expression (see syntax below) |
| `--sort` | No | - | Property name to sort by |
| `--sort-dir` | No | desc | Sort direction: asc or desc |
| `--limit` | No | - | Limit number of results |
| `--json` | No | False | Output raw JSON |

*Either `--db` or `--skills` is required

**Filter Syntax:**
```
--filter "Status = Active"           # Equals
--filter "Status != Done"            # Not equals
--filter "Name contains project"     # Contains
--filter "Priority > 5"              # Greater than
--filter "Due Date < 2025-01-01"     # Less than
--filter "Tags is_empty"             # Is empty
--filter "Tags is_not_empty"         # Is not empty
```

**When to Use:** Use when user wants to query any Notion database, search for records, filter by properties, find skills in the Skills DB (--skills mode), or list database contents with sorting/pagination.

---

#### Page Operations

**[create_page.py](scripts/create_page.py)** - Create page in database (POST /pages)
```bash
python create_page.py --db "Database" [--properties JSON] [--interactive] [--json]
```
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--db` | **Yes** | - | Database name or ID (fuzzy match) |
| `--properties` | No | - | JSON object with property values |
| `--interactive` | No | False | Prompt for each property |
| `--json` | No | False | Output raw JSON |

**When to Use:** Use when user wants to add a new entry to a database, create a new record, or add an item to a Notion table. Use --interactive for guided property entry.

---

**[manage_page.py](scripts/manage_page.py)** - Page management (GET/PATCH /pages/{id})
```bash
python manage_page.py get --page PAGE_ID [--json]
python manage_page.py update --page PAGE_ID --properties JSON [--json]
python manage_page.py delete --page PAGE_ID [--confirm] [--json]
```

**Subcommand: get**
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--page` | **Yes** | - | Page ID |
| `--json` | No | False | Output raw JSON |

**Subcommand: update**
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--page` | **Yes** | - | Page ID |
| `--properties` | **Yes** | - | JSON object with property values |
| `--json` | No | False | Output raw JSON |

**Subcommand: delete**
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--page` | **Yes** | - | Page ID |
| `--confirm` | No | False | Skip confirmation prompt |
| `--json` | No | False | Output raw JSON |

**When to Use:** Use `get` to retrieve page details/properties, `update` to modify page properties (status, tags, dates), `delete` to archive/remove pages. Requires page ID from query results.

---

#### Database Management

**[manage_database.py](scripts/manage_database.py)** - Database operations (POST/PATCH /databases)
```bash
python manage_database.py create --parent PAGE_ID --title "Title" [--properties JSON] [--inline] [--json]
python manage_database.py update --db DB_ID [--title TEXT] [--add-property JSON] [--update-property JSON] [--json]
```

**Subcommand: create**
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--parent` | **Yes** | - | Parent page ID |
| `--title` | **Yes** | - | Database title |
| `--properties` | No | `[]` | JSON array of property definitions |
| `--inline` | No | False | Create inline database |
| `--json` | No | False | Output raw JSON |

**Subcommand: update**
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--db` | **Yes** | - | Database ID |
| `--title` | No | - | New title |
| `--add-property` | No | - | JSON property definition to add |
| `--update-property` | No | - | JSON property update |
| `--json` | No | False | Output raw JSON |

**When to Use:** Use `create` to make a new database inside a page, `update` to add/modify database properties (columns), change database title, or add new select options.

---

#### Block Operations

**[manage_blocks.py](scripts/manage_blocks.py)** - Block operations (GET/PATCH/DELETE /blocks/{id})
```bash
python manage_blocks.py get --block BLOCK_ID [--json]
python manage_blocks.py children --block BLOCK_ID [--limit N] [--all] [--json]
python manage_blocks.py append --block BLOCK_ID [--content JSON] [--type TYPE] [--text TEXT] [--language LANG] [--checked] [--json]
python manage_blocks.py update --block BLOCK_ID --content JSON [--json]
python manage_blocks.py delete --block BLOCK_ID [--confirm] [--json]
```

**Subcommand: get**
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--block` | **Yes** | - | Block ID |
| `--json` | No | False | Output raw JSON |

**Subcommand: children**
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--block` / `--page` | **Yes** | - | Block or page ID |
| `--limit` | No | 50 | Max blocks to return |
| `--all` | No | False | Fetch all pages |
| `--json` | No | False | Output raw JSON |

**Subcommand: append**
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--block` / `--page` | **Yes** | - | Parent block or page ID |
| `--content` | No | - | JSON block content |
| `--type` | No | - | Block type (paragraph, heading_1, etc.) |
| `--text` | No | - | Text content |
| `--language` | No | - | Code block language |
| `--checked` | No | False | For to_do blocks |
| `--json` | No | False | Output raw JSON |

**Subcommand: update**
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--block` | **Yes** | - | Block ID |
| `--content` | **Yes** | - | JSON block content |
| `--json` | No | False | Output raw JSON |

**Subcommand: delete**
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--block` | **Yes** | - | Block ID |
| `--confirm` | No | False | Skip confirmation |
| `--json` | No | False | Output raw JSON |

**When to Use:** Use `get` to retrieve block info, `children` to read page content, `append` to add text/headings/code blocks to pages, `update` to modify existing blocks, `delete` to remove content.

---

#### User Management

**[manage_users.py](scripts/manage_users.py)** - User operations (GET /users)
```bash
python manage_users.py list [--limit N] [--all] [--save] [--json]
python manage_users.py get --user USER_ID [--json]
python manage_users.py me [--json]
```

**Subcommand: list**
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--limit` | No | 100 | Max users to return |
| `--all` | No | False | Fetch all pages |
| `--save` | No | False | Save users to context file |
| `--json` | No | False | Output raw JSON |

**Subcommand: get**
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--user` | **Yes** | - | User ID |
| `--json` | No | False | Output raw JSON |

**Subcommand: me**
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--json` | No | False | Output raw JSON |

**When to Use:** Use `list` to see all workspace members, `get` to lookup a specific user, `me` to get current authenticated user/bot identity (useful for setting notion_user_id during setup).

---

#### Comment Operations

**[manage_comments.py](scripts/manage_comments.py)** - Comment operations (GET/POST /comments)
```bash
python manage_comments.py list --block BLOCK_ID [--limit N] [--all] [--json]
python manage_comments.py create --page PAGE_ID --text "Comment text" [--json]
python manage_comments.py create --discussion THREAD_ID --text "Reply text" [--json]
python manage_comments.py get --comment COMMENT_ID [--json]
```

**Subcommand: list**
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--block` / `--page` | **Yes** | - | Block or page ID |
| `--limit` | No | 50 | Max comments |
| `--all` | No | False | Fetch all pages |
| `--json` | No | False | Output raw JSON |

**Subcommand: create**
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--page` | No* | - | Page ID for new comment |
| `--discussion` | No* | - | Discussion thread ID for reply |
| `--text` | **Yes** | - | Comment text |
| `--json` | No | False | Output raw JSON |

*Either `--page` or `--discussion` is required

**Subcommand: get**
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--comment` | **Yes** | - | Comment ID |
| `--json` | No | False | Output raw JSON |

Note: Requires "Insert comments" capability in integration settings.

**When to Use:** Use `list` to read comments on a page, `create` to add comments or reply to threads, `get` to retrieve specific comment details. Great for collaboration and feedback workflows.

---

#### Skill Import/Export

**[download_skill.py](scripts/download_skill.py)** - Download skill from Notion
```bash
python download_skill.py PAGE_ID [PAGE_ID2 ...] [--output-dir PATH] [--no-backup] [--json]
```
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `page_ids` | **Yes** | - | One or more Notion page IDs (positional) |
| `--output-dir` | No | `03-skills` | Output directory for skill folder |
| `--no-backup` | No | False | Don't backup existing skills |
| `--json` | No | False | Output result as JSON |

**When to Use:** Use when user wants to import a skill from the Skills DB, download a skill bundle from Notion, or sync a skill from the team repository to local Nexus.

---

**[upload_skill.py](scripts/upload_skill.py)** - Upload skill to Notion
```bash
python upload_skill.py SKILL_PATH --team TEAM [--integration LIST] [--dry-run] [--as-new NAME] [--skip-validation] [--json]
```
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `skill_path` | **Yes** | - | Path to skill folder (positional) |
| `--team` | **Yes** | - | Team: General, Solutions, Engineering, Sales |
| `--integration` | No | - | Comma-separated integrations (Beam AI, Linear, etc.) |
| `--dry-run` | No | False | Preview upload without pushing |
| `--as-new` | No | - | Upload as new skill with different name |
| `--skip-validation` | No | False | Skip SKILL.md validation |
| `--json` | No | False | Output as JSON |

**When to Use:** Use when user wants to share a local skill to the team, export a skill to Notion, or publish a skill to the Skills DB for others to use.

---

#### Utility Module

**[rate_limiter.py](scripts/rate_limiter.py)** - Rate limit handling (module, not CLI)
```python
from rate_limiter import with_retry, RateLimiter, make_request_with_retry

# Decorator usage
@with_retry(max_retries=3, base_delay=1.0)
def my_api_call():
    return requests.get(...)

# Direct usage
limiter = RateLimiter(max_retries=3, base_delay=1.0)
response = limiter.execute(lambda: requests.get(...))
```
Features: Exponential backoff, jitter, respects Retry-After header, auto-retry on 429/5xx

**When to Use:** This is a library module, not a CLI script. Import it in Python code when making direct API calls that need rate limit protection (3 req/s limit).

---

## Intelligent Error Detection Flow

When a Notion skill fails due to missing configuration, the AI should:

### Step 1: Run Config Check with JSON Output

```bash
python 00-system/skills/notion/notion-master/scripts/check_notion_config.py --json
```

### Step 2: Parse the `ai_action` Field

The JSON output includes an `ai_action` field that tells the AI what to do:

| ai_action | What to Do |
|-----------|------------|
| `proceed_with_operation` | Config OK, continue with the original operation |
| `proceed_with_warning` | Partial config (can query/import but not export) |
| `prompt_for_api_key` | Ask user: "I need your Notion API key. Get one at https://www.notion.so/my-integrations" |
| `create_env_file` | Create `.env` file and ask user for API key |
| `run_setup_wizard` | Run: `python 00-system/skills/notion/notion-master/scripts/setup_notion.py` |

### Step 3: Help User Fix Issues

If `ai_action` is `prompt_for_api_key`:

1. Tell user: "Notion integration needs setup. I need your API key."
2. Show them: "Get one at: https://www.notion.so/my-integrations"
3. Ask: "Paste your Notion API key here:"
4. Once they provide it, **write directly to `.env`**:
   ```
   # Edit .env file to add:
   NOTION_API_KEY=secret_their_key_here
   NOTION_SKILLS_DB_ID=2bc2cadf-bbbc-80be-af8a-d45dfc8dfa2e
   ```
5. Re-run config check to verify

### JSON Output Structure

```json
{
  "status": "not_configured",
  "exit_code": 2,
  "ai_action": "prompt_for_api_key",
  "missing": [
    {"item": "NOTION_API_KEY", "required": true, "location": ".env"}
  ],
  "fix_instructions": [...],
  "env_template": "NOTION_API_KEY=secret_YOUR_API_KEY_HERE\nNOTION_SKILLS_DB_ID=...",
  "setup_wizard": "python 00-system/skills/notion/notion-master/scripts/setup_notion.py"
}
```

---

## How Skills Reference This

Each skill loads shared resources **only when needed** (progressive disclosure):

**notion-connect** uses:
- All discovery and query scripts
- All page, block, user, and comment management scripts
- All references (filter-syntax, property-types, block-types)

**query-notion-db** uses:
- `check_notion_config.py` (validate before query)
- `api-reference.md` (query patterns)
- `error-handling.md` (troubleshooting)

**import-skill-to-nexus** uses:
- `check_notion_config.py` (validate before import)
- `api-reference.md` (file download API)
- `error-handling.md` (troubleshooting)

**export-skill-to-notion** uses:
- `check_notion_config.py` (validate before export)
- `api-reference.md` (file upload API)
- `database-schema.md` (field mapping)
- `error-handling.md` (troubleshooting)

---

## Usage Example

**User says:** "query my Projects database"

**What happens:**
1. AI loads `notion-connect` skill (NOT notion-master)
2. `notion-connect` SKILL.md says: "Run check_notion_config.py first"
3. AI executes: `python notion-master/scripts/check_notion_config.py`
4. AI executes: `python notion-master/scripts/search_skill_database.py --db "Projects"`
5. If errors occur, AI loads: `notion-master/references/error-handling.md`

**notion-master is NEVER loaded directly** - it's just a resource library.

---

**Version**: 2.6
**Created**: 2025-12-10
**Updated**: 2025-12-11
**Status**: Production Ready

**Changelog**:
- v2.6: Added "When to Use" sections to all 13 scripts for AI routing guidance
- v2.5: Added comprehensive script argument documentation with usage examples and argument tables
- v2.4: Added Intelligent Error Detection Flow with `--json` support for AI-guided setup
- v2.3: Renamed `query_database.py` to `search_skill_database.py` for clarity
