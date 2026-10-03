---
name: credit-admin
description: Manually manage user credits and subscription state directly via Supabase for support cases (webhook failures, missing credits, plan not activated). Use when a customer paid but didn't receive credits/plan activation.
---

# Credit Admin Operations

## When to use this

- Customer paid but subscription didn't activate (webhook failure)
- Missing credits after plan change
- Goodwill credit grants for support issues
- Manual plan activation after payment confirmation

## Security model

Direct updates to `subscription_credits_balance` and `purchased_credits_balance` are **blocked by a DB trigger** (`protect_credits_balance`). You MUST use the designated RPCs below.

Updates to `subscription_status` and `subscription_tier` on the `profiles` table are allowed directly.

## Setup

Use the service role key from `.env.api` (`SUPABASE_SERVICE_ROLE_KEY`) with the Supabase URL from `.env.client` (`NEXT_PUBLIC_SUPABASE_URL`).

```js
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY);
```

## Finding a user

Profiles table does NOT have an email column. Look up via `auth.admin.listUsers()`:

```js
const {
  data: { users },
} = await supabase.auth.admin.listUsers({ page: 1, perPage: 1000 });
const user = users.find(u => u.email === 'customer@example.com');
// user.id is the UUID used everywhere
```

## Checking user state

```js
const { data: profile } = await supabase
  .from('profiles')
  .select(
    'subscription_status, subscription_tier, subscription_credits_balance, purchased_credits_balance, stripe_customer_id'
  )
  .eq('id', userId)
  .single();

const { data: subs } = await supabase.from('subscriptions').select('*').eq('user_id', userId);

const { data: txns } = await supabase
  .from('credit_transactions')
  .select('*')
  .eq('user_id', userId)
  .order('created_at', { ascending: false })
  .limit(20);
```

## Granting subscription credits (RPC — bypasses trigger)

Use `add_subscription_credits` for subscription pool grants (plan grants, goodwill, etc.):

```js
const { data, error } = await supabase.rpc('add_subscription_credits', {
  target_user_id: userId,
  amount: 200,
  ref_id: 'manual_fix_hobby_2026_03_29', // unique, prevents double-grants
  description: 'Manual grant: Hobby plan 200 credits - webhook failure on signup',
});
// data = new balance
```

Use `add_purchased_credits` for purchased credit pool:

```js
const { data, error } = await supabase.rpc('add_purchased_credits', {
  target_user_id: userId,
  amount: 20,
  ref_id: 'goodwill_2026_03_29',
  description: 'Goodwill credits - apology for activation delay',
});
```

**Always use a unique `ref_id`** — the webhook handler checks for duplicate ref*ids to prevent double-grants. Format: `manual*<reason>\_<date>`.

## Activating a subscription (profile update)

Profile status/tier columns are NOT credit columns — direct update is allowed:

```js
const { error } = await supabase
  .from('profiles')
  .update({
    subscription_status: 'active', // 'active' | 'trialing' | 'canceled' | 'past_due'
    subscription_tier: 'hobby', // 'starter' | 'hobby' | 'pro' | 'business'
  })
  .eq('id', userId);
```

## Inserting a subscription record (when webhook never fired)

If `subscriptions` table is empty for the user and you don't have the Stripe sub ID, insert a placeholder:

```js
await supabase.from('subscriptions').insert({
  id: 'manual_hobby_' + userId.slice(0, 8), // placeholder ID
  user_id: userId,
  status: 'active',
  price_id: 'price_1Sz0fNL1vUl00LlZT6MMTxAg', // Hobby price ID from .env.client
  current_period_start: new Date().toISOString(),
  current_period_end: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
  cancel_at_period_end: false,
});
```

Note: When the real Stripe webhook eventually fires (e.g., on renewal), it will upsert the correct record using the real Stripe sub ID.

## Plan price IDs (from .env.client)

| Plan     | Price ID                            | Credits/mo |
| -------- | ----------------------------------- | ---------- |
| Starter  | `NEXT_PUBLIC_STRIPE_PRICE_STARTER`  | 50         |
| Hobby    | `price_1Sz0fNL1vUl00LlZT6MMTxAg`    | 200        |
| Pro      | `NEXT_PUBLIC_STRIPE_PRICE_PRO`      | 500        |
| Business | `NEXT_PUBLIC_STRIPE_PRICE_BUSINESS` | 1500       |

## Full fix script for "paid but not activated" support case

```js
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY);

async function fixSubscription(email, planKey, credits) {
  // 1. Find user
  const {
    data: { users },
  } = await supabase.auth.admin.listUsers({ page: 1, perPage: 1000 });
  const user = users.find(u => u.email === email);
  if (!user) throw new Error('User not found: ' + email);

  // 2. Activate profile
  await supabase
    .from('profiles')
    .update({
      subscription_status: 'active',
      subscription_tier: planKey,
    })
    .eq('id', user.id);

  // 3. Grant credits
  const date = new Date().toISOString().slice(0, 10).replace(/-/g, '_');
  const { data: newBalance } = await supabase.rpc('add_subscription_credits', {
    target_user_id: user.id,
    amount: credits,
    ref_id: `manual_fix_${planKey}_${date}`,
    description: `Manual grant: ${planKey} plan ${credits} credits - webhook failure`,
  });

  console.log(`Fixed ${email}: plan=${planKey}, new balance=${newBalance}`);
}

// Example: fixSubscription('customer@gmail.com', 'hobby', 200)
```

## Adding goodwill credits (bonus on top of plan credits)

```js
const { data: newBalance } = await supabase.rpc('add_subscription_credits', {
  target_user_id: userId,
  amount: 20,
  ref_id: 'goodwill_' + new Date().toISOString().slice(0, 10).replace(/-/g, '_'),
  description: 'Goodwill credits - support apology',
});
```
