---
name: bark-notifier
description: Send a Bark push notification when work is blocked, needs user input, or when all requested tasks are finished. Use by default for these cases unless the user explicitly opts out.
---

# Bark Notifier

## When to Notify

Send a notification when blocked and cannot proceed without user intervention:

- Repeated tool failures (3+ consecutive failures with different approaches)
- Missing required credentials, API keys, or authentication tokens
- File/directory permissions preventing access
- Ambiguous user request requiring clarification before proceeding
- External API/service outage blocking work
- Git conflict or repository state requiring manual resolution

**Do not notify** for:
- Routine errors that can be retried with different approaches
- Missing documentation that can be found by searching
- Normal workflow steps (e.g., "which branch should I use?")

Send a notification when all requested tasks are completed and the user asked for a completion alert.

If the user explicitly opts out (e.g., "no notifications", "don't alert me"), do not send a notification.

## Steps

1) Compose a concise, actionable message that identifies:
   - What is blocking progress
   - What specific action or input is needed from the user

2) For completion alerts, say the work is finished and optionally include the key deliverable or next action.

3) Execute the bundled script to send the notification using an absolute path (do not assume the current working directory). Prefer `$CODEX_HOME` if set; otherwise use the full skill path shown above. If sending fails, retry up to 3 times with exponential backoff. Do not ask the user for confirmation to retry.

```bash
bun "$CODEX_HOME/skills/bark-notifier/scripts/encode-msg.js" "Your concise message here"
```

Example:
```bash
bun "$CODEX_HOME/skills/bark-notifier/scripts/encode-msg.js" "Blocked: Missing API key for OpenAI. Please provide the API key to continue."
```

## Notes

- **Keep messages brief** - Mobile push notifications work best when under 100 characters
- **Never include secrets** in messages (API keys, passwords, tokens)
- **One notification per blocker** - Don't resend unless the user explicitly requests reminders
- **Prerequisites**: `BARK_ENDPOINT` and `BARK_KEY` environment variables must be set; `CODEX_HOME` should be set to the Codex home directory
