---
name: avalanche-starter-kit
description: Use when the agent wants the fastest way to start building on Avalanche — the Avalanche Starter Kit (Hardhat + ready Codespace) for spinning up contracts, L1s, and interchain examples in minutes.
category: Tooling
difficulty: Beginner
version: "0.1.0"
---

# Avalanche Starter Kit

## Overview
The **Avalanche Starter Kit** bundles **Hardhat** with a ready-to-run **GitHub Codespace** (Dev Container) so teams can build on Avalanche without local setup. It's the recommended on-ramp for prototyping eERC tokens, custom L1s, and Interchain Messaging — especially on Windows where the CLI runs best inside a container.

## What's inside
- **Hardhat** project pre-wired for Avalanche networks (local, Fuji, custom L1s).
- **avalanche-cli** available in the container for `blockchain create/deploy`.
- Examples for contracts, deployment, and Interchain Messaging (ICM).
- Dev Container spec → one-click **Codespace**.

## Get started (Codespace)
1. Open the starter kit repo on GitHub.
2. **Code → Codespaces → Create codespace on main**.
3. In the container terminal, compile/deploy with Hardhat or scaffold an L1 with `avalanche blockchain create`.

## Get started (local)
- Install the **Dev Containers** VS Code extension + Docker, then "Reopen in Container".
- Or clone and run Hardhat directly if you only need contracts (Node + npm).

## How it fits these skills
- Use it as the environment for [[eerc-deploy-contracts]] / [[eerc-deploy-fuji]] and [[create-avalanche-l1]].
- Fund test accounts via [[fuji-testnet-and-tools]].

## Common Pitfalls
- **Windows native tooling.** Prefer the Codespace/Dev Container; `avalanche-cli` doesn't run natively on Windows ([[avalanche-cli-setup]]).
- **Codespace timeouts.** Long proof builds (eERC circuits) may need a larger machine type.

## AI Agent Prompt
> "Act as a DX engineer. Get me productive on Avalanche in minutes using the Starter Kit Codespace: open the container, compile a contract with Hardhat, and deploy a sample to Fuji."

## References
See `references/README.md` (academy multi-chain-architecture 'Avalanche Starter Kit', builders-hub).
