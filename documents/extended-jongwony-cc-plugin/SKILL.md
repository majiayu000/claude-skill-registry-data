---
name: extended
description: Create and manage Linear documents and project milestones
---

## Overview

This skill extends Linear MCP capabilities by adding write operations for Documents and ProjectMilestones. While Linear MCP provides read-only access to documents and no milestone support, this skill enables full CRUD operations via direct GraphQL API calls.

**What this skill adds:**
- Document creation, updates, and deletion
- Project milestone management (create, update, delete, list, get)
- Direct GraphQL access for advanced operations

**Prerequisites:**
1. Linear API Key from https://linear.app/settings/api
2. Set environment variable: `export LINEAR_API_KEY="lin_api_xxxxx"`
3. Optional: `jq` for JSON formatting

---

## Document Operations

### Creating a Document

**Basic example:**
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation DocumentCreate($input: DocumentCreateInput!) { documentCreate(input: $input) { success document { id title url slugId createdAt creator { name } } } }",
    "variables": {
      "input": {
        "title": "API Design Document"
      }
    }
  }'
```

**With content and project:**
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation DocumentCreate($input: DocumentCreateInput!) { documentCreate(input: $input) { success document { id title url slugId } } }",
    "variables": {
      "input": {
        "title": "Q4 Roadmap",
        "content": "# Q4 Goals\n\n- Launch feature X\n- Improve performance by 30%",
        "projectId": "PROJECT_ID_HERE",
        "color": "#FF6B6B"
      }
    }
  }'
```

**Available parameters:**
- `title` (required): Document title
- `content`: Markdown content
- `projectId`: Attach to project
- `initiativeId`: Attach to initiative
- `issueId`: Attach to issue
- `color`: Icon color (hex format)
- `icon`: Icon emoji or name (optional, some emojis may not be valid - omit if validation fails)
- `sortOrder`: Display order (float)

---

### Updating a Document

**Update title and content:**
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation DocumentUpdate($id: String!, $input: DocumentUpdateInput!) { documentUpdate(id: $id, input: $input) { success document { id title updatedAt updatedBy { name } } } }",
    "variables": {
      "id": "DOCUMENT_ID_OR_SLUG",
      "input": {
        "title": "Updated Title",
        "content": "# Updated Content\n\nNew information here."
      }
    }
  }'
```

**Move to trash:**
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation DocumentUpdate($id: String!, $input: DocumentUpdateInput!) { documentUpdate(id: $id, input: $input) { success } }",
    "variables": {
      "id": "DOCUMENT_ID",
      "input": {
        "trashed": true
      }
    }
  }'
```

**Available update parameters:**
- `title`: New title
- `content`: New markdown content
- `color`: New icon color
- `icon`: New icon
- `trashed`: Move to trash (true) or restore (false)
- `projectId`: Move to different project
- `sortOrder`: Update display order

---

### Deleting a Document

**Permanently delete (archive):**
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation DocumentDelete($id: String!) { documentDelete(id: $id) { success } }",
    "variables": {
      "id": "DOCUMENT_ID"
    }
  }'
```

**Restore archived document:**
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation DocumentUnarchive($id: String!) { documentUnarchive(id: $id) { success entity { id title } } }",
    "variables": {
      "id": "DOCUMENT_ID"
    }
  }'
```

---

## Project Milestone Operations

### Creating a Milestone

**Basic milestone:**
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation ProjectMilestoneCreate($input: ProjectMilestoneCreateInput!) { projectMilestoneCreate(input: $input) { success projectMilestone { id name status progress targetDate project { id name } } } }",
    "variables": {
      "input": {
        "projectId": "PROJECT_ID_HERE",
        "name": "Beta Release"
      }
    }
  }'
```

**With description and target date:**
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation ProjectMilestoneCreate($input: ProjectMilestoneCreateInput!) { projectMilestoneCreate(input: $input) { success projectMilestone { id name status progress targetDate } } }",
    "variables": {
      "input": {
        "projectId": "PROJECT_ID_HERE",
        "name": "MVP Launch",
        "description": "# MVP Goals\n\n- Core features complete\n- 10 beta users onboarded",
        "targetDate": "2025-06-30"
      }
    }
  }'
```

**Interactive approach (using AskUserQuestion):**

When user doesn't specify a target date, use AskUserQuestion to ask:

```typescript
// Step 1: Ask user for target date
AskUserQuestion({
  questions: [{
    question: "What is the target date for this milestone?",
    header: "Target Date",
    multiSelect: false,
    options: [
      {
        label: "End of this month",
        description: "Set target date to the last day of current month"
      },
      {
        label: "End of next month",
        description: "Set target date to the last day of next month"
      },
      {
        label: "Custom date",
        description: "I'll specify a custom date in YYYY-MM-DD format"
      },
      {
        label: "No target date",
        description: "Create milestone without a specific target date"
      }
    ]
  }]
})

// Step 2: Based on user's answer, construct the mutation
// If custom date selected, prompt for YYYY-MM-DD format
// If no target date, omit targetDate from input
```

**Available parameters:**
- `projectId` (required): Parent project ID
- `name` (required): Milestone name
- `description`: Markdown description
- `targetDate`: Target date (YYYY-MM-DD format)
- `sortOrder`: Display order (float)

**Status values (auto-calculated):**
- `unstarted`: No progress yet
- `next`: Next milestone to work on
- `overdue`: Past target date
- `done`: All issues completed

---

### Updating a Milestone

**Update name and target date:**
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation ProjectMilestoneUpdate($id: String!, $input: ProjectMilestoneUpdateInput!) { projectMilestoneUpdate(id: $id, input: $input) { success projectMilestone { id name status targetDate } } }",
    "variables": {
      "id": "MILESTONE_ID",
      "input": {
        "name": "MVP Launch - Extended",
        "targetDate": "2025-07-15"
      }
    }
  }'
```

**Available update parameters:**
- `name`: New name
- `description`: New markdown description
- `targetDate`: New target date (YYYY-MM-DD)
- `sortOrder`: New display order

---

### Listing Milestones

**List all milestones:**
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "query ProjectMilestones($first: Int) { projectMilestones(first: $first) { nodes { id name status progress targetDate project { id name } issues { nodes { id title } } } } }",
    "variables": {
      "first": 50
    }
  }'
```

**List milestones for specific project:**
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "query Project($id: String!) { project(id: $id) { id name projectMilestones { nodes { id name status progress targetDate } } } }",
    "variables": {
      "id": "PROJECT_ID"
    }
  }'
```

---

### Getting a Single Milestone

**Detailed milestone info:**
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "query ProjectMilestone($id: String!) { projectMilestone(id: $id) { id name description status progress progressHistory currentProgress targetDate createdAt updatedAt project { id name state } issues { nodes { id title state { name type } assignee { name } } } } }",
    "variables": {
      "id": "MILESTONE_ID"
    }
  }'
```

---

### Deleting a Milestone

```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation ProjectMilestoneDelete($id: String!) { projectMilestoneDelete(id: $id) { success } }",
    "variables": {
      "id": "MILESTONE_ID"
    }
  }'
```

---

### Moving a Milestone to Another Project

```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation ProjectMilestoneMove($id: String!, $input: ProjectMilestoneMoveInput!) { projectMilestoneMove(id: $id, input: $input) { success projectMilestone { id name project { id name } } } }",
    "variables": {
      "id": "MILESTONE_ID",
      "input": {
        "projectId": "NEW_PROJECT_ID"
      }
    }
  }'
```

---

## Usage Guidelines

### When to use this skill

**Document operations:**
- User asks to "create a document" or "write a doc"
- User wants to "update document content"
- User needs to "delete" or "archive" a document
- User wants to "move document to trash" or "restore document"

**Milestone operations:**
- User asks to "create a milestone" or "add milestone"
- User wants to "set target date for milestone"
- User needs to "update milestone status" or "rename milestone"
- User asks to "list project milestones" or "show milestone progress"
- User wants to "delete milestone" or "move milestone to another project"

**IMPORTANT for Milestones:**
- **Always use AskUserQuestion** to ask for targetDate when creating or updating milestones
- Ask the user to provide a target date in YYYY-MM-DD format
- Validate the date format before making the API call
- If user doesn't provide a date, milestone can be created without targetDate (optional)

### How to use

1. **Always check for LINEAR_API_KEY:**
   ```bash
   if [ -z "$LINEAR_API_KEY" ]; then
     echo "Error: LINEAR_API_KEY not set. Get key from https://linear.app/settings/api"
     exit 1
   fi
   ```

2. **Get IDs first:**
   - Use Linear MCP's `list_projects` to get project IDs
   - Use Linear MCP's `list_issues` to get issue IDs
   - Use `list_documents` to get document IDs/slugs

3. **For milestone operations, use AskUserQuestion:**
   - When creating a milestone, ask for targetDate using AskUserQuestion tool
   - Example question: "What is the target date for this milestone? (YYYY-MM-DD format, or leave empty for no date)"
   - Parse the user's response and include in the mutation
   - If user provides empty/no date, omit targetDate from the input

4. **Handle JSON carefully:**
   - Escape newlines in markdown: use `\n`
   - Escape quotes: use `\"`
   - For complex content, consider using heredoc or jq

5. **Check responses:**
   - Always verify `success: true` in mutation responses
   - If `success: false`, check the `errors` array
   - Show the document/milestone URL when available

6. **Handle icon field carefully:**
   - The `icon` field is optional for documents
   - Some emojis may fail validation with "icon is not a valid icon" error
   - If icon validation fails, omit the field and retry
   - Linear API only accepts certain emojis - no definitive list available

7. **Format output for user:**
   - Use `jq` to pretty-print JSON
   - Extract key fields like `id`, `url`, `status`
   - Provide actionable next steps

---

## Error Handling

**Authentication errors:**
```json
{
  "errors": [
    {
      "message": "Authentication required",
      "extensions": { "code": "UNAUTHENTICATED" }
    }
  ]
}
```
→ Check if LINEAR_API_KEY is set and valid

**Not found errors:**
```json
{
  "errors": [
    {
      "message": "Resource not found",
      "extensions": { "code": "NOT_FOUND" }
    }
  ]
}
```
→ Verify the ID exists using list operations first

**Validation errors:**
```json
{
  "data": {
    "documentCreate": {
      "success": false
    }
  },
  "errors": [
    {
      "message": "Title is required",
      "path": ["documentCreate", "input", "title"]
    }
  ]
}
```
→ Check required fields are provided

**Rate limiting:**
```json
{
  "errors": [
    {
      "message": "Rate limit exceeded",
      "extensions": { "code": "RATE_LIMITED" }
    }
  ]
}
```
→ Wait and retry after a few seconds

**Icon validation errors:**
```json
{
  "errors": [
    {
      "message": "Argument Validation Error",
      "extensions": {
        "code": "INVALID_INPUT",
        "validationErrors": [
          {
            "property": "icon",
            "constraints": {
              "customValidation": "icon is not a valid icon"
            }
          }
        ]
      }
    }
  ]
}
```
→ Omit the `icon` field or try a different emoji/icon name. Linear API only accepts certain emojis.

---

## Examples

### Example 1: Create a project document with content

**User request:** "Create a technical spec document for project abc123 with an overview section"

**Response:**
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation DocumentCreate($input: DocumentCreateInput!) { documentCreate(input: $input) { success document { id title url } } }",
    "variables": {
      "input": {
        "title": "Technical Specification",
        "content": "# Overview\n\nThis document outlines the technical architecture and implementation details.\n\n## Architecture\n\nTBD\n\n## Implementation\n\nTBD",
        "projectId": "abc123"
      }
    }
  }' | jq '.'
```

### Example 2: Create milestone with target date (user specified)

**User request:** "Add a 'Beta Launch' milestone to project xyz789, target date is March 31, 2025"

**Response:**
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation ProjectMilestoneCreate($input: ProjectMilestoneCreateInput!) { projectMilestoneCreate(input: $input) { success projectMilestone { id name status targetDate project { name } } } }",
    "variables": {
      "input": {
        "projectId": "xyz789",
        "name": "Beta Launch",
        "targetDate": "2025-03-31"
      }
    }
  }' | jq '.'
```

### Example 2b: Create milestone asking for target date

**User request:** "Create a milestone 'Phase 1 Complete' for project xyz789"

**Step 1 - Use AskUserQuestion to ask for target date:**
```
Ask user: "What is the target date for the 'Phase 1 Complete' milestone?"
Options:
- Specific date (YYYY-MM-DD format)
- No target date
```

**Step 2 - If user provides date (e.g., "2025-06-30"):**
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation ProjectMilestoneCreate($input: ProjectMilestoneCreateInput!) { projectMilestoneCreate(input: $input) { success projectMilestone { id name status targetDate project { name } } } }",
    "variables": {
      "input": {
        "projectId": "xyz789",
        "name": "Phase 1 Complete",
        "targetDate": "2025-06-30"
      }
    }
  }' | jq '.'
```

**Step 2 - If user provides no date:**
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation ProjectMilestoneCreate($input: ProjectMilestoneCreateInput!) { projectMilestoneCreate(input: $input) { success projectMilestone { id name status project { name } } } }",
    "variables": {
      "input": {
        "projectId": "xyz789",
        "name": "Phase 1 Complete"
      }
    }
  }' | jq '.'
```

### Example 3: Update document content

**User request:** "Update document doc_abc123 to add a new section about testing"

**Response:**
```bash
# First, get current content using Linear MCP's get_document
# Then update with new content:

curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation DocumentUpdate($id: String!, $input: DocumentUpdateInput!) { documentUpdate(id: $id, input: $input) { success document { id updatedAt } } }",
    "variables": {
      "id": "doc_abc123",
      "input": {
        "content": "[EXISTING_CONTENT]\n\n## Testing\n\n- Unit tests\n- Integration tests\n- E2E tests"
      }
    }
  }' | jq '.'
```

### Example 4: List milestones with progress

**User request:** "Show me all milestones and their progress"

**Response:**
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "query { projectMilestones(first: 50) { nodes { name status progress targetDate project { name } issues { nodes { id } } } } }"
  }' | jq '.data.projectMilestones.nodes[] | "\(.project.name) - \(.name): \(.progress * 100)% complete (target: \(.targetDate // "No date set"))"'
```

---

## Combining with Linear MCP

This skill works best **alongside** the official Linear MCP server:

**Linear MCP provides (read operations):**
- `list_documents` - Get existing documents
- `get_document` - Read document content
- `list_projects` - Get project IDs
- `list_issues` - Get issue IDs
- `list_teams` - Get team info

**This skill adds (write operations):**
- `documentCreate` - Create new documents
- `documentUpdate` - Update documents
- `documentDelete` - Delete documents
- `projectMilestoneCreate` - Create milestones
- `projectMilestoneUpdate` - Update milestones
- `projectMilestoneDelete` - Delete milestones
- `projectMilestones` query - List milestones (not in MCP)

**Typical workflow:**
1. Use Linear MCP to list projects → Get project ID
2. Use this skill to create a document for that project
3. Use Linear MCP to verify the document appears in listings
4. Use this skill to create milestones for the project
5. Use this skill to query milestone progress

---

## Advanced Usage

### Using jq for complex operations

**Extract just the document URL:**
```bash
curl -X POST ... | jq -r '.data.documentCreate.document.url'
```

**Format milestone list as table:**
```bash
curl -X POST ... | jq -r '.data.projectMilestones.nodes[] | [.name, .status, (.progress * 100 | tostring + "%")] | @tsv'
```

### Using heredoc for large content

```bash
CONTENT=$(cat <<'EOF'
# Architecture Design

## Overview
System architecture overview here.

## Components
- API Gateway
- Service Mesh
- Data Layer
EOF
)

# Create temp file with Python for proper JSON encoding
TEMP_FILE=$(mktemp)
python3 << PEOF > "$TEMP_FILE"
import json
data = {
    "query": """mutation DocumentCreate(\$input: DocumentCreateInput!) {
        documentCreate(input: \$input) {
            success
            document { id url }
        }
    }""",
    "variables": {
        "input": {
            "title": "Architecture Design",
            "content": """$CONTENT"""
        }
    }
}
print(json.dumps(data, ensure_ascii=False))
PEOF

curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d @"$TEMP_FILE" | jq '.'

rm "$TEMP_FILE"
```

---

## References

For detailed schema information:
- @references/document-schema.md - Complete Document type definitions
  - Search patterns: `grep "DocumentCreateInput\|DocumentUpdateInput\|icon\|color" references/document-schema.md`
- @references/milestone-schema.md - Complete ProjectMilestone type definitions
  - Search patterns: `grep "ProjectMilestoneCreateInput\|ProjectMilestoneUpdateInput\|targetDate" references/milestone-schema.md`
- @references/examples.md - Additional usage examples
  - Search patterns: `grep "Example\|mutation\|query" references/examples.md`

For the original GraphQL schema:
- https://github.com/linear/linear/blob/master/packages/sdk/src/schema.graphql
