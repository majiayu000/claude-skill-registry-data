---
name: resend
description: Use when working with Resend email platform - routes to the template-management sub-skill and points to the Resend docs for sending and receiving emails.
---

# Resend

## Overview

Resend is an email platform for developers. This skill routes to feature-specific sub-skills.

## Sub-Skills

| Feature | Skill | Use When |
|---------|-------|----------|
| **Email templates** | `resend-templates` | Creating, updating, publishing, and managing reusable email templates via API |

## Quick Routing

**Need to manage templates (create/update/publish/delete)?** Use `resend-templates` skill
- Full template lifecycle management via API
- Variable syntax, constraints, reserved names
- Draft vs published state, version history

**Sending emails, receiving inbound emails, or an AI agent inbox?** No dedicated skill. Use the Resend docs:
- Sending (single and batch): https://resend.com/docs/api-reference/emails/send-email
- Receiving (inbound domain, `email.received` webhook): https://resend.com/docs/dashboard/receiving/introduction
- Untrusted inbound content that triggers actions (refunds, database changes, forwarding) needs input validation and a trusted-sender allowlist before anything acts on it
- Batch sending does not support attachments or scheduling, so use single sends when forwarding with attachments

**Marketing emails or newsletters?** Use [Resend Broadcasts](https://resend.com/broadcasts)
- Marketing campaigns to large subscriber lists with unsubscribe links and engagement tracking should use Resend Broadcasts, not batch sending.

## Common Setup

Store the API key in an environment variable:
```bash
export RESEND_API_KEY=re_xxxxxxxxx
```

## Resources

- [Resend Documentation](https://resend.com/docs)
- [API Reference](https://resend.com/docs/api-reference)
- [Dashboard](https://resend.com/emails)
