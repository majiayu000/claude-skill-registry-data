---
name: "new-strategy"
description: "Use this skill ONLY when creating a new trading strategy (e.g., MeanReversion, Breakout, ScalpingStrategy). Do not use for agents or scanners. This skill is part of the Phase 1 migration."
---

# Scope Constraint

**CRITICAL:** You are executing from the repository root.

- Strategy files go in `src/alpacalyzer/strategies/{name}.py`
- Tests go in `tests/test_{name}_strategy.py`
- Strategies evaluate entry/exit conditions based on signals

# Context: Migration Phase 1

This skill supports the **Strategy Abstraction** migration (Phase 1 in `migration_plan.md`). The goal is to make trading strategies pluggable and testable.

**Key concepts**:

- `Strategy` protocol defines the interface
- `BaseStrategy` provides common functionality
- `StrategyConfig` holds strategy parameters
- Strategies evaluate `TradingSignals` and return `EntryDecision`/`ExitDecision`

# Template Placeholders

- `<strategy>` - lowercase (e.g., `mean_reversion`, `breakout`)
- `<Strategy>` - PascalCase (e.g., `MeanReversion`, `Breakout`)

# Procedural Steps

## 1. Review Strategy Base Classes

**CRITICAL**: Read the strategy base classes first:

```bash
# Check if base classes exist (Phase 1 migration)
cat src/alpacalyzer/strategies/base.py
cat src/alpacalyzer/strategies/config.py

# Review existing strategy (momentum is the reference)
cat src/alpacalyzer/strategies/momentum.py
```

**If base classes don't exist yet**: You are implementing Phase 1! See `migration_plan.md` sections 1.1 and 1.2 first.

## 2. Define Strategy Configuration

Each strategy needs a `StrategyConfig` with its parameters.

**Location**: `src/alpacalyzer/strategies/<strategy>.py` (config can be inline or separate)

**Example config**:

```python
from dataclasses import dataclass, field
from alpacalyzer.strategies.base import StrategyConfig


# Default config for this strategy
DEFAULT_<STRATEGY>_CONFIG = StrategyConfig(
    name="<strategy>",
    description="<Brief description of strategy approach>",

    # Position sizing
    max_position_pct=0.05,  # 5% of portfolio per position

    # Risk management
    stop_loss_pct=0.03,     # 3% stop loss
    target_pct=0.09,        # 9% target (3:1 R:R)
    trailing_stop=False,

    # Entry filters (customize for your strategy)
    min_confidence=70.0,
    min_ta_score=0.6,
    min_momentum=-5.0,

    # Exit filters (customize for your strategy)
    exit_momentum_threshold=-15.0,
    exit_score_threshold=0.3,

    # Strategy-specific parameters
    params={
        "<param1>": <value1>,
        "<param2>": <value2>,
    }
)
```

## 3. Implement Strategy Class

**Location**: `src/alpacalyzer/strategies/<strategy>.py`

**Template structure**:

```python
"""<Strategy> trading strategy."""

from alpacalyzer.strategies.base import (
    BaseStrategy, StrategyConfig, MarketContext,
    EntryDecision, ExitDecision
)
from alpacalyzer.analysis.technical_analysis import TradingSignals, TechnicalAnalyzer
from alpacalyzer.data.models import TradingStrategy as AgentRecommendation


class <Strategy>Strategy(BaseStrategy):
    """
    <Strategy> trading strategy.

    Strategy Logic:
        Entry:
            - <Entry condition 1>
            - <Entry condition 2>
            - <Entry condition 3>

        Exit:
            - <Exit condition 1>
            - <Exit condition 2>
            - <Exit condition 3>

    Best Used For:
        - <Market condition 1>
        - <Market condition 2>

    Risk Profile:
        - <Risk characteristic 1>
        - <Risk characteristic 2>
    """

    def __init__(self, config: StrategyConfig | None = None):
        """
        Initialize <Strategy> strategy.

        Args:
            config: Strategy configuration (uses default if None)
        """
        if config is None:
            config = DEFAULT_<STRATEGY>_CONFIG
        super().__init__(config)
        self.ta = TechnicalAnalyzer()

    def evaluate_entry(
        self,
        signal: TradingSignals,
        context: MarketContext,
        agent_recommendation: AgentRecommendation | None = None
    ) -> EntryDecision:
        """
        Evaluate entry conditions for <strategy> strategy.

        Args:
            signal: Current trading signals (price, momentum, technical indicators)
            context: Market context (account, positions, cooldowns)
            agent_recommendation: Optional AI agent recommendation

        Returns:
            EntryDecision with should_enter, reason, and order parameters
        """
        # Step 1: Check basic filters (market open, cooldown, existing position)
        passed, reason = self._check_basic_filters(signal, context)
        if not passed:
            return EntryDecision(should_enter=False, reason=reason)

        # Step 2: Extract relevant signals
        momentum = signal["momentum"]
        score = signal["score"]
        price = signal["price"]
        atr = signal["atr"]
        signals_list = signal["signals"]

        # Step 3: Strategy-specific entry logic
        # TODO: Implement your strategy's entry conditions

        # Example: Mean reversion strategy
        # if score < 0.3 and momentum < -10:
        #     # Oversold condition
        #     ...

        # Example: Breakout strategy
        # has_breakout = any("Breakout" in s for s in signals_list)
        # if has_breakout and momentum > 5:
        #     # Breakout with momentum
        #     ...

        # Step 4: Check for weak signals
        weak_signals = self.ta.weak_technicals(signals_list, "buy")
        if weak_signals:
            return EntryDecision(
                should_enter=False,
                reason=f"Weak technical signals: {weak_signals}"
            )

        # Step 5: Calculate position parameters
        stop_loss = price - (atr * 1.5)  # Customize based on strategy
        target = price + (atr * 4.5)     # Customize based on strategy

        # Use agent recommendation if available
        if agent_recommendation:
            stop_loss = agent_recommendation.stop_loss
            target = agent_recommendation.target_price

        size = self.calculate_position_size(signal, context, context.buying_power)

        return EntryDecision(
            should_enter=True,
            reason=f"<Strategy> entry: <reason details>",
            suggested_size=size,
            entry_price=price,
            stop_loss=stop_loss,
            target=target
        )

    def evaluate_exit(
        self,
        position: "TrackedPosition",
        signal: TradingSignals,
        context: MarketContext
    ) -> ExitDecision:
        """
        Evaluate exit conditions for <strategy> strategy.

        Args:
            position: Current position with P&L info
            signal: Current trading signals
            context: Market context

        Returns:
            ExitDecision with should_exit, reason, and urgency
        """
        momentum = signal["momentum"]
        score = signal["score"]
        is_profitable = position.unrealized_pnl_pct > 0

        # Step 1: Profitable position logic
        if is_profitable:
            # TODO: Implement profit-taking logic
            # Example: Trail stop, target hit, reversal signal

            if momentum < self.config.exit_momentum_threshold:
                return ExitDecision(
                    should_exit=True,
                    reason=f"Major reversal: momentum {momentum:.1f}%",
                    urgency="urgent"
                )

            return ExitDecision(should_exit=False, reason="Profitable, holding")

        # Step 2: Losing position logic
        weak_signals = self.ta.weak_technicals(signal["signals"], "buy")

        # TODO: Implement stop-loss and cut-loss logic
        # Example: Strict stop on weak signals, catastrophic drop

        if momentum < -25:
            return ExitDecision(
                should_exit=True,
                reason=f"Catastrophic drop: {momentum:.1f}%",
                urgency="immediate"
            )

        return ExitDecision(should_exit=False, reason="Exit conditions not met")
```

## 4. Register Strategy

Edit `src/alpacalyzer/strategies/registry.py`:

```python
# In _register_builtins() function:
from alpacalyzer.strategies.<strategy> import <Strategy>Strategy

def _register_builtins():
    from alpacalyzer.strategies.momentum import MomentumStrategy
    from alpacalyzer.strategies.<strategy> import <Strategy>Strategy

    StrategyRegistry.register("momentum", MomentumStrategy)
    StrategyRegistry.register("<strategy>", <Strategy>Strategy)
```

## 5. Write Comprehensive Tests

**Location**: `tests/test_<strategy>_strategy.py`

**Test template**:

```python
"""Tests for <Strategy> trading strategy."""

import pytest
from unittest.mock import MagicMock

from alpacalyzer.strategies.<strategy> import <Strategy>Strategy
from alpacalyzer.strategies.base import MarketContext, EntryDecision, ExitDecision


@pytest.fixture
def market_context():
    """Standard market context for testing."""
    return MarketContext(
        vix=15.0,
        market_status="open",
        account_equity=100000.0,
        buying_power=50000.0,
        existing_positions=[],
        cooldown_tickers=[]
    )


@pytest.fixture
def bullish_signal():
    """Bullish trading signal."""
    return {
        "symbol": "AAPL",
        "price": 150.00,
        "score": 0.75,
        "momentum": 8.5,
        "atr": 3.0,
        "signals": ["Golden Cross", "RSI Bullish", "Volume Surge"],
        "rsi": 65,
        "macd": 2.5
    }


@pytest.fixture
def bearish_signal():
    """Bearish trading signal."""
    return {
        "symbol": "AAPL",
        "price": 150.00,
        "score": 0.25,
        "momentum": -12.0,
        "atr": 3.0,
        "signals": ["Death Cross", "RSI Bearish", "Breakdown"],
        "rsi": 25,
        "macd": -2.5
    }


def test_<strategy>_entry_bullish(bullish_signal, market_context):
    """Test <strategy> entry with bullish signals."""
    strategy = <Strategy>Strategy()

    decision = strategy.evaluate_entry(bullish_signal, market_context)

    # Adjust assertions based on your strategy logic
    assert isinstance(decision, EntryDecision)
    if decision.should_enter:
        assert decision.suggested_size > 0
        assert decision.entry_price > 0
        assert decision.stop_loss < decision.entry_price
        assert decision.target > decision.entry_price


def test_<strategy>_entry_bearish(bearish_signal, market_context):
    """Test <strategy> entry with bearish signals."""
    strategy = <Strategy>Strategy()

    decision = strategy.evaluate_entry(bearish_signal, market_context)

    # Most long-only strategies should not enter on bearish signals
    # Adjust based on your strategy (e.g., mean reversion might enter)
    assert isinstance(decision, EntryDecision)


def test_<strategy>_respects_market_closed(bullish_signal, market_context):
    """Test strategy does not enter when market is closed."""
    market_context.market_status = "closed"
    strategy = <Strategy>Strategy()

    decision = strategy.evaluate_entry(bullish_signal, market_context)

    assert not decision.should_enter
    assert "closed" in decision.reason.lower()


def test_<strategy>_respects_existing_position(bullish_signal, market_context):
    """Test strategy does not enter duplicate positions."""
    market_context.existing_positions = ["AAPL"]
    strategy = <Strategy>Strategy()

    decision = strategy.evaluate_entry(bullish_signal, market_context)

    assert not decision.should_enter
    assert "position" in decision.reason.lower()


def test_<strategy>_respects_cooldown(bullish_signal, market_context):
    """Test strategy respects cooldown period."""
    market_context.cooldown_tickers = ["AAPL"]
    strategy = <Strategy>Strategy()

    decision = strategy.evaluate_entry(bullish_signal, market_context)

    assert not decision.should_enter
    assert "cooldown" in decision.reason.lower()


def test_<strategy>_position_sizing(bullish_signal, market_context):
    """Test strategy calculates position size correctly."""
    strategy = <Strategy>Strategy()

    decision = strategy.evaluate_entry(bullish_signal, market_context)

    if decision.should_enter:
        # Position should not exceed max_position_pct of equity
        max_value = market_context.account_equity * strategy.config.max_position_pct
        position_value = decision.suggested_size * decision.entry_price
        assert position_value <= max_value

        # Position should not exceed buying power
        assert position_value <= market_context.buying_power


def test_<strategy>_exit_profitable_position():
    """Test exit logic for profitable position."""
    strategy = <Strategy>Strategy()

    # Mock position
    position = MagicMock()
    position.unrealized_pnl_pct = 8.0  # 8% profit
    position.symbol = "AAPL"

    # Create signal (adjust based on your exit logic)
    signal = {
        "symbol": "AAPL",
        "price": 162.00,
        "score": 0.6,
        "momentum": 3.0,
        "atr": 3.0,
        "signals": ["Bullish"],
    }

    context = MarketContext(
        vix=15.0,
        market_status="open",
        account_equity=100000.0,
        buying_power=50000.0,
        existing_positions=["AAPL"],
        cooldown_tickers=[]
    )

    decision = strategy.evaluate_exit(position, signal, context)

    # Strategy should hold profitable position unless strong reversal
    assert isinstance(decision, ExitDecision)


def test_<strategy>_exit_losing_position_catastrophic():
    """Test exit logic triggers on catastrophic loss."""
    strategy = <Strategy>Strategy()

    position = MagicMock()
    position.unrealized_pnl_pct = -4.0  # Losing
    position.symbol = "AAPL"

    signal = {
        "symbol": "AAPL",
        "price": 144.00,
        "score": 0.2,
        "momentum": -30.0,  # Catastrophic drop
        "atr": 3.0,
        "signals": ["Death Cross", "Breakdown"],
    }

    context = MarketContext(
        vix=30.0,
        market_status="open",
        account_equity=100000.0,
        buying_power=50000.0,
        existing_positions=["AAPL"],
        cooldown_tickers=[]
    )

    decision = strategy.evaluate_exit(position, signal, context)

    # Should exit on catastrophic drop
    assert decision.should_exit
    assert decision.urgency in ["urgent", "immediate"]


def test_<strategy>_with_agent_recommendation(bullish_signal, market_context):
    """Test strategy uses agent recommendation for stop/target."""
    strategy = <Strategy>Strategy()

    # Mock agent recommendation
    from alpacalyzer.data.models import TradingStrategy as AgentRec
    agent_rec = AgentRec(
        action="buy",
        quantity=100,
        stop_loss=145.00,
        target_price=160.00
    )

    decision = strategy.evaluate_entry(bullish_signal, market_context, agent_rec)

    if decision.should_enter:
        # Should use agent's stop/target
        assert decision.stop_loss == 145.00
        assert decision.target == 160.00
```

## 6. Run Tests

```bash
# Run strategy tests
uv run pytest tests/test_<strategy>_strategy.py -vv

# Run all strategy tests
uv run pytest tests/test_*_strategy.py

# Check coverage
uv run pytest tests/test_<strategy>_strategy.py --cov=src/alpacalyzer/strategies/<strategy>
```

## 7. Document Strategy

Add strategy documentation in docstring and README:

**In strategy file**:

````python
"""
<Strategy> Strategy

## Overview
<Detailed description of strategy approach>

## Entry Conditions
1. <Condition 1>
2. <Condition 2>
3. <Condition 3>

## Exit Conditions
1. <Condition 1>
2. <Condition 2>

## Risk Management
- Stop Loss: <description>
- Target: <description>
- Position Sizing: <description>

## Best Market Conditions
- <Condition 1>
- <Condition 2>

## Example Usage
```python
from alpacalyzer.strategies.<strategy> import <Strategy>Strategy
from alpacalyzer.strategies.registry import StrategyRegistry

# Use default config
strategy = StrategyRegistry.get("<strategy>")

# Or customize
from alpacalyzer.strategies.base import StrategyConfig
config = StrategyConfig(
    name="<strategy>",
    min_momentum=10.0,
    # ... other params
)
strategy = <Strategy>Strategy(config)
````

"""

```

# Reference: Existing Example

- `src/alpacalyzer/strategies/momentum.py` - Full reference implementation
- `src/alpacalyzer/strategies/base.py` - Base classes and protocols
- `migration_plan.md` Phase 1 - Strategy abstraction details

# Special Considerations

1. **Position Sizing**: Use `BaseStrategy.calculate_position_size()` or override with custom logic.

2. **Risk Management**: Every strategy must calculate stop_loss and target. Don't skip this!

3. **Agent Integration**: Strategies can optionally use AI agent recommendations for stop/target levels.

4. **Testing**: Test all entry/exit scenarios, including edge cases (market closed, duplicate positions, cooldown).

5. **Migration Phase**: This is Phase 1 of the migration. Strategies will eventually replace hardcoded logic in `trader.py`.

6. **Configuration**: Strategy parameters should be configurable via `StrategyConfig`, not hardcoded.

7. **Urgency Levels**: Exit decisions have urgency (`normal`, `urgent`, `immediate`) for prioritization.
```
