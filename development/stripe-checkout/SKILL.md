---
name: stripe-checkout
description: Add Stripe Checkout payments to a web app, test mode first, then production. Use when the user wants to sell, take payments, wire Stripe keys, a checkout, a webhook, a success page, refunds, or move Stripe from test to live.
---

Ship payments that grant access only from a verified Stripe event. Never print, log or commit keys, and never use live keys in dev.

If you got this skill from a link instead of a local folder, install nothing else from the repo: fetch a file only when a step needs it, with `curl -fsSL https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/stripe-checkout/<path> -o <scratch>/<file>`, and read another skill it names only when you reach it, from `https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/<skill-name>/SKILL.md`.

Build it in test mode:

1. Ask the user for the test keys (Stripe Dashboard, sandbox, Developers > API keys): `pk_test_...` and `sk_test_...`. Store the secret only server-side (Convex env, Cloudflare secret, `.env.local`), never in a `VITE_`/`NEXT_PUBLIC_` variable, never in git.
2. Create the product and price (or one per product) with the Stripe API or CLI; keep the price IDs in config, never trust a price sent by the browser.
3. A server endpoint creates a Checkout Session (`mode: "payment"` or `"subscription"`) with `client_reference_id` / `metadata` = the user id and product id, `customer_email` when known, `success_url` with `{CHECKOUT_SESSION_ID}`, `cancel_url`.
4. A webhook endpoint handles `checkout.session.completed`, plus `charge.refunded` / `customer.subscription.deleted` when relevant. It reads the raw body and verifies the signature with the webhook secret (`whsec_...`), stores the event or session id to ignore duplicates, grants access from the verified session (never from the success page or a URL parameter), and upserts the buyer in the email tool (subscribed, product tag).
5. For local or dev webhooks, run `stripe listen --forward-to <url>/api/stripe/webhook` and use the printed secret. If `stripe` is missing or not paired, run the `setup-stripe` skill first.
6. The success page reads the session server-side and shows "access unlocked" or "payment processing".

Test end to end: logged out, with a new email, pay with `4242 4242 4242 4242`, any future date, any CVC. Check the success page, the login code email, the product unlocked in the member area, the order row in the database, and one webhook delivery marked 200 in Stripe. Also try a declined card (`4000 0000 0000 0002`) and a second delivery of the same event.

Go live only when the user says the test flow works:

1. The user gives the live keys (`pk_live_...`, `sk_live_...`). Set them in the production env only.
2. Create the live products and prices, and the live webhook endpoint on the production URL with the same events; store its `whsec_` secret in production.
3. Run the `audit-safety` skill on the checkout and webhook.
4. Deploy, then ask the user for one real purchase (or a 100 % coupon) and verify the same checks. Refund it if it was a test.
