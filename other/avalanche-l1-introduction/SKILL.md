---
name: avalanche-l1-introduction
description: Use when the agent needs the fundamentals of Avalanche L1s (formerly Subnets) — sovereign chains, custom gas tokens, custom validator sets, and stateful precompiles — before building a private or permissioned chain.
category: Avalanche L1
difficulty: Beginner
version: "0.1.0"
---

# Avalanche L1s — Introduction

## Overview
An **Avalanche L1** (formerly "Subnet") is a **sovereign blockchain** with its own validator set and rules, secured by its own validators and coordinated via Avalanche's P-Chain. Unlike a smart contract on a shared chain, an L1 lets you control the chain itself — which makes it the foundation for **access privacy** ([[private-permissioned-l1s]]).

## What you control on an L1
- **Virtual machine** — most teams use **Subnet-EVM** (an EVM fork) for full Solidity/EVM compatibility ([[subnet-evm-precompiles]]).
- **Custom gas token** — pay fees in your own native token, not AVAX.
- **Validator set** — who validates (fixed/permissioned PoA, or open PoS) via the **ValidatorManager** ([[poa-validator-manager]]).
- **Stateful precompiles** — built-in, genesis-configurable modules for allowlisting, minting, fees, and rewards ([[subnet-evm-precompiles]]).
- **Fee configuration & rewards** — gas limits, base fee dynamics, reward routing.
- **RPC exposure** — public, or restricted to authorized nodes ([[restrict-rpc-access]]).

## Why an L1 for privacy
- **Access privacy / walled garden** — restrict who can connect, read, deploy, and transact.
- **Performance & sovereignty** — dedicated throughput, no noisy neighbors.
- **Compliance** — gate participants (KYC) at the protocol level; institutional framework via [[evergreen-institutional]].

## Build path
1. Install the CLI → [[avalanche-cli-setup]].
2. Create & deploy an L1 → [[create-avalanche-l1]].
3. Add permissioning precompiles → [[l1-transaction-allowlist]], [[l1-deployer-allowlist]].
4. Configure tokenomics → [[l1-native-minter-and-fees]].
5. Lock the validator set → [[poa-validator-manager]]; restrict RPC → [[restrict-rpc-access]].

## Common Pitfalls
- **"L1 = private by default."** No — an L1 is sovereign but, by default, data is plaintext and RPC may be open. Privacy comes from precompiles + RPC restriction (and/or eERC for data).
- **Subnet vs L1 terminology.** Post-Etna, "Subnet" is now "L1"; older docs/CLI flags may still say "subnet".

## AI Agent Prompt
> "Act as an Avalanche L1 architect. Explain what a sovereign Avalanche L1 gives me (VM, gas token, validators, precompiles) and outline the steps to launch a permissioned one."

## References
See `references/README.md` (builders-hub `docs/avalanche-l1s`, academy avalanche-fundamentals).
