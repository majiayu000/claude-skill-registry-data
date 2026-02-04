---
name: daily-report
description: |
  Daily report creation skill. Summarizes GitHub and Jira activities,
  creates a draft, and posts as an Issue.
  Use when:
  - Asked to "create daily report" or "write daily report"
  - Asked to "summarize today's activities"
  - Requested to create a daily report or journal
disable-model-invocation: true
---

# Daily Report Skill

Summarize @i9wa4's GitHub and Jira activities and post as a GitHub Issue.

## 1. Prerequisites

- gh CLI installed
- jq installed
- acli installed (for Jira)

## 2. Workflow

### 2.1. Get GitHub Activities

Use dedicated script to fetch activities.
Defaults to fetching 24 hours of activities from current time
(calculated in UTC).

#### 2.1.1. Script Location

```text
${CLAUDE_CONFIG_DIR}/skills/daily-report/scripts/get-activities.sh
```

#### 2.1.2. Command Examples

```bash
# Default: 24 hours ago to now
${CLAUDE_CONFIG_DIR}/skills/daily-report/scripts/get-activities.sh --no-url

# Specify hours: N hours ago to now
${CLAUDE_CONFIG_DIR}/skills/daily-report/scripts/get-activities.sh --hours 48 --no-url

# Specify datetime directly (ISO8601, UTC)
${CLAUDE_CONFIG_DIR}/skills/daily-report/scripts/get-activities.sh --from 2025-12-16T15:00:00Z --to 2025-12-17T15:00:00Z --no-url
```

#### 2.1.3. Options

| Option | Description |
| --- | --- |
| --no-url | Output without URLs (prevents mention notifications, for daily reports) |
| --hours N | Fetch activities from N hours ago to now |
| --from | Start datetime (ISO8601, e.g., 2025-12-17T00:00:00Z) |
| --to | End datetime (ISO8601, e.g., 2025-12-17T23:59:59Z) |
| --hostname | GitHub Enterprise Server hostname |
| --exclude-owner | Exclude repos by owner (comma-separated, default: i9wa4) |
| --include-personal | Include personal repos (overrides --exclude-owner) |

#### 2.1.4. Output Format

```markdown
### repository-owner/repository-name

- [Issue] Issue title
- [IssueComment] Issue title
- [PullRequest] PR title
- [PullRequestComment] PR title
- [ReviewedPR] PR title (PRs reviewed by me, excludes my own PRs)
```

Note: Use `--no-url` option to omit URLs and prevent mention notifications.
Note: Personal repos (i9wa4/*) are excluded by default.

### 2.2. Get Jira Activities

Use acli to fetch Jira activities.

```sh
# Today's activities
acli jira workitem search \
    --jql "updated >= startOfDay() AND (assignee = currentUser() OR reporter = currentUser()) ORDER BY updated DESC" \
    --fields "key,summary,status"

# Specific date range
acli jira workitem search \
    --jql "updated >= 'YYYY-MM-DD' AND updated < 'YYYY-MM-DD' AND (assignee = currentUser() OR reporter = currentUser()) ORDER BY updated DESC" \
    --fields "key,summary,status"
```

### 2.3. Create Draft

Create file:

```bash
FILE=$(${CLAUDE_CONFIG_DIR}/scripts/touchfile.sh ".i9wa4/$(date +%Y-%m-%d)-$(whoami).md")
```

NOTE: Keep command blocks in "AI Coding Tool Usage" section.
Execute commands and paste results below the command block.

Template:

````markdown
---
title: "YYYY-MM-DD $(whoami)"
labels:
  - name: "日報"
    color: "0887b9"
---

## 1. Today's Activities

### 1.1. GitHub

Organize gh-furik output. Classify as follows:

#### 1.1.1. Created Issues

- [repo-name] Issue title

#### 1.1.2. Created PRs

- [repo-name] PR title
- [repo-name] PR title (merged)
    - Add supplementary comments indented

#### 1.1.3. Reviewed PRs

- [repo-name] PR title

#### 1.1.4. Commented Issues/PRs

- [repo-name] Issue/PR title

### 1.2. Jira

- [KEY-123] Issue summary (status)

### 1.3. Meetings

- Meeting name
    - Supplementary comments

## 2. AI Coding Tool Usage

### 2.1. Claude Code

```console
npx ccusage@latest --compact --since $(date +%Y%m%d)
```

| Date       | Models | Input | Output | Cost (USD) |
| ---------- | ------ | ----- | ------ | ---------- |

### 2.2. Codex CLI

```console
npx @ccusage/codex@latest --compact --since $(date +%Y%m%d)
```

| Date       | Models | Input | Output | Cost (USD) |
| ---------- | ------ | ----- | ------ | ---------- |

## 3. Reflection

````

### 2.4. Wait for User Edit

Display draft and wait for user edits. User adds meetings and reflections.

### 2.5. Post Issue

Post with `gh issue create`:

```bash
gh issue create --title "YYYY-MM-DD $(whoami)" --label "日報" --body "$(cat <<'EOF'
[body]
EOF
)"
```

Display Issue URL after posting.

## 3. Important Rules

1. No direct links: Do not link PRs/Issues directly (triggers mentions),
   use titles only
2. PR/Issue numbers: Use `(# 123)` with space, not `(#123)`.
   Without space, GitHub auto-links to unintended repos.
3. Draft review: Always show draft to user and wait for edits
4. Issue posting: Post after user confirms draft is ready

## 4. Output Type Classification

Classify script output as follows:

| Output Type        | Classification       |
| ---                | ---                  |
| Issue              | Created Issues       |
| PullRequest        | Created PRs          |
| ReviewedPR         | Reviewed PRs         |
| IssueComment       | Commented Issues/PRs |
| PullRequestComment | Commented Issues/PRs |

Note: Consolidate multiple comments on same Issue/PR into one.
Note: ReviewedPR only includes PRs authored by others (my own PRs excluded).
