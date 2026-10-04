---
name: jira-connector
description: Query Jira issues, projects, and boards
activation_keywords: [jira, issue, ticket, project, board, epic, story, bug]
execution_mode: server
---

# Jira Connector Skill

Provides read-only Jira operations:
- Search issues with JQL
- Get issue details
- List projects
- Get board status

Use `builtin_jira_connector` tool with fields:
- `operation`: one of "search", "issue", "projects", "board"
- `jql`: JQL query (for search)
- `issue_key`: Issue key (for issue details)
- `jira_url`: Jira server URL
- `api_token`: Jira API token

Note: Requires Jira URL and credentials.
