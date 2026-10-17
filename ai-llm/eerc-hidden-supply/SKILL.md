---
name: eerc-hidden-supply
description: Use when the agent needs to hide an eERC token's total supply — why standalone mode can keep supply private, the privacy benefits and trade-offs vs converter mode, and design implications.
category: Privacy Deep-Dive
difficulty: Intermediate
version: "0.2.0"
---

# eERC — Hidden Total Supply

## Overview
Beyond per-user balances, **standalone-mode eERC can keep the *total supply* private**. This is a distinct, strong privacy property: observers can't infer the size of the token economy, large holders, or issuance events.

## Why standalone hides supply
- **Standalone** manages supply via `privateMint`/`privateBurn` ([[eerc-mint-burn]]) — all amounts encrypted, with no public reference asset. There is no plaintext "totalSupply" to read.
- **Converter** wraps an existing ERC-20; the **public token's supply and the contract's holdings are visible**, and deposits/withdrawals expose value at the boundary. Supply privacy is therefore weaker in converter mode.

| Property | Standalone | Converter |
|---|---|---|
| Per-user balances hidden | ✅ | ✅ |
| Transfer amounts hidden | ✅ | ✅ |
| **Total supply hidden** | ✅ | ❌ (public base token) |
| On/off-ramp amount privacy | n/a | ❌ leaks at boundary |

## When hidden supply matters
- Enterprise/native tokens where issuance size is sensitive.
- Regulated private markets that shouldn't reveal market cap.
- Preventing competitors/observers from sizing your economy or spotting whales.

## Trade-offs
- **No public peg/base asset.** Standalone is a new token; users can't trivially exit to a known ERC-20 (no withdraw). Choose standalone when that's acceptable.
- **Issuance trust.** Hidden supply means external parties can't verify supply — rely on the auditor channel ([[selective-disclosure-and-compliance]]) for accountability.

## Design tips
- If you need both hidden supply **and** a public exit, you generally must pick: standalone (hidden supply, no public exit) or converter (public exit, visible base supply).
- Pair hidden supply with the auditor key so a regulator/internal auditor can still verify issuance privately.

## Common Pitfalls
- **Expecting hidden supply in converter mode.** The wrapped ERC-20 exposes it.
- **No accountability plan.** Hidden supply without an auditor can raise trust concerns — design the disclosure channel.

## AI Agent Prompt
> "Act as a tokenomics + privacy engineer. Decide whether to use standalone (hidden total supply, no public exit) or converter (public exit, visible supply) for my token, and design auditor-based accountability for the hidden-supply case."

## References
See `references/README.md` (academy deployment modes + technology-behind, EncryptedERC README).
