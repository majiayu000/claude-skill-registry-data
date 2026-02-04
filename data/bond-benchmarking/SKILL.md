---
name: bond-benchmarking
description: Compare bond performance against market benchmarks and indices. Analyzes yield spreads, duration matching, and relative value. Requires numpy>=1.24.0, pandas>=2.0.0. Use when evaluating bonds against peers, measuring portfolio attribution, or identifying value opportunities in fixed income markets.
---

# Bond Benchmarking and Relative Performance Analysis Skill Development

## Objective

Compare bond yields, durations, and credit quality against market benchmarks and indices to identify relative value opportunities and measure portfolio performance. Master systematic frameworks for peer comparison and excess return attribution.

## Skill Classification

**Domain**: Fixed Income Portfolio Management
**Level**: Advanced
**Prerequisites**: Bond Pricing, Yield Measures, Duration, Credit Risk
**Estimated Time**: 12-15 hours

## Focus Areas

### 1. Benchmark Selection

**Treasury Curve as Benchmark**:
```python
def treasury_benchmark_yield(maturity, treasury_curve):
    """
    Interpolate Treasury yield for given maturity.

    Parameters:
    -----------
    maturity : float
        Bond maturity in years
    treasury_curve : dict
        {maturity: yield} mapping for Treasury curve

    Returns:
    --------
    float : Interpolated benchmark yield
    """
    from scipy.interpolate import interp1d

    maturities = sorted(treasury_curve.keys())
    yields = [treasury_curve[m] for m in maturities]

    interpolator = interp1d(maturities, yields, kind='cubic',
                           fill_value='extrapolate')
    return float(interpolator(maturity))
```

**Corporate Bond Index Benchmarks**:
- Bloomberg Barclays US Corporate Bond Index
- ICE BofA US Corporate Index
- S&P US Issued Investment Grade Corporate Bond Index

**Index Characteristics**:
```python
class BondIndexProfile:
    """Corporate bond index profile."""

    def __init__(self, name):
        self.name = name
        self.constituents = []

    def add_bond(self, bond_info):
        """Add bond to index."""
        self.constituents.append(bond_info)

    def calculate_metrics(self):
        """Calculate index-level metrics."""
        weights = np.array([b['market_value'] for b in self.constituents])
        weights = weights / weights.sum()

        durations = np.array([b['duration'] for b in self.constituents])
        yields = np.array([b['ytm'] for b in self.constituents])

        return {
            'weighted_duration': np.dot(weights, durations),
            'weighted_yield': np.dot(weights, yields),
            'total_market_value': weights.sum(),
            'num_constituents': len(self.constituents)
        }
```

### 2. Spread to Benchmark

**G-Spread** (Spread to Government):
```
G-Spread = YTM_Corporate - YTM_Treasury_Interpolated
```

**I-Spread** (Interpolated Spread):
```
I-Spread = YTM_Corporate - Swap_Rate_Interpolated
```

**Z-Spread** (Zero-Volatility Spread):
```
P = Σ [CF_t / (1 + r_t + Z)^t]

Where:
  P = Bond price
  r_t = Spot rate at time t
  Z = Constant spread (Z-spread)
  CF_t = Cash flow at time t
```

**Python Implementation**:
```python
def g_spread(corporate_ytm, treasury_ytm):
    """Calculate G-spread (in basis points)."""
    return (corporate_ytm - treasury_ytm) * 10000

def calculate_z_spread(bond_price, cash_flows, spot_rates, times):
    """
    Calculate Z-spread using root-finding.

    Parameters:
    -----------
    bond_price : float
        Current bond price
    cash_flows : array-like
        Future cash flows
    spot_rates : array-like
        Risk-free spot rates for each cash flow
    times : array-like
        Time to each cash flow (years)

    Returns:
    --------
    float : Z-spread (as decimal)
    """
    from scipy.optimize import newton

    def price_diff(z_spread):
        pv = sum(cf / (1 + spot + z_spread)**t
                for cf, spot, t in zip(cash_flows, spot_rates, times))
        return pv - bond_price

    z_spread = newton(price_diff, 0.01, maxiter=100)
    return z_spread

def spread_duration(bond_duration, spread_change):
    """
    Estimate price impact of spread change.

    ΔP/P ≈ -Duration × ΔSpread
    """
    return -bond_duration * spread_change
```

### 3. Relative Value Analysis

**Comparing Bonds**:
```python
class RelativeValueAnalysis:
    """Framework for relative value comparison."""

    @staticmethod
    def compare_bonds(bond1, bond2, benchmark_yield):
        """
        Compare two bonds for relative value.

        Parameters:
        -----------
        bond1, bond2 : dict
            Bond characteristics: {'ytm', 'duration', 'rating', 'price'}
        benchmark_yield : float
            Benchmark Treasury yield

        Returns:
        --------
        dict : Comparative metrics
        """
        spread1 = (bond1['ytm'] - benchmark_yield) * 10000  # bps
        spread2 = (bond2['ytm'] - benchmark_yield) * 10000

        spread_per_duration1 = spread1 / bond1['duration']
        spread_per_duration2 = spread2 / bond2['duration']

        return {
            'bond1_spread': spread1,
            'bond2_spread': spread2,
            'bond1_spread_per_duration': spread_per_duration1,
            'bond2_spread_per_duration': spread_per_duration2,
            'relative_value_winner': 'Bond 1' if spread_per_duration1 > spread_per_duration2 else 'Bond 2'
        }

    @staticmethod
    def cheapness_score(actual_spread, model_spread):
        """
        Calculate cheapness metric.

        Positive = bond is cheap (offers excess spread)
        Negative = bond is rich (offers insufficient spread)
        """
        return actual_spread - model_spread
```

### 4. Peer Comparison (Sector/Rating)

**Sector Classification**:
```python
SECTOR_GROUPS = {
    'Financial': ['Banks', 'Insurance', 'Asset Managers', 'REITs'],
    'Industrial': ['Manufacturing', 'Transportation', 'Capital Goods'],
    'Utility': ['Electric', 'Gas', 'Water'],
    'Technology': ['Software', 'Hardware', 'Semiconductors'],
    'Consumer': ['Retail', 'Food & Beverage', 'Automobiles'],
    'Energy': ['Oil & Gas', 'Renewables'],
    'Healthcare': ['Pharmaceuticals', 'Biotechnology', 'Hospitals']
}

def sector_peer_analysis(bond, peer_bonds):
    """
    Compare bond against sector peers.

    Parameters:
    -----------
    bond : dict
        Subject bond characteristics
    peer_bonds : list of dict
        Peer bond characteristics

    Returns:
    --------
    dict : Peer comparison metrics
    """
    peer_spreads = np.array([b['spread'] for b in peer_bonds])
    peer_durations = np.array([b['duration'] for b in peer_bonds])

    return {
        'bond_spread': bond['spread'],
        'peer_median_spread': np.median(peer_spreads),
        'peer_mean_spread': np.mean(peer_spreads),
        'spread_percentile': (peer_spreads < bond['spread']).sum() / len(peer_spreads) * 100,
        'peer_duration_range': (peer_durations.min(), peer_durations.max()),
        'relative_cheapness': bond['spread'] - np.median(peer_spreads)
    }
```

**Rating-Based Comparison**:
```python
def rating_tier_analysis(bond_rating, bonds_universe):
    """
    Compare bond spread within rating tier.

    Parameters:
    -----------
    bond_rating : str
        Subject bond rating
    bonds_universe : list of dict
        All bonds with ratings

    Returns:
    --------
    dict : Rating tier statistics
    """
    same_rating = [b for b in bonds_universe
                   if b['rating'] == bond_rating]

    if not same_rating:
        return None

    spreads = np.array([b['spread'] for b in same_rating])

    return {
        'rating': bond_rating,
        'count': len(same_rating),
        'spread_mean': spreads.mean(),
        'spread_median': np.median(spreads),
        'spread_std': spreads.std(),
        'spread_min': spreads.min(),
        'spread_max': spreads.max()
    }
```

### 5. Excess Return Measurement

**Total Return Components**:
```
Total Return = Coupon Income + Price Change + Reinvestment Income
```

**Excess Return (Alpha)**:
```
Excess Return = Portfolio Return - Benchmark Return
```

**Beta vs. Benchmark**:
```
β = Cov(R_portfolio, R_benchmark) / Var(R_benchmark)
```

**Python Framework**:
```python
class PerformanceAttribution:
    """Performance attribution framework."""

    @staticmethod
    def total_return(beginning_value, ending_value, coupon_income):
        """
        Calculate total return.

        Returns:
        --------
        float : Total return (as decimal)
        """
        return (ending_value + coupon_income - beginning_value) / beginning_value

    @staticmethod
    def excess_return(portfolio_return, benchmark_return):
        """Calculate alpha."""
        return portfolio_return - benchmark_return

    @staticmethod
    def calculate_beta(portfolio_returns, benchmark_returns):
        """
        Calculate portfolio beta vs. benchmark.

        Parameters:
        -----------
        portfolio_returns : array-like
            Historical portfolio returns
        benchmark_returns : array-like
            Historical benchmark returns

        Returns:
        --------
        float : Beta coefficient
        """
        covariance = np.cov(portfolio_returns, benchmark_returns)[0, 1]
        benchmark_variance = np.var(benchmark_returns)
        return covariance / benchmark_variance

    @staticmethod
    def attribution_decomposition(portfolio_return, benchmark_return,
                                  duration_effect, spread_effect,
                                  selection_effect):
        """
        Decompose excess return into components.

        Parameters:
        -----------
        duration_effect : float
            Return from duration positioning
        spread_effect : float
            Return from spread changes
        selection_effect : float
            Return from security selection

        Returns:
        --------
        dict : Attribution breakdown
        """
        total_alpha = portfolio_return - benchmark_return

        return {
            'total_excess_return': total_alpha,
            'duration_contribution': duration_effect,
            'spread_contribution': spread_effect,
            'selection_contribution': selection_effect,
            'residual': total_alpha - (duration_effect + spread_effect + selection_effect)
        }
```

### 6. Benchmark Replication and Tracking Error

**Tracking Error**:
```
TE = σ(R_portfolio - R_benchmark)
```

**Information Ratio**:
```
IR = Excess Return / Tracking Error
```

**Python Implementation**:
```python
def tracking_error(portfolio_returns, benchmark_returns):
    """
    Calculate tracking error.

    Parameters:
    -----------
    portfolio_returns : array-like
        Portfolio returns over time
    benchmark_returns : array-like
        Benchmark returns over time

    Returns:
    --------
    float : Annualized tracking error
    """
    excess_returns = np.array(portfolio_returns) - np.array(benchmark_returns)
    return excess_returns.std() * np.sqrt(12)  # Annualize if monthly

def information_ratio(portfolio_returns, benchmark_returns):
    """
    Calculate information ratio.

    Returns:
    --------
    float : IR (higher is better)
    """
    excess_returns = np.array(portfolio_returns) - np.array(benchmark_returns)
    mean_excess = excess_returns.mean() * 12  # Annualize
    te = excess_returns.std() * np.sqrt(12)

    return mean_excess / te if te > 0 else 0

def portfolio_replication(benchmark_holdings, target_budget):
    """
    Replicate benchmark with subset of holdings.

    Uses optimization to minimize tracking error.
    """
    from scipy.optimize import minimize

    n = len(benchmark_holdings)

    # Objective: minimize deviation from benchmark weights
    def objective(weights):
        benchmark_weights = np.array([h['weight'] for h in benchmark_holdings])
        return np.sum((weights - benchmark_weights)**2)

    # Constraints
    constraints = [
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}  # Sum to 1
    ]

    bounds = [(0, 1) for _ in range(n)]
    initial_weights = np.ones(n) / n

    result = minimize(objective, initial_weights, method='SLSQP',
                     bounds=bounds, constraints=constraints)

    return result.x
```

## Expected Competency

Select benchmarks, calculate spreads (G/I/Z), perform peer analysis, measure excess returns and attribution, compute tracking error/IR, identify relative value, replicate indices.

## Deliverables

**benchmark_comparison.ipynb**: Yield curves, spread tools (G/I/Z), peer comparison, excess return attribution, tracking error, relative value screener

**bond_benchmark_report.md**: Spread visualization, peer tables, attribution charts, relative value ranking, portfolio positioning

## Reference Materials

**Texts**: Fabozzi *Handbook of Fixed Income Securities* (Performance Attribution), Dynkin *Quantitative Management of Bond Portfolios*

**Standards**: Bloomberg indices methodology, ICE BofA index construction, S&P Dow Jones fixed income methodology

**Data**: Bloomberg Terminal (BVAL curves), FRED (Treasury/spreads), FINRA TRACE (transactions)

## Validation Framework

### Self-Assessment Checklist

- [ ] Calculate G-spread for corporate vs. Treasury
- [ ] Compute Z-spread using spot curve
- [ ] Perform sector peer comparison
- [ ] Calculate portfolio tracking error
- [ ] Attribute excess returns to duration/spread/selection
- [ ] Identify cheap/rich bonds vs. peers
- [ ] Compute information ratio

### Practice Problems
1. Bond 5% YTM, 7-year, Treasury 3.5% → Calculate G-spread
2. Portfolio 6% return, Benchmark 5.2%, TE 1.5% → Calculate IR
3. 10 peer bonds → Identify 3 cheapest by spread-per-duration
4. 150 bps excess return = duration (50) + spread (75) + selection (?)

## Integration with Other Skills

- **Yield Measures**: YTM serves as basis for spreads
- **Duration**: Duration-adjusted spread comparison
- **Credit Risk**: Credit quality peer grouping
- **Portfolio Management**: Benchmark-aware construction

## Standards and Compliance

All benchmarking analysis must document:
- Benchmark selection rationale
- Rebalancing frequency
- Data sources and dates
- Spread calculation methodology
- Performance calculation conventions

## Version Control

**Version**: 1.0.0 | **Last Updated**: 2025-12-07 | **Status**: Production Ready

**Previous**: `credit-risk/` | **Next**: `option-adjusted-spread/`
