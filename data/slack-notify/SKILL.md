---
name: slack-notify
description: Send daily report to Slack workspace via webhook or Bot API
---

# Slack Notify Skill

Sends the daily report to a Slack channel.

## When to Use

Use this skill when you need to:
- Send the generated daily report to Slack
- Notify the team about daily metrics
- Post formatted messages to a Slack channel

## How to Use

```bash
# Send a markdown file to Slack
$CLAUDE_CONFIG_DIR/skills/slack-notify/scripts/send-report.sh "/path/to/report.md"

# Send with custom channel (requires Bot Token)
$CLAUDE_CONFIG_DIR/skills/slack-notify/scripts/send-report.sh "/path/to/report.md" "#daily-reports"
```

### Arguments
- `report_file` (required): Path to the markdown report file
- `channel` (optional): Slack channel to post to (only works with Bot Token, not webhook)

### Prerequisites

Choose one of these authentication methods:

**Option 1: Webhook (Simpler)**
- `SLACK_WEBHOOK_URL` environment variable must be set
- Create an Incoming Webhook at: https://api.slack.com/apps → Your App → Incoming Webhooks

**Option 2: Bot Token (More features)**
- `SLACK_BOT_TOKEN` environment variable must be set (starts with `xoxb-`)
- `SLACK_CHANNEL_ID` environment variable for default channel
- Create a Slack App with `chat:write` scope

## Output

Console output:
```
Sending daily report to Slack...
Report sent successfully!
Message timestamp: 1702656000.000000
```

## Message Format

The script converts the markdown report to Slack Block Kit format:
- Headers become bold section headers
- Tables are preserved with code formatting
- Lists are converted to bullet points
- Key metrics are highlighted

Example Slack message:
```
📊 Daily Data Report - 2024-12-15

*GitHub Repository: vm0-ai/vm0*
• Stars: 1,234 (+12)
• Forks: 56 (+3)

*Website Traffic*
• Visitors: 500
• Pageviews: 1,200

*Code Changes*
• 5 commits by 2 authors
• +150 / -30 lines

📋 View full report: [link]
```

## Error Handling

- **invalid_token**: Check that SLACK_BOT_TOKEN or SLACK_WEBHOOK_URL is set correctly
- **channel_not_found**: The channel doesn't exist or bot is not invited
- **missing_scope**: The bot needs `chat:write` permission
- **rate_limited**: Too many requests, the script will retry automatically
