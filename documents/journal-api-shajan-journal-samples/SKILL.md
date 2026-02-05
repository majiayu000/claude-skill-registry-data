---
name: journal-api
description: Interact with the Journal API to manage projects, documents, tasks, and workspaces. Use when the user mentions journal, projects, documents, tasks, workspaces, task identifiers like JO-123, or needs to access Journal data.
---

# Journal API Skill

This skill enables interaction with the Journal application - a project management and documentation platform for software teams.

## Overview

Journal organizes work into a hierarchy:

```
Organization
├── Workspaces (team spaces, e.g., "Engineering", "Design")
│   └── Documents (workspace-scoped context)
├── Projects (individual initiatives with status tracking)
│   ├── Documents (PRDs, specs, research notes)
│   └── Tasks (work items with implementation plans)
└── Global Documents (organization-wide context)
```

### Core Entities

| Entity | Description | Identifier |
|--------|-------------|------------|
| **Workspace** | Top-level team container | Slug (e.g., `coding-agent`) |
| **Project** | Initiative with status, owner, summary | Slug (e.g., `context-engine`) |
| **Document** | Rich text content (markdown) | Slug (e.g., `mvp-scope`) |
| **Task** | Work item with status, priority, assignee | Identifier (e.g., `JO-123`) |

### Document Types
- `organization_context` - Org-level strategy and guidelines
- `project_context` - PRDs, solution docs, project specs
- `workspace_context` - Team-shared context and standards  
- `clipped_page` - Saved web pages for reference
- `implementation_plan` - Technical specs for tasks

### Task Statuses
`backlog` → `to_do` → `in_progress` → `in_review` → `done` | `cancelled`

### Task Priorities
`urgent` | `high` | `medium` | `low` | `none` (unassigned)

## API Configuration

```
Base URL: http://localhost:3001
MCP Endpoint: POST /api/mcp/request
Required Headers:
  Content-Type: application/json
  Accept: application/json, text/event-stream
  x-mcp-api-key: <your-api-key>
```

## Available MCP Tools

### Projects

#### `get_project_context`
Get project overview including name, status, summary, and owner.

**Input:**
- `url` (required): Journal URL containing project path

**Example:**
```json
{
  "name": "get_project_context",
  "arguments": {
    "url": "https://journal.one/projects/context-engine"
  }
}
```

**Returns:** Project id, name, slug, icon, summary, status, owner, timestamps

---

### Documents

#### `get_document`
Fetch full markdown content of a document.

**Input:**
- `url` (required): Full document URL

**URL Patterns:**
- Global: `https://journal.one/documents/<slug>`
- Project: `https://journal.one/projects/<project>/documents/<slug>`
- Workspace: `https://journal.one/workspaces/<workspace>/documents/<slug>`

**Returns:** Document id, name, slug, type, markdown content, metadata, owner, timestamps

#### `list_project_documents`
List all documents within a project.

**Input:**
- `url` (required): Any URL containing the project path
- `type` (optional): Filter by document type

**Returns:** Array of documents with id, name, slug, type, owner, timestamps

---

### Tasks

#### `get_task`
Fetch task details including implementation plan if available.

**Input:**
- `task` (required): Task identifier (e.g., `JO-123`) or full URL

**Returns:**
- Task metadata: id, identifier, name, slug, status, priority, description
- Assignee, due date, labels, project name
- `implementationPlan.markdown` - Technical spec (if exists)
- `commentCount`, `resourceCount` - For follow-up queries

**Important:** When an implementation plan exists, follow it closely. Only deviate with explicit user approval.

#### `get_task_comments`
Fetch comments on a task with pagination.

**Input:**
- `task` (required): Task identifier or URL
- `parentCommentId` (optional): Get replies to specific comment
- `limit` (optional): 1-50, default 20
- `offset` (optional): For pagination

#### `get_task_resources`
Fetch resources attached to a task (GitHub PRs, Slack messages, Figma files, linked documents).

**Input:**
- `task` (required): Task identifier or URL
- `limit` (optional): 1-50, default 20
- `offset` (optional): For pagination

---

## Current Limitations

⚠️ **The following operations are NOT available via MCP:**

| Operation | Workaround |
|-----------|------------|
| List all tasks | Must know specific task ID (JO-xxx) |
| List all projects | Must know project slug |
| List workspaces | Must know workspace slug |
| Search across entities | Not available |
| Create/update tasks | Use tRPC API directly |
| Create/update documents | Use tRPC API directly |

**Cannot answer questions like:**
- "How many tasks are in progress?"
- "What projects exist?"
- "Find all tasks assigned to John"
- "Search for documents about authentication"

---

## Example Workflows

### Get Task and Implementation Plan
```
1. get_task(task: "JO-123")
   → Returns task details + implementationPlan.markdown
2. If commentCount > 0: get_task_comments(task: "JO-123")
3. If resourceCount > 0: get_task_resources(task: "JO-123")
```

### Explore a Project
```
1. get_project_context(url: ".../projects/my-project")
   → Returns project overview
2. list_project_documents(url: ".../projects/my-project")
   → Returns all documents in project
3. get_document(url: ".../projects/my-project/documents/prd")
   → Returns full document content
```

---

## MCP Request Format

All MCP calls use JSON-RPC 2.0:

```bash
curl -X POST http://localhost:3001/api/mcp/request \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "x-mcp-api-key: YOUR_API_KEY" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "TOOL_NAME",
      "arguments": { ... }
    },
    "id": 1
  }'
```

---

## Error Handling

| Error | Meaning |
|-------|---------|
| `Invalid API key` | API key not found or disabled |
| `Task not found` | Task doesn't exist or is deleted/draft |
| `Project not found` | Project doesn't exist or no access |
| `Document not found` | Document doesn't exist or no access |
| `Not Acceptable` | Missing `Accept: application/json, text/event-stream` header |

---

## Tips for Agents

1. **Task identifiers follow pattern**: `XX-NNN` (e.g., `JO-123`, `ENG-456`)
2. **Always check implementation plans**: Tasks may have detailed tech specs
3. **Use comments/resources counts**: Fetch additional context only when available
4. **URL flexibility**: Tools accept full URLs or just slugs/identifiers
5. **Project context first**: Get project overview before diving into documents
