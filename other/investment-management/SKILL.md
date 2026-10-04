---
name: investment-management
category: finance
description: "Investment management skill — portfolio construction, analysis, and execution. Compounds finance-substrate (accounting/tax) + wealth-management (projections/goals) into a full financial framework. Covers traditional investing (stocks, ETFs, bonds), alternatives (crypto, prediction markets, real estate, VC), quantitative analytics (factor models, Monte Carlo, optimization), and platform integration (Alpaca, Coinbase, Polymarket, agent-browser for Colombian platforms). Embodies philosophies from Buffett, Dalio, Bogle, Munger, and Marks. Use when: (1) building or analyzing a portfolio, (2) screening stocks/ETFs/crypto, (3) running backtests or factor analysis, (4) executing trades or rebalancing, (5) tracking investments across platforms, (6) researching market data or fundamentals, (7) making investment decisions with structured frameworks. Triggers on 'investment', 'portfolio', 'stocks', 'ETF', 'bonds', 'crypto', 'trading', 'backtest', 'factor model', 'rebalance', 'Polymarket', 'Alpaca', 'asset allocation'."
---

# Investment Management

Full-stack investment management: from philosophy to execution. Research, analyze,
decide, execute, track, and optimize across traditional and alternative asset classes.

## Financial Management Stack

```
finance-substrate (Layer 1: Accounting & Tax)
  ├── Bank transaction import, certificate parsing
  ├── Form 210 tax projection, DIAN integration
  ├── Parafiscales, patrimonio, retenciones
  └── Gmail document collector
        ↓
wealth-management (Layer 2: Planning & Projections)
  ├── Compound growth projections
  ├── Goal-based planning, Monte Carlo
  ├── Portfolio summary & asset allocation
  └── Budget planning with tax savings
        ↓
investment-management (Layer 3: Analysis & Execution)  ← THIS SKILL
  ├── RESEARCH:   Market data, fundamentals, screening
  ├── ANALYZE:    Factor models, backtests, risk metrics
  ├── DECIDE:     Philosophy-driven frameworks, scoring
  ├── EXECUTE:    Trade via APIs (Alpaca, Coinbase, Polymarket)
  ├── TRACK:      Multi-platform position aggregation
  └── OPTIMIZE:   Rebalancing, tax-loss harvesting, lot management
```

## Investment Philosophies (Built-in Frameworks)

The skill embeds decision frameworks from legendary investors.
Each philosophy is a scoring lens that can be applied to any investment.

### Value (Buffett/Graham/Munger)

| Principle | Implementation |
|-----------|---------------|
| Economic moat analysis | Score competitive advantage: brand, network, switching cost, scale |
| Margin of safety | Require 25%+ discount to intrinsic value (DCF, owner earnings) |
| Circle of competence | Flag unfamiliar sectors; require deeper research threshold |
| Owner earnings | Net income + depreciation - capex (not GAAP earnings) |
| Quality over price | ROIC > WACC, consistent ROE > 15%, low debt/equity |

### Systematic (Dalio/AQR)

| Principle | Implementation |
|-----------|---------------|
| All-Weather allocation | Risk-parity: equal risk contribution from growth, inflation, deflation |
| Factor exposure | Decompose returns into market, value, momentum, quality, size |
| Risk parity | Weight by inverse volatility, target equal risk contribution |
| Regime awareness | Detect growth/inflation quadrant, adjust allocation |
| Correlation regime | Monitor rolling correlations; diversification fails in crises |

### Passive/Index (Bogle)

| Principle | Implementation |
|-----------|---------------|
| Three-fund portfolio | Total market + international + bonds; rebalance annually |
| Minimize costs | Flag any fund with expense ratio > 0.20% |
| Tax efficiency | Index funds in taxable, bonds in tax-deferred |
| Stay the course | Reject market timing; dollar-cost average |
| Simple beats complex | Baseline comparison for every active strategy |

### Second-Level Thinking (Marks)

| Principle | Implementation |
|-----------|---------------|
| Consensus vs reality | Flag positions where market consensus is priced in |
| Risk is not volatility | Focus on permanent capital loss, not price fluctuation |
| Market cycles | Track Shiller CAPE, yield spreads, sentiment indicators |
| Asymmetric outcomes | Seek situations where upside >> downside |
| Know what you don't know | Confidence-weighted recommendations |

### Barbell (Taleb)

| Principle | Implementation |
|-----------|---------------|
| 85% ultra-safe + 15% high-convexity | Split portfolio into safe (CDTs, treasuries) + optionality (crypto, VC, prediction markets) |
| Antifragile positions | Identify investments that benefit from volatility |
| Avoid the middle | Skip mediocre risk-return profiles |
| Small bets, big payoffs | Position size by max loss tolerance, not expected return |

## Skill Modes

### 1. `screen` — Security Screening

Search and filter stocks, ETFs, crypto, and other securities by criteria.

**Script:** `scripts/screener.py`

**Screening criteria:**
- Fundamental: P/E, P/B, EV/EBITDA, FCF yield, ROIC, ROE, debt/equity, dividend yield
- Technical: RSI, MACD signal, price vs 200-day MA, 52-week range position
- Quality: earnings consistency, revenue growth, margin stability
- Momentum: 1/3/6/12-month returns, relative strength
- Value composite: Piotroski F-Score, Greenblatt Magic Formula rank
- Size: market cap filters

**Data sources:** yfinance, Financial Modeling Prep, OpenBB

### 2. `research` — Deep Investment Research — **(Planned — not yet implemented)**

In-depth analysis of a specific security or market.

**Status:** Planned — `scripts/research.py` is not yet shipped. Do not invoke; this mode is a roadmap stub.

**Analysis includes:**
- Company overview and business model
- Financial statement analysis (3-5 year trends)
- Valuation: DCF, comparable companies, dividend discount
- Competitive landscape and moat assessment
- Risk factors and bear case
- Catalyst identification
- Philosophy alignment score (which frameworks support/oppose)

**Data sources:** yfinance fundamentals, SEC EDGAR (edgartools), news sentiment (FinBERT)

### 3. `factor` — Factor Analysis — **(Planned — not yet implemented)**

Decompose portfolio returns into systematic factor exposures.

**Status:** Planned — `scripts/factor_analysis.py` is not yet shipped. Do not invoke; this mode is a roadmap stub.

**Factors analyzed:**
- Fama-French 5 factors: Market, Size (SMB), Value (HML), Profitability (RMW), Investment (CMA)
- Momentum (UMD)
- Quality (QMJ from AQR)
- Alpha: residual return not explained by factors

**Output:** Factor loadings, R², alpha significance, factor exposure drift over time

### 4. `backtest` — Strategy Backtesting

Test investment strategies against historical data.

**Script:** `scripts/backtest.py`

**Built-in strategies:**
- Buy and hold (benchmark)
- Equal-weight rebalanced
- Risk parity (inverse vol)
- Momentum (top N by 12-1 month return)
- Value (top N by composite score)
- All-Weather (Dalio's 4-quadrant allocation)
- Custom (user-defined rules)

**Metrics:** CAGR, Sharpe, Sortino, max drawdown, Calmar, win rate, average gain/loss

### 5. `optimize` — Portfolio Optimization — **(Planned — not yet implemented)**

Find optimal portfolio weights given constraints.

**Status:** Planned — `scripts/portfolio_optimizer.py` is not yet shipped. Do not invoke; this mode is a roadmap stub.

**Methods:**
- Mean-variance (Markowitz efficient frontier)
- Black-Litterman (market equilibrium + personal views)
- Hierarchical Risk Parity (HRP, no covariance inversion)
- Risk budgeting (equal risk contribution)
- Maximum Sharpe, minimum volatility, target return
- CVaR optimization (tail-risk aware)

**Constraints:** Long-only, sector limits, position size caps, turnover limits, tax-awareness

**Libraries:** PyPortfolioOpt, Riskfolio-Lib, cvxpy

### 6. `risk` — Risk Analysis — **(Planned — not yet implemented)**

Comprehensive risk assessment of current or proposed portfolio.

**Status:** Planned — `scripts/risk_analysis.py` is not yet shipped. Do not invoke; this mode is a roadmap stub.

**Metrics:**
- Value at Risk (parametric, historical, Monte Carlo)
- Conditional VaR (Expected Shortfall)
- Maximum drawdown analysis
- Stress tests: 2008 GFC, 2020 COVID, 2022 rates, COP devaluation
- Correlation regime analysis (rolling correlations)
- GARCH volatility forecast
- Concentration risk and single-name exposure

### 7. `trade` — Trade Execution — **(Planned — not yet implemented)**

Execute trades via supported platform APIs.

**Status:** Planned — `scripts/trade.py` is not yet shipped. Do not invoke; this mode is a roadmap stub. (For a working, paper-only execution loop today, use `services/tradingview-bridge` — see below.)

**Supported platforms:**

| Platform | Assets | Auth | Library |
|----------|--------|------|---------|
| Alpaca | US stocks, ETFs | API key pair | `alpaca-trade-api` |
| Coinbase | Crypto | CDP API key + JWT | `coinbase-advanced-py` |
| Polymarket | Prediction markets | Wallet signature | `py-clob-client` |
| Interactive Brokers | Everything | TWS API | `ib_async` |

**Features:**
- Paper trading mode (default) — no real money until explicitly confirmed
- Order types: market, limit, stop-loss
- Position sizing: Kelly criterion, fixed fractional, risk-budget
- Pre-trade checks: liquidity, spread, portfolio impact

### 8. `track` — Multi-Platform Position Tracking — **(Planned — not yet implemented)**

Aggregate positions across all investment platforms.

**Status:** Planned — `scripts/tracker.py` is not yet shipped. Do not invoke; this mode is a roadmap stub.

**Sources (in priority order):**
1. API-connected platforms (Alpaca, Coinbase) — real-time
2. finance-substrate certificates (Skandia, Davivienda, etc.) — periodic
3. Browser-automated platforms (Tyba, Trii, Davivienda Corredores) — via agent-browser
4. Manual entries (portfolio.json) — user-maintained

**Output:** Unified position list with cost basis, current value, unrealized gain/loss, allocation %

### 9. `rebalance` — Intelligent Rebalancing — **(Planned — not yet implemented)**

Generate and optionally execute rebalancing trades.

**Status:** Planned — `scripts/rebalancer.py` is not yet shipped. Do not invoke; this mode is a roadmap stub.

**Rebalancing modes:**
- Cash-flow (direct new contributions to underweight positions)
- Threshold (trigger when drift exceeds band)
- Tax-aware (prefer loss-harvesting sells, defer gains)
- Calendar (monthly/quarterly/annual schedule)

**Tax-loss harvesting:**
- Scan for positions with unrealized losses
- Identify replacement securities (correlated but not identical)
- Track wash sale windows (30 days US; no equivalent in Colombia)
- Estimate tax savings

### 10. `data` — Market Data Retrieval

Fetch market data from multiple sources.

**Script:** `scripts/market_data.py`

**Sources:**

| Source | Data | Cost | Library |
|--------|------|------|---------|
| yfinance | US/intl stocks, fundamentals | Free | `yfinance` |
| Financial Modeling Prep | Financial statements, ratios | Free tier | `fmpsdk` |
| CoinGecko | Crypto prices, market data | Free tier | `pycoingecko` |
| FRED | Macro indicators (800K series) | Free | `fredapi` |
| datos.gov.co | TRM (USD/COP) | Free | `requests` |
| Banco de la República | CPI, interest rates | Free | `requests` |
| Alpha Vantage | Technical data, forex | Free tier | `alpha_vantage` |
| Polymarket | Prediction market odds | Free | `py-clob-client` |

### 11. `score` — Investment Scoring

Score a security through multiple investment philosophy lenses.

**Script:** `scripts/scorer.py`

**Scoring dimensions:**
- Value score (Graham/Buffett): P/E, P/B, FCF yield, moat rating
- Quality score (Munger): ROIC, margin stability, debt discipline
- Momentum score: price momentum, earnings momentum, analyst revisions
- Risk score (Marks): downside volatility, max drawdown, tail risk
- Growth score (Lynch): revenue growth, PEG ratio, addressable market
- Composite score: weighted average across all dimensions

**Output:** 0-100 score per dimension, overall composite, philosophy alignment

## Asset Class Coverage

### Traditional
| Class | Screening | Research | Trading | Tracking |
|-------|-----------|----------|---------|----------|
| US Stocks | yfinance, FMP | EDGAR, fundamentals | Alpaca, IBKR | API |
| International Stocks | yfinance | Limited fundamentals | IBKR | API |
| ETFs | yfinance | Holdings analysis | Alpaca, IBKR | API |
| Bonds/Fixed Income | FRED yield curves | Duration, credit | IBKR | Manual |
| CDTs (Colombia) | Superfinanciera rates | Yield comparison | Manual | Certificates |

### Alternative
| Class | Screening | Research | Trading | Tracking |
|-------|-----------|----------|---------|----------|
| Crypto | CoinGecko, CMC | On-chain, sentiment | Coinbase, Binance | API |
| Prediction Markets | Polymarket API | Market analysis | Polymarket CLOB | API |
| Real Estate | Manual | Cap rate, appreciation | Manual | Exogena/manual |
| VC/Startups | Manual | Due diligence framework | Manual | Manual |
| Colombian Equities | Yahoo (BVC tickers) | Limited | Davivienda Corredores (browser) | Browser/manual |

### Tax-Advantaged (Colombia)
| Vehicle | Max Benefit | Tracking |
|---------|-----------|----------|
| AFC (Davivienda) | 1,340 UVT cap | finance-substrate certs |
| Pensión Voluntaria (Skandia) | Combined w/ AFC | finance-substrate certs |
| Cesantías | Forced savings | finance-substrate certs |

## Platform Integration Architecture

```
investment-management
  │
  ├── API-first (real-time)
  │   ├── Alpaca ──── US stocks, ETFs (paper + live)
  │   ├── Coinbase ── Crypto (BTC, ETH, SOL, etc.)
  │   ├── Polymarket ── Prediction markets
  │   ├── CoinGecko ── Crypto market data
  │   ├── FRED ──── Macro indicators
  │   └── yfinance ── Stock data, fundamentals
  │
  ├── Browser-automated (agent-browser)
  │   ├── Davivienda Corredores ── Colombian equities
  │   ├── Tyba ── Colombian robo-advisor
  │   ├── Skandia Portal ── Pension fund data
  │   └── MiDataCredito ── Credit profile
  │
  ├── File-based (finance-substrate)
  │   ├── certificates.jsonl ── Bank saldos, investment funds
  │   ├── exogena.jsonl ── Third-party reported assets
  │   └── salary-history.jsonl ── Income trajectory
  │
  └── Manual (portfolio.json)
      ├── Private investments
      ├── Real estate
      └── VC/startup positions
```

### Autonomous decision plane — `services/tradingview-bridge`

A self-contained, **paper-only, human-gated** trading control system: a webhook
receiver + multi-broker executor, plus a closed self-improving loop — `research`
(walk-forward + anti-overfit scoring), `optimize` (EGRI param search with a true
train/test holdout), and `roster` (human-gated promotion of optimized params into
the roster the orchestrator measures). Drives TradingView's Paper simulator via the
Interceptor CLI (no inbound API), or runs the entire decision loop on synthetic/CSV
bars with no browser or broker. It measures and recommends — it never moves live
capital on its own.

→ **[services/tradingview-bridge/QUICKSTART.md](./services/tradingview-bridge/QUICKSTART.md)**
(install + the loop in 60 seconds) · [full reference](./services/tradingview-bridge/README.md)

## Quantitative Toolkit

### Libraries Used

| Purpose | Library | Install |
|---------|---------|---------|
| Portfolio optimization | PyPortfolioOpt | `pip install pyportfolioopt` |
| Advanced risk optimization | Riskfolio-Lib | `pip install riskfolio-lib` |
| Custom optimization | cvxpy | `pip install cvxpy` |
| Volatility modeling | arch | `pip install arch` |
| Technical indicators | pandas-ta | `pip install pandas_ta` |
| Factor data | pandas-datareader | `pip install pandas-datareader` |
| Backtesting | VectorBT | `pip install vectorbt` |
| Sentiment | transformers (FinBERT) | `pip install transformers` |
| Fundamental data | edgartools | `pip install edgartools` |
| Macro data | fredapi | `pip install fredapi` |

### Key Formulas

| Formula | Expression | Use |
|---------|-----------|-----|
| Sharpe Ratio | (R_p - R_f) / σ_p | Risk-adjusted return |
| Sortino Ratio | (R_p - R_f) / σ_downside | Downside risk-adjusted |
| Kelly Fraction | (bp - q) / b | Optimal position size |
| Intrinsic Value (DCF) | Σ FCF_t / (1+r)^t + TV | Valuation |
| WACC | E/(E+D)×Re + D/(E+D)×Rd×(1-T) | Discount rate |
| Black-Scholes | C = S·N(d1) - K·e^(-rT)·N(d2) | Option pricing |
| VaR (parametric) | μ - z_α × σ | Tail risk |
| CVaR | E[L \| L > VaR] | Expected tail loss |
| HHI (concentration) | Σ w_i² | Diversification |

## Data Directory

```
~/.investment-management/
├── portfolio.json              # Master holdings (all platforms)
├── targets.json                # Target allocation by strategy
├── watchlist.json              # Securities under observation
├── trades/                     # Trade history
│   └── trades.jsonl            # All executed trades
├── research/                   # Security research cache
│   └── research-{ticker}.json
├── backtests/                  # Backtest results
│   └── backtest-{strategy}-{date}.json
├── scores/                     # Investment scores
│   └── scores-{date}.json
├── market-data/                # Cached market data
│   ├── prices/                 # Historical price cache
│   └── fundamentals/           # Fundamental data cache
└── config/
    ├── api-keys.json           # Platform API keys (encrypted)
    ├── strategies.json         # Active strategy configurations
    └── rebalance-rules.json    # Rebalancing parameters
```

## Compound: Autoany Integration (EGRI)

This skill is EGRI-aware. When a user's request implies iterative optimization
or strategy search, the agent should scaffold a problem-spec from the templates
below and delegate to `/autoany` for autonomous improvement.

### Optimization Triggers

Invoke `/autoany` when the user asks to:
- **"Optimize"** — allocation, weights, strategy parameters
- **"Find the best"** — strategy, allocation, screening criteria
- **"Compare strategies"** — systematic comparison across N variants
- **"Backtest variations"** — test parameter sweeps
- **"What if I changed"** — sensitivity analysis via mutations
- **"Stress test"** — combined with optimization intent

### EGRI Problem-Spec Templates

| Template | Artifact | Evaluator | Score | Use When |
|----------|----------|-----------|-------|----------|
| `strategy-optimization` | `strategy.yaml` (weights, rules) | `backtest.py --egri` | Sharpe ratio | Optimizing portfolio allocation |
| `screen-evolution` _(planned)_ | `screen_criteria.yaml` (thresholds) | `screener.py` + `eval_screen.py` _(`eval_screen.py` not yet shipped)_ | Forward return | Evolving stock selection criteria |

The `strategy-optimization` loop is live (`backtest.py --egri` ships). The
`screen-evolution` loop is **planned** — its `eval_screen.py` evaluator is not
yet implemented. Templates are at `templates/egri/`. The strategy artifact
schema is at `templates/egri/strategy-artifact.yaml`.

### Delegation Flow

```
1. User request → agent detects optimization intent
2. Load personal context from finance-substrate (patrimonio, salary, TRM)
3. Pull historical market data (market_data.py)
4. Scaffold problem-spec from template, fill in:
   - Starting allocation as baseline artifact
   - Period, constraints from policy.yaml
   - Goal metrics from user's request
5. Invoke /autoany with scaffolded problem-spec
6. EGRI loop runs: Proposer → Executor (backtest.py) → Evaluator → Selector
7. Return promoted strategy + ledger summary to user
8. Log results for cross-session strategy inheritance (autoany-lago)
```

### EGRI Evaluator Bridge

`scripts/eval_backtest.py` wraps `backtest.py` for use as an EGRI evaluator:
- Takes a strategy YAML artifact + period
- Returns structured `Outcome` (score, constraints_passed, violations)
- Applies constraint expressions from the problem-spec
- Can be used standalone: `python3 eval_backtest.py --strategy-file strategy.yaml --period 10y`

### Safety Constraints (enforced in EGRI loops)

- EGRI loops over **historical data are autonomous** (sandbox mode)
- EGRI loops that **propose live trades require human gate** (HumanGate selector)
- Max drawdown constraint: `-15%` (from policy S6)
- Position concentration: `<= 25%` (from policy S2)
- Budget: 50 trials max, 1 hour total
- All trials logged to ledger for audit and cross-run inheritance

## Dependencies

- Python 3.10+
- `finance-substrate` skill (accounting, tax, certificates)
- `wealth-management` skill (projections, goals, portfolio summary)
- `autoany` (optional, for EGRI optimization loops)
- Market data: `yfinance`, `fredapi`, `pycoingecko` (free)
- Optimization: `pypfopt`, `riskfolio-lib`, `cvxpy` (optional, for advanced modes)
- Trading: `alpaca-trade-api`, `coinbase-advanced-py` (optional, for execution)
- Technical: `pandas-ta`, `arch` (optional, for quantitative modes)
- No paid services required. All data stays local.

## File Structure

**Shipped (live today):**

```
investment-management/
├── SKILL.md                          # This file
├── skill.json                        # Schema definition (11 modes; 4 live, 7 planned)
├── scripts/
│   ├── screener.py                   # Mode 1 (screen): security screening
│   ├── backtest.py                   # Mode 4 (backtest): strategy backtesting (+ --egri)
│   ├── market_data.py                # Mode 10 (data): data retrieval
│   ├── scorer.py                     # Mode 11 (score): investment scoring
│   └── eval_backtest.py              # EGRI evaluator wrapper (autoany bridge)
├── references/
│   └── investment-philosophies.md    # Legendary investor frameworks
├── templates/
│   └── egri/                         # EGRI problem-spec templates (autoany)
│       ├── strategy-optimization.yaml   # Portfolio strategy optimization
│       ├── screen-evolution.yaml        # Screening criteria evolution (evaluator planned)
│       └── strategy-artifact.yaml       # Strategy YAML schema (mutable artifact)
├── services/
│   └── tradingview-bridge/           # Paper-only, human-gated trading decision plane
└── README.md
```

**Planned — not yet shipped (roadmap; do not invoke):**

```
scripts/research.py                # Mode 2 (research)
scripts/factor_analysis.py         # Mode 3 (factor)
scripts/portfolio_optimizer.py     # Mode 5 (optimize)
scripts/risk_analysis.py           # Mode 6 (risk)
scripts/trade.py                   # Mode 7 (trade)
scripts/tracker.py                 # Mode 8 (track)
scripts/rebalancer.py              # Mode 9 (rebalance)
scripts/eval_screen.py             # EGRI evaluator for screen-evolution
references/platform-apis.md        # API reference for all platforms
references/quantitative-toolkit.md # Libraries, formulas, models
references/colombian-markets.md    # BVC, CDTs, FICs, regulations
references/alternative-investments.md  # Crypto, prediction markets, RE, VC
templates/strategies.json          # Pre-built strategy configurations
templates/scoring-weights.json     # Philosophy scoring weights
.control/policy.yaml               # Trading limits, risk gates
```
