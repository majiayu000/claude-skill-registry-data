---
name: slack-markdown-formatter
description: This skill should be used when users request messages, notifications, or content formatted for Slack. Use this skill when the user asks to write, draft, format, or compose messages specifically for Slack, as Slack uses "mrkdwn" which differs from standard markdown. Also use when users mention Slack Block Kit or rich message formatting for Slack.
---

# Slack Markdown Formatter

## Overview

Slack uses its own markdown variant called "mrkdwn" which differs significantly from standard markdown. This skill provides the correct syntax and best practices for formatting messages that will be displayed properly in Slack.

## When to Use This Skill

Use this skill when:
- User explicitly asks to format a message for Slack
- User requests Slack notifications or Slack messages
- User mentions Slack Block Kit or rich Slack messages
- Converting existing markdown content to Slack format
- User asks about Slack-specific formatting like mentions or channel links

## Core Differences from Standard Markdown

Slack's mrkdwn is NOT standard markdown. Key differences include:

### Text Formatting

**Bold:**
- Standard markdown: `**bold**` or `__bold__`
- Slack: `*bold*` (single asterisks)

**Italic:**
- Standard markdown: `*italic*` or `_italic_`
- Slack: `_italic_` (underscores only)

**Strikethrough:**
- Standard markdown: `~~strikethrough~~`
- Slack: `~strikethrough~` (single tildes)

**Code:**
- Standard markdown: `` `code` `` (backticks)
- Slack: `` `code` `` (backticks - same as standard)

**Code blocks:**
- Standard markdown: ` ```language\ncode\n``` `
- Slack: ` ```\ncode\n``` ` (backticks work, but no language highlighting syntax)

**Blockquotes:**
- Standard markdown: `> quote`
- Slack: `> quote` or `>>> multi-line quote` (same, with special multi-line variant)

### Links

**Standard markdown:**
```
[link text](https://example.com)
```

**Slack format:**
```
<https://example.com|link text>
```

**Auto-linking:**
```
<https://example.com>
```

### Lists

**Unordered lists:**
- Standard markdown: `- item` or `* item`
- Slack: Both work, but formatting may vary

**Ordered lists:**
- Standard markdown: `1. item`
- Slack: Limited support, often better to use bullet points

### Slack-Specific Features

**User mentions:**
```
<@U12345678>  # Mention user by ID
<@username>   # May work in some contexts
```

**Channel mentions:**
```
<#C12345678>  # Link to channel by ID
<#C12345678|channel-name>  # With display name
```

**Special mentions:**
```
<!here>      # Notify active users in channel
<!channel>   # Notify all channel members
<!everyone>  # Notify all workspace members (use sparingly)
```

**Date formatting:**
```
<!date^1392734382^{date_short}|Feb 18, 2014>
<!date^1392734382^{date_num} {time_secs}>
```

## Unsupported Features

The following standard markdown features DO NOT work in Slack:

- Headings (`#`, `##`, etc.) - Not supported
- Tables - Not supported in mrkdwn
- HTML tags - Not supported
- Nested formatting (e.g., `*bold _and italic_*`)
- Image embedding with `![alt](url)` syntax
- Footnotes
- Task lists with `[ ]` and `[x]`

## Block Kit for Rich Messages

For programmatic message formatting or complex layouts, use Slack's Block Kit instead of mrkdwn. Block Kit provides:

- Structured layouts with sections, dividers, and contexts
- Interactive elements (buttons, select menus, date pickers)
- Rich text blocks with more formatting options
- Images, file attachments, and media

When users need rich formatting, interactive elements, or structured layouts, recommend using Block Kit and reference the Block Kit Builder tool at `https://api.slack.com/block-kit/building`.

Block Kit messages can embed mrkdwn text in specific text fields using:
```json
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "Your *formatted* text here"
  }
}
```

## Workflow for Formatting Slack Messages

### Step 1: Identify the Context
- Is this a simple text message or needs Block Kit?
- Does it need mentions, links, or special formatting?
- Is it user-to-user chat or bot/webhook message?

### Step 2: Apply Slack-Specific Syntax
- Replace `**bold**` with `*bold*`
- Replace `*italic*` with `_italic_`
- Convert standard markdown links to `<url|text>` format
- Add Slack mentions using `<@user>` or `<#channel>` format
- Remove unsupported features (headings, tables, etc.)

### Step 3: Consider Context-Specific Formatting
- For notifications: Keep concise, use <!here> or <!channel> appropriately
- For documentation: Use code blocks with ```
- For structured data: Consider Block Kit instead

### Step 4: Test and Validate
- Verify all formatting renders correctly
- Check that mentions and channel links use correct IDs
- Ensure no standard markdown syntax remains

## Examples

### Simple Message

**User request:** "Format this for Slack: Check out **this article** on _productivity_"

**Slack formatted:**
```
Check out *this article* on _productivity_
```

### Message with Link

**User request:** "Format for Slack: See our [documentation](https://example.com/docs)"

**Slack formatted:**
```
See our <https://example.com/docs|documentation>
```

### Notification Message

**User request:** "Create a Slack notification about deployment"

**Slack formatted:**
```
<!here> :rocket: *Deployment Update*

Production deployment completed successfully!

• Version: v2.3.1
• Environment: Production
• Status: :white_check_mark: Success

<https://github.com/org/repo/releases/v2.3.1|View Release Notes>
```

### Code Block

**User request:** "Share this Python code in Slack"

**Slack formatted:**
```
Here's the updated function:
```
def process_data(items):
    return [item.strip() for item in items]
```
```

## References

For comprehensive details on Slack formatting differences, syntax tables, and advanced features, refer to:

- `references/slack-mrkdwn-guide.md` - Complete syntax comparison and best practices
- Official Slack documentation: https://api.slack.com/reference/surfaces/formatting
- Block Kit Builder: https://api.slack.com/block-kit/building

## Resources

### references/

- **slack-mrkdwn-guide.md** - Detailed syntax tables comparing Slack mrkdwn to standard markdown, with comprehensive examples and edge cases
