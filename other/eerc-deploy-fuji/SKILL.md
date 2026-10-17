---
name: eerc-deploy-fuji
description: Use when the agent needs to deploy and test eERC on the Avalanche Fuji testnet — Hardhat network config, RPC/chain ID, funding from the faucet, and the converter/standalone script flow on Fuji.
category: eERC
difficulty: Intermediate
version: "0.1.0"
---

# eERC — Deploy & Test on Fuji

## Overview
Fuji is Avalanche's testnet. Deploy eERC there exactly like locally ([[eerc-deploy-contracts]]) but point Hardhat at the Fuji C-Chain RPC and fund the deployer from the faucet.

## Fuji C-Chain parameters
- **RPC**: `https://api.avax-test.network/ext/bc/C/rpc`
- **Chain ID**: `43113`
- **Explorer**: `https://testnet.snowtrace.io/`
- **Faucet**: https://core.app/tools/testnet-faucet (alt: https://faucet.quicknode.com/avalanche/fuji)

## Hardhat config
```ts
// hardhat.config.ts
networks: {
  fuji: {
    url: process.env.RPC_URL ?? "https://api.avax-test.network/ext/bc/C/rpc",
    chainId: 43113,
    accounts: [process.env.PRIVATE_KEY!],
  },
},
```
`.env`:
```
RPC_URL=https://api.avax-test.network/ext/bc/C/rpc
PRIVATE_KEY=0x...
PRIVATE_KEY_2=0x...   # second user for transfer testing
```

## Deploy
```sh
# build circuits + verifiers first
npx hardhat compile && npx hardhat zkit make --force && npx hardhat zkit verifiers
# deploy (set isProd=true in the script for testnet/mainnet verifiers)
npx hardhat run scripts/deploy-standalone.ts --network fuji
# or: scripts/deploy-converter.ts
```
Save the printed `encryptedERC` and `registrar` addresses for the frontend ([[eerc-sdk-setup]]).

## End-to-end test on Fuji (converter example)
A typical flow (mirrors the academy course): init → deploy core → **register** two users → **set auditor** → **fund** from faucet → **deposit** → **transfer** → **withdraw**, checking balances between steps. Use two private keys so you can test confidential transfers between accounts.

## Browser alternative (no local setup)
The **Builder Console** can deploy an eERC token from the browser: https://build.avax.network/console → "Encrypted ERC > Deploy Your Own". Good for demos; use the Hardhat path for repeatable infra.

## Common Pitfalls
- **Unfunded deployer.** Get Fuji AVAX from the faucet before deploying.
- **Test verifiers.** Set `isProd=true` so proper trusted-setup verifiers are used even on testnet.
- **Wrong chain ID.** Must be `43113` for Fuji C-Chain.

## AI Agent Prompt
> "Act as a deployment engineer. Configure Hardhat for Fuji (chain 43113), fund the deployer from the faucet, build circuits, deploy eERC with production verifiers, and run a two-account register → deposit → transfer → withdraw test."

## References
See `references/README.md` (Fuji params, academy contracts-flow backend deployment, Builder Console).
