---
name: send-letter
description: "Sends an approved letter via Outlook email using MCP integration. Use when Mandy says 'send letter', 'send it', 'email this to', or wants to send correspondence. Requires letter to be approved first."
---

# Send Letter

## Important
- Manual-only. NEVER send without Mandy's explicit confirmation.
- Rejects letters with status "draft" — must be approved first.

## Instructions

### Step 0: Resolve Matter
Follow `_shared/resolve-matter.md`.

### Step 1: Find and Verify Letter
Find letter in `letters/`. Check status in `matter.json` letters array.
If "draft": "This letter hasn't been approved. Run `/approve-letter` first, or say 'approve and send' to do both."

### Step 2: Determine Recipients
- **To:** Check `matter.json` parties array for matching role. If not found: ask Mandy.
- **CC:** Ask Mandy to confirm CC list (client, other solicitors, agent as appropriate).
- **Attachments:** Ask if any documents should be attached.

### Step 3: Confirm
```
"Ready to send:
To: {recipient} ({email})
CC: {cc_list}
Subject: Re: {client} — Claim {claim_number} — {letter_type}
Attachments: {list or 'None'}
Send?"
```

### Step 4: Send or Fallback
If ms365 MCP available: send via Outlook.
If not: "Outlook integration not set up. Letter saved at `matters/{id}/letters/{filename}`. Send manually. To enable: `claude mcp add ms365 -- npx -y @softeria/ms-365-mcp-server --org-mode`"

### Step 5: Update and Commit
Update letter: status "sent", date_sent, sent_via ("email" or "manual").
Update index. Log. Commit.
