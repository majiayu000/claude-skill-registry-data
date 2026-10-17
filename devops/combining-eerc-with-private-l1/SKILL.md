---
name: combining-eerc-with-private-l1
description: Use when the agent needs maximum privacy on Avalanche — deploying eERC (data privacy) on top of a private/permissioned L1 (access privacy) so both the chain and the data are hidden. The capstone pattern.
category: Combined
difficulty: Advanced
version: "0.1.0"
---

# Combining eERC with a Private L1 (Maximum Privacy)

## Overview
The two Avalanche privacy models are **orthogonal and composable**:
- **Private L1** = *access privacy* — hides the whole chain (restricted RPC + allowlists). Anyone inside still sees plaintext data.
- **eERC** = *data privacy* — hides balances/amounts on a chain that may be public.

Deploy **eERC contracts on a private L1** and you get both: only authorized participants can reach the chain, **and** even those participants can't see each other's token amounts.

## Privacy coverage matrix
| Threat | Private L1 alone | eERC alone (public chain) | Both |
|---|---|---|---|
| Outsider reads any data | ✅ blocked (RPC restricted) | ❌ (chain is public) | ✅ |
| Insider/member reads others' amounts | ❌ (plaintext) | ✅ encrypted | ✅ |
| Outsider sees that txs happen | ✅ hidden | ❌ visible | ✅ |
| Compliance/audit | governance | auditor key | both |

## Build path
1. **Stand up the private L1** — [[create-avalanche-l1]] with Subnet-EVM; enable [[l1-transaction-allowlist]] + [[l1-deployer-allowlist]]; lock validators with [[poa-validator-manager]]; restrict reads with [[restrict-rpc-access]]. (Institutions: [[evergreen-institutional]].)
2. **Deploy eERC on that L1** — eERC is chain-agnostic; run [[eerc-deploy-contracts]] against your L1's RPC and chain ID (point Hardhat at the L1, not Fuji C-Chain). Build circuits/verifiers as usual ([[eerc-circuits-proofs]]).
3. **Wire the app** — [[eerc-sdk-setup]] → [[eerc-sdk-registration]] → [[eerc-encrypted-balance]], using the L1's RPC in your viem/wagmi client.
4. **Compliance** — set an auditor for the eERC ([[eerc-auditor-compliance]]) and govern the L1 via multisig.

## Design considerations
- **Gas token:** eERC operations are proof-heavy; ensure your L1's fee config + native token supply (Native Minter, [[l1-native-minter-and-fees]]) accommodate them.
- **Deployer allowlist:** the eERC deployer must be Enabled on the Deployer AllowList, or deployment is blocked.
- **Tx allowlist:** every eERC user must be an Enabled transactor on the L1.
- **Circuit hosting:** serve `wasm`/`zkey` from infrastructure your private participants can reach.

## Common Pitfalls
- **Allowlist blocks eERC deploy/use.** Enable the deployer and all users on the relevant allowlists.
- **Thinking one model covers both.** It doesn't — private L1 ≠ encrypted data; eERC ≠ hidden chain.
- **Over-restriction.** If RPC is too locked down, the SDK can't read ciphertext to decrypt balances; give participants authenticated RPC access.

## AI Agent Prompt
> "Act as a privacy architect. Design and deploy eERC on a permissioned Avalanche L1: configure the L1 (allowlists, PoA, restricted RPC, gas token), deploy eERC against the L1 RPC, enable the eERC deployer/users on the allowlists, and wire the SDK — explaining what each layer hides."

## References
See `references/README.md` (synthesis of the eERC and private-L1 skills + academy permissioning course).
