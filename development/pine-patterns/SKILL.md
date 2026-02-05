---
name: pine-patterns
description: Pine Script v5/v6 indicator scaffold and patterns. Provides structure guidance and triggers doc-researcher for current syntax verification. Use when developing TradingView indicators.
---

# Pine Script Patterns

Lightweight scaffold for Pine Script v5/v6 indicator development.

## Before Generating Code

ALWAYS use doc-researcher agent or Ref MCP tools to verify:
- Current function signatures
- v5 vs v6 syntax differences
- Deprecated functions

## File Conventions

- Version header: `//@version=6` (prefer v6)
- License: Mozilla Public License 2.0
- File naming: `LB_*.pine`
- Author: Luther Barnum

## Input Group Structure

Standard groups (use `group=` parameter):
```
"Feature Toggles"     - Master enable/disable switches
"VWAP Settings"       - VWAP configuration
"VWAP Bands"          - Standard deviation band settings
"Session Settings"    - Time-based parameters
"Initial Balance"     - IB configuration
"Opening Range"       - OR settings
"Pivot Points"        - Pivot configuration
"Display Options"     - Visual settings
"Colors"              - Color configuration
```

## Session Defaults

- RTH: 9:30 AM - 4:00 PM ET
- Timezone: America/New_York
- Detection: `time(timeframe.period, sessionString)`

## Resource Limits

Set appropriately:
- `max_bars_back` - Historical data access
- `max_labels_count` - Label objects (default 500)
- `max_lines_count` - Line objects (default 500)

## Complete Example

Reference: `/Users/lgbarn/Personal/Indicators/Tradingview/LB_RH_MAs.pine`

```pinescript
//@version=6
// This Pine Script® code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © lgbarn

indicator('LB Simple MA Crossover', shorttitle='LB_MACross', overlay=true)

// === INPUTS ===
fastLength = input.int(9, "Fast MA Length", minval=1, group="MA Settings")
slowLength = input.int(21, "Slow MA Length", minval=1, group="MA Settings")
useLightTheme = input.bool(false, "Light Theme", group="Display")

// === CALCULATIONS ===
fastMA = ta.ema(close, fastLength)
slowMA = ta.sma(close, slowLength)

// === COLORS ===
fastColor = useLightTheme ? color.new(#0000FF, 0) : color.new(#00FFFF, 0)
slowColor = useLightTheme ? color.new(#FF0000, 0) : color.new(#FF6600, 0)

// === PLOTS ===
plot(fastMA, title="Fast MA", color=fastColor, linewidth=2)
plot(slowMA, title="Slow MA", color=slowColor, linewidth=2)
```

## Key Patterns

### Persistent State (Session Reset)
```pinescript
var float cumulativeValue = 0.0
var float sessionHigh = na
var float sessionLow = na

if ta.change(time("D")) != 0
    cumulativeValue := 0.0
    sessionHigh := high
    sessionLow := low
```

### Session Detection
```pinescript
// Check if in RTH session
isSessionTime = time(timeframe.period, "0930-1600:23456")

// Detect new session start
isNewSession = ta.change(time("D")) != 0

// Session with timezone
isRTH = not na(time(timeframe.period, "0930-1600", "America/New_York"))
```

### Theme Colors
```pinescript
useLightTheme = input.bool(false, "Light Theme", group="Display")
lineColor = useLightTheme ? color.new(#000000, 0) : color.lime
fillColor = useLightTheme ? color.new(#000000, 90) : color.new(color.lime, 90)
```

### VWAP Calculation Pattern
```pinescript
var float cumVolume = 0.0
var float cumVwap = 0.0
var float cumVwap2 = 0.0

if isNewSession
    cumVolume := 0.0
    cumVwap := 0.0
    cumVwap2 := 0.0

cumVolume += volume
cumVwap += volume * hlc3
cumVwap2 += volume * hlc3 * hlc3

vwapValue = cumVolume > 0 ? cumVwap / cumVolume : na
variance = cumVolume > 0 ? cumVwap2 / cumVolume - vwapValue * vwapValue : na
stdev = variance > 0 ? math.sqrt(variance) : na

upperBand = vwapValue + stdev
lowerBand = vwapValue - stdev
```

### Moving Average Patterns
```pinescript
// Simple Moving Average
smaValue = ta.sma(close, length)

// Exponential Moving Average
emaValue = ta.ema(close, length)

// Weighted Moving Average
wmaValue = ta.wma(close, length)

// Hull Moving Average
hmaValue = ta.hma(close, length)
```

## Error Handling Patterns

### Check for NA values
```pinescript
// Use nz() to replace NA with default
safeValue = nz(calculatedValue, 0.0)

// Check if value is valid before use
if not na(vwapValue)
    plot(vwapValue, color=color.blue)
```

### Validate inputs
```pinescript
// Ensure slow > fast
validatedSlow = math.max(slowLength, fastLength + 1)
```

### Handle division by zero
```pinescript
divisor = high - low
result = divisor != 0 ? (close - low) / divisor : 0.5
```

### Check bar history
```pinescript
// Ensure enough bars for calculation
if bar_index >= length - 1
    // Safe to calculate
    value = ta.sma(close, length)
```

### Runtime errors (v6)
```pinescript
if period < 1
    runtime.error("Period must be >= 1")
```

## Trading Context

- Focus: /ES, /NQ futures
- Timeframe: 5-minute
- Key concepts: VWAP+1SD, TWAP, IB, Classic Pivots
- Approach: Institutional over retail patterns

## External Libraries

Available imports:
- `import jmosullivan/SessionVolumeProfile/12 as SVP`
- `import jmosullivan/Session/5 as Session`

## Documentation Sources

Use Ref MCP to search:
- TradingView Pine Script Reference
- Pine Script User Manual
