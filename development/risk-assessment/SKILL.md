---
name: risk-assessment
description: Use this skill when evaluating portfolio risk, checking position sizes, assessing market volatility, or performing risk management checks before trade execution. Based on TradingAgents risk management framework with conservative/aggressive/neutral debate system.
---

# Risk Assessment Skill

## When to Use
Activate when:
- Evaluating trade risk before execution
- Checking portfolio exposure and concentration
- Assessing market volatility levels
- Determining appropriate position sizes
- Reviewing risk/reward ratios
- Performing pre-trade risk checks

## Risk Management Framework (refs/TradingAgents/)

### Risk Debate System (refs/TradingAgents/tradingagents/agents/risk_mgmt/)

**Three Risk Perspectives**:
1. **Conservative Debator** (conservative_debator.py)
   - Focuses on downside protection
   - Emphasizes capital preservation
   - Advocates for smaller positions
   - Highlights potential risks

2. **Aggressive Debator** (aggresive_debator.py)
   - Focuses on upside potential
   - Advocates for larger positions
   - Emphasizes opportunity cost
   - Pushes for action

3. **Neutral Debator** (neutral_debator.py)
   - Balanced perspective
   - Data-driven analysis
   - Objective risk assessment
   - Mediation between extremes

### Risk Manager (refs/TradingAgents/tradingagents/agents/managers/risk_manager.py)

**Responsibilities**:
- Evaluate portfolio risk continuously
- Assess market volatility
- Check liquidity conditions
- Review proposed trades
- Provide final approval/rejection
- Monitor overall portfolio health

## Risk Assessment Process

### Step 1: Portfolio Risk Analysis

```python
def assess_portfolio_risk(portfolio: Dict, market_data: Dict) -> Dict:
    """
    Analyze current portfolio risk metrics
    """

    # 1. Calculate portfolio value
    total_value = portfolio["cash"]
    for ticker, shares in portfolio["positions"].items():
        current_price = market_data[ticker]["price"]
        total_value += shares * current_price

    # 2. Position concentration
    concentrations = {}
    for ticker, shares in portfolio["positions"].items():
        position_value = shares * market_data[ticker]["price"]
        concentration_pct = (position_value / total_value) * 100
        concentrations[ticker] = concentration_pct

    # 3. Identify concentration risk
    max_concentration = max(concentrations.values()) if concentrations else 0
    high_concentration = max_concentration > 20  # Alert if >20% in one position

    # 4. Calculate diversification
    num_positions = len([s for s in portfolio["positions"].values() if s > 0])
    diversification_score = min(num_positions / 10, 1.0)  # Ideal: 10+ positions

    # 5. Cash buffer
    cash_pct = (portfolio["cash"] / total_value) * 100
    adequate_cash = cash_pct >= 10  # Want at least 10% cash

    return {
        "total_value": total_value,
        "cash_pct": cash_pct,
        "adequate_cash": adequate_cash,
        "num_positions": num_positions,
        "max_concentration": max_concentration,
        "high_concentration_risk": high_concentration,
        "diversification_score": diversification_score,
        "concentrations": concentrations
    }
```

### Step 2: Market Volatility Assessment

```python
def assess_market_volatility(ticker: str, market_data: Dict) -> Dict:
    """
    Evaluate current market volatility using technical indicators
    """

    # Use indicators from market-analysis skill
    indicators = get_indicators(
        ticker,
        ["atr", "boll_ub", "boll_lb", "boll"],
        start_date,
        end_date
    )

    # ATR (Average True Range) - absolute volatility
    atr = indicators["atr"][-1]  # Latest value
    price = market_data[ticker]["price"]
    atr_pct = (atr / price) * 100  # As percentage of price

    # Bollinger Band width - relative volatility
    bb_width = ((indicators["boll_ub"][-1] - indicators["boll_lb"][-1])
                / indicators["boll"][-1]) * 100

    # Classify volatility
    if atr_pct < 2:
        volatility_level = "Low"
    elif atr_pct < 4:
        volatility_level = "Medium"
    else:
        volatility_level = "High"

    return {
        "ticker": ticker,
        "atr": atr,
        "atr_pct": atr_pct,
        "bb_width": bb_width,
        "volatility_level": volatility_level,
        "high_volatility": atr_pct > 4
    }
```

### Step 3: Position Sizing

```python
def calculate_position_size(
    ticker: str,
    portfolio: Dict,
    volatility: Dict,
    risk_tolerance: str = "medium"
) -> Dict:
    """
    Determine appropriate position size based on risk
    """

    total_value = calculate_portfolio_value(portfolio, market_data)

    # Risk tolerance factors
    risk_factors = {
        "conservative": 0.02,  # Risk 2% per position
        "medium": 0.05,        # Risk 5% per position
        "aggressive": 0.10     # Risk 10% per position
    }

    risk_factor = risk_factors.get(risk_tolerance, 0.05)

    # Adjust for volatility
    if volatility["volatility_level"] == "High":
        risk_factor *= 0.5  # Reduce position size in high volatility
    elif volatility["volatility_level"] == "Low":
        risk_factor *= 1.2  # Can increase slightly in low volatility

    # Maximum position value
    max_position_value = total_value * risk_factor

    # Calculate shares
    current_price = market_data[ticker]["price"]
    max_shares = int(max_position_value / current_price)

    # Ensure we have enough cash
    available_cash = portfolio["cash"]
    affordable_shares = int(available_cash / current_price)

    recommended_shares = min(max_shares, affordable_shares)

    return {
        "ticker": ticker,
        "recommended_shares": recommended_shares,
        "position_value": recommended_shares * current_price,
        "pct_of_portfolio": (recommended_shares * current_price / total_value) * 100,
        "risk_factor_used": risk_factor,
        "volatility_adjusted": volatility["volatility_level"] != "Medium"
    }
```

### Step 4: Trade Evaluation

```python
def evaluate_proposed_trade(
    action: str,
    ticker: str,
    shares: int,
    portfolio: Dict,
    market_data: Dict,
    analysis: Dict
) -> Dict:
    """
    Full risk assessment of proposed trade
    Run the 3-way risk debate (conservative/aggressive/neutral)
    """

    # 1. Get current risk metrics
    portfolio_risk = assess_portfolio_risk(portfolio, market_data)
    volatility = assess_market_volatility(ticker, market_data)

    # 2. Conservative perspective
    conservative_view = {
        "recommendation": "REDUCE_SIZE" if action == "BUY" else "APPROVE",
        "concerns": [],
        "suggested_adjustment": 0.5  # Reduce by 50%
    }

    if portfolio_risk["high_concentration_risk"]:
        conservative_view["concerns"].append("Portfolio too concentrated")
    if not portfolio_risk["adequate_cash"]:
        conservative_view["concerns"].append("Insufficient cash buffer")
    if volatility["high_volatility"]:
        conservative_view["concerns"].append("High market volatility")

    # 3. Aggressive perspective
    aggressive_view = {
        "recommendation": "APPROVE" if action in ["BUY", "SELL"] else "INCREASE",
        "opportunities": [],
        "suggested_adjustment": 1.5  # Increase by 50%
    }

    if action == "BUY" and analysis.get("strong_signal"):
        aggressive_view["opportunities"].append("Strong buy signal")
    if portfolio_risk["cash_pct"] > 50:
        aggressive_view["opportunities"].append("Excess cash - opportunity cost")

    # 4. Neutral/balanced perspective
    position_size = calculate_position_size(ticker, portfolio, volatility)

    neutral_view = {
        "recommendation": "APPROVE_WITH_ADJUSTMENT",
        "suggested_shares": position_size["recommended_shares"],
        "reasoning": "Balanced approach based on portfolio size and volatility"
    }

    # 5. Risk Manager final decision
    final_decision = make_final_risk_decision(
        conservative_view,
        aggressive_view,
        neutral_view,
        portfolio_risk
    )

    return {
        "trade_details": {
            "action": action,
            "ticker": ticker,
            "requested_shares": shares,
            "price": market_data[ticker]["price"]
        },
        "risk_assessment": {
            "portfolio_risk": portfolio_risk,
            "market_volatility": volatility
        },
        "debate_views": {
            "conservative": conservative_view,
            "aggressive": aggressive_view,
            "neutral": neutral_view
        },
        "final_decision": final_decision,
        "approved": final_decision["approved"],
        "final_shares": final_decision.get("final_shares", shares)
    }

def make_final_risk_decision(
    conservative: Dict,
    aggressive: Dict,
    neutral: Dict,
    portfolio_risk: Dict
) -> Dict:
    """Risk manager makes final call"""

    # Default to neutral recommendation
    approved = True
    final_shares = neutral["suggested_shares"]
    reasoning = neutral["reasoning"]

    # Override if major risks
    critical_risks = [
        portfolio_risk["high_concentration_risk"],
        not portfolio_risk["adequate_cash"],
        portfolio_risk["diversification_score"] < 0.3
    ]

    if any(critical_risks):
        approved = False
        reasoning = "Trade rejected due to critical portfolio risks: " + \
                   ", ".join(conservative["concerns"])

    return {
        "approved": approved,
        "final_shares": final_shares if approved else 0,
        "reasoning": reasoning,
        "risk_level": "HIGH" if any(critical_risks) else "MODERATE"
    }
```

## Risk Report Format

```markdown
## Risk Assessment Report

### Portfolio Status
- **Total Value**: ${total_value}
- **Cash**: ${cash} ({cash_pct}%)
- **Positions**: {num_positions}
- **Diversification Score**: {score}/1.0

### Concentration Analysis
| Ticker | Value | % of Portfolio | Risk Level |
|--------|-------|----------------|------------|
| AAPL   | $2500 | 25%            | HIGH       |
| NVDA   | $1800 | 18%            | MEDIUM     |
| MSFT   | $1200 | 12%            | OK         |

### Market Volatility
- **{Ticker} ATR**: {value}% - {volatility_level}
- **Bollinger Width**: {value}%
- **Assessment**: {interpretation}

### Proposed Trade Evaluation
**Trade**: {action} {shares} shares of {ticker} @ ${price}

**Risk Debate Summary**:
- **Conservative**: {recommendation} - Concerns: {list}
- **Aggressive**: {recommendation} - Opportunities: {list}
- **Neutral**: {recommendation} - {reasoning}

**Final Decision**: {APPROVED/REJECTED}
**Recommended Shares**: {final_shares}
**Risk Level**: {HIGH/MODERATE/LOW}

**Reasoning**: {detailed explanation}
```

## Integration with Trading Flow

### Pre-Trade Risk Check
```python
async def execute_trade_with_risk_check(
    model_name: str,
    action: str,
    ticker: str,
    shares: int
) -> Dict:
    """
    Always perform risk assessment before trade execution
    """

    # 1. Get current portfolio and market data
    portfolio = get_model_portfolio(model_name)
    market_data = get_current_market_data([ticker])

    # 2. Get analysis that led to this decision
    analysis = get_latest_analysis(model_name, ticker)

    # 3. Run risk assessment
    risk_eval = evaluate_proposed_trade(
        action, ticker, shares,
        portfolio, market_data, analysis
    )

    # 4. Log risk assessment to ModelChat
    await log_risk_assessment(model_name, ticker, risk_eval)

    # 5. Execute only if approved
    if risk_eval["approved"]:
        final_shares = risk_eval["final_decision"]["final_shares"]
        result = await execute_trade(
            model_name, action, ticker,
            final_shares, market_data[ticker]["price"]
        )
        return {
            "success": True,
            "trade": result,
            "risk_assessment": risk_eval
        }
    else:
        return {
            "success": False,
            "reason": risk_eval["final_decision"]["reasoning"],
            "risk_assessment": risk_eval
        }
```

## Risk Limits & Guardrails

### Hard Limits
```python
RISK_LIMITS = {
    "max_position_pct": 20,      # No single position >20% of portfolio
    "min_cash_pct": 10,          # Keep at least 10% cash
    "max_concentration_top3": 50, # Top 3 positions <50% combined
    "min_diversification": 5,     # At least 5 different positions
    "max_daily_trades": 10,       # Limit to 10 trades per day
    "max_leverage": 1.0           # No leverage (paper trading)
}

def check_hard_limits(portfolio: Dict, proposed_trade: Dict) -> Dict:
    """
    Check if trade violates hard limits
    """
    violations = []

    # Check each limit
    # ... (implementation details)

    return {
        "passed": len(violations) == 0,
        "violations": violations
    }
```

## Code References

All code from `refs/TradingAgents/`:
- Risk Manager: `tradingagents/agents/managers/risk_manager.py`
- Conservative Debator: `tradingagents/agents/risk_mgmt/conservative_debator.py`
- Aggressive Debator: `tradingagents/agents/risk_mgmt/aggresive_debator.py`
- Neutral Debator: `tradingagents/agents/risk_mgmt/neutral_debator.py`
- Agent States: `tradingagents/agents/utils/agent_states.py`

## Best Practices

1. **Always run risk check before trade execution**
2. **Use 3-way debate** for balanced perspective
3. **Adjust for volatility** - reduce size in volatile markets
4. **Monitor concentration** - no single position >20%
5. **Maintain cash buffer** - keep minimum 10% cash
6. **Diversify holdings** - aim for 10+ positions
7. **Log all risk decisions** to ModelChat for audit trail
8. **Respect hard limits** - never override critical guardrails

## Usage Example

**User**: "Check if it's safe to buy 100 shares of NVDA"

**Execution**:
1. Fetch current portfolio state
2. Analyze NVDA volatility (ATR, Bollinger Bands)
3. Check portfolio concentration
4. Run 3-way risk debate
5. Calculate recommended position size
6. Make final approval decision
7. Generate detailed risk report
8. Log to ModelChat
