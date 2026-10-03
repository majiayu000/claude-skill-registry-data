---
name: smart-contract-audit
description: Smart contract and Web3 security audit skill for Solidity, Vyper, Move, and Cairo. Covers reentrancy, access control, oracle manipulation, MEV/sandwich exposure, signature replay, upgrade safety, ERC token edge cases, bridge risk, and DeFi invariants. Tooling includes Slither, Mythril, Echidna, Foundry, Halmo, Certora, and custom invariant tests. Use for design review, code audit, and incident analysis on contracts you own or are authorized to assess.
---

# Smart Contract Audit

## Authorization Boundary

- Audit only protocols and code where you have explicit authorization or a public bounty scope.
- Treat private keys and seed phrases as untouchable; never request, store, or use them.
- Distinguish lab/testnet from mainnet; never simulate exploits against live user funds.

## Audit Workflow

1. Architecture: contract map, upgrade pattern, proxy admin, roles, external calls, oracles, AMMs, bridges, governance.
2. Threat model: trust assumptions, economic invariants, privileged actors, off-chain dependencies, MEV exposure.
3. Static and semantic: `slither`, `aderyn`, `semgrep`, `mythril`, Solidity compiler warnings; review storage layout for upgradeable contracts.
4. Property tests: write invariants in Foundry/Echidna/Halmo; fuzz with state-machine harnesses; run differential tests vs reference.
5. Manual review: reentrancy (CEI), unchecked external calls, signature replay, frontrunning, slippage, rounding, oracle freshness/TWAP, ERC-20 fee-on-transfer and rebasing edge cases, ERC-721/1155 callbacks.
6. Economic: invariant set on liquidity, fees, debt, collateral; simulate MEV (`mev-share`, `cannon`, `tenderly`).
7. Report: severity, likelihood, impact, fix, regression test.

## High-Risk Patterns Checklist

- Upgrade safety: storage gaps, initializer guards, admin keys, timelocks.
- Bridge messages: replay protection, finality, message origin validation.
- Oracles: single-source, manipulable spot price, missing staleness checks.
- Governance: flash-loan-driven votes, quorum manipulation, proposal hijack.
- Token assumptions: non-standard ERC-20 (USDT-style, rebasing, fee-on-transfer, blocklist).

## Output Contract

- `scope.md`, `architecture.md`, `threat-model.md`.
- `findings/<id>.md`: severity, code refs, PoC, fix, test.
- `invariants/`: Foundry/Echidna harnesses.
- `report.pdf` or `report.md`: exec summary, findings, appendices, remediation status matrix.
