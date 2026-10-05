---
name: syncfusion-vue-stock-chart
description: Comprehensive guide for implementing Syncfusion Stock Chart component in Vue 3 applications. Always use this skill when users mention stock chart, financial data visualization, OHLC series, candlestick charts, technical indicators (EMA, SMA, RSI, MACD, Bollinger Bands), trend lines, range/period selectors, stock market data visualization, Vue Stock Chart component. Trigger immediately for any stock chart related queries, even without explicit component name mention.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Data Visualization - Financial Charts"
---

# Implementing Syncfusion Stock Chart

A comprehensive guide for implementing the Syncfusion Stock Chart component in Vue 3 applications for visualizing financial data with advanced features like technical indicators, trend lines, and interactive controls.

## When to Use This Skill

Use this skill when the user needs to:
- **Set up Stock Chart** in a Vue 3 project with stock/financial data
- **Visualize OHLC data** (Open, High, Low, Close) using candlestick or OHLC series
- **Display volume data** with volume indicators below the main chart
- **Implement technical indicators** - Moving Averages (SMA, EMA), RSI, MACD, Bollinger Bands, ATR, Momentum, Stochastic
- **Add trend lines** to stock chart for technical analysis
- **Create interactive selectors** - Period selector (1D, 1W, 1M, 3M, 6M, 1Y, YTD) and range selector with sliders
- **Handle real-time data** updates and streaming stock prices
- **Configure axes** for DateTime (x-axis) and numeric (y-axis) values
- **Customize appearance** - colors, gradients, themes, responsive sizing
- **Export charts** to PDF, SVG, or print stock charts
- **Ensure accessibility** - WCAG compliance, keyboard navigation, screen readers
- **Troubleshoot** series rendering, data binding, performance issues

## Component Overview

The Syncfusion Stock Chart is specifically designed for financial data visualization with:
- **Series types:** Candlestick, OHLC, Line, Area, Spline Area, HiLo, HiLoOpenClose, Range Area
- **Volume indicator:** Display trading volume below the main chart area
- **20+ Technical Indicators:** EMA, SMA, RSI, MACD, Bollinger Bands, ATR, Momentum, Stochastic, and more
- **Trend lines:** Support for linear, exponential, logarithmic, power, and moving average trend lines
- **Interactive selectors:** Period selector for quick date range selection, range selector with sliders for custom ranges
- **Real-time updates:** Support for streaming and live data updates
- **Export & Print:** Export to PDF/SVG formats and print functionality
- **Accessibility:** Full WCAG compliance with keyboard navigation and screen reader support
- **Responsive design:** Automatic scaling based on container size
- **Themes:** Support for Material, Bootstrap, Fabric, and other Syncfusion themes

## Documentation & Navigation Guide

Refer to the following documentation files based on your specific need:

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup for Stock Chart
- Basic component initialization
- Data structure (OHLC format requirement)
- Simple working example with candle series
- CSS imports and theming

### Series Types & Data Visualization
📄 **Read:** [references/series-types.md](references/series-types.md)
- Candlestick series (most common for stock charts)
- OHLC series (alternative to candlestick)
- Line and area series for trend visualization
- Spline area and range area variants
- HiLo and HiLoOpenClose series
- When to use each series type
- Volume indicator configuration

### Axis Configuration & Customization
📄 **Read:** [references/axis-configuration.md](references/axis-configuration.md)
- DateTime axis setup for time-based data
- Numeric Y-axis configuration
- Axis label formatting (dates, prices)
- Multiple axes for different value ranges
- Grid line customization
- Axis ranges and zooming

### Technical Indicators & Analysis
📄 **Read:** [references/technical-indicators.md](references/technical-indicators.md)
- Exponential Moving Average (EMA)
- Simple Moving Average (SMA)
- Relative Strength Index (RSI)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands for volatility analysis
- Average True Range (ATR)
- Momentum and Stochastic indicators
- Adding multiple indicators simultaneously

### Trend Lines & Styling
📄 **Read:** [references/trend-lines-styling.md](references/trend-lines-styling.md)
- Adding trend lines to stock charts
- Trend line types (Linear, Exponential, Logarithmic, Power, Moving Average)
- Gradient fills for visual enhancement
- Series color and appearance customization
- Theme integration and CSS variables
- Custom styling with CSS classes

### Interactive Features & Selection
📄 **Read:** [references/interactive-features.md](references/interactive-features.md)
- Period selectors (1D, 1W, 1M, 3M, 6M, 1Y, YTD buttons)
- Range selector with slider controls
- Crosshair for data point inspection
- Trackball for multi-series tracking
- Tooltips and legends configuration
- Stock market events and annotations

### Data Binding & Real-Time Updates
📄 **Read:** [references/data-binding-events.md](references/data-binding-events.md)
- Data binding patterns (static JSON, API calls)
- Working with live/streaming data
- Event handling and callbacks
- Real-time price updates
- Performance optimization for large datasets

### Export, Print & Accessibility
📄 **Read:** [references/export-accessibility.md](references/export-accessibility.md)
- Export to PDF format
- Export to SVG format
- Print functionality
- WCAG accessibility compliance
- Keyboard navigation (Tab, Arrow keys)
- Screen reader support (ARIA labels)
- Color contrast and visual indicators

### Advanced Customization & Performance
📄 **Read:** [references/advanced-customization.md](references/advanced-customization.md)
- Volume indicator configuration
- Custom styling with CSS
- Responsive design patterns
- Performance optimization techniques
- Lazy loading and virtualization
- Theme customization and CSS variables

## Quick Start Example

```vue
<template>
  <div id="app">
    <ejs-stockchart
      id="stockchart-container"
      :primaryXAxis="primaryXAxis"
      :primaryYAxis="primaryYAxis"
      :title="title"
      :tooltip="tooltip"
    >
      <e-stockchart-series-collection>
        <e-stockchart-series
          :dataSource="chartData"
          type="Candle"
          xName="date"
          open="open"
          high="high"
          low="low"
          close="close"
        />
      </e-stockchart-series-collection>
    </ejs-stockchart>
  </div>
</template>

<script setup>
import { provide } from 'vue'
import {
  StockChartComponent as EjsStockchart,
  StockChartSeriesCollectionDirective as EStockchartSeriesCollection,
  StockChartSeriesDirective as EStockchartSeries,
  DateTime,
  CandleSeries,
  RangeTooltip,
  Tooltip
} from '@syncfusion/ej2-vue-charts'

const chartData = [
  { date: new Date('2024-01-01'), open: 100, high: 105, low: 98, close: 102 },
  { date: new Date('2024-01-02'), open: 102, high: 108, low: 101, close: 106 },
  { date: new Date('2024-01-03'), open: 106, high: 110, low: 104, close: 108 }
]

const primaryXAxis = {
  valueType: 'DateTime',
  majorGridLines: { color: 'transparent' }
}

const primaryYAxis = {
  majorTickLines: { color: 'transparent', width: 0 }
}

const title = 'Stock Chart'

const tooltip = {
  enable: true,
  shared: true
}

provide('stockChart', [DateTime, CandleSeries, RangeTooltip, Tooltip])
</script>
```

## Common Patterns

**Pattern 1: Display multiple series with volume**
- Use Candle series for OHLC data
- Add separate Line/Column series for volume
- Configure two Y-axes: one for price, one for volume

**Pattern 2: Add technical analysis indicators**
- Include EMA or SMA for trend identification
- Add RSI or Bollinger Bands for momentum analysis
- Combine multiple indicators on same chart

**Pattern 3: Interactive date range selection**
- Use Period Selector for preset ranges (1M, 3M, 1Y)
- Use Range Selector with slider for custom date ranges
- Bind range changes to update displayed data

**Pattern 4: Real-time data updates**
- Initialize chart with historical data
- Use events to append new data points
- Set data update interval for live streaming

## Key Props & Configuration

| Prop | Type | Purpose |
|------|------|---------|
| `dataSource` | Array | OHLC data points |
| `type` | String | Series type (Candle, OHLC, Line, Area) |
| `xName` | String | Property name for X-axis (usually 'date') |
| `open`, `high`, `low`, `close` | String | Property names for OHLC values |
| `volume` | String | Property name for volume data |
| `valueType` | String | X-axis type (DateTime for stock charts) |
| `periods` | Object | Configuration for period selector buttons |
| `tooltip` | Object | Tooltip settings |
| `crosshair` | Object | Crosshair configuration |
| `indicators` | Array | Array of indicator configurations |
| `trendlines` | Array | Array of trend line configurations |

## Common Use Cases

1. **Stock Market Dashboard** - Display real-time stock prices with technical indicators
2. **Financial Analysis Tool** - Interactive chart with multiple indicators for technical analysis
3. **Price History Viewer** - Historical stock data with period selection
4. **Cryptocurrency Tracker** - Real-time crypto price visualization with volume
5. **Forex Charts** - Currency pair visualization with trend analysis
6. **Commodity Prices** - Oil, gold, commodity price tracking
7. **Portfolio Performance** - Multiple stocks comparison on single chart

## Next Steps

1. Install `@syncfusion/ej2-vue-charts` package
2. Read [getting-started.md](references/getting-started.md) for initial setup
3. Choose appropriate series type from [series-types.md](references/series-types.md)
4. Configure axes in [axis-configuration.md](references/axis-configuration.md)
5. Add technical indicators from [technical-indicators.md](references/technical-indicators.md) if needed
6. Customize appearance in [trend-lines-styling.md](references/trend-lines-styling.md)
7. Add interactive features from [interactive-features.md](references/interactive-features.md)
