---
name: eerc-cryptography
description: Use when the agent needs to understand or explain the cryptography behind eERC — BabyJubJub curve, ElGamal homomorphic encryption, Poseidon hashing, and Groth16 zk-SNARKs — e.g. when choosing a proving system or debugging proof generation.
category: eERC
difficulty: Intermediate
version: "0.1.0"
---

# eERC — Cryptography & Proving System

## Overview
eERC combines four ZK-friendly primitives so that token amounts stay encrypted while still being provably valid.

## The primitives
1. **BabyJubJub elliptic curve** — a twisted Edwards curve optimized for zk-SNARKs. Used for key generation and in-circuit signature/encryption operations. User keys are points on this curve.
2. **ElGamal encryption** — public-key encryption over BabyJubJub used to encrypt balances and transfer amounts. It is **homomorphic for addition**, so encrypted balances can be updated (credited/debited) on-chain *without decryption*.
3. **Poseidon hashing** — a ZK-friendly hash used for commitments and ciphertext integrity (the "PCT" — Poseidon Cipher Text) inside proof circuits; cheap to verify in-circuit.
4. **Groth16 zk-SNARKs** — the proving system: small proofs, fast verification, low gas. Each operation (register/mint/transfer/withdraw/burn) has its own circuit and on-chain verifier.

## Why Groth16 (and how to change it)
The proving system is **fixed by the deployed verifiers**, not chosen by end-users. The official eERC contracts use **Groth16**.

| Proof System | Trade-off | Status in eERC |
|---|---|---|
| **Groth16** | Fast verify, tiny proof, low gas; needs per-circuit trusted setup | ✅ Default |
| PLONK | Universal setup, flexible | ❌ Requires custom build |
| Halo2 | No trusted setup, recursion | ❌ Major changes |

To switch: modify the Circom circuits → regenerate verifiers → deploy new contracts. See [[eerc-circuits-proofs]].

## What is and isn't hidden
- **Hidden:** balances, transfer/mint/withdraw amounts (encrypted ElGamal ciphertext on-chain).
- **Visible:** that a transaction happened, the sender/receiver addresses, and timing (on a public chain). For full opacity, host eERC on a private L1 — [[combining-eerc-with-private-l1]].

## Common Pitfalls
- **Believing the contract decrypts anything.** It only verifies Groth16 proofs and applies homomorphic ciphertext updates.
- **Mixing up Groth16 trusted setups.** Each circuit needs the correct `.ptau` size (transfer/mint = 15, withdraw = 14, registration = 11).

## AI Agent Prompt
> "Act as a ZK cryptographer. Explain how BabyJubJub + ElGamal + Poseidon + Groth16 fit together in eERC so that on-chain balances stay encrypted yet provably correct."

## References
See `references/README.md` (academy "Technology behind eERC" + EncryptedERC `contracts/libraries/BabyJubJub.sol`).
