---
name: daily-report
description: |
  Daily report creation skill. Summarizes GitHub activities,
  creates a draft, and posts as an Issue.
  Use when:
  - Asked to "create daily report" or "write daily report"
  - Asked to "summarize today's activities"
  - Requested to create a daily report or journal
---

# Daily Report Skill

Summarize @i9wa4's GitHub activities and post as a GitHub Issue.

## 1. Prerequisites

- gh CLI installed
- jq installed

## 2. Workflow

### 2.1. Get GitHub Activities

Use dedicated script to fetch activities.
Defaults to fetching 24 hours of activities from current time
(calculated in UTC).

#### Script Location

```text
~/.config/claude/skills/daily-report/scripts/get-activities.sh
```

#### Command Examples

```bash
# Default: 24 hours ago to now
~/.config/claude/skills/daily-report/scripts/get-activities.sh --no-url

# Specify hours: N hours ago to now
~/.config/claude/skills/daily-report/scripts/get-activities.sh --hours 48 --no-url

# Specify datetime directly (ISO8601, UTC)
~/.config/claude/skills/daily-report/scripts/get-activities.sh --from 2025-12-16T15:00:00Z --to 2025-12-17T15:00:00Z --no-url
```

#### Options

| Option | Description |
| --- | --- |
| --no-url | Output without URLs (prevents mention notifications, for daily reports) |
| --hours N | Fetch activities from N hours ago to now |
| --from | Start datetime (ISO8601, e.g., 2025-12-17T00:00:00Z) |
| --to | End datetime (ISO8601, e.g., 2025-12-17T23:59:59Z) |
| --hostname | GitHub Enterprise Server hostname |

#### Output Format

```markdown
### repository-owner/repository-name

- [Issue] Issue title
- [IssueComment] Issue title
- [PullRequest] PR title
- [PullRequestComment] PR title
- [PullRequestReview] PR title
```

Note: Use `--no-url` option to omit URLs and prevent mention notifications.

### 2.2. Create Draft

Save to `.i9wa4/YYYY-MM-DD-Mawatari.md` (without keyword initially).

Template:

```markdown
---
title: "YYYY-MM-DD Mawatari"
labels:
  - name: "Daily Report"
    color: "0E8A16"
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

### 1.2. Meetings

- Meeting name
    - Supplementary comments

### 1.3. Other

- Notes

## 2. Reflection

Today's thoughts and learnings.
```

### 2.3. Wait for User Edit

Display draft and wait for user edits. User adds meetings and reflections.

### 2.4. Keyword Suggestion

After draft completion, suggest keywords from activities.

Suggestion tips:

- Serious candidates (dbt, Review, Meeting, etc.)
- Mix in humorous candidates (ideas inspired by activities)

Example: On an expensive dbt Labs deal day
-> "Expensive", "Declined" as candidates

### 2.5. Update Title

After user decides keyword, update only the title in file.
Do not change filename.

```markdown
title: "YYYY-MM-DD Mawatari {keyword}"
```

### 2.6. Post Issue

Post with `gh issue create`:

```bash
gh issue create --title "YYYY-MM-DD Mawatari {keyword}" --label "Daily Report" --body "$(cat <<'EOF'
[body]
EOF
)"
```

Display Issue URL after posting.

## 3. Important Rules

1. No direct links: Do not link PRs/Issues directly (triggers mentions),
   use titles only
2. Draft review: Always show draft to user and wait for edits
3. Keyword last: Suggest after draft completion. Include humor.
4. Fixed filename: Add keyword to title only, do not change filename
5. Issue posting: Post immediately after keyword confirmation

## 4. gh-furik Output Organization

Classify gh-furik output as follows:

| Output Type | Classification |
| --- | --- |
| Issue | Created Issues |
| PullRequest | Created PRs |
| PullRequestReview | Reviewed PRs |
| IssueComment | Commented Issues/PRs |
| PullRequestComment | Commented Issues/PRs |

Note: Consolidate multiple comments on same Issue/PR into one.
