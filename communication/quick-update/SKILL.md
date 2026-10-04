---
name: quick-update
description: Send a one-liner status update to a client. Picks the right channel, drafts in David's voice, sends via Remy. Use when user says "tell [client]", "update [client]", "let them know", or wants to break silence with a client.
user-invocable: true
---

# Quick Update

One-liner status update to any client. Breaks silence fast.

## Trigger Conditions

Auto-fire when:

- User says "tell Sarah...", "update Mike...", "let [client] know..."
- User wants to send a quick status to a client
- After `/client-pulse` shows someone critical

## Usage

```
/quick-update Sarah - menu is almost ready, sending tomorrow
/quick-update Mike R. - confirmed April 15, will follow up with details
/quick-update [client name] - [message]
```

## Step 1: Identify Client

Parse the client name from the command. Search for them:

```bash
curl -s "http://localhost:3000/api/v2/clients?search=[name]" \
  -H "Cookie: $(cat .auth/agent-cookie.txt 2>/dev/null || echo '')" \
  2>/dev/null
```

If ambiguous (multiple matches), ask which one. If not found, say so.

## Step 2: Determine Channel

Check client's preferred contact method from their profile:

- `preferred_contact_method` field on client record
- If not set, default to email
- Channels: email, SMS (Twilio), portal message

## Step 3: Draft Message

Transform the user's intent into a natural message following David's voice:

**Rules for David's email voice (from memory):**

- No AI formatting, no bold headers, no bullet points
- No negative framing of client requests
- Keep it natural and short
- Treat dish lists as references, not demands
- After sign-off, plain text only

**Example transforms:**

- User: "menu is almost ready" -> "Hey Sarah, just wanted to let you know the menu is coming together nicely. I'll send it over tomorrow for your review."
- User: "confirmed for April 15" -> "Hey Mike, all confirmed for April 15! I'll follow up soon with the full details."

## Step 4: Confirm and Send

Show the drafted message to the user:

```
TO: Sarah M. (sarah@email.com)
VIA: email
DRAFT:
  Hey Sarah, just wanted to let you know the menu is coming
  together nicely. I'll send it over tomorrow for your review.

Send? [y/n]
```

Wait for confirmation. Then send via the appropriate channel:

- Email: use `lib/email/send.ts` or Remy email actions
- SMS: use `lib/communication/twilio-webhook.ts`
- Portal: use `lib/communication/actions.ts`

Log the touchpoint via `lib/clients/touchpoint-actions.ts`.

## Step 5: Confirm Delivery

```
Sent to Sarah M. via email. Touchpoint logged.
```

## Key Files

- Email sending: `lib/email/send.ts`
- Draft emails: `lib/ai/agent-actions/draft-email-actions.ts`
- Remy email: `lib/ai/remy-email-actions.ts`
- Quick replies: `lib/communication/quick-reply-actions.ts`
- Touchpoints: `lib/clients/touchpoint-actions.ts`
- Templates: `lib/communication/template-actions.ts`
- Client lookup: `lib/clients/actions.ts`

## Rules

- ALWAYS confirm before sending. Never auto-send.
- Use David's natural voice. No corporate tone.
- Log every touchpoint. This is how we track silence.
- If client has no email/phone, say so and suggest portal.
