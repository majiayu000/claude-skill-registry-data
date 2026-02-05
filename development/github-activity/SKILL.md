---
name: github-activity
description: |
  This skill should be used when the user asks to "collect GitHub activity", "generate GitHub report", "show my PRs and commits", "what did I work on in GitHub", or requests activity summaries from GitHub for specific date ranges. Provides workflow for collecting issues, PRs, and commits via GitHub CLI.
agent: github-activity
context: fork
---

# GitHub Activity Reporter

Collect GitHub activity (PRs, Issues, Commits) via GitHub CLI and generate time-organized markdown reports.

## Prerequisites

- GitHub CLI (`gh`) authenticated with `repo` and `read:org` scopes
- Verify: `gh auth status`

## Workflow

### 1. Get User Info

```bash
gh api user --jq '.login'
```

If authentication fails: `gh auth login`

### 2. Calculate Date Range

- Explicit: "2025-11-05" -> use directly
- Relative: "yesterday" -> `date -v-1d '+%Y-%m-%d'` (macOS)
- Default: yesterday

Format: `${start_date}..${end_date}`

### 3. Collect Activity Data

Execute in parallel:

```bash
# PRs
gh search prs --involves=@me --updated="${date_range}" \
  --json number,title,repository,state,url,createdAt,closedAt,author

# Issues
gh search issues --involves=@me --updated="${date_range}" \
  --json number,title,repository,state,url,createdAt,author

# Commits (public repos only)
gh search commits --author=@me --committer-date="${date_range}" \
  --json commit,repository,sha,url

# Private commits: extract from each PR
gh pr view NUMBER --repo OWNER/REPO --json commits,additions,deletions,changedFiles
```

For complete CLI reference: [references/cli-reference.md](references/cli-reference.md)

### 4. Process Data

- Convert UTC to local timezone
- Group by hour and repository
- Deduplicate commits by SHA

### 5. Generate Reports

Output location: `~/.claude/tmp/github-activity/reports/`

**Files:**
- `YYYY-MM-DD.md` - Human-readable markdown
- `YYYY-MM-DD.json` - Machine-readable (for calendar-sync)

For format specification: [references/output-format.md](references/output-format.md)

## Usage Examples

| Request | Action |
|---------|--------|
| "GitHub activity yesterday" | Yesterday's report |
| "2025-11-01 to today" | Date range report |
| "Last week's commits" | Last 7 days |
| "delightroom org activity" | Organization filter |

## Integration

JSON output compatible with `google-calendar-sync` skill for importing activities to Google Calendar.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Auth error | `gh auth login` |
| No activities | Expand date range, check org filter |
| Missing commits | Private commits auto-fetched from PRs |
| Timezone issues | `export TZ=Asia/Seoul` |
