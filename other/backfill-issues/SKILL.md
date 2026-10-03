---
name: backfill-issues
disable-model-invocation: true
allowed-tools: Bash(gh pr list:*), Bash(gh pr view:*), Bash(date:*), Read, mcp__linear-server__list_issues, mcp__linear-server__list_cycles, mcp__linear-server__save_issue, mcp__linear-server__list_issue_statuses
description: Generate tracker issues from merged PRs for the current sprint following strict grouping and review rules.
---

# Issue Generator from Merged PRs

You generate tracker issues from merged GitHub PRs that lack corresponding issues. You group related PRs into single issues and require user review before creation.

> **Setup:** this skill files through an issue-tracker MCP server (examples use a Linear-style
> API). Fill in your own IDs via `.env` (see `.env.example`) and enable the server in
> `.claude/settings.local.json`. The `mcp__linear-server__*` tool names are placeholders — swap
> them for your tracker's tools.

## Tracker Metadata

Read these from `.env` (never hardcode real account IDs in the repo):

- **Assignee:** `${TRACKER_ASSIGNEE_ID}`
- **Team:** `${TRACKER_TEAM_ID}`
- **Project:** `${TRACKER_PROJECT_ID}`

## Workflow

### 1. Date Range & Context

- Check `$ARGUMENTS` for `--since YYYY-MM-DD`.
- If missing, call `mcp__linear-server__list_cycles(teamId: "${TRACKER_TEAM_ID}", type: "current")`.
- Use the cycle's `startDate`. Inform the user of the start date being used.

### 2. Fetch Merged PRs

Execute:

```bash
gh pr list --author=@me --state=merged --search="merged:>=YYYY-MM-DD" --json number,title,url,mergedAt,body --limit 100
```

_Stop if no PRs are found._

### 3. Filter Linked PRs

Call `mcp__linear-server__list_issues(assignee: "${TRACKER_ASSIGNEE_ID}", team: "${TRACKER_TEAM_ID}")`.

- Exclude PRs where the URL exists in an issue description or attachment.
- Exclude PRs where the body contains "Closes ${TRACKER_ISSUE_PREFIX}-XXXX" (flag these to the user).
- Report the count of filtered/skipped PRs. _Stop if none remain._

### 4. Auto-Group Logic

Group unlinked PRs based on:

- **Scope/Prefix:** (e.g., `fix(engine):`, `feat(api):`).
- **Semantic Similarity:** Related features or bug fixes.
- **Labels:**
  - `feat:` → **Feature**
  - `fix:` → **Bug**
  - `chore:`/`refactor:` → **Chore**
  - `perf:` → **Improvement**
- **Estimates:** 1 PR = 1pt, 2-3 PRs = 2pts, 4+ PRs = 3pts.

### 5. Present Proposal

Display the groups clearly:

```text
📋 Proposed Issues (X groups from Y PRs)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Group 1: "title" [Label] (N pts)
  - #PR_NUM title
...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Skipped: Z PRs
```

### 6. Review & Adjust

Wait for user approval. Users may:

- **Approve all**
- **Merge/Split** groups.
- **Rename/Reclassify** or change **estimates**.
- **Remove** specific PRs or groups.
  Update and re-display the proposal until approved.

### 7. Issue Creation

For each approved group, call `mcp__linear-server__save_issue`:

- **State:** "Done" (PRs are already merged).
- **Description:** Include a summary and a markdown list of linked PRs with URLs.
- **Metadata:** Assignee, Team, Project, and Current Cycle ID.
- **Links:** Attach PR URLs as issue links.

### 8. Summary

Display the final results:

```text
✅ Created X issues:
  - ${TRACKER_ISSUE_PREFIX}-XXXX: "title" (Label, N pts) — N PRs linked
Total: X points across Y PRs
```

**CRITICAL:** NEVER create issues without explicit user approval of the grouping. Always link PR URLs to prevent duplicates in future runs.
