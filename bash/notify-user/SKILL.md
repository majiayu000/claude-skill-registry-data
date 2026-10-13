---
name: notify-user
description: "Sends a Pushover push notification to Matt when Claude is blocked and needs user input to continue working. Use PROACTIVELY when stuck on a decision, missing information, or needing approval during an active task. Do NOT use for routine questions at the end of a task."
disable-model-invocation: true
allowed-tools:
  - Bash(curl:*)
  - Read
---

# Notify User via Pushover

## Purpose

Send a push notification to Matt's phone when Claude is actively working on a task and hits a blocker that requires human input. This lets Matt step away while Claude works, knowing he'll get pinged when needed.

## When to Use

Use this skill when ALL of these are true:
1. You are in the middle of a multi-step task (not just answering a question)
2. You cannot make a reasonable default choice on your own
3. The blocker is genuine -- you need a decision, credentials, clarification, or approval
4. Matt may not be watching the terminal

## When NOT to Use

- Routine end-of-task summaries ("here's what I did, what's next?")
- Questions where a sensible default exists (just pick it and note the choice)
- Simple confirmations that can wait for Matt to check back
- Multiple times in quick succession for the same blocker

## How to Use

Run the script via Bash:

```bash
bash ~/.claude/skills/notify-user/send-pushover.sh "Title" "Message"
```

**Title**: Short label (under 50 chars). Examples:
- "Input Needed: DB Migration"
- "Blocked: API Key Missing"
- "Decision Required: Auth Flow"

**Message**: 1-2 sentences explaining what you need. Be specific enough that Matt knows what to answer when he gets back.

## Example

```bash
bash ~/.claude/skills/notify-user/send-pushover.sh \
  "Decision Needed: Auth Strategy" \
  "Building the login flow. Should I use session-based auth or JWT? This affects the middleware structure so I need to know before continuing."
```

## After Sending

1. Tell the user in the terminal that you sent a notification
2. Continue working on anything you CAN do without the blocked input
3. When the user responds, resume the blocked work
