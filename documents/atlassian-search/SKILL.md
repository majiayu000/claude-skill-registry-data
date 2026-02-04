---
name: atlassian-search
description: Search and retrieve information from Jira and Confluence using the atlassian-cli tool. Use this skill to find issues, search documentation, manage projects, and track sprints in Atlassian products.
---

# Atlassian Search Skill

This skill enables you to search and retrieve information from Jira and Confluence using the `atlassian-cli` command-line tool.

## Prerequisites

Before using this skill, ensure:
1. Environment variables are set:
   - `ATLASSIAN_URL`: Your Atlassian instance URL (e.g., `https://your-domain.atlassian.net`)
   - `ATLASSIAN_USERNAME`: Your email address
   - `ATLASSIAN_API_TOKEN`: Your API token
   - `ATLASSIAN_CLOUD`: Set to `true` for Cloud, `false` for Server/DC (default: true)
   - `CONFLUENCE_BASE_PATH`: Confluence API base path (default: `/wiki`)
2. The `atlassian-cli` binary is built and available in PATH

## Available Commands

### Jira Commands

#### 1. Get Issue Details

Get detailed information about a specific Jira issue:

```bash
atlassian-cli jira issue <issue-key>
```

**Examples:**
```bash
# Get issue details in readable text format (default)
atlassian-cli jira issue PROJECT-123

# Get raw JSON output
atlassian-cli jira issue PROJECT-123 --format=json
```

#### 2. Search Issues with JQL

Search for Jira issues using JQL (Jira Query Language):

```bash
atlassian-cli jira search "<jql>" [--max=20] [--format=text|json]
```

**Examples:**
```bash
# Find open issues in project
atlassian-cli jira search "project=DEV AND status=Open"

# Find issues assigned to current user
atlassian-cli jira search "assignee=currentUser() ORDER BY created DESC" --max=50

# Find recently created bugs
atlassian-cli jira search "issuetype=Bug AND created >= -7d"

# Get high priority issues
atlassian-cli jira search "priority=High AND status!=Done" --max=30
```

**Common JQL Operators:**
- `project=<KEY>`: Filter by project
- `status=<Status>`: Filter by status (Open, In Progress, Done, etc.)
- `assignee=<user>`: Filter by assignee (`currentUser()` for yourself)
- `issuetype=<Type>`: Filter by type (Bug, Task, Story, etc.)
- `created >= -Nd`: Issues created in last N days
- `updated >= -Nd`: Issues updated in last N days
- `priority=<Priority>`: Filter by priority (High, Medium, Low)
- `labels=<label>`: Filter by label
- `ORDER BY <field> DESC/ASC`: Sort results

#### 3. List All Projects

Get a list of all accessible Jira projects:

```bash
atlassian-cli jira projects [--format=text|json]
```

#### 4. Get Project Issues

Get issues from a specific project:

```bash
atlassian-cli jira project-issues <project-key> [--max=20] [--format=text|json]
```

**Example:**
```bash
atlassian-cli jira project-issues DEV --max=50
```

#### 5. List Agile Boards

Get a list of Scrum/Kanban boards:

```bash
atlassian-cli jira boards [--type=scrum|kanban] [--max=50] [--format=text|json]
```

**Examples:**
```bash
# List all boards
atlassian-cli jira boards

# List only Scrum boards
atlassian-cli jira boards --type=scrum
```

#### 6. List Sprints

Get sprints from a specific board:

```bash
atlassian-cli jira sprints <board-id> [--state=active|closed|future] [--format=text|json]
```

**Examples:**
```bash
# List all sprints
atlassian-cli jira sprints 123

# List only active sprints
atlassian-cli jira sprints 123 --state=active
```

#### 7. Get Sprint Issues

Get issues in a specific sprint:

```bash
atlassian-cli jira sprint-issues <sprint-id> [--max=50] [--format=text|json]
```

#### 8. Get Current User

Get information about the authenticated user:

```bash
atlassian-cli jira user [--format=text|json]
```

### Confluence Commands

#### 1. Get Page Details

Get content of a specific Confluence page by ID:

```bash
atlassian-cli confluence page <page-id> [--format=text|json]
```

**Example:**
```bash
# Get page with ID 123456
atlassian-cli confluence page 123456
```

#### 2. Search with CQL

Search Confluence using CQL (Confluence Query Language):

```bash
atlassian-cli confluence search "<cql>" [--limit=10] [--format=text|json] [--full-content]
```

**Examples:**
```bash
# Search pages in specific space
atlassian-cli confluence search "type=page AND space=DEV"

# Search with text query
atlassian-cli confluence search "siteSearch ~ \"important concept\""

# Search recent pages
atlassian-cli confluence search "created >= \"2024-01-01\" AND space=TEAM" --limit=20

# Search with full content
atlassian-cli confluence search "type=page AND space=DEV" --full-content
```

**Common CQL Operators:**
- `type=page`: Filter by content type
- `space=<KEY>`: Filter by space key
- `siteSearch ~ "<text>"`: Full-text search
- `text ~ "<text>"`: Title/content text search
- `title ~ "<text>"`: Title search
- `label=<label>`: Filter by label
- `created >= "<date>"`: Created after date (YYYY-MM-DD)
- `lastModified >= "<date>"`: Modified after date
- `creator=<user>`: Filter by creator
- `contributor=<user>`: Filter by contributor

#### 3. Simple Text Search

Easy-to-use text search (automatically converts to proper CQL):

```bash
atlassian-cli confluence text-search "<query>" [--limit=10] [--format=text|json] [--full-content]
```

**Examples:**
```bash
# Simple text search (shows preview by default)
atlassian-cli confluence text-search "情報セキュリティ" --limit=20

# Show full content
atlassian-cli confluence text-search "meeting notes" --full-content

# Get raw JSON
atlassian-cli confluence text-search "API documentation" --format=json
```

**Note:** Use `--full-content` to display complete page content (up to 2000 chars per page). Without this flag, only 200-character previews are shown.

#### 4. List Spaces

Get a list of all accessible Confluence spaces:

```bash
atlassian-cli confluence spaces [--limit=50] [--format=text|json]
```

#### 5. Get Space Details

Get information about a specific space:

```bash
atlassian-cli confluence space <space-key> [--format=text|json]
```

#### 6. Get Child Pages

Get child pages of a specific page:

```bash
atlassian-cli confluence children <page-id> [--limit=25] [--format=text|json] [--full-content]
```

#### 7. Get Page Comments

Get comments on a specific page:

```bash
atlassian-cli confluence comments <page-id> [--format=text|json]
```

#### 8. Get Page Labels

Get labels/tags on a specific page:

```bash
atlassian-cli confluence labels <page-id> [--format=text|json]
```

## Output Formats

### Text Format (Default)

Readable, formatted output with essential information:

**Jira Issue:**
```
Issue: PROJECT-123
Summary: Fix login bug
─────────────────────────────────────────

Status: In Progress
Type: Bug
Priority: High
Assignee: John Doe
Reporter: Jane Smith
Labels: backend, security
Created: 2024-11-15T10:30:00Z
Updated: 2024-11-20T14:45:00Z

Description:
─────────────────────────────────────────
Users are unable to login when...
```

**Confluence Search Results:**
```
Found 5 result(s):

[1] Information Security Rules

[2] Security Training Content
    ...
```

### JSON Format

Raw API response for programmatic processing:

```bash
atlassian-cli jira issue PROJECT-123 --format=json
```

Returns complete JSON with all fields from the API.

## Usage Guidelines

### When to Use This Skill

Use this skill when you need to:
- Find specific Jira issues or track their status
- Search for documentation in Confluence
- Review project progress and sprint planning
- Investigate problems mentioned in issues or pages
- Gather information for reports or summaries
- Track team activities and decisions

### Best Practices

1. **Use Specific Search Terms**: Precise keywords yield better results
2. **Leverage JQL/CQL**: Use query languages for advanced filtering
3. **Start with Text Format**: Use `--format=text` for readability, `--format=json` for processing
4. **Use --full-content Wisely**: Only use for detailed content review to avoid overwhelming output
5. **Combine Commands**: Search broadly first, then drill down into specific items
6. **Check Multiple Sources**: Search both Jira and Confluence for comprehensive information

### Common Use Cases

**Finding Related Issues:**
```bash
# Search for bugs related to authentication
atlassian-cli jira search "issuetype=Bug AND text ~ \"authentication\""
```

**Reviewing Sprint Progress:**
```bash
# List active sprints
atlassian-cli jira sprints 123 --state=active

# Get issues in sprint
atlassian-cli jira sprint-issues 456 --max=50
```

**Finding Documentation:**
```bash
# Search Confluence for API docs
atlassian-cli confluence text-search "API documentation" --limit=10

# Get full page content
atlassian-cli confluence page 789012
```

**Investigating Issues:**
```bash
# First, find the Jira issue
atlassian-cli jira search "text ~ \"database timeout\""

# Then, search related documentation
atlassian-cli confluence text-search "database configuration" --full-content
```

**Tracking Team Work:**
```bash
# See what's assigned to you
atlassian-cli jira search "assignee=currentUser() AND status!=Done"

# Check recent updates
atlassian-cli jira search "updated >= -3d AND project=MYPROJECT" --max=30
```

## Error Handling

### Common Errors and Solutions

1. **"ATLASSIAN_URL environment variable not set"**
   - Set the environment variable: `export ATLASSIAN_URL=https://your-domain.atlassian.net`

2. **"Authentication failed"**
   - Verify your API token is valid
   - Check that username (email) is correct
   - Ensure token has not expired

3. **"Permission denied"**
   - You don't have access to the requested resource
   - Check project/space permissions with admin
   - Ensure your account has appropriate licenses

4. **"Resource not found"**
   - Verify issue key, page ID, or space key is correct
   - Check spelling and format (e.g., "PROJECT-123" not "project123")
   - Ensure resource exists and hasn't been deleted

5. **"Connection error"**
   - Check network connectivity
   - Verify ATLASSIAN_URL is correct (include https://)
   - For Confluence, ensure CONFLUENCE_BASE_PATH is set correctly (default: `/wiki`)

## Limitations

- **Read-Only**: This tool provides read-only access; cannot create or modify issues/pages
- **Rate Limits**: Atlassian APIs have rate limits; avoid rapid consecutive requests
- **Permissions**: Only retrieves resources your account has access to
- **Content Length**: Text format truncates very long content (use `--format=json` for complete data)
- **Binary Formats**: Cannot retrieve file attachments, only metadata

## Tips for Effective Searching

### Jira

1. **Use Specific JQL**: `status=Open` is better than searching all statuses
2. **Order Results**: Add `ORDER BY created DESC` to see newest first
3. **Limit Scope**: Filter by project or sprint to reduce noise
4. **Use Labels**: Search by labels for categorized issues
5. **Date Ranges**: Use relative dates like `-7d` for recent items

### Confluence

1. **Know Your Space**: Search within specific spaces for faster results
2. **Use Text Search**: `text-search` is easier than writing CQL
3. **Request Full Content**: Use `--full-content` when you need complete information
4. **Check Page Hierarchy**: Use `children` command to explore page structure
5. **Combine Searches**: Search by keyword, then browse space or check labels

## Integration with Workflows

This skill works well in combination with other tasks:

- **Search Jira** → Analyze status → Summarize progress → Create report
- **Find Confluence docs** → Extract information → Answer questions → Document findings
- **Track sprint** → Identify blockers → Suggest actions → Update stakeholders
- **Search issues** → Investigate patterns → Propose solutions → Generate recommendations
- **Browse documentation** → Compile knowledge → Create summaries → Share insights

## API Token Setup

To use this skill, you need an Atlassian API token:

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a descriptive name (e.g., "Claude CLI")
4. Copy the token immediately (you won't see it again)
5. Set environment variable: `export ATLASSIAN_API_TOKEN=<your-token>`

**Security Note:** Keep your API token secure. Do not commit it to version control or share it publicly.
