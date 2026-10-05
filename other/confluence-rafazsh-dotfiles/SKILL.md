---
name: confluence
description: >-
  This skill should be used when the user asks to "read a Confluence page", "search Confluence",
  "create a wiki page", "update a Confluence page", "list Confluence spaces", "find documentation",
  or mentions Confluence, wiki pages, spaces, or CQL queries. Provides access to Confluence Cloud
  for reading, creating, updating pages, managing comments, labels, and searching content.
---

# Confluence Skill

Interact with Confluence Cloud using the `confluence.sh` script at `~/.claude/skills/confluence/scripts/confluence.sh`. All calls go through the Confluence REST API (v2 primarily, v1 for CQL search) using curl with Basic Auth.

## Prerequisites

Same Atlassian credentials as the Jira skill. The user must have these environment variables set (typically in `~/.zshrc`):

```
JIRA_DOMAIN or JIRA_URL   - e.g. mycompany.atlassian.net
JIRA_EMAIL                 - e.g. user@example.com
JIRA_API_TOKEN             - from https://id.atlassian.com/manage-profile/security/api-tokens
```

If any are missing, tell the user which variables need to be set and link to the token page.

## How to Use

Run commands via Bash:

```bash
bash ~/.claude/skills/confluence/scripts/confluence.sh <command> [args...]
```

### Available Commands

| Command | Args | Description |
|---------|------|-------------|
| `test` | | Verify authentication works |
| `get-spaces` | `[limit]` | List available spaces |
| `get-pages` | `<SPACE_ID>` `[limit]` `[sort]` | List pages in a space |
| `get-page` | `<PAGE_ID>` `[format]` | Get page content |
| `search` | `<CQL>` `[limit]` | Search with CQL |
| `create-page` | `<SPACE_ID>` `<TITLE>` `<BODY>` `[PARENT_ID]` | Create a page |
| `update-page` | `<PAGE_ID>` `<TITLE>` `<BODY>` | Update a page |
| `get-child-pages` | `<PAGE_ID>` `[limit]` | List child pages |
| `get-comments` | `<PAGE_ID>` `[limit]` | Get footer comments |
| `add-comment` | `<PAGE_ID>` `<BODY>` | Add a footer comment |
| `get-labels` | `<PAGE_ID>` | Get page labels |
| `add-label` | `<PAGE_ID>` `<LABEL>` | Add a label |

### Workflow Patterns

**Finding a page**: First get the space ID, then list pages or search.

```bash
bash ~/.claude/skills/confluence/scripts/confluence.sh get-spaces
bash ~/.claude/skills/confluence/scripts/confluence.sh get-pages 123456
```

**Reading a page**: Get page by ID with storage format (default) or ADF.

```bash
bash ~/.claude/skills/confluence/scripts/confluence.sh get-page 789012
```

**Searching content**: Use CQL (Confluence Query Language) for flexible search.

```bash
bash ~/.claude/skills/confluence/scripts/confluence.sh search "type = page AND space = 'PROJ' AND text ~ 'deployment'"
```

**Creating a page**: Provide space ID, title, and HTML body in Confluence storage format.

```bash
bash ~/.claude/skills/confluence/scripts/confluence.sh create-page 123456 "Page Title" "<p>Content here</p>"
```

**Updating a page**: Version number is auto-incremented by the script.

```bash
bash ~/.claude/skills/confluence/scripts/confluence.sh update-page 789012 "Updated Title" "<p>New content</p>"
```

### Output Handling

- Pipe output through `jq` for formatting when presenting to the user
- For `get-spaces`, present as a table with ID, key, and name
- For `get-page`, extract title, body content, and version info
- Storage format body contains XHTML - convert to readable text when presenting
- For `search`, extract and present title, space, and page ID from results

### Content Format

Confluence uses XHTML-like "storage format" for page bodies. For simple content, wrap text in `<p>` tags. For rich content (code blocks, panels, tables), consult `~/.claude/skills/confluence/references/confluence-api.md`.

### Error Handling

- **401**: Authentication failed - check JIRA_EMAIL and JIRA_API_TOKEN
- **403**: Permission denied - user may not have access to that space/page
- **404**: Page or space not found - verify the ID
- **409**: Version conflict - page was modified by someone else (retry)
- **429**: Rate limited - wait a few seconds and retry

## Reference

For detailed API endpoint documentation, CQL syntax, storage format examples, and macros, see `~/.claude/skills/confluence/references/confluence-api.md`.
