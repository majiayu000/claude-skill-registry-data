---
name: wealth-management
category: finance
description: >
  Wealth management, financial planning, and investment analytics skill.
  Compounds on finance-substrate for Colombian tax-optimized wealth building.
  Runs descriptive (portfolio health), predictive (compound growth projections,
  Monte Carlo), and prescriptive (allocation, rebalancing, tax-efficient
  withdrawal) analytics. Use when: (1) projecting long-term wealth growth,
  (2) optimizing asset allocation, (3) running scenario/stress tests on a
  portfolio, (4) planning tax-efficient contributions or withdrawals,
  (5) generating a wealth dashboard or net worth timeline,
  (6) goal-based financial planning (retirement, housing, education).
  Triggers on: 'wealth management', 'compound interest', 'asset allocation',
  'portfolio projection', 'net worth forecast', 'retirement planning',
  'investment strategy', 'rebalancing', 'monte carlo', 'financial plan'.
---

# Wealth Management

Long-term wealth building, investment analytics, and financial planning engine.
Builds on `finance-substrate` for data ingestion (bank certificates, patrimonio,
TRM rates, salary history) and adds forward-looking projection, optimization,
and scenario analysis.

## Architecture

```
finance-substrate (data layer)
  ├── certificates.jsonl     → current holdings, bank saldos
  ├── patrimonio_calc.py     → net worth snapshot (R29/R30/R31)
  ├── tax_projection.py      → annual tax liability
  ├── salary-history.jsonl   → income trajectory
  └── trm-history.jsonl      → FX rates
        ↓
wealth-management (analytics layer)
  ├── Descriptive:  portfolio health, allocation drift, performance
  ├── Predictive:   compound growth, Monte Carlo, goal feasibility
  └── Prescriptive: rebalancing trades, contribution strategy, withdrawal order
```

## Data Sources

### From finance-substrate (automatic)

| Source | Data | Used by |
|--------|------|---------|
| `certificates.jsonl` | Bank saldos, pension funds, cesantías, investment funds | All modes |
| `exogena.jsonl` | Real estate (Marval), vehicle, stocks (Ecopetrol) | `summary`, `project` |
| `salary-history.jsonl` | Income trajectory (monthly USD + TRM) | `project`, `goal` |
| `patrimonio_calc.py` | Net worth aggregation (deduplication) | `summary`, `project` |
| `trm-history.jsonl` | USD/COP exchange rates | FX conversion |

### User-provided (portfolio input)

| Source | Format | Data |
|--------|--------|------|
| Investment holdings | JSON/CSV | Ticker, units, cost basis, account type |
| Target allocation | JSON | Asset class → target % |
| Goals | JSON | Name, target amount, target date, priority |

Portfolio data stored at `~/.wealth-management/portfolio.json`.

## Skill Modes

Four modes are **live** (scripts shipped): `summary`, `project`, `goal`, `scenario`.
Three modes are **Planned** (design documented below, scripts not yet shipped):
`allocation`, `rebalance`, `optimize`. Planned modes are not in `skill.json`'s
`mode` enum and have no runnable command yet.

### 1. `summary` — Portfolio Health Dashboard (Descriptive)

Current-state analysis of all holdings aggregated from finance-substrate
and user portfolio data.

**Script:** `scripts/portfolio_summary.py --year 2025`

**Outputs:**
- Net worth breakdown by asset class (cash, fixed income, equities, real estate, pension)
- Allocation pie: actual vs target %
- Concentration risk: any single position > 20% of portfolio
- Currency exposure: COP vs USD vs other
- Year-over-year growth: patrimonio líquido trajectory
- Liquidity analysis: liquid vs illiquid assets

### 2. `project` — Compound Growth Projection (Predictive)

Forward-looking wealth projection with configurable assumptions.

**Script:** `scripts/project_wealth.py --years 20 --monthly-contribution-usd 2000`

**Inputs:**
- Starting capital (from patrimonio or manual)
- Monthly/annual contribution amount
- Expected real return by asset class (default: equities 7%, bonds 3%, RE 5%)
- Inflation assumption (Colombia CPI: ~5-7%, US CPI: ~2-3%)
- Tax drag (from finance-substrate effective rate)
- TRM trend assumption (mean-reverting to historical average)

**Outputs:**
- Year-by-year table: contributions, growth, taxes, net value
- Milestones: when you hit $100M, $500M, $1B COP or $100K, $500K, $1M USD
- Contribution vs growth ratio over time (crossover point)
- Inflation-adjusted purchasing power
- Sensitivity table: ±2% return scenarios

**Formulas:**
```
FV = PV × (1 + r)^n + PMT × [((1+r)^n - 1) / r]
Real return = nominal - inflation - tax_drag
CAGR = (Ending / Beginning)^(1/Years) - 1
```

### 3. `goal` — Goal-Based Financial Planning (Predictive)

Reverse-engineer: given a target, what's needed?

**Script:** `scripts/goal_planner.py --target-usd 500000 --target-date 2035`

**Inputs:**
- Target amount (COP or USD)
- Target date
- Current savings (from patrimonio)
- Risk tolerance (conservative / moderate / aggressive)
- Income growth assumption

**Outputs:**
- Required monthly savings (COP + USD)
- Required return rate to meet goal with current savings only
- Probability of success (linked to Monte Carlo)
- Gap analysis: on track / behind / ahead
- Recommended asset allocation for the goal's time horizon

### 4. `allocation` — Asset Allocation Strategy (Prescriptive) — Planned

Recommend an optimal asset allocation based on risk profile and time horizon.

**Status:** Planned — `allocate_assets.py` is not yet shipped. The design below
is the intended contract; there is no runnable command for this mode yet.

**Framework: Modified Bogle Three-Fund + Colombian Extensions**

| Risk Profile | Equities | Fixed Income | Real Estate | Cash/AFC |
|-------------|----------|--------------|-------------|----------|
| Conservative | 30% | 50% | 10% | 10% |
| Moderate | 55% | 25% | 10% | 10% |
| Aggressive | 75% | 10% | 10% | 5% |

**Colombian-specific considerations:**
- AFC cuenta as cash/fixed income (tax-deferred, housing-eligible)
- Pensión voluntaria (Skandia) = long-term equity proxy (10yr lock)
- Cesantías = forced savings (annual withdrawal allowed)
- Colombian equities (BVC) vs international via DolarApp/ARQ or US brokerage
- TRM hedging: maintain USD reserves for FX diversification

**Outputs:**
- Target allocation table
- Current vs target delta
- Rebalancing trades needed
- Tax impact of rebalancing (from finance-substrate tax projection)

### 5. `rebalance` — Tactical Rebalancing (Prescriptive) — Planned

Generate specific trades to bring portfolio back to target.

**Status:** Planned — `rebalance.py` is not yet shipped. The design below is the
intended contract; there is no runnable command for this mode yet.

**Inputs:**
- Current holdings (from portfolio.json + certificates)
- Target allocation (from allocation mode or manual)
- Drift threshold (default: 5% absolute deviation triggers rebalance)
- Tax sensitivity (minimize realized gains)

**Outputs:**
- Trades to execute (buy/sell, amount, account)
- Tax impact estimate (short-term vs long-term gains)
- Priority order (tax-loss harvest first, then rebalance)
- "Do nothing" zones where drift is within tolerance

### 6. `scenario` — Monte Carlo & Stress Testing (Predictive)

Simulate portfolio outcomes under uncertainty.

**Script:** `scripts/scenario_analysis.py --simulations 10000 --years 20`

**Scenarios:**
- **Monte Carlo:** 10,000 simulations with log-normal returns, historical volatility
- **Historical stress:** 2008 GFC, 2020 COVID, 2022 rate hike, 1999 Colombian crisis
- **COP devaluation:** TRM shock (+30%, +50%)
- **Stagflation:** High inflation (10%) + low growth (0%) for 5 years
- **Career disruption:** 0 income for 6-12 months

**Outputs:**
- Success probability (% of simulations meeting goal)
- Percentile outcomes: P10, P25, P50, P75, P90
- Worst-case scenario: minimum portfolio value
- Sequence-of-returns risk: early vs late bear market impact
- Safe withdrawal rate for given success probability

### 7. `optimize` — Tax-Efficient Strategy (Prescriptive) — Planned

Maximize after-tax wealth growth using Colombian tax law.

**Status:** Planned — `optimize_strategy.py` is not yet shipped. The design below
is the intended contract; there is no runnable command for this mode yet.

**Strategies analyzed:**
1. **Contribution ordering:** AFC vs voluntaria vs libre inversión
   - AFC: tax-deferred, 10yr lock or housing withdrawal
   - Voluntaria: tax-deferred, 10yr lock or pension age
   - Libre: no tax benefit, full liquidity
   - Decision depends on marginal tax rate and cap utilization (1,340 UVT)

2. **Account type placement:** Which assets in which account?
   - High-growth (equities) → tax-deferred (voluntaria/AFC) for tax-free compounding
   - Income-producing (bonds, rendimientos) → taxable, claim INCR deduction
   - International (USD equities) → DolarApp/ARQ for FX diversification

3. **Withdrawal sequencing** (for wealth distribution phase):
   - Taxable accounts first (lower tax rate on capital gains)
   - AFC for housing needs (tax-free withdrawal)
   - Voluntaria after 10yr + pension age (tax-free)
   - Cesantías annually (forced, taxable)

4. **Tax-loss harvesting:** Identify positions with unrealized losses to offset gains

**Outputs:**
- Optimal contribution plan (monthly amounts by account)
- Account placement recommendations
- 5-year after-tax growth comparison: optimized vs naive
- Marginal benefit table (extra $1M COP in each account → after-tax impact)

## Integration with finance-substrate

wealth-management imports directly from finance-substrate scripts:

```python
# Import patrimonio for current net worth
from patrimonio_calc import compute_patrimonio

# Import tax projection for effective rates
from tax_projection import project_tax

# Import budget for contribution capacity
from budget_planner import estimate_annual_tax

# Read salary trajectory
salary = load_jsonl("~/.finance-substrate/tax/salary-history.jsonl")
```

## Data Directory

```
~/.wealth-management/
├── portfolio.json          # Current holdings (user-maintained)
├── targets.json            # Target allocation profiles
├── goals.json              # Financial goals with timelines
├── projections/            # Saved projection results
│   └── projection-YYYY-MM-DD.json
├── scenarios/              # Monte Carlo results
│   └── scenario-YYYY-MM-DD.json
└── history/                # Net worth snapshots over time
    └── networth-history.jsonl
```

## References

### Key Formulas

| Formula | Expression | Use |
|---------|-----------|-----|
| Future Value | `FV = PV(1+r)^n + PMT[((1+r)^n - 1)/r]` | Compound growth |
| CAGR | `(FV/PV)^(1/n) - 1` | Historical return |
| Real Return | `(1+nominal)/(1+inflation) - 1` | Purchasing power |
| Sharpe Ratio | `(R_p - R_f) / σ_p` | Risk-adjusted return |
| Safe Withdrawal | `Annual spend / Portfolio value` | Distribution phase |
| Tax Drag | `r_nominal × effective_tax_rate` | After-tax return |
| Rule of 72 | `72 / r` | Years to double |

### Colombian-Specific Parameters

| Parameter | Value | Source |
|-----------|-------|--------|
| UVT 2025 | $49,799 COP | DIAN |
| AFC/VP cap | 1,340 UVT ($66.7M) | Art. 336, Ley 2277/2022 |
| Pensión oblig. rate | 16% of IBC | Ley 797/2003 |
| Colombian CPI (2024) | ~6.1% | DANE |
| US CPI (2024) | ~2.9% | BLS |
| Avg TRM 2025 | ~4,052 COP/USD | datos.gov.co |
| BVC COLCAP return (5yr avg) | ~8-12% nominal | BVC |
| S&P 500 return (10yr avg) | ~12% nominal | Historical |
| CDT rates (2024) | ~10-13% nominal | Banks |
| FIC (fondos inversión colectiva) | ~7-10% nominal | Skandia/Davivienda |

### Asset Class Expected Returns (Real, After Inflation)

| Asset Class | Conservative | Moderate | Aggressive |
|-------------|-------------|----------|-----------|
| Colombian equities (BVC) | 3% | 5% | 7% |
| US equities (S&P 500) | 5% | 7% | 9% |
| Colombian CDT/bonds | 2% | 3% | 4% |
| Real estate (Colombia) | 3% | 5% | 6% |
| Pension voluntaria (Skandia) | 3% | 5% | 7% |
| AFC (Davivienda) | 1% | 2% | 2% |
| Cash/savings | 0% | 0% | 0% |

## Compound: Autoany Integration (EGRI)

This skill is EGRI-aware. When a user's request implies iterative optimization
of savings strategies, contribution plans, or investment horizons, the agent
should scaffold a problem-spec and delegate to `/autoany`.

### Optimization Triggers

Invoke `/autoany` when the user asks to:
- **"Optimize contributions"** — AFC vs pension vs brokerage split
- **"Maximize probability"** — probability of reaching a financial goal
- **"Best allocation for my goals"** — multi-horizon allocation
- **"How should I split my savings"** — tax-efficient contribution ordering
- **"Run simulations"** — with optimization intent (not just a single run)
- **"Stress test my plan"** — combined with finding a better plan

### EGRI Problem-Spec Templates

| Template | Artifact | Evaluator | Score | Use When |
|----------|----------|-----------|-------|----------|
| `contribution-optimization` | `contribution_plan.yaml` | `scenario_analysis.py --egri` | P(goal) | Optimizing savings splits |
| `horizon-evaluation` | `horizon_plan.yaml` | `scenario_analysis.py --egri` | Risk-adjusted P(all goals) | Multi-goal allocation |

Templates are at `templates/egri/`.

### Delegation Flow

```
1. User request → agent detects optimization intent
2. Load personal context:
   - patrimonio from finance-substrate (starting capital)
   - salary trajectory (budget constraint)
   - TRM rates (COP/USD conversion)
   - existing goals from ~/.wealth-management/goals.json
3. Scaffold problem-spec from template
4. Invoke /autoany
5. EGRI loop: Proposer → Executor (scenario_analysis.py) → Evaluator → Selector
6. Return promoted plan + ledger summary
7. Show concrete action items:
   - "Increase AFC contributions to $X/month"
   - "Shift 10% from fixed income to equities in retirement bucket"
```

### EGRI Evaluator Bridge

`scenario_analysis.py --egri` outputs structured `Outcome` for autoany:
- Score: `probability_of_goal_pct` (0-100)
- Constraints: `median_max_drawdown_pct > -25`, `probability_of_ruin_pct <= 5`
- Metrics: full Monte Carlo statistics for the proposer to learn from

### Safety Constraints (enforced in EGRI loops)

- All simulations use **historical/synthetic data only** (no live data risk)
- Contribution plans are **advisory** — no automatic financial actions
- AFC + pensión voluntaria combined cap: 1,340 UVT (~$66.7M COP)
- Monthly contribution cannot exceed income
- Ruin probability must stay below 5%
- Budget: 20-40 trials max, 10-40 minutes total

## Related Skills

- **[finance-substrate](https://github.com/broomva/finance-substrate)** — Data layer: bank certificates, patrimonio, tax projection, salary history, TRM rates
- **[investment-management](https://github.com/broomva/investment-management)** — Execution layer: security screening, scoring, market data, trade execution, factor analysis, backtesting
- **[autoany](https://github.com/broomva/autoany)** — EGRI framework for recursive improvement loops

## Dependencies

- Python 3.10+
- `finance-substrate` skill (data layer — certificates, patrimonio, tax, salary)
- `autoany` (optional, for EGRI optimization loops)
- `numpy` (optional, for Monte Carlo simulations)
- No paid services. All data stays local.

## File Structure

```
wealth-management/
├── SKILL.md                          # This file
├── skill.json                        # Schema definition (4 live modes)
├── scripts/                          # 4 shipped scripts (modes 4/5/7 Planned)
│   ├── portfolio_summary.py          # Mode 1: descriptive dashboard
│   ├── project_wealth.py             # Mode 2: compound growth projection
│   ├── goal_planner.py               # Mode 3: goal-based planning
│   └── scenario_analysis.py          # Mode 6: Monte Carlo & stress tests
├── references/
│   ├── compounding-formulas.md       # Mathematical foundations
│   └── colombian-investment-landscape.md  # Local market reference
├── templates/
│   └── egri/                         # EGRI problem-spec templates (autoany)
│       ├── contribution-optimization.yaml  # Savings split optimization
│       └── horizon-evaluation.yaml         # Multi-goal horizon allocation
└── README.md
```
