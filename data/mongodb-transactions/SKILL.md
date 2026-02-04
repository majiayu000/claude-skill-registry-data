---
name: mongodb-transactions
version: "2.1.0"
description: Master MongoDB ACID transactions for multi-document operations. Learn session management, transaction mechanics, error handling, and production patterns. Guarantee data consistency across multiple operations.
sasmp_version: "1.3.0"
bonded_agent: 07-mongodb-application-development
bond_type: PRIMARY_BOND

# Production-Grade Skill Configuration
capabilities:
  - session-management
  - multi-document-transactions
  - retry-logic
  - error-recovery
  - consistency-guarantees

input_validation:
  required_context:
    - operations_list
    - consistency_requirement
  optional_context:
    - read_concern
    - write_concern
    - timeout_ms

output_format:
  transaction_code: string
  session_handling: string
  error_handling: string
  retry_logic: string
  rollback_procedure: string

error_handling:
  common_errors:
    - code: TXN001
      condition: "TransientTransactionError"
      recovery: "Retry entire transaction with exponential backoff"
    - code: TXN002
      condition: "UnknownTransactionCommitResult"
      recovery: "Check operation idempotency, verify state before retry"
    - code: TXN003
      condition: "Transaction timeout"
      recovery: "Increase maxTransactionLockRequestTimeoutMillis or optimize operations"

prerequisites:
  mongodb_version: "4.0+ (replica set), 4.2+ (sharded)"
  required_knowledge:
    - crud-operations
    - session-basics
  deployment_requirements:
    - "Replica set or sharded cluster"
    - "Not available on standalone or M0 Atlas"

testing:
  unit_test_template: |
    // Test transaction with rollback
    const session = client.startSession()
    try {
      await session.withTransaction(async () => {
        await collection1.insertOne(doc1, { session })
        await collection2.insertOne(doc2, { session })
      })
      // Verify both inserted
    } catch (error) {
      // Verify neither inserted (rollback)
    } finally {
      await session.endSession()
    }
---

# MongoDB Multi-Document Transactions

Guarantee consistency with ACID transactions across multiple operations.

## Quick Start

### Basic Transaction
```javascript
const session = client.startSession()

try {
  await session.withTransaction(async () => {
    // All operations here are atomic
    await users.insertOne({ name: 'John' }, { session })
    await accounts.insertOne({ userId: 'xxx', balance: 100 }, { session })

    // If any fails, ALL roll back
  })
} catch (error) {
  console.error('Transaction failed:', error)
} finally {
  await session.endSession()
}
```

### Real-World: Money Transfer
```javascript
async function transferMoney(fromId, toId, amount) {
  const session = client.startSession()

  try {
    await session.withTransaction(async () => {
      // Deduct from account A
      await accounts.updateOne(
        { _id: fromId },
        { $inc: { balance: -amount } },
        { session }
      )

      // Add to account B
      await accounts.updateOne(
        { _id: toId },
        { $inc: { balance: amount } },
        { session }
      )

      // Both succeed, or both rollback - NO PARTIAL TRANSFERS!
    })
  } catch (error) {
    // Transaction failed, money not transferred
    console.error('Transfer failed:', error)
  } finally {
    await session.endSession()
  }
}
```

## Transaction Requirements

### MongoDB Version
- **MongoDB 4.0+**: Single-document transactions (all versions)
- **MongoDB 4.0**: Multi-document transactions (replica sets)
- **MongoDB 4.2+**: Multi-document transactions (sharded clusters)

### Deployment Type
- **Replica Set**: Required for transactions
- **Sharded Cluster**: MongoDB 4.2+
- **Standalone**: Single-document transactions only
- **Atlas Free**: No transactions (shared clusters)

## Session Management

### Create Session
```javascript
const session = client.startSession()

// Configure session
const session = client.startSession({
  defaultTransactionOptions: {
    readConcern: { level: 'snapshot' },
    writeConcern: { w: 'majority' },
    readPreference: 'primary'
  }
})
```

### Session Lifecycle
```javascript
// 1. Start session
const session = client.startSession()

// 2. Start transaction
session.startTransaction()

// 3. Execute operations with session
await collection.insertOne(doc, { session })

// 4. Commit or abort
await session.commitTransaction()  // Success
await session.abortTransaction()   // Rollback

// 5. End session
await session.endSession()
```

## Transaction Options

### Read Concern
```javascript
// snapshot: See committed data at transaction start
// local: See latest data (default)
// majority: See data confirmed on majority
// linearizable: Latest confirmed data

await session.withTransaction(async () => {
  // Operations
}, {
  readConcern: { level: 'snapshot' }
})
```

### Write Concern
```javascript
// w: 1 (default): Acknowledged by primary
// w: 'majority': Acknowledged by majority
// w: N: Acknowledged by N replicas

await session.withTransaction(async () => {
  // Operations
}, {
  writeConcern: { w: 'majority' }
})
```

### Read Preference
```javascript
// primary: Read from primary only
// primaryPreferred: Primary, fallback to secondary
// secondary: Read from secondary
// secondaryPreferred: Secondary, fallback to primary
// nearest: Nearest server

{
  readPreference: 'primary'
}
```

## Error Handling

### Handle Transaction Errors
```javascript
async function robustTransaction() {
  const session = client.startSession()

  try {
    await session.withTransaction(async () => {
      // Operations
    })
  } catch (error) {
    if (error.hasErrorLabel('TransientTransactionError')) {
      // Temporary error - retry
      return robustTransaction()
    } else if (error.hasErrorLabel('UnknownTransactionCommitResult')) {
      // Commit outcome unknown - check state
      console.log('Commit outcome unknown')
    } else {
      // Fatal error
      throw error
    }
  } finally {
    await session.endSession()
  }
}
```

### Retry Logic
```javascript
async function executeWithRetry(fn, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    const session = client.startSession()

    try {
      await session.withTransaction(async () => {
        await fn(session)
      })
      return  // Success
    } catch (error) {
      if (error.hasErrorLabel('TransientTransactionError') && attempt < maxRetries) {
        continue  // Retry
      } else {
        throw error
      }
    } finally {
      await session.endSession()
    }
  }
}
```

## Real-World Examples

### Order Placement with Inventory
```javascript
async function placeOrder(userId, items) {
  const session = client.startSession()

  try {
    await session.withTransaction(async () => {
      // 1. Create order
      const order = {
        userId,
        items,
        status: 'pending',
        createdAt: new Date()
      }
      const orderResult = await orders.insertOne(order, { session })

      // 2. Update inventory
      for (const item of items) {
        const updated = await products.findOneAndUpdate(
          { _id: item.productId },
          { $inc: { stock: -item.quantity } },
          { session, returnDocument: 'after' }
        )

        // Check if stock went negative
        if (updated.value.stock < 0) {
          throw new Error('Insufficient inventory')
        }
      }

      // 3. Deduct from user account
      const userUpdate = await users.findOneAndUpdate(
        { _id: userId },
        { $inc: { balance: -calculateTotal(items) } },
        { session, returnDocument: 'after' }
      )

      if (userUpdate.value.balance < 0) {
        throw new Error('Insufficient funds')
      }

      return orderResult.insertedId
    })
  } catch (error) {
    // ALL operations rolled back if any fails
    // Inventory stays same
    // User balance unchanged
    // Order not created
    console.error('Order failed:', error.message)
    throw error
  } finally {
    await session.endSession()
  }
}
```

### Account Reconciliation
```javascript
async function reconcileAccounts(mainId, secondaryIds) {
  const session = client.startSession()

  try {
    await session.withTransaction(async () => {
      // Calculate total balance
      const secondary = await accounts.find(
        { _id: { $in: secondaryIds } },
        { session }
      ).toArray()
      const totalBalance = secondary.reduce((sum, acc) => sum + acc.balance, 0)

      // Update main account
      await accounts.updateOne(
        { _id: mainId },
        { $set: { balance: totalBalance } },
        { session }
      )

      // Delete secondary accounts
      await accounts.deleteMany(
        { _id: { $in: secondaryIds } },
        { session }
      )

      // Log reconciliation
      await reconciliationLog.insertOne({
        mainId,
        secondaryIds,
        totalBalance,
        timestamp: new Date()
      }, { session })

      // All succeed together, or all rollback
    })
  } finally {
    await session.endSession()
  }
}
```

## Limitations & Considerations

### Transaction Limits
```
- Maximum 16MB of write operations
- Cannot create/drop collections
- Cannot create/drop indexes
- Cannot alter collections
- Cannot write to system collections
```

### Performance Impact
```
- Transactions have overhead
- Write operations slower (more coordination)
- Locking increases lock contention
- Not for every operation
```

## Best Practices

✅ **Transaction Best Practices:**
1. **Keep short** - Minimize lock time
2. **Retry transient errors** - Network issues happen
3. **Order operations** - Prevent deadlocks
4. **Use appropriate write concern** - 'majority' for safety
5. **Monitor latency** - Transactions add overhead

✅ **When to Use:**
1. ✅ Money transfers
2. ✅ Order processing
3. ✅ Inventory management
4. ✅ Account operations
5. ✅ Any multi-collection atomic operations

❌ **When NOT to Use:**
1. ❌ Single document operations (inherently atomic)
2. ❌ Simple inserts/updates
3. ❌ Performance-critical reads
4. ❌ Batch operations (use bulk)
5. ❌ If not on replica set

## Next Steps

1. **Learn session basics** - StartSession, endSession
2. **Write simple transaction** - Insert and update
3. **Add error handling** - Try-catch blocks
4. **Implement retry logic** - Handle transient errors
5. **Monitor performance** - Measure transaction time

---

**Guarantee consistency with transactions!** ✅
