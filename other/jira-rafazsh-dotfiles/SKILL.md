---
name: jira
description: >-
  Interact with Jira Cloud: read, create, edit issues, manage transitions, add comments and worklogs.
  Use when the user asks about Jira issues, wants to search tickets, create/update issues,
  change status, add comments, or log work. Triggers on keywords like "jira", "ticket",
  "issue", "sprint", "backlog", "PROJ-123" (issue key patterns), "JQL".
triggers:
  - jira
  - ticket
  - sprint
  - backlog
  - JQL
---

# Jira Skill

You can interact with Jira Cloud using the `jira.sh` script at `~/.claude/skills/jira/scripts/jira.sh`. All calls go through the Jira REST API v3 using curl with Basic Auth.

## Prerequisites

The user must have these environment variables set (typically in `~/.zshrc`):

```
JIRA_DOMAIN   - e.g. mycompany.atlassian.net
JIRA_EMAIL    - e.g. user@example.com
JIRA_API_TOKEN - from https://id.atlassian.com/manage-profile/security/api-tokens
```

If any are missing, tell the user which variables need to be set and link to the token page.

## How to Use

Run commands via Bash:

```bash
bash ~/.claude/skills/jira/scripts/jira.sh <command> [args...]
```

### Available Commands

| Command | Args | Description |
|---------|------|-------------|
| `test` | | Verify authentication works |
| `get-issue` | `<KEY>` `[fields]` | Get issue details |
| `search` | `<JQL>` `[maxResults]` `[fields]` | Search with JQL |
| `create-issue` | `<PROJECT>` `<TYPE>` `<SUMMARY>` `[DESC]` | Create an issue |
| `edit-issue` | `<KEY>` `<FIELDS_JSON>` | Update issue fields |
| `get-comments` | `<KEY>` `[maxResults]` | Get comments |
| `add-comment` | `<KEY>` `<BODY>` | Add a comment |
| `get-transitions` | `<KEY>` | List available transitions |
| `transition-issue` | `<KEY>` `<TRANSITION_ID>` | Change issue status |
| `add-worklog` | `<KEY>` `<TIME>` `[COMMENT]` | Log time |
| `get-projects` | `[maxResults]` | List projects |

### Workflow Patterns

**Reading an issue**: Get the issue, then present a clean summary with key, summary, status, assignee, and description.

```bash
bash ~/.claude/skills/jira/scripts/jira.sh get-issue PROJ-123
```

**Searching**: Construct appropriate JQL from the user's natural language request.

```bash
bash ~/.claude/skills/jira/scripts/jira.sh search "project = PROJ AND status = 'In Progress' ORDER BY priority DESC"
```

**Changing status**: Always get transitions first to find the correct transition ID, then transition.

```bash
bash ~/.claude/skills/jira/scripts/jira.sh get-transitions PROJ-123
bash ~/.claude/skills/jira/scripts/jira.sh transition-issue PROJ-123 31
```

**Editing fields**: Pass fields as a JSON object.

```bash
bash ~/.claude/skills/jira/scripts/jira.sh edit-issue PROJ-123 '{"summary":"New title","priority":{"name":"High"}}'
```

### Output Handling

- Pipe output through `jq` for formatting when presenting to the user
- For `get-issue`, extract and present: key, summary, status, priority, assignee, description
- For `search`, present results as a table with key, summary, status, assignee
- For `create-issue`, confirm with the new issue key from the response
- ADF description fields need to be converted to plain text for readability

### Error Handling

- **401**: Authentication failed - ask user to check JIRA_EMAIL and JIRA_API_TOKEN
- **403**: Permission denied - user may not have access to that project/issue
- **404**: Issue not found - verify the issue key
- **429**: Rate limited - wait a few seconds and retry

## Reference

For detailed API endpoint documentation, field formats, JQL syntax, and ADF structure, see `~/.claude/skills/jira/references/jira-api.md`.
