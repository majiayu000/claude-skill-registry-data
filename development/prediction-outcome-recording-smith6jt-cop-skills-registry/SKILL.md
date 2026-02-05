---
name: prediction-outcome-recording
description: "Record prediction outcomes when positions close. Trigger when: (1) predictions logged but outcomes missing, (2) calculating prediction accuracy, (3) tracking model performance."
author: Claude Code
date: 2024-12-29
---

# Prediction Outcome Recording Pattern

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-29 |
| **Goal** | Complete the prediction lifecycle by recording outcomes when positions close |
| **Environment** | live_trader.py, prediction_metrics.py, db_manager.py |
| **Status** | Success |

## Context

The system was logging predictions when positions opened but never recording outcomes when positions closed. This broke:
- Accuracy calculations (no outcomes to compare against)
- Model evaluation (can't measure prediction quality)
- Retraining decisions (no performance data)

**Root cause**: Predictions were being made and logged, but no code existed to update them with actual results.

## Verified Workflow

### 1. Track prediction_id in Position State

```python
# In PositionState dataclass or equivalent
@dataclass
class PositionState:
    symbol: str
    entry_price: float
    entry_time: datetime
    prediction_id: Optional[int] = None  # Track the prediction
    # ... other fields
```

### 2. Store prediction_id When Opening Position

```python
# When logging prediction and opening position
prediction_id = prediction_tracker.log_prediction(
    symbol=symbol,
    timeframe=timeframe,
    predicted_direction=signal,
    predicted_magnitude=magnitude,
    confidence=confidence,
    model_version=model_version,
    regime=regime,
    entry_price=entry_price,
)

# Store in position state
position_state.prediction_id = prediction_id
```

### 3. Record Outcome at ALL Exit Points

There are typically 3 exit paths that ALL need outcome recording:

**Exit Point 1: Stop-Loss / Take-Profit**
```python
# After stop-loss or take-profit triggers
if state.prediction_id is not None:
    actual_magnitude = (exit_price - state.entry_price) / state.entry_price
    actual_direction = 1 if actual_magnitude > 0.001 else (-1 if actual_magnitude < -0.001 else 0)

    prediction_tracker.db.update_prediction_outcome(
        prediction_id=state.prediction_id,
        actual_direction=actual_direction,
        actual_magnitude=actual_magnitude,
        final_price=exit_price
    )
```

**Exit Point 2: Signal-Based Flatten**
```python
# When signal goes to 0/HOLD and position is flattened
if state.prediction_id is not None:
    actual_magnitude = (exit_price - state.entry_price) / state.entry_price
    actual_direction = 1 if actual_magnitude > 0.001 else (-1 if actual_magnitude < -0.001 else 0)

    prediction_tracker.db.update_prediction_outcome(
        prediction_id=state.prediction_id,
        actual_direction=actual_direction,
        actual_magnitude=actual_magnitude,
        final_price=exit_price
    )
```

**Exit Point 3: Reverse Signal Close**
```python
# When signal reverses (long -> short or vice versa)
if state.prediction_id is not None:
    actual_magnitude = (exit_price - state.entry_price) / state.entry_price
    actual_direction = 1 if actual_magnitude > 0.001 else (-1 if actual_magnitude < -0.001 else 0)

    prediction_tracker.db.update_prediction_outcome(
        prediction_id=state.prediction_id,
        actual_direction=actual_direction,
        actual_magnitude=actual_magnitude,
        final_price=exit_price
    )
```

### 4. Pass prediction_tracker to Functions

```python
def decide_and_trade_optimized(
    symbol: str,
    df: pd.DataFrame,
    state: PositionState,
    prediction_tracker: Optional[PredictionTracker] = None,  # ADD THIS
    # ... other params
) -> Tuple[int, float, str]:
    ...
```

### 5. Direction Calculation

```python
# Threshold for direction: must be > 0.1% to count as up/down
def calculate_direction(actual_magnitude: float) -> int:
    if actual_magnitude > 0.001:    # > 0.1% up
        return 1
    elif actual_magnitude < -0.001: # < -0.1% down
        return -1
    else:
        return 0  # Neutral
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Recording outcome only at one exit point | Missed 2 of 3 exit paths | ALL exit paths need outcome recording |
| Using raw price difference for magnitude | Values inconsistent | Use percentage: (exit - entry) / entry |
| Direction threshold of 0 | Too many neutral classifications | Use 0.1% threshold for meaningful moves |
| Not checking if prediction_id exists | AttributeError on None | Always check `if state.prediction_id is not None` |
| Global prediction_tracker variable | Threading issues | Pass as function parameter |

## Final Parameters

```yaml
# Direction thresholds
up_threshold: 0.001    # > 0.1% = direction 1
down_threshold: -0.001 # < -0.1% = direction -1
neutral: 0             # otherwise

# Outcome fields
actual_direction: int    # -1, 0, 1
actual_magnitude: float  # % change (e.g., 0.025 = 2.5%)
final_price: float       # Exit price
directional_correct: int # 1 if predicted == actual, else 0
magnitude_error: float   # abs(predicted_mag - actual_mag)
```

## Key Insights

- **Track prediction_id in position state**: Essential for correlating entries to exits
- **Cover ALL exit paths**: Stop-loss, take-profit, signal flatten, signal reverse
- **Guard against None**: Always check prediction_id before recording
- **Use percentages**: Magnitude as % change, not absolute price difference
- **0.1% threshold**: Avoid classifying tiny moves as directional

## Verification Query

```sql
-- Check if outcomes are being recorded
SELECT
    DATE(p.timestamp, 'unixepoch') as date,
    COUNT(p.id) as predictions,
    COUNT(o.prediction_id) as outcomes,
    ROUND(100.0 * COUNT(o.prediction_id) / COUNT(p.id), 1) as outcome_pct
FROM predictions p
LEFT JOIN prediction_outcomes o ON p.id = o.prediction_id
WHERE p.timestamp > strftime('%s', 'now') - 7*86400
GROUP BY DATE(p.timestamp, 'unixepoch')
ORDER BY date DESC;
```

## References
- `scripts/live_trader.py`: Lines 1395-1404, 1469-1478, 1546-1555 (exit points)
- `alpaca_trading/evaluation/prediction_metrics.py`: PredictionTracker class
- `alpaca_trading/data/db_manager.py`: update_prediction_outcome()
