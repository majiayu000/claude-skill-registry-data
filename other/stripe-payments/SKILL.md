---
name: stripe-payments
description: Stripe payments integration — checkout, subscriptions, webhooks, customer portal, pricing tables.
---

# Stripe Payments Reference

> Local repo: `repos/stripe-sdk` (Node.js/TypeScript SDK)
> **CRITICAL**: Stripe SDK is server-side only. NEVER import `stripe` or expose `STRIPE_SECRET_KEY` in client-side code.

---

## 1. Setup

```bash
npm install stripe
```

```typescript
// lib/stripe.ts — SERVER ONLY
import Stripe from 'stripe'

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-12-18.acacia',
  typescript: true,
})
```

---

## 2. Checkout Session

### Create a One-Time Payment Session

```typescript
// app/api/checkout/route.ts
import { stripe } from '@/lib/stripe'
import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function POST(req: Request) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const { priceId } = await req.json()

  const session = await stripe.checkout.sessions.create({
    customer_email: user.email,
    line_items: [
      {
        price: priceId,
        quantity: 1,
      },
    ],
    mode: 'payment', // 'subscription' for recurring
    success_url: `${process.env.NEXT_PUBLIC_SITE_URL}/checkout/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.NEXT_PUBLIC_SITE_URL}/pricing`,
    metadata: {
      supabase_user_id: user.id,
    },
  })

  return NextResponse.json({ url: session.url })
}
```

### Redirect to Checkout (Client)

```typescript
'use client'

async function handleCheckout(priceId: string) {
  const res = await fetch('/api/checkout', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ priceId }),
  })
  const { url } = await res.json()
  window.location.href = url
}
```

---

## 3. Subscriptions

### Create Subscription Checkout

```typescript
const session = await stripe.checkout.sessions.create({
  customer: customerId, // existing Stripe customer
  line_items: [
    {
      price: 'price_monthly_pro', // price ID from Stripe dashboard
      quantity: 1,
    },
  ],
  mode: 'subscription',
  success_url: `${siteUrl}/dashboard?session_id={CHECKOUT_SESSION_ID}`,
  cancel_url: `${siteUrl}/pricing`,
  subscription_data: {
    trial_period_days: 14,
    metadata: {
      supabase_user_id: userId,
    },
  },
  allow_promotion_codes: true,
})
```

### Retrieve Subscription Status

```typescript
const subscription = await stripe.subscriptions.retrieve(subscriptionId)

// Key fields:
// subscription.status: 'active' | 'trialing' | 'past_due' | 'canceled' | 'unpaid' | 'incomplete'
// subscription.current_period_end: Unix timestamp
// subscription.cancel_at_period_end: boolean
// subscription.items.data[0].price.id: current price/plan
```

### Cancel / Pause Subscription

```typescript
// Cancel at end of billing period (recommended)
await stripe.subscriptions.update(subscriptionId, {
  cancel_at_period_end: true,
})

// Cancel immediately
await stripe.subscriptions.cancel(subscriptionId)

// Pause collection (keep subscription active but stop charging)
await stripe.subscriptions.update(subscriptionId, {
  pause_collection: {
    behavior: 'mark_uncollectible', // or 'keep_as_draft', 'void'
  },
})

// Resume paused subscription
await stripe.subscriptions.update(subscriptionId, {
  pause_collection: '', // empty string to resume
})
```

### Change Plan / Upgrade / Downgrade

```typescript
const subscription = await stripe.subscriptions.retrieve(subscriptionId)

await stripe.subscriptions.update(subscriptionId, {
  items: [
    {
      id: subscription.items.data[0].id,
      price: 'price_new_plan_id',
    },
  ],
  proration_behavior: 'create_prorations', // or 'none', 'always_invoice'
})
```

### Trial Periods

```typescript
// Trial on subscription creation
const session = await stripe.checkout.sessions.create({
  mode: 'subscription',
  subscription_data: {
    trial_period_days: 14,
    trial_settings: {
      end_behavior: {
        missing_payment_method: 'cancel', // or 'pause', 'create_invoice'
      },
    },
  },
  // ...
})
```

---

## 4. Webhooks

### Verify Signature & Handle Events

```typescript
// app/api/webhooks/stripe/route.ts
import { stripe } from '@/lib/stripe'
import { createClient } from '@supabase/supabase-js'
import { headers } from 'next/headers'

// Use service role to bypass RLS in webhook handler
const supabaseAdmin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
)

export async function POST(req: Request) {
  const body = await req.text()
  const headersList = await headers()
  const signature = headersList.get('stripe-signature')!

  let event: Stripe.Event

  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    )
  } catch (err) {
    console.error('Webhook signature verification failed:', err)
    return new Response('Webhook Error', { status: 400 })
  }

  switch (event.type) {
    case 'checkout.session.completed': {
      const session = event.data.object as Stripe.Checkout.Session
      const userId = session.metadata?.supabase_user_id

      if (session.mode === 'subscription') {
        // Store customer ID and subscription ID
        await supabaseAdmin
          .from('profiles')
          .update({
            stripe_customer_id: session.customer as string,
            stripe_subscription_id: session.subscription as string,
            subscription_status: 'active',
          })
          .eq('id', userId)
      }
      break
    }

    case 'invoice.paid': {
      const invoice = event.data.object as Stripe.Invoice
      const subscriptionId = invoice.subscription as string

      await supabaseAdmin
        .from('profiles')
        .update({ subscription_status: 'active' })
        .eq('stripe_subscription_id', subscriptionId)
      break
    }

    case 'customer.subscription.updated': {
      const subscription = event.data.object as Stripe.Subscription

      await supabaseAdmin
        .from('profiles')
        .update({
          subscription_status: subscription.status,
          subscription_tier: subscription.items.data[0].price.lookup_key,
          current_period_end: new Date(
            subscription.current_period_end * 1000
          ).toISOString(),
        })
        .eq('stripe_subscription_id', subscription.id)
      break
    }

    case 'customer.subscription.deleted': {
      const subscription = event.data.object as Stripe.Subscription

      await supabaseAdmin
        .from('profiles')
        .update({
          subscription_status: 'canceled',
          subscription_tier: null,
        })
        .eq('stripe_subscription_id', subscription.id)
      break
    }

    case 'invoice.payment_failed': {
      const invoice = event.data.object as Stripe.Invoice
      // Notify user, update status to past_due
      await supabaseAdmin
        .from('profiles')
        .update({ subscription_status: 'past_due' })
        .eq('stripe_subscription_id', invoice.subscription as string)
      break
    }
  }

  return new Response('ok', { status: 200 })
}
```

### Idempotency

```typescript
// Stripe webhooks can send the same event multiple times.
// Use event.id to deduplicate:

const { data: existing } = await supabaseAdmin
  .from('stripe_events')
  .select('id')
  .eq('event_id', event.id)
  .single()

if (existing) {
  return new Response('Already processed', { status: 200 })
}

// Process event...

// Record that we processed it
await supabaseAdmin
  .from('stripe_events')
  .insert({ event_id: event.id, type: event.type })
```

---

## 5. Customer Portal

```typescript
// app/api/billing/portal/route.ts
import { stripe } from '@/lib/stripe'
import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function POST() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const { data: profile } = await supabase
    .from('profiles')
    .select('stripe_customer_id')
    .eq('id', user.id)
    .single()

  if (!profile?.stripe_customer_id) {
    return NextResponse.json({ error: 'No billing account' }, { status: 400 })
  }

  const portalSession = await stripe.billingPortal.sessions.create({
    customer: profile.stripe_customer_id,
    return_url: `${process.env.NEXT_PUBLIC_SITE_URL}/dashboard/settings`,
  })

  return NextResponse.json({ url: portalSession.url })
}
```

Customer Portal allows self-service:
- View invoices and payment history
- Update payment method
- Cancel or change subscription plan
- Update billing information

Configure portal in Stripe Dashboard → Settings → Customer Portal.

---

## 6. Supabase Integration

### Profiles Table Schema

```sql
CREATE TABLE public.profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT,
  full_name TEXT,
  stripe_customer_id TEXT UNIQUE,
  stripe_subscription_id TEXT UNIQUE,
  subscription_status TEXT DEFAULT 'none',
  subscription_tier TEXT,
  current_period_end TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile"
  ON public.profiles FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON public.profiles FOR UPDATE
  USING (auth.uid() = id);
```

### RLS Based on Subscription Tier

```sql
-- Only pro users can access premium content
CREATE POLICY "Pro users can view premium content"
  ON public.premium_content
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM public.profiles
      WHERE profiles.id = auth.uid()
        AND profiles.subscription_status = 'active'
        AND profiles.subscription_tier IN ('pro', 'enterprise')
    )
  );
```

### Create Stripe Customer on Signup

```sql
-- Alternatively, create customer in webhook or trigger
-- This is the webhook approach:
```

```typescript
// In your checkout flow, create customer if needed:
async function getOrCreateCustomer(userId: string, email: string) {
  const { data: profile } = await supabaseAdmin
    .from('profiles')
    .select('stripe_customer_id')
    .eq('id', userId)
    .single()

  if (profile?.stripe_customer_id) {
    return profile.stripe_customer_id
  }

  const customer = await stripe.customers.create({
    email,
    metadata: { supabase_user_id: userId },
  })

  await supabaseAdmin
    .from('profiles')
    .update({ stripe_customer_id: customer.id })
    .eq('id', userId)

  return customer.id
}
```

---

## 7. Testing

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login and listen for webhooks locally
stripe login
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# Trigger test events
stripe trigger checkout.session.completed
stripe trigger customer.subscription.updated
stripe trigger invoice.payment_failed
```

Use `STRIPE_SECRET_KEY=sk_test_...` for test mode. All test card numbers:
- `4242424242424242` — successful payment
- `4000000000000002` — card declined
- `4000000000003220` — requires 3D Secure
