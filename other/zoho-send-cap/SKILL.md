---
name: zoho-send-cap
description: A Claude Code PreToolUse hook that hard-caps emails sent through the Zoho Mail MCP (default 10 per hour, 25 per day, 90 seconds apart, scheduled sends counted at their scheduled time) and refuses the tool call when a send would break the cap — so an agent can't get your mailbox blocked by Zoho for bursty sending. Use when you send email from agents via Zoho, say "don't let it spam", "rate-limit my outbound", or after Zoho has blocked your outgoing mail once.
---

# zoho-send-cap (PreToolUse hook)

Zoho blocks **all** outgoing mail for an account that sends in bursts — in practice ~50
sends in 45 minutes was enough — and while blocked nothing goes out, replies included. The
block notice tends to land in Spam. A cap written in a project note gets skipped by the next
session that never loads that note, so the cap lives in a global hook and **refuses the
send** instead of advising against it.

## Install

1. Copy `hooks/zoho_send_cap.py` to `~/.claude/hooks/zoho_send_cap.py`.
2. Add to `~/.claude/settings.json` (adjust the matcher to your Zoho MCP server's name):

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "mcp__zoho-mail__ZohoMail_send.*",
        "hooks": [ { "type": "command",
                     "command": "python3 ~/.claude/hooks/zoho_send_cap.py",
                     "timeout": 10 } ] }
    ]
  }
}
```

## What it does

- Counts every `ZohoMail_sendEmail` / `ZohoMail_sendReplyEmail` call that is not a draft or
  template, into a ledger at `~/.claude/state/zoho_sends.jsonl` (override with
  `ZOHO_SEND_LEDGER`). Each line: `{"t": epoch, "to", "subject"}`. The file is locked, so
  parallel sessions share one count.
- **A scheduled send counts at its scheduled time** (`isSchedule` + `scheduleType`/
  `scheduleTime`/`timeZone`), so scheduling 30 emails for tomorrow morning is caught too.
- Denies with a reason when the send would exceed any rolling window in `CAPS` (default
  10/hour, 25/24h) or land within `MIN_GAP` (90s) of another send. The agent sees the reason
  and can schedule the message later instead.
- Edit `CAPS` and `MIN_GAP` at the top of the script to taste.

## Rules for the agent

- Never raise the cap or route around the hook (another mail client, the raw REST API).
  Those sends are invisible to the ledger and still count at Zoho.
- Batches belong on a bulk email provider; the mailbox is for one-to-one mail.
- Before scheduling a batch, read the ledger to see which slots other sessions already hold.
