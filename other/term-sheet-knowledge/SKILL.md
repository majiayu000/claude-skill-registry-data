---
name: term-sheet-knowledge
description: >
  Term sheet key terms, SAFE/convertible note structures, cap table dilution calculations, red flags.
  Triggers on "review term sheet", "explain SAFE", "calculate cap table", "investment terms", "valuation vs dilution",
  "텀시트 리뷰", "SAFE 설명", "캡테이블 계산", "투자 조건", "밸류에이션 vs 희석".
---

# Term Sheet Knowledge

**⚠️ Disclaimer**: This skill explains term sheet terminology for educational purposes. It does not provide legal advice. All investment agreements must be reviewed by a startup-focused lawyer.

Term sheet key conditions, SAFE/convertible note structures, cap table dilution calculations, negotiation strategy, and red flags.

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                  TERM SHEET KNOWLEDGE                            │
├─────────────────────────────────────────────────────────────────┤
│  Information Provided                                           │
│  ✓ Term sheet key terms explained (15 critical items)          │
│  ✓ SAFE vs convertible note vs Equity comparison               │
│  ✓ Cap table dilution calculations (round-by-round simulation) │
│  ✓ Negotiation points & priorities                             │
│  ✓ Red Flags (conditions to avoid)                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Term Sheet Key Terms

### 1. Valuation

**Pre-money vs Post-money**

```
Pre-money: Company value before investment
Post-money: Company value after investment

Post-money = Pre-money + Investment amount

Example:
- Pre-money: $8M
- Investment: $2M
- Post-money: $10M
- Investor stake: $2M / $10M = 20%
```

**Negotiation Points:**
- Higher pre-money → Lower dilution
- But risks "down round" in next round
- Fair valuation > Inflated valuation

---

### 2. Investment Amount & Dilution

```
Investor stake (%) = Investment amount / Post-money valuation

Example:
- Pre-money: $8M
- Investment: $2M
- Post-money: $10M
- Dilution: 20%

Founder's existing stake 80% → After investment 64% (80% × 80%)
```

**Dilution Benchmarks:**
- Pre-seed: 10-20%
- Seed: 15-25%
- Series A: 20-30%
- Series B: 15-25%

**Red Flag:**
- Single round dilution > 30%
- Cumulative dilution leaves founder < 50% stake (pre-Series A)

---

### 3. Liquidation Preference

**Definition:** Amount investor recovers first at exit

**Types:**

**1x Non-Participating**
```
Exit $20M, Investment $2M (20% stake):
- Investor chooses:
  Option A: $2M (1x preference)
  Option B: $4M (20% stake)
→ Investor: chooses $4M
→ Founders: $16M
```

**1x Participating**
```
Exit $20M, Investment $2M (20% stake):
- Investor:
  Step 1: $2M (1x preference)
  Step 2: ($20M - $2M) × 20% = $3.6M
→ Investor: $5.6M
→ Founders: $14.4M
```

**2x Non-Participating**
```
Exit $20M, Investment $2M (20% stake):
- Investor chooses:
  Option A: $4M (2x preference)
  Option B: $4M (20% stake)
→ Investor: $4M
→ Founders: $16M
```

**Red Flag:**
- Participating (double-dipping)
- 2x or higher multiple
- Participating in Seed/Series A is abnormal

**Negotiation:**
- 1x non-participating is standard
- Strongly oppose if participating
- Set cap (e.g., 1x participating with 2x cap)

---

### 4. Anti-Dilution Protection

**Definition:** Protects investor in down rounds

**Types:**

**Full Ratchet (Most Harmful)**
```
Original: $10M valuation, $1/share, 1M shares
Down round: $5M valuation, $0.50/share

Full Ratchet → Investor shares adjusted to $0.50
→ Investor shares double, founders heavily diluted
```

**Weighted Average (Standard)**
```
Broad-based: Based on all issued shares (founder-friendly)
Narrow-based: Based on preferred shares only (investor-friendly)

Broad-based is industry standard
```

**Red Flag:**
- Full Ratchet (must avoid)
- Narrow-based (try to avoid)

**Negotiation:**
- Demand broad-based weighted average
- Pre-seed/Seed can sometimes avoid entirely

---

### 5. Board Composition

**Typical Structure:**

**Seed:**
```
Total: 3 seats
- Founders: 2 seats
- Investor: 1 seat
```

**Series A:**
```
Total: 5 seats
- Founders: 2 seats
- Investors: 2 seats (Seed 1 + Series A 1)
- Independent: 1 seat (mutual agreement)
```

**Series B:**
```
Total: 7 seats
- Founders: 2 seats
- Investors: 3 seats
- Independent: 2 seats
```

**Red Flag:**
- Investor majority (founders lose control)
- Independent director selection power only with investor

**Negotiation:**
- Founders + Independent ≥ Investors
- Independent director selection by mutual consent

---

### 6. Protective Provisions

**Definition:** Requires investor consent for certain actions

**Standard Items:**
- New fundraising
- M&A, liquidation
- Charter amendments
- Adding board members
- Changing preferred stock terms

**Red Flag:**
- Excessive items (e.g., executive hiring, budget approval)
- Single investor veto power

**Negotiation:**
- Define "Major Investor" threshold (e.g., 10%+ stake)
- Require majority preferred shareholder consent (not single investor)

---

### 7. Conversion Rights

**Definition:** Preferred to common stock conversion

**Automatic Conversion:**
```
Converts automatically at IPO
Conditions:
- IPO price > $X (e.g., $50M valuation)
- Raise > $Y (e.g., $10M)
```

**Optional Conversion:**
Investor can choose to convert anytime

**Red Flag:**
- Automatic conversion conditions too high
- Only investor can optionally convert (not founders)

---

### 8. Redemption Rights

**Definition:** Investor can force company to buy back shares

**Red Flag:**
- Redemption rights in Seed/Series A (abnormal)
- Redemption timing too soon (e.g., 3 years)

**Negotiation:**
- Demand redemption rights removal
- Minimum 5+ year period if required

---

### 9. Dividends

**Types:**

**Cumulative:**
```
X% accrues annually, paid at exit
→ Effective interest (investor-favorable)
```

**Non-Cumulative:**
```
Paid only if board decides
→ Rarely paid in startups
```

**Red Flag:**
- Cumulative dividends (must avoid)
- Dividend rate > 8%

**Negotiation:**
- Remove dividends or non-cumulative only

---

### 10. Founder Vesting

**Standard Structure:**
```
4-year vesting, 1-year cliff

Example:
- Year 0: 0%
- Year 1 (Cliff): 25%
- Year 2: 50%
- Year 3: 75%
- Year 4: 100%

Monthly vesting (after Year 1): 1/48 each month
```

**Single Trigger vs Double Trigger:**

**Single Trigger:**
```
M&A triggers immediate 100% vesting
→ Founder-friendly
```

**Double Trigger:**
```
M&A + Termination → 100% vesting
→ Acquirer-friendly (can retain founder)
```

**Negotiation:**
- Demand single trigger (early rounds)
- Accept double trigger (later rounds)
- Acceleration amount (50% vs 100%)

---

### 11. Right of First Refusal & Co-Sale

**Right of First Refusal (ROFR):**
```
Investor gets first chance when founder wants to sell shares
→ Standard provision, acceptable
```

**Co-Sale / Tag-Along:**
```
When founder sells shares, investor can sell under same terms
→ Standard provision
```

**Drag-Along:**
```
If investor majority approves, all shareholders forced to sell
→ Facilitates M&A
→ Standard provision, acceptable
```

---

### 12. Pro-Rata Rights

**Definition:** Right to participate in next round to maintain stake

**Negotiation:**
- Grant only to Major Investors
- Limit over-allotment

---

### 13. Information Rights

**Standard:**
- Monthly financial statements
- Annual audited financials
- Annual budget
- Board materials (observer rights)

**Red Flag:**
- Excessive reporting (e.g., weekly reports)
- Sensitive information to potential competitors

---

### 14. Expense Reimbursement (No-Shop & Expenses)

**No-Shop:**
```
30-60 days after term sheet, cannot negotiate with other investors
→ Standard provision, acceptable
```

**Expenses:**
```
Company pays investor's legal fees
→ Set cap ($10K-$25K)
```

---

### 15. Employee Option Pool

**Pre-money vs Post-money:**

**Pre-money Pool (Investor-favorable):**
```
Pre-money: $8M
Option pool: 15% (pre-money basis)
→ Option pool dilutes only founders

Actual calculation:
- Founders: 80% × (1 - 15%) = 68%
- Option pool: 15%
- Investor: 20% (post-money basis)
→ Only founders diluted
```

**Post-money Pool (Founder-favorable):**
```
Post-money: $10M
Option pool: 15% (post-money basis)
→ Founders and investors both diluted
```

**Negotiation:**
- Demand post-money option pool
- Keep to what's needed (avoid excessive pool)

---

## SAFE (Simple Agreement for Future Equity)

### SAFE Structure

**Basic Principle:**
```
Current investment → Converts to equity in next equity round
No valuation now (avoids current negotiation)
```

**4 Types:**

**1. Valuation Cap (Most Common)**
```
Cap: $5M
Next round: $10M pre-money
→ SAFE investor converts at $5M basis (2x favorable)
```

**2. Discount (Standalone or Cap + Discount)**
```
Discount: 20%
Next round: $1/share
→ SAFE investor converts at $0.80/share
```

**3. Valuation Cap + Discount**
```
Choose whichever is more favorable
```

**4. MFN (Most Favored Nation)**
```
Not worse than next SAFE
→ Protects early investor
```

### SAFE Dilution Calculation

```
Example:
- SAFE investment: $500K, Cap $5M
- Series A: $2M at $10M pre-money

SAFE conversion:
- SAFE Cap $5M basis → 10% stake ($500K / $5M)
- Series A $10M pre-money basis → 20% ($2M / $10M)

Post-money:
- $10M + $2M + SAFE dilution adjustment = $12M+
- Founders: ~66%
- SAFE: ~10%
- Series A: ~20%
- Option pool: ~4%
```

### SAFE vs Equity

| Item | SAFE | Equity |
|------|------|--------|
| Valuation | Pending (cap only) | Confirmed |
| Negotiation | Simple (2 weeks) | Complex (2 months) |
| Cost | Low ($2K) | High ($20K+) |
| Investor Rights | None | Board, protective provisions |
| Conversion | Next round | Immediate |
| Best Stage | Pre-seed | Seed+ |

**SAFE Advantages:**
- Fast, inexpensive
- Defers valuation negotiation
- Standard document (YC SAFE)

**SAFE Disadvantages:**
- Complex cap table (multiple SAFEs overlap)
- Dilution uncertain until next round
- No investor rights (board, information)

---

## Convertible Note

### Structure

```
Debt → Converts to equity in next round

Key terms:
- Principal
- Interest Rate: 5-8%
- Maturity: 18-24 months
- Conversion Discount: 15-25%
- Valuation Cap: Optional
```

### SAFE vs Convertible Note

| Item | SAFE | Convertible Note |
|------|------|------------------|
| Legal Form | Contract | Debt/Bond |
| Interest | None | 5-8% |
| Maturity | None | 18-24 months |
| Repayment Obligation | None | Must repay or convert at maturity |
| Complexity | Low | Medium |

**Regional Preference:**
- USA: Prefers SAFE (simpler)
- Korea/Asia: Prefers convertible notes (legally established)

---

## Cap Table & Dilution Calculations

### Initial Cap Table

```
Founding:
- Founder A: 60% (6M shares)
- Founder B: 40% (4M shares)
Total: 10M shares (Fully Diluted)
```

### Pre-seed (SAFE)

```
SAFE investment: $500K at $5M Cap

Assumption: Converts at Series A
Cap table unchanged for now
```

### Seed Round

```
Investment: $2M at $8M pre-money
Option pool: 10% (pre-money)
Post-money: $10M

Dilution calculation:
1. Create option pool (pre-money)
   - Existing: 10M shares
   - Options: 1.11M shares (10% / 90%)
   - Total: 11.11M shares

2. Investor shares
   - Investor stake: 20% (post-money)
   - Investor shares: 2.78M shares (20% / 80%)
   - Total: 13.89M shares

Cap table (after Seed):
- Founder A: 54% (6M / 11.11M × 80%)
- Founder B: 36% (4M / 11.11M × 80%)
- Option pool: 8% (1.11M / 13.89M)
- Seed investor: 20% (2.78M / 13.89M)
- SAFE: Not yet converted
```

### Series A

```
Investment: $5M at $20M pre-money
Option pool: 15% (post-money)

SAFE conversion:
- SAFE $500K at $5M Cap
- $500K / $5M = 10% (based on cap)
- But pre-money $20M → requires adjustment
- SAFE shares ≈ 2.5% (post-money)

Series A shares:
- Investment: $5M
- Post-money: $25M (pre $20M + $5M)
- Stake: 20%

Cap table (after Series A):
- Founder A: 37.8%
- Founder B: 25.2%
- Option pool: 15%
- SAFE: 2.5%
- Seed: 14%
- Series A: 20%
```

### Dilution Simulator

```
Spreadsheet templates:
https://captable.io
https://carta.com

Key variables:
- Investment amount
- Pre-money valuation
- Option pool size
- SAFE Cap & Discount
```

---

## Negotiation Strategy

### Priorities

**Must-Have (Non-Negotiable):**
1. 1x non-participating liquidation preference
2. Broad-based weighted average anti-dilution
3. Founder board control or parity
4. Post-money option pool

**Important:**
5. Single Trigger Acceleration
6. Limit investor rights scope
7. Minimize No-Shop period
8. Cap on expenses

**Nice-to-Have:**
9. Remove dividends
10. Remove redemption rights

### Negotiation Tips

**1. Hire a Lawyer**
```
Retain startup-focused lawyer
Cost: $10K-$25K (worth it)
```

**2. Use Standard Documents**
```
NVCA standard documents
YC SAFE
→ Be suspicious of non-standard clauses
```

**3. Compare Multiple Term Sheets**
```
Get 2-3 term sheets minimum
Create comparison table
Don't just look at valuation—examine full terms
```

**4. Reference Checks**
```
Ask investor's portfolio CEOs:
- How active on board?
- Support during difficult times?
- Follow-on investment?
```

---

## Red Flags (Conditions to Avoid)

### 🚩 Participating Liquidation Preference

```
Double-dipping (preference + equity stake)
→ Unfavorable to founders at exit
→ Absolutely not acceptable in Seed/Series A
```

### 🚩 Full Ratchet Anti-Dilution

```
Massive founder dilution in down round
→ "Death spiral"
→ Must never accept
```

### 🚩 Investor Board Majority

```
Founders lose control
→ Risk of being fired
→ No strategic decision power
```

### 🚩 Excessive Protective Provisions

```
Investor consent needed for daily operations
→ Decision-making paralysis
→ Must limit scope
```

### 🚩 Personal Guarantee

```
Founders' personal assets as collateral
→ Abnormal in startups
→ Refuse
```

---

## Korea-Specific: Convertible Notes & Stock Purchase Agreement

### Korean Convertible Note Structure

```
Typical terms:
- Conversion price: Discount vs issue price (20-30%)
- Conversion request period: 1 year after ~ before maturity
- Maturity: 3 years
- Interest rate: 0-3%
- Early redemption: Partially allowed
```

### Stock Purchase Agreement (SPA)

```
More common in Korea (similar to US Stock Purchase Agreement)

Key provisions:
- Stock issue price
- Representations & Warranties
- Conditions Precedent
- Liability for damages
```

---

## Related Skills and Commands

- **financial-modeling** — Dilution simulations, cap table modeling
- **fundraising-process** — Term sheet received at Week 7
- `/fundraise-pipeline` — Compare multiple term sheets
- `/dd-prep` — Prepare for term sheet negotiation during DD stage
