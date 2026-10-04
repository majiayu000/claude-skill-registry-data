---
name: gomining-cashback
description: "GoMining central cashback processing service for Cards and Travel products. Calculates cashback in TH/s (mining power) based on spending events, asset type, and pricing. Covers Card cashback rates by VIP level (0.5%-5%), Travel cashback rates by VIP level (1%-4%), TH/s conversion formula, miner selection rules, daily accrual for cards, booking-based accrual for travel, miner eligibility restrictions, and 5000 TH max accumulation per miner."
license: Apache-2.0
compatibility: "Compatible with Claude Code, Codex, and all Agent Skills spec tools."
metadata:
  author: gomining
  version: "1.0"
  tags:
    - cashback
    - mining-power
    - cards
    - travel
    - vip
    - th-upgrade
  triggers:
    - "gomining cashback"
    - "card cashback"
    - "travel cashback"
    - "cashback rate"
    - "mining power cashback"
    - "miner upgrade"
    - "th cashback"
---

# GoMining Cashback

## Overview

The GoMining Cashback service is the central processing system for cashback rewards from Cards and Travel products. All cashback is calculated and delivered in TH/s (mining power), which is applied as an upgrade to the user's selected miner. A single miner is selected across all cashback sources.

---

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                 Cashback Processing Flow                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. SPENDING EVENT                                          │
│     ┌──────────────────────────────────────────┐           │
│     │ Card transaction or Travel booking       │           │
│     │ Input: user_id, value, amount             │           │
│     └──────────────────────────────────────────┘           │
│                         │                                   │
│                         ▼                                   │
│  2. CASHBACK CALCULATION                                    │
│     ┌──────────────────────────────────────────┐           │
│     │ Determine VIP level cashback rate        │           │
│     │ Calculate TH/s based on spend + pricing  │           │
│     └──────────────────────────────────────────┘           │
│                         │                                   │
│                         ▼                                   │
│  3. MINER UPGRADE                                           │
│     ┌──────────────────────────────────────────┐           │
│     │ Apply TH/s upgrade to selected miner     │           │
│     │ Output: status, amount in TH/s           │           │
│     └──────────────────────────────────────────┘           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Technical Interface

| Direction | Fields |
|-----------|--------|
| **Input** | `user_id`, `value`, `amount` |
| **Output** | `status`, `amount` (in TH/s) |

---

## Card Cashback

Card cashback is earned on successful card transactions and accrues daily. The cashback rate depends on the user's VIP level.

### Card Cashback Rates (TH/s by VIP Level)

| VIP Level | Cashback Rate |
|-----------|---------------|
| **Bronze** | 0.5% |
| **Silver** | 1% |
| **Gold** | 1.5% |
| **Platinum** | 2% |
| **Diamond** | 3% |
| **Legend** | 5% |

### Card Cashback Rules

| Rule | Details |
|------|---------|
| Accrual frequency | Daily |
| Eligible transactions | Successful transactions only |
| Failed/reversed transactions | No cashback |
| Redemption | Miner TH/s upgrades only |
| Currency | Calculated and applied in TH/s |

> **Important:** Card cashback is redeemable only for miner upgrades. It cannot be withdrawn as tokens or fiat.

---

## Travel Cashback

Travel cashback is earned on hotel bookings through GoMining Travel. The cashback rate depends on the user's VIP level.

### Travel Cashback Rates (TH/s by VIP Level)

| VIP Level | Cashback Rate |
|-----------|---------------|
| **Bronze** | 1% |
| **Silver** | 1.6% |
| **Gold** | 2.2% |
| **Platinum** | 2.8% |
| **Diamond** | 3.4% |
| **Legend** | 4.0% |

### Travel Cashback Formula

```
TH/s Cashback = Booking Amount (USD) x VIP Cashback Rate / Cost per 1 TH/s
```

| Parameter | Value |
|-----------|-------|
| Cost per 1 TH/s | ~$25 (approximate, subject to change) |

**Example Calculation:**

| Step | Value |
|------|-------|
| Booking amount | $500 USD |
| VIP level | Gold (2.2%) |
| Cashback value | $500 x 2.2% = $11 |
| TH/s awarded | $11 / $25 = **0.44 TH/s** |

### Travel Cashback Rules

| Rule | Details |
|------|---------|
| Eligible bookings | Hotels only (flights not included initially) |
| Accrual timing | Accrues after booking is confirmed |
| Finalization | Finalizes after guest check-out |
| Cancellation | Cashback reversed if booking is cancelled before check-out |
| Currency | Calculated and applied in TH/s |

### Travel Cashback Timeline

```
Booking Confirmed  ──>  Cashback Accrues (pending)  ──>  Check-Out  ──>  Cashback Finalized
```

> **Note:** If a booking is cancelled before check-out, the pending cashback is reversed.

---

## Miner Selection

A single miner is selected to receive all cashback from both Cards and Travel sources. The system handles miner selection automatically with manual override available.

### Auto-Selection Logic

| Priority | Rule |
|----------|------|
| 1st | Previously used miner (if still eligible) |
| 2nd | Strongest eligible miner |

### Miner Eligibility Restrictions

The following miners **cannot** be selected for cashback:

| Restriction | Description |
|-------------|-------------|
| **Installment miners** | Miners purchased via installment plan |
| **Miners on sale** | Miners currently listed for sale |
| **Low efficiency miners** | Miners with less than 20 wt/th |
| **Bonus miners** | Miners received as promotional bonuses |

### Accumulation Limits

| Limit | Value |
|-------|-------|
| **Max TH per miner** | 5,000 TH |

> **Warning:** Once a miner reaches the 5,000 TH cap, no additional cashback can be applied to it. The user must select a different eligible miner to continue receiving cashback.

---

## Combined Cashback Summary

| Feature | Card Cashback | Travel Cashback |
|---------|---------------|-----------------|
| **Source** | Card transactions | Hotel bookings |
| **Unit** | TH/s | TH/s |
| **VIP Range** | 0.5% - 5% | 1% - 4% |
| **Accrual** | Daily | After booking, finalized after check-out |
| **Eligible Activity** | Successful transactions | Hotels only (not flights) |
| **Miner** | Shared selected miner | Shared selected miner |
| **Max TH/miner** | 5,000 TH | 5,000 TH |

---

## Frequently Asked Questions

### What is GoMining cashback?

GoMining cashback is a reward system that converts a percentage of your Card spending and Travel bookings into TH/s (mining power), which is applied as an upgrade to your selected miner.

### Is cashback the same for Cards and Travel?

No. Cards and Travel have different cashback rate tables. Travel rates are generally higher (1%-4%) compared to Card rates (0.5%-5%), though Card Legend level (5%) exceeds Travel Legend level (4%).

### How is cashback calculated for Travel bookings?

Travel cashback uses the formula: Booking Amount (USD) x VIP Cashback Rate / Cost per 1 TH/s (~$25). For example, a $500 booking at Gold VIP (2.2%) yields $11 / $25 = 0.44 TH/s.

### Can I receive cashback as tokens or fiat?

No. All cashback is delivered exclusively as TH/s mining power upgrades to your selected miner.

### How do I select which miner receives cashback?

The system auto-selects your previously used miner or your strongest eligible miner. You can manually change the selection. The same miner is used for both Card and Travel cashback.

### Why can't I select a specific miner?

Certain miners are ineligible: installment miners, miners listed for sale, miners with less than 20 wt/th efficiency, and bonus miners. Ensure your chosen miner meets all eligibility criteria.

### What happens when my miner reaches 5,000 TH?

Once a miner hits the 5,000 TH accumulation cap, no further cashback can be applied to it. You must select a different eligible miner to continue receiving cashback rewards.

### When does Travel cashback finalize?

Travel cashback accrues when the booking is confirmed but only finalizes after the guest completes check-out. If the booking is cancelled before check-out, the pending cashback is reversed.

### Do flights earn Travel cashback?

Not initially. Travel cashback currently applies to hotel bookings only. Flight cashback may be added in the future.

### How often does Card cashback accrue?

Card cashback accrues daily based on successful transactions from the previous period. Failed or reversed transactions do not generate cashback.

---

## Official Resources

| Resource | URL |
|----------|-----|
| Main Website | https://gomining.com/ |

---

## References

- [Cashback Rates](references/CASHBACK-RATES.md) — Complete rate tables, formulas, and miner selection rules
- [FAQ: Cashback Program](references/FAQ-CASHBACK.md) — How cashback works for GoMining Card and Travel, rates, and miner selection
