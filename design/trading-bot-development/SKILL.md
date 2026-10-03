---
name: trading-bot-development
description: Develop, extend, and maintain the Meridian 10-layer trading bot. Covers indicators, strategies, risk, learning, portfolio, resilience, and UI.
---

# Trading Bot Development Skill

## Domain Knowledge

This is a 10-layer autonomous crypto trading platform (Meridian) with:
- Paper-first safety model (no live trading by default)
- Operator-gated learning (L6 bounded activation)
- Immutable risk gates (L7)
- React operator console (13 screens)
- Python backend with HTTP API

## Architecture Layers

| Layer | Module | Purpose | Key Files |
|-------|--------|---------|-----------|
| L1 | `app/market/` | Data collection, orderbook, indicators | `candles.py`, `orderbook.py` |
| L2 | `app/market/candles.py` | 17 technical indicators | `_add_indicators()` |
| L3 | `app/market/orderbook.py`, `app/l3_microstructure_depth.py` | Microstructure | `snapshot()`, `build_microstructure_signals()` |
| L4 | `app/strategies/`, `app/l4_signal_quality.py` | Signal generation | `breakout.py`, `ema_pullback.py`, `mean_reversion.py` |
| L5 | `app/ai/`, `app/l5_ai_context.py` | AI advisory | `openai_service.py`, `build_ai_context_package()` |
| L6 | `app/learning/bounded_activation.py` | Bounded learning | `BoundedLearningActivator` |
| L7 | `app/risk/` | Risk management | `manager.py`, `position_sizer.py` |
| L8 | `app/l8_correlation_aware_allocation.py` | Portfolio | `CorrelationAwareAllocator` |
| L9 | `app/l9_operational_resilience.py` | Resilience | `OperationalResilience` |
| L10 | `app/ui/operator-console/` | Dashboard | 13 React screens |

## Development Rules

1. **Never bypass risk gates** — L7 is immutable
2. **Paper trading only** — EXECUTION_ADAPTER=paper is default
3. **L6 requires operator approval** — No autonomous live changes
4. **Extend, don't redesign** — Prefer minimal diffs
5. **Maintain observability** — All changes must be traceable
6. **Bilingual UI** — TR/EN aligned for operator text

## Build Commands

```bash
# Backend validation
python -m compileall app
python -m app.autonomous_research_loop --cycles=2 --delay-seconds=1

# Frontend build
cd app/ui/operator-console && npm run build

# Quality gate
powershell -ExecutionPolicy Bypass -File scripts/run_quality_gate.ps1

# Safe run
powershell -ExecutionPolicy Bypass -File scripts/run_safe.ps1
```

## Common Patterns

### Adding a new indicator
Edit `app/market/candles.py` → `_add_indicators()` method → add computation method

### Adding a new signal
Create `app/strategies/<name>.py` → implement `evaluate()` → register in pipeline

### Adding a UI panel
Create component in `src/components/<screen>/` → import in screen → add CSS

### Adding an API endpoint
Add method to `OperatorPanelService` → add route in `do_GET`/`do_POST`

## Testing

- Always run `npm run build` after UI changes
- Always run `python -m compileall app` after Python changes
- Test with `--cycles=2` for quick validation
- Check operator panel at `http://127.0.0.1:8765`

## Indicator Reference

### Trend Family
- `ema_fast` (span=10), `ema_slow` (span=21), `ema_gap_pct`

### Momentum Family
- `rsi` (period=14), `stochastic_k` (period=14)

### Volatility Family
- `atr` (period=14), `atr_pct`, `bb_mid`, `bb_width`, `bb_position`

### Volume Family
- `obv`, `volume_ma` (window=20), `volume_ratio`

### Structure Family
- `rolling_high` (window=20), `rolling_low` (window=20), `price_range`

### Divergence Family
- `macd` (12,26,9), `macd_signal`, `macd_histogram`

## Risk Gates (L7)

All must pass for trade execution:
- Account balance check
- Daily loss cap
- Position loss cap
- Max concurrent trades
- Anti-overtrading limit
- Strategy exposure cap
- Regime exposure cap
- Total exposure cap
- Rolling week loss (optional)

## UI Message System

### Severity Tones
- `info` — Blue, informational
- `success` — Green, action completed
- `warning` — Yellow, needs attention
- `error` — Red, action failed

### Message Structure
```typescript
{
  tone: "info" | "success" | "warning" | "error";
  title: string;
  detail: string;
  remediation?: string;  // Recommended action
  persistent?: boolean;  // Auto-dismiss or stay
}
```

### Component
- `MessageBanner` — Professional banner with icon, title, detail, remediation
- Located in `src/components/shared/MessageBanner.tsx`

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Build fails | TypeScript errors | Run `npm run build` for details |
| Import error | Missing module | Check file exists and path |
| 409 Conflict | Runtime already running | Use pause/resume/stop |
| Timeout | Service slow | Wait for next refresh cycle |
| Risk blocked | Gate failed | Check risk context in logs |
3. **L6 requires operator approval** — No autonomous live changes
4. **Extend, don't redesign** — Prefer minimal diffs
5. **Maintain observability** — All changes must be traceable
6. **Bilingual UI** — TR/EN aligned for operator text

## Build Commands

```bash
# Backend validation
python -m compileall app
python -m app.autonomous_research_loop --cycles=2 --delay-seconds=1

# Frontend build
cd app/ui/operator-console && npm run build

# Quality gate
powershell -ExecutionPolicy Bypass -File scripts/run_quality_gate.ps1

# Safe run
powershell -ExecutionPolicy Bypass -File scripts/run_safe.ps1
```

## Common Patterns

### Adding a new indicator
Edit `app/market/candles.py` → `_add_indicators()` method → add computation method

### Adding a new signal
Create `app/strategies/<name>.py` → implement `evaluate()` → register in pipeline

### Adding a UI panel
Create component in `src/components/<screen>/` → import in screen → add CSS

### Adding an API endpoint
Add method to `OperatorPanelService` → add route in `do_GET`/`do_POST`

## Testing

- Always run `npm run build` after UI changes
- Always run `python -m compileall app` after Python changes
- Test with `--cycles=2` for quick validation
- Check operator panel at `http://127.0.0.1:8765`
