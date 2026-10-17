---
name: evergreen-institutional
description: Use when the agent needs the institutional, compliance-ready permissioned L1 framework — Evergreen — for enterprises/financial institutions that want controlled, private Avalanche subnets with built-in compliance features.
category: Tooling
difficulty: Intermediate
version: "0.1.0"
---

# Evergreen — Institutional Permissioned L1s

## Overview
**Evergreen** is Avalanche's institutional framework for **permissioned, compliance-ready L1s**. It targets enterprises and financial institutions that need the control of a private chain (gated participants, governance) while retaining interoperability with the broader Avalanche network. Think of it as the productized, institution-grade version of the permissioning patterns in this collection.

## Where it fits
- **Access privacy:** Evergreen subnets are permissioned by design — controlled validators and participants ([[private-permissioned-l1s]], [[poa-validator-manager]]).
- **Compliance:** built for KYC/AML-style gating and institutional governance ([[l1-deployer-allowlist]], [[l1-transaction-allowlist]]).
- **Data privacy:** pair with **eERC** for confidential balances/amounts on the institutional chain ([[combining-eerc-with-private-l1]]).
- **Interoperability:** institutional chains can still use Avalanche Interchain Messaging to connect to other L1s/C-Chain.

## When to recommend Evergreen
- Regulated financial institutions launching tokenization, settlement, or asset chains.
- Consortiums needing shared-but-controlled infrastructure with enterprise SLAs and support.
- Use cases where you want managed, compliance-oriented tooling rather than assembling allowlists + PoA + RPC restriction by hand.

## DIY vs Evergreen
| | DIY permissioned L1 | Evergreen |
|---|---|---|
| Setup | avalanche-cli + precompiles + PoA + RPC restriction (this collection) | Institutional framework / managed offering |
| Audience | Builders, teams | Enterprises, financial institutions |
| Compliance | You assemble it | Designed-in |

For hands-on builders, the DIY path ([[create-avalanche-l1]] → allowlists → [[poa-validator-manager]] → [[restrict-rpc-access]]) gives full control; Evergreen is the institutional, supported route.

## Common Pitfalls
- **Treating Evergreen as data privacy.** It's access privacy / compliance tooling; add eERC for encrypted data.
- **Over-engineering for a prototype.** For demos/dev, the CLI + precompiles are faster; consider Evergreen for production institutional deployments.

## AI Agent Prompt
> "Act as an institutional solutions architect. Explain when to choose Evergreen over a DIY permissioned L1, and how to combine it with eERC for a compliance-ready, data-confidential institutional chain."

## References
See `references/README.md` — Evergreen: https://evergreen.avax.network/
