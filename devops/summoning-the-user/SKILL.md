---
name: summoning-the-user
description: Use when an agent encounters a blocking decision or when proceeding without user input could lead to wasted work - helps Claude determine when to block and request user input versus making reasonable assumptions
---

# Summoning the User

## Overview

Help Claude and subagents identify when to block and request user input rather than proceeding with assumptions or guesses.

**Core principle:** When uncertain, assess the risk. High-risk decisions require summoning the user. Low-risk decisions can proceed with reasonable defaults.

**Announce at start:** "I'm using the summoning-the-user skill to determine if I need your input before proceeding."

## When to Use This Skill

Use this skill when:
- You encounter a blocking decision mid-execution
- Proceeding without user input could lead to wasted work or incorrect implementation

**Special note for subagents:** If you're running in the background, default to summoning for anything uncertain. The user isn't watching, so making wrong assumptions wastes their time.

## Decision Framework: Should I Summon?

### SUMMON (High Risk - Block and Wait)

**You MUST summon the user when:**
- Multiple valid implementation paths exist, no clear "right" answer
- Decision affects security, data integrity, or user privacy
- Requirements are ambiguous or contradictory
- You're about to make an assumption that could waste significant work if wrong
- The choice has architectural implications (hard to change later)
- You don't have enough context about user's actual needs

### PROCEED (Low Risk - Make Reasonable Choice)

**You can proceed without summoning when:**
- One clear best practice or standard approach exists
- It's a minor implementation detail (variable name, code style)
- Decision is easily reversible
- You're following established patterns in the codebase
- User has already provided sufficient context

## How to Summon Effectively

When you've determined summoning is needed, follow this process:

### 1. Send External Notification

**First time:** Ask user which notification method they prefer.

**Check user preference, then use one of:**

**Option A: terminal-notifier (macOS - requires installation)**

```bash
# Check if installed
which terminal-notifier

# If not installed, install via Homebrew
brew install terminal-notifier

# Get terminal bundle ID
case "$TERM_PROGRAM" in
  "iTerm.app") BUNDLE_ID="com.googlecode.iterm2" ;;
  "Apple_Terminal") BUNDLE_ID="com.apple.Terminal" ;;
  "WezTerm") BUNDLE_ID="com.github.wez.wezterm" ;;
  "Ghostty") BUNDLE_ID="com.mitchellh.ghostty" ;;
  "Warp") BUNDLE_ID="dev.warp.Warp-Stable" ;;
  *) BUNDLE_ID="com.apple.Terminal" ;;
esac

# Send notification that activates terminal on click
terminal-notifier -message "🤖 Claude needs your input" -title "Claude Code" -activate "$BUNDLE_ID"
```

**Notes:**
- Requires `terminal-notifier` (install via `brew install terminal-notifier`)
- Clicking notification focuses the terminal application
- Auto-detects terminal type via `$TERM_PROGRAM`
- Works with iTerm2, Terminal.app, Ghostty, WezTerm, Warp

**Option B: OSA Script (macOS - no installation, basic)**

```bash
TERMINAL_APP="${TERM_PROGRAM:-Terminal}"
osascript -e 'display notification "🤖 Claude needs your input" with title "Claude Code"' && \
osascript -e "tell application \"$TERMINAL_APP\" to activate"
```

**Notes:**
- No installation required but less reliable
- Activates terminal immediately (not on click)
- May open Script Editor on notification click
- Consider using terminal-notifier or Slack CLI instead

**Option C: Slack CLI**
- Check if installed: `slack version`
- If not installed: Follow https://docs.slack.dev/tools/slack-cli/guides/installing-the-slack-cli-for-mac-and-linux
- Send notification: `slack chat send --channel @username --text "Claude needs your input"`

### 2. Use AskUserQuestion Tool

- Creates UI prompt that demands attention
- Provides structured options (prevents vague responses)
- Forces explicit choice before proceeding

### 3. Be Explicit About Blocking

- State clearly: "I need your input before proceeding"
- Explain WHY you're blocked (what decision/ambiguity you're facing)
- Don't hide the question in lots of other text

### 4. Provide Context

- Briefly explain what you were doing when you got blocked
- State what information you need
- Explain the consequences of different choices if relevant

## Example

```
I'm blocked and need your input.

I was implementing the user authentication system and encountered
an ambiguity: should failed login attempts be logged with the
username included (better for security auditing but potential
privacy concern) or without (more private but harder to trace
attack patterns)?

[Sends OSA notification or Slack message]
[Uses AskUserQuestion with structured options]
```

## Key Principles

| Principle | Application |
|-----------|-------------|
| **Assess risk first** | Use the decision framework before acting |
| **Default to summoning when uncertain** | Especially for background agents |
| **Always send external notification** | User may not be watching terminal |
| **Use AskUserQuestion tool** | Structured choices get better responses |
| **Be explicit about blocking** | Don't hide that you're waiting |
| **Provide context** | Help user understand why you need input |

## Anti-Patterns

**DON'T:**
- Summon for trivial decisions you can make yourself
- Proceed with high-risk assumptions to "save time"
- Ask questions without sending external notification
- Hide questions in verbose output
- Make the user guess what you need

**DO:**
- Assess risk using the framework
- Send notification before asking
- Be clear and concise about what you need
- Use structured questions (AskUserQuestion)
- Explain the stakes of the decision
