---
name: crypto-pair-fee-optimization
description: "Analysis of crypto-to-crypto vs crypto-to-fiat (USD) trading on Alpaca for fee optimization and risk considerations"
author: Claude Code
date: 2026-01-01
---

# Crypto Pair Fee Optimization - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2026-01-01 |
| **Goal** | Determine if crypto-to-crypto trading is advantageous vs crypto-to-fiat given Alpaca fee schedule and risk factors |
| **Environment** | Alpaca Crypto LLC, Fee schedule as of Aug 2023 |
| **Status** | Success |

## Context
When rebalancing crypto portfolios or rotating between assets, there are two approaches:
1. **Crypto-to-USD route**: Sell asset A for USD, buy asset B with USD (2 trades)
2. **Crypto-to-crypto route**: Trade asset A directly for asset B (1 trade)

The question: Does Alpaca's fee structure favor one approach over the other?

## Key Finding: Fee Structure is Identical

Per `docs/rules_and_fees/AlpacaCryptoLLCFeeDisclosure.pdf`, Alpaca uses the **same maker/taker fees** regardless of pair type:

| Tier | 30D Volume (USD) | Maker | Taker |
|------|------------------|-------|-------|
| 1 | $0 - 100K | 0.15% | 0.25% |
| 2 | $100K - 500K | 0.12% | 0.22% |
| 3 | $500K - 1M | 0.10% | 0.20% |
| 4 | $1M - 10M | 0.08% | 0.18% |
| 5 | $10M - 25M | 0.05% | 0.15% |
| 6 | $25M - 50M | 0.02% | 0.13% |
| 7 | $50M - 100M | 0.02% | 0.12% |
| 8 | $100M+ | 0.00% | 0.10% |

**No per-trade fee advantage exists between pair types.**

## Verified Advantage: Trade Count Reduction

The only fee advantage comes from reducing the number of trades:

| Scenario | Crypto-to-USD Route | Crypto-to-Crypto Route | Savings |
|----------|---------------------|------------------------|---------|
| Rotate ETH → BTC | ETH→USD + USD→BTC = 2×0.25% = **0.50%** | ETH→BTC = **0.25%** | **50%** |
| Rebalance 3 assets | Up to 6 trades | Up to 3 trades | **50%** |

```python
# Fee calculation for portfolio rotation
def calculate_rotation_fees(num_assets: int, fee_rate: float = 0.0025) -> dict:
    """Compare fees for crypto rotation strategies."""
    # Via USD: sell all to USD, buy new positions
    usd_route_trades = num_assets * 2  # sell + buy for each
    usd_route_fee = usd_route_trades * fee_rate

    # Via crypto pairs: direct swaps where available
    crypto_route_trades = num_assets  # direct swaps
    crypto_route_fee = crypto_route_trades * fee_rate

    return {
        'usd_route_trades': usd_route_trades,
        'usd_route_fee_pct': usd_route_fee * 100,
        'crypto_route_trades': crypto_route_trades,
        'crypto_route_fee_pct': crypto_route_fee * 100,
        'savings_pct': (1 - crypto_route_fee / usd_route_fee) * 100
    }
```

## When Crypto-to-Crypto is Advantageous

1. **Portfolio rebalancing** - Rotating between crypto assets you intend to hold
2. **Stablecoin parking** - Using USDC/USDT pairs to avoid USD conversion delays
3. **Tax strategy** - Potentially avoiding USD realization events (jurisdiction-dependent, consult tax advisor)

## When Crypto-to-USD is Better

1. **Profit realization** - Converting to USD for withdrawal/spending
2. **Risk-off moves** - USD doesn't fluctuate while waiting to re-enter
3. **Simpler accounting** - USD basis is clearer for tax reporting
4. **Wider liquidity** - USD pairs typically have tighter spreads

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Assuming crypto pairs have lower fees | Fee schedule is identical per trade | Advantage is only in trade count reduction |
| Looking for spread differences in docs | Alpaca doesn't publish spread data | Would need live testing to compare actual execution costs |

## Risk Considerations

```yaml
# Risk factors for crypto-to-crypto pairs
double_volatility_exposure: true  # Both sides of trade can move
liquidity_variance: "USD pairs typically deeper"
spread_risk: "Exotic pairs may have wider spreads"
implementation_complexity: "Requires broker/backtest updates"
```

## Available Alpaca Crypto Pairs

```yaml
# Base currencies for crypto-to-crypto
BTC_pairs: [BCH, ETH, LTC, UNI]
USDT_pairs: [AAVE, BCH, BTC, DOGE, ETH, LINK, LTC, SUSHI, UNI, YFI]
USDC_pairs: [AAVE, AVAX, BAT, BCH, BTC, CRV, DOGE, DOT, ETH, GRT, LINK, LTC, SHIB, SKY, SUSHI, UNI, XTZ, YFI]
USD_pairs: "20+ assets including all USDC/USDT options plus XRP"
```

## Implementation Notes

Current codebase trades crypto/USD only (e.g., `BTC/USD`). To implement crypto-to-crypto:

1. Update `alpaca_trading/trading/broker.py` to handle non-USD quote currencies
2. Modify backtest infrastructure for multi-base accounting
3. Add fee calculation that tracks the "credited side" denomination
4. Consider liquidity/spread modeling for exotic pairs

## Key Insights

- Fee percentages are identical across all pair types on Alpaca
- The only fee advantage is reducing trade count (50% savings on rotations)
- Crypto-to-crypto exposes you to volatility on both sides of the trade
- Stablecoin pairs (USDC/USDT) offer a middle ground: crypto liquidity with USD-like stability
- Implementation requires non-trivial changes to broker and backtest systems

## References

- `docs/rules_and_fees/AlpacaCryptoLLCFeeDisclosure.pdf` (local)
- [Alpaca Crypto Fees Documentation](https://docs.alpaca.markets/docs/crypto-fees)
- [Alpaca Crypto Coin Pair FAQ](https://alpaca.markets/support/alpaca-crypto-coin-pair-faq)
- [Alpaca Crypto Trading Documentation](https://docs.alpaca.markets/docs/crypto-trading)
