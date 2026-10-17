---
name: private-l1-metadata-leakage
description: Use when the agent must understand the privacy limits of a "private"/permissioned Avalanche L1 — what still leaks even with restricted RPC (insiders, validators, node operators, logs) — and how to defend in depth.
category: Privacy Deep-Dive
difficulty: Advanced
version: "0.2.0"
---

# Private L1 — Metadata & Data Leakage

## Overview
A permissioned/private L1 provides **access privacy** (a walled garden), not **data privacy**. Even with restricted RPC ([[restrict-rpc-access]]), plenty is visible *inside* the wall. Know these limits before calling a chain "private."

## What still leaks on a private L1
- **Plaintext to all participants.** Anyone with RPC access reads all balances, txs, and contract state. There is no encryption.
- **Validators & node operators** see everything — transactions, state, and (at the node) mempool and peer info.
- **Logs & backups.** Node logs, snapshots, and explorer/indexer instances persist plaintext data.
- **The transaction graph** among participants is fully visible to insiders.
- **Operational metadata.** Who runs which validator, deployment patterns, and timing.

## Threat model by adversary
| Adversary | Sees |
|---|---|
| Outsider (no RPC) | nothing (if RPC truly restricted) |
| Authorized participant | all on-chain data (plaintext) |
| Validator / node operator | all data + mempool/peer metadata |
| Compromised RPC gateway | everything flowing through it |

## Defense in depth
1. **Add data privacy.** Deploy **eERC** on the L1 so even insiders can't see amounts/balances ([[combining-eerc-with-private-l1]]).
2. **Least-privilege RPC.** Per-member credentialed gateways, not a shared endpoint ([[restrict-rpc-access]]).
3. **Harden node infra.** Restrict log retention, secure snapshots/backups, lock down explorer/indexer access.
4. **Compartmentalize.** Separate chains per trust domain if participants shouldn't see each other's data.
5. **Govern operators.** Vet validator/node operators; they are trusted parties.

## Decision: is a private L1 enough?
- **Outsiders are the only threat** → private L1 alone may suffice.
- **Participants must not see each other's data** → private L1 + eERC (or FHE) is required.

## Common Pitfalls
- **Marketing "private" = "encrypted."** It isn't; insiders see plaintext.
- **Trusting node operators implicitly.** They see everything.
- **Forgetting logs/backups/explorers** as leak vectors.

## AI Agent Prompt
> "Act as a privacy auditor for a permissioned L1. Enumerate what still leaks (insiders, validators, logs, backups, graph) despite restricted RPC, and design defense in depth including eERC for data confidentiality."

## References
See `references/README.md` (academy permissioning 'access vs data privacy', node chain-configs).
