---
name: stripe-test-data-lifecycle
description: Set up, verify, and clean up Stripe test data end to end. Use when creating test customers, products, or subscriptions and you want a repeatable setup-then-teardown workflow, or when you need to remove leftover test customers and products with delete_stripe_test_customers, archive_stripe_test_products, and delete_stripe_test_products.
---

# Stripe Test Data Lifecycle

A round-trip workflow for Stripe test data: set up, verify, then clean up so
the test account stays tidy. Test mode only (live keys are rejected).

## 1. Setup

- **Customers:** `create_stripe_test_customers`
  - `number` (default 1), and optional `name`, `email`, `description`,
    `payment_method_id`, `test_clock`.
  - Every customer created here is tagged with
    `metadata.generator = stripe-testing-tools-mcp`. The MCP server has no tool
    to list or search customers by metadata, so **record the ids returned at
    creation** for later cleanup. The tag is still useful for finding leftovers
    in the Stripe Dashboard or Stripe CLI.
  - If attaching a `test_clock`, keep `number` at most 3 (see
    `stripe-test-clock-constraints`).
- **Subscriptions:** `create_stripe_test_subscription`
  - `customer`, `items` (`[{ price, quantity }]`), optional
    `proration_behavior`, `payment_method_id`.
- **Products/prices:** create these with your normal Stripe tooling or
  Dashboard; this MCP only archives/deletes products, it does not create them.

## 2. Verify

- Run your scenario (for time-based billing, follow
  `stripe-billing-cycle-test`).
- Confirm results (invoices, subscription status, charges) via the Stripe
  Dashboard in test mode or the Stripe API. The MCP does not expose
  list/read tools for these objects.

## 3. Cleanup (recommended order)

Tear down dependents before their dependencies to avoid leftover references:

1. **Delete customers:** `delete_stripe_test_customers`
   - `customer_ids`: array of ids to delete. You must use the ids collected at
     creation — the MCP cannot search customers by `generator` metadata. To
     recover lost ids, look them up in the Stripe Dashboard or CLI.
   - Deleting a customer immediately cancels its associated subscriptions
     ([Stripe: Delete a customer](https://docs.stripe.com/api/customers/delete)),
     so do this before touching products.
2. **Archive products:** `archive_stripe_test_products`
   - `product_ids` and/or `urls`. Archiving sets `active: false` and is
     non-destructive (recoverable). Prefer this when a product may still be
     referenced or you want a soft cleanup.
3. **Delete products (optional, permanent):** `delete_stripe_test_products`
   - `product_ids` and/or `urls`. Permanent and irreversible. Stripe only lets
     you delete a product with no active prices/usage; if deletion fails,
     archive instead. Confirm the exact deletability rules against the Stripe
     docs when in doubt.

## Notes

- Both product tools accept either explicit `product_ids` or `urls` (the URL
  form looks products up by their `url` field).
- Test clocks themselves are not deleted by these tools; remove unused clocks
  from the Stripe Dashboard if needed.
- Always double-check you are operating in test mode before any delete.
