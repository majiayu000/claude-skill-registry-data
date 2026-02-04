---
name: scan-inbox
description: Scan Apple Mail inbox for unread, actionable, and priority messages. Use this when the user asks to check their email, see unread messages, find urgent emails, or triage their inbox. Returns categorized email counts and details from the last 24-48 hours.
allowed-tools: Bash
---

# Scan Inbox

Analyzes your Apple Mail inbox to identify unread, actionable, and priority messages within a specified time range.

## When to Use This Skill

Activate this skill when the user asks questions like:
- "Check my email"
- "What unread emails do I have?"
- "Any urgent emails?"
- "Show me actionable items from my inbox"
- "Triage my email from today"

## What This Skill Does

1. Scans all inbox accounts in Apple Mail
2. Filters messages by time range (default: last 24 hours)
3. Identifies unread messages
4. Detects actionable keywords (deadline, urgent, action required, meeting, request, etc.)
5. Identifies priority/flagged messages
6. Returns structured data with counts and message details

## Instructions

### Step 1: Determine Time Range
Ask the user if they want a specific time range, or use these defaults:
- "Today" or "recent" → 24 hours
- "This week" or "recent days" → 48-72 hours
- Specific request → Honor their time range

### Step 2: Execute the Scan
Run the AppleScript skill using the Bash tool:

\`\`\`bash
osascript .claude/skills/scan-inbox/scripts/scan_inbox.scpt <hours> false
\`\`\`

Parameters:
- `<hours>`: Number of hours to look back (e.g., 24, 48, 72)
- `false`: Set to `true` for priority-only mode

### Step 3: Parse Results
The script returns:
- `success`: boolean (true/false)
- `unreadCount`: Total unread messages
- `actionableCount`: Messages with actionable keywords
- `priorityCount`: Flagged/priority messages
- `unreadList`: Array of unread message details (sender, subject, date, flagged status)
- `actionableList`: Array of actionable messages
- `priorityList`: Array of priority messages

### Step 4: Present Results to User
Format the output in a clear, actionable way:

**Example Response:**
\`\`\`
📬 Inbox Summary (Last 24 Hours)

📊 Overview:
- 38 unread messages
- 0 actionable items
- 0 priority/flagged

📧 Recent Unread:
1. Google - Security alert
2. C# Digest - Newsletter
3. BAC Credomatic - Transaction notification
... (showing top 5-10)

💡 Next Steps:
- No urgent items requiring immediate attention
- Review newsletters when you have time
\`\`\`

### Step 5: Offer Follow-up Actions
Ask if the user wants to:
- See more details about specific emails
- Flag or organize certain messages
- Extract tasks from actionable emails
- Check a different time range

## Actionable Keywords Detected

The skill identifies these keywords in email subjects:
- deadline
- urgent
- action required
- meeting
- request
- please review
- asap
- todo
- action item

## Error Handling

If the script fails:
1. Check Mail automation permissions: System Settings → Privacy & Security → Automation → Terminal/Claude
2. Verify Apple Mail is running
3. Try with a smaller time range if timeout occurs

## Example Usage

**User**: "Check my email from today"

**Claude Response**:
\`\`\`bash
osascript .claude/skills/scan-inbox/scripts/scan_inbox.scpt 24 false
\`\`\`

Then format and present the results to the user.

## Supporting Files

For advanced usage and detailed documentation, see [reference.md](reference.md).

For examples of common use cases, see [examples.md](examples.md).

## Performance

- Typical execution: ~2 seconds
- Max timeout: 30 seconds
- Works with multiple Mail accounts

## Privacy Note

This skill only reads mail metadata (sender, subject, date, flags). It does not access email body content to protect privacy.
