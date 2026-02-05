---
name: linear-manager
description: Create, update, search, and comment on Linear issues. Use for project management and issue tracking during development.
---

# Linear Manager Skill

Manage Linear issues directly from Claude Code using Linear's GraphQL API.

## When to Use

Use this skill when you need to:
- Create Linear issues for bugs or features discovered during coding
- Update issue status when completing work
- Search for existing issues before starting work
- Add comments to track progress
- Link code changes to Linear issues
- Fetch issue details when working on a ticket

## Prerequisites

1. **Linear API key** from https://linear.app/settings/api
2. **API key configured** in `arsenal/.env`:
   ```bash
   LINEAR_API_KEY=lin_api_xxxxxxxxxxxxx
   LINEAR_TEAM_ID=your-team-id  # Optional default team
   ```

## Data Model Quickstart

**ALWAYS run this first** to understand your Linear workspace:

```bash
.claude/skills/linear-manager/scripts/get_teams.sh
```

This shows you:
- All teams in your workspace
- Team IDs (needed for creating issues)
- Team keys (used in issue identifiers like "ENG-123")

## Primary Commands

### Get Issue Details

```bash
# By issue ID (e.g., "ENG-123")
.claude/skills/linear-manager/scripts/get_issue.sh ENG-123

# Returns: title, description, status, assignee, URL, labels, comments
```

### Create Issue

```bash
.claude/skills/linear-manager/scripts/create_issue.sh \
  --title "Fix authentication bug" \
  --description "Users can't log in with OAuth" \
  --team-id "a1b2c3d4-team-uuid" \
  --priority "urgent"

# Optional flags:
#   --priority: none|urgent|high|medium|low (default: none)
#   --status: backlog|todo|in_progress|done|canceled (default: backlog)
#   --assignee-id: user UUID to assign the issue to
```

### Search Issues

```bash
# Search by text
.claude/skills/linear-manager/scripts/search_issues.sh \
  --query "authentication" \
  --limit 10

# Filter by team
.claude/skills/linear-manager/scripts/search_issues.sh \
  --team-id "a1b2c3d4-team-uuid" \
  --status "in_progress"

# Filter by assignee
.claude/skills/linear-manager/scripts/search_issues.sh \
  --assignee-id "user-uuid" \
  --limit 5
```

### Update Issue

```bash
# Update status
.claude/skills/linear-manager/scripts/update_issue.sh \
  --issue-id "ENG-123" \
  --status "done"

# Update multiple fields
.claude/skills/linear-manager/scripts/update_issue.sh \
  --issue-id "ENG-123" \
  --status "in_progress" \
  --priority "high" \
  --title "Updated title"
```

### Add Comment

```bash
.claude/skills/linear-manager/scripts/add_comment.sh \
  --issue-id "ENG-123" \
  --body "Fixed in commit abc123. Ready for review."
```

### Get User Issues

```bash
# Get your assigned issues
.claude/skills/linear-manager/scripts/get_user_issues.sh

# Filter by status
.claude/skills/linear-manager/scripts/get_user_issues.sh --status "in_progress"

# Include archived issues
.claude/skills/linear-manager/scripts/get_user_issues.sh --include-archived
```

### Get Teams

```bash
# List all teams in your workspace
.claude/skills/linear-manager/scripts/get_teams.sh
```

## Integration with Claude Code

**Mandatory workflow:**

1. **Announce usage**: "I'm using the linear-manager skill to..."
2. **Run the command** with appropriate parameters
3. **Report results** back to the user with issue URL and ID

### Example Workflows

#### Creating an Issue for a Bug

```
User: "Create a Linear issue for this Redis timeout bug"

Claude: "I'm using the linear-manager skill to create a Linear issue...

First, let me get your team ID:
.claude/skills/linear-manager/scripts/get_teams.sh

Now creating the issue:
.claude/skills/linear-manager/scripts/create_issue.sh \
  --title "Fix Redis connection timeout in worker" \
  --description "Worker fails to connect to Redis after 30s, blocking message processing" \
  --team-id "abc123" \
  --priority "urgent"

✅ Created issue ENG-789: https://linear.app/team/issue/ENG-789"
```

#### Working on a Linear Ticket

```
User: "/linear-agent ENG-456"

Claude: "I'm using the linear-manager skill to fetch issue details...

.claude/skills/linear-manager/scripts/get_issue.sh ENG-456

The issue is: 'Add retry logic to message processing'
Description: Users report messages getting stuck when external API is down...

Let me search the codebase for the message processing logic..."
```

#### Updating Issue After Completing Work

```
User: "I've finished the implementation. Update the Linear issue to done."

Claude: "I'm using the linear-manager skill to update the issue status...

.claude/skills/linear-manager/scripts/update_issue.sh \
  --issue-id "ENG-456" \
  --status "done"

.claude/skills/linear-manager/scripts/add_comment.sh \
  --issue-id "ENG-456" \
  --body "Implementation completed in PR #123. All tests passing."

✅ Issue ENG-456 marked as done"
```

## Common Patterns

### Before Starting Work
1. Fetch issue details: `get_issue.sh ENG-XXX`
2. Understand requirements from description
3. Update status to "in_progress"

### During Development
1. Add comments for significant progress
2. Update issue if scope changes
3. Link commits with issue ID in commit message

### After Completing Work
1. Update status to "done"
2. Add final comment with PR link
3. Note any follow-up work needed

## Linear GraphQL Schema Notes

**Issue Statuses:**
- `backlog` - Not yet prioritized
- `todo` - Ready to work on
- `in_progress` - Currently being worked on
- `done` - Completed
- `canceled` - Will not be done

**Priority Levels (0-4):**
- `0` - No priority (default)
- `1` - Urgent
- `2` - High
- `3` - Medium
- `4` - Low

**Issue Identifiers:**
- Use team key + number (e.g., "ENG-123") for human-readable IDs
- Use UUID for API operations when needed
- Scripts accept both formats

## Troubleshooting

### "LINEAR_API_KEY not set"
```bash
# Check if key is configured
grep LINEAR_API_KEY arsenal/.env

# If missing, add it:
echo "LINEAR_API_KEY=lin_api_your_key_here" >> arsenal/.env
```

### "Team ID required"
```bash
# Get your team IDs first
.claude/skills/linear-manager/scripts/get_teams.sh

# Then set default team in arsenal/.env
echo "LINEAR_TEAM_ID=your-team-uuid" >> arsenal/.env
```

### "Issue not found"
- Verify issue ID format (e.g., "ENG-123", not "eng-123")
- Check you have access to the issue's team
- Ensure the issue hasn't been deleted

### "Authentication failed"
- Verify API key is correct: https://linear.app/settings/api
- Check API key has proper permissions
- Try regenerating the key if issues persist

## Installation

This skill requires Python 3.x and the `requests` library:

```bash
cd .claude/skills/linear-manager
pip install -r requirements.txt
# OR
python3 -m pip install requests
```

## Safety Notes

✅ **Safe operations:**
- Creating issues (creates new data, doesn't modify existing)
- Reading issue details (read-only)
- Searching (read-only)
- Adding comments (additive, doesn't modify existing data)

⚠️ **Use with care:**
- Updating issues (modifies existing data)
- Changing status (affects team workflow)
- Bulk operations (test with one issue first)

## Quick Reference

```bash
# 🔥 Get started - see your teams
.claude/skills/linear-manager/scripts/get_teams.sh

# 🔥 Fetch issue details
.claude/skills/linear-manager/scripts/get_issue.sh ENG-123

# 🔥 Create new issue
.claude/skills/linear-manager/scripts/create_issue.sh \
  --title "Your title" \
  --team-id "team-uuid"

# 🔥 Search issues
.claude/skills/linear-manager/scripts/search_issues.sh --query "bug"

# 🔥 Update issue status
.claude/skills/linear-manager/scripts/update_issue.sh \
  --issue-id "ENG-123" \
  --status "done"

# 🔥 Add comment
.claude/skills/linear-manager/scripts/add_comment.sh \
  --issue-id "ENG-123" \
  --body "Your comment"

# 🔥 Get my issues
.claude/skills/linear-manager/scripts/get_user_issues.sh
```

## Notes

- All scripts source credentials from `arsenal/.env`
- Scripts print user-friendly output with emojis and formatting
- Error messages include troubleshooting hints
- Issue URLs are always included in output for easy access
- Supports both issue identifiers (e.g., "ENG-123") and UUIDs
