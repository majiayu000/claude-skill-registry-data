---
name: cheshire-noxa
description: NOXA Fun/DEX collab for Cheshire Terminal — launch feed, DEX registry, QuoterV2 quotes, EVM RPC. One-shot npm package @x402solana/cheshire-noxa.
version: 0.1.0
tags:
  - noxa
  - uniswap-v3
  - dex
  - evm
  - cheshire
  - robinhood
homepage: https://cheshireterminal.ai/noxa
---

# cheshire-noxa

Install and register:

```bash
npm install @x402solana/cheshire-noxa
npx cheshire-noxa register
# or dry-run:
npx cheshire-noxa register --dry-run
```

## Surfaces

- `/api/noxa/status`
- `/api/noxa/dexes`
- `/api/noxa/integration`
- `/api/noxa/launches`
- `/api/noxa/pool`
- `/api/noxa/quote`
- `/api/evm/rpc`
- `/noxa`

## SDK

```ts
import { createCheshireNoxaClient, getPackageIdentity } from "@x402solana/cheshire-noxa";

const client = createCheshireNoxaClient({ origin: "https://cheshireterminal.ai" });
const ready = await client.checkReadiness();
console.log(ready.message);
```
