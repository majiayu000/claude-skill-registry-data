---
name: gomining-promos
description: "GoMining promotional system — promo codes, GoBoxes, and bonus mechanics. Covers general, individual, and referral promo code types, discount and cashback bonuses (tokens or TH mining power), promo code parameters (percent, caps, validity, usage limits, VIP and payment restrictions), promo sources (email campaigns, GoBoxes, Referral codes), GoBox digital loot boxes with weighted prize pools per VIP level, bonus miner task-based completion model, trait selection system, raffles, and bounty program."
license: Apache-2.0
compatibility: "Compatible with Claude Code, Codex, and all Agent Skills spec tools."
metadata:
  author: gomining
  version: "1.0"
  tags:
    - promos
    - promo-codes
    - goboxes
    - bonuses
    - cashback
    - referral
    - vip
  triggers:
    - "gomining promos"
    - "promo code"
    - "gobox"
    - "bonus miner"
    - "referral code"
    - "discount code"
    - "promotional"
---

# GoMining Promos

## Overview

The GoMining promotional system provides promo codes, GoBoxes, and bonus mechanics to incentivize user engagement, purchases, and referrals. Promos are distributed via email campaigns, GoBoxes, or generated as referral codes.

---

## Promo Code Types

| Type | Description | Scope |
|------|-------------|-------|
| **General** | One code shared across a user segment | Many users, same code |
| **Individual** | Unique code generated per user | One code per user |
| **Referral** | Binds a new user to the referrer on first purchase | Referrer-specific |

### General Codes

- A single code is created and distributed to a target segment (e.g., all Gold VIP users).
- Any eligible user can redeem the code within the defined limits.

### Individual Codes

- A unique code is generated and assigned to each user individually.
- Typically distributed via email campaigns or in-app notifications.

### Referral Codes

- Each user has a unique referral code.
- When a new user enters the referral code during their first purchase, they are permanently bound to the referrer.
- Both referrer and referee may receive bonuses depending on campaign configuration.

---

## Bonus Types

| Bonus Type | Description | Unit |
|------------|-------------|------|
| **Discount** | Fixed dollar amount subtracted from purchase price | USD ($) |
| **Cashback in Tokens** | Percentage of purchase returned as GOMINING tokens | GOMINING |
| **Cashback in Mining Power** | Percentage of purchase returned as mining power | TH/s |

---

## Promo Code Parameters

| Parameter | Description | Range / Notes |
|-----------|-------------|---------------|
| **Bonus Percent** | Percentage bonus applied to the purchase | 0-100% |
| **Max Bonus Cap** | Maximum bonus amount regardless of percent | Optional; caps the total bonus value |
| **Validity Period** | When the code is active | Date range (start-end) or N days from issuance |
| **Min Purchase Amount** | Minimum spend required to activate the code | Optional; USD threshold |
| **Global Usage Limit** | Total number of times the code can be redeemed | Across all users |
| **Per-User Usage Limit** | Maximum redemptions per individual user | Per user |
| **VIP Level Restriction** | Restricts code to specific VIP levels | Optional; e.g., Gold+ only |
| **Payment Method Restriction** | Limits code to specific payment methods | Fiat only, Crypto only, or both |

---

## Promo Sources

| Source | Description |
|--------|-------------|
| **Email Campaigns** | Automated distribution via email/push notifications |
| **GoBoxes** | Promo codes as prizes inside GoBox loot boxes |
| **Referral Codes** | User-generated referral codes |

---

## GoBoxes

GoBoxes are digital loot boxes awarded for achievements and milestones. Each GoBox contains a random prize drawn from a weighted probability pool.

### Prize Types

| Prize | Description |
|-------|-------------|
| **Promo Codes** | Discount or cashback codes |
| **Avatar Keys** | Unlock cosmetic avatar items |
| **Bonus Miner Days** | Extra days of miner operation |
| **GOMINING Tokens** | Direct token rewards |
| **Gameplay Boosts** | Temporary gameplay enhancements |

### VIP Collections

Each VIP level has its own GoBox collection with different prize pools and probabilities:

| VIP Level | Collection | Prize Quality |
|-----------|------------|---------------|
| **Bronze** | Bronze Collection | Standard prizes |
| **Silver** | Silver Collection | Improved prizes |
| **Gold** | Gold Collection | Premium prizes |
| **Platinum** | Platinum Collection | Elite prizes |

### GoBox Limits

| Rule | Value |
|------|-------|
| Maximum keys per week | 1-2 keys |
| Distribution | Achievement-based |

> **Note:** See [GoBox Mechanics](references/GOBOXES.md) for detailed prize weights and collection breakdowns.

---

## Bonus Miner

The Bonus Miner is a task-based reward system where users complete tasks to earn a bonus miner.

### How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                   Bonus Miner Flow                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. TASK ASSIGNMENT                                         │
│     ┌──────────────────────────────────────────┐           │
│     │ User receives a set of tasks to complete │           │
│     │ Tasks vary by campaign and VIP level     │           │
│     └──────────────────────────────────────────┘           │
│                         │                                   │
│                         ▼                                   │
│  2. TASK COMPLETION                                         │
│     ┌──────────────────────────────────────────┐           │
│     │ Complete all required tasks              │           │
│     │ Progress tracked automatically           │           │
│     └──────────────────────────────────────────┘           │
│                         │                                   │
│                         ▼                                   │
│  3. TRAIT SELECTION                                         │
│     ┌──────────────────────────────────────────┐           │
│     │ Choose miner traits upon completion      │           │
│     │ Traits affect miner appearance/stats     │           │
│     └──────────────────────────────────────────┘           │
│                         │                                   │
│                         ▼                                   │
│  4. MINER AWARDED                                           │
│     ┌──────────────────────────────────────────┐           │
│     │ Bonus miner added to user's collection   │           │
│     │ Miner begins generating rewards          │           │
│     └──────────────────────────────────────────┘           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Trait Selection System

- Upon completing all tasks, users select traits for their bonus miner.
- Traits determine visual appearance and may affect miner characteristics.
- Trait options depend on the specific bonus miner campaign.

---

## Promo Code Redemption Flow

```
┌─────────────────────────────────────────────────────────────┐
│                Promo Code Redemption Flow                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. USER ENTERS CODE                                        │
│     ┌──────────────────────────────────────────┐           │
│     │ Code entered at checkout or promo page   │           │
│     └──────────────────────────────────────────┘           │
│                         │                                   │
│                         ▼                                   │
│  2. VALIDATION                                              │
│     ┌──────────────────────────────────────────┐           │
│     │ Check: code exists and is active         │           │
│     │ Check: within validity period            │           │
│     │ Check: global usage limit not reached    │           │
│     │ Check: per-user limit not reached        │           │
│     │ Check: VIP level eligible (if set)       │           │
│     │ Check: payment method matches (if set)   │           │
│     │ Check: min purchase amount met (if set)  │           │
│     └──────────────────────────────────────────┘           │
│                         │                                   │
│                         ▼                                   │
│  3. BONUS APPLIED                                           │
│     ┌──────────────────────────────────────────┐           │
│     │ Calculate bonus (percent x purchase)     │           │
│     │ Apply max bonus cap (if set)             │           │
│     │ Apply discount / queue cashback          │           │
│     └──────────────────────────────────────────┘           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Frequently Asked Questions

### What types of promo codes does GoMining offer?

GoMining offers three types: General codes (shared across a user segment), Individual codes (unique per user), and Referral codes (binds a new user to a referrer on first purchase).

### What bonuses can a promo code provide?

Promo codes can provide a fixed dollar discount, cashback in GOMINING tokens, or cashback in mining power (TH/s).

### How long are promo codes valid?

Validity depends on configuration: either a fixed date range (start and end dates) or a number of days from the date of issuance.

### Can promo codes be restricted to certain users?

Yes. Codes can be restricted by VIP level (e.g., Gold and above only) and by payment method (fiat only, crypto only, or both). They can also have minimum purchase requirements.

### What is a GoBox?

A GoBox is a digital loot box awarded for achievements. It contains a random prize selected from a weighted probability pool. Prizes include promo codes, avatar keys, bonus miner days, GOMINING tokens, and gameplay boosts.

### How many GoBox keys can I earn per week?

Users can earn a maximum of 1-2 keys per week, depending on achievements and activity.

### Are GoBox prizes the same for all VIP levels?

No. Each VIP level (Bronze, Silver, Gold, Platinum) has its own collection with different prize pools and probabilities. Higher VIP levels have access to better prizes.

### What is the Bonus Miner?

The Bonus Miner is a task-based reward system. Users complete a set of assigned tasks and, upon completion, select traits for a bonus miner that is added to their collection.

### How do referral codes work?

Each user has a unique referral code. When a new user enters the referral code during their first purchase, they are permanently bound to the referrer. Both parties may receive bonuses depending on the active campaign configuration.

---

## Official Resources

| Resource | URL |
|----------|-----|
| Main Website | https://gomining.com/ |

---

## References

- [GoBox Mechanics](references/GOBOXES.md) — GoBox prize pools, VIP collections, and probability mechanics
- [FAQ: Promos Overview](references/FAQ-OVERVIEW.md) — Overview of all GoMining promotional programs
- [FAQ: Bonus Miner](references/FAQ-BONUS-MINER.md) — How the free Bonus Miner works and how to use it
- [FAQ: Bounty Program](references/FAQ-BOUNTY.md) — Earning GOMINING tokens through weekly Bounty tasks
- [FAQ: Raffles and Contests](references/FAQ-RAFFLES.md) — How raffles and contests work, tickets, and prize claiming
- [FAQ: Referral and Ambassador Program](references/FAQ-REFERRAL.md) — Referral rewards, ambassador benefits, and program rules
