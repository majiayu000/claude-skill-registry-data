---
name: stripe-integration
description: Implements Stripe payments correctly the first time. Handles checkout sessions, webhooks, subscriptions, and customer management following Stripe best practices.
---

# Stripe Integration Skill

Implements Stripe payments following official best practices. Covers checkout, webhooks, subscriptions, and error handling.

## When I Activate

- User mentions "Stripe", "payments", "checkout", "subscription", "billing"
- Building payment flows, upgrading plans, or handling purchases
- Setting up webhooks or handling payment events

---

## Core Principles

1. **Never trust client-side data for amounts** - Always compute prices server-side
2. **Use webhooks for fulfillment** - Don't rely on redirect success alone
3. **Test with test keys first** - Never use live keys in development
4. **Handle all webhook events** - Especially `checkout.session.completed`
5. **Store Stripe customer IDs** - Link users to their Stripe customers

---

## Implementation Checklist

### Environment Variables Required
```env
STRIPE_SECRET_KEY=sk_test_...          # Server-side only
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...  # Client-side OK
STRIPE_WEBHOOK_SECRET=whsec_...        # For webhook verification
```

### Getting STRIPE_WEBHOOK_SECRET
1. Go to https://dashboard.stripe.com/webhooks
2. Click "Add endpoint"
3. Enter your webhook URL: `https://yourdomain.com/api/webhooks/stripe`
4. Select events: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`
5. Click "Add endpoint"
6. Click "Reveal" under "Signing secret" - this is your `STRIPE_WEBHOOK_SECRET`

For local development:
```bash
# Install Stripe CLI: brew install stripe/stripe-cli/stripe
stripe login
stripe listen --forward-to localhost:3000/api/webhooks/stripe
# Copy the webhook signing secret it displays
```

---

## Standard Implementation Pattern

### 1. Install Dependencies
```bash
npm install stripe @stripe/stripe-js
```

### 2. Create Stripe Client (Server)
```typescript
// src/lib/stripe.ts
import Stripe from 'stripe'

if (!process.env.STRIPE_SECRET_KEY) {
  throw new Error('STRIPE_SECRET_KEY is not set')
}

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  apiVersion: '2024-12-18.acacia',
  typescript: true,
})
```

### 3. Create Checkout Session API Route
```typescript
// src/app/api/checkout/route.ts
import { NextResponse } from 'next/server'
import { auth } from '@clerk/nextjs/server'
import { stripe } from '@/lib/stripe'
import { getUserByClerkId } from '@/lib/supabase/queries'

const PRICES = {
  starter: process.env.STRIPE_STARTER_PRICE_ID,
  pro: process.env.STRIPE_PRO_PRICE_ID,
  business: process.env.STRIPE_BUSINESS_PRICE_ID,
}

export async function POST(req: Request) {
  try {
    const { userId } = await auth()
    if (!userId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { priceId, planName } = await req.json()

    // Validate price ID exists
    if (!priceId || !Object.values(PRICES).includes(priceId)) {
      return NextResponse.json({ error: 'Invalid price' }, { status: 400 })
    }

    // Get user from database
    const { data: user } = await getUserByClerkId(userId)
    if (!user) {
      return NextResponse.json({ error: 'User not found' }, { status: 404 })
    }

    // Create or retrieve Stripe customer
    let stripeCustomerId = user.stripe_customer_id

    if (!stripeCustomerId) {
      const customer = await stripe.customers.create({
        email: user.email,
        metadata: { userId: user.id, clerkId: userId },
      })
      stripeCustomerId = customer.id
      // TODO: Save stripeCustomerId to user record
    }

    // Create checkout session
    const session = await stripe.checkout.sessions.create({
      customer: stripeCustomerId,
      mode: 'subscription',
      payment_method_types: ['card'],
      line_items: [{ price: priceId, quantity: 1 }],
      success_url: `${process.env.NEXT_PUBLIC_APP_URL}/dashboard?checkout=success`,
      cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/pricing?checkout=cancelled`,
      metadata: {
        userId: user.id,
        planName: planName,
      },
      subscription_data: {
        metadata: { userId: user.id, planName: planName },
      },
    })

    return NextResponse.json({ url: session.url })
  } catch (error) {
    console.error('[CHECKOUT] Error:', error)
    return NextResponse.json({ error: 'Checkout failed' }, { status: 500 })
  }
}
```

### 4. Create Webhook Handler (CRITICAL)
```typescript
// src/app/api/webhooks/stripe/route.ts
import { NextResponse } from 'next/server'
import { headers } from 'next/headers'
import { stripe } from '@/lib/stripe'
import Stripe from 'stripe'

const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET!

export async function POST(req: Request) {
  const body = await req.text()
  const headersList = await headers()
  const signature = headersList.get('stripe-signature')!

  let event: Stripe.Event

  try {
    event = stripe.webhooks.constructEvent(body, signature, webhookSecret)
  } catch (err) {
    console.error('[STRIPE_WEBHOOK] Signature verification failed:', err)
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 })
  }

  try {
    switch (event.type) {
      case 'checkout.session.completed': {
        const session = event.data.object as Stripe.Checkout.Session
        await handleCheckoutCompleted(session)
        break
      }
      case 'customer.subscription.updated': {
        const subscription = event.data.object as Stripe.Subscription
        await handleSubscriptionUpdated(subscription)
        break
      }
      case 'customer.subscription.deleted': {
        const subscription = event.data.object as Stripe.Subscription
        await handleSubscriptionDeleted(subscription)
        break
      }
      case 'invoice.payment_failed': {
        const invoice = event.data.object as Stripe.Invoice
        await handlePaymentFailed(invoice)
        break
      }
    }

    return NextResponse.json({ received: true })
  } catch (error) {
    console.error('[STRIPE_WEBHOOK] Handler error:', error)
    return NextResponse.json({ error: 'Webhook handler failed' }, { status: 500 })
  }
}

async function handleCheckoutCompleted(session: Stripe.Checkout.Session) {
  const userId = session.metadata?.userId
  const planName = session.metadata?.planName

  if (!userId || !planName) {
    console.error('[STRIPE_WEBHOOK] Missing metadata:', session.id)
    return
  }

  // Update user's plan and credits in database
  // This is where you fulfill the purchase!
  console.log(`[STRIPE_WEBHOOK] Upgrading user ${userId} to ${planName}`)

  // TODO: Call your database update function
  // await updateUserPlan(userId, planName)
}

async function handleSubscriptionUpdated(subscription: Stripe.Subscription) {
  const userId = subscription.metadata?.userId
  // Handle plan changes, status changes
  console.log(`[STRIPE_WEBHOOK] Subscription updated for user ${userId}`)
}

async function handleSubscriptionDeleted(subscription: Stripe.Subscription) {
  const userId = subscription.metadata?.userId
  // Downgrade user to free plan
  console.log(`[STRIPE_WEBHOOK] Subscription cancelled for user ${userId}`)
  // TODO: await downgradeUserToFree(userId)
}

async function handlePaymentFailed(invoice: Stripe.Invoice) {
  // Notify user of failed payment
  console.log(`[STRIPE_WEBHOOK] Payment failed for invoice ${invoice.id}`)
}
```

### 5. Create Checkout Button Component
```typescript
// src/components/CheckoutButton.tsx
'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'

interface CheckoutButtonProps {
  priceId: string
  planName: string
  children: React.ReactNode
}

export function CheckoutButton({ priceId, planName, children }: CheckoutButtonProps) {
  const [loading, setLoading] = useState(false)

  const handleCheckout = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ priceId, planName }),
      })

      const { url, error } = await response.json()

      if (error) {
        alert(error)
        return
      }

      // Redirect to Stripe Checkout
      window.location.href = url
    } catch (error) {
      console.error('Checkout error:', error)
      alert('Failed to start checkout')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Button onClick={handleCheckout} disabled={loading}>
      {loading ? 'Loading...' : children}
    </Button>
  )
}
```

---

## Stripe Dashboard Setup

### Create Products and Prices
1. Go to https://dashboard.stripe.com/products
2. Click "Add product"
3. For each plan (Starter, Pro, Business):
   - Name: "RankEasy Starter" etc.
   - Pricing: Recurring, Monthly
   - Price: $29, $79, $199 etc.
4. Copy the Price ID (starts with `price_`)
5. Add to `.env.local`:
   ```
   STRIPE_STARTER_PRICE_ID=price_...
   STRIPE_PRO_PRICE_ID=price_...
   STRIPE_BUSINESS_PRICE_ID=price_...
   ```

---

## Testing Checklist

### Test Cards
- Success: `4242 4242 4242 4242`
- Declined: `4000 0000 0000 0002`
- Requires auth: `4000 0025 0000 3155`

### Test Flow
1. Click checkout button
2. Should redirect to Stripe Checkout
3. Use test card `4242 4242 4242 4242`
4. Any future expiry, any CVC
5. Complete payment
6. Should redirect back with `?checkout=success`
7. Webhook should fire and update user's plan

### Webhook Testing (Local)
```bash
# Terminal 1: Run your app
npm run dev

# Terminal 2: Forward webhooks
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# Terminal 3: Trigger test event
stripe trigger checkout.session.completed
```

---

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "No such price" | Invalid price ID | Check STRIPE_*_PRICE_ID env vars |
| "Invalid signature" | Wrong webhook secret | Update STRIPE_WEBHOOK_SECRET |
| Webhook not firing | Endpoint not registered | Add endpoint in Stripe Dashboard |
| Customer not found | No stripe_customer_id | Create customer first |

---

## Security Best Practices

1. **Never expose STRIPE_SECRET_KEY to client** - Only use in server components/API routes
2. **Always verify webhook signatures** - Prevents spoofed events
3. **Use metadata for user linking** - Store userId in checkout session metadata
4. **Validate prices server-side** - Don't trust client-provided amounts
5. **Handle all webhook events** - Don't just rely on success redirect
