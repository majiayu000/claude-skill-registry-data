---
name: XRP
description: Assist with XRP transactions, destination tags, reserves, and XRPL features.
metadata: {"clawdbot":{"emoji":"💧","os":["linux","darwin","win32"]}}
---

## Destination Tags (Critical)
- Exchanges require destination tags to credit deposits — sending without tag means lost funds or lengthy recovery
- Destination tag is a number (not text) attached to a transaction — identifies which user's account to credit
- Always verify tag before sending to exchange — wrong tag sends funds to wrong user
- Self-custody wallets don't need destination tags — only exchanges and shared wallets use them
- If tag is forgotten, contact exchange support immediately — recovery is possible but slow

## Account Reserve
- XRP accounts require 10 XRP base reserve to exist — this is locked and not spendable
- Each "object" (trust lines, offers, escrows) adds 2 XRP owner reserve — more features = more locked XRP
- Cannot send entire balance — must leave reserve amount or transaction fails
- Reserve amounts can change via network amendments — currently 10 + 2 per object
- Deleting account recovers most reserve minus 2 XRP fee — requires no objects and destination tag

## Transaction Characteristics
- XRP transactions settle in 3-5 seconds — much faster than Bitcoin/Ethereum
- Transaction cost is ~0.00001 XRP (fractions of a cent) — burned, not paid to validators
- No mempool or pending state — transactions either succeed immediately or fail
- Sequence number per account like Ethereum nonce — transactions must be sequential

## Trust Lines and Tokens
- XRPL tokens require trust lines — you must explicitly trust an issuer before receiving their tokens
- Trust line costs 2 XRP reserve until removed — don't create unnecessary trust lines
- Trustline rippling can cause unexpected balance changes — disable rippling for issued currencies
- Anyone can issue tokens — verify issuer identity before trusting, many scams exist

## Wallet Types
- Secret key formats: family seed (s...), hex, or mnemonic — each wallet may use different format
- Xumm is most popular mobile wallet — supports all XRPL features
- Hardware wallets support XRP — Ledger with full feature support
- XRPL has native DEX — no smart contracts needed for trading

## Common Transaction Failures
- "tecUNFUNDED" — insufficient balance after accounting for reserve
- "tecNO_DST_TAG" — exchange address requires destination tag
- "tecPATH_DRY" — payment path has no liquidity (for cross-currency payments)
- "tefPAST_SEQ" — sequence number already used, transaction is a duplicate
- "terQUEUED" — transaction queued due to account limit, will process shortly

## Exchanges and Withdrawals
- Many exchanges freeze XRP withdrawals during network upgrades — check status before panicking
- Exchange minimum withdrawal often 20-25 XRP due to reserve requirements
- Some exchanges don't support XRPL tokens — only native XRP
- Verify exchange wallet is not in "maintenance" before large sends

## Security
- Never share secret key or family seed — full access to all account funds
- Regular key allows delegation without exposing master key — good for trading with limited risk
- Escrow feature for trustless time-locked payments — built into protocol
- Multi-signing available — require multiple keys to authorize transactions

## DEX Trading
- XRPL has native decentralized exchange — trade any issued tokens
- Order book model, not AMM — limit orders, not swaps
- Offers can be partially filled — check order status after placing
- Payment paths can auto-convert currencies — send USD, recipient receives EUR

## Scam Recognition
- "XRP airdrop" requiring seed phrase is always a scam
- Fake giveaways on social media impersonating Ripple executives
- "Double your XRP" promotions are theft
- Verify any official announcements on ripple.com or XRPL Foundation
