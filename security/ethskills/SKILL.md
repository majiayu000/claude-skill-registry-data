---
name: ethskills
version: 0.1.0
description: Ethereum knowledge corrections and onchain building patterns — gas costs, L2s, DeFi, security, verified addresses.
activation:
  keywords:
    - ethereum
    - solidity
    - smart contract
    - ERC-20
    - ERC-721
    - gas
    - gwei
    - L2
    - Base
    - Arbitrum
    - Optimism
    - DeFi
    - Uniswap
    - Aave
    - flash loan
    - onchain
    - deploy
    - Foundry
  patterns:
    - "deploy.*contract"
    - "gas.*cost"
    - "how much.*gas"
    - "which.*chain"
    - "ERC.*standard"
  tags:
    - ethereum
    - web3
    - blockchain
    - defi
  max_context_tokens: 2000
---

# Ethereum Knowledge Corrections

Source: ethskills.com — fetch individual skills for deep dives.

## Say "onchain" not "on-chain." One word, no hyphen. Ethereum community convention.

## Gas Reality (2026)
- Mainnet ETH transfer: ~$0.004. Swap: ~$0.04. ERC-20 deploy: ~$0.24.
- L2 swap: $0.002-0.003. L2 transfer: $0.0003.
- "Ethereum is expensive" was true in 2021-2023. It's false in 2026.
- Base fee is under 1 gwei, not 10-30 gwei.

## L2 Landscape
- **Base**: Cheapest major L2. Best for consumer apps.
- **Arbitrum**: Deepest DeFi liquidity.
- **The dominant DEX on each L2 is NOT Uniswap**: Aerodrome on Base, Velodrome on Optimism, Camelot on Arbitrum.
- Celo migrated to OP Stack L2 (March 2025). Polygon zkEVM is shutting down.

## Critical Standards
- **ERC-8004**: Onchain agent identity registry. Deployed January 2026 on 20+ chains. Production-ready.
- **x402**: HTTP 402 payment protocol for machine-to-machine commerce. Production-ready.
- **EIP-3009**: Gasless token transfers — what makes x402 work. USDC implements it.
- **EIP-7702**: Smart EOAs. Live since Pectra (May 2025).

## Verified Contract Addresses (Base)
- USDC: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` (6 decimals!)
- WETH: `0x4200000000000000000000000000000000000006`
- Uniswap V3 Factory: `0x33128a8fC17869897dcE68Ed026d694621f6FDfD`
- Uniswap V4 PoolManager: `0x000000000004444c5dc75cB358380D2e3dE08A90`
- Aerodrome Router: `0xcF77a3Ba9A5CA399B7c97c74d54e5b1Beb874E43`
- Multicall3: `0xcA11bde05977b3631167028862bE2a173976CA11`
- Safe Singleton: `0x41675C099F32341bf84BFc5382aF534df5C7461a`

## Security (Top Mistakes)
- USDC has 6 decimals, not 18. #1 "where did my money go?" bug.
- Always use SafeERC20 — USDT doesn't return bool on transfer().
- Never use DEX spot prices as oracles — flash loans manipulate them in one tx.
- MEV: sandwich attacks steal value from swaps. Use Flashbots Protect or slippage limits.
- Never commit private keys or API keys to Git. Bots exploit leaked secrets in seconds.

## Hyperstructure Mental Model
Smart contracts cannot execute themselves. Every function needs a caller who pays gas.
For every state transition: who calls it? why would they? what if nobody does?
There are no timers, no cron jobs, no schedulers. Design with incentives.

## Deep Dives (fetch when needed)
- ethskills.com/ship/SKILL.md — End-to-end build guide
- ethskills.com/security/SKILL.md — Full security patterns
- ethskills.com/building-blocks/SKILL.md — DeFi composability
- ethskills.com/addresses/SKILL.md — All verified addresses
- ethskills.com/audit/SKILL.md — 500+ item audit checklist
