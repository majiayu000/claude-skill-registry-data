---
name: jira-to-todo
description: Export a user's pending (non-Done) Jira issues into a structured local todo.md with descriptions, links, and parent/epic grouping. Use when user says "export my jira tasks", "pull my open jira issues", "sync jira to todo", "what's on my jira board", "gera minha lista de tarefas do jira", or "exportar tarefas pendentes do jira". Do NOT use for general task tracking unrelated to Jira, PRD/requirements generation (taskmaster-prd-generator), or non-Jira todo list creation.
---

# Step-by-step: Export pending Jira tasks for a user to a local todo.md

**Goal:** Given a user's email, find their open (non-Done) Jira issues and write a structured markdown todo file with full context (description, links, parent grouping).

## Steps

1. **Discover available Atlassian MCP tools.** Search tool registry for `jira|atlassian` pattern. Confirm presence of: `getAccessibleAtlassianResources`, `atlassianUserInfo`, `searchJiraIssuesUsingJql`, `getJiraIssue`.

2. **Resolve identity and workspace.**
   - Call `getAccessibleAtlassianResources` → get `cloudId` for the target site.
   - Call `atlassianUserInfo` → get `account_id` for the requesting user (or use `lookupJiraAccountId` if searching for someone else by email/name).

3. **Get a total count before fetching full data.** Run `searchJiraIssuesUsingJql` with `searchResultMode: "count"` and JQL:

   ```
   assignee = "<accountId>" AND statusCategory != Done ORDER BY updated DESC
   ```

   This avoids blind pagination and tells you if the result set is small enough to fetch in one call.

4. **Fetch minimal-but-sufficient fields first.** Call `searchJiraIssuesUsingJql` again with explicit `fields`: `summary, description, status, issuetype, priority, labels, components, duedate, parent`. Avoid `"*all"` — it bloats token usage. If the response exceeds the tool's token limit, it auto-saves to a file — note the path.

5. **When output is saved to file, use jq, not manual reading.** Extract exactly the fields needed per issue, one JSON object per line (`jq -c '.issues.nodes[] | {...}'`), instead of reading the full file into context. This keeps token usage low and output structured.

6. **Extract parent/grouping relationships.** Re-run jq against the same file for `.fields.parent.key` and `.fields.parent.fields.summary` to build a hierarchy (epic/task → sub-tasks) for logical grouping in the output doc.

7. **Verify completeness before declaring done.** Don't assume default fields were exhaustive. Explicitly re-check for comments, attachments, and issue links by requesting those fields (`comment`, `attachment`, `issuelinks`) and counting them via jq (`length` per issue). If all counts are zero, that confirms nothing was missed — state this explicitly rather than assuming.

8. **Write the output file directly via shell heredoc** (`cat > file << 'EOF' ... EOF`), not via manual multi-step editing. Structure:
   - Header with generation date and data source (site name).
   - One section per parent task/epic, with sub-tasks as checkboxes underneath, each with key, status, and any description/link content inline.
   - A final section for ungrouped/standalone issues.
   - Preserve embedded links (Figma, etc.) and any structured data from descriptions (payload examples, validation rules) as sub-bullets rather than dropping them.

9. **Report back concisely**: total count, grouping summary, and explicitly confirm what verification pass was done (e.g. "checked comments/attachments/links — all zero, nothing missed").

## Reusable pattern (generalizable to a skill)

```
resolve cloudId + accountId
  → JQL count query (sanity check size)
  → JQL fields query (targeted fields only)
  → [if truncated] jq-extract from saved file, never bulk-read
  → jq-extract parent hierarchy
  → jq-extract verification fields (comments/attachments/links) as a completeness check
  → write structured .md via heredoc
  → report counts + verification result
```

**Key anti-patterns avoided:**

- Requesting `fields: ["*all"]` upfront (wastes tokens, triggers truncation).
- Reading a large saved JSON file in full via Read tool instead of jq-filtering.
- Declaring "done" without a completeness check against secondary fields (comments/links/attachments).
