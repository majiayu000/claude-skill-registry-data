---
name: eerc-private-transfers
description: Use when the agent needs to implement or explain confidential eERC transfers — client-side proof generation, the transfer ZK circuit, amount PCTs, and the on-chain transfer call. Applies to both standalone and converter modes.
category: eERC
difficulty: Advanced
version: "0.1.0"
---

# eERC — Confidential Transfers

## Overview
A private transfer moves encrypted value from sender to receiver without revealing the amount on-chain. The SDK generates a **transfer ZK proof** client-side; the contract verifies it and homomorphically updates both encrypted balances.

## What happens in a transfer
1. SDK reads the sender's current encrypted balance + decryption key.
2. It builds the **transfer circuit** inputs: new sender balance, receiver-encrypted amount, and an **auditor PCT** (so the auditor can later decrypt) — all using the auditor's public key.
3. It encrypts the amount for the **receiver** (with the receiver's public key) and records a **sender PCT** for the sender's own history.
4. It produces a Groth16 proof and submits `transfer(...)`.
5. The contract verifies the proof and updates `EncryptedUserBalances` for both parties.

## Frontend call
```ts
const { privateTransfer, refetchBalance } = eerc.useEncryptedBalance(tokenAddress /* converter */);

const { transactionHash, receiverEncryptedAmount, senderEncryptedAmount } =
  await privateTransfer(recipient, amount /* bigint, base units */);
await refetchBalance();
```

## Preconditions (enforced by SDK/contract)
- Sender is **registered** and has a **decryption key** loaded.
- **Recipient is registered** — check with `isAddressRegistered(recipient)` first ([[eerc-sdk-registration]]).
- `0 < amount <= decryptedBalance` (the hook throws "Invalid amount" otherwise).
- The auditor public key is set on the contract (the transfer encodes an auditor PCT) — [[eerc-auditor-compliance]].

## What's visible vs hidden
- **Hidden:** the transfer amount and both parties' balances.
- **Visible:** that a transfer happened, the from/to addresses, gas, and timing. For full opacity, run eERC on a private L1 ([[combining-eerc-with-private-l1]]).

## Common Pitfalls
- **Recipient not registered.** Transfer to an unregistered address fails — there's no public key to encrypt to.
- **Missing transfer circuit URLs.** Proof generation needs the transfer `wasm`+`zkey` ([[eerc-sdk-setup]]).
- **Auditor key unset.** Transfers encode an auditor PCT; the contract/circuit expects a valid auditor public key.
- **High gas.** Proof verification is heavy (transfer ~0.95M gas on C-Chain). Set expectations / batch where possible.

## AI Agent Prompt
> "Act as an eERC engineer. Implement a confidential transfer: verify the recipient is registered, generate the transfer proof via the SDK, submit `privateTransfer`, and refetch the decrypted balance — explaining what stays hidden."

## References
See `references/README.md` (ac-eerc-sdk `EERC.ts` `transfer`/`generateTransferProof`, `useEncryptedBalance.tsx`).
