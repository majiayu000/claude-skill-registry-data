---
name: next-dinner
description: Full briefing on your next upcoming event. Menu, guests, dietary needs, shopping status, prep timeline, what's not ready. Use when user says "next dinner", "what's coming up", "next event", "what am I cooking", or before any event prep.
user-invocable: true
---

# Next Dinner - Event Briefing

Everything you need to know about your next event in one view.

## Trigger Conditions

Auto-fire when:

- User says "next dinner", "next event", "what's coming up"
- User says "what am I cooking", "what's on deck"
- 48h before any event (morning briefing integration)
- User is about to start prep or shopping

## Step 1: Find Next Event

Query for the nearest future event:

```bash
curl -s "http://localhost:3000/api/v2/events?upcoming=true&limit=1" \
  -H "Cookie: $(cat .auth/agent-cookie.txt 2>/dev/null || echo '')" \
  2>/dev/null
```

Or query via `lib/events/actions.ts` for the next event with status in (`accepted`, `paid`, `confirmed`) and `event_date >= today`, ordered by date ascending.

If no upcoming events, say so clearly.

## Step 2: Gather All Event Data

For the found event, fetch in parallel:

- Event details (date, time, location, guest count, occasion)
- Client info (name, contact, dietary restrictions)
- Menu (courses, dishes, ingredients)
- Guest list with dietary needs (`lib/events/dietary-conflict-actions.ts`)
- Prep timeline (`lib/events/prep-timeline.ts`)
- Shopping list status (what's bought vs needed)
- Equipment/packing checklist (`lib/events/equipment-checklist-actions.ts`)
- Readiness score (`lib/events/readiness.ts`)
- Financial summary (quote amount, paid status)

Key files to query:

- `lib/events/actions.ts` - core event data
- `lib/events/readiness.ts` - completion/readiness check
- `lib/events/prep-timeline-actions.ts` - prep timeline
- `lib/events/countdown-actions.ts` - countdown
- `lib/events/equipment-checklist-actions.ts` - gear list
- `lib/events/financial-summary-actions.ts` - money status
- `lib/events/dietary-conflict-actions.ts` - allergen cross-check

## Step 3: Display Briefing

```
NEXT DINNER BRIEFING
━━━━━━━━━━━━━━━━━━━━

EVENT: Sarah's Wedding Dinner
DATE:  Saturday, June 15 (8 days away)
TIME:  6:00 PM
LOCATION: 42 Oak St, Haverhill MA
GUESTS: 20
CLIENT: Sarah M. (sarah@email.com)
OCCASION: Wedding celebration dinner

READINESS: 72% ████████░░░░
━━━━━━━━━━━━━━━━━━━━━━━━━━━

MENU (5 courses)
  Amuse:   Tuna tartare on wonton crisp
  App:     Burrata with heirloom tomatoes, basil oil
  Salad:   Arugula, shaved parm, lemon vinaigrette
  Main:    Filet mignon, truffle mash, asparagus
  Dessert: Chocolate lava cake, vanilla ice cream

DIETARY ALERTS
  Guest 3 (Tom): tree nut allergy -> CHECK: truffle mash safe
  Guest 7 (Amy): vegetarian -> NEED: alt main course

NOT READY (blocking)
  [ ] Menu not confirmed by client
  [ ] Shopping list not generated
  [ ] Vegetarian alternative not planned

PREP TIMELINE
  Thu Jun 13:  Stock, sauces, dessert prep
  Fri Jun 14:  Butcher filets, prep garnishes, pack car
  Sat Jun 15:  Final mise, travel by 3PM, service 6PM

FINANCIAL
  Quote: $2,500 | Deposit: $1,000 received | Balance: $1,500 due

SHOPPING
  Not generated yet. Run after menu confirmation.

━━━━━━━━━━━━━━━━━━━━━━━━━━━
NEXT ACTIONS:
  1. Get menu confirmation from Sarah (critical, 8 days out)
  2. Plan vegetarian alternative for Amy
  3. Generate shopping list once menu confirmed
```

## Week-Ahead Mode

If user says "week ahead" or "this week", show a compact version for ALL events this week:

```
WEEK AHEAD [Jun 10-16]
━━━━━━━━━━━━━━━━━━━━━

Wed Jun 12 - Corporate lunch (15 guests) - 85% ready
Sat Jun 15 - Sarah's wedding dinner (20 guests) - 72% ready
Sun Jun 16 - Birthday brunch (8 guests) - 90% ready

Most urgent: Sarah's wedding (menu not confirmed, 3 days)
```

## One-Liner Mode

For `/morning` or `/status`:

```
NEXT: Sarah's wedding dinner, Jun 15 (8d), 20 guests, 72% ready. Blocker: menu not confirmed.
```

## Key Files

- Event core: `lib/events/actions.ts`
- Readiness: `lib/events/readiness.ts`
- Prep timeline: `lib/events/prep-timeline.ts`, `lib/events/prep-timeline-actions.ts`
- Countdown: `lib/events/countdown-actions.ts`
- Equipment: `lib/events/equipment-checklist-actions.ts`
- Dietary conflicts: `lib/events/dietary-conflict-actions.ts`
- Financial: `lib/events/financial-summary-actions.ts`
- Day-of checklist: `lib/events/day-of-checklist-actions.ts`
- Client actions: `lib/events/client-actions.ts`

## Rules

- NEVER fabricate event data. Show only real data from the database.
- If no upcoming events, say "No upcoming events scheduled."
- Readiness percentage comes from the completion contract engine, not guesswork.
- Dietary alerts are SAFETY-CRITICAL. Always surface them prominently.
- Financial data is real money. Show exact numbers.
