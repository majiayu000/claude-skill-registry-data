---
name: confidential-payments-patterns
description: Use when the agent needs concrete confidential use-case blueprints built on eERC — private payroll, B2B settlement, confidential treasury, OTC/escrow — including which mode and which privacy controls each needs.
category: Privacy Deep-Dive
difficulty: Intermediate
version: "0.2.0"
---

# Confidential Payments Patterns

## Overview
Reusable blueprints for real confidential-payment use cases on eERC. Each maps to a deployment mode ([[eerc-deployment-modes]]) and a privacy posture ([[eerc-privacy-threat-model]]).

## Pattern 1 — Private payroll
- **Goal:** salaries hidden from the public and from other employees.
- **Mode:** Standalone (hidden supply) or Converter (pay out an existing stablecoin).
- **Flow:** employer `privateMint`/`deposit` → `privateTransfer` to each registered employee. Employees decrypt their own balance.
- **Controls:** auditor key for payroll/tax compliance ([[selective-disclosure-and-compliance]]); fresh per-employee addresses; consider a private L1 to hide who's on payroll ([[combining-eerc-with-private-l1]]).

## Pattern 2 — B2B settlement / invoicing
- **Goal:** settle invoices confidentially with a reference.
- **Mode:** Converter (settle in a wrapped stablecoin).
- **Flow:** `deposit` → `privateTransfer` with an **encrypted invoice reference** ([[eerc-encrypted-metadata]]) → counterparty `withdraw`.
- **Controls:** normalize on/off-ramp amounts (converter boundary leaks) ([[eerc-privacy-threat-model]]); auditor for reconciliation.

## Pattern 3 — Confidential treasury
- **Goal:** an org holds/moves funds without revealing balances or moves.
- **Mode:** Standalone for max opacity (hidden total supply, [[eerc-hidden-supply]]).
- **Controls:** multisig owner; auditor for internal audit; ideally on a permissioned L1.

## Pattern 4 — OTC / escrow
- **Goal:** large transfers without revealing size to the market.
- **Mode:** Standalone or Converter.
- **Flow:** confidential `privateTransfer`; for atomicity use contract logic around eERC operations.
- **Controls:** timing/amount obfuscation; private RPC to avoid mempool/IP leakage ([[anonymity-network-privacy]]).

## Choosing controls per pattern
| Pattern | Mode | Auditor | Private L1? | Metadata |
|---|---|---|---|---|
| Payroll | Standalone/Converter | yes | recommended | optional |
| B2B settlement | Converter | yes | optional | yes (invoice ref) |
| Treasury | Standalone | yes | recommended | optional |
| OTC/escrow | either | optional | optional | optional |

## Common Pitfalls
- **Converter on/off-ramp leakage** for amounts — normalize/batch.
- **Reused addresses** linking payments across patterns.
- **No auditor** where regulation requires one.

## AI Agent Prompt
> "Act as a solutions engineer. Implement <payroll|B2B settlement|treasury|OTC> on eERC: pick the mode, wire register → fund → private transfer (+ encrypted reference if needed), and apply the right privacy controls (auditor, private L1, amount normalization)."

## References
See `references/README.md` (eERC use-cases academy, encrypted-balance + metadata skills).
