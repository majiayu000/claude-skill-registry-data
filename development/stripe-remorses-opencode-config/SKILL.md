---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: stripe
description: >
  Stripe billing patterns for spiceflow + Drizzle apps. Covers creating
  products and prices via the Stripe CLI with stable lookup keys, multi-currency
  USD+EUR pricing, monthly/yearly subscriptions, type-safe Checkout and Billing
  Portal integration in spiceflow routes, webhook handling, and the rules for
  preventing double customers and double subscriptions in the database. Load
  this skill whenever adding, modifying, or debugging any Stripe code (prices,
  checkout sessions, portal sessions, webhooks, subscription logic).
---

# Stripe

Use **Stripe Checkout** for new purchases and the **Stripe Billing Portal** for subscription management (upgrade, downgrade, cancel, switch monthly↔yearly). Do not build a custom billing UI.

Core rules, in priority order:

1. **One Stripe customer per `Org`**. Store the customer id in `Org.stripeCustomerId` and reuse it on every checkout/portal call.
2. **Prefer `lookup_key`** over hardcoded `price_xxx` ids. Fetch prices at runtime when possible.
3. **Every Price uses `currency_options` for EUR** on top of a USD base. Same integer value for both — see [Multi-currency](#multi-currency).
4. **One active Subscription row per `Org`**. Before creating a checkout session, check the DB and redirect existing subscribers to the portal instead.
5. **All Stripe-facing HTTP code lives inside spiceflow sub-apps** (`website/src/lib/spiceflow-*.tsx`). Not react-router actions. The webhook route is also a spiceflow route — spiceflow handlers receive a standard `Request` object, so `await request.text()` gives the raw body needed for Stripe's signature verification.
6. **Return errors as values, never throw.** All Stripe/Drizzle calls are wrapped with `.catch()` into tagged errore errors (`StripeApiError`, `DbError`, `PriceNotFoundError`, etc.). `constructEvent` and other sync-throwing APIs go through `errore.try`. Handlers check `instanceof Error`, early-return, and map errors to HTTP responses via `errore.matchError` at the HTTP boundary only. **Always read the [errore skill](../errore/SKILL.md) before writing or modifying error handling code in Stripe routes** — it covers tagged errors, `.catch()` boundary rules, flat control flow, cause chains, and the `matchError` exhaustive handler.

## CLI auth via sigillo (no global login)

**Never use `stripe login` for global auth.** Global CLI auth in `~/.config/stripe/config.toml` is dangerous: it silently targets whichever account was logged in last, which can be a completely different project. Instead, always run the Stripe CLI through **sigillo** so the correct API key is injected per-project.

The Stripe CLI checks the `STRIPE_API_KEY` environment variable automatically. If set, it overrides everything in `config.toml`. This is the mechanism we use with sigillo.

### Setup

Store the Stripe secret key as `STRIPE_API_KEY` in sigillo. This single env var is used by both your app code and the Stripe CLI (which picks it up automatically).

```bash
sigillo secrets set STRIPE_API_KEY sk_test_... -c dev
sigillo secrets set STRIPE_API_KEY sk_live_... -c prod
```

If a project already uses `STRIPE_SECRET_KEY` instead of `STRIPE_API_KEY`, use `--command` with shell variable expansion to alias it at runtime:

```bash
sigillo run -c prod --command 'STRIPE_API_KEY=$STRIPE_SECRET_KEY stripe products list'
```

Or copy the value permanently so `STRIPE_API_KEY` is always available:

```bash
sigillo secrets get STRIPE_SECRET_KEY --raw -c dev | sigillo secrets set STRIPE_API_KEY -c dev
sigillo secrets get STRIPE_SECRET_KEY --raw -c prod | sigillo secrets set STRIPE_API_KEY -c prod
```

### Running Stripe CLI commands

Wrap every `stripe` command with `sigillo run` so `STRIPE_API_KEY` is injected:

```bash
# simple commands, no shell expansion needed
sigillo run -- stripe products list
sigillo run -- stripe prices list --lookup-keys pro_monthly

# commands that need shell features (&&, pipes, $VARIABLES)
sigillo run --command 'stripe products create --name="Pro" --description="Pro plan"'

# when STRIPE_API_KEY is not set but STRIPE_SECRET_KEY is
sigillo run -c prod --command 'STRIPE_API_KEY=$STRIPE_SECRET_KEY stripe products list'

# webhook listener for local dev
sigillo run -- stripe listen --forward-to http://localhost:8866/api/stripe/webhook
```

Since `STRIPE_API_KEY` is in the environment, the CLI picks it up automatically. No `--api-key` flag needed on each command.

### Per-environment targeting

Use sigillo's `-c` flag to target a specific environment's Stripe account:

```bash
# list products on production Stripe account
sigillo run -c prod -- stripe products list

# create a webhook endpoint on preview
sigillo run -c preview -- stripe webhook_endpoints create \
  --url="https://preview.your-site.example/api/stripe/webhook" \
  -d "enabled_events[]=customer.subscription.created"
```

### Why not --project-name?

The `--project-name` flag creates separate sections in `config.toml`, but still relies on global state files and `stripe login`. With sigillo, the API key is scoped to the project directory and environment. No global config to get stale or point at the wrong account. Multiple projects with different Stripe accounts just work because each has its own sigillo secrets.

## Env vars

For **Vite + spiceflow** apps (not Next.js): Vite does not expose `process.env` to client code — in the browser you must use `import.meta.env.VITE_*`, and only variables prefixed `VITE_` are inlined into the client bundle. On the server (Node.js) `process.env` works normally.

Only three Stripe env vars should exist. The publishable key is the only one that runs in the browser:

```bash
# .env.local — committed to neither git nor the client bundle (server-only for the two secrets)
STRIPE_API_KEY=sk_test_...                 # server only, via process.env. Also used by Stripe CLI
STRIPE_WEBHOOK_SECRET=whsec_...            # server only, via process.env
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_...    # client + server, via import.meta.env on the client
```

```ts
// website/src/lib/env.ts — server-side accessors
export const env = {
  STRIPE_API_KEY: process.env.STRIPE_API_KEY,
  STRIPE_WEBHOOK_SECRET: process.env.STRIPE_WEBHOOK_SECRET,
  // Exposed so server code can also read it without reaching into import.meta.env
  VITE_STRIPE_PUBLISHABLE_KEY: process.env.VITE_STRIPE_PUBLISHABLE_KEY,
}
```

```ts
// Client-side code — React components, "use client" files, anything that ends up in the browser bundle
const publishableKey = import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY
```

**Never use `process.env.*` in client code.** Vite will either leave it as the literal string `process.env.X` at runtime (which explodes as `ReferenceError: process is not defined`) or silently strip it. Only `import.meta.env.VITE_*` is safe in the browser.

**Never prefix `STRIPE_API_KEY` or `STRIPE_WEBHOOK_SECRET` with `VITE_`.** Anything starting with `VITE_` is inlined into the client bundle and visible in devtools. If you accidentally rename the secret key to `VITE_STRIPE_API_KEY`, you leak it to every visitor.

**Prefer `lookup_key` over `STRIPE_PRICE_ID_FOO` env vars for each plan.** Env vars bind code to a specific Stripe account at deploy time. With `lookup_key` the code stays identical across accounts.

### TypeScript types for `import.meta.env`

Add to `website/src/vite-env.d.ts` (or wherever the existing Vite env declaration lives):

```ts
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_STRIPE_PUBLISHABLE_KEY: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
```

This gives autocomplete on `import.meta.env.VITE_*` and fails compilation if you typo the name.

### How to get each value

| Var | Where from | Notes |
|---|---|---|
| `STRIPE_API_KEY` | Copy `sk_test_`/`sk_live_` from `https://dashboard.stripe.com/apikeys` | Server only. Store in sigillo, never in the repo. Also used by Stripe CLI automatically |
| `STRIPE_WEBHOOK_SECRET` | Dev: `stripe listen --print-secret` (fails with `sk_live_` keys: live mode needs `stripe listen --live` after `stripe login`). Prod: returned once from `stripe webhook_endpoints create ...` | Server only. Returned only on endpoint creation — capture it |
| `VITE_STRIPE_PUBLISHABLE_KEY` | Copy `pk_test_`/`pk_live_` from `https://dashboard.stripe.com/apikeys` | Safe to ship to the browser. Must be `VITE_`-prefixed so Vite inlines it into the client bundle |

### Local dev webhook loop

```bash
# Terminal 1 — run the site
pnpm dev

# Terminal 2 — forward Stripe events to the local webhook route
sigillo run -- stripe listen --forward-to http://localhost:8040/api/stripe/webhooks
```

Copy the `whsec_...` it prints and set `STRIPE_WEBHOOK_SECRET` in sigillo (`sigillo secrets set STRIPE_WEBHOOK_SECRET <value> -c dev`). The secret is stable across restarts for the same machine.

## Creating products and prices via CLI

All `stripe` CLI commands in this section must be wrapped with `sigillo run` (see [CLI auth via sigillo](#cli-auth-via-sigillo-no-global-login)). Commands shown as bare `stripe ...` below are shorthand; always prefix with `sigillo run --` or use `sigillo run --command '...'` when shell variable expansion is needed.

**Prefer `lookup_key`** so app code references a stable string instead of a generated `price_xxx` id. This makes it safe to rotate prices, migrate accounts, or change numbers without redeploys.

### Naming convention

`<tier>_<interval>` — e.g. `pro_monthly`, `pro_yearly`, `team_monthly`, `team_yearly`. Keep tier names generic and decoupled from product branding so you can rename the product without rotating price lookup keys.

### Create a product once

Run this first. Copy the `id` from the JSON response into a shell variable before moving to the next step:

```bash
stripe products create \
  --name="Pro" \
  --description="Pro plan with full features"
```

Output includes `"id": "prod_SomeRealId"`. Now set the placeholder for the following commands:

```bash
export PRODUCT_ID=prod_SomeRealId   # replace with the id from above
```

The returned `prod_xxx` id doesn't need to leak into code — we look up by product via its prices' `lookup_key`.

### Create prices with monthly+yearly and USD+EUR

Run each of the two commands below **separately**, one at a time. After each one, confirm the response contains the expected `lookup_key` and `unit_amount` before moving on. `$PRODUCT_ID` is a placeholder — replace it with the id you exported above.

Set `tax_behavior=exclusive` on BOTH the top-level (USD) and the EUR `currency_options` entry — otherwise EUR defaults to `unspecified` and the mismatch can block portal plan-switching.

```bash
# 1. Monthly — $10/mo + €10/mo
stripe prices create \
  --product=$PRODUCT_ID \
  --currency=usd \
  --unit-amount=1000 \
  -d "recurring[interval]=month" \
  -d "currency_options[eur][unit_amount]=1000" \
  -d "currency_options[eur][tax_behavior]=exclusive" \
  -d "lookup_key=pro_monthly" \
  -d "nickname=Pro Monthly" \
  -d "tax_behavior=exclusive"
```

Check the response, then run the next:

```bash
# 2. Yearly — $100/yr + €100/yr
stripe prices create \
  --product=$PRODUCT_ID \
  --currency=usd \
  --unit-amount=10000 \
  -d "recurring[interval]=year" \
  -d "currency_options[eur][unit_amount]=10000" \
  -d "currency_options[eur][tax_behavior]=exclusive" \
  -d "lookup_key=pro_yearly" \
  -d "nickname=Pro Yearly" \
  -d "tax_behavior=exclusive"
```

After both succeed, verify the catalog. Pass `--expand "data.currency_options"` or the EUR amounts will NOT show in the output (Stripe omits `currency_options` unless explicitly expanded):

```bash
stripe prices list \
  --lookup-keys pro_monthly \
  --lookup-keys pro_yearly \
  --expand "data.currency_options"
```

You should see both prices. If one is missing, create the missing one manually — do not re-run the whole block or you'll get "lookup_key already exists" errors.

> **Adding a second tier** (e.g. `team`): create a new product via `stripe products create --name="Team" ...`, then two more prices with lookup keys `team_monthly` and `team_yearly`. Add both new price ids to the portal configuration under a second `products[1]` entry. The pattern scales linearly.

### Multi-currency

**USD is the base currency** (top-level `currency` field on the Price). EUR is added via `currency_options[eur][unit_amount]`. We intentionally use the **same integer value** for both currencies — at typical EUR/USD rates this captures ~8–10% extra margin on EUR customers with zero code changes.

- `unit_amount` is in **cents** (zero-decimal currencies like JPY use whole units).
- Stripe picks the currency at checkout time based on the customer's `preferred_locales` or an explicit `currency` on the Checkout Session. Once a subscription is created, the currency is **locked** — the portal cannot switch currencies. This is fine: EUR users stay on EUR, USD users stay on USD.

### Monthly ↔ yearly switching

Customers upgrade/downgrade between `_monthly` and `_yearly` via the **Billing Portal**, not custom code. The portal supports this **only if both prices belong to the same product**. The portal configuration (see [Portal configuration](#portal-configuration)) lists both prices under the single product.

### Rotating a price

To change the price amount without losing the lookup key binding. Run these **one at a time**, reading the output between each step. `$NEW_PRICE` and `$OLD_PRICE` are placeholder shell variables — set them manually from the actual ids Stripe returns.

Step 1 — Create the new price **without** the lookup_key:

```bash
stripe prices create \
  --product=$PRODUCT_ID \
  --currency=usd \
  --unit-amount=1200 \
  -d "recurring[interval]=month" \
  -d "currency_options[eur][unit_amount]=1200" \
  -d "nickname=Pro Monthly v2" \
  -d "tax_behavior=exclusive"
```

Copy the returned `id` into `NEW_PRICE`:

```bash
export NEW_PRICE=price_NewIdFromAbove
```

Step 2 — Atomically transfer the lookup_key from the old price to the new one:

```bash
stripe prices update $NEW_PRICE \
  -d "lookup_key=pro_monthly" \
  -d "transfer_lookup_key=true"
```

Confirm the response shows `"lookup_key": "pro_monthly"` on the new price.

Step 3 — Find the old price id and deactivate it. Use `stripe prices list` to find it if you don't already have it:

```bash
export OLD_PRICE=price_OldIdYouLookedUp
stripe prices update $OLD_PRICE -d active=false
```

Existing subscriptions stay on the old price. New checkouts use the new price. No redeploy needed.

If Step 2 fails (for example because `transfer_lookup_key` isn't supported on that price type), the old price still owns the lookup key and nothing is broken — you can safely delete the dangling new price via `stripe prices update $NEW_PRICE -d active=false` and retry.

## Single customer per Org

**Rule: create a Stripe Customer once per `Org`, store its id in `Org.stripeCustomerId`, reuse it forever.** This is the single biggest lever for preventing duplicate customers, duplicate subscriptions, and broken portal sessions.

```ts
// website/src/lib/stripe.ts
import * as orm from 'drizzle-orm'
import { db, schema } from 'db'
import * as errore from 'errore'
import {
  stripe,
  StripeApiError,
} from 'website/src/lib/stripe'

export class DbError extends errore.createTaggedError({
  name: 'DbError',
  message: 'Database operation failed: $operation',
}) {}

export class OrgNotFoundError extends errore.createTaggedError({
  name: 'OrgNotFoundError',
  message: 'Org $orgId not found',
}) {}

/**
 * Get or create the Stripe customer for an org. Idempotent — safe to call
 * from any flow. This is the ONLY place where
 * `stripe.customers.create` should be called.
 */
export async function getOrCreateStripeCustomer({
  orgId,
  email,
}: {
  orgId: string
  email: string | null | undefined
}) {
  const org = await db.query.orgs
    .findFirst({ where: { orgId } })
    .catch((e) => new DbError({ operation: 'orgs.findFirst', cause: e }))
  if (org instanceof Error) return org
  if (!org) return new OrgNotFoundError({ orgId })

  if (org.stripeCustomerId) return org.stripeCustomerId

  const customer = await stripe.customers
    .create({
      email: email || undefined,
      metadata: { orgId },
    })
    .catch((e) => new StripeApiError({ operation: 'customers.create', cause: e }))
  if (customer instanceof Error) return customer

  const updated = await db
    .update(schema.orgs)
    .set({ stripeCustomerId: customer.id })
    .where(orm.eq(schema.orgs.orgId, orgId))
    .catch((e) => new DbError({ operation: 'orgs.update', cause: e }))
  if (updated instanceof Error) return updated

  return customer.id
}
```

Every caller receives `string | DbError | OrgNotFoundError | StripeApiError` and must handle the failure modes explicitly:

```ts
const customerId = await getOrCreateStripeCustomer({ orgId, email })
if (customerId instanceof Error) return customerId
```

Never call `stripe.customers.create` anywhere else. Never pass `customer_email` to Checkout without also checking for an existing `stripeCustomerId` first — that creates a second customer row in Stripe on repeat purchases and the portal breaks (each customer has its own separate subscriptions).

## Server actions

Checkout and portal flows are **server actions**, not API routes. Server actions are simpler: no route definition, no `errorToResponse` mapper, no separate client file. They auto re-render the page after completing and use `redirect()` to navigate to Stripe URLs.

The **webhook** must stay as a spiceflow `.post()` route because Stripe sends raw HTTP POST requests with signature headers. Server actions are browser-only with CSRF origin checks.

```tsx
// src/actions/billing.tsx
'use server'

import { db, schema } from 'db'
import { env } from 'src/lib/env'
import {
  stripe,
  getOrCreateStripeCustomer,
} from 'src/lib/stripe'
import { getSession } from 'src/lib/auth'
import { redirect } from 'spiceflow'

/**
 * Start a Checkout Session for a new subscription, or redirect to the
 * portal if the org already has one. Prevents double subscriptions by
 * checking the DB before creating a session.
 */
export async function startCheckout(priceId: string, returnPath = '/billing') {
  const session = await getSession()
  if (!session) throw new Error('Unauthorized')

  const { orgId, email } = session
  const customerId = await getOrCreateStripeCustomer({ orgId, email })
  if (customerId instanceof Error) throw customerId

  // If already subscribed, short-circuit to the portal
  const existing = await db.query.subscriptions.findFirst({
    where: {
      orgId,
      status: { in: ['active', 'trialing', 'past_due'] },
    },
  })

  if (existing) {
    const portal = await stripe.billingPortal.sessions.create({
      customer: customerId,
      return_url: new URL(returnPath, env.PUBLIC_URL).toString(),
    })
    throw redirect(portal.url)
  }

  const checkoutSession = await stripe.checkout.sessions.create({
    mode: 'subscription',
    customer: customerId,
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: new URL(returnPath, env.PUBLIC_URL).toString(),
    cancel_url: new URL(returnPath, env.PUBLIC_URL).toString(),
    allow_promotion_codes: true,
    client_reference_id: orgId,
    // Metadata on BOTH the session and the subscription so webhooks
    // can always resolve orgId regardless of event type.
    metadata: { orgId },
    subscription_data: { metadata: { orgId } },
  })

  if (!checkoutSession.url) throw new Error('Checkout session has no URL')
  throw redirect(checkoutSession.url)
}

/**
 * Open the Billing Portal for an existing customer. Used by the
 * "Manage subscription" button.
 */
export async function openPortal(returnPath = '/billing') {
  const session = await getSession()
  if (!session) throw new Error('Unauthorized')

  const { orgId, email } = session
  const customerId = await getOrCreateStripeCustomer({ orgId, email })
  if (customerId instanceof Error) throw customerId

  const portal = await stripe.billingPortal.sessions.create({
    customer: customerId,
    return_url: new URL(returnPath, env.PUBLIC_URL).toString(),
  })

  throw redirect(portal.url)
}
```

Server action errors are caught by the nearest `ErrorBoundary`. If `getOrCreateStripeCustomer` returns an error, throwing it propagates to the client with a sanitized message.

## Billing page

Use `.loader()` to fetch subscription data server-side, and `useLoaderData()` in client components to read it without prop drilling.

```tsx
// src/main.tsx
import { Spiceflow } from 'spiceflow'
import { db } from 'db'
import { getSession } from 'src/lib/auth'
import { BillingPage } from './app/billing-page'

export const app = new Spiceflow()
  // ... layout, other pages ...

  .loader('/billing', async ({ request, redirect }) => {
    const session = await getSession(request)
    if (!session) throw redirect('/login')

    const subscription = await db.query.subscriptions.findFirst({
      where: {
        orgId: session.orgId,
        status: { in: ['active', 'trialing', 'past_due'] },
      },
    })

    return { subscription, orgId: session.orgId }
  })
  .page('/billing', async () => {
    return <BillingPage />
  })

declare module 'spiceflow/react' {
  interface SpiceflowRegister { app: typeof app }
}
```

The client component reads loader data via `useLoaderData` and calls server actions directly:

```tsx
// src/app/billing-page.tsx
'use client'

import { useLoaderData } from 'spiceflow/react'
import { startCheckout, openPortal } from '../actions/billing'

export function BillingPage() {
  const { subscription } = useLoaderData('/billing')

  if (subscription) {
    return (
      <div>
        <h1>Your Plan</h1>
        <p>Status: {subscription.status}</p>
        <p>Plan: {subscription.variantName}</p>
        <button onClick={() => openPortal()}>
          Manage Subscription
        </button>
      </div>
    )
  }

  return (
    <div>
      <h1>Choose a Plan</h1>
      <button onClick={() => startCheckout('price_pro_monthly')}>
        Pro Monthly
      </button>
      <button onClick={() => startCheckout('price_pro_yearly')}>
        Pro Yearly
      </button>
    </div>
  )
}
```

Notes on the pattern:

- **Server actions use `throw redirect(url)`** to navigate to Stripe URLs. Since every server action triggers a page re-render, using `redirect` avoids flashing the re-rendered current page before navigating.
- **Loader data stays fresh.** After a server action completes, the page re-renders with fresh loader data automatically. No manual `router.refresh()` needed.
- **`useLoaderData('/billing')`** is type-safe. TypeScript infers the return type from the loader registered at that path. If you rename a field in the loader, every component that reads it gets a compile error.
- **No `errorToResponse` mapper needed.** Server actions throw errors directly; the nearest `ErrorBoundary` catches them. No HTTP status code mapping required.
- **No separate client file.** Import server actions directly from `'use server'` files into client components. No `createSpiceflowFetch` wrapper needed for these flows.

## Webhook handler

The webhook is a **spiceflow route** (not a server action). Stripe sends raw HTTP POST requests with signature headers, so it needs a proper endpoint. Spiceflow handlers receive a standard Web `Request`, so `await request.text()` gives you the exact raw body bytes that Stripe signed — which is what `stripe.webhooks.constructEvent` needs for signature verification.

Do **not** parse the body with `await request.json()` before verifying the signature. JSON parsing normalizes whitespace and key order, which breaks the HMAC check. Always call `await request.text()` first.

The handler uses the errore pattern: `constructEvent` is a throwing sync API, so wrap it with `errore.try`. Every DB write is a `.catch()` boundary with a tagged error. Handler dispatch is a sequence of early returns, no `try/catch` for control flow.

```ts
// src/lib/stripe-webhook.tsx
import { Spiceflow } from 'spiceflow'
import * as errore from 'errore'
import {
  stripe,
  handleCheckoutSessionCompleted,
  handleSubscriptionChange,
} from 'src/lib/stripe'
import { env } from 'src/lib/env'
import { notifyError } from 'src/lib/errors'

export class WebhookSignatureError extends errore.createTaggedError({
  name: 'WebhookSignatureError',
  message: 'Stripe webhook signature verification failed',
}) {}

export const webhookApp = new Spiceflow({ basePath: '/api/stripe' })
  .post('/webhook', async ({ request }) => {
    const sig = request.headers.get('stripe-signature')
    if (!sig) return new Response('No signature', { status: 400 })

    // spiceflow exposes the full raw request body via request.text().
    // Must be called BEFORE any other body parsing — reading the stream
    // twice is an error.
    const rawBody = await request.text()

    // constructEvent is a throwing SYNC API — wrap it with errore.try
    // rather than a try/catch statement.
    const event = errore.try({
      try: () =>
        stripe.webhooks.constructEvent(
          rawBody,
          sig,
          env.STRIPE_WEBHOOK_SECRET!,
        ),
      catch: (e) => new WebhookSignatureError({ cause: e }),
    })
    if (event instanceof Error) {
      notifyError(event, 'Stripe webhook signature')
      return new Response('Bad signature', { status: 400 })
    }

    const result = await (async () => {
      if (event.type === 'checkout.session.completed') {
        return handleCheckoutSessionCompleted(event.data.object)
      }
      if (
        event.type === 'customer.subscription.created' ||
        event.type === 'customer.subscription.updated' ||
        event.type === 'customer.subscription.deleted'
      ) {
        return handleSubscriptionChange(event.data.object)
      }
      return null // unhandled event type — ignore silently
    })()

    if (result instanceof Error) {
      notifyError(result, `Stripe webhook ${event.type}`)
      return new Response('Webhook failed', { status: 500 })
    }

    return new Response('ok', { status: 200 })
  })
```

And the dispatchers in `src/lib/stripe.ts`, following the same errore conventions:

```ts
// src/lib/stripe.ts
import Stripe from 'stripe'
import * as orm from 'drizzle-orm'
import * as errore from 'errore'
import { db, schema } from 'db'
import { stripe, StripeApiError, DbError } from 'src/lib/stripe'

export class OrgResolutionError extends errore.createTaggedError({
  name: 'OrgResolutionError',
  message: 'Could not resolve orgId for Stripe event: $context',
}) {}

export async function handleCheckoutSessionCompleted(
  session: Stripe.Checkout.Session,
) {
  // Always re-fetch — event payload can be stale in out-of-order delivery.
  const latest = await stripe.checkout.sessions
    .retrieve(session.id, { expand: ['line_items'] })
    .catch(
      (e) =>
        new StripeApiError({
          operation: 'checkout.sessions.retrieve',
          cause: e,
        }),
    )
  if (latest instanceof Error) return latest

  const customerEmail = latest.customer_details?.email || null

  const orgId = await resolveStripeOrgId({
    metadataOrgId: latest.metadata?.orgId,
    customerId: typeof latest.customer === 'string' ? latest.customer : latest.customer?.id ?? null,
    customerEmail,
    context: `checkout.session.completed (${latest.id})`,
  })
  if (orgId instanceof Error) return orgId
  if (orgId === null) return null // unroutable webhook — drop it

  const item = latest.line_items?.data[0]
  if (!item || !item.price?.id) return null // nothing to record

  const record: typeof schema.paymentForCredits.$inferInsert = {
    id: latest.id,
    email: customerEmail || '',
    variantName: item.description || '',
    orderId: latest.id,
    productId: item.price.product.toString(),
    variantId: item.price.id,
    provider: 'stripe',
    orgId,
    metadata: latest.metadata || {},
  }

  const upsertResult = await db
    .insert(schema.paymentForCredits)
    .values(record)
    .onConflictDoUpdate({
      target: schema.paymentForCredits.id,
      set: record,
    })
    .catch(
      (e) => new DbError({ operation: 'paymentForCredits.upsert', cause: e }),
    )
  if (upsertResult instanceof Error) return upsertResult

  return null
}

export async function handleSubscriptionChange(
  subscription: Stripe.Subscription,
) {
  const latest = await stripe.subscriptions
    .retrieve(subscription.id)
    .catch(
      (e) =>
        new StripeApiError({
          operation: 'subscriptions.retrieve',
          cause: e,
        }),
    )
  if (latest instanceof Error) return latest

  const metadataEmail = latest.metadata?.email || null
  const orgId = await resolveStripeOrgId({
    metadataOrgId: latest.metadata?.orgId,
    customerId: typeof latest.customer === 'string' ? latest.customer : null,
    customerEmail: metadataEmail,
    context: `customer.subscription event (${latest.id})`,
  })
  if (orgId instanceof Error) return orgId
  if (orgId === null) return null

  const firstItem = latest.items.data[0]
  if (!firstItem) {
    return new OrgResolutionError({
      context: `No items in subscription ${latest.id}`,
    })
  }

  const record: typeof schema.subscriptions.$inferInsert = {
    orgId,
    orderId: latest.id,
    productId: firstItem.price.product.toString(),
    variantId: firstItem.price.id,
    subscriptionId: latest.id,
    email: metadataEmail || undefined,
    status: latest.status,
    variantName: firstItem.price.nickname || undefined,
    createdAt: new Date(latest.created * 1000),
    metadata: latest.metadata || {},
    provider: 'stripe',
    customerId: latest.customer.toString(),
  }

  const upsertResult = await db
    .insert(schema.subscriptions)
    .values(record)
    .onConflictDoUpdate({
      target: [schema.subscriptions.subscriptionId, schema.subscriptions.variantId],
      set: record,
    })
    .catch(
      (e) => new DbError({ operation: 'subscriptions.upsert', cause: e }),
    )
  if (upsertResult instanceof Error) return upsertResult

  return null
}

async function resolveStripeOrgId({
  metadataOrgId,
  customerId,
  customerEmail,
  context,
}: {
  metadataOrgId: string | undefined
  customerId: string | null
  customerEmail: string | null
  context: string
}) {
  // 1. Primary path — metadata.orgId from the checkout session or subscription
  if (!metadataOrgId) {
    console.warn(`No orgId in Stripe metadata for ${context}`)
  }
  if (metadataOrgId) {
    const org = await db.query.orgs
      .findFirst({ where: { orgId: metadataOrgId } })
      .catch((e) => new DbError({ operation: 'orgs.findFirst', cause: e }))
    if (org instanceof Error) return org
    if (org) return org.orgId
    console.warn(`Stripe webhook unknown orgId ${metadataOrgId} for ${context}`)
  }

  // 2. Fallback — metadata.orgId on the Stripe customer object itself.
  //    getOrCreateStripeCustomer writes orgId into the customer's metadata
  //    at creation time, so this is always set for customers we created.
  if (customerId) {
    const customer = await stripe.customers
      .retrieve(customerId)
      .catch(
        (e) =>
          new StripeApiError({ operation: 'customers.retrieve', cause: e }),
      )
    if (customer instanceof Error) return customer
    if (!customer.deleted) {
      const customerOrgId = customer.metadata?.orgId
      if (customerOrgId) {
        const org = await db.query.orgs
          .findFirst({ where: { orgId: customerOrgId } })
          .catch(
            (e) => new DbError({ operation: 'orgs.findFirst', cause: e }),
          )
        if (org instanceof Error) return org
        if (org) return org.orgId
      }
    }
  }

  // 3. Last resort — match customer email to a known user's first org
  if (!customerEmail) return null

  const user = await db.query.users
    .findFirst({
      where: { email: customerEmail },
      with: { orgs: true },
    })
    .catch((e) => new DbError({ operation: 'users.findFirst', cause: e }))
  if (user instanceof Error) return user

  return user?.orgs?.[0]?.orgId ?? null
}
```

**Do not add a Zod `body` schema to the webhook route.** Zod would try to parse the body as JSON, which either double-consumes the stream or normalizes whitespace and breaks HMAC verification. The raw-text handler above is the only correct pattern.

**Register the webhook URL with Stripe** once the route is mounted. Create **one endpoint per deployed environment** — production and preview have different hostnames, so they need separate endpoints, each with its own `whsec_` stored in that environment's secrets. Scope `enabled_events` to only what your handler processes (the handler silently drops unknown types, but a tight list keeps the dashboard clean):

```bash
# Production
sigillo run -c prod -- stripe webhook_endpoints create \
  --url="https://your-site.example/api/stripe/webhook" \
  -d "enabled_events[]=customer.subscription.created" \
  -d "enabled_events[]=customer.subscription.updated" \
  -d "enabled_events[]=customer.subscription.deleted"

# Preview (separate endpoint, separate secret)
sigillo run -c preview -- stripe webhook_endpoints create \
  --url="https://preview.your-site.example/api/stripe/webhook" \
  -d "enabled_events[]=customer.subscription.created" \
  -d "enabled_events[]=customer.subscription.updated" \
  -d "enabled_events[]=customer.subscription.deleted"
```

> **Always run stripe commands through `sigillo run`** so `STRIPE_API_KEY` is injected from the correct project/environment. Without it, the CLI falls back to the `[default]` profile in `~/.config/stripe/config.toml`, which may point at a different account. See [CLI auth via sigillo](#cli-auth-via-sigillo-no-global-login).

For local development, use `stripe listen --forward-to http://localhost:8040/api/stripe/webhook` and use its `whsec_` instead.

#### The webhook secret is shown ONLY on create — capture it immediately

The `secret` field (`whsec_...`) is returned **only in the `webhook_endpoints create` response**. `webhook_endpoints retrieve` and `update` return the secret **masked/absent** — there is no way to read it back later. If you miss it, you must **delete the endpoint and recreate it** (or roll the secret in the Dashboard).

So capture it in the same command that creates the endpoint, and pipe it **straight into your secrets manager via stdin** so the value never lands in shell history, logs, or an agent's context:

```bash
# Create + capture the secret directly into sigillo.
# The whsec_ value flows create -> stdin -> set, never printed.
resp=$(sigillo run -c prod -- stripe webhook_endpoints create \
  --url="https://your-site.example/api/stripe/webhook" \
  -d "enabled_events[]=customer.subscription.created" \
  -d "enabled_events[]=customer.subscription.updated" \
  -d "enabled_events[]=customer.subscription.deleted")
echo "$resp" | python3 -c 'import json,sys; sys.stdout.write(json.load(sys.stdin)["secret"])' \
  | sigillo secrets set STRIPE_WEBHOOK_SECRET -c prod
```

After storing it, sync to your deploy target (`wrangler secret put STRIPE_WEBHOOK_SECRET`, etc.) per environment.

### Idempotency on upserts

Webhooks are delivered at-least-once. Every write must be an upsert keyed on a stable column so retries are safe. The existing pattern:

- `PaymentForCredits` is upserted on `id = checkout_session_id`
- `Subscription` is upserted on the composite key `@@id([subscriptionId, variantId])`

When a subscription event arrives, always re-fetch the latest object from Stripe before writing to the DB — the event payload may be stale if events arrive out of order:

```ts
const latest = await stripe.subscriptions.retrieve(subscription.id)
```

### Resolving orgId from webhook events

Always write `metadata.orgId` on **both** the Checkout Session and its `subscription_data.metadata`. Webhooks need it on both because `checkout.session.completed` exposes session metadata, while `customer.subscription.*` exposes subscription metadata.

Fallback chain (three layers, from most reliable to least):

1. `metadata.orgId` on the event object (checkout session or subscription)
2. `metadata.orgId` on the **Stripe customer** — `getOrCreateStripeCustomer` writes `orgId` into the customer's metadata at creation time, so every customer we created has it. This survives even if session/subscription metadata is lost.
3. Email lookup: find the user by `customer_details.email` and return their first org

Never rely only on email — it's the last resort because users can change email in Stripe Checkout and break the mapping. The customer metadata (step 2) is the strongest fallback because `getOrCreateStripeCustomer` is the single place that creates customers and it always sets `metadata: { orgId }`.

### Mounting the webhook

Register the webhook sub-app in the parent spiceflow router via `.use()`. Only the webhook needs a route; checkout and portal flows use server actions.

```ts
// src/main.tsx
import { webhookApp } from 'src/lib/stripe-webhook'

export const app = new Spiceflow()
  // ... pages, layouts, other sub-apps ...
  .use(webhookApp) // ← /api/stripe/webhook
```

The webhook is publicly reachable — it does not need session auth. Stripe authenticates via the `stripe-signature` header and `constructEvent`. If the parent router has an auth middleware, make sure the webhook handler is not blocked by it.

## Preventing double subscriptions

Two layers of defense, both required:

**Layer 1 — DB check before checkout.** Inside the `startCheckout` server action, query `db.query.subscriptions` for an active row for this `orgId`. If one exists, redirect to the portal instead of creating a new Checkout Session. This is the primary guard.

```ts
const existing = await db.query.subscriptions.findFirst({
  where: {
    orgId,
    status: { in: ['active', 'trialing', 'past_due'] },
  },
})
if (existing) {
  const portal = await stripe.billingPortal.sessions.create({ ... })
  throw redirect(portal.url)
}
```

**Layer 2 — Single Stripe customer per org.** Because `Org.stripeCustomerId` is reused across every checkout, Stripe itself won't let the same customer subscribe twice to the same recurring price. Even if the DB check somehow races, Stripe returns an error and we never end up with two parallel subs for the same plan.

**Do not** rely on `customer_email` to deduplicate — Stripe will happily create a second customer with the same email if you don't pass an explicit `customer` id.

## Preventing double customers

Same pattern: `getOrCreateStripeCustomer({ orgId })` should be the only function that calls `stripe.customers.create`. Grep for it as a code review check:

```bash
rg "stripe\.customers\.create" website/src
# Should match ONLY getOrCreateStripeCustomer in website/src/lib/stripe.ts
```

If you find a second call site, delete it and route through `getOrCreateStripeCustomer` instead.

The `Org.stripeCustomerId` column in `db/src/schema.ts` is the single source of truth. It is set exactly once per org, the first time that org interacts with Stripe, and never updated afterward except on acquisition-style migrations.

## Portal configuration

The Billing Portal must be configured **once** per Stripe account so customers can cancel, switch plans, and update payment methods. Do this via the CLI, not via the dashboard, so the config is reproducible.

### Step 1 — collect the product and price ids

All the `$PRODUCT_ID`, `$PRO_MONTHLY`, `$PRO_YEARLY` variables below are **placeholder shell variables used for illustration only**. They are not stored anywhere. You set them manually in your current shell session from the ids Stripe returned when you created the product and prices earlier.

```bash
# Replace each value with the real id from the product/price creation steps above
export PRODUCT_ID=prod_yourProductIdHere
export PRO_MONTHLY=price_yourMonthlyIdHere
export PRO_YEARLY=price_yourYearlyIdHere
```

If you don't have the ids anymore, look them up with:

```bash
sigillo run -- stripe prices list --lookup-keys pro_monthly --lookup-keys pro_yearly
```

### Step 2 — create the portal configuration

Run this as a **single atomic call**. All `stripe` commands must go through `sigillo run` so the correct API key is injected (see [CLI auth via sigillo](#cli-auth-via-sigillo-no-global-login)). Use `sigillo run --command '...'` when the command uses shell variables like `$PRODUCT_ID`.

```bash
sigillo run --command 'stripe billing_portal configurations create \
  -d "business_profile[headline]=Manage your subscription" \
  -d "features[customer_update][enabled]=true" \
  -d "features[customer_update][allowed_updates][0]=email" \
  -d "features[customer_update][allowed_updates][1]=address" \
  -d "features[customer_update][allowed_updates][2]=tax_id" \
  -d "features[invoice_history][enabled]=true" \
  -d "features[payment_method_update][enabled]=true" \
  -d "features[subscription_cancel][enabled]=true" \
  -d "features[subscription_cancel][mode]=at_period_end" \
  -d "features[subscription_cancel][cancellation_reason][enabled]=true" \
  -d "features[subscription_cancel][cancellation_reason][options][0]=too_expensive" \
  -d "features[subscription_cancel][cancellation_reason][options][1]=missing_features" \
  -d "features[subscription_cancel][cancellation_reason][options][2]=switched_service" \
  -d "features[subscription_cancel][cancellation_reason][options][3]=unused" \
  -d "features[subscription_cancel][cancellation_reason][options][4]=other" \
  -d "features[subscription_update][enabled]=true" \
  -d "features[subscription_update][default_allowed_updates][0]=price" \
  -d "features[subscription_update][default_allowed_updates][1]=promotion_code" \
  -d "features[subscription_update][proration_behavior]=create_prorations" \
  -d "features[subscription_update][products][0][product]=$PRODUCT_ID" \
  -d "features[subscription_update][products][0][prices][0]=$PRO_MONTHLY" \
  -d "features[subscription_update][products][0][prices][1]=$PRO_YEARLY" \
  -d "features[subscription_update][schedule_at_period_end][conditions][0][type]=shortening_interval" \
  -d "features[subscription_update][schedule_at_period_end][conditions][1][type]=decreasing_item_amount"'
```

Listing both price ids under the same product enables portal-driven monthly/yearly switching. The `schedule_at_period_end` conditions make downgrades wait until the billing period ends.

### Enabling quantity changes (seat-based pricing)

If the subscription is seat-based (customers pay per unit), add `quantity` to `default_allowed_updates` and `adjustable_quantity` on the product. This can be done when creating the portal config or by updating an existing one.

To **update** an existing portal configuration:

```bash
# list existing configs to find the id
sigillo run -- stripe billing_portal configurations list

# update the config to enable quantity changes
sigillo run --command 'stripe billing_portal configurations update bpc_xxx \
  -d "features[subscription_update][enabled]=true" \
  -d "features[subscription_update][default_allowed_updates][0]=quantity" \
  -d "features[subscription_update][proration_behavior]=create_prorations" \
  -d "features[subscription_update][products][0][product]=$PRODUCT_ID" \
  -d "features[subscription_update][products][0][prices][0]=$PRO_MONTHLY" \
  -d "features[subscription_update][products][0][prices][1]=$PRO_YEARLY" \
  -d "features[subscription_update][products][0][adjustable_quantity][enabled]=true" \
  -d "features[subscription_update][products][0][adjustable_quantity][minimum]=1" \
  -d "features[subscription_update][products][0][adjustable_quantity][maximum]=100"'
```

To include quantity alongside price switching in the initial create, add these lines to the create command in Step 2:

```bash
  -d "features[subscription_update][default_allowed_updates][2]=quantity" \
  -d "features[subscription_update][products][0][adjustable_quantity][enabled]=true" \
  -d "features[subscription_update][products][0][adjustable_quantity][minimum]=1" \
  -d "features[subscription_update][products][0][adjustable_quantity][maximum]=100" \
```

Also set `adjustable_quantity` on the checkout `line_items` so customers can pick quantity during initial purchase:

```ts
line_items: [{
  price: priceId,
  quantity: defaultQty,
  adjustable_quantity: { enabled: true, minimum: 1, maximum: 100 },
}]
```

The webhook handler should read `firstItem.quantity` from the subscription and store it in the DB so the app can enforce seat limits.

If the command fails because any shell variable is empty or points to a non-existent id, Stripe returns a clean error and creates nothing.

> **Adding more tiers**: append a second product under `products[1][product]=$TEAM_PRODUCT` with its own `prices[0]=$TEAM_MONTHLY` / `prices[1]=$TEAM_YEARLY`. The portal will let customers switch between any of the 4 prices (pro monthly, pro yearly, team monthly, team yearly).

## DB reference

From `db/src/schema.ts` (drizzle). Table names use snake_case, accessed via `schema.orgs`, `schema.subscriptions`:

```ts
// db/src/schema.ts
import * as s from 'drizzle-orm/pg-core'
import { defineRelations } from 'drizzle-orm'

export const orgs = s.pgTable('orgs', {
  orgId:            s.text('org_id').primaryKey().notNull(),
  stripeCustomerId: s.text('stripe_customer_id'),  // ← single source of truth for the customer
  name:             s.text('name'),
  // ...
})

export const subscriptions = s.pgTable('subscriptions', {
  subscriptionId: s.text('subscription_id').notNull(),
  variantId:      s.text('variant_id').notNull(),       // ← Stripe price id (historical name from LemonSqueezy)
  productId:      s.text('product_id').notNull(),       // ← Stripe product id
  customerId:     s.text('customer_id'),                // ← Stripe customer id, denormalized from Org
  orgId:          s.text('org_id').notNull().references(() => orgs.orgId),
  status:         s.text('status').notNull(),           // active, trialing, canceled, past_due, ...
  provider:       s.text('provider').notNull(),         // stripe | lemonsqueezy (legacy)
  metadata:       s.jsonb('metadata'),
  email:          s.text('email'),
  orderId:        s.text('order_id'),
  variantName:    s.text('variant_name'),
  createdAt:      s.timestamp('created_at').defaultNow(),
}, (table) => [
  s.primaryKey({ columns: [table.subscriptionId, table.variantId] }),  // idempotent upsert key for webhooks
  s.index('subscriptions_org_id_idx').on(table.orgId),
])

export const relations = defineRelations({ orgs, subscriptions }, (r) => ({
  orgs: {
    subscriptions: r.many.subscriptions(),
  },
  subscriptions: {
    org: r.one.orgs({
      from: r.subscriptions.orgId,
      to: r.orgs.orgId,
    }),
  },
}))
```

The composite primary key `(subscriptionId, variantId)` lets a single subscription carry multiple line items (e.g. base plan + add-on) without the upsert colliding. Use `onConflictDoUpdate({ target: [schema.subscriptions.subscriptionId, schema.subscriptions.variantId], set: record })` for idempotent webhook writes.

## Common gotchas

- **Shared Stripe account between products.** Webhooks get every product's events. Tag products with `metadata.app`, skip other apps in the handler, and store `stripe_account_id` on customer and subscription rows so a later account switch keeps old subscriptions working.
- **One customer does not stop two subscriptions.** Two `/subscribe` tabs create two Checkout sessions. Reuse an open one (`checkout.sessions.list({ customer, status: 'open' })`), and turn on "Limit customers to one subscription" in the dashboard.
- **`current_period_end` moved to `subscription.items.data[n]`** in API version 2025-03-31. Reading it from the subscription gives `undefined`.


- **Portal can't switch currency.** Once a sub is USD, it stays USD. If a user wants EUR they have to cancel and re-subscribe. Don't try to build a "change currency" button — Stripe won't let you.
- **`tax_behavior` must match across prices of the same product.** Set it to `exclusive` on every price in the CLI commands above. If one price is `unspecified` and another is `exclusive`, the portal refuses to let users switch between them.
- **`customer_email` vs `customer`.** Never pass `customer_email` if you have a `customer` id. Passing both makes Stripe ignore `customer_email`, which creates confusing UX bugs.
- **Stripe CLI is a live API.** Everything in this skill runs against the account whose key is in the environment. Use `sigillo run -c dev` for test mode and `sigillo run -c prod` for production (see [CLI auth via sigillo](#cli-auth-via-sigillo-no-global-login)).
- **Webhooks must return 2xx quickly** (< 5s). If you need to run heavy work, enqueue it to `waitUntil`
- **Webhook raw body**: call `await request.text()` exactly once in the webhook handler. Calling `request.json()` first (or letting a Zod `body` schema parse the request) consumes the stream and breaks signature verification. Do not add a `body:` schema on the webhook route.
- **`Subscription.variantId` is the Stripe price id.** The name is historical from the LemonSqueezy days. Do not confuse it with the lookup key.
- **Errors as values in helpers.** Stripe/Drizzle helper functions (like `getOrCreateStripeCustomer`) should return `Error | T` via `.catch((e) => new TaggedError({ cause: e }))`. Server actions can then check `instanceof Error` and `throw` to propagate to the `ErrorBoundary`. See the [errore skill](../errore/SKILL.md) for the full pattern.
- **`currency_options` is NOT returned by default.** `stripe prices list` / `stripe prices retrieve` omit `currency_options` unless you pass `--expand currency_options` (or `--expand data.currency_options` for list). Verifying EUR pricing without the expand shows nothing and looks like the EUR amount failed to save when it actually did. Always verify multi-currency with the expand:
  ```bash
  stripe prices retrieve $PRICE_ID --expand currency_options
  stripe prices list --lookup-keys pro_monthly --expand "data.currency_options"
  ```
- **`tax_behavior` on EUR lives under `currency_options`, not the top level.** When EUR is added via `currency_options[eur][unit_amount]`, the top-level `tax_behavior=exclusive` only applies to the base USD price. The EUR currency option defaults to `tax_behavior: unspecified` unless you also pass `currency_options[eur][tax_behavior]=exclusive`. A mismatch (USD exclusive, EUR unspecified) can block portal plan-switching, so set it on both:
  ```bash
  -d "currency_options[eur][unit_amount]=9900" \
  -d "currency_options[eur][tax_behavior]=exclusive"
  ```
- **`is_default` on a portal config cannot be set via the API/CLI.** The `is_default` field is read-only — you cannot pass it to `billing_portal configurations create/update`. Only the Stripe Dashboard (Settings → Billing → Customer portal) controls which config is default, and `billingPortal.sessions.create` uses that default unless you pass an explicit `configuration` id. So: either set the default in the Dashboard, or pin the `bpc_...` id in the session-create call. Creating a new config via CLI does NOT make it the default.
- **The dashboard-managed default portal config drops API-set `subscription_update.products`.** Updating the default config (the one with `is_default: true`) via the API to add a `products` array silently does not persist — the field comes back empty/absent. Configure the portal's switchable product/price list in the **Dashboard** for the default config, or create + pin a non-default config that does persist `products`.
- **`managed_payments` for consumer products.** Pass `managed_payments: { enabled: true }` on checkout session creation to let Stripe act as merchant of record for indirect taxes (VAT, GST, sales tax). This is designed for consumer-facing products (B2C subscriptions, digital goods). Requires Stripe Tax with managed payments enabled in dashboard settings. Do not add `managed_payments` by default; only use it when the user explicitly asks for it.
- **Portal configuration belongs in the CLI, not in app code.** Portal configurations are account-level Stripe objects created once and reused forever. Do not write code to create or manage portal configurations at runtime (e.g. `stripe.billingPortal.configurations.create()` in a request handler). Instead, create and update them via the Stripe CLI through sigillo as documented in [Portal configuration](#portal-configuration). The app code only needs `stripe.billingPortal.sessions.create()` to open a portal session.
- **`cancel_at` vs `cancel_at_period_end` in portal cancellations.** When a customer cancels via the Billing Portal, Stripe may set `cancel_at` (epoch timestamp) to the period end date while leaving `cancel_at_period_end = false`. This happens because the portal uses `cancel_at` internally instead of the `cancel_at_period_end` boolean flag. If your webhook handler only checks `cancel_at_period_end`, cancellations from the portal will appear as still active in your DB/UI. Always normalise both fields into a single `cancelAt` timestamp:
  ```ts
  let cancelAt: number | null = null
  if (latest.cancel_at) {
    cancelAt = latest.cancel_at * 1000
  } else if (latest.cancel_at_period_end && currentPeriodEnd) {
    cancelAt = currentPeriodEnd * 1000
  }
  ```
  Then use `cancelAt` in the UI to show "cancelling on ..." regardless of which Stripe field was set. Do not rely solely on `cancel_at_period_end`.

## Disputes and chargebacks

For handling Stripe disputes, collecting evidence, generating evidence PDFs, and submitting responses, load the [stripe-disputes skill](../stripe-disputes/SKILL.md). It covers the full chargeback response workflow including CLI commands, evidence formatting rules, per-reason-code strategies, Visa CE 3.0, and PDF generation with react-pdf.
