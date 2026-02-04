---
name: user-journey-tracking
description: Track user journeys with intent context and friction signals. Use when instrumenting onboarding, checkout, or any multi-step flow where you need to understand WHY users fail.
triggers:
  - "checkout funnel"
  - "conversion tracking"
  - "drop-off tracking"
  - "onboarding flow"
  - "track user funnels"
  - "user journey"
priority: 2
---

# User Journey Tracking

Track not just WHAT users do, but WHETHER they accomplished their goal.

## Core Principle

Every journey event should help answer: **"Why did users fail to complete their intended task?"**

## Key Context to Attach

| Field | Example | Purpose |
|-------|---------|---------|
| `job_name` | "checkout" | User's intended task |
| `job_step` | "payment" | Current step in journey |
| `job_progress` | "3/4" | How far they got |
| `outcome` | "success" / "friction" / "abandon" | Did they succeed? |

## Friction Signals to Track

Detect user struggle before they contact support:

| Signal | Detection |
|--------|-----------|
| Rage taps | 3+ taps same element in 1s |
| Retry exhaustion | 3+ retries of same action |
| Quick abandonment | Exit within 5s of error |
| Navigation loops | 3+ back navigations without progress |

## Outcome Quality

Not just success/failure:

- **Completed smoothly** — no friction
- **Completed with friction** — retries, errors, slow
- **Abandoned after friction** — struggled, then quit
- **Abandoned immediately** — no engagement

"Completed with friction" is often the most actionable signal.

## When to Use This Skill

- Onboarding flows
- Checkout/payment funnels
- Signup/registration
- Any multi-step process
- Feature adoption tracking

## Implementation References

| Topic | Reference |
|-------|-----------|
| Full methodology | `references/user-focused-observability.md` |
| Job-based patterns | `references/jtbd.md` |
| Friction detection code | `references/user-journeys.md` |
| Journey correlation | `references/user-journeys.md` |

## Decision Tree

Before adding journey instrumentation:

1. Does this help identify what the user was trying to do? → Add intent context
2. Does this help determine if they succeeded? → Track outcomes
3. Does this help explain why they failed? → Add friction signals

If no to all three → probably don't need it.

## Related Skills

- See `skills/instrumentation-planning` for prioritization framework
- Combine with `skills/interaction-latency` for friction detection on key actions
- Combine with `skills/navigation-latency` for screen transition context
