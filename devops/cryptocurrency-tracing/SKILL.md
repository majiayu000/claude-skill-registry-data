---
name: "Cryptocurrency Tracing"
description: "Trace cryptocurrency wallet activity and blockchain transactions"
allowed-tools:
  - src.tools.crypto_trace
---

# Cryptocurrency Tracing

## Purpose

Trace cryptocurrency transactions, analyze wallet activities, and investigate blockchain-based financial flows for AML compliance, fraud investigation, and asset recovery.

## When to Use

- Anti-money laundering (AML) investigations
- Cryptocurrency fraud and theft investigation
- Sanctions compliance for digital assets
- Asset tracing and recovery efforts
- Investigation of ransomware payments
- Due diligence on cryptocurrency businesses
- Analysis of suspicious transaction patterns
- Compliance screening for crypto exchanges

## How to Use

The crypto tracing tool analyzes blockchain data across multiple cryptocurrencies:

- **Transaction Analysis**: Inputs, outputs, amounts, timestamps, fees
- **Wallet Investigation**: Address clustering, balance history, activity patterns
- **Flow Analysis**: Fund flows between addresses, mixing services, exchanges
- **Risk Assessment**: Sanctioned addresses, known criminal wallets, darknet markets
- **Exchange Attribution**: Deposits/withdrawals to known cryptocurrency exchanges
- **Pattern Recognition**: Unusual transaction patterns, potential money laundering

## Examples

**Ransomware investigation:**
```
Bitcoin Address: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
Analysis: Large payments from multiple victims, funds consolidated
Flow: Transfers through mixing service, then to exchange
Intelligence: Track to potential cash-out point for law enforcement
```

**AML compliance screening:**
```
Customer Wallet: 3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy
Investigation: Regular transactions with OFAC-sanctioned addresses
Risk: High - customer engaged with prohibited counterparties
Action: File suspicious activity report, freeze account
```

**Asset recovery:**
```
Stolen Funds: $500K in Ethereum from DeFi exploit
Tracing: Funds split across multiple addresses, some to exchanges
Recovery: Identify exchange wallets for freezing/recovery action
Legal: Coordinate with exchanges and law enforcement
```

**Due diligence on crypto business:**
```
Exchange Wallet: bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh
Analysis: High volume, multiple fiat off-ramps, compliance procedures
Risk Assessment: Low - legitimate exchange with proper AML controls
```

## Important Notes

- Blockchain analysis requires specialized tools and expertise
- Privacy coins (Monero, Zcash) present significant tracing challenges
- Mixing services and tumblers can obscure transaction flows
- Cross-chain bridges add complexity to tracing efforts
- Consider multiple blockchain networks (Bitcoin, Ethereum, others)
- Real-time monitoring may be needed for active investigations
- Coordinate with law enforcement for criminal investigations
- Be aware of evolving privacy technologies and countermeasures
- Document chain of custody for potential legal proceedings
- Stay current with sanctions lists for cryptocurrency addresses