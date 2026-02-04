---
name: credit-risk
description: Assess credit risk and default probability for bonds using credit spreads, rating transitions, and recovery analysis. Requires numpy>=1.24.0, pandas>=2.0.0, scipy>=1.10.0. Use when evaluating corporate bonds, analyzing credit events, estimating default probabilities, or managing credit portfolio risk.
---

# Credit Risk Assessment and Rating Analysis Skill Development

## Objective

Evaluate and model issuer default risk, downgrade probability, and credit spread behavior using both fundamental analysis and market-implied approaches. Develop systematic frameworks for assessing credit quality and monitoring credit migrations.

## Skill Classification

**Domain**: Fixed Income Credit Analysis
**Level**: Advanced
**Prerequisites**: Bond Pricing, Yield Measures
**Estimated Time**: 20-25 hours

## Focus Areas

### 1. Fundamental vs. Market-Implied Credit Risk

#### Fundamental Credit Analysis
**Approach**: Bottom-up analysis of issuer financials and business fundamentals.

**Key Metrics**:
```python
class CreditMetrics:
    """Fundamental credit analysis metrics."""

    @staticmethod
    def interest_coverage(ebit, interest_expense):
        """Times Interest Earned (TIE) ratio."""
        return ebit / interest_expense

    @staticmethod
    def debt_to_ebitda(total_debt, ebitda):
        """Leverage ratio."""
        return total_debt / ebitda

    @staticmethod
    def debt_to_equity(total_debt, total_equity):
        """Capital structure ratio."""
        return total_debt / total_equity

    @staticmethod
    def current_ratio(current_assets, current_liabilities):
        """Liquidity ratio."""
        return current_assets / current_liabilities

    @staticmethod
    def free_cash_flow_to_debt(fcf, total_debt):
        """Debt service capacity."""
        return fcf / total_debt
```

#### Market-Implied Credit Risk
**Approach**: Extract default probability from market prices.

**Credit Spread**:
```
Credit Spread = YTM_Corporate - YTM_Treasury
```

**Implied Default Probability**:
```python
def implied_default_probability(credit_spread, recovery_rate, years):
    """
    Calculate market-implied annual default probability.

    Parameters:
    -----------
    credit_spread : float
        Yield spread over risk-free rate (decimal)
    recovery_rate : float
        Expected recovery in default (decimal, e.g., 0.40 for 40%)
    years : float
        Time horizon

    Returns:
    --------
    float : Implied annual default probability
    """
    loss_given_default = 1 - recovery_rate
    annual_pd = credit_spread / loss_given_default
    return annual_pd

def cumulative_default_prob(annual_pd, years):
    """
    Calculate cumulative default probability.

    Returns:
    --------
    float : Probability of default within 'years' horizon
    """
    survival_prob = (1 - annual_pd) ** years
    return 1 - survival_prob
```

### 2. Credit Rating Agencies

**Major Rating Agencies**:
- **Moody's**: Aaa to C scale
- **S&P**: AAA to D scale
- **Fitch**: AAA to D scale

**Rating Categories**:
- **Investment Grade**: BBB-/Baa3 and above
- **High Yield (Junk)**: BB+/Ba1 and below

**Rating Equivalence**:
```python
RATING_SCALE = {
    'Moody\'s': ['Aaa', 'Aa1', 'Aa2', 'Aa3', 'A1', 'A2', 'A3',
                 'Baa1', 'Baa2', 'Baa3', 'Ba1', 'Ba2', 'Ba3',
                 'B1', 'B2', 'B3', 'Caa1', 'Caa2', 'Caa3', 'Ca', 'C'],
    'S&P': ['AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-',
            'BBB+', 'BBB', 'BBB-', 'BB+', 'BB', 'BB-',
            'B+', 'B', 'B-', 'CCC+', 'CCC', 'CCC-', 'CC', 'C', 'D'],
    'Fitch': ['AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-',
              'BBB+', 'BBB', 'BBB-', 'BB+', 'BB', 'BB-',
              'B+', 'B', 'B-', 'CCC+', 'CCC', 'CCC-', 'CC', 'C', 'D']
}

def numerical_rating(rating, agency='S&P'):
    """Convert letter rating to numerical score (higher = better)."""
    scale = RATING_SCALE[agency]
    try:
        return len(scale) - scale.index(rating)
    except ValueError:
        return None

def is_investment_grade(rating, agency='S&P'):
    """Determine if rating is investment grade."""
    numeric = numerical_rating(rating, agency)
    if agency == 'Moody\'s':
        threshold = numerical_rating('Baa3', agency)
    else:
        threshold = numerical_rating('BBB-', agency)
    return numeric >= threshold if numeric else False
```

**Historical Default Rates by Rating**:
```python
# Average 10-year cumulative default rates (%)
HISTORICAL_DEFAULT_RATES = {
    'AAA': 0.60, 'AA': 1.50, 'A': 2.91,
    'BBB': 7.20, 'BB': 19.00, 'B': 35.00,
    'CCC': 54.00
}
```

### 3. Probability of Default (PD) and Loss Given Default (LGD)

**Expected Loss Framework**:
```
Expected Loss = PD × LGD × Exposure at Default
```

**PD Modeling Approaches**:

#### Structural Model (Merton Model)
```python
from scipy.stats import norm

def merton_default_probability(firm_value, debt_face_value,
                               volatility, risk_free_rate, time_horizon):
    """
    Calculate default probability using Merton structural model.

    Based on Black-Scholes option pricing framework.

    Parameters:
    -----------
    firm_value : float
        Current market value of firm's assets
    debt_face_value : float
        Face value of debt
    volatility : float
        Volatility of firm value (annual)
    risk_free_rate : float
        Risk-free rate
    time_horizon : float
        Time to debt maturity (years)

    Returns:
    --------
    float : Probability of default
    """
    d2 = (np.log(firm_value / debt_face_value) +
          (risk_free_rate - 0.5 * volatility**2) * time_horizon) / \
         (volatility * np.sqrt(time_horizon))

    return norm.cdf(-d2)
```

#### Reduced-Form Model
```python
def hazard_rate_pd(hazard_rate, time_horizon):
    """
    Calculate default probability from constant hazard rate.

    Parameters:
    -----------
    hazard_rate : float
        Instantaneous default intensity (annual)
    time_horizon : float
        Time period (years)

    Returns:
    --------
    float : Cumulative default probability
    """
    return 1 - np.exp(-hazard_rate * time_horizon)
```

**LGD Estimation**:
```python
class LGDEstimator:
    """Loss Given Default estimation."""

    # Historical average recovery rates by seniority
    RECOVERY_RATES = {
        'Senior Secured': 0.65,
        'Senior Unsecured': 0.45,
        'Senior Subordinated': 0.35,
        'Subordinated': 0.25,
        'Junior Subordinated': 0.15
    }

    @classmethod
    def lgd_from_seniority(cls, seniority):
        """Estimate LGD based on debt seniority."""
        recovery = cls.RECOVERY_RATES.get(seniority, 0.40)
        return 1 - recovery

    @staticmethod
    def lgd_from_collateral(debt_value, collateral_value,
                           liquidation_costs=0.20):
        """
        Calculate LGD considering collateral.

        Parameters:
        -----------
        debt_value : float
            Outstanding debt amount
        collateral_value : float
            Market value of collateral
        liquidation_costs : float
            Costs of liquidating collateral (as fraction)

        Returns:
        --------
        float : Loss given default
        """
        net_recovery = collateral_value * (1 - liquidation_costs)
        loss = max(0, debt_value - net_recovery)
        return loss / debt_value
```

### 4. Credit Spreads and Yield Differentials

**Components of Credit Spread**:
```
Credit Spread = Expected Loss + Risk Premium + Liquidity Premium
```

**Spread Analysis**:
```python
def credit_spread_decomposition(corporate_yield, treasury_yield,
                               expected_loss_component):
    """
    Decompose credit spread into components.

    Parameters:
    -----------
    corporate_yield : float
        YTM of corporate bond
    treasury_yield : float
        YTM of comparable Treasury
    expected_loss_component : float
        Expected loss (PD × LGD)

    Returns:
    --------
    dict : Spread decomposition
    """
    total_spread = corporate_yield - treasury_yield
    risk_liquidity_premium = total_spread - expected_loss_component

    return {
        'total_spread': total_spread,
        'expected_loss': expected_loss_component,
        'risk_premium': risk_liquidity_premium * 0.60,  # Estimate
        'liquidity_premium': risk_liquidity_premium * 0.40  # Estimate
    }

def option_adjusted_spread_credit(z_spread, option_cost):
    """
    Calculate credit-adjusted OAS.

    Parameters:
    -----------
    z_spread : float
        Zero-volatility spread
    option_cost : float
        Value of embedded options

    Returns:
    --------
    float : Option-adjusted spread
    """
    return z_spread - option_cost
```

**Credit Spread Curve**:
```python
import matplotlib.pyplot as plt

def plot_credit_spread_curve(maturities, spreads, rating, date):
    """
    Visualize credit spread term structure.

    Parameters:
    -----------
    maturities : array-like
        Bond maturities
    spreads : array-like
        Credit spreads (basis points)
    rating : str
        Credit rating
    date : str
        Observation date
    """
    plt.figure(figsize=(10, 6))
    plt.plot(maturities, spreads, 'ro-', linewidth=2, markersize=6)
    plt.xlabel('Maturity (Years)')
    plt.ylabel('Credit Spread (bps)')
    plt.title(f'{rating} Credit Spread Curve - {date}')
    plt.grid(True, alpha=0.3)
    plt.show()
```

### 5. Event Risk and Credit Migration

**Event Risk Categories**:
- **M&A Activity**: Leverage increases from acquisitions
- **Dividend Recapitalization**: Debt-funded special dividends
- **Regulatory Changes**: New compliance costs or restrictions
- **Litigation**: Major legal judgments

**Credit Migration Matrix**:
```python
# One-year transition probabilities (%)
TRANSITION_MATRIX = {
    'AAA': {'AAA': 90.81, 'AA': 8.33, 'A': 0.68, 'BBB': 0.06, 'Default': 0.00},
    'AA':  {'AAA': 0.70, 'AA': 90.65, 'A': 7.79, 'BBB': 0.64, 'Default': 0.02},
    'A':   {'AAA': 0.09, 'AA': 2.27, 'A': 91.05, 'BBB': 5.52, 'Default': 0.06},
    'BBB': {'AAA': 0.02, 'AA': 0.33, 'A': 5.95, 'BBB': 86.93, 'BB': 5.30, 'Default': 0.18},
    'BB':  {'AAA': 0.03, 'BBB': 0.67, 'BB': 80.53, 'B': 8.84, 'Default': 1.06},
    'B':   {'BB': 0.43, 'B': 83.46, 'CCC': 4.07, 'Default': 4.89},
    'CCC': {'B': 0.69, 'CCC': 58.24, 'Default': 26.92}
}

def expected_rating_migration(current_rating, years=1):
    """
    Calculate probability distribution of future ratings.

    Returns:
    --------
    dict : Probabilities for each rating category
    """
    return TRANSITION_MATRIX.get(current_rating, {})

def downgrade_probability(current_rating, years=1):
    """
    Calculate probability of downgrade within time horizon.
    """
    transitions = TRANSITION_MATRIX.get(current_rating, {})

    # Sum probabilities of lower ratings
    ratings_order = ['AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'CCC']
    current_index = ratings_order.index(current_rating)

    downgrade_prob = sum(transitions.get(r, 0)
                        for r in ratings_order[current_index+1:])
    downgrade_prob += transitions.get('Default', 0)

    return downgrade_prob / 100  # Convert to decimal
```

## Expected Competency

Upon completion, you will be able to:

1. **Perform fundamental credit analysis** using financial ratios
2. **Extract market-implied default probabilities** from credit spreads
3. **Interpret credit ratings** and understand rating methodologies
4. **Model PD and LGD** using structural and reduced-form approaches
5. **Analyze credit spread behavior** and decompose spread components
6. **Assess credit migration risk** using transition matrices
7. **Monitor credit events** and evaluate impact on portfolio

## Deliverables

### 1. credit_risk_model.py
Production Python module containing:
- Fundamental credit metrics calculators
- PD/LGD modeling (Merton, hazard rate)
- Credit spread analysis tools
- Rating migration simulator
- Monte Carlo default scenario generator
- Portfolio credit risk aggregation

### 2. credit_spread_dashboard.md
Analysis documentation including:
- Credit spread tracking vs. Treasuries
- Spread curve analysis by rating tier
- Credit migration monitoring
- Event risk assessment framework
- Portfolio credit exposure report

## Reference Materials

### Foundational Texts
1. Lando, D. *Credit Risk Modeling: Theory and Applications*
2. Duffie, D. & Singleton, K. *Credit Risk: Pricing, Measurement, and Management*
3. CFA Institute. *Fixed Income* - Credit Analysis

### Rating Agency Methodologies
1. **Moody's**: [Rating Methodology](https://www.moodys.com/research/Rating-Methodologies)
2. **S&P**: [Corporate Criteria](https://www.spglobal.com/ratings/en/research-insights/methodology)
3. **Fitch**: [Rating Criteria](https://www.fitchratings.com/research/methodology)

### Data Sources
1. **FRED**: [Corporate Bond Spreads](https://fred.stlouisfed.org/)
2. **FINRA**: [Corporate Bond Data](https://www.finra.org/data)
3. **Bloomberg**: Credit default swap (CDS) spreads

## Validation Framework

### Self-Assessment Checklist

- [ ] Calculate key credit ratios from financial statements
- [ ] Estimate implied default probability from credit spread
- [ ] Interpret rating agency methodologies
- [ ] Model PD using Merton framework
- [ ] Estimate LGD by seniority and collateral
- [ ] Decompose credit spread into components
- [ ] Apply credit migration matrices
- [ ] Assess portfolio credit concentration risk

### Practice Problems

1. Calculate implied PD for BB-rated bond: 300 bps spread, 40% recovery
2. Estimate LGD for senior secured debt with $100M collateral, $150M debt
3. Determine downgrade probability for A-rated issuer over 1 year
4. Decompose 250 bps spread into expected loss and risk premium

## Integration with Other Skills

- **Bond Pricing**: Credit spreads adjust discount rates
- **Yield Measures**: Credit component in yield analysis
- **Benchmarking**: Credit quality comparison vs. peers
- **Portfolio Management**: Credit risk aggregation and limits

## Standards and Compliance

All credit analysis must document:
- Data sources and dates
- Rating sources and effective dates
- Assumptions (recovery rates, transition probabilities)
- Model validation and back-testing results

## Version Control

**Version**: 1.0.0
**Last Updated**: 2025-12-07
**Author**: Ordinis-1 Bond Analysis Framework
**Status**: Production Ready

---

**Previous Skill**: `duration-convexity/`
**Next Skill**: `bond-benchmarking/`
