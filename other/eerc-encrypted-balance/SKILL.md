---
name: eerc-encrypted-balance
description: Use when the agent needs the eERC useEncryptedBalance hook — reading the decrypted balance and calling privateMint, privateBurn, privateTransfer, deposit, and withdraw from a frontend.
category: eERC SDK
difficulty: Intermediate
version: "0.1.0"
---

# eERC SDK — useEncryptedBalance

## Overview
`useEncryptedBalance` is the operations hook returned by `useEERC`. It decrypts the user's balance locally and exposes all value-moving actions. Pass a `tokenAddress` for converter-mode (wrapped) tokens; omit it for standalone.

## Usage
```ts
const eerc = useEERC(/* ... */);

// standalone:
const balance = eerc.useEncryptedBalance();
// converter (wrapped token):
const balance = eerc.useEncryptedBalance(WRAPPED_TOKEN_ADDRESS);

const {
  decryptedBalance,        // bigint, decrypted locally
  parsedDecryptedBalance,  // string
  encryptedBalance,        // bigint[] (ciphertext components)
  decimals,
  privateMint,             // standalone
  privateBurn,             // standalone
  privateTransfer,         // both
  deposit,                 // converter
  withdraw,                // converter
  refetchBalance,
} = balance;
```

## The actions
| Function | Signature | Mode | Notes |
|---|---|---|---|
| `privateMint` | `(recipient, amount: bigint)` | standalone | Mint encrypted tokens to a registered recipient (owner). [[eerc-mint-burn]] |
| `privateBurn` | `(amount: bigint)` | standalone | Burn your encrypted tokens. [[eerc-mint-burn]] |
| `privateTransfer` | `(to, amount: bigint)` | both | Confidential transfer; returns `{ transactionHash, receiverEncryptedAmount, senderEncryptedAmount }`. [[eerc-private-transfers]] |
| `deposit` | `(amount: bigint)` | converter | Wrap ERC-20 → eERC. [[eerc-deposit-withdraw]] |
| `withdraw` | `(amount: bigint)` | converter | Unwrap eERC → ERC-20. [[eerc-deposit-withdraw]] |
| `refetchBalance` | `()` | both | Re-read + re-decrypt after an op. |

## How decryption works
The hook reads the on-chain ciphertext (`balanceOf` or `getBalanceFromTokenAddress`), then calls `eerc.calculateTotalBalance(...)` locally using the decryption key. If the key is not set or the wallet changed, the balance resets to `0n`.

## Example: confidential send
```ts
async function send(to: `0x${string}`, human: string) {
  const amount = BigInt(Math.floor(Number(human) * 10 ** Number(decimals)));
  const { transactionHash } = await privateTransfer(to, amount);
  await refetchBalance();
  return transactionHash;
}
```

## Common Pitfalls
- **Amounts are `bigint` in base units.** Scale by `decimals` yourself.
- **Wrong action for the mode.** `deposit`/`withdraw` need a `tokenAddress`; `privateMint`/`privateBurn` are standalone-only.
- **Stale balance.** Call `refetchBalance()` after operations (the hook also watches, but explicit refetch is safer in flows).
- **Insufficient balance / zero amount.** The hook throws "Invalid amount" if `amount <= 0` or exceeds the decrypted balance.

## AI Agent Prompt
> "Act as a frontend engineer. Using `useEncryptedBalance`, render the decrypted balance and wire buttons for private transfer (+ mint/burn for standalone, deposit/withdraw for converter), scaling amounts by decimals and refetching after each op."

## References
See `references/README.md` (ac-eerc-sdk `src/hooks/useEncryptedBalance.tsx`).
