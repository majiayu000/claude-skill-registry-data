---
name: stripe-billing-cycle-test
description: Verify Stripe subscription billing cycles using a test clock. Use when you need to simulate time passing to trigger subscription renewals, recurring invoices, or to confirm that the next billing date generates the expected charge in Stripe test mode.
---

# Stripe Billing Cycle Test

Standard procedure for validating that a subscription bills correctly on its
next cycle by simulating time with a Stripe test clock. All steps run against
Stripe **test mode only** (the MCP rejects live keys).

## Order matters

The steps below are strictly ordered. A customer can be attached to a test
clock **only at creation time**, so the clock must exist before the customer,
and the customer before the subscription.

## Steps

1. **Create the test clock.**
   Tool: `create_stripe_test_clock`
   - `frozen_time` (required): Unix timestamp in **seconds** for the starting
     time.
   - `name` (optional): a label to find it later.
   - Keep the returned `test clock id` for the next steps.

2. **Create a customer attached to that clock.**
   Tool: `create_stripe_test_customers`
   - `test_clock`: the id from step 1.
   - `number`: keep it at most `3` (max 3 customers per clock).
   - `payment_method_id` (optional but recommended): attach a test payment
     method (for example `pm_card_visa`) so the renewal invoice can be paid
     instead of staying open. Confirm against the Stripe docs which test
     payment method fits the card behavior you want.
   - Keep the returned customer id(s).

3. **Create the subscription.**
   Tool: `create_stripe_test_subscription`
   - `customer`: the id from step 2.
   - `items`: array of `{ price, quantity }`. The `price` must be a recurring
     price id from your test data.
   - `proration_behavior` (optional): `create_prorations`, `none`, or
     `always_invoice`.
   - `payment_method_id` (optional): the same test payment method.
   - This creates the first invoice for the current period.

4. **Advance the clock to the next billing date.**
   Tool: `advance_stripe_test_clock`
   - `test_clock_id`: the id from step 1.
   - `frozen_time`: a Unix timestamp (seconds) **after** the current frozen
     time. Advance is forward-only; you cannot move a clock backward. Pick a
     time just past the subscription's `current_period_end` to cross the
     renewal boundary.

5. **Wait for the clock to settle, then verify.**
   - `advance_stripe_test_clock` reports the clock `status` once, in its
     response text. Advancing is **asynchronous**. This MCP server does not
     expose a tool to retrieve or re-poll the clock, so you cannot
     programmatically watch it transition to `ready`.
   - If the response shows `advancing`, either wait a few seconds before
     proceeding, or ask the user to confirm the clock has settled in the
     Stripe Dashboard (test mode) before continuing.
   - Then confirm the new invoice for the renewed period was generated and has
     the expected amount and status. Inspect this in the Stripe Dashboard
     (test mode) or via the Stripe API, since the MCP does not expose an
     invoice-listing tool.

## Notes

- `frozen_time` is always a Unix timestamp in seconds (not milliseconds).
- Customers created by this MCP are tagged with `metadata.generator = stripe-testing-tools-mcp`. The MCP cannot search customers by this tag, but it helps you locate them in the Stripe Dashboard or CLI; record the returned ids for programmatic cleanup.
- For cleanup after verification, see the `stripe-test-data-lifecycle` skill.
- For the full list of test-clock constraints, see the
  `stripe-test-clock-constraints` skill.
