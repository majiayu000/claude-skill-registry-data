---
name: square-api
description: Read a Square seller's register (payments, orders, locations) through OAuth, and know how a third-party app gets paid on Square — "connect their Square", "pull daily sales from Square", "list on the Square App Marketplace", "does Square bill app subscriptions", "Square OAuth", "Square sandbox", "Square developer console". Carries the billing facts, the two marketplace gates, token lifetimes, pagination caps, and the shadow-DOM traps in the developer console.
---

# Square API

## The one fact: who bills the merchant for an app

**Square does, inside the seller's own Square account**, but only for a listed app.
*App Subscriptions* (developer.squareup.com/docs/app-marketplace/app-subscriptions/billing):
the developer sets a plan (free, monthly or annual, optional trial), the seller subscribes from
the listing, Square charges them every 30/365 days, and the money lands in the developer's
**Square Balance**. Fees: 2.9% + $0.30 per card payment; **20% revenue share** under the
Partner Integrated Marketplace Agreement, waived for the first year after launching App
Subscriptions. Failed payments do not auto-cancel; the seller gets an invoice.

**Two gates sit in front of it (both read 2026-11):**
1. A marketplace listing needs **five active Square sellers already using the app** (Square
   developer forum, 2025-04; no provisional listing). Onboard them from your own site first.
2. Square **paused onboarding new apps/partners for marketplace listing** (forum reply,
   2026-10-01). The Developer Console's App Marketplace → "+ New Submission" is the route when
   it reopens.

Until both open: bill through your own checkout (e.g. Stripe) on your own site and connect
Square by OAuth from there.

## Hosts

- Production API `https://connect.squareup.com`; OAuth page `…/oauth2/authorize`.
- Sandbox API `https://connect.squareupsandbox.com`; OAuth page on the same host.
  `session=false` is not supported in sandbox. Real sellers must use the production URL.
- Header on every call: `Square-Version: <date>` (pin the version the docs show when you build;
  2026-09-16 at the time of writing).

## OAuth (code flow, server-side)

Authorize URL params: `client_id` (the application id), `scope` (space-separated), `state`,
optional `session=false` (forces a fresh login), `redirect_uri` only if you registered more
than one. Read-only register scopes: `MERCHANT_PROFILE_READ PAYMENTS_READ ORDERS_READ`. The
code lasts **5 minutes**, once.

Token: `POST /oauth2/token` JSON `{client_id, client_secret, code,
grant_type:"authorization_code"}` → `{access_token, token_type:"bearer", expires_at (ISO),
merchant_id, refresh_token, short_lived:false}`. Access tokens live **30 days**; code-flow
refresh tokens do not expire (PKCE ones are single-use, 90 days). Refresh: same endpoint,
`grant_type:"refresh_token"`. Lose the refresh token and the seller has to re-authorize.

Marketplace review requires: access tokens AES-encrypted at rest with the key outside source
control, separate staging/production keys, the OAuth secret outside source control, and
exponential backoff on 429s (requirements changelog 2024-08-23). Build that in from day one.

## Reading the register

- `GET /v2/locations` → `locations[]` with `id`, `name`, `address{address_line_1, locality,
  administrative_district_level_1, postal_code}`, `status`, `type` (`PHYSICAL`/`MOBILE`),
  `timezone`, `mcc`.
- `GET /v2/payments?location_id&begin_time&end_time&limit=100&cursor` (RFC 3339, filtered on
  `created_at`; **limit caps at 100**, page by `cursor`). Sum `amount_money.amount` (cents)
  where `status == "COMPLETED"`; other statuses are `APPROVED`, `PENDING`, `CANCELED`,
  `FAILED`. `created_at` is UTC; shift to the location's `timezone` for a local "day".
- `POST /v2/orders/search` for itemised totals: `{location_ids:[…≤10], query:{filter:
  {date_time_filter:{closed_at:{start_at,end_at}}, state_filter:{states:["COMPLETED"]}},
  sort:{sort_field:"CLOSED_AT"}}, limit:500}`; `return_entries:true` gives ids only.
  Payments is enough for gross and count; Orders is for what sold.

## Driving the developer console (no API for most of it)

- Signup and every console form are `market-*` web components in **shadow DOM**. Light-DOM
  `querySelectorAll` sees nothing; walk `shadowRoot`s or use puppeteer `pierce/` selectors (one
  selector per `$$` call). Hidden checkbox inputs are zero-sized: click the `MARKET-CHECKBOX`.
- Email verification is a 6-digit code with a 5-minute expiry; the field is
  `pierce/input[autocomplete=one-time-code]` — focus it and press digit keys.
- The onboarding walkthrough is mandatory (every console URL redirects to it until done).
  Typed text does not reach Ember's model: set the inner input through the native value setter
  and fire composed `input`/`change` events, or Continue stays disabled. Skip/Continue sit low
  on the page: use a viewport ≥1100 px tall.
- OAuth tab: Sandbox/Production is a `MARKET-SEGMENTED-CONTROL`; click the `MARKET-SEGMENT`
  host from `evaluate` (a mouse click does not switch it). "Copy Application secret" writes to
  the clipboard: override `navigator.clipboard.writeText` first and read it back.
- Redirect URL: host `.click()` on the `market-link` "Update" opens the modal; set the field in
  ONE native-setter write to the full URL (clearing it to empty re-renders the modal away), then
  click **Confirm** (not Save). Verify with an in-page `fetch('/api/portal/oauth-clients')`,
  which returns `redirect_uri` — and the **plain application secret**, so never paste that JSON
  anywhere.
- Sign-in at `app.squareup.com/login`: email in `#mpui-combo-field-input` → Continue, password
  in `#password`, both via the native setter (`keyboard.type` on a set value doubles it;
  Cmd-A does not select inside the shadow input). A phone-OTP enrollment nag after login is
  skippable: "Remind me next time" → "Continue to Square".
- A second `puppeteer.connect` to the same Chrome can hang; relaunch on a new port with the
  same `--user-data-dir` to keep the session.
- The authorize page shows "<app> wants access to your Square Account" with Deny/Allow; a
  broken registered redirect shows nothing until after Allow, so the API read above is the
  real check.

Keep app ids, secrets and passwords in a gitignored `.env`, never in a skill.

## Related

`clover-api` for the other big register (open marketplace, 70% share); `browser-as-you` for
driving consoles; `product-paywall` for the Stripe side.
