---
name: polkadot-api-patterns
description: Essential patterns for polkadot-api (PAPI) development. Use when implementing blockchain interactions with Polkadot/Substrate chains including transactions (signing, batching, watching), queries (storage, multi-key), observables (lifecycle tracking), type handling (MultiAddress, Binary), client setup, or debugging PAPI code. Critical for preventing the common mistake of using @polkadot/api (PJS) instead of polkadot-api (PAPI). Load whenever user mentions polkadot-api, blockchain transactions, pallet calls, or needs to fix PAPI-related type errors.
---

# polkadot-api Patterns

Essential patterns for developing with `polkadot-api` (PAPI).

## Critical Rule: Package Imports

**NEVER use `@polkadot/api` (PJS) - ONLY use `polkadot-api` (PAPI).**

### Correct Imports

```typescript
// Core PAPI
import { Binary, createClient, type Transaction, type TypedApi } from 'polkadot-api'

// WebSocket
import { getWsProvider } from 'polkadot-api/ws-provider'

// Descriptors (generated)
import { MultiAddress, type qfn } from '@polkadot-api/descriptors'

// Utils
import { type PolkadotSigner } from '@polkadot-api/utils'
```

### Forbidden Imports

```typescript
// ❌ NEVER import these
import { ApiPromise } from '@polkadot/api'
import { WsProvider } from '@polkadot/rpc-provider'
```

**Why:** PJS and PAPI are different, incompatible libraries. PJS is maintenance mode, PAPI is the future.

## Client Setup

Create client once, reuse TypedApi:

```typescript
import { createClient } from 'polkadot-api'
import { getWsProvider } from 'polkadot-api/ws-provider'
import { qfn as chain } from '@polkadot-api/descriptors'

// Provider
const provider = getWsProvider('wss://test.qfnetwork.xyz')

// Client (connection manager)
const client = createClient(provider)

// TypedApi (typed interface)
const api = client.getTypedApi(chain)

// Type for signatures
type QfnApi = TypedApi<typeof qfn>
```

Access: `api.tx.*` `api.query.*` `api.constants.*`

## Type Wrappers

### MultiAddress.Id() for Addresses

```typescript
import { MultiAddress } from '@polkadot-api/descriptors'

// ✅ Always wrap addresses
const tx = api.tx.Assets.transfer({
  id: assetId,
  target: MultiAddress.Id(recipientAddress),
  amount: 1000n
})

// ❌ Raw strings fail
target: recipientAddress  // Type error!
```

### Binary.fromText() for Strings

```typescript
import { Binary } from 'polkadot-api'

// ✅ Wrap strings for chain
const tx = api.tx.Assets.set_metadata({
  id: assetId,
  name: Binary.fromText("Token Name"),
  symbol: Binary.fromText("SYMB"),
  decimals: 12
})

// ❌ Raw strings fail
name: "Token Name"  // Type error!
```

## Transaction Patterns

### Basic Transaction

```typescript
// Build
const tx = api.tx.Balances.transfer_keep_alive({
  dest: MultiAddress.Id(recipientAddress),
  value: 1_000_000_000_000n
})

// Execute
const observable = tx.signSubmitAndWatch(polkadotSigner)
```

### Batch Transactions

All-or-nothing atomicity with `Utility.batch_all`:

```typescript
import { Binary, type TxCallData } from 'polkadot-api'

// Build calls
const createCall = api.tx.Assets.create({
  id: assetId,
  admin: MultiAddress.Id(signerAddress),
  min_balance: minBalance
}).decodedCall  // ← Key: use .decodedCall

const metadataCall = api.tx.Assets.set_metadata({
  id: assetId,
  name: Binary.fromText("Token"),
  symbol: Binary.fromText("TKN"),
  decimals: 12
}).decodedCall

// Batch
const calls: TxCallData[] = [createCall, metadataCall]
const batchTx = api.tx.Utility.batch_all({ calls })
```

**Pattern:** Individual tx → `.decodedCall` → Array → `Utility.batch_all({ calls })`

### Observable Lifecycle

```typescript
import type { TxBroadcastEvent } from 'polkadot-api'

observable.subscribe({
  next: (event: TxBroadcastEvent) => {
    if (event.type === 'broadcasted') {
      console.log('Broadcasted')
    }
    if (event.type === 'txBestBlocksState' && event.found) {
      console.log('In block')
    }
    if (event.type === 'finalized') {
      console.log('Finalized:', event.block.hash)
    }
  },
  error: (err) => console.error('Transaction error:', err),
  complete: () => console.log('Complete')
})
```

Events: `broadcasted` → `txBestBlocksState` → `finalized`

## Query Patterns

### Single Value

```typescript
// Current value
const balance = await api.query.System.Account.getValue(address)

// At block
const balanceAt = await api.query.System.Account.getValue(address, { at: blockHash })
```

### Multiple Entries

```typescript
// All entries
const assets = await api.query.Assets.Asset.getEntries()

assets.forEach(({ keyArgs, value }) => {
  const [assetId] = keyArgs
  console.log(`Asset ${assetId}:`, value)
})

// With pagination
const page = await api.query.Assets.Asset.getEntries({ at: 'best', pageSize: 100 })
```

### Multi-key Query

```typescript
// Multiple keys at once
const addresses = [addr1, addr2, addr3]
const balances = await api.query.System.Account.getValues(addresses)
```

### Watch Changes

```typescript
// Subscribe to updates
const unsubscribe = api.query.System.Account.watchValue(
  address,
  (accountInfo) => console.log('Balance:', accountInfo.data.free)
)

// Clean up
unsubscribe()
```

## Constants

```typescript
// Access chain constants
const existentialDeposit = api.constants.Balances.ExistentialDeposit()
const maxAssets = api.constants.Assets.MaxAssets()
```

## Error Handling

See `references/error-handling.md` for complete error handling patterns:
- Observable errors (before finalization)
- Pallet errors (runtime errors)
- Query errors
- Connection errors
- User-friendly error messages

## Common Mistakes

### Missing Type Wrappers

```typescript
// ❌ Wrong
api.tx.Assets.transfer({
  target: recipientAddress,  // Missing MultiAddress.Id()
})

// ✅ Correct
api.tx.Assets.transfer({
  target: MultiAddress.Id(recipientAddress),
})
```

### Not Using .decodedCall for Batches

```typescript
// ❌ Wrong - missing .decodedCall
const calls = [
  api.tx.Assets.create({ ... }),
]

// ✅ Correct - use .decodedCall
const calls: TxCallData[] = [
  api.tx.Assets.create({ ... }).decodedCall,
]
```

### Using PJS Instead of PAPI

```typescript
// ❌ Wrong - @polkadot/api
import { ApiPromise } from '@polkadot/api'

// ✅ Correct - polkadot-api
import { createClient } from 'polkadot-api'
```

### Raw Strings Without Binary.fromText

```typescript
// ❌ Wrong - raw string
api.tx.Assets.set_metadata({
  name: "Token",  // Type error
})

// ✅ Correct - wrapped
api.tx.Assets.set_metadata({
  name: Binary.fromText("Token"),
})
```

## Integration with Template

If using a template with ConnectionContext:

```typescript
import { useConnectionContext } from '@/hooks'

const { api, client, isConnected } = useConnectionContext()
// api is TypedApi, ready to use
```

Transaction management:

```typescript
import { useTransaction } from '@/hooks'

const { executeTransaction } = useTransaction(toastConfig)
await executeTransaction('key', observable, params)
```

## Validation

After implementing PAPI code:

```bash
# Check for forbidden imports
grep -r "@polkadot/api" src/
# Should return ZERO results

# Type check
tsc --noEmit

# Verify descriptors exist
ls .papi/descriptors/
```

## Reference Links

- **polkadot-api docs:** https://papi.how
- **Generate descriptors:** Run `papi` or `pnpm papi`
- **TypeScript:** Let types guide you - they prevent runtime errors
