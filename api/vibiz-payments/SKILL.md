---
name: vibiz-payments
description: Use when editing pricing, offers, checkout CTAs, payment links, redirects, or revenue-related UI in the Vibiz sandbox template.
compatibility: opencode
---

# Vibiz Payments

The customer site must stay Stripe-free. Vibiz owns Stripe products, prices, Payment Links, webhooks, attribution, refunds, and reporting in the parent app. This sandbox template only renders platform-minted links.

Before editing payment surfaces, read:

- `src/lib/offers.ts`
- `src/lib/entitlements.ts`
- `src/lib/vibiz-runtime.ts`
- `src/components/EntitlementGate.tsx`
- `src/app/payment-success/page.tsx`
- `src/components/landing/pricing.tsx`
- `data/offers.json`
- `template.config.ts`

Rules:

- Never install or import the `stripe` SDK.
- Never create `lib/stripe.ts`, `/api/stripe/*`, checkout-session routes, webhook routes, or payment-intent code.
- Never add `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, or secret Stripe values to any file.
- Never modify `data/offers.json`; it is seeded by Vibiz on sandbox bootstrap and deploy.
- Render real checkout CTAs with `href={offer.paymentLinkUrl}` when seeded offers exist.
- Gate paid post-checkout features with `offer.entitlementKey`, `src/components/EntitlementGate.tsx`, or the helpers in `src/lib/entitlements.ts`; those helpers revalidate the local entitlement with Vibiz before unlocking.
- Keep `/?payment=success&claim=...` as the legacy-safe Stripe landing URL and `/payment-success?claim=...` as the Vibiz claim exchange route. The root page forwards claims to `/payment-success`, which calls the Vibiz runtime claim endpoint, stores the returned entitlement locally, and future visits unlock only after Vibiz runtime revalidation succeeds.
- Keep the `NEXT_PUBLIC_VIBIZ_DEPLOY === "1"` behavior: Vibiz-managed deployments must not show placeholder pricing when offers are missing.
- If offers are empty on a Vibiz-managed deployment, show a truthful empty state instead of fake tiers.

Verification:

- Search for forbidden Stripe additions with `rg -n "stripe|STRIPE|checkout.session|payment_intent|/api/stripe"`.
- Run `npm run build` after code changes.
- Confirm customer-visible CTAs still point at seeded `paymentLinkUrl` values, not locally generated checkout URLs.
