---
name: finance-charts
description: |
  Financial data collection and visualization using TradingView lightweight-charts.
  Fetches market data from trusted sources and renders interactive charts.
  
  USE WHEN user says "create chart", "visualize stock data", "show price chart",
  "fetch market data", "display financial chart", "chart [ticker]", "plot [asset]",
  or any request related to financial data visualization and charting.
location: user
---

# Finance Charts

**Financial Data Visualization System**

## Workflow Routing (SYSTEM PROMPT)

**CRITICAL: This section MUST be FIRST and route EVERY workflow.**

**When user requests fetching financial data:**
Examples: "fetch stock data", "get market data for AAPL", "retrieve price data", "download financial data", "pull data for BTC"
→ **READ:** ~/.claude/skills/finance-charts/workflows/fetch-data.md
→ **EXECUTE:** Fetch financial data from trusted source (Yahoo Finance, Alpha Vantage, or Coinbase)

**When user requests creating a chart:**
Examples: "create chart", "visualize data", "plot price chart", "show chart for TSLA", "chart this data", "display chart"
→ **READ:** ~/.claude/skills/finance-charts/workflows/create-chart.md
→ **EXECUTE:** Generate interactive TradingView lightweight-charts visualization

**When user requests updating chart data:**
Examples: "update chart", "refresh data", "update prices", "reload chart data", "sync latest data"
→ **READ:** ~/.claude/skills/finance-charts/workflows/update-data.md
→ **EXECUTE:** Refresh data and update existing chart

**When user requests exporting chart:**
Examples: "export chart", "save chart data", "download chart", "export to CSV", "save visualization"
→ **READ:** ~/.claude/skills/finance-charts/workflows/export-chart.md
→ **EXECUTE:** Export chart data or visualization to specified format

---

## When to Activate This Skill

### Direct Finance Chart Requests (Categories 1-4)
- "finance charts", "financial charts", "market charts", "trading charts"
- "do finance chart", "run finance chart", "create finance chart", "generate finance chart"
- "quick chart", "simple chart", "basic chart", "comprehensive chart", "full chart"
- "chart for [ticker]", "chart on [asset]", "chart about [market]"

### Data Visualization (Categories 5-7)
- "visualize stock", "visualize crypto", "visualize market data", "visualize prices"
- "show price chart", "display chart", "plot data", "graph prices"
- "financial visualization", "market visualization", "trading visualization"
- "candlestick chart", "line chart", "OHLC chart", "area chart"

### Financial Data Collection (Category 8)
- "fetch market data", "get stock prices", "retrieve financial data", "download market data"
- "pull data from [source]", "collect price data", "gather market info"
- Ticker symbols: "AAPL", "TSLA", "BTC-USD", "ETH-USD", etc.
- Asset requests: "chart Bitcoin", "show Apple stock", "Tesla prices"

### TradingView Integration
- "use TradingView charts", "lightweight charts", "TradingView visualization"
- "interactive chart", "web-based chart", "browser chart"

---

## Core Capabilities

**What this skill provides:**
- **Data Collection**: Fetch OHLCV (Open, High, Low, Close, Volume) data from trusted financial APIs
- **Chart Rendering**: Create interactive charts using TradingView lightweight-charts library
- **Multiple Chart Types**: Candlestick, line, area, histogram (volume), baseline charts
- **Real-time Updates**: Refresh data and update charts dynamically
- **Export Options**: Save data to CSV, JSON, or export chart as image
- **Multi-Asset Support**: Stocks, crypto, forex, commodities, indices

---

## Workflow Overview

**Data Collection**
- **fetch-data.md** - Retrieve financial data from Yahoo Finance, Alpha Vantage, or Coinbase API

**Visualization**
- **create-chart.md** - Generate TradingView lightweight-charts visualization with fetched data
- **update-data.md** - Refresh data and synchronize chart in real-time

**Export & Storage**
- **export-chart.md** - Export chart data or save visualization to file

---

## Extended Context

### Trusted Data Sources

**1. Yahoo Finance (via yfinance Python library)**
- Free, no API key required
- Stocks, ETFs, indices, forex, crypto
- Historical and recent data
- Limitations: Rate limiting, unofficial API

**2. Alpha Vantage**
- Free tier available (5 API calls/minute, 500 calls/day)
- Requires API key (stored in ~/.claude/.env)
- Stock, forex, crypto, technical indicators
- Official API with good documentation

**3. Coinbase API**
- Free, no authentication for public data
- Cryptocurrency market data
- Real-time and historical OHLCV
- Official exchange API

**4. Polygon.io**
- Premium service with free tier
- High-quality financial data
- Stocks, options, forex, crypto
- Requires API key

**Configuration:**
```bash
# Add to ~/.claude/.env
ALPHA_VANTAGE_API_KEY=your_key_here
POLYGON_API_KEY=your_key_here
```

### TradingView Lightweight Charts

**Library:** https://github.com/tradingview/lightweight-charts

**Features:**
- Lightweight and performant (no dependencies)
- Multiple chart types (candlestick, line, area, histogram, baseline)
- Interactive (zoom, pan, crosshair, tooltips)
- Responsive and mobile-friendly
- Customizable appearance and behavior

**Installation:**
```bash
# Via bun (preferred)
cd ~/.claude/skills/finance-charts/tools/chart-app
bun add lightweight-charts

# Or via npm/yarn
npm install lightweight-charts
```

**Basic Usage:**
```typescript
import { createChart } from 'lightweight-charts';

const chart = createChart(document.body, {
  width: 800,
  height: 400,
  layout: {
    background: { color: '#ffffff' },
    textColor: '#333',
  },
  grid: {
    vertLines: { color: '#e1e1e1' },
    horzLines: { color: '#e1e1e1' },
  },
});

const candlestickSeries = chart.addCandlestickSeries({
  upColor: '#26a69a',
  downColor: '#ef5350',
  borderVisible: false,
  wickUpColor: '#26a69a',
  wickDownColor: '#ef5350',
});

candlestickSeries.setData([
  { time: '2023-01-01', open: 100, high: 105, low: 98, close: 103 },
  { time: '2023-01-02', open: 103, high: 110, low: 102, close: 108 },
  // ... more data
]);
```

### Chart Application Structure

**Location:** `~/.claude/skills/finance-charts/tools/chart-app/`

**Files:**
- `index.html` - Chart display page
- `chart.ts` - Chart rendering logic (TypeScript)
- `data-loader.ts` - Data fetching and processing
- `package.json` - Dependencies and scripts
- `tsconfig.json` - TypeScript configuration

**Running the chart app:**
```bash
cd ~/.claude/skills/finance-charts/tools/chart-app
bun run dev    # Development server with hot reload
bun run build  # Production build
bun run serve  # Serve production build
```

### Data Format

**OHLCV Format (required for candlestick charts):**
```json
[
  {
    "time": "2023-01-01",
    "open": 150.00,
    "high": 155.50,
    "low": 149.00,
    "close": 153.25,
    "volume": 1000000
  }
]
```

**Time Format:**
- YYYY-MM-DD for daily data
- Unix timestamp (seconds) for intraday data

### Storage Locations

**Data Cache:**
- `~/.claude/skills/finance-charts/tools/data-cache/` - Cached API responses
- Format: `{ticker}_{interval}_{date}.json`

**Generated Charts:**
- `~/.claude/skills/finance-charts/tools/charts/` - Static HTML chart files
- `~/.claude/context/projects/finance-charts/` - Project-specific charts

**Exports:**
- `~/.claude/scratchpad/` - Temporary exports
- User-specified paths - Custom export locations

---

## Examples

### Example 1: Create Bitcoin Price Chart

**User:** "Create a chart for Bitcoin"

**Skill Response:**
1. Routes to `fetch-data.md` → Fetches BTC-USD data from Coinbase API (last 30 days)
2. Routes to `create-chart.md` → Generates TradingView candlestick chart
3. Opens chart in browser at `http://localhost:3000`
4. Outcome: Interactive Bitcoin price chart with candlesticks and volume

### Example 2: Visualize Apple Stock with Custom Range

**User:** "Show me AAPL stock chart for the last 3 months"

**Skill Response:**
1. Routes to `fetch-data.md` → Fetches AAPL data via yfinance (3-month range)
2. Routes to `create-chart.md` → Creates candlestick chart with MA overlays
3. Saves chart to `~/.claude/skills/finance-charts/tools/charts/AAPL_3M.html`
4. Outcome: Apple stock visualization with moving averages

### Example 3: Update Existing Chart

**User:** "Update the Tesla chart with latest data"

**Skill Response:**
1. Routes to `update-data.md` → Fetches latest TSLA data
2. Updates existing chart data without recreating
3. Chart auto-refreshes in browser
4. Outcome: Chart synchronized with current market data

### Example 4: Export Chart Data

**User:** "Export the BTC chart data to CSV"

**Skill Response:**
1. Routes to `export-chart.md` → Extracts data from chart state
2. Converts to CSV format with headers
3. Saves to `~/.claude/scratchpad/BTC_data_2025-11-19.csv`
4. Outcome: CSV file ready for spreadsheet analysis

---

## Stack & Tools

**Languages:**
- TypeScript (preferred for chart app)
- Python (for data fetching with yfinance)
- JavaScript (alternative)

**Key Dependencies:**
- `lightweight-charts` - Chart rendering library
- `yfinance` (Python) or `yahoo-finance2` (Node) - Free market data
- `node-fetch` or `axios` - HTTP requests
- `bun` - Runtime and package manager

**Development Server:**
- Bun's built-in dev server (recommended)
- Or Vite for hot module replacement

---

## Related Documentation

- `~/.claude/skills/CORE/SKILL-STRUCTURE-AND-ROUTING.md` - Canonical structure guide
- `~/.claude/skills/CORE/CONSTITUTION.md` - CLI-First principles
- `~/.claude/skills/CORE/stack-preferences.md` - TypeScript > Python preference
- `~/.claude/skills/finance-charts/documentation/data-sources.md` - Detailed API documentation
- `~/.claude/skills/finance-charts/documentation/chart-customization.md` - Chart styling and options

---

**Created:** 2025-11-19
**Last Updated:** 2025-11-19
**Archetype:** Standard (4 workflows)
**Status:** Active
