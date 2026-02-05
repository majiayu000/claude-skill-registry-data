---
name: user-journey-tracking
description: Track user journeys with intent context and friction signals. Use when instrumenting funnels or multi-step flows.
triggers:
  - "track user journey"
  - "funnel instrumentation"
  - "drop-off analysis"
priority: 2
---

# User Journey Tracking

Instrument flows to answer: "Why did users fail to complete their intended task?"

## Core Principle

Every event should include intent context:

| Field | Example | Why |
|-------|---------|-----|
| `job_name` | "checkout" | Which user goal |
| `job_step` | "payment" | Where in the journey |
| `job_progress` | "3/4 steps" | How far they got |

## Friction Signals

Detect when users are struggling:

| Signal | Detection | Indicates |
|--------|-----------|-----------|
| **Rage clicks** | 3+ clicks on same element within 1s | UI unresponsive |
| **Retry exhaustion** | 3+ retries of same action | Persistent failure |
| **Quick abandonment** | Exit within 5s of error | Lost trust |
| **Form thrashing** | Repeated focus/blur on same field | Confusion |
| **Back loops** | 3+ backs without progress | Lost/confused |

## Key Events

| Event | When |
|-------|------|
| `journey.started` | User begins multi-step flow |
| `journey.step_complete` | User advances to next step |
| `journey.friction` | Friction signal detected |
| `journey.success` | User completes goal |
| `journey.abandoned` | User exits without completing |

## Anti-Patterns

- Tracking steps without job context (can't correlate)
- Missing friction signals (only see drop-off, not why)
- Not tracking "success with friction" (silent failures)
- High-cardinality step names (use patterns, not IDs)

## Implementation

Use Read tool to load `references/user-focused-observability.md` for detailed patterns.

## Related

- `skills/instrumentation-planning` - JTBD framework
- `skills/error-tracking` - Enriching errors with journey context
- `references/jtbd.md` - Jobs-to-be-Done methodology
