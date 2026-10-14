---
name: quillshield
description: "Smart contract security audit skill for the BD pipeline. Analyzes Solana token contracts for red flags: honeypots, rug pull patterns, authority risks, liquidity locks, and holder concentration. Produces a safety score (0-100) to inform listing decisions."
metadata: { "openclaw": { "emoji": "🛡️", "requires": {} } }
---

# QuillShield — Smart Contract Safety Scoring

Analyze Solana token contracts for security risks before recommending them for listing on SolCex Exchange. Produce a safety score from 0-100.

## Safety Score Framework

### Score Ranges

- **80-100**: Safe — low risk, recommend for listing review
- **60-79**: Caution — some risks, needs manual review
- **40-59**: Warning — significant risks, not recommended
- **0-39**: Danger — high risk, reject immediately

### Scoring Criteria (100 points total)

#### 1. Authority Analysis (25 points)

- Mint authority revoked? (+10 if yes, -10 if no)
- Freeze authority revoked? (+10 if yes, -10 if no)
- Update authority status (+5 if revoked/multisig)

#### 2. Liquidity Analysis (25 points)

- Liquidity pool size vs market cap ratio (+10 if >10%)
- Liquidity locked? (+10 if locked >6 months)
- LP token burn status (+5 if burned)

#### 3. Holder Distribution (25 points)

- Top 10 holders concentration (+10 if <30%)
- Creator wallet holdings (+10 if <5%)
- Whale wallet analysis (+5 if no single wallet >10%)

#### 4. Contract Patterns (25 points)

- Trading enabled both ways (buy AND sell)? (+10)
- No excessive tax/fee (>5%)? (+5)
- Contract verified/open source? (+5)
- No suspicious transfer restrictions? (+5)

## Data Sources

Use these APIs to gather contract data:

### DexScreener API

```
GET https://api.dexscreener.com/latest/dex/tokens/{contractAddress}
```

Returns: price, market cap, volume, liquidity, pair info

### Helius API (Solana-specific)

```
POST https://api.helius.xyz/v0/token-metadata?api-key={HELIUS_API_KEY}
Body: { "mintAccounts": ["{contractAddress}"] }
```

Returns: token metadata, authority info, supply data

### Solana FM

```
GET https://api.solana.fm/v0/tokens/{contractAddress}/holders
```

Returns: holder distribution

## Audit Workflow

1. **Input**: Contract address (CA) from prospect pipeline
2. **Fetch**: Pull data from DexScreener + Helius + Solana FM
3. **Analyze**: Score against all 4 criteria categories
4. **Output**: Safety score + risk summary + recommendation

## Output Format

```
🛡️ QuillShield Audit Report
Token: {name} ({symbol})
Contract: {address}
Safety Score: {score}/100 [{SAFE|CAUTION|WARNING|DANGER}]

Authority:    {score}/25 — {summary}
Liquidity:    {score}/25 — {summary}
Distribution: {score}/25 — {summary}
Contract:     {score}/25 — {summary}

Recommendation: {APPROVE for review | MANUAL REVIEW needed | REJECT}
Risk Flags: {list of specific risks found}
```

## Integration with BD Pipeline

- Run QuillShield on every prospect that scores 70+ in the BD pipeline
- Add safety score to prospect metadata before outreach
- Reject prospects with safety score below 40
- Flag prospects with safety score 40-59 for manual review
- Include safety score in listing proposal to SolCex team
