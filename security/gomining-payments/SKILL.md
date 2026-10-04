---
name: gomining-payments
description: "GoMining payment infrastructure — methods for purchasing crypto and miners. Covers card payments, on-ramp, Open Banking (PSD2) in EU, SEPA/SEPA Instant protocols, MNPL (Mine Now Pay Later) 0% APR installment plans, KYC/compliance levels, and restricted territories."
license: Apache-2.0
compatibility: "Compatible with Claude Code, Codex, and all Agent Skills spec tools."
metadata:
  author: gomining
  version: "1.0"
  tags:
    - payments
    - on-ramp
    - kyc
    - open-banking
    - mnpl
    - installments
    - compliance
  triggers:
    - "payment methods"
    - "buy crypto"
    - "buy miners"
    - "open banking"
    - "mine now pay later"
    - "mnpl"
    - "kyc verification"
    - "payment provider"
---

# GoMining Payments

## Overview

GoMining provides multiple payment methods for purchasing cryptocurrency and Digital Miners. Payment options include card payments, on-ramp services, Open Banking (PSD2), and installment plans (MNPL). All transactions are subject to KYC/compliance requirements.

---

## Payment Methods

| Method | Assets | Currency | Commission | Chargebacks |
|--------|--------|----------|-----------|------------|
| **Card payment** | GMT | EUR, USD | Varies | Yes |
| **On-Ramp** | BTC, ETH, SOL, etc. | EUR, USD | Varies | No |
| **Open Banking** | BTC, ETH, etc. | EUR, HUF | Lower than card | No |

### Key Differences

| Feature | Card Payment | On-Ramp | Open Banking |
|---------|-------------|---------|--------------|
| Speed | Instant | Near-instant | Instant (SEPA Instant) |
| Chargebacks | Yes | No | No |
| Fees | Varies | Varies | Lower |
| Availability | Global | Global | EU only |

---

## Open Banking (PSD2)

Open Banking enables direct bank-to-platform transfers within the European Union, leveraging the PSD2 directive for secure, low-cost payments.

### Supported Countries

| Country | Status |
|---------|--------|
| France | Active |
| Spain | Active |
| Estonia | Active |
| Belgium | Active |
| Hungary | Active |

### Protocols

| Protocol | Description | Speed |
|----------|-------------|-------|
| **SEPA** | Standard Euro transfers | 1-2 business days |
| **SEPA Instant** | Instant Euro transfers | Seconds |

### Benefits

| Benefit | Description |
|---------|-------------|
| Lower Fees | Significantly lower than card or on-ramp |
| No Chargebacks | Transactions are irreversible |
| Instant Settlement | Via SEPA Instant protocol |
| Direct Transfer | Bank-to-platform without intermediaries |
| PSD2 Security | Regulated under EU payment services directive |

---

## MNPL (Mine Now, Pay Later)

MNPL is an installment plan that allows users to purchase Digital Miners with a down payment and equal monthly installments at 0% APR.

### Terms

| Parameter | Value |
|-----------|-------|
| **APR** | 0% |
| **Down Payment** | 25% of miner price |
| **Max Down Payment** | $5,000 (iteration 1) |
| **Installments** | Equal monthly payments |
| **Price Range** | $0 - $20,000 |

### Eligibility

| Requirement | Detail |
|-------------|--------|
| KYC | Must be verified |
| Territory | Not available in India and other restricted territories |
| Credit Check | May apply |

### How MNPL Works

1. Select a Digital Miner priced between $0 and $20,000.
2. Pay 25% of the price as a down payment (max $5,000).
3. Remaining balance is split into equal monthly installments.
4. No interest or APR charges are applied.
5. Miner begins operating immediately upon purchase.

---

## KYC / Compliance

GoMining requires identity verification, with two levels of KYC depending on the services accessed.

### Verification Levels

#### Level 1 - Proof of Identity (POI)

| Requirement | Description |
|-------------|-------------|
| **ID Document** | Valid government-issued ID |
| **Selfie** | Liveness verification photo |
| **Questionnaire** | Basic user questionnaire |

**Required for:** Withdrawals, miner minting, marketplace access

#### Level 2 - Enhanced Due Diligence (EDD)

| Requirement | Description |
|-------------|-------------|
| **Tax Information** | Tax residency and identification |
| **Employment Details** | Current employment status and information |
| **Proof of Address** | Document confirming residential address |
| **Phone Verification** | Verified phone number |

**Required for:** GoMining Visa card issuance

### Blocked Territories

The following countries are fully blocked from all GoMining services:

| Country |
|---------|
| North Korea |
| Myanmar |
| Iran |
| Afghanistan |
| Syria |
| Yemen |
| Cuba |

---

## FAQ

### Which payment method has the lowest fees?
Open Banking (PSD2) offers the lowest fees among available payment methods. It is available to users in supported EU countries.

### Can I get a chargeback on a crypto purchase?
Only card payments support chargebacks. On-ramp and Open Banking transactions are irreversible.

### What on-ramp options are available?
GoMining offers on-ramp services for purchasing crypto with fiat. Availability may depend on your region.

### How does MNPL work?
MNPL (Mine Now, Pay Later) lets you buy a miner with 25% down and pay the rest in equal monthly installments at 0% APR. The miner starts operating immediately.

### Is MNPL available worldwide?
No. MNPL is not available in India and certain other restricted territories.

### What is the maximum miner price for MNPL?
MNPL supports miners priced from $0 to $20,000 with a maximum down payment of $5,000 in the current iteration.

### What KYC level do I need?
Level 1 (POI) is required for withdrawals, minting, and marketplace. Level 2 (EDD) is required for the Visa card.

### What if my KYC verification fails?
If your KYC verification is unsuccessful, contact support for assistance.

### Why is my country blocked?
GoMining cannot provide services to users in sanctioned territories (North Korea, Myanmar, Iran, Afghanistan, Syria, Yemen, Cuba) due to international compliance regulations.
