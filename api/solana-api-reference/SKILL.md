---
name: solana-api-reference
description: Compact, reliable reference for the most-used Jupiter endpoints, Solana RPC methods, rugcheck patterns, and Solscan queries. Prevents hallucination of API shapes.
---

# Solana API Reference

## Jupiter
- Prefer current lite / swap endpoints; fall back to legacy if needed
- Key parameters: inputMint, outputMint, amount, slippageBps

## Solana RPC (common)
- getBalance
- getTokenAccountsByOwner
- getAccountInfo (mint / freeze authority)
- getRecentPrioritizationFees
- getTokenLargestAccounts
- getTransaction / getSignaturesForAddress

## Usage Rule
When in doubt about an endpoint, re-read this skill or the live documentation rather than guessing.
