---
name: jira
description: Jira via Atlassian MCP — issue ops, JQL, branch naming, PR comment.
---

# Jira

## MCP Detection

Before any operation, verify the Atlassian MCP is available using this three-step check. **Do not show setup instructions until all three steps fail.**

1. **Check the CLI's MCP config** (`~/.claude.json` for Claude Code; `opencode.json` / Codex's MCP config otherwise) for an entry under `mcpServers` with key `atlassian` pointing to `mcp.atlassian.com`. If found, proceed to Step 2. If present but not loaded in this session, tell the user to restart their CLI.
2. **Run ToolSearch** with `query="atlassian", max_results=5`. If Atlassian tools appear, load the schema and proceed to Step 3.
3. **Verify connectivity** via `mcp__atlassian__atlassianUserInfo`. Success = fully operational. Auth error = guide re-authentication.

Only show setup instructions when all three steps fail. For setup details, load `references/mcp-setup.md`. For REST API fallback, load `references/rest-api.md`.

---

## Project Pattern Detection

After confirming the MCP, scan recent issues to detect team conventions:

```
mcp__atlassian__searchJiraIssuesUsingJql
  jql: "project = PROJ ORDER BY created DESC"
  fields: ["summary", "issuetype", "status", "labels", "components", "priority", "assignee", "reporter", "customfield_*"]
  maxResults: 10
```

Detect: custom issue types, label patterns, non-standard workflow statuses, custom fields, assignee norms, linked issue patterns. Store in working memory — do not re-query per operation.

**Pre-operation assignment confirmation:** before any write operation (create, update, transition, comment, assign), ask once per session: *"Should I assign this task to you as well?"* Remember the answer — do not ask again.

---

## Operations

For full MCP tool call signatures, load `references/operations.md`. Summary:

| Goal | MCP tool |
|------|----------|
| Fetch issue | `mcp__atlassian__getJiraIssue` |
| Search (JQL) | `mcp__atlassian__searchJiraIssuesUsingJql` |
| Create issue | `mcp__atlassian__createJiraIssue` |
| Update issue | `mcp__atlassian__editJiraIssue` |
| Transition | `mcp__atlassian__transitionJiraIssue` (fetch transitions first) |
| Comment | `mcp__atlassian__addCommentToJiraIssue` |
| Log work | `mcp__atlassian__addWorklogToJiraIssue` |
| Link issues | `mcp__atlassian__createIssueLink` (fetch types first) |

---

## Branch / Worktree Naming

Pattern: `{type}/{taskId}_short-description`

- `{type}` — Conventional Commits type (feat, fix, docs, chore, refactor, perf, test, build, ci, revert)
- `{taskId}` — Jira key exactly as-is (e.g., `VHI-450`)
- `short-description` — lowercase, hyphen-separated, ≤5 words, imperative

Examples: `feat/VHI-450_add-user-authentication`, `fix/PROJ-123_prevent-double-charge`

After creating the branch, confirm the assignment preference and act accordingly. Do not change issue status unless explicitly asked.

---

## Workflow Pattern

**Start work on an issue:**
1. Fetch issue → determine branch `type` from summary + issue type
2. Propose branch name → on approval, create branch (or worktree)
3. Ask assignment question once

**Create a bug report:**
1. Create issue: type `Bug`, priority matching severity, description with steps + expected + actual
2. Link to PR/commit if available

**After a PR is created:** ask *"Should I add a comment on {issueKey}?"* If yes, post comment with PR link following the QA comment format in `references/operations.md`.

---

## Conventions

- Always read the issue before creating a branch
- Never hard-code `cloudId` — fetch via `getAccessibleAtlassianResources` on first use
- Prefer `searchJiraIssuesUsingJql` for bulk lookups
- **Never transition status automatically** — only when the user explicitly requests it; always call `getTransitionsForJiraIssue` first (IDs vary per project)
- Every comment must begin with `Created by: @{reporter.displayName}` — always fetch reporter before posting
- All comments must follow the QA comment format in `references/operations.md`
- Ask the assignment question once per session; do not ask again once answered
