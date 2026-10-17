---
name: eerc-circuits-proofs
description: Use when the agent works with eERC zero-knowledge circuits and proofs — building Circom circuits, generating wasm/zkey artifacts, the trusted setup (.ptau), production vs test verifiers, and snarkjs vs gnark proving.
category: eERC
difficulty: Advanced
version: "0.1.0"
---

# eERC — Circuits, Proofs & Trusted Setup

## Overview
eERC ships **Circom circuits** (one per operation) compiled to Groth16. The SDK uses the resulting `wasm` + `zkey` to generate proofs in the browser; the contract verifies with the matching Solidity verifier. There are five circuits: **registration, mint, transfer, withdraw, burn**.

## Build the circuits & verifiers
```sh
cd EncryptedERC
npx hardhat zkit make --force   # compile circuits -> wasm, zkey, etc.
npx hardhat zkit verifiers      # generate Solidity Groth16 verifiers
```
Outputs include per-circuit `*.wasm` (witness) and `*.zkey` (proving key). Host these for the SDK ([[eerc-sdk-setup]]).

## Trusted setup (.ptau) — get the size right
Groth16 needs a Powers-of-Tau ceremony file per circuit size:
| Circuit | `.ptau` |
|---|---|
| transfer / mint | `powersOfTau28_hez_final_15.ptau` |
| withdraw | `powersOfTau28_hez_final_14.ptau` |
| registration | `powersOfTau28_hez_final_11.ptau` |
Verify a zkey:
```sh
snarkjs zkey verify <circuit>.r1cs powersOfTau28_hez_final_<size>.ptau <circuit>.zkey
```

## Production vs test verifiers
- Deploy scripts take `isProd`. **Set `isProd = true` for any non-local deployment** so the secure trusted-setup verifiers in `contracts/prod/*` are used. Test verifiers are insecure for real funds.

## snarkjs vs gnark
- The SDK supports two proving backends. `useEERC` auto-detects `snarkjsMode` from the contract bytecode (`bytecode.includes("a509711610")`). The `prove(data, type)` function and the prover WASM assets (`transferURL`, `multiWasmURL`) handle proof generation; you usually don't toggle this manually.

## Changing the proving system
To move off Groth16 (e.g. PLONK/Halo2) you must edit the Circom circuits, regenerate verifiers, and redeploy — see [[eerc-cryptography]].

## Common Pitfalls
- **Wrong `.ptau` size** → zkey generation/verification fails.
- **Stale artifacts** → rebuild after any circuit change; mismatched wasm/zkey/verifier reject valid proofs.
- **Shipping test verifiers** → never on mainnet.
- **Large assets** → `.zkey`/`.wasm` are big; serve from CDN and cache.

## AI Agent Prompt
> "Act as a ZK engineer. Build the eERC circuits, generate wasm/zkey with the correct `.ptau` per circuit, deploy production verifiers (`isProd=true`), and host artifacts for the SDK."

## References
See `references/README.md` (EncryptedERC `circom/`, `zk/`, README security/setup notes).
