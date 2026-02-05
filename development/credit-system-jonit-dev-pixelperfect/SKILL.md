---
name: credit-system
description: Implement and manage complex credit system with subscription credits, purchased credits, rollover logic, and atomic transactions. Use when working with credit deductions, refunds, subscriptions, and billing.
---

# Credit System Implementation

## Overview

The credit system handles two separate credit pools:

- **Subscription Credits**: Monthly allocation from subscription plans
- **Purchased Credits**: One-time purchases that never expire

## Key Concepts

### Credit Pools

- Subscription credits expire and rollover with caps
- Purchased credits are permanent
- Always deduct subscription credits first

### Rollover Logic

- Unused subscription credits roll over to next cycle
- Capped based on plan (e.g., Pro caps at 200% of monthly allocation)
- Purchased credits don't count toward rollover caps

### Atomic Operations

- All credit operations must be atomic
- Use database transactions to prevent race conditions
- Create audit trails for all transactions

## Database Functions

### Deduct Credits (Subscription First)

```sql
CREATE OR REPLACE FUNCTION deduct_credits(
  p_user_id UUID,
  p_amount INTEGER,
  p_reason TEXT DEFAULT 'image_generation'
) RETURNS TABLE(
  success BOOLEAN,
  subscription_used INTEGER,
  purchased_used INTEGER,
  new_balance_subscription INTEGER,
  new_balance_purchased INTEGER,
  transaction_id UUID
) LANGUAGE plpgsql SECURITY DEFINER AS $$
DECLARE
  v_transaction_id UUID := gen_random_uuid();
  v_subscription_balance INTEGER;
  v_purchased_balance INTEGER;
  v_subscription_to_deduct INTEGER;
  v_purchased_to_deduct INTEGER;
BEGIN
  -- Lock user credits row to prevent race conditions
  PERFORM 1 FROM user_credits WHERE user_id = p_user_id FOR UPDATE;

  -- Get current balances
  SELECT subscription_credits, purchased_credits
  INTO v_subscription_balance, v_purchased_balance
  FROM user_credits
  WHERE user_id = p_user_id;

  -- Check if enough credits
  IF v_subscription_balance + v_purchased_balance < p_amount THEN
    RETURN QUERY SELECT false, 0, 0, v_subscription_balance, v_purchased_balance, v_transaction_id;
    RETURN;
  END IF;

  -- Calculate deduction: subscription first, then purchased
  v_subscription_to_deduct := LEAST(v_subscription_balance, p_amount);
  v_purchased_to_deduct := p_amount - v_subscription_to_deduct;

  -- Update balances
  UPDATE user_credits SET
    subscription_credits = subscription_credits - v_subscription_to_deduct,
    purchased_credits = purchased_credits - v_purchased_to_deduct,
    updated_at = now()
  WHERE user_id = p_user_id;

  -- Record transaction
  INSERT INTO credit_transactions (
    id, user_id, amount, reason,
    subscription_credits_before, subscription_credits_after,
    purchased_credits_before, purchased_credits_after,
    created_at
  ) VALUES (
    v_transaction_id, p_user_id, -p_amount, p_reason,
    v_subscription_balance, v_subscription_balance - v_subscription_to_deduct,
    v_purchased_balance, v_purchased_balance - v_purchased_to_deduct,
    now()
  );

  RETURN QUERY SELECT
    true,
    v_subscription_to_deduct,
    v_purchased_to_deduct,
    v_subscription_balance - v_subscription_to_deduct,
    v_purchased_balance - v_purchased_to_deduct,
    v_transaction_id;
END;
$$;
```

### Add Subscription Credits with Rollover

```sql
CREATE OR REPLACE FUNCTION add_subscription_credits(
  p_user_id UUID,
  p_amount INTEGER,
  p_rollover_cap INTEGER DEFAULT NULL, -- NULL = no cap
  p_reason TEXT DEFAULT 'monthly_grant'
) RETURNS TABLE(
  credits_added INTEGER,
  rollover_credits INTEGER,
  new_balance INTEGER,
  expired_credits INTEGER
) LANGUAGE plpgsql SECURITY DEFINER AS $$
DECLARE
  v_current_balance INTEGER;
  v_current_rollover INTEGER;
  v_total_before INTEGER;
  v_total_after INTEGER;
  v_expired INTEGER := 0;
  v_rollover_to_add INTEGER := 0;
  v_credits_to_add INTEGER := p_amount;
BEGIN
  -- Lock row
  PERFORM 1 FROM user_credits WHERE user_id = p_user_id FOR UPDATE;

  -- Get current state
  SELECT
    subscription_credits,
    rollover_credits,
    last_credit_reset
  INTO v_current_balance, v_current_rollover, last_credit_reset
  FROM user_credits
  WHERE user_id = p_user_id;

  -- Calculate total before
  v_total_before := v_current_balance + v_current_rollover;

  -- Handle expiration (if monthly reset)
  -- This would be called by a separate monthly reset function

  -- Add new credits
  v_current_balance := v_current_balance + p_amount;

  -- Handle rollover
  IF p_rollover_cap IS NOT NULL THEN
    -- Calculate what would be over cap
    IF v_current_balance > p_rollover_cap THEN
      v_rollover_to_add := v_current_balance - p_rollover_cap;
      v_current_balance := p_rollover_cap;
    END IF;
  END IF;

  -- Update database
  UPDATE user_credits SET
    subscription_credits = v_current_balance,
    rollover_credits = v_current_rollover + v_rollover_to_add,
    updated_at = now()
  WHERE user_id = p_user_id;

  -- Return results
  v_total_after := v_current_balance + v_current_rollover + v_rollover_to_add;

  RETURN QUERY SELECT
    v_credits_to_add,
    v_rollover_to_add,
    v_current_balance,
    v_expired;
END;
$$;
```

### Refund Credits (Original Pool)

```sql
CREATE OR REPLACE FUNCTION refund_credits(
  p_transaction_id UUID,
  p_reason TEXT DEFAULT 'refund'
) RETURNS BOOLEAN LANGUAGE plpgsql SECURITY DEFINER AS $$
DECLARE
  v_user_id UUID;
  v_amount INTEGER;
  v_original_reason TEXT;
  v_subscription_used INTEGER;
  v_purchased_used INTEGER;
BEGIN
  -- Get original transaction details
  SELECT user_id, amount, reason, subscription_credits_used, purchased_credits_used
  INTO v_user_id, v_amount, v_original_reason, v_subscription_used, v_purchased_used
  FROM credit_transactions
  WHERE id = p_transaction_id;

  -- Lock user credits
  PERFORM 1 FROM user_credits WHERE user_id = v_user_id FOR UPDATE;

  -- Refund to original pools
  UPDATE user_credits SET
    subscription_credits = subscription_credits + v_subscription_used,
    purchased_credits = purchased_credits + v_purchased_used,
    updated_at = now()
  WHERE user_id = v_user_id;

  -- Record refund transaction
  INSERT INTO credit_transactions (
    user_id, amount, reason,
    subscription_credits_used, purchased_credits_used,
    refund_transaction_id, created_at
  ) VALUES (
    v_user_id, v_amount, p_reason,
    v_subscription_used, v_purchased_used,
    p_transaction_id, now()
  );

  RETURN true;
END;
$$;
```

## Service Layer Patterns

### Credit Transaction Service

```typescript
export interface ICreditTransaction {
  id: string;
  userId: string;
  amount: number;
  reason: string;
  subscriptionCreditsUsed: number;
  purchasedCreditsUsed: number;
  createdAt: Date;
}

export interface ICreditDeductionRequest {
  userId: string;
  amount: number;
  reason?: string;
}

export interface ICreditDeductionResult {
  success: boolean;
  transactionId?: string;
  subscriptionUsed: number;
  purchasedUsed: number;
  newSubscriptionBalance: number;
  newPurchasedBalance: number;
  error?: string;
}

export class CreditTransactionService {
  /**
   * Deduct credits atomically with subscription-first logic
   */
  static async deductCredits(request: ICreditDeductionRequest): Promise<ICreditDeductionResult> {
    const { userId, amount, reason = 'usage' } = request;

    // Validate input
    if (amount <= 0) {
      return {
        success: false,
        subscriptionUsed: 0,
        purchasedUsed: 0,
        newSubscriptionBalance: 0,
        newPurchasedBalance: 0,
        error: 'Amount must be positive',
      };
    }

    try {
      // Use database transaction for atomicity
      const result = await supabase.rpc('deduct_credits', {
        p_user_id: userId,
        p_amount: amount,
        p_reason: reason,
      });

      if (result.error) {
        throw new Error(result.error.message);
      }

      const data = result.data[0];

      return {
        success: data.success,
        transactionId: data.transaction_id,
        subscriptionUsed: data.subscription_used,
        purchasedUsed: data.purchased_used,
        newSubscriptionBalance: data.new_balance_subscription,
        newPurchasedBalance: data.new_balance_purchased,
        error: data.success ? undefined : 'Insufficient credits',
      };
    } catch (error) {
      return {
        success: false,
        subscriptionUsed: 0,
        purchasedUsed: 0,
        newSubscriptionBalance: 0,
        newPurchasedBalance: 0,
        error: error.message,
      };
    }
  }

  /**
   * Refund credits to original pools
   */
  static async refundCredits(transactionId: string, reason?: string): Promise<boolean> {
    try {
      const result = await supabase.rpc('refund_credits', {
        p_transaction_id: transactionId,
        p_reason: reason || 'refund',
      });

      return !result.error && result.data;
    } catch (error) {
      console.error('Refund failed:', error);
      return false;
    }
  }

  /**
   * Get credit balance for user
   */
  static async getBalance(userId: string): Promise<{
    subscription: number;
    purchased: number;
    total: number;
  }> {
    const { data, error } = await supabase
      .from('user_credits')
      .select('subscription_credits, purchased_credits')
      .eq('user_id', userId)
      .single();

    if (error || !data) {
      return { subscription: 0, purchased: 0, total: 0 };
    }

    return {
      subscription: data.subscription_credits,
      purchased: data.purchased_credits,
      total: data.subscription_credits + data.purchased_credits,
    };
  }
}
```

### Subscription Credit Service

```typescript
export interface ISubscriptionTier {
  id: string;
  creditsPerCycle: number;
  rolloverCapPercentage: number; // e.g., 200 = 200% of monthly
}

export class SubscriptionCreditService {
  /**
   * Calculate rollover cap for tier
   */
  static calculateRolloverCap(tier: ISubscriptionTier): number {
    return Math.floor(tier.creditsPerCycle * (tier.rolloverCapPercentage / 100));
  }

  /**
   * Process monthly credit renewal
   */
  static async processMonthlyRenewal(
    userId: string,
    tier: ISubscriptionTier
  ): Promise<{
    added: number;
    rollover: number;
    expired: number;
    total: number;
  }> {
    const rolloverCap = this.calculateRolloverCap(tier);

    // Reset and add new credits with rollover logic
    const result = await supabase.rpc('add_subscription_credits', {
      p_user_id: userId,
      p_amount: tier.creditsPerCycle,
      p_rollover_cap: rolloverCap,
      p_reason: 'monthly_renewal',
    });

    if (result.error) {
      throw new Error(result.error.message);
    }

    const data = result.data[0];

    // Record audit trail
    await this.recordRenewal(userId, tier, data);

    return {
      added: data.credits_added,
      rollover: data.rollover_credits,
      expired: data.expired_credits,
      total: data.new_balance,
    };
  }

  /**
   * Handle upgrade credits (use SubscriptionCreditsService)
   */
  static async handleUpgrade(
    userId: string,
    previousTier: ISubscriptionTier,
    newTier: ISubscriptionTier,
    currentBalance: number
  ): Promise<number> {
    // Use the existing SubscriptionCreditsService for calculations
    const { SubscriptionCreditsService } = await import('./SubscriptionCredits');

    const calculation = SubscriptionCreditsService.calculateUpgradeCredits({
      currentBalance,
      previousTierCredits: previousTier.creditsPerCycle,
      newTierCredits: newTier.creditsPerCycle,
    });

    if (calculation.creditsToAdd > 0) {
      await supabase.rpc('add_subscription_credits', {
        p_user_id: userId,
        p_amount: calculation.creditsToAdd,
        p_reason: 'upgrade_bonus',
      });
    }

    return calculation.creditsToAdd;
  }

  private static async recordRenewal(
    userId: string,
    tier: ISubscriptionTier,
    data: any
  ): Promise<void> {
    // Create audit record
    await supabase.from('credit_renewals').insert({
      user_id: userId,
      tier_id: tier.id,
      credits_added: data.credits_added,
      rollover_credits: data.rollover_credits,
      expired_credits: data.expired_credits,
      new_balance: data.new_balance,
    });
  }
}
```

## Testing Patterns

### Unit Tests

```typescript
describe('CreditTransactionService', () => {
  describe('deductCredits', () => {
    it('should deduct subscription credits first', async () => {
      // Setup: User has 50 subscription, 30 purchased
      // Test: Deduct 60 credits
      // Expect: 50 subscription used, 10 purchased used
    });

    it('should fail with insufficient credits', async () => {
      // Setup: User has 10 credits total
      // Test: Deduct 20 credits
      // Expect: Failure with error message
    });

    it('should handle concurrent requests safely', async () => {
      // Test: Multiple concurrent deductions
      // Expect: No race conditions, atomic operations
    });
  });

  describe('refundCredits', () => {
    it('should refund to original pools', async () => {
      // Setup: Deducted 40 credits (30 subscription, 10 purchased)
      // Test: Refund transaction
      // Expect: 30 subscription restored, 10 purchased restored
    });
  });
});
```

### Integration Tests

```typescript
describe('Credit System Integration', () => {
  it('should handle full credit lifecycle', async () => {
    // 1. Grant monthly credits
    // 2. Add purchased credits
    // 3. Deduct credits (subscription first)
    // 4. Process monthly renewal with rollover
    // 5. Verify all balances and audit trail
  });
});
```

## Best Practices

### Preventing Race Conditions

1. Always use `SELECT ... FOR UPDATE` to lock rows
2. Keep transactions short and focused
3. Use database functions for atomic operations
4. Implement proper retry logic

### Audit Trail

1. Record every credit movement
2. Link refunds to original transactions
3. Store before/after balances
4. Include reason codes

### Performance

1. Index user_credits.user_id
2. Batch credit operations when possible
3. Use materialized views for reporting
4. Cache frequently accessed balances

### Error Handling

1. Validate all inputs
2. Use explicit transactions
3. Log all failures
4. Implement circuit breakers for external dependencies

## Monitoring

### Key Metrics

- Credit deduction success rate
- Average transaction time
- Credit pool distribution
- Rollover utilization
- Refund rate by reason

### Alerts

- Failed credit transactions
- Unusual credit balance changes
- High refund rates
- Database lock timeouts
