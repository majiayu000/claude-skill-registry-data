---
name: fuji-testnet-and-tools
description: Use when the agent needs Avalanche Fuji testnet connection details and dev tools — C-Chain RPC, chain ID, explorer, faucets, and the Builder Console for browser-based deploys.
category: Tooling
difficulty: Beginner
version: "0.1.0"
---

# Fuji Testnet & Developer Tools

## Overview
Fuji is Avalanche's primary testnet. Use it to deploy and exercise eERC tokens and L1s with free test AVAX before mainnet.

## Fuji C-Chain connection
- **RPC:** `https://api.avax-test.network/ext/bc/C/rpc`
- **Chain ID:** `43113`
- **Currency:** AVAX (test)
- **Explorer:** `https://testnet.snowtrace.io/`

## Faucets (free test AVAX)
- **Core faucet:** https://core.app/tools/testnet-faucet
- **QuickNode faucet:** https://faucet.quicknode.com/avalanche/fuji

Fund your deployer/test accounts here before deploying eERC ([[eerc-deploy-fuji]]) or an L1 on Fuji ([[create-avalanche-l1]]).

## Builder Console (no local setup)
https://build.avax.network/console — deploy from the browser:
- **Encrypted ERC → Deploy Your Own** — stand up an eERC token without Hardhat.
- **Create L1** — scaffold an L1 from the sidebar.
Great for demos and quick validation; use the CLI/Hardhat paths for reproducible infrastructure.

## Wallet setup snippet
```ts
// viem chain config for Fuji C-Chain
import { defineChain } from "viem";
export const fuji = defineChain({
  id: 43113,
  name: "Avalanche Fuji",
  nativeCurrency: { name: "Avalanche", symbol: "AVAX", decimals: 18 },
  rpcUrls: { default: { http: ["https://api.avax-test.network/ext/bc/C/rpc"] } },
  blockExplorers: { default: { name: "SnowTrace", url: "https://testnet.snowtrace.io" } },
  testnet: true,
});
```

## Common Pitfalls
- **Wrong chain ID.** Fuji C-Chain is `43113` (mainnet C-Chain is `43114`).
- **Empty faucet balance.** Faucets rate-limit; some require a small mainnet balance or social verification.
- **Custom L1 ≠ C-Chain.** Your own Fuji L1 has its own RPC/chain ID, not the C-Chain values above.

## AI Agent Prompt
> "Act as a dev-environment assistant. Configure my wallet/SDK for Fuji C-Chain (RPC, chain 43113, explorer), fund the deployer from a faucet, and point me to the Builder Console for a no-setup eERC deploy."

## References
See `references/README.md` (Fuji params, faucets, Builder Console).
