---
name: claude-mail-bridge-init
description: Use when Claude Mail Bridge is installed (presence.json exists). Provides behavior guidelines for remote collaboration scenarios, including presence detection and MCP usage.
---

# Claude Mail Bridge Initial Behavior Guidelines

## Overview

This skill defines the basic behavior guidelines for Claude Mail Bridge plugin. When the plugin configuration is detected, AI should follow these guidelines for remote collaboration.

## Quick Start

Key MCP tools for remote control:
1. Read user presence: mcp__presence_system__get_presence
2. Set user presence: mcp__presence_system__set_presence
3. Control DND mode: mcp__presence_system__set_dnd_mode
4. Communicate with user: mcp__email_system__mail_user_and_wait
5. Communicate with teammates: mcp__email_system__mail_teammates

## Status Detection

### Reading User Status

Use `mcp__presence_system__get_presence` tool to read the current user status:

```bash
# Return values
"online"  # User is at terminal, can communicate directly
"away"    # User is not at terminal, need to communicate via email
```

### Setting User Status

Use `mcp__presence_system__set_presence` when you have clear knowledge of the user's status that differs from the current presence state:

```bash
mcp__presence_system__set_presence(mode="away", _init_skill_invoked=True)   # Set to away
mcp__presence_system__set_presence(mode="online", _init_skill_invoked=True)  # Set to online
```

**Note**: Only set user status when you are certain of the actual state, such as:
- User explicitly states they are leaving or returning
  - Examples (English): "I'm leaving", "I'm back", "I'm here", "I'm at the terminal"
  - Examples (中文): "我要走了", "我回来了", "我在", "我在电脑前"
- Received `[Remote System : Wakeup]` message
- System explicitly notifies of user status change

Do not set status based on guesses or assumptions.

## Online Mode

When user status is `online`:
- Can communicate directly in terminal
- No need to communicate via email
- Can ask questions or confirm directly without blocking
- ✅ AskUserQuestion and interactive prompts work normally

## Away Mode

When user status is `away`:
- Use email tools to communicate with user (like next steps, progress report, important decision)
- You MUST use `mail_user_and_wait` to report your movements or thoughts or questions before STOP.
- ❌ DO NOT use `AskUserQuestion` tool (use `mail_user_and_wait` instead). This restriction ONLY applies in away mode; when user is online, `AskUserQuestion` works normally.
- Keep email with user until one of the following conditions happen

### Email With User Stopping Conditions

**Continue sending emails UNTIL one of these conditions is met:**

1. **Explicit stop instruction** - User explicitly indicates they are leaving or stopping
   - Examples: "stop", "够了", "不用了"
   - No further emails needed for this stop

2. **No response timeout** - User does not respond to a `question` type email within the timeout period
    - No further emails needed for this stop

3. **User becomes online** - Presence status changes from `away` to `online`
   - User can now see output directly in terminal
   - No further emails needed for this stop

**Important:** When receiving a user reply, do NOT assume the session is over unless the reply explicitly indicates stopping. Continue sending emails as needed for ongoing work.

## Email MCP Tools

### mail_user_and_wait - Communicate with User

Use this tool to ask questions or report progress to user.

**⚠️ REQUIRED PARAMETERS:**
All parameters below MUST be provided when calling this tool:
- `subject`: Short summary for email subject
- `background`: Context and progress status
- `content`: The question or conclusion message
- `type`: Must be `"question"` or `"conclusion"`
- `timeout_minutes`: Keep the default value except for specified instructions
- `attachments`: List of file paths to attach (optional, default: `[]`)
  - Max 15MB per file
  - Allowed types:
    - Text/code: `.txt`, `.md`, `.py`, `.js`, `.json`, `.csv`, `.yaml`, `.yml`, `.xml`, `.html`, `.css`, `.sql`, `.sh`
    - Images: `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.webp`, `.bmp`
    - PDFs: `.pdf`
    - Archives: `.zip`, `.tar`, `.gz`, `.7z`, `.bz2`, `.xz`
    - Documents: `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx`
  - Example: `["/path/to/report.pdf", "/var/log/output.txt"]`
- `_init_skill_invoked`: MUST be set to `True` when calling from FastMCP

**When to use:**
- User is 'away'
- User explicitly asks to communicate via email
- Receiving `[Remote System : Wakeup]` message

### mail_teammates - Communicate with Teammates

⚠️ CRITICAL: You MUST invoke /claude-mail-bridge-team_rules before using this tool.

This tool is for emailing teammates. Due to privacy concerns, strict rules apply.

**When to use:**
- User explicitly mentions teammate name/email
- User provides specific content to send
- After getting explicit user approval through /claude-mail-bridge-team_rules

## Email Format (Auto-Generated by System)

The system automatically generates emails with this format:

**Subject:**
```
🎫 [CMB] [machine] [tmux: session] ❓ Question #ticket_xxx# (title)
🎫 [CMB] [machine] [tmux: session] 🏁 Conclusion #ticket_xxx# (title)
```

**Body:**
```
📝 Background
{background content}

❓ Question / 🏁 Conclusion
{content}

---
{footer}
```

**Note:** Emoji prefixes (🎫, 📝, ❓, 🏁) are auto-added by system. AI-provided `background` and `content` are encouraged to use emoji and structured format, but not enforced.

## Prohibited Behaviors

**Absolutely prohibited:**
1. Prohibited from guessing input before receiving permission or user reply
2. Prohibited from bypassing security mechanisms
3. Prohibited from executing sensitive operations when user source is unknown
4. Prohibited from waiting indefinitely for user input when presence status is `away`

**Note**:
- Permission requests are handled automatically by the system, AI does not need to intervene
- When encountering permission suspension, just wait for automatic system recovery

## DND Mode

`mcp__presence_system__set_dnd_mode` - Control permission request behavior:
- **off**: Email notification (default)
- **on**: Silent block
- **fixed**: Silent block with duration, then auto-off
- **auto**: Silent when online, email when away

⚠️ **CRITICAL**: ONLY invoke when user explicitly specifies. Never guess.
