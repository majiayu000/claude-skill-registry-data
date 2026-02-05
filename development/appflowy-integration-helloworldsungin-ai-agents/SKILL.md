---
name: appflowy-integration
description: >
  Integration with AppFlowy project management tool for task tracking, database management,
  and workspace organization. Use when working with AppFlowy, managing project tasks,
  creating databases, organizing workspaces, syncing agent work with project tracking,
  syncing documentation or tasks to AppFlowy, setting up automated sync workflows,
  or when the user mentions AppFlowy, project tracking, task management, or sync automation.
  Includes generic sync script that works with ANY project. Supports rich text formatting
  (bold, italic, code, links, strikethrough) and git pushsync workflow for automated syncing.
version: 2.4.0
author: AI Agents Team
category: custom
token_estimate: ~1500
---

# AppFlowy Integration Skill

<objective>
Integration with AppFlowy, an open-source collaborative workspace and project management tool. Provides capabilities for managing tasks, databases, workspaces, and project organization through AppFlowy's REST API.
</objective>

<context>
**When to use:**
- Creating or updating tasks in AppFlowy databases
- Managing project workspaces and folders
- Organizing work items in Kanban boards or database views
- Syncing agent work with project tracking
- Automating project management workflows
- Creating documentation in AppFlowy workspaces
- When user mentions AppFlowy, project tracking, or task management

**Prerequisites:**
- AppFlowy deployed (self-hosted or cloud)
- API endpoint URL configured
- Authentication credentials (JWT token)
- Workspace ID known for operations
- Python `requests` library installed

**Do NOT use when:**
- Working with other project management tools (Jira, Asana, Trello)
- Managing local files without AppFlowy integration
- Tasks don't require project management tracking
</context>

<quick_start>
**AI Agents Workspace Configuration:**
```bash
export APPFLOWY_API_URL="https://appflowy.ark-node.com"
export APPFLOWY_WORKSPACE_ID="c9674d81-6037-4dc3-9aa6-e2d833162b0f"
export APPFLOWY_DOCS_PARENT_ID="c7f9f933-ca10-4206-8be4-a2967f1085aa"
```

**Credentials Location:**
- Stored in: `/Users/sunginkim/GIT2/ArkNode-AI/projects/appflowy-deployment/.env`
- Workspace: AI Agents
- Documentation parent: c7f9f933-ca10-4206-8be4-a2967f1085aa

**Access:**
- Web UI: https://appflowy.ark-node.com
- WebSocket: wss://appflowy.ark-node.com/ws/v2/

**Git PushSync Workflow (Recommended):**
```bash
# Push to GitHub and auto-sync to AppFlowy
git add .
git commit -m "docs: update documentation"
git pushsync  # Push + sync to AppFlowy in one command
```

**Mapping File:**
Create `appflowy-mapping.yaml` to prevent duplicate pages:
```yaml
mappings:
  README.md: page-id-here
  docs/guide.md: another-page-id
```

**Generic Project Sync (Any Repository):**
```bash
# Sync with config file (uses mapping file if present)
python3 sync_project.py --config appflowy-sync.yaml

# Auto-discover and sync documentation
python3 sync_project.py --auto-discover --parent "Documentation"

# Sync specific folder
python3 sync_project.py --source docs/ --parent "API Docs"

# Preview before syncing (dry run)
python3 sync_project.py --config appflowy-sync.yaml --dry-run

# Force re-sync all files
python3 sync_project.py --config appflowy-sync.yaml --force
```

**AI_agents Specific Sync Scripts:**
```bash
# Sync AI_agents documentation to AppFlowy
cd skills/custom/appflowy-integration/scripts/
python3 sync_docs.py

# Sync AI_agents tasks to AppFlowy Kanban
python3 sync_tasks.py

# Preview before syncing (dry run)
python3 sync_docs.py --dry-run
python3 sync_tasks.py --dry-run

# Force re-sync all items
python3 sync_docs.py --force
python3 sync_tasks.py --force
```

**Environment Variables:**
```bash
export APPFLOWY_API_URL="https://appflowy.ark-node.com"
export APPFLOWY_API_TOKEN="your_jwt_token"
export APPFLOWY_WORKSPACE_ID="22bcbccd-9cf3-41ac-aa0b-28fe144ba71d"
export APPFLOWY_DOCS_PARENT_ID="parent_page_id"  # Optional: Parent page for docs
export APPFLOWY_DATABASE_ID="bb7a9c66-8088-4f71-a7b7-551f4c1adc5d"
```

**Python Client Quick Start:**
```python
from appflowy_client import AppFlowyClient

# Initialize client (uses environment variables)
client = AppFlowyClient()

# List workspaces
workspaces = client.list_workspaces()

# List databases in workspace
databases = client.list_databases(client.workspace_id)

# Get database fields
fields = client.get_database_fields(client.workspace_id, database_id)

# Create a task
task = client.create_row(
    workspace_id=client.workspace_id,
    database_id=database_id,
    data={
        'title': 'Implement user authentication',
        'status': 'In Progress',
        'priority': 'High',
        'assignee': 'AI Agent',
        'description': 'Add JWT-based authentication'
    }
)
```

For detailed workflows, see:
- `workflows/sync-documentation.md` - Sync AI_agents docs to AppFlowy
- `workflows/sync-tasks.md` - Sync AI_agents tasks to Kanban board
- `workflows/git-sync.md` - Automated sync with git hooks and cron
- `workflows/task-management.md` - Creating and updating tasks
- `workflows/workspace-operations.md` - Workspace and database setup
- `workflows/troubleshooting.md` - Common issues and solutions
- `references/api-reference.md` - Complete API documentation
</quick_start>

<success_criteria>
- AppFlowy client initialized successfully
- Can list workspaces and databases
- Can create and update tasks via API
- Authentication token valid and working
- Tasks visible in AppFlowy UI (if view exists - see limitations)
- No 401/403 authentication errors
- API responses return expected data structures
</success_criteria>

<api_endpoints>
**Correct API Endpoints for Page Management:**

AppFlowy uses a **block-based Delta format** for page content, NOT raw markdown. You must create pages first, then append content blocks.

**1. Create Page (Empty):**
```
POST /api/workspace/{workspace_id}/page-view
{
  "name": "Page Title",
  "layout": 0,                    // 0 = Document layout
  "parent_view_id": "parent_id"   // Optional: for nested pages
}
```
Response: `{"data": {"view_id": "...", "database_id": null}, "code": 0}`

**2. Append Content Blocks:**
```
POST /api/workspace/{workspace_id}/page-view/{page_id}/append-block
{
  "blocks": [
    {"type": "heading", "data": {"level": 1, "delta": [{"insert": "Title"}]}},
    {"type": "paragraph", "data": {"delta": [{"insert": "Text content"}]}},
    {"type": "bulleted_list", "data": {"delta": [{"insert": "List item"}]}},
    {"type": "numbered_list", "data": {"delta": [{"insert": "Numbered item"}]}},
    {"type": "code", "data": {"language": "python", "delta": [{"insert": "code"}]}},
    {"type": "quote", "data": {"delta": [{"insert": "Quote text"}]}}
  ]
}
```

**3. Update Page Metadata (Name/Icon only):**
```
PATCH /api/workspace/{workspace_id}/page-view/{page_id}
{
  "name": "Updated Title"
}
```
Note: PATCH does NOT update content. Use append-block endpoint for content.

**Delta Block Format:**
AppFlowy uses Delta format (compatible with Quill.js):
- Each block has a `type` (heading, paragraph, bulleted_list, numbered_list, code, quote)
- Each block has `data` containing `delta` array with `{"insert": "text"}` objects
- Headings have additional `level` field (1-6)
- Code blocks have additional `language` field

**Markdown to Blocks Converter:**
Use the `markdown_to_blocks()` function from `update_page_content.py`:
```python
from update_page_content import markdown_to_blocks

# Convert markdown to AppFlowy blocks
blocks = markdown_to_blocks(markdown_content)

# Append to page
append_blocks_to_page(api_url, workspace_id, page_id, blocks, token)
```

Supported markdown elements:
- Headings (# through ######)
- Bullet lists (-, *)
- Numbered lists (1., 2., etc.)
- Code blocks (``` with language detection)
- Blockquotes (>)
- Paragraphs (regular text)
- Rich text formatting: **bold**, *italic*, `code`, [links](url), ~~strikethrough~~
- Tables (rendered as code blocks)
</api_endpoints>

<workflow>
<overview>
AppFlowy integration follows a standard pattern: authenticate → verify workspace → list databases → perform operations. For page content, use a two-step process: (1) create page, (2) append blocks. The skill provides specialized workflows for different use cases.
</overview>

<router>
**Choose your workflow:**

1. **Documentation Sync** → `workflows/sync-documentation.md`
   - Sync AI_agents docs to AppFlowy
   - Incremental sync with hash tracking
   - Configuration options (dry-run, force)
   - Hierarchical folder structure
   - Troubleshooting sync issues

2. **Task Sync** → `workflows/sync-tasks.md`
   - Sync AI_agents tasks to Kanban board
   - Multiple data source extraction
   - Status and priority mapping
   - Kanban column organization
   - Task deduplication logic

3. **Git Sync Automation** → `workflows/git-sync.md`
   - Git post-commit hooks
   - Cron job scheduling
   - CI/CD integration (GitHub Actions, GitLab)
   - Incremental sync strategies
   - Conflict handling (one-way sync)

4. **Task Management** → `workflows/task-management.md`
   - Create tasks
   - Update task status
   - Query and filter tasks
   - Bulk operations
   - Agent task tracking pattern
   - Daily standup summary

5. **Workspace Operations** → `workflows/workspace-operations.md`
   - Workspace setup
   - Database creation and management
   - Folder structure organization
   - View management
   - Project workspace initialization

6. **Server Management** → `workflows/server-deployment.md`
   - Start/stop AppFlowy backend
   - Monitor server health
   - Backup and restore
   - Container management
   - Auto-start configuration

7. **Troubleshooting** → `workflows/troubleshooting.md`
   - Environment variables not updating
   - WebSocket connection issues
   - View-database association problems
   - API authentication failures
   - Container restart behavior

8. **API Reference** → `references/api-reference.md`
   - Authentication endpoints
   - Workspace API
   - Database API
   - Row operations
   - Field operations
   - Error handling patterns
</router>

<authentication>
**Method 1: JWT Token (Recommended for automation)**
```bash
# Obtain JWT token via API
curl -X POST "https://appflowy.ark-node.com/gotrue/token" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-email@example.com",
    "password": "your-password",
    "grant_type": "password"
  }'
```

**Method 2: Environment Variables**
```bash
export APPFLOWY_API_URL="https://appflowy.ark-node.com"
export APPFLOWY_API_TOKEN="your_jwt_token_here"
export APPFLOWY_WORKSPACE_ID="your_workspace_id"
```

**Python Client Configuration:**
```python
import os
import requests

class AppFlowyClient:
    def __init__(self):
        self.api_url = os.getenv('APPFLOWY_API_URL')
        self.token = os.getenv('APPFLOWY_API_TOKEN')
        self.workspace_id = os.getenv('APPFLOWY_WORKSPACE_ID')
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

    def _make_request(self, method, endpoint, **kwargs):
        """Make authenticated API request."""
        url = f"{self.api_url}{endpoint}"
        response = requests.request(method, url, headers=self.headers, **kwargs)
        response.raise_for_status()
        return response.json()
```

See `references/api-reference.md` for complete authentication documentation.
</authentication>

<error_handling>
**Robust Error Handling Pattern:**
```python
import logging
from requests.exceptions import RequestException, HTTPError

logger = logging.getLogger(__name__)

def safe_api_call(func):
    """Decorator for safe API calls with error handling."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPError as e:
            if e.response.status_code == 401:
                logger.error("Authentication failed - check API token")
                raise Exception("AppFlowy authentication failed")
            elif e.response.status_code == 403:
                logger.error("Permission denied - check workspace access")
                raise Exception("Permission denied for AppFlowy resource")
            elif e.response.status_code == 404:
                logger.error(f"Resource not found: {e.request.url}")
                raise Exception("AppFlowy resource not found")
            else:
                logger.error(f"API error: {e}")
                raise
        except RequestException as e:
            logger.error(f"Network error connecting to AppFlowy: {e}")
            raise Exception("Failed to connect to AppFlowy instance")
    return wrapper

# Apply to API methods
@safe_api_call
def create_row_safe(client, workspace_id, database_id, data):
    return create_row(client, workspace_id, database_id, data)
```

**Rate Limiting:**
```python
import time
from functools import wraps

def rate_limit(calls_per_minute=60):
    """Rate limit API calls to avoid overwhelming server."""
    min_interval = 60.0 / calls_per_minute
    last_called = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator
```

See `workflows/troubleshooting.md` for specific error scenarios and solutions.
</error_handling>
</workflow>

<best_practices>
<practice name="secure_credentials">
**Never hardcode credentials.** Use environment variables or secure credential storage.

```python
from dotenv import load_dotenv
load_dotenv()

# Credentials loaded from .env file
api_token = os.getenv('APPFLOWY_API_TOKEN')
```
</practice>

<practice name="cache_ids">
**Cache workspace and database IDs** to avoid repeated lookups.

```python
class AppFlowyManager:
    def __init__(self):
        self.client = AppFlowyClient()
        self._workspace_cache = None
        self._database_cache = {}

    def get_workspace_id(self):
        if not self._workspace_cache:
            workspaces = list_workspaces(self.client)
            self._workspace_cache = workspaces[0]['id']
        return self._workspace_cache

    def get_database_id(self, database_name):
        if database_name not in self._database_cache:
            databases = list_databases(self.client, self.get_workspace_id())
            db = next((d for d in databases if d['name'] == database_name), None)
            if db:
                self._database_cache[database_name] = db['id']
        return self._database_cache.get(database_name)
```
</practice>

<practice name="validate_fields">
**Validate field compatibility** before inserting data.

```python
def validate_task_data(client, workspace_id, database_id, task_data):
    """Ensure task data matches database schema."""
    fields = get_database_fields(client, workspace_id, database_id)
    field_names = {f['name'] for f in fields}

    # Remove fields that don't exist in database
    validated = {k: v for k, v in task_data.items() if k in field_names}

    # Warn about missing fields
    missing = set(task_data.keys()) - field_names
    if missing:
        logger.warning(f"Fields not in database: {missing}")

    return validated
```
</practice>

<practice name="degree_of_freedom">
**Medium Freedom:** Follow authentication and API endpoint patterns exactly. Implement error handling and rate limiting. Customize workflow functions based on your project needs.
</practice>
</best_practices>

<security_checklist>
- Never hardcode credentials - use environment variables
- Store API tokens securely (not in git)
- Validate all user input before API calls
- Use HTTPS for production deployments
- Rotate JWT tokens regularly
- Never log API tokens or passwords
- Verify workspace/database IDs before operations
- Implement rate limiting to prevent API abuse
- Use proper error handling to avoid credential leaks
- Set up firewall rules for self-hosted instances
</security_checklist>

<limitations>
<limitation name="view_database_association">
**Tasks Created via API May Not Be Visible Immediately**

**Issue:** Tasks created via REST API may not appear in the AppFlowy UI right away.

**Cause:** AppFlowy requires view objects (Grid, Board, Calendar) to exist as separate collab records in PostgreSQL. The REST API cannot create these view-database associations - only the UI can.

**Symptoms:**
- Task created successfully via API (returns row ID)
- Task exists in database (verified in PostgreSQL)
- Task does NOT appear in UI
- Browser console shows: `[useViewOperations] databaseId not found for view`

**Solution:**
1. Create a database view in AppFlowy UI first (click "+" → "Grid" or "Board")
2. Then use the API to create tasks - they will appear in the view
3. Alternative: Create tasks via browser console (uses WebSocket like UI)

**Browser Console Workaround:**
```javascript
// This uses your existing session (no auth needed)
const WORKSPACE_ID = '22bcbccd-9cf3-41ac-aa0b-28fe144ba71d';
const DATABASE_ID = 'bb7a9c66-8088-4f71-a7b7-551f4c1adc5d';

fetch(`/api/workspace/${WORKSPACE_ID}/database/${DATABASE_ID}/row`, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    cells: {
      phVRgL: 'Task Title',     // Description field
      YAgo8T: 'Task details',   // Text field
      SqwRg1: 'CEZD'            // Status: To Do
    }
  })
})
.then(r => r.json())
.then(d => console.log('Created:', d.data));
```

**Reference:** See `workflows/troubleshooting.md` for detailed diagnosis and solutions.
</limitation>

<limitation name="api_versioning">
**API Documentation is Evolving**
- API endpoints may change between versions
- Self-hosted instances may have different API versions
- Some features may require specific AppFlowy versions
- Always check AppFlowy documentation for latest API changes
</limitation>

<limitation name="rate_limiting">
**Rate Limiting**
- Rate limiting depends on deployment configuration
- Self-hosted instances may have different limits than cloud
- Implement client-side rate limiting for safety
</limitation>
</limitations>

<anti_patterns>
<pitfall name="expired_tokens">
❌ **Don't:** Continue using expired JWT tokens, causing 401 errors

✅ **Do:** Implement token refresh logic or re-authenticate automatically
```python
if response.status_code == 401:
    token = refresh_jwt_token()
    retry_request()
```
</pitfall>

<pitfall name="workspace_id_confusion">
❌ **Don't:** Hardcode workspace IDs or use wrong IDs

✅ **Do:** List and verify resources first, use descriptive variable names
```python
workspaces = client.list_workspaces()
arknode_workspace = next(w for w in workspaces if w['name'] == 'ArkNode Infrastructure')
workspace_id = arknode_workspace['id']
```
</pitfall>

<pitfall name="missing_view_objects">
❌ **Don't:** Expect API-created tasks to appear in UI without views

✅ **Do:** Create views in UI first, then use API for task operations

See `workflows/troubleshooting.md` for view-database association issue.
</pitfall>

<pitfall name="restart_vs_recreate">
❌ **Don't:** Use `docker compose restart` to reload .env changes

✅ **Do:** Use `docker compose down && docker compose up -d` to recreate containers
```bash
# WRONG - doesn't reload .env
docker compose restart

# RIGHT - recreates containers with new .env
docker compose down
docker compose up -d
```
</pitfall>

<pitfall name="network_issues">
❌ **Don't:** Assume AppFlowy is accessible without testing

✅ **Do:** Test connectivity before running operations
```bash
# Test connectivity
curl -v https://appflowy.ark-node.com/api/workspace

# Test DNS resolution
nslookup appflowy.ark-node.com
```
</pitfall>
</anti_patterns>

<examples>
<example name="agent_task_tracking">
**Context:** Agent needs to track its work in AppFlowy for team visibility.

```python
#!/usr/bin/env python3
from appflowy_client import AppFlowyClient

def track_agent_task(task_description, status="In Progress"):
    """Create or update task for agent work."""
    client = AppFlowyClient()

    task_info = {
        'title': task_description,
        'status': status,
        'assignee': 'AI Agent',
        'priority': 'Medium',
        'tags': ['automated', 'agent-work']
    }

    result = client.create_row(
        workspace_id=client.workspace_id,
        database_id=os.getenv('APPFLOWY_TODOS_DB_ID'),
        data=task_info
    )
    print(f"✅ Task tracked: {result['id']}")
    return result['id']

# Usage
task_id = track_agent_task("Implementing AppFlowy integration skill")
```

See `workflows/task-management.md` for complete patterns.
</example>

<example name="daily_standup">
**Context:** Generate daily standup summary from AppFlowy tasks.

```python
def generate_standup_summary(client, database_id):
    """Generate daily standup summary from AppFlowy tasks."""
    from datetime import datetime, timedelta

    # Get tasks updated in last 24 hours
    yesterday = (datetime.utcnow() - timedelta(days=1)).isoformat() + 'Z'
    updated_rows = client.get_updated_rows(client.workspace_id, database_id, yesterday)

    # ... organize by status and format output ...

    return formatted_summary

# Usage
standup = generate_standup_summary(client, database_id)
print(standup)
```

See `workflows/task-management.md` for complete implementation.
</example>

<example name="project_dashboard">
**Context:** Generate project status dashboard from AppFlowy data.

```python
def generate_project_dashboard(client, database_id):
    """Create comprehensive project status dashboard."""
    # Get all tasks
    rows = client.get_database_rows(client.workspace_id, database_id)

    # Analyze status, priority, assignee workload
    # ... (see workflows/task-management.md for full code) ...

    return dashboard_output
```

See `workflows/task-management.md` for complete implementation.
</example>

<example name="generic_project_sync">
**Context:** Sync any project's documentation to AppFlowy using the generic sync script.

**Scenario 1: Using a configuration file**
```yaml
# appflowy-sync.yaml
parent_page: "My Project Docs"
structure:
  - folder: "Getting Started"
    documents:
      - source: "README.md"
        name: "Overview"
      - source: "docs/quickstart.md"
        name: "Quick Start"

  - folder: "API Reference"
    documents:
      - source: "docs/api/**/*.md"  # Glob pattern

  - folder: "Examples"
    documents:
      - source: "examples/*/README.md"
        name_from_path: true  # Use parent folder name
```

```bash
# Sync with config
python sync_project.py --config appflowy-sync.yaml

# Dry run first to preview
python sync_project.py --config appflowy-sync.yaml --dry-run

# Force re-sync all files
python sync_project.py --config appflowy-sync.yaml --force
```

**Scenario 2: Auto-discovery mode (no config needed)**
```bash
# Automatically discover and sync all documentation
python sync_project.py --auto-discover --parent "Documentation"

# Auto-discover with dry run
python sync_project.py --auto-discover --parent "Docs" --dry-run
```

**Scenario 3: Sync specific folder**
```bash
# Sync only the docs/ folder
python sync_project.py --source docs/ --parent "API Docs"

# Sync with custom project root
python sync_project.py --source docs/ --parent "Docs" --project-root /path/to/project
```

**Scenario 4: Use with custom .env file**
```bash
# For projects outside the default credential location
python sync_project.py \
  --config appflowy-sync.yaml \
  --env-file /path/to/project/.env
```

**Integration with CI/CD:**
```yaml
# .github/workflows/sync-docs.yml
name: Sync Documentation to AppFlowy
on:
  push:
    branches: [main]
    paths: ['docs/**', 'README.md']

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: pip install requests pyyaml

      - name: Sync to AppFlowy
        env:
          APPFLOWY_API_URL: ${{ secrets.APPFLOWY_API_URL }}
          APPFLOWY_API_TOKEN: ${{ secrets.APPFLOWY_API_TOKEN }}
          APPFLOWY_WORKSPACE_ID: ${{ secrets.APPFLOWY_WORKSPACE_ID }}
        run: |
          python sync_project.py --config appflowy-sync.yaml
```

**Benefits:**
- ✅ Works with ANY project, not just AI_agents
- ✅ No code changes needed - pure configuration
- ✅ Incremental sync saves time and API calls
- ✅ Supports complex folder hierarchies
- ✅ Glob patterns for flexible file matching
- ✅ Can be integrated into git hooks, cron, or CI/CD
</example>
</examples>

<related_skills>
This skill works well with:

- **api-endpoint-creator**: When building custom integrations with AppFlowy
- **database-migration**: When setting up AppFlowy database schemas
- **incident-response**: Track incidents in AppFlowy
- **deployment-workflow**: Track deployment tasks in AppFlowy
- **documentation-writer**: Generate documentation for AppFlowy workflows
</related_skills>

<integration_notes>
**Working with Other Tools:**

**Zapier Integration:** AppFlowy supports Zapier, enabling no-code automation between AppFlowy and 5,000+ apps.

**GitHub Integration:** Combine with GitHub Actions to auto-create AppFlowy tasks from issues or PRs.

**Skill Composition:**
1. Use this skill for project tracking
2. Use code-related skills for implementation
3. Update AppFlowy status as work progresses
</integration_notes>

<reference_guides>
**Documentation:**
- `workflows/sync-documentation.md` - Sync AI_agents docs to AppFlowy
- `workflows/sync-tasks.md` - Sync AI_agents tasks to Kanban board
- `workflows/git-sync.md` - Automated sync with git hooks and cron
- `workflows/task-management.md` - Creating, updating, and tracking tasks
- `workflows/workspace-operations.md` - Workspace and database management
- `workflows/server-deployment.md` - Server setup and operations
- `workflows/troubleshooting.md` - Common issues and solutions
- `references/api-reference.md` - Complete API endpoint documentation
- `references/setup_guide.md` - Deployment and configuration guide

**Sync Scripts:**
- `scripts/sync_project.py` - **Generic sync for any project** (config-driven, YAML/JSON config)
- `scripts/sync_docs.py` - AI_agents documentation sync (hardcoded mappings)
- `scripts/sync_tasks.py` - AI_agents task sync from multiple data sources
- `appflowy-sync.example.yaml` - Example configuration for generic sync
- Support for dry-run, force sync, and custom .env files
- Hash-based change detection for efficient syncing
- One-way sync: Repository → AppFlowy (source of truth)

**Generic Sync Features:**
The `sync_project.py` script is designed to work with ANY project:
- **Configuration-driven**: Define document structure in YAML/JSON
- **Auto-discovery mode**: Automatically find and sync documentation files
- **Glob pattern support**: Use wildcards to match multiple files (e.g., `docs/**/*.md`)
- **Hierarchical structure**: Create nested folder organization
- **Incremental sync**: Track changes via MD5 hashing, only sync what changed
- **Flexible naming**: Auto-generate page names or specify custom names
- **Multiple input modes**: Config file, auto-discover, or specific folder sync
- **Dry-run support**: Preview changes before syncing
- **Force mode**: Re-sync everything, ignoring cache

**Other Scripts:**
- `scripts/appflowy_client.py` - Python client library
- `scripts/task_tracker.py` - Task tracking utilities
- `scripts/workspace_setup.py` - Workspace initialization
- `scripts/manage_server.sh` - Server management script

**External Resources:**
- [AppFlowy GitHub Repository](https://github.com/AppFlowy-IO/AppFlowy)
- [AppFlowy Cloud Documentation](https://github.com/AppFlowy-IO/AppFlowy-Cloud)
- [AppFlowy API Documentation](https://github.com/AppFlowy-IO/documentations/blob/main/documentation/appflowy-cloud/openapi/README.md)
- [AppFlowy Zapier Integration](https://appflowy.com/blog/appflowy-is-now-on-zapier)
</reference_guides>

<version_history>
**Version 2.4.0 (2025-12-08)**
- **NEW: Rich text formatting support** (bold, italic, code, links, strikethrough)
- **NEW: git pushsync workflow** - Push to GitHub + auto-sync to AppFlowy
- **NEW: Mapping file support** (`appflowy-mapping.yaml`) for explicit page IDs
- **NEW: Rename-and-recreate strategy** for content updates (AppFlowy API limitation)
- Updated to AI Agents workspace (c9674d81-6037-4dc3-9aa6-e2d833162b0f)
- Fixed duplicate page creation issues with mapping files
- Enhanced markdown parser with inline formatting attributes
- 15 documentation pages synced successfully
- 10 tasks synced to Kanban board

**Version 2.3.0 (2025-12-08)**
- **NEW: Generic sync script for any project** (`sync_project.py`)
- Added YAML/JSON configuration support for flexible document mapping
- Auto-discovery mode to find documentation automatically
- Glob pattern support for matching multiple files (`docs/**/*.md`)
- Hierarchical folder structure with nested organization
- Multiple input modes: config file, auto-discover, or specific folder
- Created `appflowy-sync.example.yaml` with comprehensive examples
- Added generic sync usage examples and CI/CD integration patterns
- Updated documentation with generic sync features and benefits
- Script is now portable and can work with any repository

**Version 2.2.0 (2025-12-08)**
- Documented correct API endpoints (append-block for content)
- Added Delta block format documentation
- Added markdown_to_blocks converter documentation
- Updated sync_docs.py to use block-based content sync
- Documented APPFLOWY_DOCS_PARENT_ID environment variable
- Clarified two-step process: create page then append blocks
- Added supported markdown elements list
- Fixed content update workflow (PATCH only updates metadata)

**Version 2.1.0 (2025-12-08)**
- Added automated sync capabilities
- Created sync_docs.py for documentation syncing
- Created sync_tasks.py for task syncing
- Added workflows/sync-documentation.md
- Added workflows/sync-tasks.md
- Added workflows/git-sync.md
- Updated HTTPS URL to https://appflowy.ark-node.com
- Documented git hooks, cron jobs, and CI/CD integration
- Hash-based incremental sync with change detection
- One-way sync from repository to AppFlowy

**Version 2.0.0 (2025-12-04)**
- Migrated to pure XML structure
- Implemented progressive disclosure
- Split content into workflow files
- Added security checklist
- Improved YAML description with broader triggers
- Reduced main skill file from 1,256 to ~450 lines

**Version 1.0.0 (2025-11-22)**
- Initial creation
- Core API integration patterns
- Self-hosted deployment guides
- Task tracking workflows
- Project dashboard examples
</version_history>
