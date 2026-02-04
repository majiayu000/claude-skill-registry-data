---
name: using-interactive-transactions
description: Use interactive transactions with $transaction callback for atomic operations and automatic rollback. Use when operations must succeed or fail together.
allowed-tools:
  - Read
  - Write
  - Edit
---

# Interactive Transactions

Use the `$transaction` callback API for operations that must succeed or fail atomically. Interactive transactions provide automatic rollback on errors and allow complex multi-step logic.

## When to Use

Use interactive transactions when:
- Multiple operations must all succeed or all fail
- Operations depend on results from previous operations
- Complex business logic requires atomic execution
- Implementing financial transfers, inventory management, or state changes

Do NOT use for:
- Single operations (no transaction needed)
- Read-only operations (use batch queries instead)
- Independent operations that can fail separately

## $transaction Callback Pattern

```typescript
await prisma.$transaction(async (tx) => {
  const result1 = await tx.model1.create({ data: { ... } });

  const result2 = await tx.model2.update({
    where: { id: result1.relatedId },
    data: { ... }
  });

  return { result1, result2 };
});
```

All operations use the `tx` client. If any operation throws, the entire transaction rolls back automatically.

## Banking Transfer Example

```typescript
async function transferMoney(fromId: string, toId: string, amount: number) {
  return await prisma.$transaction(async (tx) => {
    const fromAccount = await tx.account.findUnique({
      where: { id: fromId }
    });

    if (!fromAccount || fromAccount.balance < amount) {
      throw new Error('Insufficient funds');
    }

    const updatedFrom = await tx.account.update({
      where: { id: fromId },
      data: { balance: { decrement: amount } }
    });

    const updatedTo = await tx.account.update({
      where: { id: toId },
      data: { balance: { increment: amount } }
    });

    const transfer = await tx.transfer.create({
      data: {
        fromAccountId: fromId,
        toAccountId: toId,
        amount
      }
    });

    return { updatedFrom, updatedTo, transfer };
  });
}
```

If any step fails, all changes roll back. Both accounts and the transfer record are consistent.

## Inventory Reservation Pattern

```typescript
async function reserveInventory(orderId: string, items: Array<{ productId: string; quantity: number }>) {
  return await prisma.$transaction(async (tx) => {
    const order = await tx.order.update({
      where: { id: orderId },
      data: { status: 'PROCESSING' }
    });

    for (const item of items) {
      const product = await tx.product.findUnique({
        where: { id: item.productId }
      });

      if (!product || product.stock < item.quantity) {
        throw new Error(`Insufficient stock for product ${item.productId}`);
      }

      await tx.product.update({
        where: { id: item.productId },
        data: { stock: { decrement: item.quantity } }
      });

      await tx.orderItem.create({
        data: {
          orderId,
          productId: item.productId,
          quantity: item.quantity,
          price: product.price
        }
      });
    }

    return await tx.order.update({
      where: { id: orderId },
      data: { status: 'RESERVED' }
    });
  });
}
```

If stock is insufficient for any item, the entire reservation rolls back. No partial inventory deductions occur.

## Multi-Step Atomic Operations

```typescript
async function createUserWithProfile(userData: UserData, profileData: ProfileData) {
  return await prisma.$transaction(async (tx) => {
    const user = await tx.user.create({
      data: {
        email: userData.email,
        name: userData.name
      }
    });

    const profile = await tx.profile.create({
      data: {
        userId: user.id,
        bio: profileData.bio,
        avatar: profileData.avatar
      }
    });

    await tx.notification.create({
      data: {
        userId: user.id,
        message: 'Welcome to our platform!'
      }
    });

    return { user, profile };
  });
}
```

User, profile, and notification are created atomically. If profile creation fails, the user is not created.

## Error Handling and Rollback

```typescript
try {
  const result = await prisma.$transaction(async (tx) => {
    const step1 = await tx.model.create({ data: { ... } });

    if (someCondition) {
      throw new Error('Business rule violation');
    }

    const step2 = await tx.model.update({ ... });

    return { step1, step2 };
  });
} catch (error) {
  console.error('Transaction failed, all changes rolled back:', error);
}
```

Any thrown error triggers automatic rollback. No manual cleanup needed.

## Transaction Timeout

```typescript
await prisma.$transaction(async (tx) => {

}, {
  timeout: 10000
});
```

Default timeout is 5 seconds. Increase for long-running transactions.

## Isolation Level

```typescript
await prisma.$transaction(async (tx) => {

}, {
  isolationLevel: 'Serializable'
});
```

Available levels: `ReadUncommitted`, `ReadCommitted`, `RepeatableRead`, `Serializable`. Default is database-specific.

## Common Patterns

**Conditional Rollback:**
```typescript
await prisma.$transaction(async (tx) => {
  const record = await tx.model.create({ data: { ... } });

  if (!isValid(record)) {
    throw new Error('Validation failed');
  }

  return record;
});
```

**Dependent Operations:**
```typescript
await prisma.$transaction(async (tx) => {
  const parent = await tx.parent.create({ data: { ... } });
  const child = await tx.child.create({
    data: { parentId: parent.id, ... }
  });
  return { parent, child };
});
```

**Batch with Validation:**
```typescript
await prisma.$transaction(async (tx) => {
  const records = await Promise.all(
    items.map(item => tx.model.create({ data: item }))
  );

  if (records.length !== items.length) {
    throw new Error('Not all records created');
  }

  return records;
});
```

## Anti-Patterns

**Mixing transaction and non-transaction calls:**
```typescript
await prisma.$transaction(async (tx) => {
  await tx.model.create({ data: { ... } });
  await prisma.model.create({ data: { ... } });
});
```

Use `tx` for ALL operations inside the transaction.

**Long-running operations:**
```typescript
await prisma.$transaction(async (tx) => {
  await tx.model.create({ data: { ... } });
  await fetch('https://api.example.com');
  await tx.model.update({ ... });
});
```

Keep external API calls outside transactions. Transactions hold database locks.

**Catching errors inside transaction:**
```typescript
await prisma.$transaction(async (tx) => {
  try {
    await tx.model.create({ data: { ... } });
  } catch (error) {

  }
  await tx.model.update({ ... });
});
```

Let errors propagate to trigger rollback. Handle errors outside the transaction.

## Implementation Steps

1. **Identify atomic operations** that must succeed or fail together
2. **Wrap in $transaction callback** with `async (tx) => { ... }`
3. **Use tx client** for all operations inside the callback
4. **Validate before operations** to fail fast
5. **Throw errors** to trigger rollback on business rule violations
6. **Return result** from the callback for success case
7. **Handle errors** outside the transaction for logging/recovery

## Verification

After implementing interactive transactions:

1. Test successful execution path
2. Test rollback on database errors
3. Test rollback on business rule violations
4. Verify no partial state changes after failures
5. Check transaction timeout for long operations
6. Validate isolation level for concurrent access

Interactive transactions ensure data consistency through automatic rollback and atomic execution.
