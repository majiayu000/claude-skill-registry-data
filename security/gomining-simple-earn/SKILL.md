---
name: gomining-simple-earn
description: "GoMining Simple Earn — passive earning mechanism for interest on crypto asset balances. Covers one-button activation, BTC rewards every 4 hours, supported assets (non-EEA: BTC, ETH, SOL, BNB, TON, USDT, USDC; EEA: same but no USDT), VIP yield multipliers (Bronze I: none through Elite: x1.46), individual APR per asset, yield sources (staking, DeFi protocols, internal liquidity), KYC Level-1 requirement, no lockup or penalties, full withdrawal anytime. Available globally except the USA."
license: Apache-2.0
compatibility: "Compatible with Claude Code, Codex, and all Agent Skills spec tools."
metadata:
  author: gomining
  version: "1.0"
  tags:
    - simple-earn
    - yield
    - interest
    - passive-income
    - btc-rewards
    - staking
  triggers:
    - "simple earn"
    - "gomining earn"
    - "earn interest"
    - "passive income"
    - "btc yield"
    - "auto compound"
    - "earn on crypto"
    - "simple earn eligibility"
    - "simple earn yield"
---

# GoMining Simple Earn

## Overview

Simple Earn is GoMining's passive earning mechanism that lets users earn interest on their crypto asset balances. Deposits auto-compound at fixed intervals, and dividends are paid in BTC regardless of the deposited asset type. There are no lockup periods and no penalties — users can withdraw their full balance at any time.

---

## How It Works

### Activation

| Step | Description |
|------|-------------|
| 1. Invest | One-button invest from the GoMining app |
| 2. Agreement | Sign the Simple Earn agreement |
| 3. Auto-enter | All deposits automatically enter the earning cycle |
| 4. Withdraw | Full withdrawal available at any time |

### Key Principles

| Principle | Details |
|-----------|---------|
| Dividend currency | **BTC** — always paid in BTC regardless of deposited asset |
| Principal protection | Capital preservation is **not absolutely guaranteed** — Simple Earn uses DeFi protocols; in rare cases (e.g. smart contract vulnerability) losses may occur. GoMining actively monitors and rebalances to reduce risk. |
| Interest guarantee | Interest is **NOT** guaranteed; yield can be zero |
| APR | Each asset has an individual APR set by the liquidity manager |
| Estimated yield | Weighted average across all deposited assets |
| Lockup | **None** — no lockup, no penalties |
| Compounding | Auto-compounds at fixed intervals |

---

## Supported Assets

Assets available depend on the user's region:

| Asset | Non-EEA Users | EEA Users |
|-------|--------------|-----------|
| **BTC** | Available | Available |
| **ETH** | Available | Available |
| **SOL** | Available | Available |
| **BNB** | Available | Available |
| **TON** | Available | Available |
| **USDT** | Available | Not available |
| **USDC** | Available | Available |
| **GOMINING** | Excluded | Excluded |

> **Note:** GOMINING token is excluded from Simple Earn and has its own separate earning mechanics. Specific availability may change due to local regulations.

---

## Reward Cycle (Every 4 Hours)

Simple Earn operates on a 4-hour reward cycle:

```
┌─────────────────────────────────────────────────────────────┐
│                  Simple Earn 4-Hour Cycle                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Starting 00:00 UTC — cycles repeat every 4 hours:          │
│  00:00 → 04:00 → 08:00 → 12:00 → 16:00 → 20:00 → 00:00    │
│                                                              │
│  Each cycle:                                                 │
│  ┌──────────────────────────────────────────┐               │
│  │ REWARDS CALCULATED & CREDITED             │               │
│  │ Based on minimum balance held during      │               │
│  │ the full 4-hour cycle                     │               │
│  │ BTC credited directly to wallet           │               │
│  └──────────────────────────────────────────┘               │
│                                                              │
│  IMPORTANT:                                                  │
│  Rewards use the LOWEST balance recorded during the cycle.   │
│  A withdrawal reduces the minimum and affects that cycle.    │
│  New deposits are counted from the START of the next cycle.  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

| Parameter | Details |
|-----------|---------|
| Cycle frequency | **Every 4 hours** (6 times per day) |
| Cycle start | 00:00 UTC, then every 4 hours |
| Reward basis | Minimum balance held during the full cycle |
| Reward currency | **BTC** |
| New deposit effective | Start of next cycle |

---

## VIP Yield Multipliers

Your VIP level applies a multiplier to the base APR for each asset. Higher tiers earn more.

| Tier | Multiplier |
|------|------------|
| Bronze I | x1 (base APR) |
| Bronze II | x1.08 |
| Silver I | x1.1 |
| Silver II | x1.12 |
| Silver III | x1.14 |
| Gold I | x1.16 |
| Gold II | x1.18 |
| Platinum I | x1.2 |
| Platinum II | x1.22 |
| Platinum III | x1.24 |
| Diamond I | x1.26 |
| Diamond II | x1.28 |
| Diamond III | x1.3 |
| Diamond IV | x1.32 |
| Diamond V | x1.34 |
| Legend I | x1.36 |
| Legend II | x1.38 |
| Legend III | x1.4 |
| Legend IV | x1.42 |
| Legend V | x1.44 |
| Elite | x1.46 |

> **Note:** The "Maximum APR" shown in the app reflects the Elite VIP rate. Platinum+ subscription grants a x1.2 multiplier (equivalent to Platinum I) without changing your VIP tier.

---

## Yield Sources

Yield is generated from three primary sources:

| Source | Description |
|--------|-------------|
| **Staking** | Blockchain validation rewards |
| **DeFi Protocols** | Liquidity pools and lending platforms |
| **Internal Liquidity Management** | GoMining's own liquidity operations |

For detailed yield mechanics, see [Yield Mechanics](references/YIELD-MECHANICS.md).

---

## Eligibility

| Requirement | Details |
|-------------|---------|
| KYC | **Level-1** verification required |
| Jurisdiction | Must be in an available (non-restricted) country |
| Minimum balance | **10 USD** equivalent |
| Wallet transfer | Funds must be transferred from main wallet to Simple Earn balance |

### Restricted Jurisdictions

> **Warning:** Simple Earn is not available in several jurisdictions including the USA, Belarus, Cuba, Iran, Iraq, North Korea, Syria, Venezuela, Zimbabwe, and others.

| Region | Restriction | Reason |
|--------|-------------|--------|
| **USA** | Blocked | SEC requires Broker-Dealer license |
| **EEA** | Limited | MiCA CASP requirements |
| **UK** | Restricted | FCA license needed |

For the full list of restrictions, see [Eligibility](references/ELIGIBILITY.md).

---

## Frequently Asked Questions

### What is Simple Earn?

Simple Earn is GoMining's passive earning product that pays BTC interest on your crypto asset balances. It auto-compounds at fixed intervals with no lockup periods or penalties.

### How do I activate Simple Earn?

Tap the one-button invest option in the GoMining app, sign the Simple Earn agreement, and your deposits will automatically begin earning. You need KYC Level-1 verification and a minimum balance of 10 USD equivalent.

### What currency are rewards paid in?

All rewards are paid in **BTC**, regardless of which asset you deposited (BTC, USDT, or USDC).

### Are my funds safe?

GoMining carefully selects and continuously monitors the protocols used in Simple Earn. Protocols may be rotated if needed to reduce risks — the system is actively managed, not "set and forget."

At the same time, Simple Earn works with DeFi protocols, so risks cannot be fully eliminated. In rare cases, such as a smart contract vulnerability, losses may occur. Simple Earn is not a bank deposit, and capital preservation cannot be absolutely guaranteed. Interest is also not guaranteed and yield can be zero in any given period.

### When do I receive rewards?

Rewards are credited every 4 hours (6 times per day), at 00:00, 04:00, 08:00, 12:00, 16:00, and 20:00 UTC. Each reward is calculated based on the minimum balance held during the full 4-hour cycle.

### What if I deposit mid-cycle?

New deposits are counted from the start of the next 4-hour cycle. If you withdraw during a cycle, the reward for that cycle is calculated based on the lowest balance held during it.

### Can I withdraw at any time?

Yes. There are no lockup periods and no penalties. You can withdraw your full balance at any time.

### What assets are supported?

Non-EEA users: BTC, ETH, SOL, BNB, TON, USDT, and USDC. EEA users: BTC, ETH, SOL, BNB, TON, and USDC (USDT is not available in the EEA). GOMINING token is excluded from Simple Earn and has separate mechanics.

### Why is Simple Earn not available in my country?

Simple Earn is restricted in jurisdictions including the USA (SEC Broker-Dealer license required), EEA (MiCA CASP regulations), UK (FCA license needed), and several other countries. See the full list in the Eligibility reference.

### How is APR determined?

Each asset has an individual APR set by GoMining's liquidity manager. The estimated yield displayed is a weighted average across all your deposited assets.

---

## Official Resources

| Resource | URL |
|----------|-----|
| Main Website | https://gomining.com/ |

---

## References

- [Yield Mechanics](references/YIELD-MECHANICS.md) — How yield works, snapshot system, and yield sources
- [Eligibility](references/ELIGIBILITY.md) — KYC requirements, jurisdictions, restrictions, and legal considerations
- [FAQ: Simple Earn](references/FAQ-SIMPLE-EARN.md) — How Simple Earn works, APR, eligibility, and reward mechanics
