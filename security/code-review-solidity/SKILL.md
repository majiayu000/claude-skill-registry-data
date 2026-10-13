---
name: code-review-solidity
description: >
  Security review of Solidity / EVM smart contracts — reentrancy, access control, arithmetic, and
  DeFi economic bugs. Load when reviewing a smart contract / web3 codebase or PR, on .sol source in
  scope, or "audit this contract". Signals: *.sol, foundry/hardhat, ERC-20/721, external calls,
  delegatecall, proxy patterns, price oracles.
domain: code-review
type: reference
stability: learning
modes: [bugbounty, defense, pentest]
severity: info
cwe: [CWE-841, CWE-284, CWE-682]
tools: [slither, mythril, echidna, foundry]
schema_version: 1
---

# Solidity / smart-contract review

## When it applies
Reviewing on-chain code (a protocol, a token, a bridge). Smart-contract bugs are usually
irreversible and directly financial, so the review bar is high and the classic patterns are
well known — start there, then look for economic/logic flaws unique to the protocol.

## Why it works
The EVM executes exactly as written with real money at stake: an external call can re-enter before
state updates, arithmetic wraps, and a missing modifier means anyone can call a privileged function.
Most losses trace to a small set of patterns a careful read (plus Slither/Mythril) will surface.

## Sinks & patterns (read, then reason about ordering and trust)
- **Reentrancy**: state changed *after* an external call/`.call{value:}`/token callback (ERC-777/721
  hooks). Enforce checks-effects-interactions or a `nonReentrant` guard.
- **Access control**: privileged functions missing `onlyOwner`/role modifiers; `tx.origin` used for
  auth (phishable); unprotected `initialize()` on upgradeable proxies.
- **Arithmetic**: unchecked math (pre-0.8, or inside `unchecked{}`) → over/underflow; precision loss
  from divide-before-multiply; rounding that favors the attacker.
- **Unchecked calls**: ignoring `call`/`send` return values; assuming an external call succeeded.
- **delegatecall**: to attacker-influenced targets → storage/logic hijack; storage-layout mismatch in
  proxies.
- **Oracle / economics**: spot-price from a manipulable AMM (flash-loan price manipulation), missing
  slippage/deadline, MEV/front-running of state-changing txs, first-depositor share inflation.
- **Other**: `selfdestruct`/force-fed ether assumptions, weak randomness (`block.timestamp`/
  `blockhash`), signature replay (missing nonce/chainId in EIP-712), DoS via unbounded loops.

## Method
1. Run `slither` (fast, high-signal) and `mythril`; triage findings.
2. Read every external call and check state-update ordering (reentrancy) and return-value handling.
3. Map roles/modifiers to every state-changing and fund-moving function.
4. Model the economics: how does price/valuation get set, and can a flash loan move it within one tx?
5. Property-test invariants with `echidna`/Foundry fuzzing where feasible.

## Gotchas
- Solidity ≥0.8 checks arithmetic by default — the risk moves into `unchecked{}` blocks and casts.
- A "reentrancy guard" doesn't help cross-function or cross-contract reentrancy — check the whole path.
- Upgradeable proxies add initializer, storage-collision, and `delegatecall` risks absent in plain contracts.

## References
SWC Registry; Slither/Mythril docs; Trail of Bits & OpenZeppelin audit guidance; rekt.news post-mortems.
