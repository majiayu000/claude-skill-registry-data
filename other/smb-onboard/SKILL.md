---
name: smb-onboard
version: 1.0.0
description: Onboard a new small-business owner — connect their first two tools, run one recipe, interview them, store context, and set a weekly check-in.
author: matrixx0070
tags: [onboarding, setup, interview, context, check-in, first-run]
capabilities: []
---

# Onboard

## When to use
Run this the first time a small-business owner arrives, or when they want to reset their setup. It gets them from zero to one real result and captures enough context to be useful going forward.

**Not for:** routing an already-onboarded owner to a task (use smb-router); deep analysis in any one area — onboarding produces a taste, not a full report.

## Method
1. **Welcome and orient.** In two sentences: what the toolkit does, and that the owner approves anything touching money or customers.
2. **Connect the first two tools.** Typically accounting or payments, plus a CRM or storefront. Decision point: pick the two that match the owner's biggest headache, not a fixed list. Confirm each connection actually works.
3. **Run one recipe end to end.** For example a sales brief or a month heads-up, so they see a real result in the first session.
4. **Interview the owner.** Business type, what they sell, busy seasons, biggest current headache, goals. Keep it short and conversational.
5. **Store durable context.** Save the answers so later skills personalize. Decision point: read the result and interview back to confirm before storing — don't persist a wrong guess.
6. **Set cadence and hand off.** Agree a weekly check-in day and point them to smb-router for what's next. No spend or customer contact happens during onboarding without approval.

## Example
Bakery owner arrives. Connect Square (payments) and Mailchimp (CRM); both confirm green. Run smb-sales-brief on the last 30 days — croissants top revenue, day-old bread stale. Interview: wholesale + retail, holidays are peak, headache is slow weekday mornings, goal is +15% weekday sales. Store that context. Set Monday check-in; hand off to smb-run-campaign for a weekday-morning promo when ready.

## Pitfalls
- Connecting five tools and finishing none; two working connections beat five half-configured.
- Skipping the live recipe — an owner who hasn't seen one result won't come back.
- Storing interview answers without confirming them, so every later skill inherits a wrong assumption.
- Quietly acting on money or customers "to demonstrate" — the approval rule starts at minute one.

## Output format
- **Connection status:** each of the two tools (connected / failed + reason).
- **First recipe result:** the actual output produced.
- **Business-context summary:** saved, and shown for the owner to correct.
- **Cadence + next steps:** confirmed weekly check-in day + a short "what's next" menu.
- **Approval note:** no spend or customer contact during onboarding without approval.

## Reference

### First-session run sheet (target: under 30 minutes)
| Minute | Step | Done-when |
|--------|------|-----------|
| 0-2 | Welcome + approval rule stated | Owner confirms they hold the money/customer switch |
| 2-8 | Connect tool 1 (money) | Test call returns real data, not a 401 |
| 8-14 | Connect tool 2 (customers/sales) | Same live-data check |
| 14-22 | Run one recipe end-to-end | Owner sees a real number about *their* business |
| 22-28 | Interview (7 questions below) | Answers read back and confirmed |
| 28-30 | Set weekly cadence + hand off | Check-in day agreed, next skill named |

### Connect-first priority by business type
- **Retail / e-commerce:** payments/POS (Square, Shopify, Stripe) + email/CRM (Mailchimp, Klaviyo).
- **Services / agency:** accounting (QuickBooks, Xero, Wave) + invoicing or CRM (HubSpot, FreshBooks).
- **Restaurant / cafe:** POS (Toast, Square) + review/reservations (Google, OpenTable).
- **Solo / freelance:** bank feed or accounting + calendar/email. Two is the cap; a third waits for a real need.

### The 7 onboarding-interview questions
1. What do you sell, and who buys it?
2. How do you take payment and track sales today?
3. When is your busy season vs. your slow stretch?
4. What's the single headache eating your week right now?
5. What would "a good next 90 days" look like in one number?
6. Who else touches the money or talks to customers?
7. How do you want to hear from me — and how often?

### Connection-health quick checks
- **OAuth token:** make one read call and confirm a known record comes back (not just a 200).
- **Empty-data trap:** a new store may legitimately return zero rows — say "connected, no data yet" rather than "failed."
- **Scope check:** read-only scope is enough for onboarding; never request write/charge scopes until a skill needs them.

### Business-context record (what to store)
`business_type · what_they_sell · sales_channel(s) · busy_season · slow_season · top_headache · 90_day_goal · brand_voice_note · cadence_day · connected_tools[]`. Store only after read-back confirmation — a wrong value here poisons every downstream skill.

### Cadence defaults
Weekly Monday pulse (smb-sales-brief or smb-monday-brief) is the safe default. Add a month-end cash look (smb-month-heads-up) and a quarter-end review (smb-quarterly-review) only once the owner has seen value from the weekly rhythm. Never auto-schedule anything that emails a customer.

### Common first-session failure modes
- Connection "green" but wrong account (personal vs. business) — verify the account name.
- Owner watches you work but never touches it themselves — hand them the keyboard for the recipe run.
- Over-collecting context you'll never use; the 7 questions are enough to personalize the first month.
