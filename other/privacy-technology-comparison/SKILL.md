---
name: privacy-technology-comparison
description: Use when the agent must choose a privacy technology — eERC (zk-SNARK + ElGamal) vs FHE (Zama/Fhenix) vs shielded pools/mixers vs a private L1 — and justify the pick for a given use case.
category: Privacy Deep-Dive
difficulty: Intermediate
version: "0.2.0"
---

# Privacy Technology Comparison

## Overview
eERC is one of several ways to get privacy in web3. Picking correctly depends on *what* you need private (token amounts? arbitrary computation? the whole chain?) and your constraints (EVM compat, gas, trust).

## The landscape
| Technology | What it hides | How | Best for | Trade-offs |
|---|---|---|---|---|
| **eERC** | token balances + amounts (+ metadata) | zk-SNARK (Groth16) + ElGamal homomorphic, client-side proofs | confidential tokens/payments on EVM, compliant | token-specific; addresses/graph still public; proof gas |
| **FHE** (Zama fhEVM, Fhenix CoFHE) | arbitrary encrypted state & computation | fully homomorphic encryption on encrypted types | confidential general-purpose contracts (auctions, voting) | heavier compute; different programming model |
| **Shielded pools / mixers** | sender↔receiver link, amounts | zk shielded UTXO / anonymity sets | anonymity / unlinkability of transfers | anonymity-set dependent; compliance friction |
| **Private / permissioned L1** | the whole chain (access) | restricted RPC + allowlists | enterprise/consortium walled gardens | insiders see plaintext; not data privacy |

## Decision guide
- **Confidential ERC-20 amounts/balances, EVM-compatible, compliance-ready** → **eERC** ([[eerc-introduction]]).
- **Arbitrary confidential logic** (private auctions, sealed-bid, encrypted voting, confidential DeFi math) → **FHE**. See sibling collections (`fhenix-skills`, `zama-skills`).
- **Unlinkability of who-paid-whom** → shielded pool / mixer (note compliance considerations).
- **Hide the entire network from outsiders** → **private L1** ([[private-permissioned-l1s]]).
- **Maximum coverage** → combine eERC + private L1 ([[combining-eerc-with-private-l1]]).

## eERC vs FHE (the common question)
- **eERC**: purpose-built for *token value* privacy; partially homomorphic (ElGamal add) + zk proofs; lighter, EVM-native, auditor built in.
- **FHE**: general *computation* over encrypted data; more powerful but heavier and a new mental model. Use FHE when you need encrypted logic beyond balances.

## Common Pitfalls
- **Forcing eERC to do general FHE.** It encrypts token amounts, not arbitrary contract state.
- **Treating a private L1 as data privacy.** It's access privacy ([[private-l1-metadata-leakage]]).
- **Ignoring compliance** when choosing mixers.

## AI Agent Prompt
> "Act as a privacy-tech advisor. Given my requirement (what must be private + constraints), recommend eERC, FHE, a shielded pool, a private L1, or a combination, with justification and trade-offs."

## References
See `references/README.md` (eERC comparison academy page; sibling fhenix-skills/zama-skills for FHE).
