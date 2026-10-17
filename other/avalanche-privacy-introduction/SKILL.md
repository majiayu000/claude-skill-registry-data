---
name: avalanche-privacy-introduction
description: Use this first for any Avalanche privacy request to decide between eERC (data privacy on a public chain) and a private/permissioned L1 (access privacy), or both. Covers the access-vs-data privacy distinction and a decision matrix.
category: Foundation
difficulty: Beginner
version: "0.1.0"
---

# Avalanche Privacy — Introduction & Decision Guide

## Overview
Avalanche offers **two complementary, independent privacy models**. Picking the right one (or both) is the first decision in any privacy project.

| | **eERC (Encrypted ERC)** | **Private / Permissioned L1** |
|---|---|---|
| Privacy type | **Data privacy** | **Access privacy** ("walled garden") |
| What is hidden | Token *balances* and *transfer amounts* | The *whole chain* (who can read/write) |
| Chain | Runs on a **public** chain (C-Chain, Fuji, any EVM) | A **sovereign L1** you control |
| How | zk-SNARKs + ElGamal homomorphic encryption | Restricted RPC + allowlist/KYC precompiles |
| Data on chain | Encrypted (ciphertext + handles) | Plaintext (but access-restricted) |
| Compliance | Rotatable auditor keys (selective decrypt) | Validator/operator governance, KYC gating |

> **One-liner:** eERC hides the *data* on an open chain. A private L1 hides the *whole chain* behind a wall. Use either, or both.

## Decision matrix
- **"I need confidential token balances/amounts, but on a public, composable chain"** → **eERC**. Start at [[eerc-introduction]].
- **"I need to control who can even connect, read, or transact on the network (enterprise/consortium)"** → **Private L1**. Start at [[private-permissioned-l1s]].
- **"I need encrypted data on a network only my participants can access"** → **Both**. See [[combining-eerc-with-private-l1]].
- **"I need public auditability with no hidden data"** → neither; use a standard permissionless L1 or C-Chain.

## Common Pitfalls
- **Assuming a "private L1" encrypts data.** It does not. Anyone with RPC access reads plaintext. Add eERC for data confidentiality.
- **Assuming eERC hides metadata.** Transaction *existence*, sender/receiver addresses, and timing are visible on a public chain; only amounts/balances are encrypted.
- **Treating the two as alternatives only.** They compose — eERC contracts deploy fine on a custom L1.

## AI Agent Prompt
> "Act as an Avalanche privacy architect. Given my requirements, classify whether I need data privacy (eERC), access privacy (a private/permissioned L1), or both, and route me to the correct skills with a justification."

## References
See `references/README.md` — based on the Builder Hub permissioning course and the eERC academy.
