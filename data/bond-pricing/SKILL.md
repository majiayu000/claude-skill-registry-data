---
name: bond-pricing
description: Price fixed income securities using present value, yield-to-maturity, and market conventions. Handles treasuries, corporates, municipals with various coupon frequencies. Requires numpy>=1.24.0, pandas>=2.0.0, scipy>=1.10.0. Use when valuing bonds, calculating accrued interest, or analyzing price sensitivity to yield changes.
---

# Bond Pricing and Valuation Skill Development

## Objective

Master the theoretical and quantitative foundations of bond pricing and valuation, including how interest rates, credit spreads, and time affect bond prices. Develop the ability to price any bond instrument accurately using both manual formulas and quantitative libraries.

## Skill Classification

**Domain**: Fixed Income Analytics
**Level**: Foundation
**Prerequisites**: Basic financial mathematics, time value of money concepts
**Estimated Time**: 15-20 hours

## Focus Areas

### 1. Bond Price-Yield Relationship

**Concept**: Understanding the inverse relationship between bond prices and yields.

**Key Principles**:
- When yields rise, bond prices fall (inverse correlation)
- Longer-maturity bonds exhibit greater price sensitivity
- Lower-coupon bonds show higher price volatility
- Market efficiency and arbitrage constraints

**Quantitative Framework**:
```
P = C/(1+y) + C/(1+y)² + ... + (C+FV)/(1+y)ⁿ

Where:
  P  = Bond price
  C  = Coupon payment
  y  = Yield to maturity
  FV = Face value
  n  = Number of periods
```

### 2. Present Value of Future Cash Flows

**Concept**: Bond pricing as discounted cash flow analysis.

**Methodology**:
- Identify all future cash flows (coupons + principal)
- Determine appropriate discount rate (yield/required return)
- Calculate present value of each cash flow
- Sum all present values to derive bond price

**Python Implementation**:
```python
import numpy as np

def bond_price_pv(face_value, coupon_rate, yield_rate, periods):
    """
    Calculate bond price using present value approach.

    Parameters:
    -----------
    face_value : float
        Par value of bond
    coupon_rate : float
        Annual coupon rate (as decimal)
    yield_rate : float
        Yield to maturity (as decimal)
    periods : int
        Number of periods to maturity

    Returns:
    --------
    float : Bond price
    """
    coupon = face_value * coupon_rate

    # PV of coupon payments
    pv_coupons = sum(coupon / (1 + yield_rate)**t
                     for t in range(1, periods + 1))

    # PV of principal
    pv_principal = face_value / (1 + yield_rate)**periods

    return pv_coupons + pv_principal
```

### 3. Yield to Maturity (YTM) and Yield to Call (YTC)

**YTM Definition**: Internal rate of return assuming bond held to maturity.

**YTC Definition**: Internal rate of return assuming bond called at first call date.

**Calculation Approaches**:
- Analytical (for simple bonds)
- Numerical iteration (Newton-Raphson)
- Financial calculator/software

**Python Implementation**:
```python
from scipy.optimize import newton

def ytm_calculator(price, face_value, coupon_rate, periods):
    """
    Calculate yield to maturity using numerical methods.
    """
    coupon = face_value * coupon_rate

    def price_diff(y):
        return price - sum(coupon / (1 + y)**t
                          for t in range(1, periods + 1)) \
                     - face_value / (1 + y)**periods

    return newton(price_diff, 0.05)  # Initial guess 5%
```

### 4. Pricing Specialized Bonds

#### Zero-Coupon Bonds
```
P = FV / (1 + y)ⁿ
```

No periodic coupons; all return from price appreciation.

#### Callable Bonds
Price consideration of issuer's call option:
```
P_callable = P_straight - P_call_option
```

#### Puttable Bonds
Price consideration of investor's put option:
```
P_puttable = P_straight + P_put_option
```

#### Floating-Rate Notes
Coupon resets periodically based on reference rate (LIBOR, SOFR):
- Price typically near par on reset dates
- Credit spread affects pricing between resets

### 5. Market Conventions

#### Clean Price vs. Dirty Price

**Clean Price**: Quoted price excluding accrued interest
```
Clean Price = Dirty Price - Accrued Interest
```

**Dirty Price**: Actual settlement price including accrued interest
```
Dirty Price = Clean Price + Accrued Interest
```

**Accrued Interest Calculation**:
```
Accrued Interest = (Coupon × Days Since Last Payment) / Days in Coupon Period
```

**Day Count Conventions**:
- **30/360**: Assumes 30 days/month, 360 days/year (corporate bonds)
- **Actual/Actual**: Actual days in period and year (Treasury bonds)
- **Actual/360**: Actual days in period, 360-day year (money market)

### 6. Python-Based Valuation Models

#### Discount Factor Approach
```python
def discount_factors(yield_curve, periods):
    """
    Calculate discount factors from yield curve.

    Parameters:
    -----------
    yield_curve : array-like
        Spot rates for each period
    periods : int
        Number of periods

    Returns:
    --------
    array : Discount factors
    """
    return np.array([1 / (1 + yield_curve[t])**t
                     for t in range(1, periods + 1)])

def bond_price_df(cash_flows, discount_factors):
    """
    Price bond using pre-calculated discount factors.
    """
    return np.dot(cash_flows, discount_factors)
```

#### Spot Curve Fitting
```python
from scipy.interpolate import CubicSpline

def fit_spot_curve(maturities, yields):
    """
    Fit smooth spot curve using cubic spline interpolation.

    Parameters:
    -----------
    maturities : array-like
        Bond maturities
    yields : array-like
        Corresponding yields

    Returns:
    --------
    callable : Interpolation function
    """
    return CubicSpline(maturities, yields)
```

## Expected Competency

Upon completion, you will be able to:

1. **Calculate bond prices** for any standard fixed-income security given coupon rate, yield, and maturity
2. **Compute YTM and YTC** using both analytical and numerical methods
3. **Price specialized bonds** including zero-coupon, callable, puttable, and floating-rate notes
4. **Apply market conventions** correctly (clean vs. dirty price, day count conventions)
5. **Implement Python models** for automated bond valuation and scenario analysis
6. **Validate pricing** against market quotes and identify arbitrage opportunities

## Deliverables

### 1. bond_pricing_model.ipynb
Jupyter notebook containing:
- Comprehensive bond pricing functions
- Scenario analysis (yield changes, time decay)
- Visualization of price-yield relationship
- Comparison across bond types (fixed, callable, zero-coupon)
- Validation against market data

### 2. pricing_examples.md
Case study documentation including:
- Example 1: Corporate bond pricing (fixed-rate)
- Example 2: Treasury zero-coupon bond
- Example 3: Callable bond with embedded option
- Example 4: Floating-rate note pricing
- Comparative analysis and interpretation

## Reference Materials

### Foundational Texts
1. Fabozzi, F. (Latest Edition). *Bond Markets, Analysis, and Strategies*. Pearson.
   - Chapters 5-7: Bond pricing and yield measures

2. CFA Institute. *Fixed Income* (CFA Program Curriculum).
   - Reading: Introduction to Fixed-Income Valuation

### Online Resources
1. **FINRA**: [Bond Calculator](https://www.finra.org/investors/calculators/bond-calculator)
2. **Investopedia**: [Bond Pricing Guide](https://www.investopedia.com/terms/b/bond-valuation.asp)
3. **Federal Reserve**: [Treasury Rates](https://fred.stlouisfed.org/)

### Python Libraries
1. **QuantLib-Python**: Comprehensive fixed-income library
   ```bash
   pip install QuantLib-Python
   ```

2. **yfinance**: Market data retrieval
   ```bash
   pip install yfinance
   ```

3. **numpy-financial**: Financial calculations
   ```bash
   pip install numpy-financial
   ```

## Validation Framework

### Self-Assessment Checklist

- [ ] Can price a standard corporate bond given market parameters
- [ ] Understand and explain the inverse price-yield relationship
- [ ] Calculate YTM using numerical methods
- [ ] Apply correct day count conventions
- [ ] Distinguish between clean and dirty prices
- [ ] Price callable bonds considering embedded options
- [ ] Implement Python functions for automated pricing
- [ ] Validate calculations against market quotes (±0.01% accuracy)

### Practice Problems

1. **Problem 1**: Price a 10-year corporate bond with 5% annual coupon, YTM of 4.5%, $1,000 face value
2. **Problem 2**: Calculate YTM for a bond trading at $1,050 with 6% coupon, 8 years to maturity
3. **Problem 3**: Price a 5-year zero-coupon bond with YTM of 3.2%
4. **Problem 4**: Compare prices of callable vs. non-callable bonds with same characteristics

## Integration with Other Skills

- **Yield Measures**: YTM from pricing serves as input for yield analysis
- **Duration/Convexity**: Price sensitivity calculations require pricing models
- **Credit Risk**: Credit spreads adjust discount rates in pricing
- **Benchmarking**: Relative pricing requires accurate valuation framework
- **OAS Analysis**: Option-adjusted pricing builds on basic bond pricing

## Standards and Compliance

- All calculations must maintain audit trail with:
  - Input parameters (coupon, yield, maturity, face value)
  - Calculation methodology
  - Date/time of calculation
  - Data sources

- Python implementations must include:
  - Type hints for all functions
  - Comprehensive docstrings
  - Unit tests with known solutions
  - Error handling for edge cases

## Version Control

**Version**: 1.0.0
**Last Updated**: 2025-12-07
**Author**: Ordinis-1 Bond Analysis Framework
**Status**: Production Ready

## Notes

This skill forms the foundation for all advanced bond analytics. Proficiency in bond pricing is essential before progressing to duration, convexity, or option-adjusted analysis.

---

**Next Skills**: Proceed to `yield-measures/` after mastering bond pricing fundamentals.
