---
name: notion-connect
description: "Connect to any Notion database by name. Load when user mentions 'notion', 'connect notion', 'setup notion', 'query [database-name]', 'add to [database]', 'notion databases', or any database name from persistent context. Meta-skill that discovers workspace, caches schemas, and routes to appropriate operations."
version: "1.1"
---

# Notion Connect

**Meta-skill for complete Notion workspace integration.**

## Purpose

Enable natural language interaction with ANY Notion database. User says "query my Projects database" or "add a page to CRM" and it just works - no manual API calls, no remembering database IDs, no schema lookups.

---

## Shared Resources

This skill uses `notion-master` shared library. Load references as needed:

| Resource | When to Load |
|----------|--------------|
| `notion-master/scripts/check_notion_config.py` | Always first (pre-flight) |
| `notion-master/references/setup-guide.md` | If config check fails |
| `notion-master/references/error-handling.md` | On any API errors |
| `notion-master/references/api-reference.md` | For API details |

---

## First-Time User Setup

**If user has never used Notion integration before:**

1. Run config check to detect setup state:
   ```bash
   python 00-system/skills/notion-master/scripts/check_notion_config.py
   ```

2. If exit code 2 (not configured), run the interactive setup wizard:
   ```bash
   python 00-system/skills/notion-master/scripts/setup_notion.py
   ```

   The wizard will:
   - Guide user to get/enter API key
   - Save configuration to `.env`
   - Get user's Notion ID (for export functionality)
   - Save to `user-config.yaml`
   - Auto-run database discovery
   - Create `01-memory/integrations/notion-databases.yaml`

3. After setup completes, user can immediately start querying databases

**Setup triggers**: "setup notion", "connect notion", "configure notion"

---

## Workflow 0: Config Check (ALWAYS FIRST)

Every workflow MUST start with config validation:

```bash
python 00-system/skills/notion-master/scripts/check_notion_config.py
```

**Exit code meanings:**
- **Exit 0**: Fully configured (query, import, AND export all work)
- **Exit 1**: Partial config (query and import work, export needs user ID)
- **Exit 2**: Not configured (run setup wizard)

**If exit code 2** (config incomplete):
1. Tell user: "Notion integration needs to be set up first."
2. Run: `python 00-system/skills/notion-master/scripts/setup_notion.py`
3. Restart workflow after setup complete

**If exit code 0 or 1**: Continue to requested operation

---

## Workflow 1: Discover Databases

**Triggers**: "connect notion", "sync notion", "discover databases", "what databases", "refresh notion"

**Purpose**: Find all accessible databases in user's Notion workspace and cache schemas.

**Steps**:
1. Run config check (Workflow 0)
2. Run discovery script:
   ```bash
   python 00-system/skills/notion-master/scripts/discover_databases.py
   ```
3. Script outputs:
   - Number of databases found
   - Database names and IDs
   - Creates/updates: `01-memory/integrations/notion-databases.yaml`
4. Show user summary of discovered databases
5. Confirm context file saved

**First-time flow**: If `notion-databases.yaml` doesn't exist, discovery runs automatically.

---

## Workflow 2: Query Database

**Triggers**: "query [database]", "find in [database]", "search [database]", "show [database]", "list [database]"

**Purpose**: Query any database by name with optional filters.

**Steps**:
1. Run config check (Workflow 0)
2. Load context: Read `01-memory/integrations/notion-databases.yaml`
   - If file doesn't exist → Run Workflow 1 (Discover) first
3. Match database name (fuzzy):
   - User says "Projects" → matches "Client Projects", "My Projects", etc.
   - If multiple matches → Show disambiguation prompt
   - If no match → Suggest running discovery
4. Run query:
   ```bash
   python 00-system/skills/notion-master/scripts/search_skill_database.py --db <database_id> [--filter "..."] [--sort ...] [--limit N]
   ```
5. Format and display results using property types from cached schema
6. Offer follow-up actions: "Want to add a page?" / "Query with different filters?"

**Filter Syntax** (load `notion-master/references/filter-syntax.md` if user needs help):
- `--filter "Status = Active"`
- `--filter "Priority = High"`
- `--filter "Tags contains Design"`

**Note**: Currently supports single filter per query. Multiple filters (AND/OR) planned for future.

---

## Workflow 3: Create Page

**Triggers**: "add to [database]", "create in [database]", "new [item] in [database]"

**Purpose**: Create a new page in any database with property validation.

**Steps**:
1. Run config check (Workflow 0)
2. Load context and match database (same as Workflow 2)
3. Load schema for target database from context file
4. Prompt user for required properties based on schema:
   - Show property name + type + options (for select/multi-select)
   - Validate input against property type
5. Run create:
   ```bash
   python 00-system/skills/notion-master/scripts/create_page.py --db <database_id> --properties '{"Title": "...", "Status": "..."}'
   ```
6. Confirm creation with page URL
7. Offer: "Add another?" / "View in Notion?"

---

## Workflow 4: Manage Database Schema

**Triggers**: "create database", "new database", "add property to [database]", "update [database] schema"

**Purpose**: Create new databases or modify existing database schemas.

**Steps**:

### Create New Database
1. Run config check (Workflow 0)
2. Get parent page ID (where database will live)
3. Define database name and properties:
   ```bash
   python 00-system/skills/notion-master/scripts/manage_database.py create \
     --parent <page_id> \
     --title "Database Name" \
     --properties '[{"name": "Name", "type": "title"}, {"name": "Status", "type": "select", "options": ["Todo", "Done"]}]'
   ```
4. Confirm creation with database URL
5. Run discovery to update context: `python discover_databases.py`

### Update Schema (Add Property)
1. Run config check
2. Match database name (fuzzy) from context
3. Run schema update:
   ```bash
   python 00-system/skills/notion-master/scripts/manage_database.py update \
     --db <database_id> \
     --add-property '{"name": "Priority", "type": "select", "options": ["Low", "Medium", "High"]}'
   ```
4. Run discovery to refresh context

**Supported Property Types for Creation**:
- `title` - Primary name field (required, one per database)
- `rich_text` - Multi-line text
- `number` - Numeric values (with optional precision)
- `select` - Single choice from options
- `multi_select` - Multiple choices from options
- `date` - Date/datetime
- `checkbox` - Boolean true/false
- `url`, `email`, `phone_number` - Validated text fields
- `people` - User assignment
- `relation` - Link to another database

---

## Workflow 5: Update Page

**Triggers**: "update [page]", "edit [page]", "change [property] to [value]", "modify page"

**Purpose**: Modify properties of an existing page.

**Steps**:
1. Run config check (Workflow 0)
2. Identify page:
   - By page ID if known
   - By title search in database: `python search_skill_database.py --db <id> --filter "Name contains [search]"`
3. Show current properties
4. Accept changes from user
5. Run update:
   ```bash
   python 00-system/skills/notion-master/scripts/manage_page.py update \
     --page <page_id> \
     --properties '{"Status": "Done", "Priority": "High"}'
   ```
6. Confirm changes with updated page details

---

## Workflow 6: Get/Delete Page

**Triggers**: "get page [id]", "show page details", "delete page", "remove [page]"

**Purpose**: Retrieve full page details or delete a page.

**Steps**:

### Get Page
1. Run config check
2. Run retrieval:
   ```bash
   python 00-system/skills/notion-master/scripts/manage_page.py get --page <page_id>
   ```
3. Display all properties in formatted output

### Delete Page (Archive)
1. Run config check
2. Confirm with user: "Are you sure you want to delete [page title]?"
3. Run deletion:
   ```bash
   python 00-system/skills/notion-master/scripts/manage_page.py delete --page <page_id>
   ```
4. Confirm page archived (Notion doesn't hard-delete, only archives)

---

## Workflow 7: Manage Content/Blocks

**Triggers**: "append to [page]", "add section to [page]", "edit content of [page]", "list blocks", "delete block"

**Purpose**: Read, append, update, and delete content blocks within pages.

**Steps**:

### List Page Content
1. Run config check (Workflow 0)
2. Get page blocks:
   ```bash
   python 00-system/skills/notion-master/scripts/manage_blocks.py children --page <page_id>
   ```
3. Display block hierarchy with types and previews

### Append Content
1. Run config check
2. Identify target page/block
3. Build block content (simple or complex):
   ```bash
   # Simple block
   python 00-system/skills/notion-master/scripts/manage_blocks.py append \
     --page <page_id> --type paragraph --text "Your content here"

   # Multiple blocks
   python 00-system/skills/notion-master/scripts/manage_blocks.py append \
     --page <page_id> --content '[{"type": "heading_1", ...}, {"type": "paragraph", ...}]'
   ```
4. Confirm appended blocks

### Update Block
1. Run config check
2. Get block ID (from children list or user)
3. Update block content:
   ```bash
   python 00-system/skills/notion-master/scripts/manage_blocks.py update \
     --block <block_id> --content '{"paragraph": {"rich_text": [...]}}'
   ```
4. Confirm update

### Delete Block
1. Run config check
2. Confirm with user: "Delete block [preview]?"
3. Delete block:
   ```bash
   python 00-system/skills/notion-master/scripts/manage_blocks.py delete --block <block_id> --confirm
   ```

**Supported Block Types** (load `notion-master/references/block-types.md` for full list):
- Text: `paragraph`, `heading_1`, `heading_2`, `heading_3`, `quote`, `callout`
- Lists: `bulleted_list_item`, `numbered_list_item`, `to_do`, `toggle`
- Code: `code` (with language), `equation`
- Media: `image`, `video`, `file`, `bookmark`
- Structure: `divider`, `table_of_contents`

---

## Workflow 8: User Management

**Triggers**: "list users", "who can access", "get user", "find user"

**Purpose**: List workspace users and get user details for @mentions.

**Steps**:

### List All Users
1. Run config check (Workflow 0)
2. List workspace users:
   ```bash
   python 00-system/skills/notion-master/scripts/manage_users.py list --save
   ```
3. Display user list with IDs (for people properties and @mentions)
4. Optionally save to `01-memory/integrations/notion-users.yaml`

### Get Current Bot
1. Run config check
2. Get bot info:
   ```bash
   python 00-system/skills/notion-master/scripts/manage_users.py me
   ```
3. Display integration details

---

## Workflow 9: Comments

**Triggers**: "add comment", "list comments", "comment on [page]", "reply to comment"

**Purpose**: Create and list comments on pages and discussions.

**Steps**:

### List Comments
1. Run config check (Workflow 0)
2. Get page/block ID
3. List comments:
   ```bash
   python 00-system/skills/notion-master/scripts/manage_comments.py list --page <page_id>
   ```
4. Display comments with authors and timestamps

### Create Comment
1. Run config check
2. Identify target page or discussion
3. Get comment text from user
4. Create comment:
   ```bash
   # New comment on page
   python 00-system/skills/notion-master/scripts/manage_comments.py create \
     --page <page_id> --text "Your comment here"

   # Reply to existing discussion
   python 00-system/skills/notion-master/scripts/manage_comments.py create \
     --discussion <discussion_id> --text "Your reply here"
   ```
5. Confirm comment created

---

## Workflow 10: Advanced Operations (Future)

**Status**: Planned for Phase 6

**Sub-workflows**:
- "upload file to [page]" → File upload flow (3-step process)
- "create data source" → Data source API (2025 feature)

---

## Context File Format

**Location**: `01-memory/integrations/notion-databases.yaml`

```yaml
---
last_synced: 2025-12-10T23:00:00
sync_count: 3
databases:
  - id: "abc123-def456"
    name: "Client Projects"
    parent: "Marketing"  # For disambiguation
    url: "https://notion.so/..."
    properties:
      - name: "Name"
        type: "title"
      - name: "Status"
        type: "select"
        options: ["Not Started", "In Progress", "Complete"]
      - name: "Priority"
        type: "select"
        options: ["Low", "Medium", "High"]
      - name: "Due Date"
        type: "date"
      - name: "Assignee"
        type: "people"
  - id: "ghi789-jkl012"
    name: "Content Calendar"
    parent: null
    url: "https://notion.so/..."
    properties:
      - name: "Title"
        type: "title"
      - name: "Publish Date"
        type: "date"
      - name: "Channel"
        type: "multi_select"
        options: ["Blog", "Twitter", "LinkedIn"]
---

# Notion Databases Context

Auto-generated by notion-connect skill.
Run "refresh notion" to update.
```

---

## Fuzzy Matching Logic

When user says a database name:

1. **Exact match**: "Client Projects" → finds "Client Projects"
2. **Case-insensitive**: "client projects" → finds "Client Projects"
3. **Partial match**: "Projects" → finds "Client Projects", "Personal Projects"
4. **Word match**: "calendar" → finds "Content Calendar", "Editorial Calendar"

**Disambiguation prompt** (if multiple matches):
```
Found 3 databases matching "Projects":
1. Client Projects (Marketing)
2. Personal Projects
3. Project Templates

Which one? (enter number or be more specific)
```

---

## Error Handling

| Error | Action |
|-------|--------|
| No databases found | Check Notion integration has database access |
| Database not in context | Run discovery: "refresh notion" |
| Permission denied | Verify integration connected to database |
| Rate limited | Wait and retry with exponential backoff |
| Invalid property | Show valid options from cached schema |

Load `notion-master/references/error-handling.md` for detailed troubleshooting.

---

## Examples

**First-time setup**:
```
User: "connect to notion"
AI: Running Notion discovery...
    Found 5 databases: Client Projects, Content Calendar, CRM, Tasks, Meeting Notes
    Saved to context. You can now query any database by name!
```

**Query by name**:
```
User: "query my Projects for active items"
AI: Querying "Client Projects"...
    Found 12 active items:
    1. Website Redesign (High priority, due Jan 15)
    2. Q1 Marketing Plan (Medium priority, due Jan 30)
    ...
```

**Create page**:
```
User: "add a new task to my Tasks database"
AI: Creating in "Tasks" database.
    Required properties:
    - Task Name: [your input]
    - Status: Not Started / In Progress / Complete
    - Due Date: [optional, format: YYYY-MM-DD]

    What's the task name?
```

---

*Notion Connect v1.1 - Meta-skill for complete Notion workspace integration*

---

**Changelog**:
- v1.1 (2025-12-11): Added first-time user setup section, improved exit code documentation
- v1.0 (2025-12-10): Initial release with 10 workflows
