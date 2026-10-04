---
name: gomining-wallet
description: "GoMining Wallet — custodial cryptocurrency wallet. Covers supported assets and networks (BTC, GMT/GOMINING, USDT, USDC, ETH, BNB, SOL, TON), deposit and withdrawal parameters (minimum amounts, network fees, daily limits), KYC Level-1 requirements for full access, withdrawal processing times (new users 15 min, established 2 min), and BTC withdrawal rules tied to mining rewards."
license: Apache-2.0
compatibility: "Compatible with Claude Code, Codex, and all Agent Skills spec tools."
metadata:
  author: gomining
  version: "1.0"
  tags:
    - wallet
    - crypto
    - deposit
    - withdrawal
    - custodial
    - kyc
  triggers:
    - "gomining wallet"
    - "crypto wallet"
    - "deposit crypto"
    - "withdraw crypto"
    - "wallet balance"
    - "supported assets"
    - "network fees"
    - "withdrawal limits"
---

# GoMining Wallet

## Overview

The GoMining Wallet is a custodial cryptocurrency wallet available to all registered GoMining users. It enables depositing, storing, and withdrawing a range of crypto assets across multiple blockchain networks.

---

## Supported Assets

| Asset | Networks |
|-------|----------|
| **BTC** | Bitcoin |
| **GMT / GOMINING** | Ethereum, BSC, Solana, TON |
| **USDT** | ERC-20, BEP-20, TRC-20, Solana, TON |
| **USDC** | Ethereum, BSC, Base, Arbitrum |
| **ETH** | Ethereum |
| **BNB** | BSC |
| **SOL** | Solana |
| **TON** | TON |

---

## Transaction Parameters

| Asset | Min Deposit | Min Withdrawal | Network Fee |
|-------|------------|----------------|-------------|
| BTC | 0.0001 | varies | 0.00006 |
| USDT | 10 | 1–10 | 1–4 |
| USDC | 10 | 0.0025–10 | 0.0005–1 |
| GMT | 10–50 | 50–250 | 1–10 |
| ETH | 10 | 0.0025 | 0.0005 |
| BNB | 10 | 0.013 | 0.001 |
| SOL | 10 | 0.02 | 0.01 |
| TON | 10 | 1 | 0.2 |

> **Note:** Minimum withdrawal and network fee values may vary by network. Ranges indicate variation across supported chains.

---

## Daily Withdrawal Limits

| Asset | User Daily Limit | System Daily Limit |
|-------|------------------|--------------------|
| USDT | 12,500 | 60,000 |
| USDC | 12,500 | 100,000 |
| ETH | 2.14 | 6.3 |
| BNB | 11.8 | 35 |
| SOL | 55 | 55 |
| TON | 3,050 | 30,700 |
| GMT | 37,500 | 1,000,000 |

---

## KYC Requirements

| KYC Status | Capabilities |
|------------|-------------|
| **Without KYC Level-1** | Basic deposits only. No withdrawal of GOMINING, USDT, USDC, BTC (instant). No miner operations. No marketplace sales. |
| **With KYC Level-1** | Full access to all wallet features, withdrawals, miner operations, and marketplace. |

---

## Withdrawal Processing Times

| User Category | Processing Delay |
|---------------|-----------------|
| New users (account < 1 month) | 15 minutes |
| Established users | 2 minutes |

---

## BTC Withdrawal Rules

| Condition | Withdrawal Access |
|-----------|-------------------|
| Before any BTC deposit | Cannot withdraw mining or game rewards. Access opens after creating a personal miner. |
| After BTC deposit | Can withdraw amounts exceeding accumulated mining rewards. |

---

## Wallet Flow

```
┌─────────────────────────────────────────────────────────────┐
│                   GoMining Wallet Flow                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. REGISTER & VERIFY                                       │
│     ┌──────────────────────────────────────────┐            │
│     │ Create GoMining account                  │            │
│     │ Complete KYC Level-1 for full access      │            │
│     └──────────────────────────────────────────┘            │
│                         │                                   │
│                         ▼                                   │
│  2. DEPOSIT                                                 │
│     ┌──────────────────────────────────────────┐            │
│     │ Select asset and network                 │            │
│     │ Send crypto to generated address         │            │
│     │ Minimum deposit thresholds apply          │            │
│     └──────────────────────────────────────────┘            │
│                         │                                   │
│                         ▼                                   │
│  3. MANAGE & WITHDRAW                                       │
│     ┌──────────────────────────────────────────┐            │
│     │ View balances across all assets           │            │
│     │ Withdraw to external address              │            │
│     │ Daily limits and network fees apply        │            │
│     └──────────────────────────────────────────┘            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Frequently Asked Questions

### What is the GoMining Wallet?

A custodial cryptocurrency wallet allowing registered users to deposit, store, and withdraw crypto assets across multiple blockchain networks.

### What assets and networks are supported?

BTC (Bitcoin), GMT/GOMINING (Ethereum, BSC, Solana, TON), USDT (ERC-20, BEP-20, TRC-20, Solana, TON), USDC (Ethereum, BSC, Base, Arbitrum), ETH, BNB, SOL, and TON.

### Do I need KYC to use the wallet?

Basic deposits work without KYC. However, KYC Level-1 is required for withdrawing GOMINING, USDT, USDC, and BTC (instant), as well as for miner operations and marketplace sales.

### What are the withdrawal limits?

Each asset has both a per-user daily limit and a system-wide daily limit. For example, USDT has a 12,500 user daily limit and a 60,000 system daily limit. See the full table above or the references for details.

### How long do withdrawals take?

New users (account under 1 month) experience a 15-minute delay. Established users (1 month or older) have a 2-minute delay.

### Can I withdraw BTC earned from mining?

Before making any BTC deposit, you cannot withdraw mining or game rewards — this access opens after creating a personal miner. After depositing BTC, you can withdraw amounts that exceed your accumulated mining rewards.

### What fees apply?

Network fees vary by asset and blockchain. There are no additional GoMining service fees on top of network fees for standard wallet operations.

### Is the wallet custodial?

Yes. The GoMining Wallet is a custodial solution. Private keys are not held by the user directly.

---

## Official Resources

| Resource | URL |
|----------|-----|
| GoMining App | https://app.gomining.com/ |
| Main Website | https://gomining.com/ |

---

## References

- [Supported Assets](references/SUPPORTED-ASSETS.md) — All assets, networks, fees, and limits
- [Deposit & Withdrawal](references/DEPOSIT-WITHDRAWAL.md) — Deposit/withdrawal rules, processing times, KYC requirements
- [FAQ: Wallet Overview](references/FAQ-OVERVIEW.md) — Overview of the GoMining wallet and its features
- [FAQ: Wallet FAQ](references/FAQ-WALLET.md) — Deposits, withdrawals, supported assets, and wallet mechanics
