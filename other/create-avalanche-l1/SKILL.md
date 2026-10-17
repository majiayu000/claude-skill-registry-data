---
name: create-avalanche-l1
description: Use when the agent needs to create and deploy a first Avalanche L1 with the CLI — the blockchain create/deploy flow, genesis configuration (chain ID, gas token, precompiles), and deploying locally then to Fuji.
category: Avalanche L1
difficulty: Intermediate
version: "0.1.0"
---

# Create Your First Avalanche L1

## Overview
Creating an L1 is a two-step CLI flow: **`create`** writes a chain spec (genesis), **`deploy`** launches it. For a *private/permissioned* L1, you enable allowlist precompiles and a permissioned validator manager during `create`.

## Quickstart
```sh
avalanche blockchain create myL1     # interactive config
avalanche blockchain deploy myL1     # Local / Fuji / Mainnet
```

## `create` — key choices
- **VM:** choose **Subnet-EVM** for EVM compatibility.
- **Chain ID:** unique EVM chain ID for your L1.
- **Token symbol / gas token:** your native fee token.
- **Genesis precompiles** (for permissioning — see [[subnet-evm-precompiles]]):
  - **Transaction AllowList** → gate who can submit txs ([[l1-transaction-allowlist]]).
  - **Contract Deployer AllowList** → gate who can deploy ([[l1-deployer-allowlist]]).
  - **Native Minter / Fee Manager / Reward Manager** → tokenomics ([[l1-native-minter-and-fees]]).
- **Initial allowlist admin addresses** for each enabled precompile.

## Genesis breakdown (what `create` produces)
A `genesis.json` containing `config` (chain ID, fee config, and a `*Config` block per enabled precompile with `adminAddresses`/`managerAddresses`/`enabledAddresses` and an `blockTimestamp` activation), plus the initial `alloc` (prefunded accounts). Activating precompiles **at genesis** vs later via upgrade: [[precompile-genesis-and-upgrades]].

## Deploy targets
- **Local:** instant dev network (`avalanche network stop/start` to control). Great for iterating.
- **Fuji:** testnet — needs Fuji AVAX for the deployer ([[fuji-testnet-and-tools]]).
- **Mainnet:** production; consider multisig deploy auth and Evergreen for institutions.

## Permissioned validator set
During/after deploy you convert the Subnet to an L1 and configure the **ValidatorManager** (PoA) so only approved validators join — [[poa-validator-manager]].

## Common Pitfalls
- **Forgetting an allowlist admin.** If you enable an allowlist precompile with no admin, you can't manage roles later (recoverable only via network upgrade).
- **Reusing a public chain ID.** Pick a unique chain ID to avoid wallet/replay confusion.
- **Open RPC on a "private" L1.** Creating with allowlists gates writes, not reads — also restrict RPC ([[restrict-rpc-access]]).

## AI Agent Prompt
> "Act as an Avalanche L1 engineer. Walk me through `avalanche blockchain create` for a permissioned Subnet-EVM L1: chain ID, gas token, enabling the tx + deployer allowlists with admin addresses, then deploy locally and explain the genesis."

## References
See `references/README.md` (academy permissioned-l1s "Create an L1", builders-hub create-avalanche-l1 docs).
