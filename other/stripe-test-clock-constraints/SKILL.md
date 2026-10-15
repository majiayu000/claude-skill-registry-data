---
name: stripe-test-clock-constraints
description: Reference for Stripe test clock constraints and pitfalls. Use when planning or debugging test-clock workflows, when an advance or customer-attach step fails, or to check rules before building a time-simulation scenario with create_stripe_test_clock, advance_stripe_test_clock, and create_stripe_test_customers.
---

# Stripe Test Clock Constraints

Quick reference for the rules and gotchas of Stripe test clocks as exposed by
this MCP. Consult this before designing a time-simulation scenario.

## Hard constraints

- **Max 3 customers per clock.** `create_stripe_test_customers` with a
  `test_clock` set rejects `number > 3`. To exceed 3 customers in one
  scenario, use additional clocks.
- **Clock attachment is creation-time only.** A customer can be linked to a
  test clock **only when it is created** (`create_stripe_test_customers` with
  `test_clock`). There is no way to attach or move an existing customer to a
  clock afterward, so create the clock first.
- **Advance is forward-only.** `advance_stripe_test_clock` can only move
  `frozen_time` to a time **after** the current frozen time. You cannot rewind
  a clock; to test an earlier point, create a new clock.
- **Advance is asynchronous.** After `advance_stripe_test_clock`, the clock
  enters an `advancing` state and processes billing events in the background.
  The tool returns the `status` once in its response, but this MCP server does
  **not** expose a tool to retrieve or re-poll the clock, so you cannot
  programmatically watch it reach `ready`. If the response shows `advancing`,
  wait a few seconds before follow-up operations, or have the user confirm the
  clock has settled in the Stripe Dashboard.

## Time format

- `frozen_time` is a **Unix timestamp in seconds** (epoch seconds), not
  milliseconds and not an ISO string.
- Convert carefully:
  - Many languages give milliseconds (`Date.now()` in JS) — divide by 1000 and
    floor.
  - From an ISO date: compute epoch seconds (for example, in shell
    `date -d '2024-02-01T00:00:00Z' +%s`).
  - When reading a value back, multiply by 1000 to build a JS `Date`.
- A common bug is passing milliseconds, which lands the clock far in the
  future; double-check the magnitude (a 2024-2026 timestamp is ~1.7e9, a
  millisecond value is ~1.7e12).

## Practical guidance

- Plan all the time points you need up front; since you cannot rewind, build a
  fresh clock per backward scenario.
- Keep the `test_clock_id` returned at creation; it is required for every
  advance.
- To cross a billing boundary, advance to just past the subscription's
  `current_period_end`.
- For an end-to-end billing procedure, see `stripe-billing-cycle-test`.
- For setup/cleanup of the data around clocks, see
  `stripe-test-data-lifecycle`.
