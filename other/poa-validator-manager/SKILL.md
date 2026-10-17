---
name: poa-validator-manager
description: Use when the agent needs to control the validator set of an Avalanche L1 — Proof of Authority, the ValidatorManager contract, adding/removing validators and weights, and multisig (Safe) governance for a permissioned chain.
category: Avalanche L1
difficulty: Advanced
version: "0.1.0"
---

# Proof of Authority & the ValidatorManager

## Overview
A permissioned L1 controls **who validates**. Avalanche does this with the **ValidatorManager contract (VMC)** — a smart contract (typically behind a transparent proxy) that governs the validator set via the P-Chain. With **Proof of Authority (PoA)**, a known, approved set of validators secures the chain; the owner/governance adds or removes them.

## Permissioning models the VMC enables
- **Permissioned Private:** fixed validator set + restricted RPC ([[restrict-rpc-access]]).
- **Permissioned Public (PoA):** controlled validator additions, public RPC.
- **Permissionless (PoS):** anyone validates by staking.

## Lifecycle (PoA)
1. **Create & convert:** create the L1 ([[create-avalanche-l1]]), then convert the Subnet to an L1 so the VMC manages validators.
2. **Deploy the ValidatorManager** (behind a transparent proxy so it's upgradeable).
3. **Set initial configuration** and **initialize the validator set** with your bootstrap validators.
4. **Operate:** add validators, change weights, remove validators, and handle expired registrations / P-Chain disable.

## Validator operations (conceptual)
- **Add validator** — register a NodeID with a weight; completes via P-Chain warp message.
- **Change weight** — adjust a validator's influence.
- **Remove validator** — deregister; or disable on the P-Chain.
- **Query** — read the current validator set and weights.

## Multisig governance (production)
Don't let a single EOA own the validator set. Use a **Safe (multisig)** as the VMC owner and a **PoA Manager** wrapper:
1. Create a Safe wallet with your signer set.
2. Deploy the **PoA Manager**.
3. **Transfer VMC ownership** to the Safe/PoA Manager.
4. All validator changes now require multisig approval.

This is also the recommended home for **AllowList Admin** keys ([[l1-transaction-allowlist]], [[l1-deployer-allowlist]]).

## Common Pitfalls
- **EOA owner.** Single-key ownership of validators/allowlists is a critical risk — use a multisig.
- **Losing quorum.** If too many validators are removed/offline, the chain halts; change weights/sets carefully.
- **Forgetting the proxy.** Deploy the VMC behind a transparent proxy so you can upgrade logic later.
- **Etna/terminology.** Post-Etna L1 conversion is required for VMC-managed validators; older "subnet" guides differ.

## AI Agent Prompt
> "Act as an L1 governance engineer. Deploy a ValidatorManager behind a proxy for a PoA L1, initialize the validator set, then transfer ownership to a Safe multisig + PoA Manager and demonstrate adding a validator via multisig."

## References
See `references/README.md` (academy permissioned-l1s: proof-of-authority, validator-manager-deployment/operations, multisig-setup).
