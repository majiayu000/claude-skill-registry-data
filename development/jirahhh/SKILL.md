---
name: jirahhh
description: Interact with Jira
---

# Jira CLI Guide - jirahhh

Complete reference for using the `jirahhh` CLI tool to create, update, view, and search Jira issues with proper formatting and custom field support.

**Repository**: https://github.com/shanemcd/jirahhh

## Quick Start

The easiest way to use `jirahhh` is with `uvx` - no installation or repository cloning required:

```bash
# View an issue
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh view AAP-12345 --env prod

# Create an issue
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh create \
  --env prod \
  --project AAP \
  --type Task \
  --summary "My Task Title" \
  --description "Task description here" \
  --acceptance-criteria "- Criteria 1"

# Search for issues
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh search \
  "project = AAP AND status = Open" \
  --env prod \
  --max-results 10
```

**Tip**: Add an alias to your shell for convenience:
```bash
alias jirahhh='uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh'

# Then use it simply:
jirahhh view AAP-12345 --env prod
```

## Available Commands

The `jirahhh` CLI has six subcommands:

- **`create`** - Create new Jira issues with markdown support
- **`update`** - Update existing issues
- **`view`** - View issue details with all fields
- **`search`** - Search issues using JQL queries
- **`fields`** - List available fields for a project/issue type
- **`api`** - Make generic API calls to Jira REST API

## Common Operations

### View an Issue

```bash
# View with all details
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh view ANSTRAT-1567 --env prod

# View specific fields
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh view AAP-12345 \
  --env stage \
  --fields "summary,status,description,assignee"
```

### Create an Issue

**With inline description:**
```bash
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh create \
  --env prod \
  --project AAP \
  --type Task \
  --summary "My Task Title" \
  --description "Task description" \
  --acceptance-criteria "- Must do X\n- Must do Y"
```

**With markdown file (recommended for complex issues):**
```bash
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh create \
  --env prod \
  --project AAP \
  --type Epic \
  --summary "My Epic Title" \
  --epic-name "My Epic Name" \
  --parent ANSTRAT-1234 \
  --description "path/to/description.md" \
  --acceptance-criteria "path/to/acceptance-criteria.md"
```

The `--description` parameter automatically detects `.md` files and converts markdown to Jira wiki markup using pypandoc.

**Create Initiative with child Epic:**
```bash
# 1. Create Initiative
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh create \
  --env prod \
  --project ANSTRAT \
  --type Initiative \
  --summary "My Initiative" \
  --description "description.md" \
  --acceptance-criteria "- Acceptance criteria"

# 2. Create child Epic (use ANSTRAT-XXXX from step 1 as parent)
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh create \
  --env prod \
  --project AAP \
  --type Epic \
  --summary "My Epic" \
  --epic-name "My Epic" \
  --parent ANSTRAT-1586 \
  --description "description.md" \
  --acceptance-criteria "- Acceptance criteria"
```

### Update an Issue

```bash
# Update summary
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh update AAP-12345 \
  --env prod \
  --summary "New Title"

# Update description from markdown file
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh update AAP-12345 \
  --env stage \
  --description "path/to/updated.md"

# Update multiple fields
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh update AAP-12345 \
  --env prod \
  --summary "Updated Title" \
  --description "updated.md" \
  --acceptance-criteria "- New criteria"
```

### Search for Issues

```bash
# Basic JQL search
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh search \
  "project = AAP AND status = Open" \
  --env prod \
  --max-results 10

# Search with custom fields
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh search \
  "assignee = currentUser() ORDER BY created DESC" \
  --env stage \
  --fields "summary,status,priority,assignee" \
  --max-results 10

# Find issues in an Epic
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh search \
  "'Epic Link' = AAP-12345" \
  --env prod \
  --max-results 100

# Find child issues of a parent (IMPORTANT: use "Parent Link" not "parent")
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh search \
  '"Parent Link" = ANSTRAT-1567' \
  --env prod

# Find child issues across all projects (AAP epics under ANSTRAT features)
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh search \
  '"Parent Link" = ANSTRAT-1567 ORDER BY created ASC' \
  --env prod \
  --max-results 50
```

### Discover Available Fields

```bash
# List all fields
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh fields --env prod

# List fields for specific project and issue type (shows required fields)
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh fields \
  --project AAP \
  --type Epic \
  --env stage
```

This shows which fields are required and available for creating that issue type.

### Make Generic API Calls

```bash
# Get issue comments
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh api GET \
  /rest/api/2/issue/AAP-12345/comment \
  --env prod

# Add a comment
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh api POST \
  /rest/api/2/issue/AAP-12345/comment \
  --env stage \
  --data '{"body": "This is a comment"}'

# Mention a user in a comment (use full email address)
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh api POST \
  /rest/api/2/issue/AAP-12345/comment \
  --env prod \
  --data '{"body": "Thanks [~user@redhat.com] for the feedback!"}'

# Get available transitions
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh api GET \
  /rest/api/2/issue/AAP-12345/transitions \
  --env prod

# Transition an issue
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh api POST \
  /rest/api/2/issue/AAP-12345/transitions \
  --env stage \
  --data '{"transition": {"id": "5"}}'
```

## Configuration

### Step 1: Generate Jira API Token

**For Red Hat Jira (issues.redhat.com):**

1. Go to https://issues.redhat.com
2. Click your profile icon (top right) → **Profile**
3. Click **Personal Access Tokens** in the left sidebar
4. Click **Create token**
5. Give it a name (e.g., "jirahhh CLI")
6. Set expiration (recommend 1 year or non-expiring for personal use)
7. Click **Create**
8. **Copy the token immediately** - you won't be able to see it again!

**For Stage Jira (issues.stage.redhat.com):**
- Follow the same steps but at https://issues.stage.redhat.com
- You'll need a separate token for stage

### Step 2: Create Config File (Recommended)

Create `~/.config/jirahhh/config.yaml`:

```yaml
# Jira Configuration File

stage:
  url: "https://issues.stage.redhat.com"
  token: "your-stage-token-here"
  proxy: "http://squid.corp.redhat.com:3128"

prod:
  url: "https://issues.redhat.com"
  token: "your-prod-token-here"

# Custom field IDs for ANSTRAT/AAP projects (optional - already in code)
custom_fields:
  acceptance_criteria: "customfield_12315940"
  epic_name: "customfield_12311141"
  parent_link: "customfield_12313140"
  epic_link: "customfield_12311140"

# Security level IDs (optional - already in code)
security_levels:
  default: "11795"  # Red Hat Employee
```

**Create the config directory and file:**
```bash
mkdir -p ~/.config/jirahhh
nano ~/.config/jirahhh/config.yaml  # or use your preferred editor
```

Then use `--env` flag to switch between environments:
```bash
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh view AAP-12345 --env stage
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh view AAP-12345 --env prod
```

### Alternative: Environment Variable

If you prefer not to store tokens in a config file:

```bash
export JIRA_API_TOKEN="your-token"
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh view AAP-12345 --env prod
```

The environment variable overrides the config file if both are present.

### Important Notes

- **Stage requires proxy**: The Red Hat proxy (`squid.corp.redhat.com:3128`) is required for stage Jira access
- **Prod does NOT use proxy**: Production Jira is directly accessible
- **Token security**: Keep your tokens secure - don't commit them to git
- **Token expiration**: Set reminders to regenerate tokens before they expire

## Important Project Rules

### Project Selection
- **ANSTRAT** project for: Initiative, Outcome, Feature
- **AAP** project for: Epic, Story, Task, Bug, Sub-task

ANSTRAT is for strategic planning and high-level features. AAP is for implementation work (Epics and below).

### Required Fields

**Acceptance Criteria** - Required for ALL issue types in ANSTRAT/AAP projects:
- Field ID: `customfield_12315940`
- Always include `--acceptance-criteria` parameter when creating issues

**Epic Name** - Required when creating Epic issue type:
- Field ID: `customfield_12311141`
- Include `--epic-name` parameter when `--type Epic`

### Security Level

All issues are automatically created with **"Red Hat Employee" security level** (ID: 11795), which restricts access to Red Hat employees and contractors only. This is set automatically and cannot be disabled.

## Custom Fields Reference

Common custom field IDs used in ANSTRAT/AAP projects:

| Field | Field ID | Usage |
|-------|----------|-------|
| Acceptance Criteria | `customfield_12315940` | Required for all issue types |
| Epic Name | `customfield_12311141` | Required when creating Epics |
| Parent Link | `customfield_12313140` | Links child to parent issue |
| Epic Link | `customfield_12311140` | Links issue to an Epic |

### Important: Finding Child Issues

**CRITICAL**: To find child issues of a parent, you MUST use `"Parent Link"` (the custom field name), NOT `parent` (the JQL keyword).

**❌ WRONG - This will NOT work:**
```bash
jirahhh search "parent = ANSTRAT-1567" --env prod
# Returns 0 results even if children exist!
```

**✅ CORRECT - Use "Parent Link" field name:**
```bash
jirahhh search '"Parent Link" = ANSTRAT-1567' --env prod
# Returns all child issues across all projects (AAP epics under ANSTRAT feature, etc.)
```

**Why this matters:**
- `parent =` is a JQL keyword that only works for subtasks (not Epics/Stories/Tasks)
- `"Parent Link"` is the custom field name (customfield_12313140) that works for all parent-child relationships
- Child issues can exist in different projects (e.g., AAP epics under ANSTRAT features)
- Using `"Parent Link"` searches across ALL projects for children

**Common use case:**
```bash
# Find all child epics under ANSTRAT-1567 feature
jirahhh search '"Parent Link" = ANSTRAT-1567 ORDER BY created ASC' \
  --env prod \
  --max-results 50 \
  --fields "summary,status,issuetype,assignee"
```

This will return child issues from ANY project (ANSTRAT, AAP, etc.) that have ANSTRAT-1567 as their parent.

## Command Reference

### `jirahhh create`

**Required:**
- `--project` - Project key (ANSTRAT, AAP)
- `--summary` - Issue title
- `--type` - Issue type (Initiative, Epic, Story, Task, Spike, Bug)

**Description (one required):**
- `--description` - Inline text or path to file (.md auto-converted, .txt used as-is)
- `--description-file` - Path to Jira wiki markup file (use `-` for stdin)

**Optional:**
- `--acceptance-criteria` - Acceptance criteria (required in ANSTRAT/AAP)
- `--epic-name` - Epic name (required when creating Epic)
- `--parent` - Parent issue key (e.g., ANSTRAT-1587)
- `--epic-link` - Epic to link to (e.g., AAP-12345)
- `--env` - Environment: `stage` or `prod` (default: stage)

### `jirahhh update`

**Required:**
- `issue_key` - Issue key to update (positional, e.g., AAP-12345)

**Optional (at least one should be provided):**
- `--summary` - New title
- `--description` - Inline text or path to file (.md auto-converted)
- `--description-file` - Path to Jira wiki markup file (use `-` for stdin)
- `--acceptance-criteria` - New acceptance criteria
- `--env` - Environment: `stage` or `prod` (default: stage)

### `jirahhh view`

**Required:**
- `issue_key` - Issue key to view (positional, e.g., AAP-12345)

**Optional:**
- `--fields` - Comma-separated list of fields (default: all common fields)
- `--env` - Environment: `stage` or `prod` (default: stage)

### `jirahhh search`

**Required:**
- `jql` - JQL query string (positional, e.g., `"project = AAP AND status = Open"`)

**Optional:**
- `--fields` - Comma-separated fields (default: summary,status,issuetype,assignee)
- `--max-results` - Maximum results to return (default: 50)
- `--env` - Environment: `stage` or `prod` (default: stage)

### `jirahhh fields`

**Optional:**
- `--project` - Project key to filter (e.g., AAP)
- `--type` - Issue type to filter (e.g., Epic)
- `--env` - Environment: `stage` or `prod` (default: stage)

When `--project` and `--type` are specified, shows which fields are required for creating that issue type.

### `jirahhh api`

**Required:**
- `method` - HTTP method: GET, POST, PUT, DELETE
- `endpoint` - API endpoint path (e.g., `/rest/api/2/issue/AAP-12345/comment`)

**Optional:**
- `--data` - JSON data for POST/PUT requests
- `--env` - Environment: `stage` or `prod` (default: stage)

## Markdown Conversion

The CLI automatically converts markdown files to Jira wiki markup when you use `.md` file extensions.

**Supported conversions:**
- Headers: `####` → `h4.`
- Bold: `**text**` → `*text*`
- Bullets: `-` → `*`
- Links: `[text](url)` → `[text|url]`
- Anchors: `<span id="anchor"></span>` → `{anchor:anchor}`

**Round-trip workflow:**

1. Pull from Jira:
```bash
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh view ANSTRAT-1587 --env prod
# Manually convert output to markdown using pandoc if needed
```

2. Edit markdown locally in your preferred editor

3. Push back to Jira:
```bash
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh update ANSTRAT-1587 \
  --env stage \
  --description "path/to/updated.md"
```

## Draft Workflow

Organize markdown files before creating issues:

```
Drafts/
└── Initiative - Title/
    ├── description.md
    ├── acceptance-criteria.md
    └── Epic - Title/
        ├── description.md
        ├── acceptance-criteria.md
        └── Story - Title/
            ├── description.md
            └── acceptance-criteria.md
```

Then create issues from the markdown files:
```bash
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh create \
  --env stage \
  --project AAP \
  --type Epic \
  --summary "Epic Title" \
  --epic-name "Epic Title" \
  --parent ANSTRAT-1234 \
  --description "Drafts/Initiative - Title/Epic - Title/description.md" \
  --acceptance-criteria "Drafts/Initiative - Title/Epic - Title/acceptance-criteria.md"
```

## Environment Switching

The `--env` flag automatically configures everything:

**Stage** (auto-enables proxy):
```bash
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh create --env stage ...
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh view AAP-12345 --env stage
```

**Prod** (auto-sets URL, no proxy):
```bash
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh create --env prod ...
uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh view AAP-12345 --env prod
```

The `--env` flag:
- Selects correct token from config file
- Sets appropriate Jira URL (stage or prod)
- Enables/disables proxy as needed

## Key Features

- **No installation required**: Use `uvx` to run directly from GitHub
- **Markdown support**: Write issues in markdown, auto-convert to Jira format
- **Environment-aware**: Simple `--env` flag switches between stage and prod
- **Custom fields**: Automatic handling of acceptance criteria, epic name, parent links
- **JQL search**: Full JQL query support for issue discovery
- **Field discovery**: List available fields and requirements per issue type
- **API access**: Make any Jira REST API call via the `api` command
- **Security**: All issues automatically restricted to Red Hat employees

## Tips

1. **Add a shell alias** for convenience:
   ```bash
   alias jirahhh='uvx --from "git+https://github.com/shanemcd/jirahhh" jirahhh'
   ```

2. **Use markdown files** for complex descriptions - easier to edit and version control

3. **Discover fields first** when creating new issue types:
   ```bash
   jirahhh fields --project AAP --type Epic --env prod
   ```

4. **Search before creating** to avoid duplicates:
   ```bash
   jirahhh search "project = AAP AND summary ~ 'My Feature'" --env prod
   ```

5. **User mentions in comments**: Use full email format `[~user@redhat.com]` not `[~username]`

6. **Use `view` to inspect** existing issues when learning field formats

7. **Finding child issues**: Always use `"Parent Link" = ISSUE-KEY` not `parent = ISSUE-KEY` (see Custom Fields Reference section for details)

## Technical Details

- Uses `pycontribs/jira` Python library for Jira API access
- Uses Red Hat proxy (squid.corp.redhat.com:3128) for stage instance
- Authentication via Bearer token (not Basic Auth)
- Markdown conversion via `pypandoc` library
- Supports all Jira REST API v2 endpoints via `api` command

## Links

- **Repository**: https://github.com/shanemcd/jirahhh
- **Issues**: https://github.com/shanemcd/jirahhh/issues
- **Jira Production**: https://issues.redhat.com
- **Jira Stage**: https://issues.stage.redhat.com

---

*Last updated: 2025-10-20*
