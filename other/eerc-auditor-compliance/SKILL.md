---
name: eerc-auditor-compliance
description: Use when the agent needs eERC compliance/auditing — setting and rotating the auditor public key, and using auditorDecrypt() so an authorized auditor can read transaction history. Key to making confidential tokens regulation-ready.
category: eERC
difficulty: Advanced
version: "0.1.0"
---

# eERC — Auditor & Compliance

## Overview
eERC has a **built-in auditability module**: every private operation encodes an **auditor PCT** (Poseidon ciphertext) using the auditor's public key. A designated auditor can therefore **selectively decrypt** transaction history for compliance — without weakening privacy for anyone else, and **without redeploying** when keys rotate.

## Set the auditor key
The contract owner designates an auditor; the auditor must be a **registered** eERC user (has a public key).
```ts
// SDK: set the auditor by address (reads their registered public key)
const { setContractAuditorPublicKey } = useEERC(/* ... */);
const txHash = await setContractAuditorPublicKey(auditorAddress);
```
On-chain this corresponds to `setAuditorPublicKey(address)` on `EncryptedERC` (owner-only). After this, `isAuditorKeySet` becomes true and operations can encode auditor PCTs.

## Audit (decrypt history)
The wallet that holds the auditor key can decrypt all transactions:
```ts
const { areYouAuditor, auditorDecrypt } = useEERC(/* ... */);

if (areYouAuditor) {
  const txs = await auditorDecrypt();
  // txs: { type, amount, sender, receiver, transactionHash }[]
}
```
`hasBeenAuditor()` / `hasBeenAuditor` state lets you check whether the current wallet was ever the auditor.

## Key rotation & revocation
- Rotate by calling `setAuditorPublicKey` with a **new** auditor address — future operations encode PCTs for the new auditor.
- This does **not** retroactively grant the new auditor access to history encoded for a previous auditor (plan rotation windows accordingly).
- No redeploy needed; the registrar/auditor manager handle the swap.

## Compliance considerations (production)
- Treat the auditor key as **highly privileged** — it can decrypt all flows. Store it securely; consider a dedicated, access-controlled wallet.
- Align who holds the auditor key and retention of decrypted data with your jurisdiction (KYC/AML).
- Document rotation procedure and revocation triggers.

## Common Pitfalls
- **Auditor not registered.** You cannot set an auditor that has no registered public key.
- **Operating with no auditor set.** Transfers/mints encode an auditor PCT and expect a valid auditor public key.
- **Assuming rotation is retroactive.** It is forward-looking only.

## AI Agent Prompt
> "Act as a compliance engineer. Set a registered auditor via `setContractAuditorPublicKey`, implement an auditor dashboard using `auditorDecrypt()`, and document a secure key-rotation procedure."

## References
See `references/README.md` (ac-eerc-sdk `useEERC.tsx` auditor functions, `EERC.ts` auditorDecrypt, academy auditability module).
