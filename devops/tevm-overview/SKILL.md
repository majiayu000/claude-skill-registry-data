---
name: tevm-overview
description: Lightweight EVM that runs in the browser. Use for local blockchain testing, contract debugging, and fork testing.
---

# Tevm Overview

Tevm is a lightweight EVM that runs in the browser for local testing and debugging.

## Quick Start

```typescript
import { createMemoryClient } from 'tevm'

const client = createMemoryClient()

// Execute a contract call
const result = await client.tevmCall({
  to: contractAddress,
  data: '0x...'
})
```

## Key Capabilities

- **In-memory EVM** - No external node required
- **Fork mode** - Fork from mainnet/testnet
- **EVM tracing** - Step-by-step execution debugging
- **Account impersonation** - Act as any address
- **Time manipulation** - Control block timestamps

## Skills

- **Setup**: `tevm-setup` - Client initialization
- **Actions**: `tevm-actions` - Core API (call, mine, etc.)
- **Account Management**: `tevm-account-management` - State manipulation
- **Events**: `tevm-events` - EVM execution tracing
- **Contract Deployment**: `tevm-contract-deployment` - Deploy with ethers
- **Debugging**: `tevm-debugging` - Gas profiling, tracing

## Use Cases

1. **Frontend testing** - Test contract interactions without mainnet
2. **Contract debugging** - Trace execution at opcode level
3. **Fork testing** - Fork mainnet state locally
4. **CI/CD** - Fast test execution
