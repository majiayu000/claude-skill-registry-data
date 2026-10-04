---
name: client-pulse
description: Who is waiting on you? Shows all clients needing a response, ranked by urgency and wait time. Use when user says "who's waiting", "client pulse", "anyone in the dark", "silence check", or morning briefing needs communication status.
user-invocable: true
---

# Client Pulse

Shows every client waiting on the chef, ranked by urgency. Stops the silence bleeding.

## Trigger Conditions

Auto-fire when:

- User says "who's waiting", "anyone waiting", "client pulse", "silence check"
- `/morning` needs a communication section
- User asks about client communication status

## How It Works

1. Call the ChefFlow API to get pulse data
2. Format as a scannable dashboard
3. Recommend immediate actions

## Step 1: Fetch Pulse Data

Hit the local server to get pulse data:

```bash
curl -s http://localhost:3000/api/v2/clients/pulse \
  -H "Content-Type: application/json" \
  -H "Cookie: $(cat .auth/agent-cookie.txt 2>/dev/null || echo '')" \
  2>/dev/null
```

If the API endpoint doesn't exist yet, fall back to querying the database directly:

```bash
curl -s http://localhost:3000/api/trpc/clients.list 2>/dev/null
```

Or read `lib/clients/pulse-actions.ts` and understand the `getClientPulse()` function to know what data it returns. The function queries:

- Inquiries in status: new, awaiting_chef, awaiting_client, quoted
- Events in status: draft, accepted, paid
- Quotes awaiting response
- Follow-ups that are overdue

## Step 2: Display Dashboard

Format output as:

```
CLIENT PULSE [timestamp]
━━━━━━━━━━━━━━━━━━━━━━━

CRITICAL (7+ days silent)
  Sarah M. - inquiry (12d) - "Wedding dinner for 20"
    -> Needs: quote response | Contact: email

OVERDUE (3-7 days)
  Mike R. - event prep (5d) - "Anniversary dinner Apr 15"
    -> Needs: menu confirmation | Contact: phone

DUE (1-3 days)
  Lisa K. - follow-up (2d) - "Post-event thank you"
    -> Needs: send debrief | Contact: email

OK (< 1 day)
  (none waiting)

━━━━━━━━━━━━━━━━━━━━━━━
SUMMARY: 3 waiting | 1 critical | longest: 12 days
NEXT ACTION: Reply to Sarah M. (critical, 12 days)
```

## Step 3: Recommend Actions

For each critical/overdue client, suggest:

- What to say (1-line draft)
- Which channel (email/phone/portal based on client preference)
- Link to their page in ChefFlow

## One-Liner Mode

For `/morning` or `/status` integration, output single line:

```
CLIENTS: 3 waiting (1 critical, 12d max). Next: reply to Sarah M.
```

## Key Files

- Pulse engine: `lib/clients/pulse-actions.ts`
- Communication actions: `lib/communication/actions.ts`
- Follow-up tracking: `lib/communication/follow-up-actions.ts`
- Client touchpoints: `lib/clients/touchpoint-actions.ts`
- Dormancy detection: `lib/clients/dormancy.ts`
- Quick replies: `lib/communication/quick-reply-actions.ts`

## Rules

- NEVER fabricate client names or wait times. Only show real data.
- If API is down, say so. Don't show empty as "no one waiting."
- Urgency thresholds: critical (7d+), overdue (3-7d), due (1-3d), ok (<1d)
- Sort by urgency first, then by wait days descending within each tier.
