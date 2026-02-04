---
name: nvidia-supply-chain-analysis
description: Comprehensive toolkit for analyzing and anticipating Nvidia and semiconductor supply chain stock movements. Use when users need to (1) analyze Nvidia ecosystem dependencies and correlations, (2) identify trading opportunities across the supply chain, (3) track earnings catalysts and events, (4) understand bottlenecks and risk factors, (5) develop supply chain investment strategies, or (6) monitor technical indicators and momentum across semiconductor names. Provides real-time data fetching, technical analysis, fundamental relationships mapping, and predictive signals based on supply chain dynamics.
---

# Nvidia Supply Chain Analysis

Advanced toolkit for analyzing the complete Nvidia semiconductor supply chain ecosystem, identifying trading opportunities, and anticipating market movements based on supply chain dynamics.

## Quick Start

For immediate analysis of current supply chain status:

```bash
# Full supply chain overview with signals
python scripts/fetch_supply_chain_data.py --format summary

# Technical analysis scan for opportunities  
python scripts/technical_analysis.py --scan

# Upcoming earnings catalysts
python scripts/earnings_calendar.py
```

## Core Analysis Workflows

### 1. Supply Chain Health Assessment

Evaluate the current state of Nvidia's supply chain:

```bash
# Fetch comprehensive supply chain data
python scripts/fetch_supply_chain_data.py

# Review correlations and dependencies
# Look for correlation breaks (<0.3) as opportunity signals
# Monitor companies with beta >1.5 for leveraged exposure
```

Key metrics to examine:
- **Correlation to NVDA**: >0.7 indicates tight coupling
- **3-month momentum**: Identify leaders and laggards
- **Volatility**: >50% suggests elevated risk
- **Volume patterns**: Unusual volume precedes moves

### 2. Trading Signal Generation

Identify actionable opportunities across the ecosystem:

```bash
# Scan for technical buy/sell signals
python scripts/technical_analysis.py --scan

# Deep dive on specific ticker
python scripts/technical_analysis.py --ticker TSM --period 6mo
```

Signal priorities:
1. **RSI extremes** (<30 or >70) with volume confirmation
2. **MACD crossovers** in Tier-2/3 suppliers
3. **Breakout patterns** in equipment stocks (leading indicators)
4. **Bollinger Band** squeezes in memory names

### 3. Event-Driven Analysis

Track and anticipate catalyst impacts:

```bash
# Get complete event calendar
python scripts/earnings_calendar.py --calendar

# Analyze specific ticker's earnings impact
python scripts/earnings_calendar.py --ticker NVDA
```

Earnings sequence strategy:
1. Equipment companies report first → Leading signal
2. Memory suppliers → Pricing/supply updates
3. TSMC → Manufacturing confirmation
4. Nvidia → Final confirmation
5. System integrators → Deployment trends

### 4. Bottleneck Identification

Monitor critical constraints:

```python
# Check HBM availability (primary bottleneck)
python scripts/fetch_supply_chain_data.py --ticker SK
python scripts/fetch_supply_chain_data.py --ticker MU

# CoWoS packaging capacity (secondary bottleneck)
python scripts/technical_analysis.py --ticker TSM
```

Current bottlenecks (2024-2025):
- **HBM3/HBM3E memory**: SK Hynix, Micron
- **Advanced packaging**: TSMC CoWoS
- **EUV capacity**: ASML equipment delivery

### 5. Pair Trading Opportunities

Identify and execute relative value trades:

```python
# Compare correlated pairs
# High correlation pairs (>0.7): NVDA/TSM, AMAT/LRCX
# Competitive pairs: NVDA/AMD, TSM/INTC
# Memory pairs: MU/SK

# Look for 2+ standard deviation spreads
```

## Supply Chain Tiers & Dependencies

For detailed relationships, consult: `references/supply_chain_map.md`

### Critical Dependencies
- **NVDA → TSM**: 100% of advanced GPU production
- **TSM → ASML**: EUV lithography monopoly
- **NVDA → SK Hynix**: Primary HBM supplier
- **NVDA → SMCI**: Server integration partner

### Risk Propagation
- Equipment orders → 6-9 month signal
- Foundry utilization → 3-4 month signal  
- Memory pricing → 2-3 month signal
- Hyperscaler capex → 2-3 month signal

## Advanced Analysis Strategies

For comprehensive strategies, see: `references/analysis_strategies.md`

### Leading Indicator Sequence
1. **ASML backlog** → Future capacity (9-12 months)
2. **Equipment billings** → Capacity additions (6-9 months)
3. **TSM utilization** → Supply tightness (3-4 months)
4. **Memory pricing** → Cost pressures (2-3 months)
5. **Hyperscaler capex** → Demand signals (1-3 months)

### Portfolio Construction
```
Aggressive Growth (Higher Risk):
- 40% NVDA
- 20% SMCI  
- 20% Equipment (ASML, AMAT)
- 20% Memory (MU, SK)

Balanced Exposure:
- 30% NVDA
- 30% TSM
- 20% Equipment basket
- 10% Memory
- 10% System integrators

Conservative/Hedged:
- 25% NVDA
- 25% TSM
- 25% Diversified equipment
- 15% Large-cap integrators (DELL, HPE)
- 10% Cash/Hedges
```

## Risk Management

### Key Risk Factors
1. **Taiwan geopolitical risk** - Affects TSM, ASX
2. **China restrictions** - Impacts equipment 20-30% revenue
3. **Technology transitions** - 3nm migration risks
4. **Competitive threats** - AMD, Intel alternatives
5. **Demand digestion** - Hyperscaler pause risk

### Hedging Strategies
- Put spreads on high-beta names before earnings
- Inverse semiconductor ETFs (SOXS) for systemic hedges
- Pair trades to neutralize market risk
- Geographic diversification (Korea, Europe, US)

## Real-Time Monitoring

### Daily Checklist
1. Pre-market: Check Asian suppliers (TSM, SK Hynix)
2. Equipment stocks as leading indicators
3. Memory pricing trends
4. Unusual options activity
5. Correlation breaks or extremes

### Weekly Review
- Supply chain aggregate momentum
- Earnings calendar updates
- Insider transaction patterns
- Analyst revision trends
- Technical setup scans

### Event Preparation
- Reduce exposure before equipment earnings
- Add on supply chain confirmation
- Hedge before NVDA reports
- Watch for cluster catalysts

## Resources

### scripts/
Python scripts for real-time analysis and signal generation:

- `fetch_supply_chain_data.py`: Fetches current prices, calculates correlations, identifies momentum leaders/laggards across the Nvidia supply chain
- `technical_analysis.py`: Generates trading signals using RSI, MACD, Bollinger Bands, identifies patterns and breakouts
- `earnings_calendar.py`: Tracks upcoming earnings dates, analyzes historical price impacts, identifies catalyst clusters

### references/
Comprehensive documentation for supply chain relationships and strategies:

- `supply_chain_map.md`: Complete mapping of Nvidia ecosystem with tier classifications, dependencies, risk factors, and signal propagation patterns
- `analysis_strategies.md`: Advanced trading strategies including fundamental frameworks, technical patterns, sentiment analysis, and portfolio construction

### assets/
This skill does not require asset files - delete the example_asset.txt file.
