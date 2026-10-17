---
name: anonymity-network-privacy
description: Use when the agent must address network-layer privacy for Avalanche privacy apps — RPC providers seeing IP and queries, address clustering, mempool exposure, and using private RPC / relayers / account abstraction to reduce metadata leakage.
category: Privacy Deep-Dive
difficulty: Advanced
version: "0.2.0"
---

# Anonymity & Network-Layer Privacy

## Overview
On-chain encryption (eERC) and access control (private L1) don't cover the **network layer**. The RPC you talk to, your IP, your address reuse, and the mempool all leak metadata that can deanonymize otherwise-confidential activity. This skill closes that gap.

## Leak vectors
- **RPC provider visibility.** A public RPC sees your **IP address**, the **addresses you query**, and the **transactions you broadcast** — linking your identity to your on-chain activity even if amounts are encrypted.
- **Address clustering.** Reusing one address across contexts links them; funding patterns tie addresses to a real identity.
- **Mempool exposure.** Pending txs reveal sender/intent before inclusion (on chains with a public mempool).
- **Frontend/RPC fingerprinting.** Wallet + dApp + RPC combination can fingerprint users.

## Mitigations
1. **Use private/self-hosted RPC.** Run your own node or a trusted private endpoint so a third party isn't logging your IP + queries. On a private L1, give each member a credentialed gateway ([[restrict-rpc-access]]).
2. **Fresh addresses.** Use a new address per counterparty/context to break clustering ([[eerc-privacy-threat-model]]).
3. **Network anonymity.** Access RPC over VPN/Tor where IP exposure is a concern.
4. **Relayers / account abstraction.** Submit transactions via a relayer or ERC-4337 paymaster so the broadcasting address/IP isn't the user's — reduces sender-side metadata.
5. **Avoid leaky reads.** Balance/state queries to a public RPC reveal interest in specific addresses; route reads through your own node too.

## Layered privacy stack
| Layer | Tool |
|---|---|
| Token value | eERC ([[eerc-introduction]]) |
| Transaction context | encrypted metadata ([[eerc-encrypted-metadata]]) |
| Who can read the chain | private L1 / restricted RPC |
| **IP / RPC metadata** | **private RPC, VPN/Tor, relayers (this skill)** |
| Address linkage | fresh/stealth addresses |

## Common Pitfalls
- **Encrypting on-chain but using a public RPC.** The provider links your IP to your addresses — a major leak.
- **Single reused address.** Clusters all your private activity.
- **Ignoring the mempool/reads.** Both leak intent.

## AI Agent Prompt
> "Act as an opsec engineer for a confidential dApp. Identify network-layer leaks (RPC/IP, address reuse, mempool) and implement mitigations: private RPC, fresh addresses, VPN/Tor, and relayer/AA submission."

## References
See `references/README.md` (network privacy synthesis; restrict-rpc-access, threat-model skills).
