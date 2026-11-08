---
name: jobber-api
description: Build or operate an app on Jobber (field-service CRM for home-service pros) — "list on the Jobber marketplace", "push leads into Jobber", "Jobber OAuth", "Jobber GraphQL", "Jobber app review", "Jobber Developer Center", "Jobber tester account". Covers why Jobber is the open door among field-service platforms, the GraphQL API's traps (refresh-token rotation, userErrors on HTTP 200, auto-stamped lead source), and the marketplace rules that block a draft app.
---

# Jobber API and App Marketplace

Why Jobber: among field-service platforms it is the open door for a new developer (read
2026-11). Housecall Pro has no open marketplace (API is per-account, top plan only);
ServiceTitan paused new applicants and charges dues plus revenue share. Jobber: 300k+ pros,
~100 apps, self-serve review, and its terms make the transaction between pro and app provider
(no revenue share found). You bill with your own checkout.

## Access

- Developer Center: developer.getjobber.com. **Turn on 2FA (TOTP)**: it is required to submit
  for review. Keep the TOTP seed in a gitignored `.env` so automation can produce codes.
- Testing needs a separate **developer tester account** (special signup link inside the
  Developer Center; the account lasts 90 days). Signup asks for a phone number — expect sales
  calls.

## API

- GraphQL, `POST https://api.getjobber.com/api/graphql`, headers `Authorization: Bearer
  <token>` and `X-JOBBER-GRAPHQL-VERSION: <date>` (e.g. 2025-04-16).
- OAuth 2.0 authorization code (PKCE works). Access token 60 min. **Refresh-token rotation:
  every refresh returns a new refresh token — store it or the next refresh fails.**
- Scopes are fixed at app creation; changing them means a new app.
- Throttle: 2,500 requests / 5 min plus GraphQL query cost (`extensions.cost`).
- Always read `userErrors` in mutation responses; HTTP is 200 even on failure.
- `clientCreate` needs `lastName` unless `isCompany: true` + `companyName`.
- **Your app's name is auto-stamped as the client's Lead Source and cannot be edited** — a free
  usage metric for anything that creates clients or requests.
- `requestCreate` takes `clientId` + `propertyId`; attach the "why" as a note.
- Handle the `APP_DISCONNECT` webhook (HMAC-verified) — review tests it.

## Marketplace rules (each costs a cycle if missed)

- A **Draft** app may connect at most **5 paying Jobber accounts**; more gets API access
  blocked. Route a sixth to a waitlist.
- No public announcement until approved. Don't recruit real Jobber customers to test without a
  Jobber developer rep.
- Review = "Request a review" in Manage Apps → pre-submission checklist → Jobber tests
  connect / disconnect / reconnect, data formatting, duplicate prevention, listing copy → **a
  review call with a human** → ~2-week beta with selected pros → public.
- Listing fields: name, developer, description, features/benefits, gallery, logo, optional
  Manage App URL.

## Distribution once live

On app marketplaces the durable plan is **reviews**: fast replies, features shipped the week
they are asked for, setup that works first try. Solo apps that grew mostly through one
marketplace (e.g. Zigpoll on Shopify) did exactly that for years.

## Related

`clover-api` and `square-api` for POS marketplaces; `browser-as-you` for the Developer Center.
