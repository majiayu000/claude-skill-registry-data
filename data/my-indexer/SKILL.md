---
name: HyperIndex Development
description: This skill should be used when the user asks to "create an indexer", "build a hyperindex", "index blockchain events", "write event handlers", "configure config.yaml", "define schema.graphql", "use envio", "set up hyperindex", "index smart contract events", "create graphql schema for blockchain data", or mentions Envio, HyperIndex, blockchain indexing, or event handler development.
version: 1.0.0
---

# HyperIndex Development

HyperIndex is Envio's blazing-fast, developer-friendly multichain blockchain indexer. It transforms on-chain events into structured, queryable databases with GraphQL APIs.

## Quick Start

Initialize a new indexer:

```bash
pnpx envio init
```

Run locally:

```bash
pnpm dev
```

## Essential Files

Every HyperIndex project contains three core files:

1. **`config.yaml`** - Defines networks, contracts, events to index
2. **`schema.graphql`** - Defines GraphQL entities for indexed data
3. **`src/EventHandlers.ts`** - Contains event processing logic

After changes to `config.yaml` or `schema.graphql`, run:

```bash
pnpm codegen
```

## Development Environment

**Requirements:**
- Node.js v20+ (v22 recommended)
- pnpm v8+
- Docker Desktop (for local development)

**Key commands:**
- `pnpm codegen` - Generate types after config/schema changes
- `pnpm tsc --noEmit` - Type-check TypeScript
- `TUI_OFF=true pnpm dev` - Run indexer with visible output

## Configuration (config.yaml)

Basic structure:

```yaml
# yaml-language-server: $schema=./node_modules/envio/evm.schema.json
name: my-indexer
networks:
  - id: 1  # Ethereum mainnet
    start_block: 0  # HyperSync is fast - start from genesis
    contracts:
      - name: MyContract
        address: 0xContractAddress
        handler: src/EventHandlers.ts
        events:
          - event: Transfer(address indexed from, address indexed to, uint256 value)
```

**Key options:**
- `address` - Single or array of addresses
- `start_block` - Block to begin indexing. **Use `0` with HyperSync** (default) - it's extremely fast and syncs millions of blocks in minutes. Only specify a later block if using RPC on unsupported networks.
- `handler` - Path to event handler file
- `events` - Event signatures to index

**For transaction/block data access**, use `field_selection`. By default, `event.transaction` is `{}` (empty).

**Per-event (recommended)** - Only fetch extra fields for events that need them. More fields = more data transfer = slower indexing:

```yaml
events:
  - event: Transfer(address indexed from, address indexed to, uint256 value)
    field_selection:
      transaction_fields:
        - hash
  - event: Approval(address indexed owner, address indexed spender, uint256 value)
    # No field_selection - this event doesn't need transaction data
```

**Global** - Applies to ALL events. Use only when most/all events need the same fields:

```yaml
field_selection:
  transaction_fields:
    - hash
```

**Available fields:**
- `transaction_fields`: `hash`, `from`, `to`, `value`, `gasPrice`, `gas`, `input`, `nonce`, `transactionIndex`, `gasUsed`, `status`, etc.
- `block_fields`: `miner`, `gasLimit`, `gasUsed`, `baseFeePerGas`, `size`, `difficulty`, etc.

**For dynamic contracts** (factory pattern), omit address and use contractRegister.

## Schema (schema.graphql)

Define entities without `@entity` decorator:

```graphql
type Token {
  id: ID!
  name: String!
  symbol: String!
  decimals: BigInt!
  totalSupply: BigInt!
}

type Transfer {
  id: ID!
  from: String!
  to: String!
  amount: BigInt!
  token_id: String!  # Relationship via _id suffix
  blockNumber: BigInt!
  timestamp: BigInt!
}
```

**Key rules:**
- Use `String!` instead of `Bytes!`
- Use `_id` suffix for relationships (e.g., `token_id` not `token`)
- Entity arrays require `@derivedFrom`: `transfers: [Transfer!]! @derivedFrom(field: "token")`
- No `@entity` decorators needed

## Event Handlers

Basic handler pattern:

```typescript
import { MyContract } from "generated";

MyContract.Transfer.handler(async ({ event, context }) => {
  const entity = {
    id: `${event.chainId}-${event.transaction.hash}-${event.logIndex}`,
    from: event.params.from,
    to: event.params.to,
    amount: event.params.amount,
    blockNumber: BigInt(event.block.number),
    timestamp: BigInt(event.block.timestamp),
  };

  context.Transfer.set(entity);
});
```

**Entity updates** - Use spread operator (entities are immutable):

```typescript
const existing = await context.Token.get(tokenId);
if (existing) {
  context.Token.set({
    ...existing,
    totalSupply: newSupply,
  });
}
```

**Dynamic contract registration** (factory pattern):

```typescript
Factory.PairCreated.contractRegister(({ event, context }) => {
  context.addPair(event.params.pair);
});

Factory.PairCreated.handler(async ({ event, context }) => {
  // Handle the event...
});
```

## Effect API for External Calls

When using `preload_handlers: true`, external calls MUST use the Effect API:

```typescript
import { S, createEffect } from "envio";

export const getTokenMetadata = createEffect({
  name: "getTokenMetadata",
  input: S.string,
  output: S.object({
    name: S.string,
    symbol: S.string,
    decimals: S.number,
  }),
  cache: true,
}, async ({ input: address }) => {
  // Fetch token metadata via RPC
  return { name: "Token", symbol: "TKN", decimals: 18 };
});

// In handler:
MyContract.Event.handler(async ({ event, context }) => {
  const metadata = await context.effect(getTokenMetadata, event.params.token);
});
```

## Common Patterns

**Multichain IDs** - Prefix with chainId:
```typescript
const id = `${event.chainId}-${event.params.tokenId}`;
```

**Timestamps** - Always cast to BigInt:
```typescript
timestamp: BigInt(event.block.timestamp)
```

**Address consistency** - Use lowercase:
```typescript
const address = event.params.token.toLowerCase();
```

**BigDecimal precision** - Import from generated:
```typescript
import { BigDecimal } from "generated";
const ZERO_BD = new BigDecimal(0);
```

## Logging & Debugging

**Logging in handlers:**
```typescript
context.log.debug("Detailed info");
context.log.info("Processing transfer", { from, to, value });
context.log.warn("Large transfer detected");
context.log.error("Failed to process", { error, txHash });
```

**Run with visible output:**
```bash
TUI_OFF=true pnpm dev
```

**Log levels via env vars:**
```bash
LOG_LEVEL="debug"     # Show debug logs (default: "info")
LOG_LEVEL="trace"     # Most verbose
```

**Common issues checklist:**
- Missing `await` on `context.Entity.get()`
- Wrong field names (check generated types)
- Missing `field_selection` for transaction data
- Logs not appearing? They're skipped during preload phase

See `references/logging-debugging.md` for structured logging, log strategies, and troubleshooting patterns.

## Block Handlers

Index data on every block (or interval) without specific events:

```typescript
import { Ethereum } from "generated";

Ethereum.onBlock(
  async ({ block, context }) => {
    context.BlockStats.set({
      id: `${block.number}`,
      number: BigInt(block.number),
      timestamp: BigInt(block.timestamp),
      gasUsed: block.gasUsed,
    });
  },
  { interval: 100 }  // Every 100 blocks
);
```

See `references/block-handlers.md` for intervals, multichain, and preset handlers.

## Multichain Indexing

Index the same contract across multiple chains:

```yaml
networks:
  - id: 1       # Ethereum
    start_block: 0
    contracts:
      - name: MyToken
        address: 0x...
  - id: 137     # Polygon
    start_block: 0
    contracts:
      - name: MyToken
        address: 0x...
```

**Important:** Use chain-prefixed IDs to prevent collisions:
```typescript
const id = `${event.chainId}_${event.params.tokenId}`;
```

See `references/multichain-indexing.md` for ordered vs unordered mode.

## Wildcard Indexing

Index events across all contracts (no address specified):

```typescript
ERC20.Transfer.handler(
  async ({ event, context }) => {
    context.Transfer.set({
      id: `${event.chainId}_${event.block.number}_${event.logIndex}`,
      token: event.srcAddress,  // The actual contract
      from: event.params.from,
      to: event.params.to,
    });
  },
  { wildcard: true }
);
```

See `references/wildcard-indexing.md` for topic filtering.

## Testing

Unit test handlers with MockDb:

```typescript
import { TestHelpers } from "generated";
const { MockDb, MyContract, Addresses } = TestHelpers;

it("creates entity on event", async () => {
  const mockDb = MockDb.createMockDb();
  const event = MyContract.Transfer.createMockEvent({
    from: Addresses.defaultAddress,
    to: "0x456...",
    value: BigInt(1000),
  });

  const updatedDb = await mockDb.processEvents([event]);
  const transfer = updatedDb.entities.Transfer.get("...");
  assert.ok(transfer);
});
```

See `references/testing.md` for complete patterns.

## Querying Data Locally

When running `pnpm dev`, query indexed data via GraphQL at `http://localhost:8080/v1/graphql`.

**Check indexing progress first** (always do this before assuming data is missing):

```bash
curl -s http://localhost:8080/v1/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ _meta { chainId startBlock progressBlock sourceBlock eventsProcessed isReady } }"}'
```

- `progressBlock` - Current processed block
- `sourceBlock` - Latest block on chain (target)
- `isReady` - `true` when fully synced

**Query entities:**

```bash
curl -s http://localhost:8080/v1/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ Transfer(limit: 10, order_by: {blockNumber: desc}) { id chainId from to amount blockNumber } }"}'
```

**Filter by chain (multichain):**

```bash
curl -s http://localhost:8080/v1/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ Transfer(where: {chainId: {_eq: 42161}}, limit: 10) { id from to amount } }"}'
```

**Common filter operators:** `_eq`, `_neq`, `_gt`, `_gte`, `_lt`, `_lte`, `_in`, `_like`

**Tip:** BigInt values must be quoted strings in filters: `{amount: {_gt: "1000000000000000000"}}`

See `references/local-querying.md` for comprehensive query patterns, pagination, and debugging tips.

## Database Indexes

Optimize query performance with `@index`:

```graphql
type Transfer {
  id: ID!
  from: String! @index
  to: String! @index
  timestamp: BigInt! @index
}

type Swap @index(fields: ["pair", "timestamp"]) {
  id: ID!
  pair_id: String! @index
  timestamp: BigInt!
}
```

See `references/database-indexes.md` for optimization tips.

## Preload Optimization

> **Important:** Handlers run TWICE when `preload_handlers: true` (default since v2.27).

This flagship feature reduces database roundtrips from thousands to single digits:

```typescript
// Phase 1 (Preload): All handlers run concurrently, reads are batched
// Phase 2 (Execution): Handlers run sequentially, reads come from cache
MyContract.Event.handler(async ({ event, context }) => {
  // Use Promise.all for concurrent reads
  const [sender, receiver] = await Promise.all([
    context.Account.get(event.params.from),
    context.Account.get(event.params.to),
  ]);

  // Skip non-essential logic during preload
  if (context.isPreload) return;

  // Actual processing (only runs in execution phase)
  context.Transfer.set({ ... });
});
```

**Critical rule:** Never call `fetch()` or external APIs directly. Use the Effect API.

See `references/preload-optimization.md` for the full mental model and best practices.

## Production Deployment

Deploy to Envio's hosted service for production-ready infrastructure:

```yaml
# Production config
name: my-indexer
rollback_on_reorg: true  # Always enable for production
networks:
  - id: 1
    start_block: 18000000
    confirmed_block_threshold: 250  # Reorg protection
```

**Pre-deployment checklist:**
1. `pnpm codegen` - Generate types
2. `pnpm tsc --noEmit` - Type check
3. `TUI_OFF=true pnpm dev` - Test locally with visible logs
4. Push to GitHub → Auto-deploy via Envio Hosted Service

See `references/deployment.md` for hosted service setup and `references/reorg-support.md` for chain reorganization handling.

## Additional Resources

### Reference Files

For detailed patterns and advanced techniques, consult:

**Core Concepts:**
- **`references/config-options.md`** - Complete config.yaml options
- **`references/effect-api.md`** - External calls and RPC patterns
- **`references/entity-patterns.md`** - Entity relationships and updates
- **`references/preload-optimization.md`** - How preload works, common footguns

**Advanced Features:**
- **`references/block-handlers.md`** - Block-level indexing with intervals
- **`references/multichain-indexing.md`** - Ordered vs unordered mode
- **`references/wildcard-indexing.md`** - Topic filtering, dynamic contracts
- **`references/contract-state.md`** - Read on-chain state via RPC/viem
- **`references/rpc-data-source.md`** - RPC config and fallback

**Operations:**
- **`references/logging-debugging.md`** - Logging, TUI, troubleshooting
- **`references/graphql-querying.md`** - Query indexed data, check progress, debug
- **`references/database-indexes.md`** - Index optimization
- **`references/testing.md`** - MockDb and test patterns

**Production:**
- **`references/deployment.md`** - Hosted service deployment
- **`references/reorg-support.md`** - Chain reorganization handling

### Example Files

Working examples in `examples/`:
- **`examples/basic-handler.ts`** - Simple event handler
- **`examples/factory-pattern.ts`** - Dynamic contract registration

### External Documentation

- Full docs: https://docs.envio.dev/docs/HyperIndex-LLM/hyperindex-complete
- Example indexers:
  - Uniswap v4: https://github.com/enviodev/uniswap-v4-indexer
  - Safe: https://github.com/enviodev/safe-analysis-indexer
