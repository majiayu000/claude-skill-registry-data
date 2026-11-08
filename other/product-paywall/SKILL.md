---
name: product-paywall
description: Put a small web prototype behind a paywall — part of it free, the full thing for one fixed price — with Stripe embedded Checkout, an emailed HMAC password, and a data API that refuses without it. Use when you say "they get some of it free but must pay for the full thing", "add a paywall", "charge for it", "sell the full list", "what should we charge". Covers the free/paid split, the build, the shared-webhook pattern for Stripe's 16-endpoint cap, the price rule, and the live verification checklist (including the static-file leak that makes paywalls decorative).
---

# Free slice, one price, the full thing

## The build

- **The static site ships only the free slice plus counts.** The full data is served by a
  function, `/api/data`, which requires a password: a nonce plus an HMAC under
  `ACCESS_SECRET`.
- **The password is minted at checkout.** `/api/checkout` creates an embedded Checkout
  Session and puts the password (or the nonce) in session `metadata`; on
  `checkout.session.completed` a webhook emails it (Mailgun, Postmark, SES...). A
  `/api/session-status` endpoint lets the return page show it immediately, and a
  `pw_emailed` marker in metadata prevents double emails.
- Env: `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `ACCESS_SECRET`, mail provider keys.
- **Track `preview_open`, `checkout_open` and `paid` as analytics events.** "Sales" means
  nothing without the step people stop at; many checkouts with no payments is a price signal.
- **The free slice proves value on the reader's own row**, and the page opens pre-loaded
  with a real example. A blank tool loses an attention-poor visitor.

## Webhook: one shared endpoint, not one per product

Stripe caps an account at **16 webhook endpoints**. Past that, a new product gets none, and a
buyer who closes the tab before the return page loads never gets a password. So run **one
router endpoint** for every paywall: it verifies the signature, reads `metadata.product`,
and forwards to that product's webhook with a per-product secret. Each product's handler
accepts a comma-separated list of secrets.

- **`metadata.product` at checkout must equal the name registered in the router**; the
  handler ignores any other product.
- **Don't create a fresh endpoint per product.** Every slot used is one the next product
  can't have, and two deliveries of one event can race the `pw_emailed` marker into a double
  email.
- **Probe it**: send a signed fake event for an unpaid session and expect a `not ours or not
  paid` reply — that proves both signature and routing, with no charge and no email.

## Rules, each with its why

1. **Check repo visibility before calling it done.** If the repo is public and its history
   ever held the full data, the paywall is decorative. Make it private
   (`gh repo edit --visibility private --accept-visibility-change-consequences`).
2. **One fixed price, one plain line. No badges, discounts or bundles.** Set the price at
   about a tenth of what one use is worth to the buyer. Write the arithmetic and the date in
   the README under "Price", **labelled a hypothesis**, so it can be revised on evidence.
3. **Put the recipient token in the path (`/for/<token>/`), not the query string.** Vercel
   Analytics drops `?query` and `#hash`; a path token is the only way to see which recipient
   opened it.
4. **A personalised page with no record of the reader's own is not sendable.** Hold it rather
   than showing them a generic example.
5. **Verify on the live site before reporting:**
   - `/api/data` returns 401 without a password.
   - `POST /api/checkout` returns a `cs_live_` client secret.
   - A comp password unlocks the full data.
   - The analytics tags show up in a curl of the page.
   - One page renders at 390 and 1440 wide.
   - **The paid bundle is NOT a static file:** curl `/api/%5Ffull/full.json.gz` and
     `/api/_full%2Ffull.json.gz` (and the plain path); each must be 307/404, never 200. A
     deploy that sets `outputDirectory: "."` (or uploads the whole folder) makes every file a
     URL, and exact-path redirects miss the `%5F` spelling. Fix: upload static files under
     `public/`, set `outputDirectory: "public"` in both the deploy payload and `vercel.json`,
     and ship the bundle only via the function's `includeFiles`. Add a test that the bundle
     path 404s. Static downloads don't appear in function logs, so a leak can't be audited
     after the fact.
   - **The host is a Stripe payment method domain** (`GET /v1/payment_method_domains`;
     `POST domain_name=<host>` if missing). Without it embedded Checkout silently hides Apple
     Pay and Google Pay, and phone buyers face a typed-card form and leave.
   - **Make no real payment.** The emailed password is then untested; say so.
6. **Done means committed, pushed and deployed.** Check the commit and the live response,
   not an agent's message saying it's done.

## Getting it to buyers

Pick the channel before writing the message. Whatever the channel: open on the reader's
own record (their listing, filing, menu price or site), then one fact your data adds, then
the link and the one price. Send one-to-one, in waves, verified addresses only, and read
visits, checkouts and replies on day 3 before sending wave 2. Fewer than ~50 recipients
across 3 segments is a probe, not a verdict.

## Known gaps

- The price is a hypothesis until real buyers pay or don't.
- Test the full purchase -> webhook -> email path at least once with a real (refunded)
  payment before trusting it.
