---
name: stripe-integration
description: Implement Stripe payment flows, webhooks, and billing logic. Use when working with payments, subscriptions, checkout, or credit systems.
---

# Stripe Integration Skill

Comprehensive patterns for Stripe payment integration in this Next.js SaaS project.

## Architecture Overview

```
server/stripe/           # Server-only Stripe instance
├── config.ts           # Stripe SDK initialization
└── index.ts            # Re-exports

shared/config/
├── stripe.ts           # Price IDs, plan config, display helpers
├── subscription.config.ts  # Single source of truth for plans
└── subscription.utils.ts   # Helpers (resolvePriceId, getPlanByKey, etc.)

client/services/
└── stripeService.ts    # Frontend API wrapper

app/api/
├── checkout/route.ts   # Create checkout sessions
├── portal/route.ts     # Customer portal sessions
├── subscription/       # Subscription management
│   ├── change/route.ts
│   ├── preview-change/route.ts
│   └── cancel-scheduled/route.ts
└── webhooks/stripe/    # Webhook handlers
    ├── route.ts
    └── handlers/
        └── subscription.handler.ts
```

## Server-Side Stripe Client

```typescript
// Import the singleton Stripe instance
import { stripe } from '@server/stripe';

// Example: Retrieve customer
const customer = await stripe.customers.retrieve(customerId);

// Example: Create checkout session
const session = await stripe.checkout.sessions.create({
  customer: customerId,
  line_items: [{ price: priceId, quantity: 1 }],
  mode: 'subscription',
  success_url: `${baseUrl}/success?session_id={CHECKOUT_SESSION_ID}`,
  cancel_url: `${baseUrl}/canceled`,
});

// Example: Retrieve subscription
const subscription = await stripe.subscriptions.retrieve(subscriptionId);

// Example: Update subscription (plan change)
const updated = await stripe.subscriptions.update(subscriptionId, {
  items: [{ id: itemId, price: newPriceId }],
  proration_behavior: 'create_prorations',
});
```

## Price Resolution (Single Source of Truth)

Always use the unified resolver functions:

```typescript
import {
  resolvePriceId,
  resolvePlanOrPack,
  assertKnownPriceId,
  getPlanByPriceId,
  getPlanByKey,
} from '@shared/config/stripe';

// Resolve any price ID to its metadata
const resolved = resolvePriceId(priceId);
// Returns: { type: 'plan' | 'pack', key, name, credits, ... } | null

// Assert price is valid (throws if unknown)
const plan = assertKnownPriceId(priceId);

// Get plan details by key (e.g., 'starter', 'pro')
const plan = getPlanByKey('pro');
// Returns: { key, name, creditsPerCycle, maxRollover, features, ... }

// Get display name for UI (adds " Plan" suffix for consistency)
import { getPlanDisplayName } from '@shared/config/stripe';
const displayName = getPlanDisplayName({ subscriptionTier: 'starter' });
// Returns: "Starter Plan"
```

## Client-Side Service Usage

```typescript
import { StripeService } from '@client/services/stripeService';

// Redirect to Stripe Checkout
await StripeService.redirectToCheckout(priceId, {
  successUrl: '/success',
  cancelUrl: '/pricing',
});

// Create checkout session (for embedded checkout)
const { url, sessionId, clientSecret } = await StripeService.createCheckoutSession(priceId, {
  uiMode: 'embedded',
});

// Purchase credit pack
const { url } = await StripeService.purchaseCredits('medium');

// Redirect to Customer Portal
await StripeService.redirectToPortal();

// Preview subscription change (proration)
const preview = await StripeService.previewSubscriptionChange(targetPriceId);

// Execute subscription change
const result = await StripeService.changeSubscription(targetPriceId);

// Cancel subscription (at period end)
const result = await StripeService.cancelSubscription('reason');

// Get user profile with credits
const profile = await StripeService.getUserProfile();

// Check credit balance
const hasSufficient = await StripeService.hasSufficientCredits(5);
```

## Subscription Configuration

Plans are defined in `shared/config/subscription.config.ts`:

```typescript
// Current plan structure
{
  key: 'pro',                    // Internal identifier (stored in DB)
  name: 'Professional',          // Display name
  stripePriceId: 'price_xxx',   // Stripe price ID
  priceInCents: 4900,           // $49.00
  currency: 'usd',
  interval: 'month',
  creditsPerCycle: 1000,
  maxRollover: 6000,            // 6x monthly
  rolloverMultiplier: 6,
  features: [...],
  recommended: true,
  batchLimit: 50,               // Max images in batch
}
```

## Webhook Handling

Webhooks are processed in `app/api/webhooks/stripe/route.ts`:

```typescript
// Key events handled:
// - checkout.session.completed → Add credits or create subscription
// - customer.subscription.updated → Update subscription tier, add credits for upgrades
// - customer.subscription.deleted → Mark subscription canceled
// - invoice.payment_succeeded → Add monthly credits on renewal
// - customer.subscription.trial_will_end → Send trial ending notification

// Subscription tier is stored as plan KEY (e.g., 'pro'), not name ('Professional')
await supabaseAdmin
  .from('profiles')
  .update({
    subscription_status: subscription.status,
    subscription_tier: planMetadata.key, // 'pro', not 'Professional'
  })
  .eq('id', userId);
```

## Key Types

```typescript
// From shared/types/stripe.types.ts
interface IUserProfile {
  id: string;
  stripe_customer_id: string | null;
  subscription_credits_balance: number; // From subscription (expire at cycle end)
  purchased_credits_balance: number; // From purchases (never expire)
  subscription_status: SubscriptionStatus | null;
  subscription_tier: string | null; // Plan key: 'starter', 'pro', etc.
  role: 'user' | 'admin';
}

interface ISubscription {
  id: string; // Stripe subscription ID
  user_id: string;
  status: string;
  price_id: string;
  current_period_start: string;
  current_period_end: string;
  cancel_at_period_end: boolean;
  scheduled_price_id?: string; // For scheduled downgrades
  scheduled_change_date?: string;
}

type SubscriptionStatus = 'active' | 'trialing' | 'past_due' | 'canceled' | 'unpaid';
```

## Setup Scripts

### Initial Stripe Setup

```bash
# Create products and prices in Stripe dashboard, then update subscription.config.ts
yarn stripe:setup  # or scripts/stripe-setup.sh
```

### Manual Price Creation (via API)

```bash
# The stripe-setup.sh script uses curl to create products/prices:
curl -X POST \
  -u "$STRIPE_SECRET_KEY:" \
  -d "name=Professional Plan" \
  -d "description=For professionals - 1000 credits per month" \
  "https://api.stripe.com/v1/products"

curl -X POST \
  -u "$STRIPE_SECRET_KEY:" \
  -d "product=prod_xxx" \
  -d "currency=usd" \
  -d "unit_amount=4900" \
  -d "recurring[interval]=month" \
  "https://api.stripe.com/v1/prices"
```

## Common Patterns

### Checking User's Plan

```typescript
// From profile
const tier = user.profile?.subscription_tier; // 'starter', 'pro', etc.

// Display name
const displayName = getPlanDisplayName({ subscriptionTier: tier });

// Get plan config
const plan = getPlanByKey(tier);
const batchLimit = plan?.batchLimit ?? 1;
```

### Credit Operations

```typescript
// Check sufficient credits (RPC)
const { data } = await supabase.rpc('has_sufficient_credits', {
  target_user_id: userId,
  required_amount: 5,
});

// Deduct credits (RPC - handles dual pools)
const { data: newBalance } = await supabase.rpc('deduct_credits', {
  target_user_id: userId,
  amount: 5,
  ref_id: jobId,
  description: 'Image upscale',
});

// Add subscription credits (RPC)
await supabaseAdmin.rpc('add_subscription_credits', {
  target_user_id: userId,
  amount: 100,
  ref_id: subscriptionId,
  description: 'Monthly subscription credits',
});
```

### Proration Preview

```typescript
// Get proration cost before plan change
const preview = await stripe.invoices.retrieveUpcoming({
  customer: customerId,
  subscription: subscriptionId,
  subscription_items: [{ id: itemId, price: newPriceId }],
  subscription_proration_behavior: 'create_prorations',
});
```

## Environment Variables

```bash
# .env.client (public)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_xxx

# .env.api (secrets)
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

## Cloudflare Workers Compatibility

The Stripe client uses fetch-based HTTP client for edge compatibility:

```typescript
// server/stripe/config.ts
export const stripe = new Stripe(serverEnv.STRIPE_SECRET_KEY, {
  apiVersion: '2025-12-15.clover',
  httpClient: Stripe.createFetchHttpClient(),
  telemetry: false,
});
```

## Testing

```typescript
// Mock tokens for test mode
const token = 'test_token_mock_user_123';

// Test price IDs are accepted in test mode
// Configure ENV=test to enable mock responses
```
