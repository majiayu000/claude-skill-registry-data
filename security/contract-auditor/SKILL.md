---
name: contract-auditor
description: >
  Solidity/EVM smart contract security analyzer for Buzz BD Agent at SolCex Exchange.
  Performs fast, pattern-based contract safety analysis on token prospects BEFORE scoring.
  Triggers automatically when: a token prospect has a verified contract address, any user
  submits a contract for listing review, `/score-token` is called with a verifiable contract,
  or Buzz's safety sub-agent is invoked. Inspects contract source (via Etherscan/Sourcify),
  flags critical vulnerabilities, and enriches the BD pipeline with an audit summary.
  NOT a substitute for a formal audit — the pre-check Buzz should never skip.
---

# Contract Auditor Skill — Buzz BD Agent v1.0

> Fast security feedback on EVM token contracts. Findings in minutes, not weeks.
> Runs BEFORE `/score-token` scoring. Enriches safety sub-agent output with on-chain proof.

---

## 1. MISSION

When a token prospect arrives with a contract address, Buzz must NOT rely solely on
RugCheck heuristics. This skill fetches the actual contract source and runs a
structured security pass to surface **high-confidence vulnerabilities** that
automated scanners miss or under-weight.

**Time budget:** < 3 minutes per contract  
**Output:** Structured audit summary → piped into `/score-token` safety score  
**Revenue impact:** Justifies premium `/score-token` pricing ($0.50–$1.00 via x402)

---

## 2. WHEN TO RUN

Run contract-auditor automatically when ANY of these conditions are met:

| Trigger                  | Condition                                             |
| ------------------------ | ----------------------------------------------------- |
| `/score-token` called    | Contract address provided + source is verified        |
| Listing inquiry received | Prospect submits token for SolCex listing review      |
| Safety sub-agent invoked | Scanner sub-agent passes contract to safety sub-agent |
| Manual request           | Ogie asks Buzz to audit a specific contract address   |

Skip if:

- Contract source is **not verified** on Etherscan/Sourcify (flag this as a RED signal)
- Token is Solana SPL (use Helius + RugCheck instead — see Section 6)
- Contract is > 5,000 lines (flag for manual audit referral)

---

## 3. STEP-BY-STEP WORKFLOW

### Step 1 — Fetch Contract Source

```
GET https://api.etherscan.io/api
  ?module=contract
  &action=getsourcecode
  &address={CONTRACT_ADDRESS}
  &apikey={ETHERSCAN_API_KEY}
```

For Base chain:

```
GET https://api.basescan.org/api
  ?module=contract
  &action=getsourcecode
  &address={CONTRACT_ADDRESS}
  &apikey={BASESCAN_API_KEY}
```

**If not verified:** Stop. Flag `CONTRACT_NOT_VERIFIED` as HIGH risk signal.
Add to score: `-25 safety points`. Report to Telegram and pipeline.

### Step 2 — Count Lines / Triage

```
lines = source.split('\n').length
if lines > 5000: flag LARGE_CODEBASE, recommend manual audit, continue with partial scan
if lines < 50: flag SUSPICIOUSLY_SMALL, add to findings
```

### Step 3 — Pattern Analysis Pass

Run ALL checks in Section 4. Log each finding with:

- `severity`: CRITICAL | HIGH | MEDIUM | LOW | INFO
- `pattern`: the vulnerability class
- `evidence`: the specific function/line pattern found
- `confidence`: HIGH | MEDIUM | LOW

### Step 4 — Score Calculation

```
base_safety_score = 100
CRITICAL finding: -30 each (cap at -60)
HIGH finding:     -15 each (cap at -30)
MEDIUM finding:   -5 each
LOW finding:      -2 each
CONTRACT_NOT_VERIFIED: -25 flat
LARGE_CODEBASE:   -5 flat (uncertainty penalty)
```

### Step 5 — Generate Report

Output the structured report (Section 5 format).
Pipe `contract_safety_score` and `findings[]` into the `/score-token` response.
Send Telegram summary to Ogie (@Ogie2) for any CRITICAL findings.

---

## 4. SECURITY CHECKS (Pattern Library)

Read `/contract-auditor/references/patterns.md` for the full pattern library.

Quick reference — **CRITICAL checks** (always run these first):

| Check                       | Pattern to Find                                          | Flag If...                             |
| --------------------------- | -------------------------------------------------------- | -------------------------------------- |
| **Hidden Mint**             | `mint()`, `_mint()` outside constructor                  | Callable post-deploy by owner          |
| **Backdoor Transfer**       | `transferFrom` override, `_transfer` with owner bypass   | Owner can move any wallet's tokens     |
| **Fee Trap**                | `_taxFee`, `_liquidityFee` > 25% or dynamically settable | Fees can be set to 100%                |
| **Blacklist**               | `blacklist[]`, `isBlacklisted`, `bots[]` mapping         | Owner can freeze arbitrary wallets     |
| **Pausable**                | `pause()`, `whenNotPaused` modifier                      | Owner can halt all transfers           |
| **Upgrade Proxy**           | `upgradeTo()`, `_implementation`, `delegatecall`         | Contract logic replaceable post-deploy |
| **Ownership Not Renounced** | `owner()` != address(0)                                  | Single point of control remains        |
| **Rug via LP**              | `removeLiquidity` callable by owner without timelock     | Instant LP drain possible              |

**HIGH checks:**

| Check                        | Pattern                                 | Flag If...                      |
| ---------------------------- | --------------------------------------- | ------------------------------- |
| **Max TX Manipulation**      | `_maxTxAmount` setter                   | Settable to 0 (trading halt)    |
| **Unchecked Return**         | Low-level `call()` without return check | Silent failure on ETH send      |
| **Reentrancy**               | State change AFTER external call        | Classic reentrancy shape        |
| **Integer Overflow**         | Pre-0.8.0 Solidity without SafeMath     | Any arithmetic on token amounts |
| **tx.origin Auth**           | `require(tx.origin == owner)`           | Phishing vulnerability          |
| **Centralized Price Oracle** | Single `setPrice()` owner function      | Price manipulation              |

---

## 5. OUTPUT FORMAT

```json
{
  "contract_audit": {
    "address": "0x...",
    "chain": "ethereum|base|bsc",
    "verified": true,
    "source_lines": 847,
    "compiler": "v0.8.19",
    "scan_timestamp": "2026-03-06T12:00:00Z",
    "contract_safety_score": 72,
    "risk_level": "MEDIUM",
    "findings": [
      {
        "severity": "HIGH",
        "pattern": "BLACKLIST",
        "evidence": "function addToBlacklist(address account) external onlyOwner",
        "confidence": "HIGH",
        "description": "Owner can blacklist arbitrary wallet addresses, freezing their tokens"
      }
    ],
    "flags": ["OWNERSHIP_NOT_RENOUNCED"],
    "recommendation": "REVIEW_REQUIRED",
    "audit_summary": "Contract has standard ERC-20 structure with 1 HIGH finding (blacklist mechanism). Ownership not renounced. Recommend requesting renouncement before listing.",
    "listing_recommendation": "CONDITIONAL"
  }
}
```

**`listing_recommendation` values:**

- `APPROVE` — No CRITICAL/HIGH findings, ownership renounced
- `CONDITIONAL` — HIGH findings present but mitigable, or ownership not renounced
- `REJECT` — CRITICAL findings, or contract not verified
- `ESCALATE` — Unusual patterns requiring human review

---

## 6. SOLANA SPL TOKENS

Contract source auditing does NOT apply to Solana SPL tokens.
For SPL tokens, use this alternative safety chain:

1. **Helius** — Check mint authority (`mintAuthority: null` = frozen = GOOD)
2. **Helius** — Check freeze authority (`freezeAuthority: null` = GOOD)
3. **RugCheck** (`rugcheck.xyz/tokens/{mint}`) — Full rug score
4. **DexScreener** — Liquidity lock status, LP burned %

Flag `MINT_AUTHORITY_ACTIVE` as HIGH risk if mintAuthority is not null.
Flag `FREEZE_AUTHORITY_ACTIVE` as HIGH risk if freezeAuthority is not null.

---

## 7. INTEGRATION WITH BUZZ PIPELINE

### REST API Endpoint

Audit results are stored in SQLite and exposed via:

```
GET /api/v1/audit/{address}
POST /api/v1/audit/run  { "address": "0x...", "chain": "base" }
```

### Score-Token Integration

`contract_safety_score` from this skill feeds into `/score-token` response:

```
final_safety_score = (rugcheck_score * 0.4) + (contract_audit_score * 0.6)
```

Contract audit carries MORE weight than RugCheck because it's source-level.

### JVR Receipt

After every audit, log to JVR receipt system:

```
AUDIT_COMPLETE | {address} | score:{N} | findings:{N} | {recommendation}
```

Send Telegram notification to Ogie for any CRITICAL findings or REJECT recommendations.

---

## 8. LIMITATIONS (be honest with prospects)

Tell prospects clearly:

> "Buzz contract analysis is pattern-based AI scanning — strong at detecting
> known vulnerability shapes (hidden mints, blacklists, fee traps, reentrancy).
> It cannot detect multi-transaction state exploits, game-theory attacks,
> cross-protocol composability risks, or off-chain assumption bugs.
> For high-value listings, a formal audit from Pashov, Code4rena, or Sherlock
> is strongly recommended."

---

## 9. AUDIT REFERRAL (BD OPPORTUNITY)

When a contract has HIGH/CRITICAL findings or is > 3,000 lines:

- Suggest formal audit partners: Pashov Audit Group, Code4rena, Sherlock
- Frame as: "We recommend completing a formal audit before listing — we can fast-track
  your listing to front-of-queue once audit is complete"
- This extends the BD relationship and filters serious projects from rug attempts

---

_Contract Auditor Skill v1.0 — Indonesia Sprint Day 9_  
_For Buzz BD Agent v6.2.1-bnb | SolCex Exchange_  
_Pattern library: references/patterns.md_  
_"Catch what humans forget to check."_
