---
name: slack-search
description: Search and retrieve information from Slack workspace using the slack-cli tool. Use this skill to find messages, get channel history, or search for user posts in Slack.
---

# Slack Search Skill

This skill enables you to search and retrieve information from Slack workspace using the `slack-cli` command-line tool.

## Prerequisites

Before using this skill, ensure:
1. `SLACK_TOKEN` environment variable is set with a valid User OAuth Token (starting with `xoxp-`)
2. The `slack-cli` binary is built and available in PATH

## Available Commands

### 1. Search Messages Across All Channels

Search for messages containing specific keywords across all accessible channels:

```bash
slack-cli search "<query>"
```

**Options:**
- `--sort=timestamp` or `--sort=score`: Sort by timestamp (default) or relevance score
- `--sort-dir=desc` or `--sort-dir=asc`: Sort direction (desc = newest first, default)
- `--count=N`: Number of results to retrieve (default: 20)

**Date Filters (in query):**
- `after:YYYY-MM-DD`: Messages after specified date
- `before:YYYY-MM-DD`: Messages before specified date
- `on:YYYY-MM-DD`: Messages on specific date

**Examples:**
```bash
# Search for error messages
slack-cli search "error"

# Search with date filter
slack-cli search "deployment after:2025-11-01"

# Search with custom sorting and count
slack-cli search "bug" --sort=score --count=50

# Search for multiple terms
slack-cli search "database connection error"
```

### 2. Get Channel Messages

Retrieve the latest messages from a specific channel:

```bash
slack-cli channel <channel-name>
```

**Example:**
```bash
# Get messages from #general channel
slack-cli channel general

# Get messages from #engineering channel
slack-cli channel engineering
```

**Note:** Use the channel name without the `#` symbol.

### 3. Search User Posts

Find all messages posted by a specific user:

```bash
slack-cli user <username>
```

**Example:**
```bash
# Get messages from user "john.doe"
slack-cli user john.doe
```

**Note:** Use the Slack username (not display name).

## Output Format

All commands output results in the following format:

```
Found N messages:
================================================================================

[1] username:
Message text content here
Posted: YYYY-MM-DD HH:MM:SS UTC
Channel: #channel-name

[2] username:
Another message text
Posted: YYYY-MM-DD HH:MM:SS UTC
Channel: #another-channel

================================================================================
```

## Usage Guidelines

### When to Use This Skill

Use this skill when you need to:
- Find specific information mentioned in Slack conversations
- Track discussions about particular topics or issues
- Retrieve historical messages from channels
- Search for messages from specific team members
- Investigate when something was discussed or decided

### Best Practices

1. **Be Specific with Search Terms**: Use precise keywords to get relevant results
2. **Use Date Filters**: When looking for recent or historical information, add date filters
3. **Adjust Result Count**: If you need more context, increase `--count` parameter
4. **Check Multiple Sources**: Try searching by keyword, then verify in specific channels
5. **Handle Token Issues**: If you get "not_allowed_token_type" error, verify you're using a User Token (xoxp-) not a Bot Token (xoxb-)

### Common Use Cases

**Finding Error Reports:**
```bash
slack-cli search "error" --sort=timestamp --sort-dir=desc --count=30
```

**Checking Recent Deployments:**
```bash
slack-cli search "deployed after:2025-11-15"
```

**Getting Team Updates:**
```bash
slack-cli channel team-updates
```

**Finding Specific User's Contributions:**
```bash
slack-cli user jane.smith
```

**Investigating Issues:**
```bash
# First search broadly
slack-cli search "database timeout"

# Then check specific channels
slack-cli channel infrastructure

# Then check who reported it
slack-cli user devops-bot
```

## Error Handling

### Common Errors and Solutions

1. **"SLACK_TOKEN environment variable is not set"**
   - Set the environment variable: `export SLACK_TOKEN=xoxp-your-token`

2. **"not_allowed_token_type"**
   - You're using a Bot Token instead of User Token
   - Create a new User Token with `search:read` scope

3. **"Channel not found"**
   - Verify the channel name is correct (without `#`)
   - Ensure the bot is invited to private channels

4. **"User not found"**
   - Use the Slack username, not display name
   - Check spelling of username

5. **No results returned**
   - Try broader search terms
   - Check if you have access to the channels containing the messages
   - Verify date filters are correct

## Limitations

- **Enterprise Grid**: Results are limited to the connected workspace, not all workspaces in the organization
- **Permissions**: Only searches in channels/conversations the User Token has access to
- **Rate Limits**: Slack API has rate limits; avoid rapid consecutive requests
- **Result Limit**: Maximum results per query is constrained by the `--count` parameter

## Tips for Effective Searching

1. **Use Quotes for Phrases**: `slack-cli search '"exact phrase"'`
2. **Combine Keywords**: Search for multiple relevant terms together
3. **Filter by Date Range**: Narrow down results with `after:` and `before:`
4. **Sort by Relevance**: Use `--sort=score` when keyword matching is more important than recency
5. **Iterate Searches**: Start broad, then refine based on initial results

## Integration with Workflows

This skill works well in combination with other tasks:
- Search Slack → Summarize findings → Create report
- Find error messages → Investigate logs → Propose fixes
- Track feature discussions → Compile requirements → Document decisions
- Monitor team communications → Identify blockers → Suggest actions
