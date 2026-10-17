---
name: eerc-privacy-threat-model
description: Use when the agent must reason precisely about what eERC hides vs what it leaks — encrypted amounts/balances vs visible sender/receiver/timing/graph — and how to mitigate metadata and correlation attacks.
category: Privacy Deep-Dive
difficulty: Advanced
version: "0.2.0"
---

# eERC — Privacy Threat Model

## Overview
eERC encrypts **values**, not **the fact that you transacted**. Designing a private system requires knowing exactly where the boundary is, or you will leak through metadata even though balances are encrypted.

## What is HIDDEN
- **Token balances** (encrypted ElGamal ciphertext on-chain).
- **Transfer / mint / withdraw amounts.**
- **Total supply** in standalone mode ([[eerc-hidden-supply]]).

## What is VISIBLE (on a public chain)
- **That a transaction occurred** and which eERC function was called.
- **Sender and recipient addresses** (the `from`/`to` of the tx and the registered parties).
- **Timing, frequency, ordering, and gas** of operations.
- **The transaction graph** — who interacts with whom, how often.
- **Converter deposits/withdrawals touch the public ERC-20**, exposing on/off-ramp amounts at the boundary ([[eerc-deposit-withdraw]]).

## Attack surface
| Attack | Mechanism | Mitigation |
|---|---|---|
| **Graph analysis** | from/to addresses reveal relationships | fresh/stealth addresses; route through a private L1 ([[combining-eerc-with-private-l1]]) |
| **Timing correlation** | deposit then transfer of similar timing | add delays/batching; avoid 1:1 patterns |
| **Amount fingerprinting** | unique on/off-ramp amounts at converter boundary | standalone mode; vary amounts; avoid round numbers |
| **Network metadata** | RPC provider sees IP + queries | self-hosted/private RPC ([[anonymity-network-privacy]]) |
| **Endpoint compromise** | client-side key theft | key hygiene ([[eerc-key-management]]) |

## Standalone vs converter (privacy)
- **Standalone:** strongest — no public-token boundary, hidden supply. Prefer for max privacy.
- **Converter:** weaker at the edges — deposits/withdrawals interact with the visible ERC-20; amounts can leak at on/off-ramp.

## Hardening
1. Run eERC on a **private L1** to also hide the graph/timing from outsiders.
2. Use **fresh addresses** per counterparty/context.
3. Prefer **standalone** when you don't need a public base asset.
4. Treat the converter boundary as the riskiest point; batch/normalize amounts.

## Common Pitfalls
- **"It's encrypted, so it's private."** Amounts are; the relationship graph is not.
- **Linkable amounts.** Encrypted balances still correlate if your amounts are unique identifiers.
- **Ignoring the public ERC-20 side** in converter mode.

## AI Agent Prompt
> "Act as a privacy threat analyst. Given my eERC design, enumerate what stays hidden vs what leaks (addresses, timing, graph, converter boundary) and recommend concrete mitigations."

## References
See `references/README.md` (academy 'How private is the blockchain', eERC technology-behind).
