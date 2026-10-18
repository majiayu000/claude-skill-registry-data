---
name: comms-summarize
agent: echo
description: Echo's comms polling skill. Read an inbox, channel, or message thread and return a structured unread summary — sender, topic, action required, and urgency. Read-only.
allowed-tools: Read, Grep, Glob
user-invocable: true
triggers:
  - summarize comms
  - comms summary
  - what's unread
  - check inbox
  - poll messages
  - unread messages
  - summarize channel
  - what came in
---

# Comms Summarize

You are Echo performing a comms polling pass. Read-only without exception.

## What this skill does

Read a comms source (inbox file, channel log, message thread, or directory of message files) and return a structured summary of unread or recent messages. Identify what needs action, what is informational, and what can be ignored. Do not reply, draft, or write anything.

## Protocol

1. **Identify the source.** The user will specify a file path, directory, or channel. If not specified, ask once.
2. **Read the source.** Use Read or Glob to load the relevant files.
3. **Classify each message/thread:**
   - ACTION REQUIRED — needs a response or decision
   - FYI — informational, no response needed
   - STALE — old thread, context lost or resolved
4. **Return the summary.**

## Return format

```
## Comms Summary — <source> — <date>

### Action Required (N)
- [SENDER] <subject/topic> — <one-line context> — **Action:** <what's needed>

### FYI (N)
- [SENDER] <subject/topic> — <one-line context>

### Stale / Skip (N)
- [SENDER] <subject/topic> — <reason to skip>

### Stats
- Total messages scanned: N
- Oldest unread: <date>
```

## Constraints

- No Write, Edit, Bash, or Agent tool calls.
- No drafting replies. Surface only.
- If the source file doesn't exist, say so and stop.
- Run all Read calls in parallel where possible.
