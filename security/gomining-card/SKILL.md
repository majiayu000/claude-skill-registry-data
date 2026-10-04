---
name: gomining-card
description: "GoMining Card — virtual and physical cards for crypto payments. Covers card types and features, supported cryptocurrencies (GOMINING, BTC, USDT, USDC), instant crypto-to-fiat conversion, Apple Pay and Google Wallet compatibility, ATM withdrawals, KYC Level 1+2 requirements, $100 minimum balance, eligibility by region (European/Global), document requirements, passport restrictions (Belarus, Russia), 60+ prohibited jurisdictions, and pricing (no commission, internal exchange rate)."
license: Apache-2.0
compatibility: "Compatible with Claude Code, Codex, and all Agent Skills spec tools."
metadata:
  author: gomining
  version: "1.0"
  tags:
    - card
    - payments
    - crypto-card
    - kyc
    - debit-card
  triggers:
    - "gomining card"
    - "crypto card"
    - "kyc requirements"
    - "card eligibility"
    - "crypto payments"
    - "supported regions"
---

# GoMining Card

## Overview

The GoMining Card is a virtual (and later, physical) debit card linked to your GoMining crypto card wallet balance. Transactions trigger instant cryptocurrency-to-fiat conversion at current exchange rates.

---

## Card Types

| Type | Availability | Delivery | Activation |
|------|--------------|----------|------------|
| **Virtual** | Issued immediately upon approval | Digital | Auto-activated |
| **Physical** | Coming soon | Shipped to address | Manual activation |

---

## Supported Cryptocurrencies

Users can select payment assets from:

| Currency | Type | Description |
|----------|------|-------------|
| **GOMINING** | Utility Token | Native ecosystem token |
| **BTC** | Cryptocurrency | Bitcoin |
| **USDT** | Stablecoin | Tether USD |
| **USDC** | Stablecoin | USD Coin |

---

## Card Features

### Instant Conversion

| Feature | Description |
|---------|-------------|
| Conversion | Crypto-to-fiat at transaction time |
| Rate | Internal exchange rate |
| Settlement | Instant at point of sale |

### Digital Wallet Compatibility

| Wallet | Status |
|--------|--------|
| Apple Pay | Supported |
| Google Wallet | Supported |
| Samsung Pay | Coming soon |

### Security

| Feature | Description |
|---------|-------------|
| PIN Protection | Required for physical transactions |
| 3DS Password | Static password for online security |
| NFC | Contactless payments supported |

---

## Requirements

### Minimum Balance

| Requirement | Value |
|-------------|-------|
| Minimum wallet balance | **$100** |
| Calculation | Across all assets in GoMining wallet |

### KYC Verification

| Level | Required | Description |
|-------|----------|-------------|
| Level 1 | Yes | Basic identity verification |
| Level 2 | Yes | Enhanced verification with address proof |

### Card Limits

| Limit | Value |
|-------|-------|
| Cards per user | **Up to 3 virtual cards** |

---

## Eligibility

### European Residents (EEA+)

| Requirement | Description |
|-------------|-------------|
| Identity Document | Valid national passport OR ID card |
| Address Proof | Document under 3 months old |
| Regions | EEA+ and listed European countries |

### Global Residents

| Requirement | Description |
|-------------|-------------|
| Identity Document | Valid national passport OR ID card (where supported) |
| Address Proof | From non-prohibited jurisdictions |
| Note | Identity and address documents can be from different countries |

### Excluded Documents

The following cannot serve as primary identity proof:

| Document Type | Exception |
|---------------|-----------|
| Driver's licenses | Not accepted |
| Residence permits | Only accepted for non-European citizens residing in Europe |

### Passport Restrictions

| Restriction | Details |
|-------------|---------|
| Rejected passports | Certain nations' passports are not accepted |
| Belarus | Must provide valid EEA+ residence permit |
| Russia | Must provide valid EEA+ residence permit |

### Prohibited Jurisdictions

> **Warning:** Card applications are not available in **60+ countries**. Check the full list in the references.

---

## Pricing

| Item | Cost |
|------|------|
| Card issuance | Check current fees |
| Transaction commission | **No commission** |
| Exchange rate | Internal rate (may differ from public sources) |

> **Note:** There is no commission on transactions; however, GoMining uses an internal exchange rate, which might be different from publicly available sources.

---

## Card Usage Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    GoMining Card Flow                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. FUND WALLET                                              │
│     ┌──────────────────────────────────────────┐            │
│     │ Deposit GOMINING, BTC, USDT, or USDC     │            │
│     │ Minimum: $100 total balance              │            │
│     └──────────────────────────────────────────┘            │
│                         │                                    │
│                         ▼                                    │
│  2. MAKE PURCHASE                                            │
│     ┌──────────────────────────────────────────┐            │
│     │ Use card at POS or online                │            │
│     │ Tap with Apple Pay / Google Wallet       │            │
│     └──────────────────────────────────────────┘            │
│                         │                                    │
│                         ▼                                    │
│  3. INSTANT CONVERSION                                       │
│     ┌──────────────────────────────────────────┐            │
│     │ Crypto converted to fiat at current rate │            │
│     │ Transaction settled immediately          │            │
│     └──────────────────────────────────────────┘            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Frequently Asked Questions

### What is the GoMining Card?

It's a virtual (and later, physical) debit card linked to your GoMining crypto card wallet balance. Transactions trigger instant cryptocurrency-to-fiat conversion at current exchange rates.

### What cryptocurrencies are supported?

Users can select payment assets from: GOMINING, BTC, USDT, or USDC.

### What are the GoMining Card features?

Virtual cards are issued immediately upon approval and ready for online purchases instantly. The card is compatible with Apple Pay and Google Wallet for contactless NFC payments and is PIN-protected with static 3DS password for online security.

### What are the requirements for a GoMining Card?

To create a card, you need at least $100 in your GoMining wallet (calculated across all assets). KYC Level 1 and 2 verification is required. Up to 3 virtual cards per user at any time.

### What documents do I need?

European residents need a valid national passport/ID card plus proof of address under 3 months old. Global residents need a valid national passport/ID card (where supported) plus proof of address from non-prohibited jurisdictions.

### Are there fees for the GoMining Card?

There is no commission; however, GoMining uses an internal exchange rate, which might be different from publicly available sources.

### Are there restrictions on who can get a GoMining Card?

Certain nations' passports are rejected. Belarus and Russian passport holders must provide valid EEA+ residence permits. There are 60+ prohibited jurisdictions where card applications are not available.

---

## Official Resources

| Resource | URL |
|----------|-----|
| Cards FAQ | https://help.cards.gomining.com/ |
| Main Website | https://gomining.com/ |

---

## References

- [KYC Requirements](references/KYC-REQUIREMENTS.md) — Detailed verification process
- [Supported Regions](references/SUPPORTED-REGIONS.md) — Countries and restrictions
- [Exchange Rates](references/EXCHANGE-RATES.md) — How conversion rates work
- [FAQ: Card Overview](references/FAQ-OVERVIEW.md) — General overview of the GoMining Card product section
- [FAQ: About the GoMining Card](references/FAQ-ABOUT.md) — What the GoMining Card is and its key features
- [FAQ: Gift Miner](references/FAQ-GIFT-MINER.md) — How to get a free miner with the GoMining Card
- [FAQ: Payments](references/FAQ-PAYMENTS.md) — How payments work with the GoMining Card
- [FAQ: Card Security](references/FAQ-SECURITY.md) — Security features and best practices for the card
- [FAQ: Troubleshooting](references/FAQ-TROUBLESHOOTING.md) — Common card issues and how to resolve them
- [How-to: Card Instructions Overview](references/INSTRUCTION-OVERVIEW.md) — Overview of card how-to guides
- [How-to: Block or Unblock Your Card](references/INSTRUCTION-BLOCK.md) — Steps to block or unblock the GoMining Card
- [How-to: Change Email or Phone Number](references/INSTRUCTION-CHANGE-CONTACT.md) — How to update contact details for the card
- [How-to: Choose Crypto Asset for Payments](references/INSTRUCTION-CHOOSE-ASSET.md) — How to select which crypto to use for transactions
- [How-to: Get Your Virtual Card](references/INSTRUCTION-GET-CARD.md) — Step-by-step guide to issuing a virtual card
- [How-to: Set a New PIN Code](references/INSTRUCTION-PIN.md) — How to set or change your card PIN
- [How-to: Top Up and Withdrawal](references/INSTRUCTION-TOPUP.md) — How to fund and withdraw from your card wallet
- [How-to: View Your Card Details](references/INSTRUCTION-VIEW-DETAILS.md) — How to access card number, CVV, and expiry
- [How-to: Security Instructions Overview](references/INSTRUCTION-SECURITY-OVERVIEW.md) — Overview of security-related how-to guides
- [How-to: Pass Identity Verification (KYC)](references/INSTRUCTION-KYC.md) — How to complete KYC verification
- [How-to: Verify a GoMining Representative](references/INSTRUCTION-VERIFY-REP.md) — How to confirm you are speaking with official GoMining support
- [FAQ: Card Usage](references/FAQ-CARD-USAGE.md) — Where to use the card, ATM withdrawals, order status, email code
- [FAQ: Exchange Rates Policy](references/FAQ-EXCHANGE-RATES-POLICY.md) — Variable spreads, no fixed fees, top-up restrictions, transaction visibility
- [FAQ: Cashback Program](references/FAQ-CASHBACK.md) — How TH cashback works, eligible miners, daily crediting schedule
