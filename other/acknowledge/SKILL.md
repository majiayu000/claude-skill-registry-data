---
name: acknowledge
description: Auto-acknowledge new inquiries within minutes. Sends a warm "got it, working on it" response so clients never sit in silence. Use when user says "acknowledge", "ack inquiries", or when morning report shows unacknowledged inquiries.
user-invocable: true
---

# Acknowledge - Inquiry Auto-Ack

Clients should never wonder if their inquiry was received. This skill sends a warm acknowledgment within the 0-72h window.

## Trigger Conditions

Auto-fire when:

- User says "acknowledge", "ack", "acknowledge inquiries"
- `/client-pulse` shows new/unacknowledged inquiries
- Morning report flags silent inquiries

## Step 1: Find Unacknowledged Inquiries

Query for inquiries that:

- Status is `new` or `awaiting_chef`
- Have NOT received any outbound message from the chef
- Were created in the last 7 days (older ones need a different approach)

```bash
curl -s "http://localhost:3000/api/v2/inquiries?status=new,awaiting_chef" \
  -H "Cookie: $(cat .auth/agent-cookie.txt 2>/dev/null || echo '')" \
  2>/dev/null
```

Or check via the database through `lib/inquiries/actions.ts`.

Cross-reference with communication log to find which have zero outbound messages.

## Step 2: Show What Needs Ack

```
UNACKNOWLEDGED INQUIRIES
━━━━━━━━━━━━━━━━━━━━━━━━

1. Sarah M. (2d ago) - "Wedding dinner for 20, June 15"
   Via: Take a Chef | Email: sarah@email.com

2. Mike R. (4d ago) - "Anniversary dinner, looking for private chef"
   Via: Direct email | Email: mike@email.com

3. Corporate Inc. (1d ago) - "Team building cooking event for 30"
   Via: Website form | Email: events@corp.com

Acknowledge all 3? [y/all/pick numbers]
```

## Step 3: Draft Acknowledgments

For each, draft a warm, personal acknowledgment in David's voice:

**Template (adapt per inquiry):**

```
Hey [first name],

Thanks for reaching out! I got your message about the [occasion].
I'm looking at my calendar and will get back to you with
availability and details within [timeframe].

Looking forward to it,
David
```

**Adaptation rules:**

- If they mentioned a specific date, reference it: "the June 15 dinner"
- If they mentioned guest count, acknowledge: "dinner for 20 sounds great"
- If corporate, slightly more formal but still warm
- If referral, mention: "Thanks for thinking of me"
- NEVER promise pricing or availability. Just acknowledge receipt.
- Keep under 4 sentences.

## Step 4: Confirm and Send

Show all drafts:

```
DRAFT ACKNOWLEDGMENTS
━━━━━━━━━━━━━━━━━━━━

1. TO: Sarah M. (sarah@email.com)
   "Hey Sarah, thanks for reaching out! I got your message about
   the wedding dinner for 20 on June 15. I'm looking at my calendar
   and will get back to you with details soon. Looking forward to it!"

2. TO: Mike R. (mike@email.com)
   "Hey Mike, thanks for reaching out about the anniversary dinner!
   Let me check my availability and I'll get back to you shortly
   with some ideas."

3. TO: Corporate Inc. (events@corp.com)
   "Hi there, thanks for reaching out about the team building event
   for 30! I'd love to learn more. I'll follow up soon with some
   options and availability."

Send all? [y/n/edit #]
```

## Step 5: Send and Log

On confirmation:

1. Send via email (`lib/email/send.ts`)
2. Log touchpoint per client (`lib/clients/touchpoint-actions.ts`)
3. Update inquiry status to `awaiting_client` (chef has responded)
4. Log in communication timeline

```
Sent 3 acknowledgments. All inquiries updated to "awaiting client."
Next: follow up with quotes within 48h.
```

## Key Files

- Inquiry actions: `lib/inquiries/actions.ts`
- Follow-up tracking: `lib/inquiries/follow-up-actions.ts`
- Auto-response: `lib/communication/auto-response.ts`
- Email send: `lib/email/send.ts`
- Draft emails: `lib/ai/agent-actions/draft-email-actions.ts`
- Inquiry response: `lib/ai/agent-actions/inquiry-response-actions.ts`
- Touchpoints: `lib/clients/touchpoint-actions.ts`
- Templates: `lib/communication/template-actions.ts`

## Rules

- ALWAYS confirm before sending. Show every draft.
- Never promise pricing, availability, or specifics. Just acknowledge.
- Use David's voice: warm, brief, professional but not corporate.
- If inquiry is older than 7 days, draft a slightly apologetic version: "Sorry for the delayed response..."
- Track which inquiries were acked so we don't double-send.
