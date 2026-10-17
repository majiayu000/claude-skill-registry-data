---
name: private-permissioned-l1s
description: Use when the agent needs the conceptual model for private vs permissioned vs permissionless Avalanche L1s, the access-privacy (walled garden) vs data-privacy distinction, and how to choose RPC and write-access restrictions.
category: Avalanche L1
difficulty: Intermediate
version: "0.1.0"
---

# Private & Permissioned L1s — Access Privacy

## Overview
"Private" means two different things. Getting this right drives the whole design.
- **Access privacy (Walled Garden):** the chain is hidden — only authorized participants can reach the RPC to read anything. **Natively supported on Avalanche.**
- **Data privacy (Encryption):** the chain is public, but transaction *contents* are encrypted (e.g. **eERC** zk-SNARKs, Zama FHE). Anyone sees that txs happened; contents are hidden.

Most private blockchains use **access** privacy; some public chains add **data** privacy. eERC ([[eerc-introduction]]) is the data-privacy tool; this skill is the access-privacy tool.

## The three models
| Aspect | Permissioned **Private** | Permissioned **Public** | **Permissionless** |
|---|---|---|---|
| RPC access | Restricted endpoints | Public | Public |
| Data visibility | Authorized only | Anyone | Anyone |
| Tx submission | Authorized users | Authorized / anyone | Anyone |
| Contract deploy | Authorized users | Authorized / anyone | Anyone |
| Validator entry | Permission required | Permission required | Anyone (with stake) |
| Governance | Centralized/Hybrid | Centralized/Hybrid | Decentralized |

## How Avalanche implements each
- **Permissioned Private L1:** fixed validator set (ValidatorManager, [[poa-validator-manager]]) **+ restricted RPC** ([[restrict-rpc-access]]) **+ write gating** ([[l1-transaction-allowlist]], [[l1-deployer-allowlist]]).
- **Permissioned Public L1:** Proof of Authority with controlled validator additions; public RPC; gated writes.
- **Permissionless L1:** Proof of Stake; anyone validates by staking.

## Choosing the model — questions to ask
1. Regulatory: do you need KYC/AML gating? → permissioned + allowlists.
2. Transparency: must the public audit it? → public RPC (or data privacy via eERC).
3. Trust: closed validator set acceptable, or need economic security? → PoA vs PoS.
4. Participant control: must you control who interacts? → restrict RPC + tx allowlist.

## Common Pitfalls
- **Confusing the two privacies.** A walled-garden L1 still stores plaintext; anyone who gets RPC access reads everything. Combine with eERC for data confidentiality ([[combining-eerc-with-private-l1]]).
- **Restricting writes but not reads (or vice-versa).** "Private" needs both: restricted RPC (reads) and allowlists (writes/deploys).

## AI Agent Prompt
> "Act as an enterprise blockchain architect. Classify whether I need access privacy, data privacy, or both, then map my Avalanche L1 to permissioned-private / permissioned-public / permissionless with the concrete restrictions to apply."

## References
See `references/README.md` (academy permissioned-l1s "Blockchain Permissioning", access-restriction course).
