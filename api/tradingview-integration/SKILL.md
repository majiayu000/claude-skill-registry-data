---
name: tradingview-integration
description: TradingView Integration Engineer — Institutional capability and runbook for tradingview-integration.
---

# SKILL: TradingView Integration Engineer
## Domain: Charting Library, Custom Data Feeds, Broker Integration

**Activation triggers:** TradingView chart, custom data feed, OHLCV bars,
chart widget, symbol search, order markers, Lightweight Charts, charting
configuration.

---

## Two Charting Approaches

```
Option A: TradingView Lightweight Charts (open-source, self-hosted)
  → Use when: custom charts, full control, no licensing cost
  → Package: @tradingview/lightweight-charts
  → Best for: imJournal equity curve, imCopying PnL charts

Option B: TradingView Advanced Charts Widget (commercial license required)
  → Use when: professional trading terminal, full order book, DOM
  → Requires: valid TradingView Advanced Charts license
  → Best for: imCharts main trading terminal
```

---

## Lightweight Charts — Equity Curve

```typescript
// components/EquityCurveChart.tsx
import { createChart, ColorType, LineData } from '@tradingview/lightweight-charts';
import { useEffect, useRef } from 'react';

interface EquityCurveChartProps {
  data: Array<{ time: string; value: number }>;
  height?: number;
}

export function EquityCurveChart({ data, height = 300 }: EquityCurveChartProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const chart = createChart(containerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: 'transparent' },
        textColor: '#9ca3af',
      },
      grid: {
        vertLines: { color: 'rgba(31, 41, 55, 0.5)' },
        horzLines: { color: 'rgba(31, 41, 55, 0.5)' },
      },
      width: containerRef.current.clientWidth,
      height,
      rightPriceScale: { borderColor: '#1f2937' },
      timeScale: { borderColor: '#1f2937', timeVisible: true },
    });

    const lineSeries = chart.addLineSeries({
      color: '#00d4ff',
      lineWidth: 2,
      crosshairMarkerVisible: true,
      priceFormat: { type: 'price', precision: 2, minMove: 0.01 },
    });

    lineSeries.setData(data);
    chart.timeScale().fitContent();

    const handleResize = () => {
      if (containerRef.current) {
        chart.applyOptions({ width: containerRef.current.clientWidth });
      }
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, [data, height]);

  return <div ref={containerRef} className="w-full" style={{ height }} />;
}
```

---

## Lightweight Charts — Candlestick with Volume

```typescript
// components/CandlestickChart.tsx
import { createChart, CandlestickData, HistogramData } from '@tradingview/lightweight-charts';

export function CandlestickChart({ candles, volumes }: CandlestickChartProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const chart = createChart(containerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: 'transparent' },
        textColor: '#9ca3af',
      },
      width: containerRef.current.clientWidth,
      height: 400,
    });

    const candleSeries = chart.addCandlestickSeries({
      upColor: '#22c55e',
      downColor: '#ef4444',
      borderUpColor: '#22c55e',
      borderDownColor: '#ef4444',
      wickUpColor: '#22c55e',
      wickDownColor: '#ef4444',
    });
    candleSeries.setData(candles);

    const volumeSeries = chart.addHistogramSeries({
      color: '#26a69a',
      priceFormat: { type: 'volume' },
      priceScaleId: 'volume',
    });
    chart.priceScale('volume').applyOptions({
      scaleMargins: { top: 0.8, bottom: 0 },
    });
    volumeSeries.setData(volumes);

    chart.timeScale().fitContent();

    return () => chart.remove();
  }, [candles, volumes]);

  return <div ref={containerRef} className="w-full" />;
}
```

---

## OHLCV Data Feed (Backend)

```python
# app/api/v1/endpoints/imcharts.py
# Serves OHLCV bars — consumed by TradingView chart widget

from fastapi import APIRouter, Query
from app.services.market_data import MarketDataService

router = APIRouter()

@router.get("/imcharts/bars/{symbol}")
async def get_bars(
    symbol: str,
    resolution: str = Query("D", description="1, 5, 15, 60, D, W, M"),
    from_ts: int = Query(..., description="Unix timestamp"),
    to_ts: int = Query(..., description="Unix timestamp"),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user),
):
    service = MarketDataService(db)
    bars = await service.get_ohlcv(
        symbol=symbol.upper(),
        resolution=resolution,
        from_ts=from_ts,
        to_ts=to_ts,
    )
    return {
        "s": "ok",
        "t": [b.time for b in bars],
        "o": [b.open for b in bars],
        "h": [b.high for b in bars],
        "l": [b.low for b in bars],
        "c": [b.close for b in bars],
        "v": [b.volume for b in bars],
    }

@router.get("/imcharts/symbols/{symbol}")
async def search_symbol(
    symbol: str,
    current_user: User = Depends(get_current_active_user),
):
    """Symbol info for TradingView datafeed."""
    return {
        "name": symbol,
        "full_name": symbol,
        "description": f"{symbol} — Integral Market",
        "type": "forex",
        "session": "0000-2359",
        "timezone": "Etc/UTC",
        "ticker": symbol,
        "minmov": 1,
        "pricescale": 100000,
        "has_intraday": True,
        "has_daily": True,
        "supported_resolutions": ["1", "5", "15", "30", "60", "240", "D", "W", "M"],
    }
```

---

## Trade Markers on Chart

```typescript
// Mark executed trades on the equity curve / candlestick chart
function addTradeMarkers(series: ISeriesApi<'Candlestick'>, trades: Trade[]) {
  const markers: SeriesMarker<Time>[] = trades.map(trade => ({
    time: Math.floor(new Date(trade.opened_at).getTime() / 1000) as Time,
    position: trade.direction === 'buy' ? 'belowBar' : 'aboveBar',
    color: trade.direction === 'buy' ? '#22c55e' : '#ef4444',
    shape: trade.direction === 'buy' ? 'arrowUp' : 'arrowDown',
    text: `${trade.direction.toUpperCase()} ${trade.volume}`,
  }));
  series.setMarkers(markers);
}
```

---

## Symbol Watchlist Data Feed

```typescript
// hooks/useSymbolPrice.ts — real-time price for watchlist symbols
export function useSymbolPrice(symbol: string) {
  const [price, setPrice] = useState<SymbolPrice | null>(null);
  const { subscribe } = useExpertWS();

  // Subscribe to live price updates
  useEffect(() => {
    return subscribe(`market.prices.${symbol}`, (data) => {
      setPrice(data as SymbolPrice);
    });
  }, [symbol, subscribe]);

  // Initial price from REST while WS connects
  const { data: initialPrice } = useQuery({
    queryKey: ['price', symbol],
    queryFn: () => expertApi.get(`/imcharts/price/${symbol}`).then(r => r.data),
    staleTime: 5_000,
    enabled: !price,  // stop polling once WS delivers data
  });

  return price ?? initialPrice ?? null;
}
```

---

## Anti-Patterns

```
✗ Using TradingView Advanced Charts without a valid license
✗ Creating a new chart instance on every re-render (heavy — create once, update data)
✗ Fetching full OHLCV history in one request (paginate by date range)
✗ Missing chart cleanup on unmount (chart.remove() must be called)
✗ Symbol names not normalized (always .toUpperCase())
✗ Not handling no-data response from bars endpoint (return { s: "no_data" })
✗ Blocking requests with chart load — fetch data first, render loading skeleton
✗ Fixed chart width (always respond to container resize)
```
