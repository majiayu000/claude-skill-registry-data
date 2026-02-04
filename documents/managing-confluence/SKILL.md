---
name: managing-confluence
description: Reads, creates, and updates Confluence pages via MCP. Use when working with wiki pages, documentation, knowledge bases, CQL searches, or page hierarchies in Confluence. For Jira issues, use managing-jira instead.
allowed-tools: Bash
---

# Managing Confluence

Model Context Protocol server for Confluence pages, spaces, and content management.

## Overview

The Atlassian MCP server provides 13 tools for Confluence operations through the Model Context Protocol. It automatically connects to your Confluence instance when properly configured.

## Configuration

### Required Setup

The MCP server requires API credentials in `~/.atlassian-mcp.json`:

```json
{
  "domain": "your-domain.atlassian.net",
  "email": "your-email@example.com",
  "apiToken": "your-api-token-here"
}
```

**Create an API token:** https://id.atlassian.com/manage-profile/security/api-tokens

**Set permissions:**
```bash
chmod 600 ~/.atlassian-mcp.json
```

## Available Operations

### Spaces

**List Spaces:**
- View all accessible Confluence spaces
- Supports pagination for large instances
- Returns space keys, names, and types

### Pages

**Create Page:**
- Create new pages in any space
- Set title, content (in Confluence storage format), and parent page
- Supports both top-level and nested pages

**Get Page:**
- Retrieve page content by ID or title
- Returns full content including metadata
- Access page properties and versions

**Update Page:**
- Modify existing page content and title
- Requires page ID and version number
- Preserves page history

**Delete Page:**
- Remove pages from Confluence
- Requires page ID
- Moves page to trash (can be restored)

**List Child Pages:**
- Get all child pages of a parent page
- Navigate page hierarchies
- Returns page IDs and titles

**Get Page Ancestors:**
- Retrieve full page ancestor chain
- Navigate up the page tree
- Useful for breadcrumb generation

### Search

**Search Content:**
- Use CQL (Confluence Query Language) for powerful searches
- Search across pages, spaces, and content
- Filter by type, space, label, and more

**CQL Examples:**
```
type=page and space=MYSPACE
title ~ "meeting notes" and created > now("-30d")
label = "documentation" and space in (SPACE1, SPACE2)
```

### Comments

**Create Comment:**
- Add comments to pages
- Supports threaded discussions
- Requires page ID

**List Comments:**
- View all comments on a page
- Returns comment content and authors
- Includes nested replies

### Labels

**Add Label:**
- Tag pages with labels for organization
- Supports multiple labels per page
- Enables label-based search

**Remove Label:**
- Delete labels from pages
- Clean up outdated tags

**List Labels:**
- View all labels on a page
- Useful for content categorization

### Users

**Search Users:**
- Find users by name, email, or display name
- Get user account IDs for permissions
- Returns user profiles

## Common Patterns

### Creating a New Page

When creating a Confluence page, the MCP server will handle the operation through its available tools. Simply request the creation with the necessary details:

- **Space key**: The Confluence space where the page should be created
- **Title**: The page title
- **Content**: Page content in Confluence storage format (can be HTML or Markdown-like)
- **Parent page ID** (optional): For nested pages

### Searching for Pages

Use CQL queries to find specific content:

- Search by title: `title ~ "keyword"`
- Search by space: `space = SPACEKEY`
- Search by date: `created > now("-7d")`
- Combine filters: `type=page and space=DOCS and label="important"`

### Updating Existing Content

To update a page:

1. First retrieve the page to get its current version
2. Modify the content as needed
3. Update the page with new content and incremented version number

### Managing Page Hierarchies

Navigate page relationships:

- **List child pages** to see what's under a parent
- **Get ancestors** to understand page location in the space
- **Create nested pages** by specifying a parent page ID

## Important Notes

### Content Format

Confluence uses **storage format** for page content:
- HTML-like structure with Confluence-specific elements
- Use `<ac:structured-macro>` for macros
- Tables, images, and formatting use XHTML syntax

### Permissions

- MCP operations respect Confluence permissions
- You can only access spaces and pages you have permission to view
- Create/update/delete operations require appropriate permissions

### Rate Limiting

- Atlassian Cloud APIs have rate limits
- Batch operations carefully to avoid throttling
- The MCP server handles basic rate limiting

## Integration with Work Logs

When documenting Confluence work in dev/active/ logs:

- Reference pages by URL and page ID
- Note space keys for context
- Include CQL queries used for search operations
- Document any permission or access issues encountered

## Troubleshooting

### Authentication Errors

If you get authentication failures:
1. Verify `~/.atlassian-mcp.json` exists and has correct format
2. Check API token is valid (not expired)
3. Confirm email matches your Atlassian account
4. Ensure domain includes `.atlassian.net`

### Permission Errors

If operations fail due to permissions:
- Verify you have access to the space in Confluence web UI
- Check if page restrictions are limiting access
- Confirm your account has required permissions (view/edit/create)

### Page Not Found

If pages can't be located:
- Verify space key is correct (case-sensitive)
- Check if page was deleted or moved
- Try searching with CQL to locate the page

## Differences from ACLI

**Use Atlassian MCP for:**
- ✅ Confluence pages, spaces, and wiki content
- ✅ CQL search queries
- ✅ Page hierarchies and navigation
- ✅ Confluence comments and labels

**Use ACLI for:**
- ✅ Jira issues, work items, and tickets
- ✅ Jira comments and transitions
- ✅ JQL queries for Jira
- ✅ Sprints, epics, and Jira-specific features

## Resources

- **API Token Creation**: https://id.atlassian.com/manage-profile/security/api-tokens
- **Confluence REST API**: https://developer.atlassian.com/cloud/confluence/rest/
- **CQL Reference**: https://developer.atlassian.com/cloud/confluence/cql/
- **MCP Package**: https://github.com/xuanxt/atlassian-mcp
