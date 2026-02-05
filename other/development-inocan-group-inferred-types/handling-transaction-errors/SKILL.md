---
name: handling-transaction-errors
description: Handle transaction errors properly with P-code checking and timeout configuration. Use when implementing transaction error recovery.
allowed-tools: Read, Write, Edit
---

# Transaction Error Handling

Handle transaction errors properly with P-code checking, timeout configuration, and recovery patterns.

## Error Catching in Transactions

All transaction operations must be wrapped in try/catch blocks to handle failures gracefully.

```typescript
try {
  await prisma.$transaction(async (tx) => {
    const user = await tx.user.create({
      data: { email: 'user@example.com' }
    });

    await tx.profile.create({
      data: { userId: user.id, bio: 'Hello' }
    });
  });
} catch (error) {
  if (error instanceof Prisma.PrismaClientKnownRequestError) {
    console.error(`Transaction failed: ${error.code}`);
  }
  throw error;
}
```

## P-Code Error Handling

### P2002: Unique Constraint Violation

```typescript
import { Prisma } from '@prisma/client';

try {
  await prisma.$transaction(async (tx) => {
    await tx.user.create({
      data: { email: 'duplicate@example.com' }
    });
  });
} catch (error) {
  if (
    error instanceof Prisma.PrismaClientKnownRequestError &&
    error.code === 'P2002'
  ) {
    const target = error.meta?.target as string[];
    throw new Error(`Unique constraint failed on: ${target.join(', ')}`);
  }
  throw error;
}
```

### P2025: Record Not Found

```typescript
try {
  await prisma.$transaction(async (tx) => {
    const user = await tx.user.update({
      where: { id: nonExistentId },
      data: { name: 'New Name' }
    });
  });
} catch (error) {
  if (
    error instanceof Prisma.PrismaClientKnownRequestError &&
    error.code === 'P2025'
  ) {
    throw new Error('Record to update not found');
  }
  throw error;
}
```

### Comprehensive P-Code Handler

```typescript
function handlePrismaError(error: unknown): Error {
  if (error instanceof Prisma.PrismaClientKnownRequestError) {
    switch (error.code) {
      case 'P2002':
        return new Error(
          `Unique constraint violation: ${error.meta?.target}`
        );
      case 'P2025':
        return new Error('Record not found');
      case 'P2034':
        return new Error('Transaction conflict, please retry');
      default:
        return new Error(`Database error: ${error.code}`);
    }
  }
  if (error instanceof Prisma.PrismaClientUnknownRequestError) {
    return new Error('Unknown database error');
  }
  if (error instanceof Prisma.PrismaClientValidationError) {
    return new Error('Invalid query parameters');
  }
  return error instanceof Error ? error : new Error('Unknown error');
}

try {
  await prisma.$transaction(async (tx) => {
    await tx.user.create({ data: { email: 'test@example.com' } });
  });
} catch (error) {
  throw handlePrismaError(error);
}
```

## Timeout Configuration

### Basic Timeout Settings

```typescript
await prisma.$transaction(
  async (tx) => {
    await tx.user.create({ data: { email: 'user@example.com' } });
    await tx.profile.create({ data: { userId: 1, bio: 'Bio' } });
  },
  {
    maxWait: 5000,
    timeout: 10000,
  }
);
```

Configuration:
- `maxWait`: Maximum time (ms) to wait for transaction to start (default: 2000)
- `timeout`: Maximum time (ms) for transaction to complete (default: 5000)

### Handling Timeout Errors

```typescript
try {
  await prisma.$transaction(
    async (tx) => {
      await tx.user.findMany();
      await new Promise(resolve => setTimeout(resolve, 15000));
    },
    { timeout: 10000 }
  );
} catch (error) {
  if (error instanceof Prisma.PrismaClientKnownRequestError) {
    if (error.message.includes('timeout')) {
      throw new Error('Transaction timed out, please try again');
    }
  }
  throw error;
}
```

### Long-Running Transactions

```typescript
await prisma.$transaction(
  async (tx) => {
    const users = await tx.user.findMany();

    for (const user of users) {
      await tx.auditLog.create({
        data: {
          userId: user.id,
          action: 'BATCH_UPDATE',
          timestamp: new Date(),
        }
      });
    }
  },
  {
    maxWait: 10000,
    timeout: 60000,
  }
);
```

## Recovery Patterns

### Retry Strategy with Exponential Backoff

```typescript
async function transactionWithRetry<T>(
  operation: (tx: Prisma.TransactionClient) => Promise<T>,
  maxRetries = 3
): Promise<T> {
  let lastError: Error | null = null;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await prisma.$transaction(operation, {
        timeout: 10000,
      });
    } catch (error) {
      lastError = error instanceof Error ? error : new Error('Unknown error');

      if (
        error instanceof Prisma.PrismaClientKnownRequestError &&
        error.code === 'P2034'
      ) {
        const delay = Math.pow(2, attempt) * 100;
        await new Promise(resolve => setTimeout(resolve, delay));
        continue;
      }

      throw error;
    }
  }

  throw new Error(`Transaction failed after ${maxRetries} retries: ${lastError?.message}`);
}

const result = await transactionWithRetry(async (tx) => {
  return await tx.user.create({
    data: { email: 'user@example.com' }
  });
});
```

### Idempotent Retry Pattern

```typescript
async function upsertWithRetry(email: string, name: string) {
  try {
    return await prisma.$transaction(async (tx) => {
      return await tx.user.upsert({
        where: { email },
        create: { email, name },
        update: { name },
      });
    });
  } catch (error) {
    if (
      error instanceof Prisma.PrismaClientKnownRequestError &&
      error.code === 'P2002'
    ) {
      return await prisma.user.update({
        where: { email },
        data: { name },
      });
    }
    throw error;
  }
}
```

### Graceful Degradation

```typescript
async function transferFunds(fromId: number, toId: number, amount: number) {
  try {
    return await prisma.$transaction(
      async (tx) => {
        const from = await tx.account.update({
          where: { id: fromId },
          data: { balance: { decrement: amount } },
        });

        if (from.balance < 0) {
          throw new Error('Insufficient funds');
        }

        await tx.account.update({
          where: { id: toId },
          data: { balance: { increment: amount } },
        });

        return { success: true };
      },
      {
        isolationLevel: Prisma.TransactionIsolationLevel.Serializable,
        timeout: 5000,
      }
    );
  } catch (error) {
    if (error instanceof Error && error.message === 'Insufficient funds') {
      return { success: false, reason: 'insufficient_funds' };
    }

    if (
      error instanceof Prisma.PrismaClientKnownRequestError &&
      error.code === 'P2025'
    ) {
      return { success: false, reason: 'account_not_found' };
    }

    throw error;
  }
}
```

### Compensating Transactions

```typescript
async function createOrderWithInventory(
  productId: number,
  quantity: number,
  userId: number
) {
  let orderId: number | null = null;

  try {
    const result = await prisma.$transaction(async (tx) => {
      const product = await tx.product.update({
        where: { id: productId },
        data: { stock: { decrement: quantity } },
      });

      if (product.stock < 0) {
        throw new Error('Insufficient stock');
      }

      const order = await tx.order.create({
        data: {
          userId,
          productId,
          quantity,
          status: 'PENDING',
        },
      });

      orderId = order.id;

      return order;
    });

    return result;
  } catch (error) {
    if (orderId) {
      await prisma.order.update({
        where: { id: orderId },
        data: { status: 'FAILED' },
      });
    }

    throw error;
  }
}
```

## Isolation Level Error Handling

```typescript
try {
  await prisma.$transaction(
    async (tx) => {
      const balance = await tx.account.findUnique({
        where: { id: accountId },
      });

      await tx.account.update({
        where: { id: accountId },
        data: { balance: balance!.balance + amount },
      });
    },
    {
      isolationLevel: Prisma.TransactionIsolationLevel.Serializable,
    }
  );
} catch (error) {
  if (
    error instanceof Prisma.PrismaClientKnownRequestError &&
    error.code === 'P2034'
  ) {
    throw new Error('Serialization failure, transaction will be retried');
  }
  throw error;
}
```

## Common Patterns

### Validation Before Transaction

```typescript
async function createUserWithProfile(email: string, name: string) {
  const existing = await prisma.user.findUnique({
    where: { email },
  });

  if (existing) {
    throw new Error('User already exists');
  }

  try {
    return await prisma.$transaction(async (tx) => {
      const user = await tx.user.create({
        data: { email, name },
      });

      await tx.profile.create({
        data: { userId: user.id },
      });

      return user;
    });
  } catch (error) {
    if (
      error instanceof Prisma.PrismaClientKnownRequestError &&
      error.code === 'P2002'
    ) {
      throw new Error('User was created by another request');
    }
    throw error;
  }
}
```

### Nested Error Context

```typescript
class TransactionError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly context?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'TransactionError';
  }
}

async function complexTransaction(data: unknown) {
  try {
    return await prisma.$transaction(async (tx) => {
      const user = await tx.user.create({
        data: data as Prisma.UserCreateInput,
      });

      return user;
    });
  } catch (error) {
    if (error instanceof Prisma.PrismaClientKnownRequestError) {
      throw new TransactionError(
        'Transaction failed',
        error.code,
        { meta: error.meta, data }
      );
    }
    throw error;
  }
}
```

## Anti-Patterns

### DON'T: Ignore Error Types

```typescript
try {
  await prisma.$transaction(async (tx) => {
    await tx.user.create({ data: { email: 'test@example.com' } });
  });
} catch (error) {
  console.error('Error occurred');
}
```

### DO: Handle Specific Error Types

```typescript
try {
  await prisma.$transaction(async (tx) => {
    await tx.user.create({ data: { email: 'test@example.com' } });
  });
} catch (error) {
  if (error instanceof Prisma.PrismaClientKnownRequestError) {
    console.error(`Database error ${error.code}: ${error.message}`);
  } else {
    console.error('Unexpected error:', error);
  }
  throw error;
}
```

### DON'T: Use Default Timeouts for Long Operations

```typescript
await prisma.$transaction(async (tx) => {
  for (let i = 0; i < 10000; i++) {
    await tx.log.create({ data: { message: `Log ${i}` } });
  }
});
```

### DO: Configure Appropriate Timeouts

```typescript
await prisma.$transaction(
  async (tx) => {
    const logs = Array.from({ length: 10000 }, (_, i) => ({
      message: `Log ${i}`,
    }));

    await tx.log.createMany({ data: logs });
  },
  { timeout: 30000 }
);
```

## Related Skills

**TypeScript Error Handling:**

- If implementing runtime checks for error codes, use the using-runtime-checks skill from typescript for assertion and guard patterns
