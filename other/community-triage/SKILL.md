---
name: community-triage
description: Classify creator community comments, DMs, replies, member posts, and fan feedback by intent, urgency, sentiment, risk, owner, and next action. Use when Codex is asked to triage social comments, creator DMs, Discord or community posts, fan replies, audience questions, moderation queues, engagement backlogs, or community feedback packets for review.
license: MIT
---

# Community Triage

## Core Workflow

1. Identify the source, audience context, message text, public/private status,
   platform, thread context, requested action, and available policy or brand
   guidance.
2. Classify each item by intent, urgency, sentiment, risk, owner, and next
   action.
3. Separate audience-facing reply candidates from internal notes, moderation
   questions, escalation needs, and missing context.
4. Flag items that need human review before response, removal, escalation,
   sponsor visibility, refund/account support, legal/compliance review, or
   crisis handling.
5. Draft a triage table and summary. Use `reply-drafting` only for reviewed
   response drafts after triage is clear.
6. Keep all community, social, CRM, support, moderation, publishing, and member
   systems read-only unless the user approves a specific action.

## Classification Fields

- Channel or source
- Message summary
- Intent
- Sentiment
- Urgency
- Risk level
- Suggested owner
- Next action
- Public reply candidate
- Private/internal note
- Missing context
- Escalation reason

## Safety Rules

- Do not send replies, delete comments, ban users, mute users, approve members,
  change roles, publish posts, or update community tools without explicit
  approval.
- Do not invent audience quotes, identity, sentiment, member status, threats,
  screenshots, policy violations, metrics, or relationship history.
- Escalate harassment, threats, self-harm, minors, doxxing, hate, legal claims,
  privacy issues, payment/account issues, sponsor conflicts, and crisis or
  reputation risks.
- Verify current platform policy only when giving platform-specific tactical
  guidance.

## Deliverable Shape

For community triage, provide:

- Triage summary
- Message table
- Priority queue
- Draft reply candidates
- Escalation list
- Missing context
- Review owner
- Approval status

## References

- Read `references/community-triage-checklist.md` when preparing a creator
  community triage table or priority queue.
