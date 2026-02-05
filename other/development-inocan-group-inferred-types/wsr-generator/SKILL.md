---
name: wsr-generator
description: |
  Generate professional weekly status report entries from git history and Azure DevOps activity.
  Use when asked for: wsr, status, weekly report, status entry, what did I complete,
  status update, generate report, weekly summary, send wsr, send status.
  Requires: azure-devops skill configured (.ado/config.json), git repository.
---

# Weekly Status Report Generator

Generate professional WSR entries from git history and Azure DevOps activity with:
- **Live links** to work items and commits
- **Audience-based detail levels** (executive, standard, technical)
- **Multiple output formats** (Markdown, HTML)
- **Professional status indicators** (Unicode symbols, styled badges)
- **Multi-channel notifications** (Email, Teams, Slack)

## Quick Start

When user asks for their WSR or to send a status report:

```bash
# 1. Initialize WSR (if not done)
python3 skills/wsr-generator/scripts/wsr_config.py init

# 2. Gather and import data (Claude orchestrates - see Workflow below)

# 3. Generate report
python3 skills/wsr-generator/scripts/wsr_report.py generate

# 4. Send to configured channel
python3 skills/wsr-generator/scripts/wsr_notify.py send
```

## Workflow (Claude Orchestration)

This skill uses Claude as the orchestrator. Data gathering happens via the **azure-devops skill** and **git commands**, then gets imported into WSR.

### Step 1: Gather Work Items (via azure-devops skill)

Query work items changed this week:

```bash
python3 skills/azure-devops/scripts/query-work-items.py --preset changed-this-week --format json
```

Or completed items:

```bash
python3 skills/azure-devops/scripts/query-work-items.py --preset completed-this-week --format json
```

### Step 2: Gather Git Commits

Get commits from this week:

```bash
git log --since="Monday" --author="$(git config user.email)" \
  --pretty=format:'{"sha":"%H","short_sha":"%h","subject":"%s","author":"%an","date":"%ai"}' \
  --numstat
```

Or simpler format:

```bash
git log --since="Monday" --oneline --author="$(git config user.email)"
```

### Step 3: Transform and Import

Transform the gathered data into WSR entry format and import:

```bash
# Claude creates JSON and pipes to import
echo '{"entries": [...]}' | python3 skills/wsr-generator/scripts/wsr_entries.py import
```

Or use a file:

```bash
python3 skills/wsr-generator/scripts/wsr_entries.py import --file entries.json
```

### Step 4: Generate Report

```bash
python3 skills/wsr-generator/scripts/wsr_report.py generate
```

### Step 5: Send Notification

```bash
# Uses default channel from config
python3 skills/wsr-generator/scripts/wsr_notify.py send

# Or specify channel
python3 skills/wsr-generator/scripts/wsr_notify.py send --channel teams
```

## Entry JSON Format

When importing entries, use this JSON structure:

```json
{
  "entries": [
    {
      "title": "Implemented user authentication",
      "status": "Completed",
      "priority": "High",
      "domain": "Development",
      "objective": "Enable secure user login for the application",
      "business_impact": "Users can now securely access their accounts",
      "next_steps": "Add password reset functionality",
      "work_items": [
        {
          "id": 1234,
          "title": "Implement login API",
          "type": "Task",
          "state": "Done"
        }
      ],
      "commits": [
        {
          "sha": "abc123def456",
          "short_sha": "abc123d",
          "subject": "feat: add JWT authentication",
          "author": "user@example.com",
          "date": "2025-12-10",
          "insertions": 150,
          "deletions": 20
        }
      ]
    }
  ]
}
```

### Entry Fields

| Field | Required | Description |
|-------|----------|-------------|
| `title` | Yes | Max 80 chars, action-oriented |
| `status` | Yes | `Completed`, `In Progress`, `Blocked`, `On Hold` |
| `priority` | No | `High`, `Medium`, `Low` (default: Medium) |
| `domain` | No | `Development`, `Architecture`, `Infrastructure`, `Security`, `Documentation`, `Support` |
| `objective` | No | Why this work was undertaken |
| `business_impact` | No | Value delivered to users/business |
| `next_steps` | No | Follow-up actions planned |
| `work_items` | No | Array of linked ADO work items |
| `commits` | No | Array of linked git commits |

## Prerequisites

1. **Azure DevOps configured**: `.ado/config.json` must exist (via azure-devops skill)
2. **Git repository**: Must be inside a git repo with commit history
3. **WSR initialized**: Run `wsr_config.py init` first

## Entry Management

### Add Entry Manually

```bash
python3 skills/wsr-generator/scripts/wsr_entries.py add \
  --title "Implemented new feature" \
  --status Completed \
  --priority High \
  --domain Development \
  --work-items 1234 1235
```

### List Entries

```bash
python3 skills/wsr-generator/scripts/wsr_entries.py list
```

### Remove Entry

```bash
python3 skills/wsr-generator/scripts/wsr_entries.py remove --id abc123
```

### Export Entries

```bash
python3 skills/wsr-generator/scripts/wsr_entries.py export
```

### Clear All Entries

```bash
python3 skills/wsr-generator/scripts/wsr_entries.py clear --confirm
```

## Report Generation

### Standard Report

```bash
python3 skills/wsr-generator/scripts/wsr_report.py generate
```

### Executive Summary

```bash
python3 skills/wsr-generator/scripts/wsr_report.py generate --audience executive
```

### Technical Detail

```bash
python3 skills/wsr-generator/scripts/wsr_report.py generate --audience technical
```

### HTML Format

```bash
python3 skills/wsr-generator/scripts/wsr_report.py generate --format html
```

### Output to Stdout

```bash
python3 skills/wsr-generator/scripts/wsr_report.py generate --stdout
```

## Notifications

Send reports directly to Email, Microsoft Teams, or Slack.

### Quick Send (Default Channel)

```bash
# Uses default_channel from .wsr/notify.json
python3 skills/wsr-generator/scripts/wsr_notify.py send
```

### Send to Specific Channel

```bash
python3 skills/wsr-generator/scripts/wsr_notify.py send --channel teams
python3 skills/wsr-generator/scripts/wsr_notify.py send --channel email
python3 skills/wsr-generator/scripts/wsr_notify.py send --channel slack
```

### Configure Channel

```bash
python3 skills/wsr-generator/scripts/wsr_notify.py configure teams
python3 skills/wsr-generator/scripts/wsr_notify.py configure email
python3 skills/wsr-generator/scripts/wsr_notify.py configure email-cli
```

### Show Configuration

```bash
python3 skills/wsr-generator/scripts/wsr_notify.py show
```

### Default Channel

Set `default_channel` in `.wsr/notify.json`:

```json
{
  "default_channel": "teams",
  ...
}
```

## Status Indicators

Professional Unicode symbols used throughout reports:

| Status | Symbol | Badge |
|--------|--------|-------|
| Completed | ● | `● DONE` |
| In Progress | ◐ | `◐ IN PROGRESS` |
| Blocked | ■ | `■ BLOCKED` |
| On Hold | ○ | `○ ON HOLD` |

| Priority | Symbol | Badge |
|----------|--------|-------|
| High | ▲ | `▲ HIGH` |
| Medium | ● | `● MED` |
| Low | ▽ | `▽ LOW` |

## Audience Levels

| Level | Description | Sections Included |
|-------|-------------|-------------------|
| **executive** | High-level for leadership | Objective, Business Impact, Next Steps |
| **standard** | Balanced for stakeholders | + Solution, Technical Impact |
| **technical** | Detailed for engineering | + All sections, commit details, code stats |

## Directory Structure

```
.wsr/
├── config.json              # WSR configuration
├── notify.json              # Notification settings
├── data/
│   └── 2025-W50-entries.json  # Weekly data
└── reports/
    ├── 2025-W50-draft.md      # Draft reports
    └── 2025-W50-final.md      # Final reports
```

## Configuration

### .wsr/config.json

```json
{
  "version": "2.0",
  "organization": "https://dev.azure.com/myorg",
  "project": "MyProject",
  "output_dir": ".wsr/reports",
  "data_dir": ".wsr/data",
  "git_remote_type": "azure",
  "git_remote_url": "https://dev.azure.com/myorg/MyProject/_git/MyRepo",
  "default_audience": "standard",
  "author_email": "user@example.com"
}
```

### .wsr/notify.json

```json
{
  "default_channel": "teams",
  "teams": {
    "enabled": true,
    "webhook_url": "https://outlook.office.com/webhook/..."
  },
  "email": {
    "enabled": false,
    "smtp_server": "smtp.office365.com",
    "smtp_port": 587,
    "username": "user@company.com",
    "from_address": "user@company.com",
    "to_addresses": ["manager@company.com"]
  }
}
```

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `wsr_config.py` | Configuration management |
| `wsr_entries.py` | Entry management (add, import, list, remove) |
| `wsr_report.py` | Report generation (markdown, HTML) |
| `wsr_notify.py` | Send reports via Email, Teams, Slack |

## Command Reference

### wsr_entries.py

```
Commands:
  add      Add a single entry manually
  import   Bulk import entries from JSON (stdin or file)
  list     List entries for a week
  remove   Remove an entry by ID
  export   Export entries as JSON
  clear    Clear all entries for a week

Options:
  --config, -c    Config file path
  --week, -w      Week ID (YYYY-WNN)
```

### wsr_report.py generate

```
Options:
  --audience, -a    Audience level: executive, standard, technical
  --format, -F      Output format: markdown, html
  --final, -f       Mark as final report
  --output, -o      Custom output file path
  --stdout          Print to stdout instead of file
  --week, -w        Specific week ID (YYYY-WNN)
```

### wsr_notify.py send

```
Options:
  --channel, -ch    Channel: email, email-cli, teams, slack, all
  --audience, -a    Audience level: executive, standard, technical
  --week, -w        Specific week ID (YYYY-WNN)
```

## Example: Full WSR Generation

Here's how Claude should orchestrate a complete WSR:

```bash
# 1. Ensure WSR is initialized
python3 skills/wsr-generator/scripts/wsr_config.py init

# 2. Query completed work items this week
python3 skills/azure-devops/scripts/query-work-items.py --preset completed-this-week

# 3. Get git commits this week
git log --since="Monday" --oneline --author="$(git config user.email)"

# 4. Claude transforms data and imports
# (Claude creates JSON from the above outputs)
echo '{"entries": [...]}' | python3 skills/wsr-generator/scripts/wsr_entries.py import

# 5. Generate report
python3 skills/wsr-generator/scripts/wsr_report.py generate --stdout

# 6. Send to Teams (or default channel)
python3 skills/wsr-generator/scripts/wsr_notify.py send
```

## Troubleshooting

### No entries found
- Run `wsr_entries.py list` to check current entries
- Use `wsr_entries.py import` to add entries from JSON

### Report generation fails
- Check `.wsr/config.json` exists (run `wsr_config.py init`)
- Verify entries exist for the week

### Notification fails
- Run `wsr_notify.py show` to check configuration
- For Teams, verify webhook URL is correct
- For email, check SMTP settings and credentials
