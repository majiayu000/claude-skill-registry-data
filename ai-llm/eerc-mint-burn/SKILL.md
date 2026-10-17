---
name: eerc-mint-burn
description: Use when the agent needs to mint or burn eERC tokens in standalone mode — privateMint and privateBurn via the SDK, including the auditor PCT and balance handling. Standalone-only operations.
category: eERC
difficulty: Intermediate
version: "0.1.0"
---

# eERC — Private Mint & Burn (Standalone)

## Overview
In **standalone mode** ([[eerc-deployment-modes]]), supply is managed by **`privateMint`** (create encrypted tokens) and **`privateBurn`** (destroy them). Both run client-side proof generation and update encrypted balances homomorphically. These do **not** exist in converter mode (use deposit/withdraw there).

## Private mint
```ts
const { privateMint } = eerc.useEncryptedBalance();
// recipient must be registered
const { transactionHash } = await privateMint(recipientAddress, amount /* bigint */);
```
- Typically restricted to the contract **owner**.
- The SDK encrypts the minted amount with the recipient's public key and encodes an **auditor PCT** so the auditor can decrypt it later.
- Mint circuit (`mint.wasm`/`mint.zkey`) must be configured ([[eerc-sdk-setup]]).

## Private burn
```ts
const { privateBurn } = eerc.useEncryptedBalance();
const { transactionHash } = await privateBurn(amount /* bigint, <= decryptedBalance */);
```
- Burns from the caller's encrypted balance; requires a loaded decryption key and `0 < amount <= decryptedBalance`.
- Uses the burn circuit and current encrypted balance to prove the new balance is correct.

## After either op
```ts
await refetchBalance();
```

## Gas (C-Chain reference)
- `privateMint` ≈ 0.72M gas avg. `privateBurn` ≈ 1.03M gas avg. Plan UX for proof + verification latency.

## Common Pitfalls
- **Using mint/burn in converter mode.** They revert; converter uses `deposit`/`withdraw` ([[eerc-deposit-withdraw]]).
- **Unregistered recipient for mint.** The mint target needs a registered public key.
- **Auditor key unset.** Operations encode an auditor PCT and expect a valid auditor public key ([[eerc-auditor-compliance]]).
- **Amount scaling.** `amount` is a `bigint` in base units; scale by `decimals`.

## AI Agent Prompt
> "Act as an eERC engineer. Implement owner-gated `privateMint` to a registered recipient and user `privateBurn`, generating the proofs via the SDK and refetching the decrypted balance."

## References
See `references/README.md` (ac-eerc-sdk `useEncryptedBalance.tsx` privateMint/privateBurn, `EERC.ts`).
