---
name: whop-payments-network
description: Integrate the Whop Payments Network into your platform — pay-ins, payouts, checkout, embedded components, API patterns, and webhooks.
---

# Whop Payments Network Integration

Whop provides a full payments network: accept payments (pay-ins), send payouts, embed checkout and wallet components, handle webhooks, manage connected accounts, and send notifications. This skill covers the patterns you need to integrate Whop into any platform.

## 1. SDK Packages

| Package | Purpose | Install |
|---------|---------|---------|
| `@whop/sdk` | Server-side API client (TypeScript) | `npm install @whop/sdk` |
| `whop-sdk` | Server-side API client (Python) | `pip install whop-sdk` |
| `whop_sdk` | Server-side API client (Ruby) | `gem install whop_sdk` |
| `@whop/checkout` | Embedded checkout React component | `npm install @whop/checkout` |
| `@whop/embedded-components-react-js` | Embedded payout/wallet/KYC/chat components (React) | `npm install @whop/embedded-components-react-js` |
| `@whop/embedded-components-vanilla-js` | Embedded components (Vanilla JS) | `npm install @whop/embedded-components-vanilla-js` |

## 2. SDK Setup

Base URL: `https://api.whop.com/api/v1`

```typescript
import Whop from "@whop/sdk";

// Company API Key — access your own company's data or connected accounts
const client = new Whop({
  apiKey: process.env.WHOP_API_KEY,
  // appID is NOT required for Company API Keys
});

// App API Key — access data on companies that installed your app
const appClient = new Whop({
  apiKey: process.env.WHOP_API_KEY,
  appID: "app_xxxxxxxxxxxxxx",
});
```

For webhook verification, add the webhook secret:

```typescript
const client = new Whop({
  apiKey: process.env.WHOP_API_KEY,
  webhookKey: btoa(process.env.WHOP_WEBHOOK_SECRET || ""),
});
```

## 3. Authentication

### API Key Types

| Type | When to use | How to get |
|------|-------------|------------|
| **Company API Key** | Your own company data, connected accounts, platform operations | Dashboard > Developer > Company API Keys |
| **App API Key** | Access data on companies that installed your app | Dashboard > Developer > Create App > Env Vars |
| **OAuth Token** | Act on behalf of a specific user | OAuth 2.1 + PKCE flow |

### OAuth / NextAuth v5 OIDC

Key config: `type: "oidc"`, `issuer: "https://api.whop.com"`, `token_endpoint_auth_method: "none"`, `id_token_signed_response_alg: "ES256"`, `checks: ["pkce", "nonce"]`. Profile fields: `sub`, `name`, `email`, `picture`, `username`.

> **Note:** OAuth/OIDC is still marked "in development" in official docs. The NextAuth pattern works but may change.

### Admin Authorization

```typescript
const access = await client.users.checkAccess(companyId, { id: userId });
```

## 4. Architecture Patterns

### Pattern A: Stateless / No-Database Architecture

Use Whop entities as your datastore instead of running your own database:

| Your concept | Whop entity | Store custom data via |
|--------------|-------------|----------------------|
| User accounts | Companies | `metadata` on company |
| Listings / catalog items | Products | `description` (can store JSON) |
| Pricing / variants | Plans | plan fields + `metadata` |
| Purchases / bookings | Memberships | membership lookup |

This works well for marketplaces, booking platforms, and listing sites where Whop handles all transactional state.

### Pattern B: Two-Sided Marketplace (Connected Accounts)

Each vendor/creator gets a child company. Platform takes `application_fee_amount` on checkouts:

```typescript
const vendor = await client.companies.create({
  parent_company_id: "biz_yourplatform",
  email: "vendor@example.com",
  title: "Vendor Store",
  metadata: { vendor_tier: "gold" },
});

const checkout = await client.checkoutConfigurations.create({
  company_id: vendor.id,
  mode: "payment",
  redirect_url: "https://yourplatform.com/complete",
  plan: {
    company_id: vendor.id, product_id: "prod_xxx",
    initial_price: 5000, plan_type: "one_time", currency: "usd",
    visibility: "hidden", release_method: "buy_now",
    application_fee_amount: 500, // must be > 0 AND < total
  },
});
// Dynamic fees: Math.round(price * (tier === "gold" ? 0.05 : 0.10))
```

### Pattern C: Platform Treasury Model

All payments go to the platform. Platform distributes via transfers after admin approval:

```typescript
// 1. Checkout to platform (no application_fee)
const checkout = await client.checkoutConfigurations.create({
  company_id: "biz_yourplatform",
  plan: { initial_price: 5000, plan_type: "one_time" },
});
// 2. Check balance
const ledger = await client.ledgerAccounts.retrieve("biz_yourplatform");
// 3. Transfer to vendor
const transfer = await client.transfers.create({
  amount: 4500, currency: "usd",         // amount in CENTS
  origin_id: "biz_yourplatform", destination_id: "biz_vendor",
  metadata: { order_id: "order_123" }, notes: "Payout for order #123",
  idempotence_key: "transfer_order_123", // prevents duplicates
});
```

## 5. Products & Plans

### Products API

Products are the catalog layer above plans. A product has multiple plans (pricing variants).

> Use `product_id` to link a plan to a product. `access_pass_id` is a legacy alias — prefer `product_id` for new integrations.

```typescript
const product = await client.products.create({
  company_id: "biz_xxx",
  title: "Premium Course",
  description: JSON.stringify({ category: "education", level: "advanced" }), // can store JSON
  visibility: "visible", // or "hidden"
});
await client.products.update(product.id, { title: "Updated Title" });
const products = await client.products.list({ company_id: "biz_xxx" });
```

### Plans API

```typescript
// One-time payment plan
const plan = await client.plans.create({
  company_id: "biz_xxx",
  product_id: "prod_xxx",
  initial_price: 2999,     // $29.99
  plan_type: "one_time",
  currency: "usd",
  visibility: "visible",   // or "hidden" for checkout-only plans
  release_method: "buy_now",
});

// Subscription plan
const subPlan = await client.plans.create({
  company_id: "biz_xxx",
  product_id: "prod_xxx",
  plan_type: "renewal",
  initial_price: 999,
  renewal_price: 999,
  billing_period: 30,       // days
  currency: "usd",
});

// Limited stock plan (inventory)
const limitedPlan = await client.plans.create({
  company_id: "biz_xxx",
  product_id: "prod_xxx",
  initial_price: 4999,
  plan_type: "one_time",
  stock: 100,               // sold out after 100 purchases
});

console.log(plan.purchase_url); // shareable checkout link
```

### Async Iteration for Paginated Results

All `.list()` methods return async iterators:

```typescript
for await (const product of await client.products.list({ company_id: "biz_xxx" })) {
  console.log(product.title);
}

for await (const company of await client.companies.list({ parent_company_id: "biz_xxx" })) {
  console.log(company.title, company.metadata);
}
```

## 6. Checkout

### Option A: Checkout Links (Simplest)

Create a plan, redirect to `plan.purchase_url`. Sandbox: `https://sandbox.whop.com/checkout/{plan.id}`.

### Option B: Embedded Checkout (Custom UI)

**Server — create checkout configuration:**

```typescript
const config = await client.checkoutConfigurations.create({
  company_id: "biz_xxx",
  mode: "payment",
  redirect_url: "https://yoursite.com/complete",
  plan: {
    company_id: "biz_xxx",
    product_id: "prod_xxx",
    initial_price: 1000,
    plan_type: "one_time",
    currency: "usd",
    visibility: "hidden",
    release_method: "buy_now",
    application_fee_amount: 100, // optional platform fee
  },
  metadata: { order_id: "order_123" },
});
// config.id = sessionId for client
// config.purchase_url = direct link
// config.plan.id = created plan ID
```

**Client — render embed:**

```tsx
import { WhopCheckoutEmbed } from "@whop/checkout/react";

<WhopCheckoutEmbed
  sessionId={config.id}
  returnUrl="https://yoursite.com/complete"
  environment="production"  // or "sandbox"
  themeOptions={{ accentColor: "#FF6243", highContrast: true }}
  onComplete={(paymentId) => console.log("Paid:", paymentId)}
/>
```

In production, `redirect_url` must be HTTPS. Localhost (HTTP) works in sandbox but will be rejected in production.

Or use `planId` directly (no server config needed):

```tsx
<WhopCheckoutEmbed
  planId="plan_xxx"
  returnUrl="https://yoursite.com/complete"
  environment="sandbox"
/>
```

### Option C: Aggregated Cart Checkout

Aggregate cart total into one checkout, serialize items in `metadata.cart`:

```typescript
const total = cartItems.reduce((sum, i) => sum + i.price * i.qty, 0);
const config = await client.checkoutConfigurations.create({
  company_id: "biz_xxx",
  plan: { initial_price: total, plan_type: "one_time" },
  metadata: { cart: JSON.stringify(cartItems) },
});
```

### Option D: Vanilla JS Checkout

```html
<script async defer src="https://js.whop.com/static/checkout/loader.js"></script>
<div
  data-whop-checkout-plan-id="plan_xxx"
  data-whop-checkout-return-url="https://yoursite.com/complete"
></div>
```

See `references/checkout_embed.md` for full prop reference, programmatic controls, and sandbox testing.

## 7. Connected Accounts

```typescript
// Create
const company = await client.companies.create({
  parent_company_id: "biz_yourplatform",
  email: "creator@example.com", title: "Creator Store",
  metadata: { tier: "free" },
});
// List (async iterator)
for await (const co of await client.companies.list({ parent_company_id: "biz_yourplatform" })) {
  console.log(co.id, co.title);
}
// Update metadata (SDK typing gap — use type cast)
await (client.companies as any).update(company.id, { metadata: { tier: "premium" } });
```

### Account Onboarding & KYC

```typescript
// use_case: "hosted_kyc" | "hosted_payouts" | "account_onboarding"
const link = await client.accountLinks.create({
  company_id: "biz_xxx", use_case: "hosted_kyc",
  return_url: "https://yourplatform.com/dashboard",
  refresh_url: "https://yourplatform.com/refresh",
});
// Redirect to link.url
```

### Ledger & Verification: `await client.ledgerAccounts.retrieve("biz_xxx")` — returns balances, KYC status, payments_approval_status.

## 8. Payouts

### Funding Your Platform Balance (Top-ups)

Before you can send transfers to connected accounts, your platform needs a positive balance. Use the Top-ups API to add funds by charging a saved payment method. **Top-ups have no fees.**

```typescript
// 1. First, save a payment method via the Whop Dashboard (Settings > Payment Methods)
// 2. Then top up programmatically:
const topup = await client.topups.create({
  company_id: "biz_your_platform",
  amount: 50000, // $500.00 in cents
  currency: "usd",
  payment_method_id: "pm_saved_method_id",
});
// Listen for payment.succeeded webhook to confirm
```

**Three ways money enters a platform:**
1. **Top-ups** — charge a saved payment method (ACH, card). Best for platforms that collect funds externally (wire, invoice) and need to fund their Whop balance for payouts.
2. **Direct charges** — customers pay connected accounts directly, platform takes an `application_fee_amount`. Money flows through checkout.
3. **Transfers model** — customers pay the platform via checkout, platform distributes to connected accounts via `transfers.create()`.

See [Add funds to your balance](https://docs.whop.com/developer/platforms/add-funds-to-your-balance) for full guide.

### Embedded Payout Components (React)

```tsx
import { PayoutsSession, VerifyElement, AddPayoutMethodElement } from "@whop/embedded-components-react-js";
import { loadWhopElements } from "@whop/embedded-components-vanilla-js";

const elements = loadWhopElements({ environment: "production" }); // or "sandbox"
// Server: const token = await client.accessTokens.create({ company_id: "biz_vendor" });

function VendorPayouts({ token, companyId }: { token: string; companyId: string }) {
  return (
    <PayoutsSession token={token} companyId={companyId} redirectUrl="/dashboard">
      <VerifyElement />
      <AddPayoutMethodElement />
      {/* Also: BalanceElement, WithdrawElement, PayoutMethodsElement */}
    </PayoutsSession>
  );
}
```

### Check Payout Method

```typescript
const methods = await client.payoutMethods.list({ company_id: "biz_xxx" });
const hasDefault = methods.some((m: any) => m.is_default);
```

### Transfers (cents) & Withdrawals (dollars)

```typescript
// Transfers — amount in CENTS
await client.transfers.create({
  amount: 4500, currency: "usd",
  origin_id: "biz_platform", destination_id: "biz_vendor",
  metadata: { order_id: "order_123" }, notes: "Weekly payout",
  idempotence_key: "payout_week12_vendor456",
});
// Withdrawals — amount in DOLLARS (different!)
await client.withdrawals.create({ company_id: "biz_xxx", amount: 45.00 });
```

See `references/payouts.md` for hosted payouts, embedded wallet components, and the interactive playground.

## 9. Webhooks

**Setup:** Dashboard > Developer > Create Webhook > select events > provide URL.

```typescript
import type { NextRequest } from "next/server";
import { whopsdk } from "@/lib/whop-sdk";

export async function POST(request: NextRequest): Promise<Response> {
  const body = await request.text();
  const headers = Object.fromEntries(request.headers);
  const webhookData = whopsdk.webhooks.unwrap(body, { headers });

  // GOTCHA: event field is `event`, not `type`
  // GOTCHA: events may arrive with underscores: "membership_went_valid"
  const eventType = webhookData.event.replace(/_/g, "."); // normalize

  switch (eventType) {
    case "payment.succeeded":
      // handle payment
      break;
    case "membership.went.valid":
      // handle activation
      break;
  }

  return new Response("OK", { status: 200 }); // return 2xx quickly!
}
```

See `references/webhooks.md` for all events, company vs app webhooks, and validation.

## 10. Notifications

Send push notifications to users with deep linking:

```typescript
await client.notifications.create({
  company_id: "biz_xxx",
  user_id: "user_xxx",
  title: "Your order shipped!",
  content: "Track your order in the app.",
  rest_path: "/orders/order_123", // deep link path within your app
});
```

## 11. Chat SDK

Embed real-time chat via `ChatElement` inside `ChatSession` + `Elements` wrappers. See `references/chat_sdk.md` for React, Vanilla JS, and Swift examples.

## 12. Common Gotchas

1. **Transfers use cents, Withdrawals use dollars** — `transfers.create({ amount: 4500 })` = $45.00, but `withdrawals.create({ amount: 45 })` = $45.00.
2. **`application_fee_amount` must be > 0 AND < total price** — zero or equal-to-total will error.
3. **Webhook `event` field, not `type`** — The webhook body uses `event` as the key. Some docs incorrectly show `type`.
4. **Webhook events may use underscores** — `membership_went_valid` instead of `membership.went.valid`. Normalize with `.replace(/_/g, ".")`.
5. **`returnUrl` is required for external payment methods** — Apple Pay, Google Pay, PayPal redirects fail without it.
6. **Webhook secret must be base64-encoded** — Pass `btoa(process.env.WHOP_WEBHOOK_SECRET)` to SDK's `webhookKey`.
7. **Return 2xx quickly from webhooks** — Whop retries on timeout. Use `waitUntil()` or background jobs for heavy processing.
8. **Access tokens expire** — Default 1 hour, max 3 hours. Refresh before expiry for embedded components.
9. **Company metadata SDK typing gap** — Update metadata via type cast: `(client.companies as any).update(id, { metadata })`.
10. **SDK init without appID is valid** — Company API Keys don't need `appID`.
11. **Checkout config response includes `purchase_url` and `plan.id`** — Use these for redirect flows or plan references.
12. **Sandbox checkout URL** — `https://sandbox.whop.com/checkout/{planId}`.
13. **`setupFutureUsage: "off_session"`** — Required on checkout embed when you plan to charge the user later via `chargeUser` API.
14. **Permission re-approval** — After adding new app permissions, API calls fail with `403` until the company re-approves.
15. **Always use idempotence keys** — On transfers and any money-movement operation to prevent duplicates.
16. **Payout methods pagination duplicates** — Payout methods list may return duplicates during pagination — deduplicate by `.id` when consuming the full list.
17. **Auto-withdraw after transfer** — After approving a transfer, consider auto-initiating a withdrawal to the recipient's default payout method so they don't have to manually withdraw. Note: transfers use cents, withdrawals use dollars.

## 13. Permissions System

Apps must request permissions before accessing company data. Each API endpoint has required scopes.

**Setup:** Dashboard > Developer > App > Permissions tab > Add permissions with justification > Install app > Approve.

When updating permissions, creators see a "Re-approve" button. Handle `403` errors gracefully until re-approved.

## 14. MCP Server Access

| Transport | URL |
|-----------|-----|
| HTTP Streaming (Cursor) | `https://mcp.whop.com/mcp` |
| SSE (Claude) | `https://mcp.whop.com/sse` |
| Docs MCP | `https://docs.whop.com/mcp` |

## 15. Reference Files

| File | Contents |
|------|----------|
| `references/checkout_embed.md` | Full prop reference, programmatic controls, Vanilla JS, sandbox, Apple Pay |
| `references/payouts.md` | Embedded wallet components, hosted payouts, account links, playground |
| `references/chat_sdk.md` | Chat SDK for React, Vanilla JS, Swift with full examples |
| `references/api_reference.md` | SDK initialization, key endpoints, MCP server setup |
| `references/webhooks.md` | Webhook events, validation, company vs app webhooks |
| `codebase_scan.md` | Prompt to analyze a client's codebase for Whop integration planning |
