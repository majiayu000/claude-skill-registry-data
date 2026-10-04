---
name: gmail-integration
description: Use when sending, reading, or labeling emails via Gmail ג€” drafts, threads, attachments, label-based CRM routing. Covers the Gmail MCP server and any email-based agent flow.
---

# Gmail Integration skill

## When to invoke

- Touching `src/integrations/gmail/` or `src/tools/send-email.ts`
- Customer-facing email reply flow (Customer Service agent)
- Lead intake from email source
- Document attachments arriving by email ג†’ routing to classification

## Available MCP tools

`create_draft`, `list_drafts`, `search_threads`, `get_thread`, `label_thread`, `label_message`, `unlabel_*`, `create_label`, `update_label`, `delete_label`, `list_labels`.

**Note**: there is no direct `send` ג€” always create draft then have a human/approval flow send it, OR send via our own Gmail client wrapper (`src/integrations/gmail/client.ts`).

## Hard rules

1. **Customer-facing body must be in Hebrew** (RTL, professional warm tone)
2. **Subject line in Hebrew** for Israeli clients; English only for vendor/internal
3. **Never auto-send** financial advice ג€” create draft, escalate to advisor
4. **Always log** outgoing mail to CRM as activity
5. **Preserve thread context** ג€” always reply via `get_thread` first, never start a new thread for an existing conversation
6. **Attachments**: scan and classify (`classify_document`) before storing in Drive

## Label conventions

- `Lead/New` ג€” incoming lead, before triage
- `Lead/Qualified` ג€” sales agent picked up
- `Customer/Active` ג€” existing customer thread
- `Action/Awaiting-Docs` ג€” referent agent waiting on customer
- `Compliance/Hold` ג€” escalated, do not auto-respond

## Templates location

Hebrew email templates live in `src/agents/customer-service/templates/email/`. Always reuse ג€” do not generate from scratch on every send.

## Error handling

Gmail API failure ג†’ retry once with exponential backoff ג†’ fall back to WhatsApp if customer has opted in ג†’ escalate to human if both fail.