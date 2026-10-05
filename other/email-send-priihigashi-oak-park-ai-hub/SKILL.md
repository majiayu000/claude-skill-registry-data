---
name: email-send
description: Actually SEND an email (not draft). Use when Priscila asks to email someone or when a skill/workflow needs real email delivery. Do not use for drafts — use Gmail MCP create_draft directly.
---

# Email Send — 3 Routes

## When to use
- "Send an email to X", "email Y about Z"
- Automated notifications from skills
- Matt/Mike client communication

## When NOT to use
- Just drafting — use `mcp__claude_ai_Gmail__gmail_create_draft` directly (needs ToolSearch load first)
- Gmail filter creation — use Python Gmail API (see CLAUDE.md Gmail filter section)

## Gmail MCP CANNOT send
Gmail MCP has `create_draft` only. No `send` tool exists. To actually deliver: Route B or Route C.

## 3 Routes

### Route A — DRAFT ONLY
1. Load schema: `ToolSearch("select:mcp__claude_ai_Gmail__gmail_create_draft")`
2. Call `mcp__claude_ai_Gmail__gmail_create_draft` with {to, subject, body}
3. Priscila clicks Send in Gmail

### Route B — GitHub Actions (PREFERRED for real sends)
```bash
~/bin/gh workflow run send_email.yml \
  --repo priihigashi/oak-park-ai-hub \
  -f to="recipient@example.com" \
  -f subject="Subject here" \
  -f body="Body here"
```
- Uses `PRI_OP_GMAIL_APP_PASSWORD` secret (already set)
- Actually delivers via SMTP
- Same pattern as `4am_agent.yml`
- Source: `priihigashi/oak-park-ai-hub/.github/workflows/send_email.yml`

### Route C — Local SMTP (fallback if workflow down)
```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
msg = MIMEMultipart()
msg['From'] = 'priscila@oakpark-construction.com'
msg['To'] = to
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
    s.login('priscila@oakpark-construction.com', APP_PASSWORD)
    s.send_message(msg)
```
- App password: `PRI_OP_GMAIL_APP_PASSWORD` (GitHub secret). Locally in `~/ClaudeWorkspace/.env` if set.
- Full working example: `~/.claude/scripts/eod_checker.py` (uses Gmail API build route, same pattern)

## McFolling inbox (Airbnb / Maya)
- Account: configured by `MCFOLLING_EMAIL`
- Local token: `~/ClaudeWorkspace/Credentials/mcfolling_token.json`
- GitHub secret: `MCFOLLING_TOKEN`
- Has `gmail.send` scope — use Gmail API directly for this inbox

## Confirmation rule
After send, report: `✅ Email sent via <route> to <recipient>` — only after verifying workflow succeeded / SMTP returned 250.
