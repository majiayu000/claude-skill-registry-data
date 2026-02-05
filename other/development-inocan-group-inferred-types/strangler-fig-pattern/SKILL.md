---
name: Strangler Fig Pattern
description: Safely replace legacy system piece by piece by building new implementation around it, routing traffic gradually, like a strangler fig tree
when_to_use: when you need to replace large legacy system without breaking production, cannot do big-bang rewrite, and need incremental migration path
version: 1.0.0
languages: all
---

# Strangler Fig Pattern

## Overview

The strangler fig tree grows around a host tree, gradually replacing it until the original tree is no longer needed. This pattern applies the same concept to legacy code: build the new system around the old, gradually route traffic to the new, eventually remove the old.

**Core principle:** Never rewrite big bang. Replace incrementally with production traffic validating each step.

**Named after:** Strangler fig trees that germinate in tree canopy, send roots down, eventually replace host tree.

## When to Use

Use strangler fig when:
- Legacy system is too large for big-bang rewrite
- System must stay operational during migration
- Risk of breaking changes is high
- You can't afford months without deploying
- Want to validate new implementation with real traffic
- Need ability to rollback at any step

**Don't use when:**
- System is small (just rewrite it)
- Can afford downtime
- Legacy and new can't coexist (architectural impossibility)

## The Iron Law

```
NEVER BIG-BANG REWRITE
```

Rewrites fail. Incremental replacement succeeds. Always choose strangler fig over rewrite.

## The Six-Step Process

### Step 1: Identify a Seam

**Find natural boundary in legacy code.**

**Good seams:**
- Module boundaries (payment processing, user management)
- API endpoints (/api/users, /api/orders)
- Feature boundaries (search, recommendations)
- Data boundaries (user service talks to user DB)

**Bad seams:**
- Middle of a function
- Arbitrary line in code
- "Everything that touches X"

**How to find seams:**
```bash
# Look for boundaries in architecture
- Separate modules/packages
- API boundaries
- Database boundaries
- Clear input/output contracts
```

**Example: E-commerce checkout**
```
Good seam: The entire checkout flow
- Input: Cart + user
- Output: Order confirmation
- Clear boundary

Bad seam: "The part that calculates tax"
- Too granular
- Too coupled with pricing, shipping
```

### Step 2: Add Characterization Tests

**Before touching anything: safety net.**

See `skills/refactoring/characterization-testing/SKILL.md`

```typescript
// Characterize current behavior
test('legacy checkout creates order', async () => {
  const cart = { items: [{ id: '123', quantity: 2 }] };
  const user = { id: 'user-456' };

  const order = await legacyCheckout(cart, user);

  expect(order.status).toBe('pending');
  expect(order.total).toBe(29.98);
  expect(order.items).toHaveLength(1);
});
```

**All existing behavior must have tests.** No refactoring without safety net.

### Step 3: Create Abstraction Layer

**Add facade that can route to old OR new implementation.**

**Pattern:**
```typescript
// Before: Direct call to legacy
const order = await legacyCheckout(cart, user);

// After: Call through abstraction
const order = await checkoutService.process(cart, user);
```

**Implementation:**
```typescript
class CheckoutService {
  constructor(
    private legacyCheckout: LegacyCheckout,
    private newCheckout: NewCheckout | null,
    private featureFlags: FeatureFlags
  ) {}

  async process(cart: Cart, user: User): Promise<Order> {
    // Route to new or old based on feature flag
    if (this.newCheckout && this.featureFlags.isEnabled('new-checkout', user)) {
      return this.newCheckout.process(cart, user);
    }

    return this.legacyCheckout.process(cart, user);
  }
}
```

**Deploy abstraction layer.** At this point, 100% traffic still goes to legacy. Nothing changed functionally.

### Step 4: Implement New Version

**Build new implementation behind abstraction.**

```typescript
class NewCheckout {
  async process(cart: Cart, user: User): Promise<Order> {
    // New, clean implementation
    const validation = await this.validateCart(cart);
    const pricing = await this.calculatePricing(cart, user);
    const order = await this.createOrder(cart, user, pricing);
    await this.sendConfirmation(order, user);
    return order;
  }
}
```

**Key points:**
- New implementation starts disabled (feature flag off)
- Test new implementation thoroughly in isolation
- New implementation must satisfy same contract as legacy
- Don't touch legacy code during this step

### Step 5: Gradually Route Traffic

**The strangling part - slowly shift traffic to new implementation.**

**Phase 1: Dark launch (0% user traffic)**
```typescript
if (this.featureFlags.isEnabled('new-checkout-dark', user)) {
  // Call both, return legacy result, compare
  const legacyResult = await this.legacyCheckout.process(cart, user);
  const newResult = await this.newCheckout.process(cart, user);

  this.compareAndLog(legacyResult, newResult); // Log differences
  return legacyResult; // Always return legacy
}
```

**Purpose:** Validate new implementation with real data, zero user impact.

**Phase 2: Canary (1% user traffic)**
```typescript
if (this.featureFlags.isEnabled('new-checkout', user)) {
  return this.newCheckout.process(cart, user); // Real users!
}
return this.legacyCheckout.process(cart, user);
```

Enable for 1% of users. Monitor errors, performance, business metrics.

**Phase 3: Ramp up (10%, 25%, 50%, 100%)**
```
Week 1: 1% → Monitor
Week 2: 10% → Monitor
Week 3: 25% → Monitor
Week 4: 50% → Monitor
Week 5: 100% → Victory!
```

**At any stage: rollback is just flipping feature flag off.**

### Step 6: Remove Legacy Code

**Once 100% traffic on new implementation for extended period:**

1. **Verify legacy is unused**
   ```bash
   # Check logs: zero calls to legacy in past week
   grep "legacyCheckout" logs/* | wc -l  # Should be 0
   ```

2. **Remove legacy code**
   ```typescript
   class CheckoutService {
     async process(cart: Cart, user: User): Promise<Order> {
       // Legacy code removed
       return this.newCheckout.process(cart, user);
     }
   }
   ```

3. **Clean up abstraction (optional)**
   If abstraction was only for migration, remove it too:
   ```typescript
   // Direct call to new implementation
   const order = await newCheckout.process(cart, user);
   ```

## Feature Flag Patterns

### Simple Boolean Flag

```typescript
// config/features.ts
export const features = {
  'new-checkout': process.env.NEW_CHECKOUT_ENABLED === 'true'
};
```

**Pros:** Simple
**Cons:** Requires deploy to change, all-or-nothing

### User-Based Rollout

```typescript
class FeatureFlags {
  isEnabled(flag: string, user: User): boolean {
    if (flag === 'new-checkout') {
      // Gradually roll out based on user ID
      const rolloutPercent = this.getRolloutPercent('new-checkout'); // 0-100
      const userHash = hashCode(user.id) % 100;
      return userHash < rolloutPercent;
    }
    return false;
  }
}
```

**Pros:** Gradual rollout, specific user targeting, no deploy needed
**Cons:** More complex

### A/B Test Pattern

```typescript
// Compare old vs new
const variant = this.abTest.getVariant('checkout-test', user);

if (variant === 'new') {
  result = await this.newCheckout.process(cart, user);
  this.metrics.track('checkout.new', result);
} else {
  result = await this.legacyCheckout.process(cart, user);
  this.metrics.track('checkout.legacy', result);
}
```

**Measures:** Which implementation performs better (conversion, speed, errors)

## Monitoring During Migration

**Critical metrics to track:**

```typescript
// Error rates
this.metrics.increment('checkout.new.error');
this.metrics.increment('checkout.legacy.error');

// Performance
this.metrics.timing('checkout.new.duration', duration);
this.metrics.timing('checkout.legacy.duration', duration);

// Business metrics
this.metrics.increment('checkout.new.success');
this.metrics.increment('checkout.new.abandoned');
```

**Red flags requiring rollback:**
- Error rate >2x legacy
- P95 latency >1.5x legacy
- Conversion rate drop >5%
- Revenue drop

## Checklist

- [ ] Identified clear seam with well-defined input/output
- [ ] Added characterization tests for legacy behavior
- [ ] Created abstraction layer (facade/router)
- [ ] Deployed abstraction layer (100% traffic to legacy still)
- [ ] Implemented new version with tests
- [ ] Dark launched (0% user traffic, compare results)
- [ ] Canary release (1% users)
- [ ] Monitored metrics (errors, performance, business)
- [ ] Gradually ramped up (10%, 25%, 50%, 100%)
- [ ] Verified legacy is unused
- [ ] Removed legacy code
- [ ] Cleaned up migration scaffolding

## Real-World Example

### Context
Legacy payment processing (2000 lines, 5 years old, no tests, handles $1M/day)

### Step 1: Identify Seam
```
Seam: processPayment(order, card) → PaymentResult
Clear input/output, isolated from rest of system
```

### Step 2: Characterization Tests
```typescript
test('legacy payment: successful charge', async () => {
  const order = { total: 29.99 };
  const card = { number: '4111111111111111', cvv: '123' };

  const result = await legacyPaymentProcessor.process(order, card);

  expect(result.status).toBe('success');
  expect(result.transactionId).toBeDefined();
  expect(result.amount).toBe(29.99);
});

// 20+ more tests for edge cases, errors, etc.
```

### Step 3: Abstraction Layer
```typescript
class PaymentService {
  async process(order: Order, card: Card): Promise<PaymentResult> {
    if (this.flags.isEnabled('new-payment-processor')) {
      return this.newProcessor.process(order, card);
    }
    return this.legacyProcessor.process(order, card);
  }
}
```

### Step 4: New Implementation
```typescript
class NewPaymentProcessor {
  async process(order: Order, card: Card): Promise<PaymentResult> {
    const token = await this.stripe.createToken(card);
    const charge = await this.stripe.charge({
      amount: order.total,
      token: token.id
    });
    return {
      status: 'success',
      transactionId: charge.id,
      amount: charge.amount
    };
  }
}
```

### Step 5: Gradual Rollout
```
Week 1: Dark launch - 0% users, compare results
Week 2: 1% canary - monitor error rates
Week 3: 10% - all metrics green
Week 4: 50% - confidence high
Week 5: 100% - complete!
```

### Step 6: Remove Legacy
```typescript
// 2000 lines of legacy code → deleted
// Saved ongoing maintenance cost
// New implementation: 100 lines, tested, modern API
```

## Anti-Patterns

### ❌ Big-Bang Switchover

**Bad:** Build new system for months, switch all traffic at once
**Good:** Gradual rollout with ability to rollback

Big-bang = all eggs in one basket. Gradual = validate each step.

### ❌ No Abstraction Layer

**Bad:** If statements scattered everywhere checking feature flags
**Good:** Single routing point in abstraction layer

Abstraction contains the mess, makes rollback simple.

### ❌ Touching Legacy During Migration

**Bad:** "While I'm here, let me fix this bug in legacy..."
**Good:** Don't touch legacy. All effort into new implementation.

Touching legacy = risk. New implementation will replace it anyway.

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| "I'll do it all at once" | Big-bang rewrites fail. Strangler fig succeeds. |
| "I don't need feature flags" | Feature flags enable rollback. Rollback saves production. |
| "Legacy works, so new implementation must match exactly" | Legacy has bugs. New can fix them. Match contract, not bugs. |
| "I'll migrate when new is perfect" | Perfect = never. Ship at "good enough", iterate. |
| "100% traffic → delete legacy immediately" | Wait 2-4 weeks at 100% before deleting. Verify first. |

## Integration with Other Skills

- **skills/refactoring/characterization-testing** - Safety net before strangling
- **skills/refactoring/seam-finding** - How to find good boundaries
- **skills/safety/feature-flags-for-legacy** - Routing mechanism
- **skills/refactoring/parallel-change** - Similar incremental pattern

## Remember

- Never big-bang rewrite
- Abstraction layer is key
- Gradual rollout with monitoring
- Feature flags enable rollback
- Wait before deleting legacy (verify unused)
- New implementation can fix legacy bugs
- Strangler fig = proven pattern for legacy replacement
