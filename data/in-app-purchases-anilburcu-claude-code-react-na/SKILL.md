---
name: in-app-purchases
description: In-app purchases and subscriptions with RevenueCat. Use for paywalls, odd sandbox behavior, premium not arriving after purchase, webhook verification, restore and transfer flows.
user-invocable: false
---

# Subscriptions without 2 AM incidents

## The architecture rule everything else hangs on

Entitlement truth lives on your server, not in the client. The purchase SDK tells the client "probably premium" fast; the webhook pipeline tells your database "actually premium" reliably. The client renders from server state and treats its local SDK state as an optimistic hint.

Every horror story in this domain is a variation of trusting the client: premium flags in AsyncStorage, entitlement checks that only run at purchase time, or webhook handlers that were never verified against replay.

## RevenueCat wiring that holds up

- Identify the user to the SDK with your own auth user id after sign-in. Anonymous ids merging into identified ids is where "user bought on the wrong account" tickets are born.
- Configure once at startup with the platform key; render from `customerInfo` listeners rather than one-shot fetches, so a purchase completing in the background updates the UI without a restart.
- Decide your transfer policy consciously. "Transfer to new app user id" versus blocking transfers changes what happens when one store account signs into a second app account. Whichever you pick, enforce ownership rules in your own database guards; the SDK setting alone is not a policy.
- Restore purchases must be a visible button (App Store review expects it) and must resolve through the same server-side reconciliation as a fresh purchase.

## Webhooks: the part that must be boring

- Verify the sender on every request. RevenueCat gives you two checks: the Authorization header value configured in the dashboard (compare the whole string), and optional HMAC signing, which adds `X-RevenueCat-Webhook-Signature: t=<unix seconds>,v1=<hex>` where v1 is HMAC-SHA256 over `<t>.<raw body>` with the signing secret. Turn signing on, verify against the raw request bytes before any JSON parsing, and reject timestamps outside a few minutes; the secret is shown once at creation, so store it immediately. An unverified webhook endpoint is an open "make me premium" API.
- Answer fast. RevenueCat disconnects after 60 seconds and retries a failed or timed-out delivery up to 5 times with growing delays (5, 10, 20, 40, 80 minutes), then gives up. A slow handler therefore produces duplicates first and lost events second: commit the dedupe record and the upsert, return 200, and push anything slow (email, analytics, CRM sync) to a queue.
- If the endpoint runs on a platform that enforces its own auth by default (Supabase Edge Functions and their JWT verification, for example), remember the store's webhook sender cannot present your platform's JWT. Shared-secret endpoints must have platform JWT verification disabled and their own secret check enabled, or every event bounces with 401 and premium "never arrives".
- Deduplicate by event id. Webhook senders retry; your handler will see the same event twice on a bad day.
- Store the environment (SANDBOX vs PRODUCTION) on every event and subscription row, and filter sandbox out of admin dashboards and metrics. Mixed environments make revenue numbers lie.
- Reconcile, don't accumulate: handlers should upsert the subscription to the state the event describes, so replays and out-of-order deliveries converge instead of corrupting.
- A runtime-neutral handler skeleton with the dedupe and transaction contracts spelled out is in [reference.md](reference.md).

## Sandbox behavior that looks like a bug but is not

- Sandbox subscriptions renew on an accelerated clock (a monthly plan renews in minutes, and the speed is adjustable in App Store Connect) and stop after a fixed number of renewals, so expiry during a test session is expected. TestFlight runs its own accelerated, daily-capped renewal schedule; do not read either as production timing.
- Test with multiple store accounts and record which store each test row came from. Cross-platform testing (one user, App Store purchase, Play restore attempt) is where ownership policies show their true behavior.
- iOS: purchases in TestFlight builds use sandbox. A "works in TestFlight, broken in production" report is usually an environment-filtering bug in your pipeline, not a store bug.
- A StoreKit configuration file enables local purchase testing in the simulator with no sandbox account, which is the fastest loop for paywall UI work. Treat your webhook pipeline as unverified until a real sandbox purchase has run end to end; local StoreKit testing is for the client loop, not for proving the server side.

## The purchase flow's unhappy paths, all of which will happen

- Purchase succeeds, network drops before your server hears about it: the client must not be the only messenger. The webhook arrives independently, and the client reconciles on next launch via the customer info listener. Design for "server knows before the client does" and this case disappears.
- Purchase cancelled by the user: not an error. Do not log it as one or your error budget drowns.
- Pending / deferred states (ask-to-buy, slow card processing on Play): render "purchase pending" honestly instead of failing.
- Billing retry and grace periods: decide explicitly whether grace period keeps access (usually yes) and encode it server-side, driven by the webhook event types, not by client guessing.

## Debugging "premium didn't arrive", in order

1. Did the webhook arrive at all? Check the sender's event delivery log first; a 401 there ends the investigation immediately (see the JWT note above).
2. Did the handler verify, dedupe and upsert? Read the handler's log for this event id.
3. Environment mismatch: sandbox event, production query, or the reverse.
4. Identity: which app user id was attached to the purchase? Anonymous-id purchases explain most "bought but not premium" cases.
5. Only after those four: suspect the client's entitlement rendering.
