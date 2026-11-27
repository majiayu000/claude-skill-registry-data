---
name: sell
description: "Take money from Germany: Stripe Checkout, subscriptions, digital or physical products, shop law, go-live. Use for any billing, shop or pricing work."
---

# Sell

What works, as of 2026-10-03:

- **Digital payments** were proven in yverse-studio/duo-test.
- **The shop templates** (`templates/`) are tested; `stripe-workers.md` (Verified) says how.
- **The legal and tax facts** were researched and fact-checked.

This is not legal or tax advice. The kit says what is required. Claude writes the legal texts
in-house (the `legal` skill; official model texts word for word); a paid legal-text service comes
in once sales do. Tax questions go to a Steuerberater.

Files next to this one:

| File | Read it when |
|---|---|
| `recheck.md` | first, every new project: dated facts and where to confirm them |
| `keys.md` | writing the key card for the slice that takes money, and at go-live |
| `stripe-workers.md` | building checkout, webhook and tests; it lists `templates/`. Deploys and previews: the `publish` skill |
| `physical.md` | anything gets shipped |
| `legal-de.md` | legal pages, checkout wording, registrations |

Also turn on the official Stripe plugin in the project (`"stripe@claude-plugins-official": true`
in `.claude/settings.json`) and follow its `stripe-best-practices` skill; it is Stripe's own
integration plan. Its MCP server (`mcp.stripe.com`) needs a browser login, so it works on
yskills' PC (`/mcp`), not in cloud threads; the skill works everywhere.

## 0. Re-check

Open `recheck.md` and follow its first paragraph. If a fact changed, fix this skill in the same
PR.

## 1. What is sold decides the stack

| Selling | Payments | VAT | Fulfilment |
|---|---|---|---|
| Digital, one-off (unlock, download, credits) | Stripe Checkout, hosted page, `mode: 'payment'` | Kleinunternehmer: none. Selling across the EU above the threshold: Stripe Managed Payments (Stripe is the seller and handles VAT; digital only, +3.5%) | Grant access from the webhook |
| Subscription (web and installable web app; store apps: `store` skill) | Checkout `mode: 'subscription'`, Stripe Customer Portal, the Better Auth Stripe plugin | Same as above | Access while the subscription is active. Add a Kündigungsbutton |
| Physical goods | Our order page (address, shipping, the order button), then the Stripe-hosted page to pay | Kleinunternehmer: none. Otherwise Stripe Tax plus OSS. No merchant-of-record service takes physical goods | Order in D1, then Sendcloud, then yskills prints the label |
| Many products, variants, stock, or someone else runs the shop | Shopify instead of building one | Shopify Tax | Shopify |

- **Selling a game or other digital product on itch.io or Steam as well:** itch.io has two modes (you are the seller and handle VAT yourself, or itch.io is the merchant of record) and collects VAT automatically only in the second; use it as a store page, Stripe Checkout stays our own checkout. **Keep the price the same on Steam and on our own site** (Steam's parity rule is written for Steam keys sold elsewhere; whether it reaches a key-less own site is disputed), and do not link to our shop from inside the Steam build. Read the Steamworks terms before launch. Detail and sources: `docs/research/2026-11-10-paid-games-and-service.md`.
- Turn payment methods on in the Stripe Dashboard: cards, Apple Pay and Google Pay, PayPal,
  Klarna, SEPA. The hosted page then shows them with no extra code. giropay no longer exists.
- **Why the hosted page:** it has no monthly fee and the lowest fees. Stripe.js never loads on
  our pages, which keeps the cookie banner question simple. Stripe handles PCI.
- **The order button is always on our page.** It must say "Zahlungspflichtig bestellen"
  (§ 312j BGB), and Stripe's hosted button can only say "Bezahlen". This applies to digital
  products too.
- Never build our own card processing.
- **Subscriptions:** where the paywall shows, the 14-day trial (`subscription_data.trial_period_days`)
  and annual first follow the `store` skill's paywall defaults, on the web too.

## 2. Questions when the money slice starts

Asked when the slice that takes money starts (`operator/run.md` step 1: no grill batch, never
mid-build). Claude fills every item it can decide with the recommended pick and says it in one line;
only what it cannot know (what is sold, the prices, what exists already) goes to yskills, as a key
card.

1. What is sold: digital, subscription, physical, or a mix. Multi-select.
2. Prices. For physical goods, also:
   - parcel size and weight;
   - where to ship: Germany only (recommended first), DE + EU, or worldwide.
3. Kleinunternehmer (§ 19 UStG)?
   - Yes. Recommended to start; it means no VAT on prices.
   - No.
   - Not sure. Then use yes, and confirm with a Steuerberater.
4. What exists already. Checkboxes:
   - Gewerbe registered
   - Stripe account
   - Sendcloud account
   - legal-text service
   - business bank account
5. Physical only. Checkboxes:
   - your own product (you are the manufacturer: GPSR duties, see `legal-de.md`)
   - bought from a maker
   - contains electronics
   - contains batteries
   - food or cosmetics (stop and research; extra law applies)
6. Legal texts. Claude writes them (default), or a legal-text service yskills already has.

In the same message, ask for this project's keys from `keys.md`:

- Use the message template in `keys.md`. The Worker's secrets can only be set after the repo is
  imported in Workers Builds, so that batch asks for the values and names the dashboard page.
- Ask for test keys only now. Live keys come at go-live.
- Building does not wait for keys. Until they arrive, payment slices are tested with signed fake
  webhooks.

## 3. Build in thin slices, riskiest first

1. **Products and prices live on the server** (`shared/`).
   - The client sends ids and quantities, never a price.
   - For physical goods, also store the weight.
2. **Order page and order endpoint.**
   - The page shows what `legal-de.md` lists and ends in "Zahlungspflichtig bestellen".
   - The endpoint prices the order on the server, writes a `pending` order and returns the
     hosted Checkout URL. The order id becomes `client_reference_id`.
   - Copy `templates/` (see `stripe-workers.md`).
3. **Webhook.**
   - Trust signed events only. Read the raw body.
   - Make it idempotent: a guarded `UPDATE ... WHERE status = 'pending'` or a unique session id.
   - Fulfil only when `payment_status === 'paid'`. SEPA pays later, through
     `checkout.session.async_payment_succeeded`.
   - Handle failed and expired sessions, refunds and disputes.
4. **Return page.** It retrieves the session for instant feedback, because the webhook can lag.
   It records the payment through the same idempotent function the webhook uses.
5. **Fulfilment.**
   - Digital: grant access.
   - Physical: hand the order to Sendcloud from `fulfilOrder`, which runs with `waitUntil`
     after the 2xx. See `physical.md`.
6. **Emails.**
   - Send the order confirmation from our own sender (Resend, via `toolbox`). It must carry the
     AGB, the Widerrufsbelehrung and the Muster-Widerrufsformular, because the law wants them
     on a durable medium.
   - Sendcloud sends the shipping and tracking emails.
   - Stripe sends the receipt or invoice.
7. **Legal pages and checkout wording.** See `legal-de.md`. Covers Impressum, Datenschutz, AGB,
   Widerruf with the Widerrufsbutton, shipping and payment information, and prices with
   shipping and delivery time.
8. **Orders view** for yskills behind the admin login: paid, shipped, refunded. Refunds happen
   in the Stripe Dashboard and come back by webhook.
9. **Report into HQ:** each paid and refunded order shows in the project's HQ rows
   (`docs/hq-rows.md`, revenue verified against real data).

Tests that every shop gets (all in `templates/tests/shop.spec.ts`):

- A signed fake webhook marks an order paid exactly once, even when it is sent twice.
- A paid session that is not the order's own never pays it.
- An unsigned or forged webhook gets 400.
- A price sent by the client is ignored.
- SEPA order: `completed` unpaid, then `async_payment_succeeded`, then paid.
- A refund event flips the status.
- The checkout endpoint rejects:
  - unknown products and quantities of 0 or below;
  - orders too heavy for any shipping rate;
  - countries we don't ship to;
  - malformed postal codes and control characters.
- A valid order against stripe-mock is stored as `pending` with its session id.

Run `security-reviewer` on every slice that touches money or addresses.

## 4. Go live

Claude prepares everything, then posts one manual-steps message.

**Claude does, once the test key and the sandbox webhook secret are in Production:** one real
sandbox checkout end to end on the live URL (previews have no Stripe key): order page, Stripe page
with test card `4242 4242 4242 4242`, webhook, email. stripe-mock only checks parameter names.

**Claude does before the live key** (with yskills' OK: it deletes rows):

1. Checks that no placeholder is left (`example-mug`, `Beispielshop`, `example.de`) and that
   checkout, confirm and withdrawal use the rate-limit binding.
2. Adds a one-off migration `DELETE FROM orders WHERE livemode = 0 OR livemode IS NULL` in a PR;
   after the gate's merge it reads the `Workers Builds: <worker>` check: `npm run deploy` applies it. This has to happen
   before the live key, because a live order is also `livemode IS NULL` until it is paid.

**yskills does** (deep links are in `keys.md` and `legal-de.md`):

1. Gewerbe and the ELSTER questionnaire, if not done.
2. Activate the Stripe account.
3. Worker → Settings → Build → turn off non-production branch builds (`publish` skill), so only
   merged code ever runs with the live key.
4. In live mode, create the restricted key and the webhook endpoint (`keys.md`), and put
   `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` into the Worker's Production secrets.
5. Approve the legal texts.
6. Physical goods: register in LUCID and license the packaging before the first parcel.

**Claude does after:**

1. Checks the live site:
   - a Checkout Session opens in live mode;
   - the legal pages are linked from every page;
   - the order button, shipping costs and delivery time read right.
2. Asks yskills to buy once with their own card and refund it in the Stripe Dashboard, then checks
   that the orders view shows it paid and then refunded and that the emails arrived. yskills checks
   the Sendcloud entry in the panel.

## 5. Keep it working

- **Live smoke test** (the `publish` skill's `live.yml` pattern: after every deploy of `main` and
  every Monday, holding no keys). Once the test key is in, add checks that:
  - open the shop;
  - create a Checkout Session (nothing is charged; it expires);
  - send an unsigned webhook and expect 400;
  - get 200 from the legal pages.
  A failed run emails yskills.
- Stripe emails yskills when a webhook endpoint keeps failing. PostHog alerts on errors.
- When a rule or a price in this kit turns out wrong, fix it in yverse-studio/claude-setup.
