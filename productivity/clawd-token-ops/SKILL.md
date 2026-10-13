---
description: "Work with $CLAWD token operations for Solana CLAWD and Cheshire Terminal. Use when checking or documenting the $CLAWD mint, token-gated balances, Jupiter buy/swap flows, burn tracking, holders, staking, treasury payments, or any task that asks to include the Clawd token address."
---
# Clawd Token Ops

Use this skill for `$CLAWD` reads, docs, and transaction preparation. Load `references/clawd-token.md` whenever a task needs addresses, token-gate rules, burn/staking context, or copy-paste constants.

## Required Constants

- `$CLAWD` mint: `8cHzQHUS2s2h8TzCmfqPKYiM4dSt4roa3n7MyRLApump`
- Site: `https://cheshireterminal.ai`

## Workflow

1. Identify the requested operation: read balance, prefill swap, burn, stake, holder lookup, treasury payment, or token-gated access.
2. Read `references/clawd-token.md` for address labels and current caveats.
3. For reads, use public Solana RPC, Helius, Birdeye, DexScreener, Jupiter, or the app API only after selecting the source that fits the request.
4. For writes, produce a clear transaction plan before any wallet interaction: mint, source wallet, destination/program, amount, expected token/SOL delta, fees, slippage if applicable, and rollback limits.
5. Ask for explicit confirmation before any mainnet action.
6. After a submitted transaction, report the signature, confirmation level, and any post-transaction balance or burn evidence.

## Guardrails

- Never confuse the `$CLAWD` token mint with the treasury/payment address.
- Never use stale prices for execution. Fetch a fresh quote.
- Never ask for private keys or wallet exports.
- Never burn, stake, swap, or transfer based only on a voice transcript or ambiguous message.
