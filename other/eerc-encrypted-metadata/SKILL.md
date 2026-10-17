---
name: eerc-encrypted-metadata
description: Use when the agent needs to attach arbitrary-length encrypted metadata to eERC transactions (memos, invoice refs, payment notes) using the EncryptedMetadata module — what it is, how it stays private, and how to use it.
category: Privacy Deep-Dive
difficulty: Advanced
version: "0.2.0"
---

# eERC — Encrypted Metadata

## Overview
A newer eERC feature lets users send **arbitrary-length encrypted metadata** alongside a transaction — e.g. a memo, invoice ID, or payment reference — encrypted so only the intended party (and the auditor) can read it. This extends privacy beyond amounts to the *context* of a payment.

## Where it lives
- Contract: `EncryptedERC/contracts/metadata/EncryptedMetadata.sol` (+ `IEncryptedMetadata.sol`).
- The metadata is encrypted client-side (like balances) and stored/emitted with the operation; the chain never sees plaintext.

## Why it matters for privacy
- **Memos without leaks:** traditional "memo" fields are plaintext on-chain. Encrypted metadata keeps the reference confidential.
- **Confidential invoicing / reconciliation:** attach an invoice or order ID readable only by counterparties.
- **Auditor visibility preserved:** like amounts, metadata can be made decryptable by the auditor for compliance ([[eerc-auditor-compliance]]).

## Usage pattern
1. Client encrypts the metadata payload with the recipient's (and auditor's) public key — same key model as balances ([[eerc-cryptography]]).
2. Submit it with the transfer/operation.
3. Recipient decrypts locally with their decryption key ([[eerc-key-management]]).

> Check the current `@avalabs/ac-eerc-sdk` version for the exact metadata helper/params — the feature is newer than the core transfer API. Read `EncryptedMetadata.sol` and the SDK changelog.

## Privacy considerations
- **Length leaks.** Arbitrary-length payloads can leak via ciphertext size — pad to fixed buckets if size is sensitive.
- **Still public who/when.** Metadata being encrypted doesn't hide that a tx with metadata occurred between two addresses ([[eerc-privacy-threat-model]]).
- **Don't overload metadata** with data better kept off-chain entirely.

## Common Pitfalls
- **Assuming all SDK versions support it.** It's a recent addition; verify the installed version.
- **Encrypting to the wrong key.** Use the recipient's registered public key (and auditor's) — unregistered recipients can't decrypt.

## AI Agent Prompt
> "Act as an eERC engineer. Add an encrypted memo/invoice reference to a confidential transfer using the EncryptedMetadata module, encrypting to the recipient and auditor, and pad payloads to fixed sizes to avoid length leakage."

## References
See `references/README.md` (EncryptedERC `contracts/metadata/`, README 'Encrypted Metadata').
