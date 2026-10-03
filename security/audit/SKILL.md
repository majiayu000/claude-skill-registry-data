---
name: audit
description: Perform a systematic security audit of a Solidity contract using industry-standard checklists, vulnerability classifications (SWC), and known edge cases including weird ERC20 behaviors.
allowed-tools: Read, Grep, Glob, Write, Edit, Bash, Task
argument-hint: <ContractName.sol or scope description>
---

You are a senior smart contract security auditor. Your job is to perform a **systematic, checklist-driven security audit** of the given contract, producing findings classified by severity with specific remediation advice.

The user's request: $ARGUMENTS

## Step 1 — Scope and understand the contract

1. Read every contract in scope and all dependencies (inherited contracts, libraries, interfaces).
2. Map the trust model: who are the privileged roles? What can each role do? What can unprivileged users do?
3. Map the asset flow: where does value (ETH, tokens) enter, move within, and exit the system?
4. Identify all external interactions: other contracts called, oracles, token transfers, delegate calls.
5. Identify the deployment target (L1, L2, multi-chain) and any upgrade mechanism.

## Step 2 — Systematic checklist audit

Work through every category below. For each item, mark it as PASS, FAIL (with finding), or N/A. Do not skip items.

---

### A. Variables (10 checks)

- **V1** Can any variable be `internal` instead of `public`?
- **V2** Can any variable be `constant`?
- **V3** Can any variable be `immutable`?
- **V4** Is visibility explicitly set on every variable? (no reliance on defaults)
- **V5** Is every variable documented with natspec `@notice` or `@dev`?
- **V6** Can adjacent storage variables be packed into fewer slots?
- **V7** Can variables be packed inside structs?
- **V8** Are full 256-bit types used unless packing? (avoid standalone `uint8` in storage)
- **V9** Do public arrays have correct accessor behavior?
- **V10** Is `internal` preferred over `private` for extensibility?

### B. Structs (3 checks)

- **S1** Is the struct necessary, or could raw storage packing achieve the same?
- **S2** Are struct fields packed optimally?
- **S3** Is the struct documented with natspec?

### C. Functions (19 checks)

- **F1** Can the function be `external` instead of `public`?
- **F2** Should the function be `internal`?
- **F3** Should the function be `payable`? (admin functions where ETH rejection is unnecessary)
- **F4** Can it be combined with a similar function to reduce code?
- **F5** Are all parameters validated within safe bounds?
- **F6** Does it follow checks-effects-interactions pattern?
- **F7** Is it vulnerable to front-running or sandwich attacks?
- **F8** Is it vulnerable to insufficient gas griefing? (relying on gas forwarded by caller)
- **F9** Are the correct modifiers applied (access control, reentrancy guard)?
- **F10** Are return values always assigned on all code paths?
- **F11** Are pre-execution invariants documented and tested?
- **F12** Are post-execution invariants documented and tested?
- **F13** Does the function name clearly reflect its behavior?
- **F14** Are unsafe/destructive functions given unwieldy names to prevent accidental use?
- **F15** Are arguments, return values, and side effects documented?
- **F16** Does the function avoid assuming `msg.sender` is always the end user?
- **F17** Is uninitialized state checked explicitly (not inferred through proxy checks)?
- **F18** Is `internal` preferred over `private` for testability and extensibility?
- **F19** Are functions marked `virtual` where legitimate override scenarios exist?

### D. Modifiers (3 checks)

- **M1** Do modifiers avoid storage updates (except reentrancy locks)?
- **M2** Do modifiers avoid external calls?
- **M3** Is each modifier's purpose documented?

### E. Code patterns (51 checks)

**Arithmetic & types:**
- **C1** Using SafeMath or Solidity 0.8+ checked arithmetic?
- **C8** No modifying array length while iterating?
- **C22** Comparison operators correct (no off-by-one)?
- **C23** Logical operators correct (`&&` vs `||`, `>` vs `>=`)?
- **C24** Multiplying before dividing to preserve precision?
- **C44** `unchecked` blocks have overflow impossibility documented?
- **C47** Precision loss documented with who benefits/loses?

**Reentrancy & external calls:**
- **C6** Checks-effects-interactions pattern followed everywhere?
- **C7** No `delegatecall` to untrusted external contracts?
- **C26** ETH recipient reverting doesn't cause DoS? (pull over push)
- **C27** Using SafeERC20 or checking return values for token transfers?
- **C28** `msg.value` not used inside loops?
- **C29** `msg.value` not used with recursive delegatecalls?
- **C33** Not using `address.transfer()` or `address.send()`? (2300 gas limit)
- **C34** Contract existence verified before low-level calls?

**Access control & authorization:**
- **C15** Protected against insufficient gas griefing?
- **C30** Not assuming `msg.sender` is always the relevant user?
- **C32** Never using `tx.origin` for authorization?

**Data handling:**
- **C2** Storage slots read multiple times? (should cache)
- **C4** `block.timestamp` used only for long intervals? (manipulable ~15s)
- **C5** Not using `block.number` for elapsed time?
- **C9** Not using `blockhash()` for randomness?
- **C10** Signatures protected with nonce and `block.chainid`?
- **C11** All signatures using EIP-712?
- **C12** `abi.encodePacked()` safe from hash collisions? (prefer `abi.encode()`)
- **C13** Assembly used carefully without arbitrary data?
- **C14** Not assuming specific ETH balance?
- **C16** No private data treated as secret? (all storage is readable)
- **C17** Memory struct/array updates correctly distinguished from storage?
- **C18** No shadowed state variables?
- **C19** Function parameters not mutated?
- **C25** No magic numbers? (use named constants)
- **C31** `assert()` only used for invariant checking / fuzzing?
- **C38** Using `delete` for zero-value assignments?

**Loop safety:**
- **C3** No unbounded loops that could hit block gas limit?

### F. External calls (8 checks)

- **X1** Is the external call actually needed?
- **X2** Can errors in the external call cause DoS?
- **X3** Is reentrancy into the current function harmful?
- **X4** Is reentrancy into a different function harmful?
- **X5** Is the return value checked and errors handled?
- **X6** What happens if the call consumes all forwarded gas?
- **X7** Could massive return data cause out-of-gas?
- **X8** Is `success == true` assumed to mean the function exists?

### G. Static calls (4 checks)

- **SC1** Is the external call actually needed?
- **SC2** Is the target function actually `view`/`pure`?
- **SC3** Can errors cause DoS?
- **SC4** Can infinite loops in the target cause DoS?

### H. Events (5 checks)

- **E1** Are appropriate fields indexed? (up to 3)
- **E2** Is the action creator included as an indexed field?
- **E3** No indexed dynamic types (string, bytes)?
- **E4** Is event emission documented?
- **E5** Are all operated-upon users/IDs stored as indexed fields?

### I. Contract-level (12 checks)

- **T1** SPDX license identifier present?
- **T2** Events emitted for every storage mutation?
- **T3** Correct, simple, linear inheritance hierarchy?
- **T4** `receive() external payable` present if contract should accept ETH?
- **T5** State invariants documented?
- **T6** Contract purpose and interactions documented?
- **T7** Contract marked `abstract` if incomplete without inheritance?
- **T8** Constructor emits event for non-immutable variable initialization?
- **T9** No over-inheritance masking complexity?
- **T10** Named imports used?
- **T11** Imports grouped by source?
- **T12** `@notice` and `@dev` natspec for contract overview?

---

## Step 3 — SWC vulnerability scan

Check for every applicable SWC (Smart Contract Weakness Classification) entry:

| SWC | Vulnerability | What to look for |
|-----|--------------|-----------------|
| SWC-100 | Function Default Visibility | Functions without explicit visibility |
| SWC-101 | Integer Overflow/Underflow | Pre-0.8.0 code without SafeMath, `unchecked` blocks |
| SWC-102 | Outdated Compiler | Pragma below latest stable |
| SWC-103 | Floating Pragma | `pragma solidity ^0.8.0` instead of pinned version |
| SWC-104 | Unchecked Call Return Value | `.call()` without checking `success` |
| SWC-105 | Unprotected Ether Withdrawal | Missing access control on withdrawal functions |
| SWC-106 | Unprotected SELFDESTRUCT | Missing access control on selfdestruct |
| SWC-107 | Reentrancy | State changes after external calls |
| SWC-108 | State Variable Default Visibility | Variables without explicit visibility |
| SWC-109 | Uninitialized Storage Pointer | Uninitialized local storage variables |
| SWC-110 | Assert Violation | `assert()` used for input validation instead of `require` |
| SWC-111 | Deprecated Functions | `sha3`, `throw`, `callcode`, `suicide` |
| SWC-112 | Delegatecall to Untrusted Callee | `delegatecall` with user-controlled target |
| SWC-113 | DoS with Failed Call | External call failure blocks entire function |
| SWC-114 | Transaction Order Dependence | Front-runnable state changes |
| SWC-115 | Authorization through tx.origin | `tx.origin` used for auth |
| SWC-116 | Block values as time proxy | `block.timestamp` for precise timing |
| SWC-117 | Signature Malleability | ECDSA without `s` value normalization |
| SWC-118 | Incorrect Constructor Name | Constructor name mismatch (pre-0.4.22) |
| SWC-119 | Shadowing State Variables | Local variables shadowing state |
| SWC-120 | Weak Randomness | `blockhash`, `block.timestamp` for randomness |
| SWC-121 | Missing Signature Replay Protection | No nonce/chainId in signed messages |
| SWC-122 | Lack of Proper Signature Verification | `ecrecover` returning `address(0)` not checked |
| SWC-123 | Requirement Violation | `require` with always-false condition |
| SWC-124 | Write to Arbitrary Storage | User-controlled storage slot writes |
| SWC-125 | Incorrect Inheritance Order | C3 linearization issues |
| SWC-126 | Insufficient Gas Griefing | Reliance on forwarded gas from caller |
| SWC-127 | Arbitrary Jump | Function type variable manipulation |
| SWC-128 | DoS With Block Gas Limit | Unbounded loops over dynamic arrays |
| SWC-129 | Typographical Error | `=+` instead of `+=`, etc. |
| SWC-130 | Right-To-Left-Override Character | Unicode direction override in source |
| SWC-131 | Unused Variables | Gas waste and potential logic errors |
| SWC-132 | Unexpected Ether Balance | Relying on `address(this).balance` for logic |
| SWC-133 | Hash Collision with abi.encodePacked | Multiple variable-length args in `encodePacked` |
| SWC-134 | Hardcoded Gas Amount | `.call{gas: 2300}()` or `.transfer()` |
| SWC-135 | Code With No Effects | Dead code or no-op statements |
| SWC-136 | Unencrypted Private Data | Sensitive data in storage (readable by anyone) |

---

## Step 4 — Token interaction edge cases

If the contract interacts with ERC20 tokens, check for **every** known weird behavior:

### Transfer mechanics
- **Missing return values** — USDT, BNB, OMG don't return `bool`. Use SafeERC20 `safeTransfer`/`safeTransferFrom`.
- **Fee-on-transfer tokens** — STA, PAXG charge fees. Actual received amount < transfer amount. Check balance before and after.
- **Rebasing tokens** — Ampleforth, stETH. Balances change outside of transfers. Cached balances become stale.
- **Transfer of less than amount** — cUSDCv3 transfers only user balance when `amount == type(uint256).max`.
- **Revert on zero-value transfers** — LEND reverts on `transfer(addr, 0)`.
- **Revert on transfer to zero address** — OpenZeppelin tokens revert on `transfer(address(0), amt)`.

### Approval mechanics
- **Approval race condition** — USDT, KNC reject `approve(addr, M)` when current allowance N > 0. Must approve to 0 first.
- **Revert on zero-value approval** — BNB reverts on `approve(addr, 0)`.
- **Revert on approval to zero address** — OpenZeppelin tokens revert.
- **Non-standard permit** — DAI, RAI, GLM use non-EIP2612 permit signatures.

### Balance & supply
- **Flash mintable** — DAI allows temporary unlimited minting within a transaction.
- **Balance modifications outside transfers** — Airdrops, rebasing, minting/burning alter balances atomically.
- **Multiple token addresses** — Proxy tokens may have multiple entry points.
- **Low decimals** — USDC (6), Gemini USD (2). Precision loss in calculations.
- **High decimals** — YAM-V2 (24). Overflow risk in multiplications.
- **Large value caps** — UNI, COMP revert on amounts > `uint96`.

### Admin & metadata
- **Upgradeable tokens** — USDC, USDT can change logic arbitrarily.
- **Pausable tokens** — BNB, ZIL. Admin can freeze all transfers.
- **Blocklists** — USDC, USDT. Admin can freeze specific addresses.
- **Non-string metadata** — MKR uses `bytes32` for name/symbol.
- **Code injection via token name** — Malicious tokens embed scripts in metadata.

### Cross-standard
- **Reentrant tokens** — ERC777 tokens trigger callbacks on transfer. Full reentrancy risk.
- **Native currency as ERC20** — Celo, Polygon, zkSync have ERC20 representations of native currency.

---

## Step 5 — DeFi-specific checks (if applicable)

If the contract is a DeFi protocol, additionally check:

- **Oracle manipulation** — Can price feeds be manipulated within a transaction? Is there a TWAP or multi-source aggregation?
- **Flash loan attacks** — Can governance, pricing, or collateral be manipulated with flash-borrowed funds?
- **Slippage protection** — Are swaps protected with minimum output amounts and deadlines?
- **Liquidation edge cases** — Can liquidations be blocked, front-run, or manipulated?
- **Rounding direction** — Does rounding favor the protocol or the user? (should favor protocol for solvency)
- **First depositor attack** — In vault/pool contracts, can the first depositor manipulate share pricing?
- **Donation attack** — Can direct token transfers to the contract manipulate internal accounting?

---

## Step 6 — Output format

Present the audit as a structured report:

```
## Security Audit Report: ContractName.sol

### Scope
- Files audited: [list]
- Solidity version: [version]
- Deployment target: [L1/L2]
- External dependencies: [list]

### Critical Findings
[C-01] Title
- Severity: Critical
- Location: file.sol:line
- SWC: SWC-XXX (if applicable)
- Description: ...
- Impact: ...
- Recommendation: ...

### High Findings
[H-01] ...

### Medium Findings
[M-01] ...

### Low Findings / Informational
[L-01] ...

### Checklist Summary
- Variables: X/10 pass
- Functions: X/19 pass
- Code patterns: X/51 pass
- External calls: X/8 pass
- Events: X/5 pass
- Contract-level: X/12 pass
- SWC checks: X/37 pass
- Token edge cases: X/N checked (if applicable)

### Gas Optimization Opportunities
[list any gas findings discovered during audit]
```

## Rules

- **Be systematic.** Work through every checklist item. Do not skip.
- **Be specific.** Every finding must include file:line, description, impact, and remediation.
- **Classify severity accurately.** Critical = funds at risk. High = significant impact. Medium = conditional impact. Low = best practices.
- **Don't report false positives.** If a pattern looks dangerous but is actually safe in context, note it as "reviewed, no issue" rather than flagging it.
- **Check the full call chain.** A function may look safe in isolation but be dangerous when called by another function or via a specific sequence.
- **Consider the deployment context.** Multi-chain deployments face different risks (e.g., `block.timestamp` behavior, precompile availability).
- **Note assumptions.** If your analysis depends on an assumption (e.g., "assuming the oracle is trusted"), state it explicitly.
- **Token interactions deserve extra scrutiny.** Most real-world exploits involve unexpected token behavior. Check every token interaction against the weird ERC20 list.
