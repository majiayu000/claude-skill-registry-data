---
name: using-nautilus-trader
description: Provides expert guidance for NautilusTrader algorithmic trading platform. Covers backtesting strategies, live trading deployment, event-driven architecture, and building trading systems.
---

# NautilusTrader Skill

High-performance algorithmic trading platform with event-driven architecture. Identical code for backtesting and live trading. Rust/Cython core with Python bindings.

**Always consult official docs for current API** - the API evolves frequently with breaking changes before v2.x.

- **Docs:** https://nautilustrader.io/docs/latest/
- **API Reference:** https://nautilustrader.io/docs/latest/api_reference/
- **Source:** https://github.com/nautechsystems/nautilus_trader

## File Guide

**Core Development**
- [strategy-development.md](strategy-development.md) - Strategy class, lifecycle, event handlers, order submission
- [backtesting.md](backtesting.md) - BacktestNode/Engine setup, fill models, data catalog
- [live-trading.md](live-trading.md) - TradingNode deployment, Redis, production safety

**Data & Orders**
- [data-models.md](data-models.md) - QuoteTick, TradeTick, Bar, InstrumentId, BarType
- [orders.md](orders.md) - Order types, OrderFactory, bracket orders, emulation
- [cache.md](cache.md) - Query instruments, orders, positions, market data

**Components**
- [actors.md](actors.md) - Actor base class for non-trading components
- [indicators.md](indicators.md) - Built-in indicators, registration, custom indicators
- [portfolio.md](portfolio.md) - Account balances, positions, PnL calculations
- [execution.md](execution.md) - Execution flow, risk engine, execution algorithms

**Integration**
- [integrations.md](integrations.md) - Binance, Bybit, Interactive Brokers status
- [adapters.md](adapters.md) - Custom adapter implementation
- [architecture.md](architecture.md) - NautilusKernel, MessageBus, engines

**Reference**
- [examples.md](examples.md) - Complete working strategies
- [best-practices.md](best-practices.md) - Testing, optimization, safety
- [troubleshooting.md](troubleshooting.md) - Common issues
- [installation.md](installation.md) - Setup, precision modes

## Critical Patterns

**Register indicators BEFORE subscribing:**
```python
self.register_indicator_for_bars(self.bar_type, self.ema)
self.subscribe_bars(self.bar_type)  # Must be after registration
```

**Use strategy's order_factory:**
```python
order = self.order_factory.market(
    instrument_id=instrument_id,
    order_side=OrderSide.BUY,
    quantity=Quantity.from_str("1.0"),
)
self.submit_order(order)
```

**BarType string format:**
```python
# Format: {instrument_id}-{step}-{aggregation}-{price_type}-{source}
bar_type = BarType.from_str("BTCUSDT.BINANCE-1-MINUTE-LAST-EXTERNAL")
```

**InstrumentId format:**
```python
# Format: {symbol}.{venue}
instrument_id = InstrumentId.from_str("BTCUSDT.BINANCE")
```

**Quantity/Price from strings (avoids precision issues):**
```python
quantity = Quantity.from_str("1.5")
price = Price.from_str("50000.00")
```

**Check indicator initialization:**
```python
def on_bar(self, bar: Bar):
    if not self.ema.initialized:
        return
    # Safe to use self.ema.value
```

## OMS Types

- `OmsType.NETTING` - Single position per instrument (crypto-style)
- `OmsType.HEDGING` - Multiple positions per instrument (traditional futures)

## Account Types

- `AccountType.CASH` - Spot trading
- `AccountType.MARGIN` - Margin/leverage trading
