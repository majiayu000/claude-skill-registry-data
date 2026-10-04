---
name: Taxi
slug: taxi
version: 1.0.0
description: Handle everything for ground transportation, from price comparison to booking, tracking, disputes, and expense management.
homepage: https://clawic.com/skills/taxi
metadata:
  clawdbot:
    emoji: 🚕
    requires:
      bins: []
    os:
    - linux
    - darwin
    - win32
    displayName: Taxi
---

## When to Use

User needs ANY help with taxis, rideshares, car services, or ground transportation. Agent handles research, comparison, booking assistance, price monitoring, expense tracking, and problem resolution.

## Architecture

Memory lives in `~/Clawic/data/taxi/`. See `memory-template.md` for setup.

```
~/Clawic/data/taxi/
├── memory.md          # Preferences, saved addresses, default apps
├── trips.md           # Trip history and expenses
├── accounts.md        # Which apps user has, preferences per app
└── promos.md          # Active promo codes, referral links
```

## Quick Reference

| Topic | File |
|-------|------|
| Memory setup | `memory-template.md` |
| City/app coverage | `cities.md` |
| Fare estimation | `fares.md` |
| Booking workflows | `booking.md` |
| Problem resolution | `problems.md` |

## Core Rules

### 1. Know User Context First
Before any recommendation, check `~/Clawic/data/taxi/memory.md` for:
- Preferred apps and why
- Saved addresses (home, work, airport)
- Payment preferences (card, cash, business)
- Special needs (wheelchair, car seat, pet-friendly)
- Budget sensitivity

### 2. Proactive Comparison
| Task | Agent Action |
|------|--------------|
| User needs ride | Compare 3+ options with current prices |
| Surge detected | Alert user, suggest waiting or alternatives |
| Airport transfer | Compare rideshare vs shuttle vs taxi vs car service |
| Group ride | Calculate if multiple rides or XL is cheaper |
| Regular route | Track prices over time, suggest best booking window |

### 3. Maximize Savings
- Search for active promo codes before any booking
- Check if user has referral credits in any app
- Compare scheduled vs on-demand pricing
- Suggest pool/shared when time permits
- Monitor surge and alert when it drops
- Find airport flat rates vs metered options

### 4. Assist Booking Process
What agent CAN do:
- Open booking websites/apps via browser
- Pre-fill pickup and destination
- Select vehicle type based on user needs
- Apply promo codes
- Set scheduled pickup time
- Navigate to payment confirmation step

What requires user:
- Final payment confirmation
- Entering new payment methods
- Phone verification

### 5. Handle Special Scenarios

| Scenario | Agent Handles |
|----------|---------------|
| Airport pickup | Check terminal, flight tracking for delays, meet & greet options |
| Business travel | Ensure receipt capability, corporate profile, expense categories |
| Late night | Prioritize safety features, well-rated drivers, tracked rides |
| Foreign country | Find local apps, check cash/card acceptance, language tips |
| Large group | Calculate split options, find vans/minibuses, coordinate multiple cars |
| Accessibility | Filter for wheelchair-accessible, verify with company if needed |
| With pets | Find pet-friendly options, carrier requirements |
| With kids | Car seat availability, family-friendly services |
| VIP/Executive | Car services, black car, chauffeur options |
| Event pickup | Coordinate pickup points, surge avoidance strategies |

### 6. Track Everything
Log in `~/Clawic/data/taxi/trips.md`:
- Date, route, app used
- Price paid, promo applied
- Category (personal, business, specific project)
- Notes (late driver, surge, issues)

Provide:
- Monthly expense summaries
- Per-category totals
- Comparison vs public transit
- Year-over-year trends

### 7. Resolve Problems
When user has issue:
1. Identify problem type (overcharge, route, driver, safety, lost item)
2. Find correct channel (in-app, email, phone, social)
3. Draft complaint with relevant details
4. Track resolution status
5. Escalate if no response (BBB, local regulator, social media)

See `problems.md` for dispute workflows by app.

### 8. Stay Current
- Check for new apps entering user's city
- Monitor promo code sources (RetailMeNot, Honey, app-specific)
- Track regulatory changes (some cities ban/restrict services)
- Know seasonal patterns (holiday surge, airport construction)

### 9. Multi-Modal Integration
Sometimes taxi isn't best option:
- Compare with public transit for cost/time
- Suggest train + last-mile rideshare
- Rental car for multi-day or multi-stop
- Hotel shuttle for airport
- Walking + rideshare vs door-to-door

### 10. Privacy & Security
- Never store full payment details
- Mask home address in logs if user prefers
- Share trip tracking with emergency contacts
- Verify driver details before user enters vehicle

## Common Traps

- Booking without checking surge → Always show current multiplier
- Assuming one app works everywhere → Check local alternatives first
- Ignoring scheduled ride option → Often 10-20% cheaper
- Not logging business trips immediately → Harder to categorize later
- Using first promo code found → Some stack, some conflict, check terms
- Recommending cheapest without context → Safety/reliability matter for some trips
- Forgetting airport rules → Designated pickup areas, terminal-specific pricing
- Not tracking flight delays → User waits, ride leaves or charges wait time
- Ignoring user's past preferences → Check memory before suggesting
