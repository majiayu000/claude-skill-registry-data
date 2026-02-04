---
name: stripe
description: >
  Implement Stripe Connect payments for PhotoVault marketplace using
  destination charges. Use when working with checkout sessions, webhook
  handlers, platform subscriptions ($22/month), commission splits (50/50),
  Connect onboarding, failed payment handling (dunning), or debugging
  payment issues. Includes idempotency patterns and PhotoVault product IDs.
---

# ⚠️ MANDATORY WORKFLOW - DO NOT SKIP

**When this skill activates, you MUST follow the expert workflow before writing any code:**

1. **Spawn Domain Expert** using the Task tool with this prompt:
   ```
   Read the expert prompt at: C:\Users\natha\Stone-Fence-Brain\VENTURES\PhotoVault\claude\experts\stripe-expert.md

   Then research the codebase and write an implementation plan to: docs/claude/plans/stripe-[task-name]-plan.md

   Task: [describe the user's request]
   ```

2. **Spawn QA Critic** after expert returns, using Task tool:
   ```
   Read the QA critic prompt at: C:\Users\natha\Stone-Fence-Brain\VENTURES\PhotoVault\claude\experts\qa-critic-expert.md

   Review the plan at: docs/claude/plans/stripe-[task-name]-plan.md
   Write critique to: docs/claude/plans/stripe-[task-name]-critique.md
   ```

3. **Present BOTH plan and critique to user** - wait for approval before implementing

**DO NOT read files and start coding. DO NOT rationalize that "this is simple." Follow the workflow.**

---

# Stripe Integration

## Core Principles

### Idempotency is Non-Negotiable

Webhooks can fire multiple times. API calls can timeout and retry. Your code must handle duplicates gracefully.

```typescript
async function handlePaymentSucceeded(paymentIntent: Stripe.PaymentIntent) {
  const existing = await db.payments.findOne({
    stripe_payment_intent_id: paymentIntent.id
  })

  if (existing) {
    console.log(`Payment ${paymentIntent.id} already processed, skipping`)
    return
  }

  await db.payments.create({
    stripe_payment_intent_id: paymentIntent.id,
    amount: paymentIntent.amount,
    status: 'completed'
  })
}
```

### Use Destination Charges for Marketplaces

PhotoVault uses Stripe Connect with Express accounts. Destination charges:
- Route money directly to photographer
- Deduct platform fee automatically
- Create charge + transfer atomically

```typescript
const session = await stripe.checkout.sessions.create({
  mode: 'payment',
  line_items: [{ price: priceId, quantity: 1 }],
  payment_intent_data: {
    application_fee_amount: platformFeeCents, // 50% to PhotoVault
    transfer_data: {
      destination: photographer.stripe_connect_account_id,
    },
  },
})
```

### Always Verify Webhook Signatures

```typescript
const event = stripe.webhooks.constructEvent(
  rawBody,
  signature,
  webhookSecret
)
```

## Anti-Patterns

### Webhook Mistakes

**Not verifying webhook signatures**
```typescript
// WRONG
const event = JSON.parse(req.body)

// RIGHT
const event = stripe.webhooks.constructEvent(body, sig, secret)
```

**Not handling duplicate events**
```typescript
// WRONG
case 'checkout.session.completed':
  await createCommission(session)  // Duplicates on retry!

// RIGHT
case 'checkout.session.completed':
  const exists = await db.commissions.findOne({
    stripe_session_id: session.id
  })
  if (!exists) {
    await createCommission(session)
  }
```

**Processing webhooks synchronously**
```typescript
// WRONG: Slow response, timeout risk
app.post('/webhook', async (req, res) => {
  await sendEmails()
  await updateDatabase()
  res.json({ received: true })
})

// RIGHT: Acknowledge fast
app.post('/webhook', async (req, res) => {
  await queueForProcessing(event)
  res.json({ received: true })
})
```

### Connect Mistakes

**Using transfers when you should use destination charges**
```typescript
// WRONG: Two API calls, race condition risk
const charge = await stripe.paymentIntents.create({ amount: 10000 })
const transfer = await stripe.transfers.create({ amount: 5000, destination: accountId })

// RIGHT: Atomic destination charge
const session = await stripe.checkout.sessions.create({
  payment_intent_data: {
    application_fee_amount: 5000,
    transfer_data: { destination: accountId }
  }
})
```

## Webhook Handler Pattern

```typescript
import Stripe from 'stripe'
import { NextRequest, NextResponse } from 'next/server'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

export async function POST(req: NextRequest) {
  const body = await req.text()
  const signature = req.headers.get('stripe-signature')!

  let event: Stripe.Event
  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    )
  } catch (err) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 })
  }

  try {
    switch (event.type) {
      case 'checkout.session.completed':
        await handleCheckoutComplete(event.data.object as Stripe.Checkout.Session)
        break
      case 'invoice.paid':
        await handleInvoicePaid(event.data.object as Stripe.Invoice)
        break
      case 'invoice.payment_failed':
        await handlePaymentFailed(event.data.object as Stripe.Invoice)
        break
    }
  } catch (err) {
    console.error(`Error processing ${event.type}:`, err)
  }

  return NextResponse.json({ received: true })
}
```

## PhotoVault Configuration

### Stripe Products (Test Mode)

| Product | ID | Price |
|---------|-----|-------|
| Year Package | `prod_TV5f6EOT5K3wKt` | $100 + $8/mo |
| 6-Month Package | `prod_TV5f1eAehZIlA2` | $50 + $8/mo |
| 6-Month Trial | `prod_TV5fYvY8l0WaaV` | $20 one-time |
| Client Monthly | `prod_TV5gXyg5nNn635` | $8/month |
| Direct Monthly | `prod_TV6BkuQUCil1ZD` | $8/month (0% commission) |
| Platform Fee | `prod_TV5evkNAa2Ezo5` | $22/month |

### Key Files

```
src/
├── lib/stripe.ts                    # Stripe config & helpers
├── app/api/
│   ├── stripe/
│   │   ├── create-checkout/         # Checkout session creation
│   │   ├── connect/                 # Connect onboarding
│   │   └── platform-subscription/
│   └── webhooks/stripe/             # Webhook handler
```

### Environment Variables

```bash
STRIPE_SECRET_KEY=sk_test_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRICE_PLATFORM_MONTHLY=price_...
```

### Commission Rate

- Platform takes 50% (`PHOTOGRAPHER_COMMISSION_RATE = 0.50`)
- API Version: `2025-09-30.clover`

## Testing with Stripe CLI

```bash
# Forward webhooks to local server
stripe listen --forward-to localhost:3002/api/webhooks/stripe

# Trigger test events
stripe trigger checkout.session.completed
stripe trigger invoice.payment_failed
```

### Test Cards

| Card | Number | Result |
|------|--------|--------|
| Success | `4242 4242 4242 4242` | Payment succeeds |
| Decline | `4000 0000 0000 0002` | Card declined |
| 3D Secure | `4000 0025 0000 3155` | Requires auth |
| Insufficient | `4000 0000 0000 9995` | Insufficient funds |

## Debugging Checklist

1. Check Stripe Dashboard → Payments → Find the payment
2. Check webhook logs → Developers → Webhooks → Recent events
3. Verify Connect account → Connect → Accounts → Is it enabled?
4. Check your logs → Console for errors
5. Verify webhook secret → Is it correct for this endpoint?
6. Check idempotency → Is the commission already created?
