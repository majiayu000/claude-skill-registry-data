---
skill_id: position_sizer
name: Position Sizer
version: 1.0.0
description: Calculates optimal position sizes using volatility-adjusted methods, Kelly Criterion, and risk management
author: Trading System CTO
tags: [position-sizing, risk-management, volatility, kelly-criterion, trading]
tools:
  - calculate_position_size
  - calculate_portfolio_heat
  - adjust_position_for_volatility
  - calculate_kelly_fraction
dependencies:
  - src/core/risk_manager.py
  - src/agents/risk_agent.py
integrations:
  - src/core/risk_manager.py::RiskManager.calculate_position_size
  - src/agents/risk_agent.py::RiskAgent._calculate_position_size
---

# Position Sizer Skill

Advanced position sizing using multiple methodologies to optimize risk-adjusted returns.

## Overview

This skill provides:
- Fixed percentage method (simple risk-based sizing)
- Volatility-adjusted sizing (normalizes risk across assets)
- Kelly Criterion (optimal growth rate calculation)
- ATR-based sizing (Average True Range volatility)
- Portfolio heat management (total risk exposure)
- Dynamic position adjustments based on volatility changes

## Position Sizing Methods

### 1. Fixed Percentage Method
Risk a fixed % of account per trade (e.g., 1-2%).

**Formula**: `Position Size = (Account Value × Risk %) ÷ (Entry Price - Stop Price)`

**Best For**:
- Consistent risk management
- Beginning traders
- Low volatility markets

### 2. Volatility-Adjusted Method
Adjusts size based on asset volatility.

**Formula**: `Adjusted Size = Base Size × (Target Vol ÷ Asset Vol)`

**Best For**:
- Multi-asset portfolios
- Variable volatility regimes
- Professional risk management

### 3. Kelly Criterion
Maximizes long-term growth rate based on edge.

**Formula**: `Kelly % = (Win Rate × Avg Win/Loss Ratio - (1 - Win Rate)) ÷ Avg Win/Loss Ratio`

**Best For**:
- Systems with known edge
- Experienced traders
- Always use fractional Kelly (25-50%)

### 4. ATR-Based Method
Uses Average True Range for volatility assessment.

**Formula**: `Position Size = (Account × Risk %) ÷ (ATR × Multiplier)`

**Best For**:
- Trend-following strategies
- Volatile markets
- Technical traders

## Tools

### 1. calculate_position_size

Calculates optimal position size for a trade.

**Parameters:**
- `symbol` (required): Trading symbol
- `account_value` (required): Current account value
- `risk_per_trade_pct` (optional): Risk per trade % (default: 1.0)
- `method` (optional): Sizing method ("fixed_pct", "volatility_adjusted", "kelly", "atr", default: "volatility_adjusted")
- `current_price` (optional): Current market price
- `stop_loss_price` (optional): Planned stop loss price
- `win_rate` (optional): Historical win rate (for Kelly, default: 0.55)
- `avg_win_loss_ratio` (optional): Average win/loss ratio (for Kelly, default: 1.5)

**Returns:**
```json
{
  "success": true,
  "symbol": "AAPL",
  "recommendations": {
    "primary_method": {
      "method": "volatility_adjusted",
      "position_size_dollars": 5420.00,
      "position_size_shares": 35,
      "rationale": "Adjusted for 18.5% annualized volatility"
    },
    "alternative_methods": {
      "fixed_percentage": {
        "position_size_dollars": 5000.00,
        "position_size_shares": 32
      },
      "kelly_criterion": {
        "position_size_dollars": 6250.00,
        "position_size_shares": 40,
        "kelly_fraction": 0.25
      },
      "atr_based": {
        "position_size_dollars": 5100.00,
        "position_size_shares": 33
      }
    }
  },
  "risk_metrics": {
    "dollar_risk": 500.00,
    "risk_pct": 1.0,
    "position_value_pct": 5.42,
    "estimated_volatility": 0.185,
    "max_loss_at_stop": 500.00
  },
  "constraints": {
    "max_position_size_dollars": 10000.00,
    "max_position_size_pct": 10.0,
    "min_position_size_dollars": 100.00,
    "constrained": false
  },
  "validation": {
    "within_risk_limits": true,
    "sufficient_buying_power": true,
    "liquidity_adequate": true
  }
}
```

**Usage:**
```bash
python scripts/position_sizer.py calculate_position_size \
    --symbol AAPL \
    --account-value 100000 \
    --risk-per-trade-pct 1.0 \
    --method volatility_adjusted \
    --current-price 155.00 \
    --stop-loss-price 150.00
```

### 2. calculate_portfolio_heat

Calculates total risk exposure across all positions.

**Parameters:**
- `account_value` (required): Current account value
- `positions` (required): Array of current open positions
- `pending_trades` (optional): Array of trades being considered

**Returns:**
```json
{
  "success": true,
  "portfolio_heat": {
    "total_risk_dollars": 2500.00,
    "total_risk_pct": 2.5,
    "individual_positions": [
      {
        "symbol": "AAPL",
        "position_value": 5000.00,
        "risk_dollars": 500.00,
        "risk_pct": 0.5,
        "stop_loss": 148.50
      }
    ],
    "risk_distribution": {
      "tech_sector": 1.2,
      "finance_sector": 0.8,
      "healthcare_sector": 0.5
    },
    "capacity": {
      "max_total_risk_pct": 5.0,
      "remaining_capacity_pct": 2.5,
      "remaining_capacity_dollars": 2500.00
    }
  },
  "recommendations": {
    "can_add_position": true,
    "max_new_position_dollars": 1000.00,
    "warnings": []
  }
}
```

### 3. adjust_position_for_volatility

Adjusts existing position size based on volatility changes.

**Parameters:**
- `symbol` (required): Trading symbol
- `current_position_value` (required): Current position value
- `target_volatility` (optional): Target volatility % (default: 20.0)
- `rebalance_threshold` (optional): Rebalance if exceeds threshold (default: 0.15)

**Returns:**
```json
{
  "success": true,
  "symbol": "AAPL",
  "analysis": {
    "current_position_value": 5000.00,
    "current_volatility": 0.28,
    "target_volatility": 0.20,
    "volatility_ratio": 1.40
  },
  "recommendation": {
    "action": "reduce",
    "target_position_value": 3571.00,
    "adjustment_amount": -1429.00,
    "adjustment_shares": -9,
    "rationale": "Current volatility 40% above target"
  },
  "execution_plan": {
    "recommended": true,
    "urgency": "medium",
    "method": "market_order"
  }
}
```

### 4. calculate_kelly_fraction

Calculates Kelly Criterion for position sizing.

**Parameters:**
- `win_rate` (required): Probability of winning (0-1)
- `avg_win_loss_ratio` (required): Average win ÷ average loss
- `kelly_multiplier` (optional): Conservative multiplier (default: 0.25)

**Returns:**
```json
{
  "success": true,
  "kelly_calculation": {
    "raw_kelly_pct": 25.5,
    "adjusted_kelly_pct": 6.375,
    "kelly_multiplier": 0.25,
    "inputs": {
      "win_rate": 0.55,
      "avg_win_loss_ratio": 1.8
    },
    "formula": "(win_rate * avg_win_loss_ratio - (1 - win_rate)) / avg_win_loss_ratio"
  },
  "recommendation": {
    "position_size_pct": 6.375,
    "rationale": "Using 25% Kelly for conservative approach",
    "warnings": [
      "Full Kelly (25.5%) is aggressive - using fractional Kelly"
    ]
  }
}
```

## Safety Constraints

### Hard Limits
- **Max Single Position**: 10% of account value (configurable)
- **Max Total Risk**: 5% of account value
- **Min Position Size**: $100 (avoid excessive trading costs)
- **Max Leverage**: 2x (if using margin)

### Dynamic Adjustments
- Reduce size after losing streaks
- Increase size cautiously after winning streaks
- Scale down in high volatility
- Respect circuit breakers

## Integration with Risk Manager

This skill wraps and extends the existing `src/core/risk_manager.py`:

```python
from claude_skills import load_skill

position_skill = load_skill("position_sizer")

# Calculate position size for new trade
position = position_skill.calculate_position_size(
    symbol="AAPL",
    account_value=100000,
    risk_per_trade_pct=1.0,
    method="volatility_adjusted",
    current_price=155.00,
    stop_loss_price=150.00
)

# Check portfolio capacity before adding
heat = position_skill.calculate_portfolio_heat(
    account_value=100000,
    positions=current_positions,
    pending_trades=[position]
)

if heat["recommendations"]["can_add_position"]:
    execute_trade(position)
```

## Usage Example

```python
from claude_skills import load_skill

position_skill = load_skill("position_sizer")

# Calculate position size for new trade
position = position_skill.calculate_position_size(
    symbol="AAPL",
    account_value=100000,
    risk_per_trade_pct=1.0,
    method="volatility_adjusted",
    current_price=155.00,
    stop_loss_price=150.00
)

# Check portfolio capacity
heat = position_skill.calculate_portfolio_heat(
    account_value=100000,
    positions=current_positions
)

if heat["recommendations"]["can_add_position"]:
    execute_trade(position)
```

## CLI Usage

```bash
# Calculate position size
python scripts/position_sizer.py calculate_position_size \
    --symbol AAPL --account-value 100000 --risk-per-trade-pct 1.0

# Calculate portfolio heat
python scripts/position_sizer.py calculate_portfolio_heat \
    --account-value 100000 --positions-file positions.json

# Calculate Kelly fraction
python scripts/position_sizer.py calculate_kelly_fraction \
    --win-rate 0.55 --avg-win-loss-ratio 1.8
```
