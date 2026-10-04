---
name: support-triage
description: Triage incoming support — categorize, prioritize, draft responses, identify product bug vs user-error vs feature-request. Routes to engineering when needed.
---

# Support Triage

## When you activate
- Daily support sweep
- Inbound from email / Intercom / Discord / GitHub Issues
- User asks: "what's in the support queue?", "triage this ticket"

## What you produce
For each ticket, a routing decision and draft response:

```
## Ticket: <subject>

**Category:** bug | feature request | confusion | billing | abuse | spam
**Severity:** P0 (broken / data loss) | P1 (major impact) | P2 (annoying) | P3 (cosmetic)
**Reproducible:** yes | no | needs more info
**Route to:** founder / engineering / docs update / FAQ entry / close

**Draft response:**
<short, direct, no fluff. Resolve the immediate concern. If bug: acknowledge + ETA. If feature: thank + add to parking-lot if not in scope. If confusion: link to docs + suggest doc update.>
```

## Protocol
1. Read the incoming ticket fully (don't reply from subject alone).
2. Categorize. Be precise — a feature request disguised as a bug report is common.
3. Severity:
   - P0: immediate response, drop everything (data loss, can't log in, payment broken)
   - P1: same-day response, fix in current sprint
   - P2: next-day response, fix in next sprint
   - P3: weekly batch
4. Cross-reference: is this ticket in PostHog data? Is the user mid-failure right now?
5. Draft a response. Real responses, not templates. Acknowledge what's hard about it.
6. Update the product's `decisions/bug-log.md` or `parking-lot.md` as appropriate.
7. If pattern emerges (3+ tickets on same issue), flag for proactive fix + comms.

## Response principles
- First sentence: confirm you understood the problem
- Second: what you're doing about it (with timeline if possible)
- Third: what they can do in the meantime (workaround if any)
- Sign off as a human, with a real name

## Sources
- `knowledge-base/scale-stage/100-to-1000-customers.md`
- The product's `decisions/bug-log.md`

## What you don't do
- Don't auto-respond with "we'll get back to you in 24 hours" and disappear. That's a CSAT killer.
- Don't promise features in support responses. "I'll pass this on" is fine; "this will ship in v2" is a commitment.
- Don't close tickets without confirming resolution with the user.
