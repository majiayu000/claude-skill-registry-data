---
name: pumpfun
description: Entry-point router for the local Pump.fun skill suite. Use when the user asks about launching Pump.fun tokens, bonding-curve or AMM trading, quotes, fees, claims, incentives, SDK work, agent/MCP integration, security, testing, or release workflows.
---

# Pump.fun Skill Suite

Use this skill first for Pump.fun requests, then load the narrow skill that matches the task. Treat the focused `pump-*` skills as the canonical local playbooks; the `pumpfun-*` skills are quick operational shortcuts.

## Route by Task

| User intent | Use these skills |
|---|---|
| Token launch, lifecycle, graduation, migration | `pump-token-lifecycle`, `pump-sdk-core`, `pumpfun-launcher` |
| Bonding-curve math, quotes, price impact, analytics | `pump-bonding-curve`, `pumpfun-analytics` |
| Buy/sell execution across bonding curve or AMM | `pump-token-lifecycle`, `pumpfun-trading`, `pump-fee-system` |
| Creator fees, shareholder splits, distributable balances | `pump-fee-sharing`, `pump-fee-system`, `pump-claims-readonly`, `pumpfun-fees` |
| PUMP token incentives and claim previews | `pump-token-incentives`, `pump-claims-readonly` |
| Admin and authority operations | `pump-admin-ops` |
| PDAs, account layouts, Anchor, Token-2022, RPC batching | `pump-solana-architecture`, `pump-solana-dev` |
| Wallet generation and vanity addresses | `pump-solana-wallet`, `pump-rust-vanity`, `pump-ts-vanity`, `pump-shell-scripts` |
| Agent instruction files and MCP exposure | `pump-ai-agents`, `pump-mcp-server` |
| Security, tests, releases | `pump-security`, `pump-testing`, `pump-build-release` |

## Operating Rules

- Start with read-only state fetches, quotes, and simulations before building live transactions.
- Before any real transaction, confirm network, wallet, mint, amount, slippage, priority fee, and maximum SOL/token exposure.
- Use integer lamports/token base units with `BN`, `bigint`, or equivalent exact arithmetic. Do not use JavaScript `number` for balances, reserves, quotes, or fees.
- Keep instruction builders composable: return `TransactionInstruction[]` and let callers assemble, sign, and submit transactions.
- Use the Pump SDK package actually installed in the target repo. Examples may show `@nirholas/pump-sdk`; align imports with the repo's `package.json`.
- Never log, paste, or persist private keys except to explicitly requested keypair files with owner-only permissions.
- Query RPC for current bonding-curve, AMM, fee, claim, and wallet state. Do not assume prices, balances, graduation status, or claimability from stale context.

## Program IDs

| Program | Address |
|---|---|
| Pump | `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P` |
| PumpAMM | `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA` |
| PumpFees | `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ` |
| Mayhem | `MAyhSmzXzV1pTf7LsNkrNwkWKTo4ougAJ1PPg47MD4e` |
