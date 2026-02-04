---
name: atlassian
description: Interact with Jira and Confluence via REST API - search, create, update issues and pages
---

# Atlassian Skill

Access Jira and Confluence directly via REST APIs. This skill provides full CRUD operations for issues and pages without requiring the MCP server.

## Authentication

Requires environment variables in `.env`:
- `ATLASSIAN_SITE` - Your Atlassian site (e.g., `yourcompany.atlassian.net`)
- `ATLASSIAN_EMAIL` - Your Atlassian account email
- `ATLASSIAN_API_TOKEN` - API token from https://id.atlassian.com/manage-profile/security/api-tokens

## Available Scripts

### Jira

#### Search Issues
```bash
npx tsx scripts/jira-search.ts "<JQL query>" [maxResults] [nextPageToken]
```
Examples:
- `npx tsx scripts/jira-search.ts "assignee = currentUser() AND status != Done"`
- `npx tsx scripts/jira-search.ts "project = PROJ AND type = Bug" 50`
- `npx tsx scripts/jira-search.ts "project = PROJ" 50 "token..."` (pagination)

See `docs/jql-guide.md` for JQL syntax reference.

#### Get Issue Details
```bash
npx tsx scripts/jira-get.ts <issueKey>
```
Example: `npx tsx scripts/jira-get.ts PROJ-123`

#### Create Issue
```bash
npx tsx scripts/jira-create.ts '<JSON>'
```
Single issue:
```bash
npx tsx scripts/jira-create.ts '{"project": "PROJ", "type": "Story", "summary": "New feature", "description": "Details here"}'
```

Bulk create (array):
```bash
npx tsx scripts/jira-create.ts '[{"project": "PROJ", "type": "Bug", "summary": "Bug 1"}, {"project": "PROJ", "type": "Bug", "summary": "Bug 2"}]'
```

#### Update Issue
```bash
npx tsx scripts/jira-update.ts <issueKey> '<JSON updates>'
```
Example: `npx tsx scripts/jira-update.ts PROJ-123 '{"status": "In Progress", "assignee": "user@example.com"}'`

#### Comments
```bash
# Get comments
npx tsx scripts/jira-comment.ts <issueKey> get

# Add comment
npx tsx scripts/jira-comment.ts <issueKey> add "<comment text>"
```

### Confluence

#### Search Pages
```bash
npx tsx scripts/confluence-search.ts "<CQL query>" [maxResults]
```
Examples:
- `npx tsx scripts/confluence-search.ts "title ~ 'Roadmap'"`
- `npx tsx scripts/confluence-search.ts "space = DEV AND type = page" 25`

See `docs/cql-guide.md` for CQL syntax reference.

#### Get Page Content
```bash
npx tsx scripts/confluence-get.ts <pageId>
# or by title
npx tsx scripts/confluence-get.ts --title "<page title>" --space <spaceKey>
```

#### Create Page
```bash
npx tsx scripts/confluence-create.ts '<JSON>'
```
Example:
```bash
npx tsx scripts/confluence-create.ts '{"space": "DEV", "title": "New Page", "body": "<p>Content here</p>"}'
```

Optional parent page:
```bash
npx tsx scripts/confluence-create.ts '{"space": "DEV", "title": "Child Page", "body": "<p>Content</p>", "parentId": "123456"}'
```

#### Update Page
```bash
npx tsx scripts/confluence-update.ts <pageId> '<JSON updates>'
```
Example: `npx tsx scripts/confluence-update.ts 123456 '{"title": "Updated Title", "body": "<p>New content</p>"}'`

## Query Language References

For generating correct queries:
- **Jira**: Read `docs/jql-guide.md` for JQL syntax, fields, operators, and functions
- **Confluence**: Read `docs/cql-guide.md` for CQL syntax and fields

## Common Workflows

### Find and update my open issues
1. Search: `npx tsx scripts/jira-search.ts "assignee = currentUser() AND status != Done"`
2. Update: `npx tsx scripts/jira-update.ts PROJ-123 '{"status": "Done"}'`

### Create issues from a list
1. Bulk create: `npx tsx scripts/jira-create.ts '[{...}, {...}, {...}]'`

### Find and read documentation
1. Search: `npx tsx scripts/confluence-search.ts "title ~ 'API Documentation'"`
2. Get content: `npx tsx scripts/confluence-get.ts 123456`

### Create a new documentation page
1. Create: `npx tsx scripts/confluence-create.ts '{"space": "DEV", "title": "API Guide", "body": "<h1>API Guide</h1><p>...</p>"}'`
