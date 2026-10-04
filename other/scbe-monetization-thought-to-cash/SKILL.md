---
name: scbe-monetization-thought-to-cash
description: "Drive end-to-end monetization from idea to cash for SCBE projects using offer design, Stripe/Shopify execution, launch tasks, revenue tracking, and Obsidian evidence logging. Use when the user asks to make money, launch paid products, create pricing, wire checkout and webhooks, publish store products, or run a daily cash execution loop."
---

# SCBE Monetization Thought To Cash

## Overview

Run a practical thought-to-cash loop: package an offer, activate payment rails, launch quickly, and track daily cash evidence in Obsidian.

## Workflow

1. Classify monetization objective.
- `subscription`: recurring revenue via Stripe billing tier checkout.
- `digital_product`: one-time revenue via Shopify product listings.
- `service_bundle`: Stripe payment + Shopify distribution + outbound campaign.

2. Validate rails before launch.
- Confirm Stripe billing endpoints and webhook verification are active.
- Confirm Shopify store domain and access token are configured.
- Confirm no secrets are committed and webhook signatures are checked.

3. Build offer and checkout path.
- Choose one core offer and one upsell.
- Define price, result promise, fulfillment path, and refund boundary.
- Generate execution tasks using `references/thought-to-cash-playbook.md`.

4. Ship storefront and payment.
- For Shopify product sync, use:
  - `python scripts/shopify_bridge.py products --publish-live`
- For Stripe subscription checkout, verify:
  - `api/billing/routes.py`
  - `api/billing/stripe_client.py`
  - `api/billing/webhooks.py`

5. Capture receipts and daily metrics.
- Write a daily cash node with `scripts/build_cash_scorecard.py`.
- Append outcomes to Obsidian Cross Talk and task notes.
- Keep a single next action that increases cash within 24h.

## Guardrails

- Keep credentials in environment variables only.
- Keep idempotency and replay safety on payment/webhook handlers.
- Keep launch scope narrow: one core offer, one channel, one KPI target.
- Keep evidence-first updates in Obsidian for later editing/recomposition.

## Resources

- `references/thought-to-cash-playbook.md`: end-to-end execution checklist.
- `references/stripe-shopify-status-check.md`: what exists now and what to patch next.
- `scripts/build_cash_scorecard.py`: write structured daily monetization node.
