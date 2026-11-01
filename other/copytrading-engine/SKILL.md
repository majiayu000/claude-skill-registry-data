---
name: copytrading-engine
description: Copy Trading Engine Engineer — Institutional capability and runbook for copytrading-engine.
---

# SKILL: Copy Trading Engine Engineer
## Domain: imCopying — Provider/Subscriber System, Signal Routing, Risk Engine

**Activation triggers:** copy trading, provider registration, subscription,
signal routing, risk limits, performance tracking, execution logs.

---

## Domain Model

```
Provider (trader who shares signals)
  ├── has many CopySubscriptions (subscribers)
  ├── has many ProviderSignals (trade signals emitted)
  ├── has many ProviderPerformanceSnapshots (daily stats)
  └── has many Reviews

CopySubscription (follower relationship)
  ├── belongs to Provider
  ├── has one source broker account (subscriber's account)
  └── has many ExecutionLogs (trades copied)
```

---

## SQLAlchemy Registry Rules for Copy Trading

```python
# CRITICAL: These names must be unique across ALL SQLAlchemy models in the app
# The expert backend imports from both app.models.user AND app.models.copy_trading

class CopySubscription(Base):       # NOT "Subscription" — conflicts with iam.Subscription
    __tablename__ = "subscriptions"
    __table_args__ = {"schema": "copy_trading"}

class ProviderPerformanceSnapshot(Base):
    # ForeignKey MUST be declared — TimescaleDB hypertables strip FK constraints
    # at DB level but SQLAlchemy ORM still needs them for relationship resolution
    provider_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("copy_trading.providers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    provider: Mapped["Provider"] = relationship("Provider", lazy="noload")

class ExecutionLog(Base):
    # Same pattern — ForeignKey required even on hypertables
    subscription_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("copy_trading.subscriptions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    subscription: Mapped["CopySubscription"] = relationship("CopySubscription", lazy="noload")
```

---

## Signal Routing Flow

```
Provider places trade on their broker
    → MT5/broker webhook fires
    → ProviderSignal created in copy_trading.provider_signals
    → SignalService.route_signal() called
    → Fetch all active CopySubscriptions for this provider
    → For each subscriber:
        → RiskEngine.check_limits(subscription, signal)  ← blocks if limit exceeded
        → Execute trade on subscriber's broker adapter
        → Log to ExecutionLog
        → Update ProviderPerformanceSnapshot
```

---

## Risk Engine Rules

```python
class RiskEngine:
    async def check_limits(
        self, subscription: CopySubscription, signal: ProviderSignal
    ) -> tuple[bool, str]:
        """Returns (allowed, reason). Reason is empty string if allowed."""

        # 1. Max drawdown check
        if subscription.max_drawdown_pct and self._current_drawdown(subscription) > subscription.max_drawdown_pct:
            return False, "Max drawdown limit exceeded"

        # 2. Daily loss limit
        if subscription.daily_loss_limit and self._daily_loss(subscription) > subscription.daily_loss_limit:
            return False, "Daily loss limit exceeded"

        # 3. Max lot size
        adjusted_lot = signal.lot_size * (subscription.copy_ratio or 1.0)
        if subscription.max_lot_size and adjusted_lot > subscription.max_lot_size:
            adjusted_lot = subscription.max_lot_size

        # 4. Symbol filter
        if subscription.allowed_symbols and signal.symbol not in subscription.allowed_symbols:
            return False, f"Symbol {signal.symbol} not in allowed list"

        return True, ""
```

---

## Copy Mode Reference

```
MIRROR_EXACT   → Copy exact lot size from provider
MIRROR_RATIO   → Copy proportional to account balance ratio
FIXED_LOT      → Always copy with fixed lot size (subscription.fixed_lot)
MANUAL         → Signals shown but not auto-executed
```

---

## Anti-Patterns

```
✗ Using "Subscription" as SQLAlchemy class name (conflicts with iam.Subscription)
✗ Missing ForeignKey on TimescaleDB hypertable columns
✗ Executing trades synchronously in signal handler (use async worker)
✗ Missing risk checks before execution
✗ No ExecutionLog entry (audit trail is mandatory)
✗ Provider can subscribe to themselves
✗ Missing copy_ratio bounds (allow 0.1x to 10x only)
```
