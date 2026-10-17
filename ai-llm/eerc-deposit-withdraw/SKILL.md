---
name: eerc-deposit-withdraw
description: Use when the agent needs converter-mode eERC operations — deposit (wrap an existing ERC-20 into encrypted form) and withdraw (unwrap back to the public ERC-20). Converter-only operations.
category: eERC
difficulty: Intermediate
version: "0.1.0"
---

# eERC — Deposit & Withdraw (Converter)

## Overview
In **converter mode** ([[eerc-deployment-modes]]), users move value between the public ERC-20 and its encrypted eERC form:
- **`deposit`** — wrap public ERC-20 → encrypted eERC (enter privacy).
- **`withdraw`** — unwrap eERC → public ERC-20 (exit privacy).

These replace mint/burn. They require the wrapped token's address.

## Deposit (wrap)
```ts
const balance = eerc.useEncryptedBalance(WRAPPED_TOKEN_ADDRESS);
const { deposit } = balance;

// 1) approve the EncryptedERC to pull the ERC-20 (standard ERC-20 approve)
await erc20.write.approve([EERC_ADDRESS, amount]);
// 2) deposit -> mints encrypted balance to the user
const { transactionHash } = await deposit(amount /* bigint, base units */);
await balance.refetchBalance();
```
Under the hood the SDK uses the token `decimals` and the deposit verifier; the public ERC-20 is transferred into the contract and an equivalent encrypted balance is credited.

## Withdraw (unwrap)
```ts
const { withdraw } = eerc.useEncryptedBalance(WRAPPED_TOKEN_ADDRESS);
const { transactionHash } = await withdraw(amount /* bigint, <= decryptedBalance */);
```
Generates a withdraw proof, debits the encrypted balance, and releases the public ERC-20 back to the user.

## Gas (C-Chain reference)
- `deposit` ≈ 0.56M gas avg, `withdraw` ≈ 0.80M gas avg.

## Common Pitfalls
- **No approval before deposit.** Standard ERC-20 `approve` is required first.
- **Missing `tokenAddress`.** Converter ops need the wrapped token address passed to `useEncryptedBalance`.
- **Using deposit/withdraw in standalone mode.** They revert; standalone uses `privateMint`/`privateBurn` ([[eerc-mint-burn]]).
- **Decimals mismatch.** `amount` is base units of the underlying ERC-20.

## AI Agent Prompt
> "Act as an eERC engineer. Implement converter flows: approve + `deposit` to wrap an ERC-20 into encrypted form, and `withdraw` to unwrap, refetching the decrypted balance after each."

## References
See `references/README.md` (ac-eerc-sdk `useEncryptedBalance.tsx` deposit/withdraw, `EERC.ts`, academy contracts flow).
