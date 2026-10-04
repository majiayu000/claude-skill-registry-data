---
name: inbox-zero
description: Multi-channel inbox consolidation. Shows all unread items across chat, messages, Wix submissions, notifications, inquiries, and Gmail in one view. Triage, respond, or dismiss. Use when user says "inbox zero", "what's unread", "clear inbox", "catch up", or morning briefing needs inbox status.
user-invocable: true
---

# Inbox Zero - Multi-Channel Triage

Every unread item across every channel in one view. Triage them all, get to zero.

## Trigger Conditions

Auto-fire when:

- User says "inbox zero", "inbox", "what's unread", "clear inbox"
- User says "catch up", "anything new", "what did I miss"
- `/morning` needs an inbox section
- `/client-pulse` reveals unprocessed items

## Step 1: Gather All Channels

Fetch in parallel:

### Unified Inbox

Use `lib/inbox/actions.ts` -> `getUnifiedInbox({ unreadOnly: true })`:

- Aggregates: chat, CRM messages, Wix submissions, notifications
- Returns: source, preview, activity_at, client/event/inquiry links, is_read

### Inbox Stats

Use `lib/inbox/actions.ts` -> `getInboxStats()`:

- Total items (7d window), unread count, breakdown by source

### New Inquiries

Use `lib/inquiries/actions.ts` for status `new` or `awaiting_chef`:

- Unacknowledged inquiries that need first response

### Gmail (if synced)

Use `lib/gmail/actions.ts` for unprocessed emails:

- Classified but not yet acted on

### Triage Suggestions

Use `lib/communication/triage-suggestions.ts`:

- AI-generated suggested actions per item

### Notifications

Use `lib/notifications/actions.ts` for unread notifications:

- System notifications the chef hasn't seen

## Step 2: Display Consolidated Inbox

```
INBOX [timestamp]
━━━━━━━━━━━━━━━━
12 unread items across 4 channels

INQUIRIES (3 new)
  1. Sarah M. (2d) - "Wedding dinner for 20, June 15"
     Via: Take a Chef | -> /acknowledge or /quick-update
  2. Mike R. (4d) - "Anniversary dinner"
     Via: Direct email | -> /acknowledge
  3. Corp Inc (1d) - "Team building for 30"
     Via: Website | -> /acknowledge

MESSAGES (4 unread)
  4. Lisa K. (3h) - "Can we add a gluten-free option?"
     Re: Birthday brunch Jun 16 | -> /quick-update
  5. Tom B. (1d) - "Confirming headcount is 12"
     Re: Corporate lunch Jun 12 | -> /quick-update
  6. Sarah M. (6h) - "Also, can we do passed apps?"
     Re: Wedding Jun 15 | -> /quick-update
  7. Amy L. (2d) - "Thanks for the menu!"
     Re: Dinner party Jun 20 | -> no action needed

NOTIFICATIONS (3)
  8. Payment received: $1,000 from Sarah M.
  9. Event reminder: Corporate lunch in 5 days
  10. Menu approved: Lisa K. birthday brunch

WIX SUBMISSIONS (2)
  11. New contact form: "Looking for chef for July 4th party"
  12. New contact form: "Catering inquiry for office lunch"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUMMARY: 3 inquiries need ack | 3 messages need reply | 2 Wix leads
SUGGESTED: Run /acknowledge to ack all 3 inquiries, then reply to Lisa K. (time-sensitive)
```

## Step 3: Triage Actions

Offer batch operations:

```
What to do?
  [a] Acknowledge all new inquiries (/acknowledge)
  [r] Reply to a specific item (give number)
  [d] Dismiss notifications (mark read)
  [all] Process everything (ack inquiries, mark notifications read)
  [#] Pick specific items by number
```

### Per-item actions:

- **Inquiries**: route to `/acknowledge` or `/quick-update`
- **Messages**: route to `/quick-update` with context pre-filled
- **Notifications**: mark as read, no reply needed
- **Wix submissions**: route to `/acknowledge` (new leads)
- **Gmail**: classify and route (inquiry -> `/acknowledge`, existing client -> `/quick-update`)

## Step 4: Process and Report

After user chooses actions:

```
PROCESSED:
  3 inquiries acknowledged
  1 reply sent (Lisa K. - gluten-free confirmed)
  3 notifications marked read
  2 Wix leads queued for acknowledgment

REMAINING: 3 items (2 Wix leads, 1 message - no action needed)
INBOX STATUS: near-zero
```

## One-Liner Mode

For `/morning` or `/status`:

```
INBOX: 12 unread (3 inquiries, 4 messages, 3 notifs, 2 Wix). Oldest: 4d. Action: /acknowledge first.
```

## Filters

User can filter by channel:

- `/inbox-zero inquiries` - only inquiries
- `/inbox-zero messages` - only client messages
- `/inbox-zero wix` - only Wix submissions

## Key Files

- Unified inbox: `lib/inbox/actions.ts`
- Inbox types: `lib/inbox/types.ts`
- Inquiry actions: `lib/inquiries/actions.ts`
- Inquiry follow-up: `lib/inquiries/follow-up-actions.ts`
- Gmail sync: `lib/gmail/sync.ts`
- Gmail actions: `lib/gmail/actions.ts`
- Gmail classify: `lib/gmail/classify.ts`
- Communication actions: `lib/communication/actions.ts`
- Triage suggestions: `lib/communication/triage-suggestions.ts`
- Quick replies: `lib/communication/quick-reply-actions.ts`
- Notification actions: `lib/notifications/actions.ts`
- Wix submissions: `lib/wix/submission-actions.ts`
- Touchpoints: `lib/clients/touchpoint-actions.ts`

## Rules

- NEVER fabricate inbox items. Only show real data from the database.
- If a channel query fails, show the error for that channel, not empty.
- Inquiries are HIGHEST priority (potential revenue). Always surface first.
- Messages from clients about upcoming events are time-sensitive. Flag them.
- Notifications are lowest priority (informational). Batch-dismiss is fine.
- Cross-link with `/client-pulse` for context on who's been silent.
- After processing, show remaining count. Goal is zero (or near-zero with no-action items).
