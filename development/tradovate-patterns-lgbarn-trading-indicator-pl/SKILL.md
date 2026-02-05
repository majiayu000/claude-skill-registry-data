---
name: tradovate-patterns
description: Tradovate JavaScript indicator scaffold and patterns. Provides class structure and export guidance. Use when developing Tradovate indicators.
---

# Tradovate Patterns

Lightweight scaffold for Tradovate JavaScript indicator development.

## File Conventions

- File naming: `*LB.js` or `*ProLB.js`
- Tags: Must include "Luther Barnum"

## Dependencies

```javascript
const predef = require("./tools/predef");
const meta = require("./tools/meta");
const { ParamType } = meta;
```

## Class Structure

```javascript
class IndicatorName {
    init() {
        // One-time initialization
        this.cumulativeValue = 0;
    }

    map(d, i, history) {
        // d = current bar { open, high, low, close, volume, timestamp }
        // i = bar index
        // history = historical data access

        const result = {};
        result.plotName = calculatedValue;
        return result;
    }

    filter() {
        // Optional validation
        return true;
    }
}
```

## Export Pattern

```javascript
module.exports = {
    name: "indicator-name",
    description: "Description of indicator",
    calculator: IndicatorName,
    params: {
        period: predef.paramSpecs.period(14),
        multiplier: {
            type: ParamType.NUMBER,
            def: 1.0,
            step: 0.1,
            min: 0.1,
            max: 10.0
        }
    },
    plots: {
        value: { title: "Value" },
        upperBand: { title: "Upper Band" }
    },
    inputType: meta.InputType.BARS,
    tags: ["Luther Barnum", "vwap", "trading"],
    schemeStyles: {
        dark: {
            value: predef.styles.plot({ color: "#00FF00" })
        }
    }
};
```

## Session Types

Access via `this.props.type`:
- `"chart"` - Reset per trading day
- `"session"` - Reset at specific time
- `"rolling"` - Reset per N-bar window

## History Access

```javascript
// Previous bar
const prevBar = history.prior();

// Specific historical bar
const bar = history.get(i - 5);

// Direct array access
const data = history.data[i];
```

## Session Detection

```javascript
map(d, i, history) {
    const tradeDate = d.tradeDate();

    if (tradeDate !== this.lastTradeDate) {
        // New session - reset values
        this.cumulativeValue = 0;
        this.lastTradeDate = tradeDate;
    }
}
```

## Helper Functions

```javascript
function number(defValue, step, min, max) {
    return { type: ParamType.NUMBER, def: defValue, step, min, max };
}
```

## Complete Example

Reference: `/Users/lgbarn/Personal/Indicators/Tradovate/LRBMACD.js`

```javascript
const predef = require("./tools/predef");
const meta = require("./tools/meta");
const SMA = require("./tools/SMA");

class SimpleMACD {
    init() {
        this.fastSMA = SMA(this.props.fast);
        this.slowSMA = SMA(this.props.slow);
        this.signalSMA = SMA(this.props.signal);
    }

    map(d, i) {
        const value = d.value();
        const macd = this.fastSMA(value) - this.slowSMA(value);

        let signal;
        let histogram;

        if (i >= this.props.slow - 1) {
            signal = this.signalSMA(macd);
            histogram = macd - signal;
        }

        return { macd, signal, histogram, zero: 0 };
    }

    filter(d) {
        return predef.filters.isNumber(d.histogram);
    }
}

module.exports = {
    name: "simple-macd-lb",
    description: "Simple MACD Indicator",
    calculator: SimpleMACD,
    params: {
        fast: predef.paramSpecs.period(3),
        slow: predef.paramSpecs.period(10),
        signal: predef.paramSpecs.period(16)
    },
    validate(obj) {
        if (obj.slow < obj.fast) {
            return meta.error("slow", "Slow must be >= fast");
        }
    },
    inputType: meta.InputType.BARS,
    plots: {
        macd: { title: "MACD" },
        signal: { title: "Signal" },
        histogram: { title: "Histogram" },
        zero: { displayOnly: true }
    },
    tags: ["Luther Barnum", predef.tags.Oscillators],
    schemeStyles: {
        dark: {
            macd: predef.styles.plot("#FFA500"),
            signal: predef.styles.plot("#0000FF"),
            histogram: predef.styles.plot("#FF3300"),
            zero: predef.styles.plot({ color: "#B5BAC2", lineStyle: 3 })
        }
    }
};
```

## VWAP Calculation Pattern

```javascript
class SessionVWAP {
    init() {
        this.cumVolume = 0;
        this.cumVwap = 0;
        this.cumVwap2 = 0;
        this.lastTradeDate = null;
    }

    map(d, i, history) {
        const currentDate = d.tradeDate();

        // Reset on new session
        if (currentDate !== this.lastTradeDate) {
            this.cumVolume = 0;
            this.cumVwap = 0;
            this.cumVwap2 = 0;
            this.lastTradeDate = currentDate;
        }

        const typicalPrice = (d.high() + d.low() + d.close()) / 3;
        const volume = d.volume();

        this.cumVolume += volume;
        this.cumVwap += volume * typicalPrice;
        this.cumVwap2 += volume * typicalPrice * typicalPrice;

        if (this.cumVolume === 0) {
            return { vwap: undefined, upper: undefined, lower: undefined };
        }

        const vwap = this.cumVwap / this.cumVolume;
        const variance = (this.cumVwap2 / this.cumVolume) - (vwap * vwap);
        const stdev = variance > 0 ? Math.sqrt(variance) : 0;

        return {
            vwap,
            upper: vwap + stdev,
            lower: vwap - stdev
        };
    }
}
```

## Error Handling Patterns

### Validation function
```javascript
validate(obj) {
    if (obj.period < 1) {
        return meta.error("period", "Period must be >= 1");
    }
    if (obj.slow <= obj.fast) {
        return meta.error("slow", "Slow must be greater than fast");
    }
}
```

### Check history in map()
```javascript
map(d, i, history) {
    // Not enough history
    if (i < this.props.period - 1) {
        return { value: undefined };
    }

    // Check previous bar exists
    const prev = history.prior();
    if (!prev) {
        return { value: undefined };
    }
}
```

### Safe division
```javascript
const divisor = d.high() - d.low();
const result = divisor === 0 ? 0 : (d.close() - d.low()) / divisor;
```

### Filter invalid data
```javascript
filter(d) {
    return predef.filters.isNumber(d.value);
}

// Or multiple checks
filter(d) {
    return predef.filters.isNumber(d.value) &&
           predef.filters.isNumber(d.signal);
}
```

### Undefined checks
```javascript
map(d, i, history) {
    const prev = history.prior();
    const prevClose = prev ? prev.close() : d.close();
}
```

## Trading Context

- Focus: /ES, /NQ futures
- Timeframe: 5-minute
- Key concepts: VWAP, Session detection, Cumulative calculations
- Location: `/Users/lgbarn/Personal/Indicators/Tradovate/`

## Documentation Sources

Use WebSearch to find Tradovate indicator documentation:
- Tradovate Community Forum (community.tradovate.com)
- Tradovate Indicator API examples
