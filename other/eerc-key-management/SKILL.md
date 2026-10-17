---
name: eerc-key-management
description: Use when the agent must handle eERC keys safely — the user decryption key (derived from a wallet signature, client-side only) and the privileged auditor key — covering derivation, storage, recovery, and rotation.
category: Privacy Deep-Dive
difficulty: Advanced
version: "0.2.0"
---

# eERC — Key Management

## Overview
eERC privacy depends on two keys. Mishandling either breaks confidentiality or locks users out. This skill defines their lifecycle and custody rules.

## 1. User decryption key
- **Derived deterministically from a wallet signature** during `generateDecryptionKey()` ([[eerc-sdk-registration]]). The same wallet reproduces the same key on any device — no separate backup needed.
- **Client-side only.** It decrypts the user's balances/metadata locally. The contract never sees it.
- **Bound to the wallet address.** Switching wallets resets decrypted state to `0n` (the SDK enforces this).

**Rules**
- Never log, transmit, or persist it server-side. Keep in memory or, if cached, in secure client storage.
- To "recover," just re-sign with the wallet — do not build a server-side key vault.
- Treat the wallet's signing key as the root of the user's privacy.

## 2. Auditor key (privileged)
- The auditor's public key is set on the contract by the owner ([[eerc-auditor-compliance]]); the auditor holds the matching private key and can **decrypt all transactions** via `auditorDecrypt()`.
- This is a **highly privileged** key — compromise reveals every user's amounts (and encrypted metadata).

**Rules**
- Custody it in a dedicated, access-controlled wallet (ideally hardware/HSM or a controlled signer).
- Document who holds it and the retention policy for decrypted data (compliance/jurisdiction).
- **Rotation is forward-looking:** `setAuditorPublicKey(newAuditor)` makes future operations decryptable by the new auditor; it does **not** retroactively grant access to history encoded for the old auditor. Plan rotation windows.

## Threats & mitigations
| Threat | Mitigation |
|---|---|
| Client-side key theft (XSS, malware) | minimize key lifetime in memory; CSP; hardware wallets |
| Auditor key compromise | HSM/multisig custody; rotate; least privilege |
| Lost user key | re-derive from wallet signature (no vault needed) |
| Lost wallet seed | standard wallet recovery — the root of everything |

## Common Pitfalls
- **Server-side decryption key storage.** Defeats the model — keys are client-side.
- **Assuming rotation is retroactive.** It isn't.
- **Treating the auditor key like any service key.** It can decrypt everything.

## AI Agent Prompt
> "Act as a security engineer. Implement eERC key handling: derive the user decryption key from the wallet signature (client-side only), re-derive on new devices, and define secure custody + forward-looking rotation for the auditor key."

## References
See `references/README.md` (ac-eerc-sdk generateDecryptionKey/isDecryptionKeySet, EncryptedERC AuditorManager).
