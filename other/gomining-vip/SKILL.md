---
name: gomining-vip
description: "GoMining VIP loyalty program — tiered benefits system based on hashrate (TH) or veGOMINING votes. Covers tier progression from Bronze I through Elite, maintenance discounts, Launchpad access tiers, Reinvestment bonuses, Clan creation in Miner Wars, dedicated VIP managers, card cashback rates, travel cashback, GoBox rewards per tier, and Platinum+ subscription for instant VIP benefits."
license: Apache-2.0
compatibility: "Compatible with Claude Code, Codex, and all Agent Skills spec tools."
metadata:
  author: gomining
  version: "1.1"
  tags:
    - vip
    - loyalty
    - tiers
    - hashrate
    - vegomining
    - cashback
    - launchpad
    - subscription
    - platinum+
  triggers:
    - "vip program"
    - "vip tiers"
    - "loyalty program"
    - "vip benefits"
    - "cashback rates"
    - "maintenance discount"
    - "launchpad access"
    - "platinum+ subscription"
    - "vip subscription"
    - "platinum subscription"
---

# GoMining VIP Program

## Overview

The GoMining VIP program is a loyalty system that rewards users based on their hashrate (TH) or veGOMINING voting power. Users progress through tiers to unlock increasing benefits including maintenance discounts, Launchpad allocations, cashback rates, and exclusive perks.

---

## Tier Structure

The VIP program has the following tiers, each with sub-levels (I, II, III where applicable):

| Tier | Level | Description |
|------|-------|-------------|
| **Bronze** | I, II | Entry-level tier for all users |
| **Silver** | I, II, III | Unlocked via 10 TH or 100 veGOMINING votes |
| **Gold** | I, II | Mid-level tier with Clan creation access |
| **Platinum** | I, II, III | Premium tier with dedicated VIP manager |
| **Diamond** | I, II, III, IV, V | High-tier with Tier 1 Launchpad access |
| **Legend** | I, II, III, IV, V | Elite-level rewards and cashback |
| **Elite** | — | Highest achievable tier |

---

## Tier Progression

Users qualify for a tier by meeting **either** the minimum hashrate (TH) **or** the minimum veGOMINING voting threshold — whichever is reached first.

### Complete Tier Criteria & Benefits

| Tier | Min TH | Min veGOM | Maint. Discount | Card Cashback | SE Multiplier | Travel Cashback | Instant Funds Fee | Launchpad | GoBox | Feature |
|------|--------|-----------|----------------|--------------|--------------|----------------|-------------------|-----------|-------|---------|
| **Bronze I** | 0 | 0 | 0% | 0.5% | x1 | 1% | 2.5% | — | — | — |
| **Bronze II** | 5 | 50 | 0.3% | 0.5% | x1.08 | 1% | 2.43% | — | Bronze | — |
| **Silver I** | 10 | 100 | 0.6% | 1% | x1.1 | 1.6% | 2.36% | x1 (Tier 1) | Silver | Reinvestment in TH (+5%) |
| **Silver II** | 25 | 250 | 0.9% | 1% | x1.12 | 1.6% | 2.29% | x2.5 (Tier 2) | Silver | — |
| **Silver III** | 50 | 500 | 1.2% | 1% | x1.14 | 1.6% | 2.21% | x5.3 (Tier 3) | Silver | — |
| **Gold I** | 100 | 1,000 | 1.5% | 1.5% | x1.16 | 2.2% | 2.14% | x11 (Tier 4) | Gold | Clan ownership (5% royalties) |
| **Gold II** | 200 | 2,000 | 1.8% | 1.5% | x1.18 | 2.2% | 2.07% | x23 (Tier 5) | Gold x2 | — |
| **Platinum I** | 500 | 5,000 | 2.1% | 2% | x1.2 | 2.8% | 2% | x60 (Tier 6) | Platinum | VIP-support & special offers |
| **Platinum II** | 1,000 | 10,000 | 2.4% | 2% | x1.22 | 2.8% | 1.96% | x125 (Tier 7) | Platinum x2 | — |
| **Platinum III** | 2,500 | 25,000 | 2.7% | 2% | x1.24 | 2.8% | 1.92% | x330 (Tier 8) | Platinum x3 | — |
| **Diamond I** | 5,000 | 50,000 | 3% | 3% | x1.26 | 3.4% | 1.88% | x700 (Tier 9) | Diamond | Reinvestment in TH (+10%) |
| **Diamond II** | 7,000 | 70,000 | 3.3% | 3% | x1.28 | 3.4% | 1.85% | x700 (Tier 9) | Diamond x2 | — |
| **Diamond III** | 9,000 | 90,000 | 3.6% | 3% | x1.3 | 3.4% | 1.81% | x700 (Tier 9) | Diamond x3 | — |
| **Diamond IV** | 12,000 | 120,000 | 3.9% | 3% | x1.32 | 3.4% | 1.77% | x700 (Tier 9) | Diamond x4 | — |
| **Diamond V** | 20,000 | 200,000 | 4.2% | 3% | x1.34 | 3.4% | 1.73% | x700 (Tier 9) | Diamond x5 | — |
| **Legend I** | 50,000 | 500,000 | 4.5% | 5% | x1.36 | 4% | 1.69% | x700 (Tier 9) | Legend | Coming soon |
| **Legend II** | 100,000 | 1,000,000 | 4.8% | 5% | x1.38 | 4% | 1.65% | x700 (Tier 9) | Legend x2 | — |
| **Legend III** | 250,000 | 2,500,000 | 5.1% | 5% | x1.4 | 4% | 1.62% | x700 (Tier 9) | Legend x3 | — |
| **Legend IV** | 400,000 | 4,000,000 | 5.4% | 5% | x1.42 | 4% | 1.58% | x700 (Tier 9) | Legend x4 | — |
| **Legend V** | 750,000 | 7,500,000 | 5.7% | 5% | x1.44 | 4% | 1.54% | x700 (Tier 9) | Legend x5 | — |
| **Elite** | 1,000,000 | 10,000,000 | 6% | 5% | x1.46 | 4% | 1.5% | x700 (Tier 9) | Legend x6 | Coming soon |

**Note:** Only one condition (TH or veGOMINING) needs to be met. Tokens are locked (not spent) when converted to veGOMINING. For current GOMINING price, see [Live Market Data](../gomining-overview/references/LIVE-MARKET-DATA.md).

---

## Perks by Tier

### Maintenance Discounts

All VIP tiers receive progressive maintenance fee discounts. Ranges from 0% at Bronze I to 6% at Elite. See the complete criteria table above for per-tier values.

### Launchpad Access

| Tier | Launchpad Tier | Allocation Multiplier |
|------|---------------|----------------------|
| Bronze I–II | No access | — |
| Silver I | Tier 1 | x1 |
| Silver II | Tier 2 | x2.5 |
| Silver III | Tier 3 | x5.3 |
| Gold I | Tier 4 | x11 |
| Gold II | Tier 5 | x23 |
| Platinum I | Tier 6 | x60 |
| Platinum II | Tier 7 | x125 |
| Platinum III | Tier 8 | x330 |
| Diamond I–V, Legend I–V, Elite | Tier 9 | x700 |

### Tier-Specific Perks

| Tier | Perk | Details |
|------|------|---------|
| **Silver I** | Reinvestment Bonus | +5% bonus on all reinvestments |
| **Silver I** | Launchpad Allocations | Access to Launchpad token sales (Tier 1) |
| **Gold I** | Clan Creation | Create Clans in Miner Wars |
| **Gold I** | GOMINING Royalties | 5% GOMINING royalties from Clan activity |
| **Platinum I** | Dedicated VIP Manager | Personal account manager + special offers |
| **Diamond I** | Reinvestment Bonus | +10% bonus on all reinvestments |

---

## Card Cashback Rates

VIP tier determines the cashback percentage for GoMining Card transactions and travel bookings. Card and travel cashback rates are the same across all sub-levels within a major tier.

| Tier | Card Cashback | Travel Cashback |
|------|--------------|-----------------|
| **Bronze I–II** | 0.5% | 1.0% |
| **Silver I–III** | 1.0% | 1.6% |
| **Gold I–II** | 1.5% | 2.2% |
| **Platinum I–III** | 2.0% | 2.8% |
| **Diamond I–V** | 3.0% | 3.4% |
| **Legend I–V** | 5.0% | 4.0% |
| **Elite** | 5.0% | 4.0% |

**Notes:**
- Cashback is applied automatically to eligible transactions.
- Travel cashback applies to bookings made through the GoMining Travel service.

---

## Instant Funds Fee by VIP Tier

The one-time service fee for Instant Funds (BTC collateral for USDT/USDC) decreases as VIP level increases.

| Tier | Instant Funds Fee |
|------|------------------|
| Bronze I | 2.5% |
| Bronze II | 2.43% |
| Silver I | 2.36% |
| Silver II | 2.29% |
| Silver III | 2.21% |
| Gold I | 2.14% |
| Gold II | 2.07% |
| Platinum I | 2.0% |
| Platinum II | 1.96% |
| Platinum III | 1.92% |
| Diamond I | 1.88% |
| Diamond II | 1.85% |
| Diamond III | 1.81% |
| Diamond IV | 1.77% |
| Diamond V | 1.73% |
| Legend I | 1.69% |
| Legend II | 1.65% |
| Legend III | 1.62% |
| Legend IV | 1.58% |
| Legend V | 1.54% |
| Elite | 1.5% |

---

## Platinum+ Subscription

The **Platinum+ Subscription** is an alternative path to premium VIP benefits without accumulating TH or veGOMINING votes.

### How It Works

- Pay a subscription fee to instantly unlock Platinum I-level benefits
- **Does not change your VIP tier** — benefits are granted independently
- Ideal for new users or those who prefer subscription over asset accumulation

### Subscription Benefits

| Benefit | Value |
|---------|-------|
| Card Cashback | 2% on purchases |
| Maintenance Discount | 2.1% savings |
| Spell Discounts | 15% off (Miner Wars) |
| Simple Earn APR Boost | x1.2 multiplier |
| Dedicated VIP Manager | Yes |

### Free Platinum+ via Referrals

Refer a new user to GoMining and receive **1 month of Platinum+ subscription free** (must activate within 30 days of referral's registration).

---

## Key Rules

1. **Progression is dynamic:** If your hashrate or veGOMINING drops below the threshold, your tier may be adjusted downward.
2. **Benefits are cumulative:** Higher tiers retain all benefits from lower tiers.
3. **Reinvestment bonus:** The +5% reinvestment bonus at Silver I applies on top of base reinvestment returns.
4. **Clan royalties:** The 5% GOMINING royalties at Gold I are earned from members' Clan activity in Miner Wars.
5. **Platinum+ is independent:** Subscription benefits apply separately from tier-based benefits.

---

## FAQ

### How do I check my current VIP tier?
Your VIP tier is displayed in your GoMining dashboard profile. It updates automatically when your hashrate or veGOMINING balance changes.

### Can I qualify through both TH and veGOMINING?
You only need to meet one of the two thresholds. Meeting both does not grant additional benefits beyond the tier you qualify for.

### How quickly does my tier update after increasing hashrate?
Tier updates are processed automatically and typically reflect within a short period after meeting the new threshold.

### Do maintenance discounts stack with other promotions?
Maintenance discounts from VIP tiers are applied as the base discount. Promotional discounts may or may not stack depending on the specific promotion terms.

### What happens to my Clan if I drop below Gold I?
If your tier drops below Gold I, you may lose the ability to manage your Clan. Existing Clans remain but management features are restricted until the tier is restored.

### Is Elite tier invitation-only?
Elite is the highest tier and may have additional qualification requirements beyond standard TH or veGOMINING thresholds.

### What is Platinum+ Subscription?
Platinum+ is a paid subscription that grants Platinum I-level benefits (2% cashback, 2.1% maintenance discount, 15% spell discounts, x1.2 Simple Earn APR boost) without requiring TH or veGOMINING holdings. It does not change your actual VIP tier.

### Can I have both Platinum+ Subscription and a higher VIP tier?
Yes. If you're already Diamond or Legend tier, Platinum+ subscription-specific benefits like the APR boost still apply. Overlapping benefits follow your higher tier.

---

## References

- [FAQ: VIP Program](references/FAQ-VIP-PROGRAM.md) — How the VIP program works, tier progression, and benefits
- [FAQ: Platinum+ Subscription](references/FAQ-VIP-SUBSCRIPTION.md) — The Platinum+ subscription, pricing, and what it includes
- [FAQ: GoBoxes](references/FAQ-GOBOXES.md) — GoBox mystery boxes, collections, and prize mechanics
- [FAQ: VIP Progression Rules](references/FAQ-VIP-PROGRESSION-RULES.md) — Secondary market, wallet linkage, GoBox eligibility, August 2025 policy
