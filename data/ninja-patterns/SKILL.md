---
name: ninja-patterns
description: NinjaTrader 8 NinjaScript indicator scaffold and patterns. Provides C# structure guidance and triggers doc-researcher for API verification. Use when developing NinjaTrader indicators.
---

# NinjaScript Patterns

Lightweight scaffold for NinjaTrader 8 NinjaScript/C# indicator development.

## Before Generating Code

ALWAYS use doc-researcher agent or Ref MCP tools to verify:
- NinjaTrader 8 API methods
- Property attribute usage
- Drawing object APIs

## File Conventions

- File naming: `*LB.cs`
- Author: `// Author: Luther Barnum`

## Namespace & Class

```csharp
namespace NinjaTrader.NinjaScript.Indicators.LB
{
    public class [Name]LB : Indicator
    {
        // Implementation
    }
}
```

## Lifecycle Methods

### OnStateChange()
```csharp
protected override void OnStateChange()
{
    if (State == State.SetDefaults)
    {
        Description = "Indicator description";
        Name = "IndicatorName";
        // Set property defaults
    }
    else if (State == State.Configure)
    {
        AddPlot(Brushes.Blue, "PlotName");
    }
    else if (State == State.DataLoaded)
    {
        // Initialize Series objects
    }
}
```

### OnBarUpdate()
```csharp
protected override void OnBarUpdate()
{
    if (CurrentBar < BarsRequiredToPlot) return;
    // Calculations
}
```

## Property Attributes

```csharp
[NinjaScriptProperty]
[Display(Name = "Period", Order = 1, GroupName = "Parameters")]
[Range(1, int.MaxValue)]
public int Period { get; set; }
```

## Session Detection

```csharp
if (Bars.IsFirstBarOfSession)
{
    // Reset session values
}
```

## Series Objects

```csharp
private Series<double> myValues;

// In State.DataLoaded:
myValues = new Series<double>(this);
```

## Drawing Objects

```csharp
Draw.Rectangle(this, "tag", startBar, startPrice, endBar, endPrice, Brushes.Blue);
Draw.Line(this, "tag", startBar, startPrice, endBar, endPrice, Brushes.Red);
Draw.Text(this, "tag", "Label", 0, High[0] + TickSize, Brushes.White);
```

## Complete Example

Reference: `/Users/lgbarn/Personal/Indicators/Ninjatrader/PEMA.cs`

```csharp
#region Using declarations
using System;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.Windows.Media;
using NinjaTrader.Gui.Chart;
using NinjaTrader.NinjaScript.DrawingTools;
#endregion

// Author: Luther Barnum

namespace NinjaTrader.NinjaScript.Indicators.LB
{
    public class SimpleMALB : Indicator
    {
        private EMA fastEma;
        private SMA slowSma;

        protected override void OnStateChange()
        {
            if (State == State.SetDefaults)
            {
                Description = "Simple MA Crossover Indicator";
                Name = "SimpleMALB";
                Calculate = Calculate.OnBarClose;
                IsOverlay = true;

                // Default parameters
                FastPeriod = 9;
                SlowPeriod = 21;

                // Add plots
                AddPlot(Brushes.Cyan, "FastMA");
                AddPlot(Brushes.Orange, "SlowMA");

                Plots[0].Width = 2;
                Plots[1].Width = 2;
            }
            else if (State == State.DataLoaded)
            {
                fastEma = EMA(Close, FastPeriod);
                slowSma = SMA(Close, SlowPeriod);
            }
        }

        protected override void OnBarUpdate()
        {
            if (CurrentBar < SlowPeriod)
                return;

            FastMA[0] = fastEma[0];
            SlowMA[0] = slowSma[0];
        }

        #region Properties
        [NinjaScriptProperty]
        [Range(1, int.MaxValue)]
        [Display(Name = "Fast Period", Order = 1, GroupName = "Parameters")]
        public int FastPeriod { get; set; }

        [NinjaScriptProperty]
        [Range(1, int.MaxValue)]
        [Display(Name = "Slow Period", Order = 2, GroupName = "Parameters")]
        public int SlowPeriod { get; set; }

        [Browsable(false)]
        [XmlIgnore]
        public Series<double> FastMA { get { return Values[0]; } }

        [Browsable(false)]
        [XmlIgnore]
        public Series<double> SlowMA { get { return Values[1]; } }
        #endregion
    }
}
```

## VWAP Calculation Pattern

```csharp
private double cumVolume;
private double cumVwap;
private double cumVwap2;

protected override void OnBarUpdate()
{
    if (Bars.IsFirstBarOfSession)
    {
        cumVolume = 0;
        cumVwap = 0;
        cumVwap2 = 0;
    }

    double typicalPrice = (High[0] + Low[0] + Close[0]) / 3.0;
    cumVolume += Volume[0];
    cumVwap += Volume[0] * typicalPrice;
    cumVwap2 += Volume[0] * typicalPrice * typicalPrice;

    if (cumVolume > 0)
    {
        double vwap = cumVwap / cumVolume;
        double variance = (cumVwap2 / cumVolume) - (vwap * vwap);
        double stdev = variance > 0 ? Math.Sqrt(variance) : 0;

        VWAP[0] = vwap;
        UpperBand[0] = vwap + stdev;
        LowerBand[0] = vwap - stdev;
    }
}
```

## Error Handling Patterns

### Check bar history
```csharp
protected override void OnBarUpdate()
{
    // Ensure enough bars for calculation
    if (CurrentBar < BarsRequiredToPlot)
        return;

    // Or use specific period
    if (CurrentBar < Period - 1)
        return;
}
```

### Null/zero checks
```csharp
// Safe division
double divisor = High[0] - Low[0];
double result = divisor != 0 ? (Close[0] - Low[0]) / divisor : 0.5;

// Check indicator values
if (myIndicator[0] != 0 && !double.IsNaN(myIndicator[0]))
{
    // Safe to use
}
```

### Validate parameters
```csharp
if (State == State.SetDefaults)
{
    // Use [Range] attribute for validation
}
else if (State == State.Configure)
{
    // Additional validation
    if (SlowPeriod <= FastPeriod)
        SlowPeriod = FastPeriod + 1;
}
```

### Historical data access
```csharp
// Safe access to previous bars
if (CurrentBar >= barsAgo)
{
    double previousValue = Close[barsAgo];
}
```

## Trading Context

- Focus: /ES, /NQ futures
- Timeframe: 5-minute
- Key concepts: VWAP+bands, IB, Pivots
- Location: `/Users/lgbarn/Personal/Indicators/Ninjatrader/`

## Documentation Sources

Use Ref MCP to search:
- NinjaTrader 8 Help Guide
- NinjaScript Reference
