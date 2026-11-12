---
name: email
description: Use when the user wants to send emails, run an email campaign, do cold outreach by email, or log sent emails
---

# /email: cold email with a paper trail

Needs a Gmail connector or MCP.

1. Parse what the user gives you (a profile, a post, an address, a campaign name).
2. Draft: a specific subject that references their work; 4 to 6 sentences: who you are, why them, ONE proof point from hot.md's "Strongest signals", one clear ask. Peer to peer. No filler ("excited to", "passionate about") and no em dashes.
3. Show To / Subject / Body and ask "Send this?" Never send without a yes.
4. On yes, send (or create a draft) and append to `personal/outreach/sent_log.md`:
   `| Date | To | Subject | Campaign | Status | Notes |`
5. Campaigns also get a line in `personal/outreach/campaigns/<date>-<name>.md`.
