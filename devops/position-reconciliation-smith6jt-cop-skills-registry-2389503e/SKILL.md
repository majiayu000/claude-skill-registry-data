---
name: position-reconciliation
description: "Broker position reconciliation pattern for live trading systems"
author: Claude Code
date: 2025-12-16
---

# Position Reconciliation - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-12-16 |
| **Goal** | Sync internal position state with broker to prevent state drift |
| **Environment** | Python 3.10, Alpaca API |
| **Status** | Success |

## Context
Live trading systems maintain internal position state that can drift from reality:
- Orders execute but callback/update fails
- Manual interventions via broker UI
- Partial fills not properly tracked
- Network issues during order submission
- Broker-side corporate actions (splits, mergers)

Without reconciliation, the system may try to close positions it doesn't have or miss positions it should manage.

## Verified Workflow

### 1. Reconciliation Function
```python
def reconcile_positions(
    broker: Broker,
    states: Dict[str, PositionState],
    logger: logging.Logger,
) -> Dict[str, PositionState]:
    """
    Reconcile internal position state with broker's actual positions.

    Broker is source of truth - any discrepancies update internal state.
    """
    try:
        broker_positions = broker.get_positions()
        broker_symbols = set()

        for pos in broker_positions:
            symbol = pos.get('symbol', '')
            if not symbol:
                continue
            broker_symbols.add(symbol)

            # Parse broker position
            qty = float(pos.get('qty', 0))
            side = 1 if qty > 0 else (-1 if qty < 0 else 0)
            avg_entry = float(pos.get('avg_entry_price', 0))
            unrealized_pl = float(pos.get('unrealized_pl', 0))

            # Check if we have internal state
            if symbol in states:
                internal = states[symbol]

                # Check for quantity or side mismatch
                if abs(abs(qty) - internal.shares) > 0.001 or internal.side != side:
                    logger.warning(
                        f"RECONCILE {symbol}: Internal={internal.side}x{internal.shares:.4f} vs "
                        f"Broker={side}x{abs(qty):.4f} - updating to broker"
                    )
                    states[symbol] = PositionState(
                        side=side,
                        shares=abs(qty),
                        entry_price=avg_entry,
                        unrealized_pnl=unrealized_pl,
                        trade_count=internal.trade_count,  # Preserve history
                    )
            else:
                # Broker has position we don't track
                if qty != 0:
                    logger.warning(
                        f"RECONCILE {symbol}: Found untracked broker position "
                        f"{side}x{abs(qty):.4f} @ {avg_entry:.2f} - adding to state"
                    )
                    states[symbol] = PositionState(
                        side=side,
                        shares=abs(qty),
                        entry_price=avg_entry,
                        unrealized_pnl=unrealized_pl,
                        trade_count=0,
                    )

        # Check for internal positions broker doesn't have
        for symbol, internal in list(states.items()):
            if internal.side != 0 and symbol not in broker_symbols:
                logger.warning(
                    f"RECONCILE {symbol}: Internal shows {internal.side}x{internal.shares:.4f} "
                    f"but broker has no position - clearing internal state"
                )
                states[symbol] = PositionState(trade_count=internal.trade_count + 1)

        return states

    except Exception as e:
        logger.error(f"Position reconciliation failed: {e}")
        return states  # Return unchanged on error
```

### 2. Integration in Trading Loop
```python
# Run reconciliation periodically (every 30 min = 120 loops at 15s interval)
RECONCILIATION_INTERVAL = 120

while running:
    loop_count += 1

    # ... trading logic ...

    # Position reconciliation
    if loop_count % RECONCILIATION_INTERVAL == 0:
        logger.info("Running position reconciliation with broker...")
        states = reconcile_positions(broker, states, logger)

    time.sleep(15)
```

### 3. Broker API Response Format (Alpaca)
```python
# Example broker.get_positions() response
[
    {
        'symbol': 'AAPL',
        'qty': '10.5',           # Supports fractional
        'avg_entry_price': '150.25',
        'current_price': '152.00',
        'unrealized_pl': '18.375',
        'market_value': '1596.00',
        'side': 'long'
    },
    ...
]
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Only reconciling on startup | Drift accumulates over hours | Run periodically (every 30 min) |
| Internal state as source of truth | Broker has the real positions | Broker is ALWAYS truth |
| Not handling fractional shares | qty = 10.5 parsed as 10 | Use float(), not int() |
| Raising exception on mismatch | System stops on first discrepancy | Log warning, fix, continue |
| Clearing trade_count on reconcile | Lose performance history | Preserve trade_count field |
| Not handling new broker positions | Miss manual buys via UI | Add unknown positions to state |
| Exact quantity match only | Floating point issues | Use tolerance (0.001 shares) |

## Final Parameters
```python
# Recommended reconciliation settings
RECONCILIATION_INTERVAL = 120  # loops (30 min at 15s interval)
QUANTITY_TOLERANCE = 0.001     # shares - for floating point comparison
LOG_LEVEL = logging.WARNING    # Log discrepancies prominently
```

## Key Insights
- **Broker is ALWAYS source of truth** - Never override broker with internal state
- **Run periodically, not just on startup** - State can drift anytime
- **Preserve metadata on reconcile** - Keep trade_count, strategy attribution
- **Handle three cases**: Mismatch, untracked broker position, phantom internal position
- **Use tolerance for float comparison** - Exact equality fails with fractional shares
- **Log discrepancies prominently** - RECONCILE prefix for easy grep
- **Don't raise on errors** - Log and continue with existing state
- **Reconcile BEFORE trading logic** - Ensure state is accurate before decisions

## Edge Cases to Handle
```python
# 1. Partial fills
#    Internal: 100 shares, Broker: 75 shares
#    -> Update internal to 75, order may still be working

# 2. Stock splits
#    Internal: 10 shares @ $100, Broker: 40 shares @ $25
#    -> Trust broker, update shares and price

# 3. Manual close via broker UI
#    Internal: 50 shares, Broker: 0 shares
#    -> Clear internal state, increment trade_count

# 4. Zero quantity edge case
#    Broker returns qty=0 for recently closed position
#    -> Don't add to tracking, just skip
```

## Testing Checklist
```python
# Verify these scenarios:
1. [ ] Internal 100 shares, broker 100 shares -> No change
2. [ ] Internal 100 shares, broker 50 shares -> Update to 50
3. [ ] Internal 0 shares, broker 100 shares -> Add new position
4. [ ] Internal 100 shares, broker 0 shares -> Clear internal
5. [ ] Internal long, broker short -> Flip side
6. [ ] Broker API fails -> Return unchanged state
7. [ ] Fractional shares (10.5) handled correctly
```

## References
- Alpaca API: `client.get_all_positions()`
- Best practice: Reconcile every 15-60 minutes in production
- Related: Order fill tracking, execution confirmation
