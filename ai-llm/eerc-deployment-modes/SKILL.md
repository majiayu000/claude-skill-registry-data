---
name: eerc-deployment-modes
description: Use when the agent must choose between eERC Standalone mode (a brand-new private token) and Converter mode (wrapping an existing ERC-20). This is a deploy-time decision that determines the entire operation set.
category: eERC
difficulty: Beginner
version: "0.1.0"
---

# eERC — Standalone vs Converter Mode

## Overview
eERC has two operating modes, fixed at deployment by the `isConverter` flag on `EncryptedERC`. The mode determines which operations are valid and how supply is managed.

## Standalone Mode (`isConverter: false`)
- Creates an **entirely new private ERC-20**.
- Supply managed by **`privateMint` / `privateBurn`** ([[eerc-mint-burn]]).
- **Total supply can be hidden** — strongest privacy.
- `name` / `symbol` are set at deploy (e.g. `"Test"`, `"TEST"`).
- Ideal for: enterprise/native tokens, regulated private markets, anything private from genesis.

## Converter Mode (`isConverter: true`)
- **Wraps an existing ERC-20** into an encrypted form via a `TokenTracker`.
- Supply managed by **`deposit` (wrap) / `withdraw` (unwrap)** ([[eerc-deposit-withdraw]]).
- `name` / `symbol` are typically left empty (derived per wrapped token).
- Maintains compatibility with the original asset; users opt into privacy and can exit.
- Ideal for: adding optional privacy to an existing token without changing the base asset.

## Decision matrix
| You want... | Mode |
|---|---|
| A new token that is private from day one | **Standalone** |
| Hidden total supply | **Standalone** |
| To add privacy to an existing ERC-20 (e.g. USDC) | **Converter** |
| Users to move funds in/out of a public token | **Converter** |

## How it's set (deploy)
```ts
// Standalone
await factory.deploy({ registrar, isConverter: false, name: "Test", symbol: "TEST", /* verifiers */, decimals });
// Converter
await factory.deploy({ registrar, isConverter: true, name: "", symbol: "", /* verifiers */, decimals });
```
Full deploy: [[eerc-deploy-contracts]].

## Common Pitfalls
- **Calling the wrong ops for the mode.** `deposit`/`withdraw` only work in converter mode; `privateMint`/`privateBurn` are for standalone. The SDK's `useEncryptedBalance` exposes both, but the contract reverts on the wrong one.
- **Expecting to switch modes later.** Mode is immutable post-deploy; deploy a new contract to change it.
- **Converter without a token address.** Converter operations need the wrapped `tokenAddress`; the SDK hook takes it as a parameter.

## AI Agent Prompt
> "Act as an eERC architect. Given my use case, recommend Standalone or Converter mode, justify it, and show the corresponding deploy parameters."

## References
See `references/README.md` (deploy-standalone.ts, deploy-converter.ts, academy deployment modes).
