---
name: configuring-transaction-isolation
description: Configure transaction isolation levels to prevent race conditions and handle concurrent access. Use when dealing with concurrent updates, financial operations, inventory management, or when users mention race conditions, dirty reads, phantom reads, or concurrent modifications.
allowed-tools: Read, Write, Edit
version: 1.0.0
---

# Transaction Isolation Levels

This skill teaches how to configure transaction isolation levels in Prisma to prevent race conditions and handle concurrent database access correctly.

---

<role>
This skill teaches Claude how to configure and use transaction isolation levels in Prisma 6 to prevent concurrency issues like race conditions, dirty reads, phantom reads, and lost updates.
</role>

<when-to-activate>
This skill activates when:

- User mentions race conditions, concurrent updates, or dirty reads
- Working with financial transactions, inventory systems, or booking platforms
- Implementing operations that must maintain consistency under concurrent access
- User asks about Serializable, RepeatableRead, or ReadCommitted isolation
- Dealing with P2034 errors (transaction conflicts)
</when-to-activate>

<overview>
Transaction isolation levels control how database transactions interact with each other when running concurrently. Prisma supports setting isolation levels to prevent common concurrency issues.

**Key Isolation Levels:**

1. **Serializable** - Strictest isolation, prevents all anomalies
2. **RepeatableRead** - Prevents dirty and non-repeatable reads
3. **ReadCommitted** - Prevents dirty reads only (default for most databases)
4. **ReadUncommitted** - No isolation (not recommended)

**Common Concurrency Issues:**

- **Dirty Reads:** Reading uncommitted changes from other transactions
- **Non-Repeatable Reads:** Same query returns different results within transaction
- **Phantom Reads:** New rows appear in repeated queries
- **Lost Updates:** Concurrent updates overwrite each other

**When to Set Isolation:**

- Financial operations (payments, transfers, refunds)
- Inventory management (stock reservations, order fulfillment)
- Booking systems (seat reservations, room bookings)
- Any operation requiring strict consistency
</overview>

<workflow>
## Standard Workflow

**Phase 1: Identify Concurrency Risk**

1. Analyze operation for concurrent access patterns
2. Determine what consistency guarantees are needed
3. Choose appropriate isolation level based on requirements

**Phase 2: Configure Isolation Level**

1. Set isolation level in transaction options
2. Implement proper error handling for conflicts
3. Add retry logic if appropriate

**Phase 3: Handle Isolation Conflicts**

1. Catch P2034 errors (transaction conflicts)
2. Retry with exponential backoff if appropriate
3. Return clear error messages to users
</workflow>

<isolation-level-guide>
## Isolation Level Quick Reference

| Level | Prevents | Use Cases | Trade-offs |
|-------|----------|-----------|------------|
| **Serializable** | All anomalies | Financial transactions, critical inventory | Highest consistency, lowest concurrency, more P2034 errors |
| **RepeatableRead** | Dirty reads, non-repeatable reads | Reports, multi-step reads | Good balance, still allows phantom reads |
| **ReadCommitted** | Dirty reads only | Standard operations, high-concurrency | Highest concurrency, allows non-repeatable/phantom reads |
| **ReadUncommitted** | Nothing | Not recommended | Almost never appropriate |

### Serializable Example

```typescript
await prisma.$transaction(
  async (tx) => {
    const account = await tx.account.findUnique({
      where: { id: accountId }
    });

    if (account.balance < amount) {
      throw new Error('Insufficient funds');
    }

    await tx.account.update({
      where: { id: accountId },
      data: { balance: { decrement: amount } }
    });

    await tx.transaction.create({
      data: {
        accountId,
        amount: -amount,
        type: 'WITHDRAWAL'
      }
    });
  },
  {
    isolationLevel: Prisma.TransactionIsolationLevel.Serializable
  }
);
```

### RepeatableRead Example

```typescript
await prisma.$transaction(
  async (tx) => {
    const user = await tx.user.findUnique({
      where: { id: userId },
      include: { orders: true }
    });

    const totalSpent = user.orders.reduce(
      (sum, order) => sum + order.amount,
      0
    );

    await tx.user.update({
      where: { id: userId },
      data: {
        tierLevel: calculateTier(totalSpent),
        lastCalculatedAt: new Date()
      }
    });
  },
  {
    isolationLevel: Prisma.TransactionIsolationLevel.RepeatableRead
  }
);
```

### ReadCommitted Example

```typescript
await prisma.$transaction(
  async (tx) => {
    await tx.log.create({
      data: {
        level: 'INFO',
        message: 'User logged in',
        userId
      }
    });

    await tx.user.update({
      where: { id: userId },
      data: { lastLoginAt: new Date() }
    });
  },
  {
    isolationLevel: Prisma.TransactionIsolationLevel.ReadCommitted
  }
);
```
</isolation-level-guide>

<decision-tree>
## Choosing Isolation Level

Follow this decision tree:

**Is this a financial operation (money, payments, credits)?**

- YES → Use `Serializable`
- NO → Continue

**Does the operation read data multiple times and require it to stay constant?**

- YES → Use `RepeatableRead`
- NO → Continue

**Is this a high-concurrency operation where conflicts are expensive?**

- YES → Use `ReadCommitted` (or no explicit isolation)
- NO → Continue

**Does the operation modify data based on a read within the transaction?**

- YES → Use `RepeatableRead` minimum
- NO → Use `ReadCommitted` (or no explicit isolation)

**Still unsure?**

- Start with `RepeatableRead` for safety
- Monitor P2034 error rate
- Adjust based on actual concurrency patterns
</decision-tree>

<error-handling>
## Handling Isolation Conflicts

### P2034: Transaction Conflict

When using Serializable isolation, conflicts are common under concurrency:

```typescript
async function transferWithRetry(
  fromId: string,
  toId: string,
  amount: number,
  maxRetries = 3
) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      await prisma.$transaction(
        async (tx) => {
          const fromAccount = await tx.account.findUnique({
            where: { id: fromId }
          });

          if (fromAccount.balance < amount) {
            throw new Error('Insufficient funds');
          }

          await tx.account.update({
            where: { id: fromId },
            data: { balance: { decrement: amount } }
          });

          await tx.account.update({
            where: { id: toId },
            data: { balance: { increment: amount } }
          });
        },
        {
          isolationLevel: Prisma.TransactionIsolationLevel.Serializable,
          maxWait: 5000,
          timeout: 10000
        }
      );

      return { success: true };

    } catch (error) {
      if (error.code === 'P2034' && attempt < maxRetries - 1) {
        await new Promise(resolve =>
          setTimeout(resolve, Math.pow(2, attempt) * 100)
        );
        continue;
      }

      throw error;
    }
  }

  throw new Error('Transaction failed after max retries');
}
```

**Key Elements:**

- Retry loop with attempt counter
- Check for P2034 error code
- Exponential backoff between retries
- maxWait and timeout configuration
- Final error if all retries exhausted

### Timeout Configuration

```typescript
{
  isolationLevel: Prisma.TransactionIsolationLevel.Serializable,
  maxWait: 5000,
  timeout: 10000
}
```

- `maxWait`: Maximum time to wait for transaction to start (milliseconds)
- `timeout`: Maximum time for transaction to complete (milliseconds)

Higher isolation levels need higher timeouts to handle conflicts.
</error-handling>

<constraints>
## Constraints and Guidelines

**MUST:**

- Use Serializable for financial operations
- Handle P2034 errors explicitly
- Set appropriate maxWait and timeout values
- Validate data before starting transaction
- Use atomic operations (increment/decrement) when possible

**SHOULD:**

- Implement retry logic with exponential backoff for Serializable
- Keep transactions as short as possible
- Read all data needed before making decisions
- Log isolation conflicts for monitoring
- Consider RepeatableRead before defaulting to Serializable

**NEVER:**

- Use ReadUncommitted in production
- Ignore P2034 errors
- Retry indefinitely without limit
- Mix isolation levels in same operation
- Assume isolation level is higher than default without setting it
</constraints>

<validation>
## Validation

After implementing isolation levels:

1. **Concurrency Testing:**

   - Simulate concurrent requests to same resource
   - Verify no lost updates or race conditions occur
   - Expected: Conflicts detected and handled gracefully

2. **Performance Monitoring:**

   - Monitor P2034 error rate
   - Track transaction retry attempts
   - If P2034 > 5%: Consider lowering isolation level or optimizing transaction duration

3. **Error Handling:**
   - Verify P2034 errors return user-friendly messages
   - Check retry logic executes correctly
   - Ensure transactions eventually succeed or fail definitively
</validation>

---

## References

For additional details and advanced scenarios, see:

- [Database-Specific Defaults](./references/database-defaults.md) - PostgreSQL, MySQL, SQLite, MongoDB isolation behaviors
- [Race Condition Patterns](./references/race-conditions.md) - Lost updates, double-booking, phantom reads
- [Complete Examples](./references/complete-examples.md) - Banking transfers, inventory reservations, seat bookings
