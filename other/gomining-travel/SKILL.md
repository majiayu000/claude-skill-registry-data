---
name: gomining-travel
description: "GoMining Travel — integrated hotel booking platform using GM tokens with cashback in mining power (TH/s). Covers hotel booking via GM tokens, VIP-tiered cashback rates (Bronze 1% to Legend 4%), cashback-to-TH/s conversion formula, miner selection rules, booking lifecycle (Pending, Success, Cancelled), supported payment methods (GM, BTC, USDT), and refund and cancellation policies."
license: Apache-2.0
compatibility: "Compatible with Claude Code, Codex, and all Agent Skills spec tools."
metadata:
  author: gomining
  version: "1.0"
  tags:
    - travel
    - hotels
    - booking
    - cashback
    - mining-power
    - gm-tokens
  triggers:
    - "gomining travel"
    - "travel booking"
    - "hotel booking"
    - "travel cashback"
    - "booking with gm tokens"
    - "travel mining power"
---

# GoMining Travel

## Overview

GoMining Travel is an integrated hotel booking platform embedded within the GoMining app. Users book hotels using GM tokens and receive cashback in the form of TH/s mining power upgrades applied to their miners.

**Launch Date:** February 20, 2026

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Embedded Booking** | Travel booking directly inside the GoMining app |
| **GM Token Payments** | Primary payment method for all bookings |
| **TH/s Cashback** | Cashback awarded as mining power upgrades |
| **VIP Tiers** | Cashback rates scale with VIP level (1%--4%) |
| **Hotel Search** | Full hotel search and booking engine |

---

## Payment Methods

| Method | Type | Notes |
|--------|------|-------|
| **GM** | Primary | Native GoMining token, default payment |
| **BTC** | Alternative | Converted to GM at transaction time |
| **USDT** | Alternative | Converted to GM at transaction time |

> **Note:** BTC and USDT payments are converted to GM tokens before the booking is processed.

---

## Cashback System

Cashback is awarded **only on hotel bookings** and is distributed as TH/s mining power applied to a user-selected miner.

### VIP Cashback Rates

| VIP Level | Cashback Rate |
|-----------|---------------|
| Bronze | 1.0% |
| Silver | 1.6% |
| Gold | 2.2% |
| Platinum | 2.8% |
| Diamond | 3.4% |
| Legend | 4.0% |

### Cashback Formula

```
Cashback (TH/s) = Booking Amount (USD) x VIP Cashback Rate / Current TH Price
```

**Example:** A Gold VIP user books a $650 hotel at the current TH price:

```
$650 x 2.2% / TH Price = Cashback TH/s
```

See [Cashback Tiers](references/CASHBACK-TIERS.md) for full details on miner selection rules and restrictions.

---

## Booking Lifecycle

```
┌─────────────────────────────────────────────────────────┐
│                GoMining Travel Booking Flow              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. SEARCH                                              │
│     ┌─────────────────────────────────────┐             │
│     │ User searches hotels                │             │
│     │ within the GoMining app             │             │
│     └─────────────────────────────────────┘             │
│                       │                                 │
│                       ▼                                 │
│  2. BOOK & PAY                                          │
│     ┌─────────────────────────────────────┐             │
│     │ Pay with GM tokens (or BTC/USDT)    │             │
│     │ Status: PENDING                     │             │
│     └─────────────────────────────────────┘             │
│                       │                                 │
│              ┌────────┴────────┐                        │
│              ▼                 ▼                         │
│  3a. SUCCESS              3b. CANCELLED                 │
│     ┌──────────────┐     ┌──────────────┐               │
│     │ Confirmed    │     │ Refund issued│               │
│     │ Cashback     │     │ if eligible  │               │
│     │ accrues      │     └──────────────┘               │
│     └──────────────┘                                    │
│              │                                          │
│              ▼                                          │
│  4. CHECK-OUT                                           │
│     ┌─────────────────────────────────────┐             │
│     │ Cashback finalized after check-out  │             │
│     │ TH/s applied to selected miner      │             │
│     └─────────────────────────────────────┘             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

See [Booking Flow](references/BOOKING-FLOW.md) for full lifecycle details, refund policies, and phased rollout.

---

## Rollout Phases

| Phase | Scope | Status |
|-------|-------|--------|
| Phase 1 | Hotel bookings with GM token payments | Launched (Feb 20, 2026) |

---

## Frequently Asked Questions

### What is GoMining Travel?

GoMining Travel is an integrated hotel booking platform embedded within the GoMining app. It lets users book hotels using GM tokens and earn cashback as TH/s mining power.

### How do I pay for bookings?

The primary payment method is GM tokens. You can also pay with BTC or USDT, which are converted to GM at transaction time.

### How does the cashback work?

When you book a hotel, you receive cashback based on your VIP level (1% for Bronze up to 4% for Legend). The cashback is converted into TH/s mining power using the formula: Booking Amount (USD) × VIP Rate ÷ Current TH Price. Cashback accrues after booking confirmation and finalizes after check-out.

### Does cashback apply to all bookings?

Yes. Cashback is awarded on hotel bookings based on your VIP level (1% for Bronze up to 4% for Legend).

### Which miner receives the cashback?

You select a target miner for cashback accumulation. If none is selected, the system auto-selects your strongest miner. Maximum miner capacity for accumulation is 5000 TH. If you have no miner, the cashback is saved and auto-applied when you purchase your first miner.

### Can I cancel a booking?

Yes. Refunds are allowed up to the cancellation deadline specified at booking time. Booking statuses transition from Pending to either Success or Cancelled.

### When was GoMining Travel launched?

GoMining Travel launched on February 20, 2026, starting with Phase 1 (hotel bookings).

---

## Official Resources

| Resource | URL |
|----------|-----|
| GoMining App | https://gomining.com/ |
| GoMining Help | https://help.gomining.com/ |

---

## References

- [Cashback Tiers](references/CASHBACK-TIERS.md) — VIP cashback rates, formula, and miner selection rules
- [Booking Flow](references/BOOKING-FLOW.md) — Booking lifecycle, payment methods, refunds, and phased rollout
- [FAQ: GoMining Travel](references/FAQ-TRAVEL.md) — Booking hotels, supported currencies, cashback, and support contacts
