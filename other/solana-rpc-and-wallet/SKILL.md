---
name: solana-rpc-and-wallet
description: Safe patterns for reading balances, token accounts, metadata, Token-2022 extensions, and managing the throwaway wallet connection without ever handling private keys.
---

# Solana RPC and Wallet

## Wallet Rules (non-negotiable)
- Only a dedicated throwaway wallet ≤ $200 USDC + SOL for fees
- Private keys and seed phrases never enter chat, files, or memory
- Connection is performed by human via screen hand-off only
- Public address is recorded in desk.md after successful connection

## Priority Fees & Compute
Prefer the output of `tools/priority_fee.py`. Cap maximum fee so a spike cannot drain the wallet.
